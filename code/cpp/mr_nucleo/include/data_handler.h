#pragma once

#include <cstdint>
#include <vector>
#include <string>

class DataHandler {
public:
    DataHandler();
    
    bool save_data(const std::vector<uint16_t>& data, const std::string& filename = "");
    bool save_data(const std::vector<std::vector<uint16_t>>& data, const std::string& filename = "");
    void send_data_serial(const std::vector<uint16_t>& data, int max_points = 100);
    void send_data_serial(const std::vector<std::vector<uint16_t>>& data, int max_points = 100);
    
private:
    std::vector<uint16_t> current_single_data;
    std::vector<std::vector<uint16_t>> current_multi_data;
    bool is_multi_echo;
};
