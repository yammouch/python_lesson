`timescale 1ps/1ps

module sub01(
 input  din,
 output dout);

assign dout = ~din;

endmodule


module tb;

reg  din;
wire dout;

sub01 sub01_i(
 .din  (din),
 .dout (dout) );

initial begin
  $dumpfile("ex01.vcd");
  $dumpvars(1, din, dout);
  repeat (4) begin
    #1000 din = 1'b0;
    #1000 din = 1'b1;
  end
end

endmodule
