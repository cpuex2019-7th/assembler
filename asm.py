import sys
import struct
from instructions import instruction_specs
from encode import encoder
    
def asm_lines(lines):
    labels = {}  # key: symbol_name, value: offset
    instructions = []
    jumps = []

    # asm parse lines
    ################
    for index, raw_l in enumerate(lines):
        line_num = index + 1    
        stripped_line = raw_l.strip().split(';')[0].strip()
        if stripped_line == '':
            continue
        
        components = list(map(lambda y: y.strip(), stripped_line.split()))
                                                     
        if components[0].startswith('.'): # directive
            pass # TODO
        elif components[0].endswith(':'): # labels
            label = components[0] [:-1]
            offset = len(instructions) * 4

            if label in labels:
                print("[-] label name duplicated: {}".format(label))
                exit(1)

            labels[label] = offset            
        else: # instructions            
            instr_name = components[0]
            args = list(map(lambda x: x.strip(), ' '.join(components[1:]).split(',')))
            
            try:
                if instr_name in instruction_specs:
                    spec = instruction_specs[instr_name]
                    if instr_name in ["beq", "bne", "blt", "bge", "bltu", "bgeu"] \
                       and len(args) == 3 \
                       and not args[2].isdigit(): # label jumping
                        target_label = args[2]
                        jumps.append((instr_name, len(instructions), target_label, line_num))
                        # 0 is temp addr
                        instructions.append(encoder[spec["type"]](spec, [args[0], args[1], 0]))
                    elif spec["type"] in encoder:
                        instructions.append(encoder[spec["type"]](spec, args))
                    else:
                        raise Exception
                elif instr_name == "j" and len(args) == 1:
                    target_label = args[0]
                    jumps.append((instr_name, len(instructions), target_label, line_num))
                    instructions.append(0) # 0 is temp addr
            except OverflowError:
                print("[-] overflow occcuerd at {}".format(line_num))
                exit(1)
            except IndexError:
                print("[-] invalid arguments for {} at {}".format(instr_name,
                                                                  line_num))
                exit(1)
            except NotImplementedError:                
                print("[-] instruction not found at {}: {}".format(line_num,
                                                                   instr_name))
                exit(1)
                    
    # resolve labels
    ################
    for instr_name, i, target_label, line_num in jumps:
        if target_label in labels:
            if instr_name == "j":
                current_pc = i * 4
                imm = labels[target_label] - current_pc
                spec = instruction_specs["jal"]
                instructions[i] = encoder[spec["type"]](spec, ["x0", imm])
            elif instr_name in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
                current_pc = i * 4
                imm = labels[target_label] - current_pc
                spec = instruction_specs[instr_name]                
                instructions[i] |= encoder[spec["type"]](spec, ["x0", "x0", imm])
            else:
                print("[-] label jumping with {} is not implemented yet. sorry.".format(instr_name))
                exit(1)
        else:
            print("[-] invalid label found at {}: {}".format(line_num, target_label))
    
    # pack all instructions
    ################
    return b''.join([struct.pack('<I', instr) for instr in instructions])    
        
def asm_line(l):
    asm_lines([l])
    
def asm_files(flist):
    lines = []
    for filename in flist:
        with open(filename, 'r') as f:
            lines.extend(f.read().strip().split('\n'))
    return asm_lines(lines)

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("python asm.py <output binary name> <hoge.S> [<foobar.S> ...]")
        exit(1)

    with open(sys.argv[1], 'wb') as f:
        f.write(asm_files(sys.argv[2:]))
