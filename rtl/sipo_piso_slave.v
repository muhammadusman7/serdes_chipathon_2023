// Title: SIPO PISO V 1.0 (No Changelog)
// Created: August 14, 2023
// Updated: 
//---------------------------------------------------------------------------
// Serial In Parallel Out and Parallel in Serial Out Module
// 
// Developed by Muhammad Usman (https://github.com/muhammadusman7)
//---------------------------------------------------------------------------

`timescale 1ns/1ps
`default_nettype none
`include "config.v"

module sipo_piso (
    input   wire    clk,
    input   wire    rst,
    input   wire    strobe,
    input   wire    wr_en,
    input   wire    din,
    output  reg     dout,
    output  reg     rw_flag,
    `IO_PORTS
);

    // Instantiate where required as below
    // sipo_piso sipo_piso_inst (.clk(), .rst(), .strobe(), .wr_en(), .din(), .dout(), .rw_flag(), .rd_1(), .rd_2(), .rd_3(), .rd_4(), .rd_5(), .rd_6(), .rd_7(), .rd_8(), .wr_1(), .wr_2(), .wr_3(), .wr_4(), .wr_5(), .wr_6(), .wr_7(), .wr_8());

    localparam ADDR_WIDTH = `ADDR_WIDTH;
    localparam SIPO_WIDTH = ADDR_WIDTH + `REG_WIDTH;
    localparam PISO_WIDTH = SIPO_WIDTH;
    localparam COUNT_WIDTH = $clog2(SIPO_WIDTH)-1;
    localparam IDLE = 2'b00;
    localparam PROCESS = 2'b01;
    localparam SEND = 2'b10;

    reg     [ADDR_WIDTH:0]      sipo_addr, piso_addr, piso_addr_count;
    reg     [COUNT_WIDTH:0]     count;
    reg     [SIPO_WIDTH:0]      sipo_data, discard;
    reg     [SIPO_WIDTH:0]      sipo_reg;
    reg     [`REG_WIDTH-1:0]    mem_rd1;
    reg     [`REG_WIDTH-1:0]    mem_rd2;
    reg     [`REG_WIDTH-1:0]    mem_rd3;
    reg     [`REG_WIDTH-1:0]    mem_rd4;
    reg     [`REG_WIDTH-1:0]    mem_rd5;
    reg     [`REG_WIDTH-1:0]    mem_rd6;
    reg     [`REG_WIDTH-1:0]    mem_rd7;
    reg     [`REG_WIDTH-1:0]    mem_rd8;
    reg     [`REG_WIDTH-1:0]    mem_wr0;
    reg     [`REG_WIDTH-1:0]    mem_wr1;
    reg     [`REG_WIDTH-1:0]    mem_wr2;
    reg     [`REG_WIDTH-1:0]    mem_wr3;
    reg     [`REG_WIDTH-1:0]    mem_wr4;
    reg     [`REG_WIDTH-1:0]    mem_wr5;
    reg     [`REG_WIDTH-1:0]    mem_wr6;
    reg     [`REG_WIDTH-1:0]    mem_wr7;
    reg     [`REG_WIDTH-1:0]     mem_wr8;
    reg     [`REG_WIDTH-1:0]     piso_data;
    reg     [`REG_WIDTH-1:0]     control_reg;
    reg     [2:0]               status;

    always @(*) begin
        control_reg = mem_wr0;
        wr_1 = mem_wr1;
        wr_2 = mem_wr2;
        wr_3 = mem_wr3;
        wr_4 = mem_wr4;
        wr_5 = mem_wr5;
        wr_6 = mem_wr6;
        wr_7 = mem_wr7;
        wr_8 = mem_wr8;
        if(rw_flag && wr_en) begin
            sipo_addr = sipo_reg[SIPO_WIDTH:`REG_WIDTH];
            sipo_data = sipo_reg[`REG_WIDTH-1:0];
        end else begin
            sipo_addr = 'b0;
            sipo_data = mem_wr0;
        end
        if (status == SEND) begin
            if(piso_addr < `MEM_DEPTH) begin
                dout = piso_data[count];
            end else begin
                // Address is out of range then send data of the discard which can be any data (useless to read from address out of bound)
                dout = discard[count];
            end
        end else begin
            dout = 'b0;
        end
    end

    always @(posedge clk) begin

        if (rst) begin
            status <= IDLE;
            count <= 'b0;
            sipo_reg <= 'b0;
            piso_addr <= 'b0;
            piso_addr_count <= 'b0;
            mem_wr0 <= 8'h0;
            mem_wr1 <= 8'b0;
            mem_wr2 <= 8'b1010_1010;
            mem_wr3 <= 8'b1100_1100;
            mem_wr4 <= 8'b0;
            mem_wr5 <= 8'b101_0101;
            mem_wr6 <= 8'b0;
            mem_wr7 <= 8'b0;
            mem_wr8 <= 8'b0;
            mem_rd1 <= 8'b0;
            mem_rd2 <= 8'b0;
            mem_rd3 <= 8'b0;
            mem_rd4 <= 8'b0;
            mem_rd5 <= 8'b0;
            mem_rd6 <= 8'b0;
            mem_rd7 <= 8'b0;
            mem_rd8 <= 8'b0;
            discard <= 8'b0;
        end else begin
            mem_rd1 <= rd_1;
            mem_rd2 <= rd_2;
            mem_rd3 <= rd_3;
            mem_rd4 <= rd_4;
            mem_rd5 <= rd_5;
            mem_rd6 <= rd_6;
            mem_rd7 <= rd_7;
            mem_rd8 <= rd_8;
            case (status)
                IDLE: begin
                    count <= 'b0;
                    rw_flag <= 1'b0;
                    piso_addr_count <= 'b0;
                    if(strobe) begin
                        status <= PROCESS;  // strobe should be sent for 1 clock cycle to start process
                    end else begin
                        status <= IDLE;
                    end
                end 
                PROCESS: begin
                    if (wr_en) begin    // SIPO mode
                        if (count == SIPO_WIDTH) begin
                            sipo_reg[count] <= din;
                            count <= 'b0;
                            status <= IDLE;
                            rw_flag <= 1'b1;
                        end else begin
                            sipo_reg[count] <= din;
                            count <= count + 1;
                            status <= PROCESS;
                            rw_flag <= 1'b0;
                        end
                    end else begin // PISO mode
                        if(piso_addr_count <= `ADDR_WIDTH) begin
                            piso_addr [piso_addr_count] <= din;
                            piso_addr_count <= piso_addr_count + 1;
                            status <= PROCESS;
                        end else begin
                            status <= SEND;
                            rw_flag <= 1'b1;
                        end
                    end
                end
                SEND: begin
                    status <= SEND;
                end
                default status <= IDLE;
            endcase
            case (sipo_addr)
                5'd0    : mem_wr0   <= sipo_data;
                5'd1    : mem_wr1   <= sipo_data;
                5'd2    : mem_wr2   <= sipo_data;
                5'd3    : mem_wr3   <= sipo_data;
                5'd4    : mem_wr4   <= sipo_data;
                5'd5    : mem_wr5   <= sipo_data;
                5'd6    : mem_wr6   <= sipo_data;
                5'd7    : mem_wr7   <= sipo_data;
                5'd8    : mem_wr8   <= sipo_data;
                default : discard   <= sipo_data;
            endcase
            case (piso_addr)
                5'd0    : piso_data <= mem_wr0;
                5'd1    : piso_data <= mem_wr1;
                5'd2    : piso_data <= mem_wr2;
                5'd3    : piso_data <= mem_wr3;
                5'd4    : piso_data <= mem_wr4;
                5'd5    : piso_data <= mem_wr5;
                5'd6    : piso_data <= mem_wr6;
                5'd7    : piso_data <= mem_wr7;
                5'd8    : piso_data <= mem_wr8;
                5'd9    : piso_data <= mem_rd1;
                5'd10    : piso_data <= mem_rd2;
                5'd11    : piso_data <= mem_rd3;
                5'd12    : piso_data <= mem_rd4;
                5'd13    : piso_data <= mem_rd5;
                5'd14    : piso_data <= mem_rd6;
                5'd15    : piso_data <= mem_rd7;
                5'd16    : piso_data <= mem_rd8;
                default : discard   <= discard;
            endcase
        end
    end

    always @(negedge clk) begin
        case (status)
            PROCESS: begin
                if (~wr_en) begin
                    if(piso_addr_count > `ADDR_WIDTH) begin
                        status <= SEND;
                        rw_flag <= 1'b1;
                    end
                end
            end
            SEND: begin
                if (count < `REG_WIDTH-1) begin
                    count <= count + 1;
                    status <= SEND;
                    rw_flag <= 1'b1;
                end else begin
                    count <=  'b0;
                    status <= IDLE;
                    rw_flag <= 1'b0;
                end
            end
            default status <= status;
        endcase
    end

endmodule

`default_nettype wire
