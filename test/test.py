import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()

# Helper function to display results
def display_result(op_name, dut):
    print(f"{op_name}: result = {dut.uo_out.value}, uio_out = {dut.uio_out.value}")

async def test_tt_um_Richard28277(dut):
    # Clock generation

    encryption_key = 0xAB

    cocotb.start_soon(Clock(dut.clk, 10, units='ns').start())
    # Initialize Inputs
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    dut.rst_n.value = 0

    await Timer(50, units = 'ns')
    dut.rst_n.value = 1

    opcodes = [0b0000,0b0001,0b0010,0b0011,0b0111,0b1000]
    a = [i for i in range(16)] #0,
    b = [i for i in range(16)]

    for i in range(len(opcodes)): 
        for a_val in a: 
            for b_val in b: 
                dut.ui_in.value = a_val<<4 + b_val 
                dut.uio_in.value = opcodes[i]   
                await Timer(50, units='ns')
                match opcodes[i]: 
                    case 0: #add
                        display_result("ADD",dut)
                        assert dut.uo_out.value == a_val + b_val  
                    case 1: #sub
                        display_result("SUB",dut)
                        assert dut.uo_out.value == a_val - b_val  
                    case 2: #mul
                        display_result("MUL",dut)
                        assert dut.uo_out.value == a_val * b_val  
                    case 3: #div
                        display_result("DIV",dut)
                        assert dut.uo_out.value == ((a_val % b_val) << 4) | (a_val//b_val)  
                    case 4: #and
                        display_result("AND",dut)
                        assert dut.uo_out.value == a_val & b_val  
                    case 5: #or
                        display_result("OR",dut)
                        assert dut.uo_out.value == a_val | b_val  
                    case 6: #xor
                        display_result("XOR",dut)
                        assert dut.uo_out.value == a_val ^ b_val  
                    case 7: #not 
                        display_result("NOT",dut)
                        assert dut.uo_out.value == ~a_val 
                    case 8: #encode
                        display_result("ENC",dut)
                        assert dut.uo_out.value == ((a_val << 4) | b_val) ^ encryption_key
               

    
    



