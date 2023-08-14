# Serializer and De-Serializer Verilog Code and Simulation Setup Generator

This code generator and simulation setup is specifically developed for Chipathon 2023 Tapeouts for SIPO (Serial in Parallel Out) and PISO (Parallel In Serial Out) functionality in chips. However, it can be used and integrated with any RTL code requiring the such functionality and can be implemented any FPGA or ASIC Development. This guide explains how to use the provided Python code to generate customizable Verilog code for a Serial In Parallel Out (SIPO) and Parallel In Serial Out (PISO) module. Additionally, it covers running simulations to test the generated Verilog code.

### Basic Requirements and Dependencies
Although the code can be generated on both `Windows` and `Linux` using `Python3` but the recomened system for both code generation and simulation is `Linux` following are the dependencies required for `Linux`:

##### For CentOS 7
```bash
# Install make
sudo yum install make
# Install iverilog
sudo yum install iverilog
# Install python3 (Python 3 is already installed by default in CentOS 7)
# To ensure the latest version, you can use the following commands
sudo yum install epel-release
sudo yum install python3
# Install gtkwave
sudo yum install gtkwave
```
##### For Ubuntu
```bash
# Update package list (optional but recommended)
sudo apt update
# Install make
sudo apt install make
# Install iverilog
sudo apt install iverilog
# Install python3 (Python 3 is already installed by default in Ubuntu)
# To ensure the latest version, you can use the following command
sudo apt install python3
# Install gtkwave
sudo apt install gtkwave
```

## Python Code

The Python code in this repository serves as a Verilog code generator. It creates a Verilog module for a SIPO PISO module based on specific configuration parameters. The key parameters that you can customize in the Python code are:

- `READ_DEPTH`: The number of registers for reading data (output from the chip).
- `WRITE_DEPTH`: The number of registers for writing data (input to the chip).
- `REG_WIDTH`: The number of bits in each register.

By modifying these parameters, you can tailor the generated Verilog module to match your requirements.

### Generating Verilog Code

Follow these steps to generate Verilog code using the provided Python script:

1. Clone the repository using: 
   ```bash
   git clone https://github.com/muhammadusman7/serdes_chipathon_2023.git
   ```
2. Change directory to `serdes_chipathon_2023` using:
   ```bash
   cd serdes_chipathon_2023
   ```
3. Before code generation you can modify the parameters in the python code `code_generator.py` on `LINE 7, 8, and 9` as mentioned in Purpose of the Python Code using `READ_DEPTH`, `WRITE_DEPTH`, and `REG_WIDTH` using your favorite text editor:
   ```bash
   # e.g. Using Gedit
   gedit ./python/code_generator.py
   ```
   Here's the code snippet from the Python script for clarity:

    ```python
    # Configuration parameters for generating Verilog code, it generates 8 Registers for Reading, 8 for Writing, each having 8-bit.
    ...
    READ_DEPTH = 8     # No of registers for reading data (Output from chip)
    WRITE_DEPTH = 8    # No of registers for writing data (Input to chip)
    REG_WIDTH = 8      # Number of bits in each register
    ...
    ```
4. Run the Python script `serdes_chipathon_2023/python/code_generator.py` (it generates Verilog codes in `serdes_chipathon_2023/rtl` directory) using the following command:
   ```bash
   python3 ./python/code_generator.py
   ```
5. Running the Python script will generate the Verilog RTL and Testbench code with specified configuration in step 3 in the `/serdes_chipathon_2023/rtl` directory.

You can regenerate the Verilog codes with changed configuration if required, by repeating `Step 3` to `Step 5`.

## Running the Simulation
Once you have generated the Verilog code using the Python script, you can run simulations to test the behavior of the SIPO PISO module with your chosen configuration. Here are the steps to run the simulation:

Use the generated Verilog RTL (sipo_piso_slave.v) along with testbench file (sipo_piso_slave_tb.v) and the provided simulation setup (Makefile) in the repository.
The provided Makefile supports two simulation options: Cadence Incisive/Xcelium and Iverilog. Choose the appropriate option based on your simulation tool.
Here are the commands to run simulations:

- For simulation go to `simulation` directory and run make command with appropriate options as described below:
  ```bash
  cd ./simulation
  ```
    For Cadence Incisive/Xcelium:
    ```bash
    make sim_inc
    ```
    For Cadence Iverilog:
    ```bash
    make sim_iv # Or run only (make) command
    ```
- Makefile `make` has the following options: `help`, `clean`, `sim_inc`, and `sim_iv`. You can use the `make help` for potential use of each option.

### Conclusion
Observe the simulation results to verify the functionality of the SIPO PISO module with the chosen configuration. By following above steps, you can generate Verilog code and simulate the SIPO PISO module with custom parameters.