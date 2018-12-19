`timescale 1ps/1ps

module sub01(
 input  [2:0] din,
 output [2:0] dout);

assign dout = ~din;

endmodule


module tb;

reg  [2:0] din;
//wire [2:0] dout;
wire       din_0, din_1, din_2;
wire       dout_0, dout_1, dout_2;
assign din_0 = din[0];
assign din_1 = din[1];
assign din_2 = din[2];

sub01 sub01_i(
 .din  (din),
 //.dout (dout) );
 .dout ({dout_0, dout_1, dout_2}) );

initial begin
  $dumpfile("ex01.vcd");
  //$dumpvars(1, din, dout);
  $dumpvars(1, din_0, din_1, din_2, dout_0, dout_1, dout_2);
  #1000 din = 3'b0;
  repeat (10) begin
    #1000 din = din + 3'd1;
  end
end

endmodule
