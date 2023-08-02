// Title: SIPO PSIO V 1.0 (No Changelog)
// Created: August 07, 2023
// Updated: 
//---------------------------------------------------------------------------
// Testbench for Serial In Parallel Out and Parallel in Serial Out Module
// 
// Developed by Muhammad Usman (https://github.com/muhammadusman7)
//---------------------------------------------------------------------------

`timescale 1ns/1ps
`default_nettype none
`include "config.v"

module sipo_piso_tb ();

    localparam ADDR_WIDTH = $clog2(`MEM_DEPTH)-1;
    localparam SIPO_WIDTH = ADDR_WIDTH + `REG_WIDTH;
    localparam PISO_WIDTH = SIPO_WIDTH;

    reg     clk;
    reg     rst;
    reg     strobe;
    reg     wr_en;
    reg     din;
    wire    dout;
    wire    rw_flag;
    `IO_TB
    integer i, j;
    reg     [ADDR_WIDTH + 1 + `REG_WIDTH:0]  mem [`MEM_DEPTH:0];
    reg     [ADDR_WIDTH + 1 + `REG_WIDTH:0]  mem_read;

    sipo_piso uut (.clk(clk), .rst(rst), .strobe(strobe), .wr_en(wr_en), .din(din), .dout(dout), .rw_flag(rw_flag), `IO_INST);

    initial begin
        mem[0] = 36'h0_D2F8_B804;
        mem[1] = 36'h1_2175_00CC;
        mem[2] = 36'h2_8839_E68F;
        mem[3] = 36'h3_722C_D01A;
        mem[4] = 36'h4_C0B8_ED5D;
        mem[5] = 36'h5_F6F7_3141;
        mem[6] = 36'h6_C45A_C632;
        mem[7] = 36'h7_B1AC_E73A;
        clk = 0; rst = 0; strobe = 0;
        wr_en = 0; din = 0; mem_read = 'b0;
        rd_1 = $random();
        rd_2 = $random();
        mem[8] = {4'd8, rd_1};
        mem[9] = {4'd9, rd_2};
        #1  rst = 1;
        #10 rst = 0;
    end

    initial begin
        forever begin
            #5 clk = ~clk;
        end
    end

    initial begin
        // Writing through SIPO
        #2; wr_en = 1;
        for (i=0; i<10; i=i+1) begin
            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;
            for (j=0; j<36; j=j+1) begin
                din = mem[i][j];
                #10;
            end
        end
        #50 wr_en = 0;
        // Reading through PISO
        for (i=0; i<10; i=i+1) begin
            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;
            mem_read[35:32] = i;
            for (j=0; j<36; j=j+1) begin
                if (j<4) begin
                    din = mem_read[32+j];
                    #10;
                end else begin
                    mem_read[j-4] = dout;
                    din = 0;
                    #10;
                end
            end
            if(mem_read == mem[i]) begin
                $display ("Memory Location %d: Successfully written and read", i);
            end else begin
                $display ("Reading or writing to memory location %d: was failed, Actual: %h, Received: %h", i, mem[i], mem_read);
                #10 $finish();
            end
        end
        #1000 $display("SIPO and PISO have successfully passed read and write test.");
        $finish();
    end

endmodule

`default_nettype wire
