#pragma once

#include "hardware.h"
#include "config.h"
#include <vector>
#include <cstdint>

class PulseSequence {
public:
    PulseSequence(NMRHardware& hardware);
    
    void pulse_90_degrees(float duration_ms);
    void pulse_180_degrees(float duration_ms);
    std::vector<uint16_t> acquire_data(int num_points);
    std::vector<uint16_t> spin_echo(float echo_time_ms = 10.0f, float pulse_90_duration_ms = 1.25f);
    std::vector<std::vector<uint16_t>> cpmg(int num_echoes = 16, float echo_time_ms = 10.0f, float pulse_90_duration_ms = 1.25f);

    
private:
    NMRHardware& hw;
    std::vector<uint16_t> data_buffer;
};
