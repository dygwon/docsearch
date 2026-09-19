#include <iostream>
#include <string>


int main(int argc, char* argv[]) {

  if (argc != 2) {
    std::cout << "Invalid usage: " << "./docsearch PATH/TO/DIRECTORY" << std::endl;
    return 1;
  }

  std::string dir { argv[1] };
  std::cout << "Received directory: " << dir << std::endl;

  return 0;
}
