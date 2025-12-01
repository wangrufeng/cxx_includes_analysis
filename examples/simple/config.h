#ifndef CONFIG_H
#define CONFIG_H

#include <string>
#include <map>
#include <fstream>
#include "utils.h"

class Config {
private:
    static std::map<std::string, std::string> settings;
    
public:
    static void load(const std::string& filename) {
        Utils::printMessage("Loading config from: " + filename);
        // Config loading logic here
    }
    
    static std::string get(const std::string& key) {
        return settings[key];
    }
};

#endif // CONFIG_H

