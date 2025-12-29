#include "pulse_sequences.h"
#include "pico/time.h"
#include <cstdint>
#include <iostream>
#include <stdexcept>

PulseSequence::PulseSequence(NMRHardware& hardware) 
    : hw(hardware), data_buffer(Config::BUFFER_SIZE, 0) {
}

void PulseSequence::pulse_90_degrees(float duration_ms) {
    int half_cycle_us = static_cast<int>(500000 / Config::NMR_FREQUENCY);
    int num_cycles = static_cast<int>((duration_ms * 1000) / (2 * half_cycle_us));
    
    hw.switch_to_transmit();
    
    // Generate phase-coherent audio frequency pulse
    for (int i = 0; i < num_cycles; ++i) {
        hw.set_tx_positive(true);
        hw.set_tx_negative(false);
        sleep_us(half_cycle_us);
        
        hw.set_tx_positive(false);
        hw.set_tx_negative(true);
        sleep_us(half_cycle_us);
    }
    
    hw.set_tx_positive(false);
    hw.set_tx_negative(false);
    hw.switch_to_receive();
    
    sleep_ms(static_cast<int>(Config::DEAD_TIME * 1000));  // switching transients decay
}

void PulseSequence::pulse_180_degrees(float duration_ms) {
    // Apply a 180 degree pulse (twice the 90 degree pulse)
    pulse_90_degrees(duration_ms * 2);
}

std::vector<uint16_t> PulseSequence::acquire_data(int num_points) {
    int interval_us = static_cast<int>(1000000 / Config::SAMPLE_RATE);
    int points_to_acquire = std::min(num_points, static_cast<int>(data_buffer.size()));
    
    // Acquire data points
    for (int i = 0; i < points_to_acquire; ++i) {
        data_buffer[i] = hw.read_adc();
        sleep_us(interval_us);
    }
    
    return std::vector<uint16_t>(data_buffer.begin(), data_buffer.begin() + points_to_acquire);
}

std::vector<uint16_t> PulseSequence::spin_echo(float echo_time_ms, float pulse_90_duration_ms) {
    hw.set_polarize(true);
    sleep_ms(static_cast<int>(Config::POLARIZE_TIME * 1000));
    
    hw.turn_off_polarize_adiabatic();
    
    pulse_90_degrees(pulse_90_duration_ms);
    sleep_ms(static_cast<int>(echo_time_ms / 2));
    
    pulse_180_degrees(pulse_90_duration_ms);
    sleep_ms(static_cast<int>(echo_time_ms / 2));
    
    std::vector<uint16_t> data = acquire_data(Config::BUFFER_SIZE);
    return data;
}

std::vector<std::vector<uint16_t>> PulseSequence::cpmg(int num_echoes, float echo_time_ms, float pulse_90_duration_ms) {
    // Store all echoes
    std::vector<std::vector<uint16_t>> all_echoes;
    int points_per_echo = Config::BUFFER_SIZE / num_echoes;
    
    hw.set_polarize(true);
    sleep_ms(static_cast<int>(Config::POLARIZE_TIME * 1000));
    
    hw.turn_off_polarize_adiabatic();
    
    // x-axis
    pulse_90_degrees(pulse_90_duration_ms);
    
    // Acquisition
    for (int i = 0; i < num_echoes; ++i) {
        sleep_ms(static_cast<int>(echo_time_ms / 2));
        
        // y-axis (phase shifted)
        pulse_180_degrees(pulse_90_duration_ms);
        
        sleep_ms(static_cast<int>(echo_time_ms / 2));
        
        std::vector<uint16_t> echo_data = acquire_data(points_per_echo);
        all_echoes.push_back(echo_data);
    }
    
    return all_echoes;
}