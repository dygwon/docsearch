# docsearch

Search local document contents using BM25.

## Build & Run

```bash
mkdir build && cd build
cmake ..
cmake --build .
./docsearch
```

## Preprocessing

For PDFs, the project has a helper script available to convert all PDF files in
a given directory to a markdown file. The script is written as a `uv` script.
If not using `uv`, please install the dependencies specified in the `/// script`
block prior to running the script.

```bash
uv run --script scripts/preprocess.py READ_DIR --save-dir SAVE_DIR
```
