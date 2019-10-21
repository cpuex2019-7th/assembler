#!/usr/bin/env python3
import sys
import struct
from .instructions import instruction_specs
from .encode import encoder
from .constant import CONDITIONAL_JUMP_INSTRS
from .syntax_sugars import syntax_sugars

def exit_with_error(fmt):
    print(fmt)
    exit(1)
    
def asm_lines(lines):
    """
    Asm given lines and returns machine codes in binary format. 

    Parameters
o    ----------
    lines : list of str
        lines to be assembled.

    Returns
    -------
    _ : bytes
        rv32im machine codes in binary format.
    """
    
    labels = {}  # key: symbol_name, value: offset
    instructions = []
    jumps = []

    # parse lines and emit machine codes
    ################
    for index, raw_l in enumerate(lines):
        # pre-processing
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
                exit_with_error("[-] label name duplicated: {}".format(label))
            labels[label] = offset            
        else: # instructions            
            instr_name = components[0]
            args = list(map(lambda x: x.strip(), ' '.join(components[1:]).split(',')))
            
            try:
                if instr_name in instruction_specs:
                    spec = instruction_specs[instr_name]
                    
                    # if the current instruction is one of conditional jumps and the instruction uses a label,
                    # we have to resolve it later.
                    if (instr_name in CONDITIONAL_JUMP_INSTRS \
                        # all conditional jump instructions take three ops; rs1, rs2, and rd.
                        and len(args) == 3 \
                        and not args[2].isdigit()):
                        target_label = args[2]
                        jumps.append((instr_name, len(instructions), target_label, line_num))
                        # 0 is temp addr
                        instructions.append(encoder[spec["type"]](spec, [args[0], args[1], 0]))
                    elif (instr_name == "jal" \
                        # jal takes two ops; rd and imm.
                        and len(args) == 2 \
                        and not args[1].isdigit()):
                        target_label = args[1]
                        jumps.append((instr_name, len(instructions), target_label, line_num))
                        # 0 is temp addr
                        instructions.append(encoder[spec["type"]](spec, [args[0], 0]))
                    elif spec["type"] in encoder:
                        # if the instruction does not cause jumps, it can be encoded directly.
                        instructions.append(encoder[spec["type"]](spec, args))
                    else:
                        # umm, here we got a weird metadata for the instruction ...
                        raise Exception
                elif instr_name in syntax_sugars and syntax_sugars[instr_name]['arg_num'] == len(args):
                    if instr_name == "j":
                        target_label = args[0]
                        jumps.append((instr_name, len(instructions), target_label, line_num))
                        instructions.append(0)
                    else:
                        instructions.extend(syntax_sugars[instr_name]['encoder'](args))                    
                else:
                    raise NotImplementedError
            except OverflowError:
                exit_with_error("[-] overflow occcuerd at {}".format(line_num))
            except IndexError:
                exit_with_error("[-] invalid arguments for {} at {}".format(instr_name,
                                                                            line_num))
            except NotImplementedError:                
                exit_with_error("[-] instruction not found at {}: {}".format(line_num,
                                                                             instr_name))                    
    # resolve labels
    ################
    for instr_name, i, target_label, line_num in jumps:
        if target_label in labels:
            imm = labels[target_label] - i * 4
            if instr_name == "j":
                spec = instruction_specs["jal"]
                instructions[i] = encoder[spec["type"]](spec, ["x0", imm])
            elif instr_name in CONDITIONAL_JUMP_INSTRS:
                spec = instruction_specs[instr_name]                
                instructions[i] |= encoder[spec["type"]](spec, ["x0", "x0", imm])
            elif instr_name == "jal":
                spec = instruction_specs[instr_name]                
                instructions[i] |= encoder[spec["type"]](spec, ["x0", imm])
            else:
                exit_with_error("[-] label jumping with {} is not implemented yet. sorry.".format(instr_name))
        else:
            exit_with_error("[-] invalid label found at {}: {}".format(line_num, target_label))
            
    # pack all instructions
    ################
    return b''.join([struct.pack('<I', instr) for instr in instructions])    

def asm_line(l):
    """
    Asm a given line and return a machine code (4 bytes).

    Parameters
    ----------
    l : string
        an instruction to be assembled.

    Returns
    -------
    _ : bytes
        a rv32im machine code in binary formats.
    """
    asm_lines([l])

 
def asm_files(flist):
    """
    Asm given files and returns machine codes in binary format.

    Parameters
    ----------
    flist : list of str
        file names to be assembled.

    Returns
    -------
    _ : bytes
        rv32im machine codes in binary format.
    """
    lines = []
    for filename in flist:
        with open(filename, 'r') as f:
            lines.extend(f.read().strip().split('\n'))
    return asm_lines(lines)

def main():
    # TODO: make this argument handling rich if needed
    if len(sys.argv) <= 2:
        print("{} <output binary name> <hoge.S> [<foobar.S> ...]".format(sys.argv[0]))
        exit(1)

    with open(sys.argv[1], 'wb') as f:
        f.write(asm_files(sys.argv[2:]))

if __name__ == '__main__':
    main()
