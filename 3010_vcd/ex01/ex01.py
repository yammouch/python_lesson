#from Verilog_VCD import parse_vcd
import Verilog_VCD.Verilog_VCD as vv

#vcd = parse_vcd('ex01.vcd', siglist=['tb.din', 'tb.dout'])
#vcd = vv.parse_vcd('ex01.vcd', siglist=['tb.din', 'tb.dout'])
vcd = vv.parse_vcd('ex01.vcd')

print(vcd)
