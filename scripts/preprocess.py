# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "docling[vlm]>=2.127.0",
#     "tqdm>=4.70.1",
# ]
# ///

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    PictureDescriptionVlmOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.base import ImageRefMode
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@dataclass
class Args:
    read_dir: Path
    save_dir: Path
    vlm_repo_id: str
    vlm_prompt: str

    @classmethod
    def from_namespace(cls, ns: argparse.Namespace) -> "Args":
        return cls(
            read_dir=ns.read_dir,
            save_dir=ns.save_dir,
            vlm_repo_id=ns.vlm_repo_id,
            vlm_prompt=ns.vlm_prompt,
        )


def _init_converter(repo_id: str, prompt: str) -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_picture_description = True
    pipeline_options.do_formula_enrichment = True
    pipeline_options.picture_description_options = PictureDescriptionVlmOptions(
        repo_id=repo_id, prompt=prompt
    )
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_picture_images = True
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )
    logger.info("Converter: %s", converter)

    return converter


def preprocess():
    args = _parse_args()
    rdir = args.read_dir
    sdir = args.save_dir
    logger.info("Creating %s if it doesn't exist", args.save_dir)
    sdir.mkdir(parents=True, exist_ok=True)

    converter = _init_converter(args.vlm_repo_id, args.vlm_prompt)

    logger.info("Reading PDFs from %s", rdir)
    for item in tqdm(rdir.iterdir(), desc="Converting"):
        if item.suffix.lower() != ".pdf":
            logger.info("Skipping non-PDF file %s", item)
            continue

        save_file = sdir / (item.stem + ".md")
        doc = converter.convert(item).document

        logger.info("Saving to %s", save_file)
        doc.save_as_markdown(filename=save_file, image_mode=ImageRefMode.REFERENCED)


def _parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description=(
            "Converts PDF files in a given directory to markdown using the `docling` "
            "package. Performs image annotations along with formula enrichments."
        )
    )
    parser.add_argument(
        "read_dir", type=Path, help="Directory containing PDF files for preprocessing."
    )
    parser.add_argument(
        "--save-dir",
        type=Path,
        default=Path("data").resolve(),
        help=(
            "Directory to save processed files to. "
            "Will create a directory in the CWD by default."
        ),
    )
    parser.add_argument(
        "--vlm-repo-id",
        type=str,
        default="Qwen/Qwen3-VL-2B-Instruct",
        help=(
            "Repo ID for a VLM for image annotations. Should be a HuggingFace repo id."
        ),
    )
    parser.add_argument(
        "--vlm-prompt",
        type=str,
        default="Describe the image in three sentences. Be concise and accurate.",
    )

    args = parser.parse_args()
    return Args.from_namespace(args)


if __name__ == "__main__":
    preprocess()
