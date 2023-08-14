// Title: SIPO PSIO V 1.0 (No Changelog)
// Created: August 14, 2023
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

    localparam ADDR_WIDTH = `ADDR_WIDTH;
    localparam SIPO_WIDTH = ADDR_WIDTH + `REG_WIDTH;
    localparam PISO_WIDTH = SIPO_WIDTH;

    integer seed = 90
;    reg     clk;
    reg     rst;
    reg     strobe;
    reg     wr_en;
    reg     din;
    wire    dout;
    wire    rw_flag;
    `IO_TB
    integer i, j;
    reg     [ADDR_WIDTH + `REG_WIDTH:0]  mem [`MEM_DEPTH:0];
    reg     [ADDR_WIDTH + `REG_WIDTH:0]  mem_read;

    sipo_piso uut (.clk(clk), .rst(rst), .strobe(strobe), .wr_en(wr_en), .din(din), .dout(dout), .rw_flag(rw_flag), `IO_INST);

    initial begin
        $dumpfile("sipo_psio.vcd");        $dumpvars(0, sipo_piso_tb);        mem[0] = 13'h0A2;
        mem[1] = 13'h15D;
        mem[2] = 13'h283;
        mem[3] = 13'h3C6;
        mem[4] = 13'h433;
        mem[5] = 13'h52B;
        mem[6] = 13'h635;
        mem[7] = 13'h715;
        mem[8] = 13'h847;
        clk = 0; rst = 0; strobe = 0;
        wr_en = 0; din = 0; mem_read = 'b0;
        rd_1 = $random(seed);
        rd_2 = $random(seed);
        rd_3 = $random(seed);
        rd_4 = $random(seed);
        rd_5 = $random(seed);
        rd_6 = $random(seed);
        rd_7 = $random(seed);
        rd_8 = $random(seed);
        mem[9] = {5'd9, rd_1};
        mem[10] = {5'd10, rd_2};
        mem[11] = {5'd11, rd_3};
        mem[12] = {5'd12, rd_4};
        mem[13] = {5'd13, rd_5};
        mem[14] = {5'd14, rd_6};
        mem[15] = {5'd15, rd_7};
        mem[16] = {5'd16, rd_8};
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
        for (i=0; i<17; i=i+1) begin
            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;
            for (j=0; j<13; j=j+1) begin
                din = mem[i][j];
                #10;
            end
        end
        #50 wr_en = 0;
        // Reading through PISO
        for (i=0; i<17; i=i+1) begin
            #50 strobe = 0; #10 strobe=1; #10 strobe = 0;
            mem_read[12:8] = i;
            for (j=0; j<13; j=j+1) begin
                if (j<5) begin
                    din = mem_read[8+j];
                    #10;
                end else begin
                    mem_read[j-5] = dout;
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
        #100 $display("SIPO and PISO have successfully passed read and write test.");
        $finish();
    end

endmodule

`default_nettype wire
