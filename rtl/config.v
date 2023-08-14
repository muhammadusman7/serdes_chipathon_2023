`define REG_WIDTH 8
`define READ_DEPTH 8
`define WRITE_DEPTH 8
`define MEM_DEPTH (`READ_DEPTH + `WRITE_DEPTH)
`define ADDR_WIDTH 4

`define IO_PORTS	\
	input wire [`REG_WIDTH-1:0] rd_1,	\
	input wire [`REG_WIDTH-1:0] rd_2,	\
	input wire [`REG_WIDTH-1:0] rd_3,	\
	input wire [`REG_WIDTH-1:0] rd_4,	\
	input wire [`REG_WIDTH-1:0] rd_5,	\
	input wire [`REG_WIDTH-1:0] rd_6,	\
	input wire [`REG_WIDTH-1:0] rd_7,	\
	input wire [`REG_WIDTH-1:0] rd_8,	\
	output reg [`REG_WIDTH-1:0] wr_1,	\
	output reg [`REG_WIDTH-1:0] wr_2,	\
	output reg [`REG_WIDTH-1:0] wr_3,	\
	output reg [`REG_WIDTH-1:0] wr_4,	\
	output reg [`REG_WIDTH-1:0] wr_5,	\
	output reg [`REG_WIDTH-1:0] wr_6,	\
	output reg [`REG_WIDTH-1:0] wr_7,	\
	output reg [`REG_WIDTH-1:0] wr_8

`define IO_TB	\
	reg [`REG_WIDTH-1:0] rd_1;	\
	reg [`REG_WIDTH-1:0] rd_2;	\
	reg [`REG_WIDTH-1:0] rd_3;	\
	reg [`REG_WIDTH-1:0] rd_4;	\
	reg [`REG_WIDTH-1:0] rd_5;	\
	reg [`REG_WIDTH-1:0] rd_6;	\
	reg [`REG_WIDTH-1:0] rd_7;	\
	reg [`REG_WIDTH-1:0] rd_8;	\
	wire [`REG_WIDTH-1:0] wr_1;	\
	wire [`REG_WIDTH-1:0] wr_2;	\
	wire [`REG_WIDTH-1:0] wr_3;	\
	wire [`REG_WIDTH-1:0] wr_4;	\
	wire [`REG_WIDTH-1:0] wr_5;	\
	wire [`REG_WIDTH-1:0] wr_6;	\
	wire [`REG_WIDTH-1:0] wr_7;	\
	wire [`REG_WIDTH-1:0] wr_8;

`define IO_INST	\
	 .rd_1(rd_1), .rd_2(rd_2), .rd_3(rd_3), .rd_4(rd_4), .rd_5(rd_5), .rd_6(rd_6), .rd_7(rd_7), .rd_8(rd_8),	\
	 .wr_1(wr_1), .wr_2(wr_2), .wr_3(wr_3), .wr_4(wr_4), .wr_5(wr_5), .wr_6(wr_6), .wr_7(wr_7), .wr_8(wr_8)
