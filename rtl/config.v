`define REG_WIDTH 32
`define READ_DEPTH 2
`define WRITE_DEPTH 7
`define MEM_DEPTH (`READ_DEPTH + `WRITE_DEPTH)

`define IO_PORTS	\
	input wire [`REG_WIDTH-1:0] rd_1,	\
	input wire [`REG_WIDTH-1:0] rd_2,	\
	output reg [`REG_WIDTH-1:0] wr_1,	\
	output reg [`REG_WIDTH-1:0] wr_2,	\
	output reg [`REG_WIDTH-1:0] wr_3,	\
	output reg [`REG_WIDTH-1:0] wr_4,	\
	output reg [`REG_WIDTH-1:0] wr_5,	\
	output reg [`REG_WIDTH-1:0] wr_6,	\
	output reg [`REG_WIDTH-1:0] wr_7

`define IO_TB	\
	reg [`REG_WIDTH-1:0] rd_1;	\
	reg [`REG_WIDTH-1:0] rd_2;	\
	wire [`REG_WIDTH-1:0] wr_1;	\
	wire [`REG_WIDTH-1:0] wr_2;	\
	wire [`REG_WIDTH-1:0] wr_3;	\
	wire [`REG_WIDTH-1:0] wr_4;	\
	wire [`REG_WIDTH-1:0] wr_5;	\
	wire [`REG_WIDTH-1:0] wr_6;	\
	wire [`REG_WIDTH-1:0] wr_7;

`define IO_INST	\
	 .rd_1(rd_1), .rd_2(rd_2),	\
	 .wr_1(wr_1), .wr_2(wr_2), .wr_3(wr_3), .wr_4(wr_4), .wr_5(wr_5), .wr_6(wr_6), .wr_7(wr_7)
