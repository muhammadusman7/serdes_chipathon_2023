# code_generator.py
import os 
import random
import math

READ_DEPTH = 2     # No of registers for reading data (Output from chip)
WRITE_DEPTH = 7    # No of registers for writing data (Input to chip)
REG_WIDTH = 32      # Number of bits in each register

def generate_input_ports(num_ports):
    input_ports = ""
    for i in range(num_ports):
        input_ports += f"\tinput wire [`REG_WIDTH-1:0] rd_{i+1},\t\\\n"
    return input_ports

def generate_input_tb(num_ports):
    input_ports = ""
    for i in range(num_ports):
        input_ports += f"\treg [`REG_WIDTH-1:0] rd_{i+1};\t\\\n"
    return input_ports

def generate_output_ports(num_ports):
    output_ports = ""
    for i in range(num_ports - 1):
        output_ports += f"\toutput reg [`REG_WIDTH-1:0] wr_{i+1},\t\\\n"
    # Add the last port without the backslash
    output_ports += f"\toutput reg [`REG_WIDTH-1:0] wr_{num_ports}\n"
    return output_ports

def generate_output_tb(num_ports):
    output_ports = ""
    for i in range(num_ports - 1):
        output_ports += f"\twire [`REG_WIDTH-1:0] wr_{i+1};\t\\\n"
    # Add the last port without the backslash
    output_ports += f"\twire [`REG_WIDTH-1:0] wr_{num_ports};\n"
    return output_ports

def generate_inst_io(num_ports_in, num_ports_out):
    inst_io = "\t"
    for i in range(num_ports_in):
        inst_io += f" .rd_{i+1}(rd_{i+1}),"
    inst_io += "\t\\\n\t"
    for i in range(num_ports_out - 1):
        inst_io += f" .wr_{i+1}(wr_{i+1}),"
    # Add the last port without the backslash
    inst_io += f" .wr_{num_ports_out}(wr_{num_ports_out})\n"
    return inst_io

def gen_rand_hex_values(MEM_DEPTH, REG_WIDTH):
    ADDR_BITS = math.ceil(math.log2(MEM_DEPTH))
    
    hex_values = []
    for i in range(MEM_DEPTH):
        data_value = random.randint(0, 2 ** REG_WIDTH - 1)
        addr_value = bin(i)[2:]
        if len(addr_value) > ADDR_BITS:
            addr_value = addr_value[-ADDR_BITS:]
        if len(addr_value) < ADDR_BITS:
            addr_value = addr_value.zfill(ADDR_BITS)
        bin_value = bin(data_value)[2:]
        if len(bin_value) > REG_WIDTH:
            bin_value = bin_value[-REG_WIDTH:]
        if len(bin_value) < REG_WIDTH:
            bin_value = bin_value.zfill(REG_WIDTH)
        binary_string = str(addr_value) + str(bin_value)
        decimal_value = int(binary_string, 2)
        hex_string = hex(decimal_value)[2:].upper()
        if len(hex_string) > math.ceil((REG_WIDTH + ADDR_BITS)/4):
            hex_string = hex_string[-(math.ceil((REG_WIDTH + ADDR_BITS)/4)):]
        if len(hex_string) <  math.ceil((REG_WIDTH + ADDR_BITS)/4):
            hex_string = hex_string.zfill(math.ceil((REG_WIDTH + ADDR_BITS)/4))
        hex_string = insert_underscores_from_right(hex_string, 4)
        hex_values.append(hex_string)

    return hex_values

def concatenate_bin_values(bin_value1, bin_value2):
    concatenated_bin = bin_value1 + bin_value2
    return concatenated_bin

def insert_underscores_from_right(input_string, underscore_interval):
    reversed_string = input_string[::-1]  # Reverse the input string
    split_strings = [reversed_string[i:i+underscore_interval] for i in range(0, len(reversed_string), underscore_interval)]
    underscored_string = "_".join(split_strings)[::-1]  # Reverse back and join with underscores
    return underscored_string

def generate_sipo_piso_slave(WRITE_DEPTH, READ_DEPTH, REG_WIDTH):
    MEM_DEPTH = READ_DEPTH + WRITE_DEPTH + 1
    ADDR_BITS = math.ceil(math.log2(MEM_DEPTH))
    file_path = "./python/default.mem"
    data_array = read_default_mem(file_path, WRITE_DEPTH)
    code = ''
    from datetime import datetime
    current_date = datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y")
    inst = ""
    for i in range(READ_DEPTH):
        inst += f" .rd_{i+1}(),"
    for i in range(WRITE_DEPTH - 1):
        inst += f" .wr_{i+1}(),"
    # Add the last port without the backslash
    inst += f" .wr_{WRITE_DEPTH}()"
    
    code += "// Title: SIPO PSIO V 1.0 (No Changelog)\n"
    code += f"// Created: {formatted_date}\n"
    code += "// Updated: \n"
    code += "//---------------------------------------------------------------------------\n"
    code += "// Serial In Parallel Out and Parallel in Serial Out Module\n"
    code += "// \n"
    code += "// Developed by Muhammad Usman (https://github.com/muhammadusman7)\n"
    code += "//---------------------------------------------------------------------------\n\n"
    code += "`timescale 1ns/1ps\n"
    code += "`default_nettype none\n"
    code += "`include \"config.v\"\n\n"
    code += "module sipo_piso (\n"
    code += "    input   wire    clk,\n"
    code += "    input   wire    rst,\n"
    code += "    input   wire    strobe,\n"
    code += "    input   wire    wr_en,\n"
    code += "    input   wire    din,\n"
    code += "    output  reg     dout,\n"
    code += "    output  reg     rw_flag,\n"
    code += "    `IO_PORTS\n"
    code += ");\n\n" 
    code += "    // Instantiate where required as below\n"
    code += f"    // sipo_piso sipo_piso_inst (.clk(), .rst(), .strobe(), .wr_en(), .din(), .dout(), .rw_flag(),{inst});\n\n"
    code += "    localparam ADDR_WIDTH = $clog2(`MEM_DEPTH);\n"
    code += "    localparam SIPO_WIDTH = ADDR_WIDTH + `REG_WIDTH;\n"
    code += "    localparam PISO_WIDTH = SIPO_WIDTH;\n"
    code += "    localparam COUNT_WIDTH = $clog2(SIPO_WIDTH)-1;\n"
    code += "    localparam IDLE = 2'b00;\n"
    code += "    localparam PROCESS = 2'b01;\n"
    code += "    localparam SEND = 2'b10;\n\n"
    code += "    reg     [ADDR_WIDTH:0]      sipo_addr, piso_addr, piso_addr_count;\n"
    code += "    reg     [COUNT_WIDTH:0]     count;\n"
    code += "    reg     [SIPO_WIDTH:0]      sipo_data, discard;\n"
    code += "    reg     [SIPO_WIDTH:0]      sipo_reg;\n"
    for i in range(READ_DEPTH):
        code += f"    reg     [`REG_WIDTH-1:0]     mem_rd{i+1};\n"
    for i in range(WRITE_DEPTH):
        code += f"    reg     [`REG_WIDTH-1:0]     mem_wr{i};\n"
    code += f"    reg     [`REG_WIDTH-1:0]     mem_wr{WRITE_DEPTH};\n"
    code += "    reg     [`REG_WIDTH-1:0]     piso_data;\n"
    code += "    reg     [`REG_WIDTH-1:0]     control_reg;\n"
    code += "    reg     [2:0]               status;\n\n"
    code += "    always @(*) begin\n"
    code += "        control_reg = mem_wr0;\n"
    for i in range (WRITE_DEPTH):
        code += f"        wr_{i+1} = mem_wr{i+1};\n"
    code += "        if(rw_flag && wr_en) begin\n"
    code += "            sipo_addr = sipo_reg[SIPO_WIDTH:`REG_WIDTH];\n"
    code += "            sipo_data = sipo_reg[`REG_WIDTH-1:0];\n"
    code += "        end else begin\n"
    code += "            sipo_addr = 'b0;\n"
    code += "            sipo_data = mem_wr0;\n"
    code += "        end\n"
    code += "        if (status == SEND) begin\n"
    code += "            if(piso_addr < `MEM_DEPTH) begin\n"
    code += "                dout = piso_data[count];\n"
    code += "            end else begin\n"
    code += "                // Address is out of range then send data of the discard which can be any data (useless to read from address out of bound)\n"
    code += "                dout = discard[count];\n"
    code += "            end\n"
    code += "        end else begin\n"
    code += "            dout = 'b0;\n"
    code += "        end\n"
    code += "    end\n\n"
    code += "    always @(posedge clk) begin\n\n"
    code += "        if (rst) begin\n"
    code += "            status <= IDLE;\n"
    code += "            count <= 'b0;\n"
    code += "            sipo_reg <= 'b0;\n"
    code += "            piso_addr <= 'b0;\n"
    code += "            piso_addr_count <= 'b0;\n"
    code += f"            mem_wr0 <= {REG_WIDTH}'h3D1D_2400;\n"
    for i in range(WRITE_DEPTH):
        code += f"            mem_wr{i+1} <= {REG_WIDTH}'b{insert_underscores_from_right(str(data_array[i]), 4)};\n"
        # code += f"            mem_wr{i+1} <= {REG_WIDTH}'h{insert_underscores_from_right(hex(int(str(data_array[i]), 2))[2:].upper(), 4)};\n"
    for i in range(READ_DEPTH):
        code += f"            mem_rd{i+1} <= {REG_WIDTH}'b0;\n"
    code += f"            discard <= {REG_WIDTH}'b0;\n"
    code += "        end else begin\n"
    for i in range(READ_DEPTH):
        code += f"            mem_rd{i+1} <= rd_{i+1};\n"
    code += "            case (status)\n"
    code += "                IDLE: begin\n"
    code += "                    count <= 'b0;\n"
    code += "                    rw_flag <= 1'b0;\n"
    code += "                    piso_addr_count <= 'b0;\n"
    code += "                    if(strobe) begin\n"
    code += "                        status <= PROCESS;  // strobe should be sent for 1 clock cycle to start process\n"
    code += "                    end else begin\n"
    code += "                        status <= IDLE;\n"
    code += "                    end\n"
    code += "                end \n"
    code += "                PROCESS: begin\n"
    code += "                    if (wr_en) begin    // SIPO mode\n"
    code += "                        if (count == SIPO_WIDTH) begin\n"
    code += "                            sipo_reg[count] <= din;\n"
    code += "                            count <= 'b0;\n"
    code += "                            status <= IDLE;\n"
    code += "                            rw_flag <= 1'b1;\n"
    code += "                        end else begin\n"
    code += "                            sipo_reg[count] <= din;\n"
    code += "                            count <= count + 1;\n"
    code += "                            status <= PROCESS;\n"
    code += "                            rw_flag <= 1'b0;\n"
    code += "                        end\n"
    code += "                    end else begin // PISO mode\n"
    code += "                        if(piso_addr_count <= $clog2(`MEM_DEPTH)) begin\n"
    code += "                            piso_addr [piso_addr_count] <= din;\n"
    code += "                            piso_addr_count <= piso_addr_count + 1;\n"
    code += "                            status <= PROCESS;\n"
    code += "                        end else begin\n"
    code += "                            status <= SEND;\n"
    code += "                            rw_flag <= 1'b1;\n"
    code += "                        end\n"
    code += "                    end\n"
    code += "                end\n"
    code += "                SEND: begin\n"
    code += "                    status <= SEND;\n"
    code += "                end\n"
    code += "                default status <= IDLE;\n"
    code += "            endcase\n"
    code += "            case (sipo_addr)\n"
    code += f"                {ADDR_BITS}'d0    : mem_wr0   <= sipo_data;\n"
    for i in range(WRITE_DEPTH):
        code += f"                {ADDR_BITS}'d{i+1}    : mem_wr{i+1}   <= sipo_data;\n"
    code += "                default : discard   <= sipo_data;\n"
    code += "            endcase\n"
    code += "            case (piso_addr)\n"
    for i in range(MEM_DEPTH):
        if(i <= WRITE_DEPTH):
            code += f"                {ADDR_BITS}'d{i}    : piso_data <= mem_wr{i};\n"
        else:
            code += f"                {ADDR_BITS}'d{i}    : piso_data <= mem_rd{i-WRITE_DEPTH};\n"
    code += "                default : discard   <= discard;\n"
    code += "            endcase\n"
    code += "        end\n"
    code += "    end\n\n"
    code += "   always @(negedge clk) begin\n"
    code += "       case (status)\n"
    code += "           PROCESS: begin\n\n"
    code += "               if (~wr_en) begin\n\n"
    code += "                   if(piso_addr_count > $clog2(`MEM_DEPTH)) begin\n\n"
    code += "                       status <= SEND;\n\n"
    code += "                   end\n\n"
    code += "               end\n\n"
    code += "           end\n\n"
    code += "           SEND: begin\n\n"
    code += "               if (count < `REG_WIDTH-1) begin\n\n"
    code += "                   count <= count + 1;\n\n"
    code += "                   status <= SEND;\n\n"
    code += "                   rw_flag <= 1'b1;\n\n"
    code += "               end else begin\n\n"
    code += "                   count <=  'b0;\n\n"
    code += "                   status <= IDLE;\n\n"
    code += "                   rw_flag <= 1'b0;\n\n"
    code += "               end\n\n"
    code += "           end\n\n"
    code += "           default status <= status;\n\n"
    code += "       endcase\n\n"
    code += "   end\n\n"
    code += "endmodule\n\n"
    code += "`default_nettype wire\n"
    return code

def generate_sipo_piso_tb(WRITE_DEPTH, READ_DEPTH, REG_WIDTH):
    MEM_DEPTH = READ_DEPTH + WRITE_DEPTH + 1
    ADDR_BITS = math.ceil(math.log2(MEM_DEPTH))
    code = ''
    hex_values = gen_rand_hex_values(WRITE_DEPTH+1, REG_WIDTH)
    from datetime import datetime
    current_date = datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y")
    
    code += "// Title: SIPO PSIO V 1.0 (No Changelog)\n"
    code += f"// Created: {formatted_date}\n"
    code += "// Updated: \n"
    code += "//---------------------------------------------------------------------------\n"
    code += "// Testbench for Serial In Parallel Out and Parallel in Serial Out Module\n"
    code += "// \n"
    code += "// Developed by Muhammad Usman (https://github.com/muhammadusman7)\n"
    code += "//---------------------------------------------------------------------------\n\n"
    code += "`timescale 1ns/1ps\n"
    code += "`default_nettype none\n"
    code += "`include \"config.v\"\n\n"
    code += "module sipo_piso_tb ();\n\n"
    code += "    localparam ADDR_WIDTH = $clog2(`MEM_DEPTH)-1;\n"
    code += "    localparam SIPO_WIDTH = ADDR_WIDTH + `REG_WIDTH;\n"
    code += "    localparam PISO_WIDTH = SIPO_WIDTH;\n\n"
    code += "    reg     clk;\n"
    code += "    reg     rst;\n"
    code += "    reg     strobe;\n"
    code += "    reg     wr_en;\n"
    code += "    reg     din;\n"
    code += "    wire    dout;\n"
    code += "    wire    rw_flag;\n"
    code += "    `IO_TB\n"
    code += "    integer i, j;\n"
    code += f"    reg     [ADDR_WIDTH + 1 + `REG_WIDTH:0]  mem [`MEM_DEPTH:0];\n"
    code += "    reg     [ADDR_WIDTH + 1 + `REG_WIDTH:0]  mem_read;\n\n"
    code += "    sipo_piso uut (.clk(clk), .rst(rst), .strobe(strobe), .wr_en(wr_en), .din(din), .dout(dout), .rw_flag(rw_flag), `IO_INST);\n\n"
    code += "    initial begin\n"
    for i in range(WRITE_DEPTH):
        code += f"        mem[{i}] = {ADDR_BITS+REG_WIDTH}'h{hex_values[i]};\n"
    code += f"        mem[{WRITE_DEPTH}] = {ADDR_BITS+REG_WIDTH}'h{hex_values[WRITE_DEPTH]};\n"
    code += "        clk = 0; rst = 0; strobe = 0;\n"
    code += "        wr_en = 0; din = 0; mem_read = 'b0;\n"
    for i in range(READ_DEPTH):
        code += f"        rd_{i+1} = $random();\n"
    for i in range(READ_DEPTH):
        code += f"        mem[{WRITE_DEPTH+1+i}] = {{{ADDR_BITS}'d{WRITE_DEPTH+1+i}, rd_{i+1}}};\n"
    code += "        #1  rst = 1;\n"
    code += "        #10 rst = 0;\n"
    code += "    end\n\n"
    code += "    initial begin\n"
    code += "        forever begin\n"
    code += "            #5 clk = ~clk;\n"
    code += "        end\n"
    code += "    end\n\n"
    code += "    initial begin\n"
    code += "        // Writing through SIPO\n"
    code += "        #2; wr_en = 1;\n"
    code += f"        for (i=0; i<{MEM_DEPTH}; i=i+1) begin\n"
    code += "            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;\n"
    code += f"            for (j=0; j<{REG_WIDTH+ADDR_BITS}; j=j+1) begin\n"
    code += "                din = mem[i][j];\n"
    code += "                #10;\n"
    code += "            end\n"
    code += "        end\n"
    code += "        #50 wr_en = 0;\n"
    code += "        // Reading through PISO\n"
    code += f"        for (i=0; i<{MEM_DEPTH}; i=i+1) begin\n"
    code += "            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;\n"
    code += f"            mem_read[{REG_WIDTH+ADDR_BITS-1}:{REG_WIDTH}] = i;\n"
    code += f"            for (j=0; j<{REG_WIDTH+ADDR_BITS}; j=j+1) begin\n"
    code += f"                if (j<{ADDR_BITS}) begin\n"
    code += f"                    din = mem_read[{REG_WIDTH}+j];\n"
    code += "                    #10;\n"
    code += "                end else begin\n"
    code += f"                    mem_read[j-{ADDR_BITS}] = dout;\n"
    code += "                    din = 0;\n"
    code += "                    #10;\n"
    code += "                end\n"
    code += "            end\n"
    code += "            if(mem_read == mem[i]) begin\n"
    code += "                $display (\"Memory Location %d: Successfully written and read\", i);\n"
    code += "            end else begin\n"
    code += "                $display (\"Reading or writing to memory location %d: was failed, Actual: %h, Received: %h\", i, mem[i], mem_read);\n"
    code += "                #10 $finish();\n"
    code += "            end\n"
    code += "        end\n"
    code += "        #1000 $display(\"SIPO and PISO have successfully passed read and write test.\");\n"
    code += "        $finish();\n"
    code += "    end\n\n"
    code += "endmodule\n\n"
    code += "`default_nettype wire\n"
    return code

def read_default_mem(file_path, mem_length):
    data_array = []
    index_arr = []
    value_arr = []
    found  = False

    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Process each line
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) == 2:
            index = int(parts[0].strip())
            value = int(parts[1].strip())
            index_arr.append(index)
            value_arr.append(value)
    
    for i in range(mem_length):
        try:
            index = index_arr.index(i)
            found = True
        except ValueError:
            found = False
        if(found):
            data_array.append(value_arr[index])
        else:
            data_array.append(0)
    return data_array


def main():

    input_ports = generate_input_ports(READ_DEPTH)
    output_ports = generate_output_ports(WRITE_DEPTH)
    input_tb = generate_input_tb(READ_DEPTH)
    output_tb = generate_output_tb(WRITE_DEPTH)
    io_inst = generate_inst_io(READ_DEPTH, WRITE_DEPTH)
    

    with open("./rtl/config.v", "w") as f:
        f.write("`define REG_WIDTH %i\n" %REG_WIDTH)
        f.write("`define READ_DEPTH %i\n" %READ_DEPTH)
        f.write("`define WRITE_DEPTH %i\n" %WRITE_DEPTH)
        f.write("`define MEM_DEPTH (`READ_DEPTH + `WRITE_DEPTH)\n\n")
        f.write("`define IO_PORTS\t\\\n")
        f.write(input_ports)
        f.write(output_ports)
        f.write("\n`define IO_TB\t\\\n")
        f.write(input_tb)
        f.write(output_tb)
        f.write("\n`define IO_INST\t\\\n")
        f.write(io_inst)

    with open("./rtl/sipo_piso_slave.v", "w") as f:
        f.write(generate_sipo_piso_slave(WRITE_DEPTH, READ_DEPTH, REG_WIDTH))
    
    with open("./rtl/sipo_piso_slave_tb.v", "w") as f:
        f.write(generate_sipo_piso_tb(WRITE_DEPTH, READ_DEPTH, REG_WIDTH))

if __name__ == "__main__":
    main()
