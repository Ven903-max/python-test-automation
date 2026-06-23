# Automated Bench Validation Framework

A Python framework I built to automate repetitive bench testing of hardware boards 
using lab instruments over LAN.

## Why I built this

Manual bench testing is slow and inconsistent — setting voltages by hand, reading 
DMM values, writing them down, repeating 50 times. This framework automates that 
entire process. You define your test points, run the script, and get a timestamped 
CSV with pass/fail results.

## What it does

- Connects to lab instruments (PSU, DMM, electronic load) over LAN using PyVISA
- Sweeps through operating points automatically
- Measures voltage, current, and calculates efficiency at each point
- Flags results outside tolerance as FAIL
- Logs everything to a timestamped CSV
- Shuts down instruments safely after testing

## Hardware it works with

Any SCPI-compatible instruments connected over LAN, USB, or GPIB. Tested with 
programmable power supplies and electronic loads.

## How to run

pip install pyvisa pyvisa-py numpy
python src/power_characterization.py

Update the instrument addresses in config/bench_config.example.yaml to match 
your bench setup.

## Note on simulation mode

The repo includes a simulation mode (SIMULATION_MODE = True) that runs without 
real instruments connected — useful for testing the logic or understanding the 
flow before hooking up hardware.

## Safety

Always verify voltage and current limits before enabling instrument outputs. 
Don't run on hardware without checking your wiring first.
