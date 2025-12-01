// Simple example C++ file for dependency analysis
#include <iostream>
#include <vector>
#include <string>
#include "utils.h"
#include "config.h"

int main() {
    std::vector<std::string> items = {"apple", "banana", "cherry"};
    
    for (const auto& item : items) {
        std::cout << "Item: " << item << std::endl;
    }
    
    Utils::printMessage("Hello from main!");
    Config::load("config.ini");
    
    return 0;
}

