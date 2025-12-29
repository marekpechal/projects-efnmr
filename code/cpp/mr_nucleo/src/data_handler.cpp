#include <cstdint>
#include "data_handler.h"
#include "pico/time.h"
#include <cwchar>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>

DataHandler::DataHandler() : is_multi_echo(false) {
}

bool DataHandler::save_data(const std::vector<uint16_t>& data, const std::string& filename) {
    std::string actual_filename = filename;
    if (actual_filename.empty()) {
        std::stringstream ss;
        ss << "nmr_data_" << std::fixed << std::setprecision(3) << get_absolute_time() << ".json";
        actual_filename = ss.str();
    }
    
    current_single_data = data;
    is_multi_echo = false;
    
    std::ofstream file(actual_filename);
    if (!file.is_open()) {
        std::cerr << "Could not open file: " << actual_filename << std::endl;
        return false;
    }
    
    file << "{\n";
    file << "  \"timestamp\": " << get_absolute_time() << ",\n";
    file << "  \"data\": [";
    
    for (size_t i = 0; i < data.size(); ++i) {
        file << data[i];
        if (i < data.size() - 1) {
            file << ", ";
        }
    }
    
    file << "]\n";
    file << "}\n";
    file.close();
    
    std::cout << "Data saved to " << actual_filename << std::endl;
    return true;
}

bool DataHandler::save_data(const std::vector<std::vector<uint16_t>>& data, const std::string& filename) {
    std::string actual_filename = filename;
    if (actual_filename.empty()) {
        std::stringstream ss;
        ss << "nmr_data_" << std::fixed << std::setprecision(3) << get_absolute_time() << ".json";
        actual_filename = ss.str();
    }
    
    current_multi_data = data;
    is_multi_echo = true;
    
    std::ofstream file(actual_filename);
    if (!file.is_open()) {
        std::cerr << "Could not open file: " << actual_filename << std::endl;
        return false;
    }
    
    file << "{\n";
    file << "  \"timestamp\": " << get_absolute_time() << ",\n";
    file << "  \"data\": [\n";
    
    for (size_t i = 0; i < data.size(); ++i) {
        file << "    [";
        for (size_t j = 0; j < data[i].size(); ++j) {
            file << data[i][j];
            if (j < data[i].size() - 1) {
                file << ", ";
            }
        }
        file << "]";
        if (i < data.size() - 1) {
            file << ",";
        }
        file << "\n";
    }
    
    file << "  ]\n";
    file << "}\n";
    file.close();
    
    std::cout << "Data saved to " << actual_filename << std::endl;
    return true;
}

void DataHandler::send_data_serial(const std::vector<uint16_t>& data, int max_points) {
    std::cout << "Serial data transfer:" << std::endl;
    std::cout << "Data: [";
    
    int points_to_show = std::min(max_points, static_cast<int>(data.size()));
    for (int i = 0; i < points_to_show; ++i) {
        std::cout << data[i];
        if (i < points_to_show - 1) {
            std::cout << ", ";
        }
    }
    
    if (points_to_show < static_cast<int>(data.size())) {
        std::cout << "...";
    }
    
    std::cout << "]" << std::endl;
}

void DataHandler::send_data_serial(const std::vector<std::vector<uint16_t>>& data, int max_points) {
    std::cout << "Serial data transfer:" << std::endl;
    
    int echoes_to_show = std::min(3, static_cast<int>(data.size()));
    for (int i = 0; i < echoes_to_show; ++i) {
        std::cout << "Echo " << (i + 1) << ": [";
        
        int points_to_show = std::min(10, static_cast<int>(data[i].size()));
        for (int j = 0; j < points_to_show; ++j) {
            std::cout << data[i][j];
            if (j < points_to_show - 1) {
                std::cout << ", ";
            }
        }
        
        if (points_to_show < static_cast<int>(data[i].size())) {
            std::cout << "...";
        }
        
        std::cout << "]" << std::endl;
    }
}
