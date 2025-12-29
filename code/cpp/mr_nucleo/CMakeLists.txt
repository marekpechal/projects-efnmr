# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================
set(PICO_BOARD pico2 CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(mr_nucleo C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(mr_nucleo 
    main.cpp
    src/hardware.cpp
    src/data_handler.cpp
    src/pulse_sequences.cpp
)

pico_set_program_name(mr_nucleo "mr_nucleo")
pico_set_program_version(mr_nucleo "0.1")

# Modify the below lines to enable/disable output over UART/USB
pico_enable_stdio_uart(mr_nucleo 0)
pico_enable_stdio_usb(mr_nucleo 1)

# Add the standard include files to the build
target_include_directories(mr_nucleo PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/include
        ${CMAKE_CURRENT_LIST_DIR}
)

target_include_directories(mr_nucleo PRIVATE
        ${CMAKE_CURRENT_LIST_DIR}/include
)

# Add any user requested libraries
target_link_libraries(mr_nucleo 
        hardware_gpio
        hardware_adc
        hardware_timer
        hardware_clocks
        pico_stdlib # stdlib
        )

# pico needs a .uf2 file
pico_add_extra_outputs(mr_nucleo)

