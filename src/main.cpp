#include <filesystem>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>


/* Steps to build an inverted index
 * 1. collect the documents to be indexed
 * 2. tokenize the text, turning each document into a list of tokens
 * 3. linguistic preprocessing to normalize tokens, which are the indexing terms
 * 4. index documents that each term occurs in by creating an inverted index, consisting of a dictionary and postings
 * */

std::vector<std::string> split_file(const std::string& file) {
  std::ifstream in(file);
  if (!in) throw std::runtime_error("cannot open " + file);
  std::vector<std::string> contents;
  for (std::string tok; in >> tok;)
    contents.push_back(std::move(tok));
  return contents;
}

// use simple whitespace-delimited strings and tokens for now
// later: stem, remove stop words, and deal with case sensitivity

// how are we going to keep track of documents in a way we can refer back to them?
// how can I make it easier to take any set of documents, index them, and search over them
// can I make sure an agent can use the search feature as well?

namespace fs = std::filesystem;
int main(int argc, char* argv[]) {
  if (argc != 2) {
    std::cout << "Invalid usage: " << "./docsearch PATH/TO/DIRECTORY" << std::endl;
    return 1;
  }

  std::string dir{argv[1]};
  std::cout << "Received directory: " << dir << std::endl;

  std::vector<std::string> files;
  for (const auto& entry : fs::directory_iterator(dir)) {
    if (entry.is_regular_file() && entry.path().extension() == ".md") {
      files.push_back(entry.path());
    }
  }

  // for (std::string file : files) {
  //   std::cout << file << '\n';
  // }

  std::vector<std::string> contents = split_file(files[0]);

  for (std::string tok : contents) {
    std::cout << tok << '\n';
  }
  std::cout << std::endl;

  return 0;
}
