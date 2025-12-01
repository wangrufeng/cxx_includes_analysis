#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <iostream>

class Utils {
public:
    static void printMessage(const std::string& msg) {
        std::cout << "[Utils] " << msg << std::endl;
    }
};

#endif // UTILS_H

