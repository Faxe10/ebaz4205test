`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: light & matter Leibniz Uni Hannover
// Engineer: Fabian Walther
//
// Create Date: 07/31/2025 06:36:26 AM
// Design Name:
// Module Name: io_test
// Project Name: Time Tagger / Coincidence Counter
// Target Devices: EBAZ4205
// Tool Versions:
// Description:
// This code is used to test the trigger level of the IO ports,
// Sends trigger to AFG and counts how long it takes, later the voltage can be calculated
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////



module io_test(
output reg green,
output reg red,
output [31:0] counts_ch1_high,
output [31:0] counts_ch1_low,
output [31:0] counts_ch2_high,
output [31:0] counts_ch2_low,
output [31:0] counts_delay_trigger,
output reg trigger_out_afg,
input trigger_in_afg,
input clk_250mhz,
input start_measurment,
input [7:0]start_high_delay_input,

input channel1,
input channel2

    );
reg ch1_old;
reg ch2_old;
reg trigger_in_afg_old;
reg start_measurment_old;
reg [31:0] clk_counter;
reg running;
reg [31:0] counts_ch1_high_r;
reg [31:0] counts_ch1_low_r;
reg [31:0] counts_ch2_high_r;
reg [31:0] counts_ch2_low_r;
reg [31:0] counts_delay_trigger_r;
wire ch1_rise;
wire ch1_fall;
wire ch2_rise;
wire ch2_fall;
wire  trigger_in_afg_rise;
reg [7:0] start_high_delay;
wire [7:0] start_high_delay_input;
reg start;
reg trigger_send;
reg channel1_r;
reg channel2_r;
assign ch1_rise = channel1_r & ~ch1_old;
assign ch1_fall = ~channel1_r & ch1_old;
assign ch2_rise = channel2_r & ~ch2_old;
assign ch2_fall = ~channel2_r & ch2_old;
assign trigger_in_afg_rise = trigger_in_afg & ~trigger_in_afg_old;
assign start_high_delay_input = start_high_delay_input;
assign counts_ch1_high = counts_ch1_high_r;
assign counts_ch1_low = counts_ch1_low_r;
assign counts_ch2_high = counts_ch2_high_r;
assign counts_ch2_low = counts_ch2_low_r;
assign counts_delay_trigger = counts_delay_trigger_r;

always @(posedge clk_250mhz) channel1_r <= channel1;
always @(posedge clk_250mhz) channel2_r <= channel2;

always @(posedge clk_250mhz)begin
    ch1_old <= channel1_r;
    ch2_old <= channel2_r;
    trigger_in_afg_old <= trigger_in_afg;
    start_measurment_old <= start_measurment;
end
always @(posedge clk_250mhz)begin
    if( start_measurment & ~start_measurment_old) begin
        start <= 1;
    end else begin
        start <= 0;
    end
end
always @(posedge  clk_250mhz)begin
    if (start)begin
        counts_ch1_high_r <= 1;
        counts_ch1_low_r <= 1;
        counts_ch2_high_r <= 1;
        counts_ch2_low_r <= 1;
    end
    else if (ch1_rise)begin
        counts_ch1_high_r <= clk_counter;
    end
    if (ch1_fall)begin
        counts_ch1_low_r <= clk_counter;
    end
    if (ch2_rise)begin
        counts_ch2_high_r <= clk_counter;
    end
    if (ch2_fall)begin
        counts_ch2_low_r <= clk_counter;
    end
end


always @(posedge clk_250mhz)begin
    if (start) begin
        clk_counter <= 0;
        trigger_out_afg <= 1;
        start_high_delay <= start_high_delay_input;
    end else if (start_high_delay == 0)begin
        clk_counter <= clk_counter + 1;
        trigger_out_afg <= 0;
    end else begin
        start_high_delay <= start_high_delay - 1;
    end
end

always @(posedge clk_250mhz)begin
    if (start)begin
        trigger_send <= 1;
        counts_delay_trigger_r <= 1;
    end
    else if (trigger_in_afg_rise) begin
        trigger_send <= 0;
    end
    if (trigger_send)begin
        counts_delay_trigger_r <= counts_delay_trigger_r + 1;
    end
end

endmodule

