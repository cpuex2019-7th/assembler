import sys
import struct
from registers import register_to_int
from instructions import instruction_specs

# syntax

# .directive
# hoge:
#  addi r0, t0, 8

def to_uint(s, bitwidth):
    s = int(s)
    if s >= 0 and s < 2 ** bitwidth:
        return s
    elif 2 ** bitwidth - s > 0:
        return 2 ** bitwidth - s
    else:
        print("[-] overflow occcuerd. bitwidth: {}, but given imm is {}".format(bitwidth, s))
        exit(1)

def asm(lines):
    labels = {}  # key: symbol_name, value: offset
    instructions = []
    
    for line_num, l in enumerate(lines):
        if len(l) == 0:
            continue
        if l[0].startswith('.'): # directive
            pass # TODO
        elif l[0].endswith(':'): # labels
            label = l[0] [:-1]
            offset = len(instructions) * 4

            if label in labels:
                print("[-] label name duplicated: {}".format(label))
                exit(1)

            labels[label] = offset                
        else: # instructions
            instr_name = l[0]
            args = list(map(lambda x: x.strip(), ' '.join(l[1:]).split(',')))

            if instr_name in instruction_specs:
                spec = instruction_specs[instr_name]
                machine_code = 0;
                if spec["type"] == "r" and len(args) == 3:
                    rd = register_to_int(args[0])
                    rs1 = register_to_int(args[1])
                    rs2 = register_to_int(args[2])
                    machine_code = spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (spec["funct7"] << 25)
                elif spec["type"] == "i" and len(args) == 3:
                    rd = register_to_int(args[0])
                    rs1 = register_to_int(args[1])
                    imm = to_uint(args[2], 5)
                    # TODO: shift size check and use funct7
                    machine_code = spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (imm << 20)
                elif spec["type"] == "s" and len(args) == 3:
                    # s* hoge, foo, bar
                    # should be interpreted as
                    # s* rs2, rs1, imm 
                    rs2 = register_to_int(args[1])
                    rs1 = register_to_int(args[0])
                    imm = to_uint(args[2], 12)
                    # TODO: imm size check
                    # rs1+imm <- rs2
                    imm4to0 = imm & 0b11111
                    imm11to5 = (imm & 0b111111100000) >> 5
                    machine_code = spec["opcode"] | (imm4to0 << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm11to5 << 20)
                elif spec["type"] == "b" and len(args) == 3:
                    rd = register_to_int(args[0])
                    rs1 = register_to_int(args[1])
                    imm = to_uint(args[2], 13)
                    
                    imm11 = (imm & (0b1 << 11)) >> 11
                    imm4to1 = (imm & 0b11110) >> 1
                    imm10to5 = (imm & 0b11111100000) >> 5
                    imm12 = (imm & (0b1 << 12)) >> 12
                    machine_code = spec["opcode"] | (imm11 << 7) | (imm4to1 << 8) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm10to5 << 25) | (imm12 << 31)
                elif spec["type"] == "u" and len(args) == 2:
                    rd = register_to_int(args[0])
                    imm = to_uint(args[1], 32)
                    
                    machine_code = spec["opcode"] | (rd << 7) | (imm & ~(0b111111111111))
                elif spec["type"] == "j" and len(args) == 2:
                    rd = register_to_int(args[0])
                    imm = to_uint(args[2], 21)
                    
                    imm19to12 = (imm &  0b11111111000000000000) >> 12
                    imm11 = (imm & 0b100000000000) >> 11
                    imm10to1 = (imm & 0b11111111110) >> 1
                    imm20 = (imm & (0b1 << 20)) >> 20
                    mechine_code = spec["opcode"] | (rd << 7) | (imm19to12 << 12) | (imm11 << 20) | (imm10to1 << 21) | (imm20 << 31)
                else:
                    print("[-] invalid metadata found for {}".format(instr_name))
                    exit(1)
                instructions.append(machine_code)
            else:
                print("[-] instruction not found: {}".format(instr_name))
                exit(1)
                
    return b''.join([struct.pack('<I', instr) for instr in instructions])
    
        
    
def asm_from_file(flist):
    lines = []
    for filename in flist:
        with open(filename, 'r') as f:
            # .hoge
            # foobar:
            # thinking face, foobar
            # -> [[".hoge"], ["foobar:"], ["thinking", "face,", "foobar"]]
            lines.extend(list(map(lambda x: list(map(lambda y: y.strip(),
                                                     x.split())),
                                  f.read().split('\n'))))
    return asm(lines)

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("python asm.py <output binary name> <hoge.S> [<foobar.S> ...]")
        exit(1)

    with open(sys.argv[1], 'wb') as f:
        f.write(asm_from_file(sys.argv[2:]))
