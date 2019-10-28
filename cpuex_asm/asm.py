#!/usr/bin/env python3
import sys
import struct
import string
import re
from .instructions import instruction_specs
from .encode import encoder
from .constant import CONDITIONAL_JUMP_INSTRS
from .syntax_sugars import syntax_sugars

def exit_with_error(fmt):
    print(fmt)
    exit(1)

def is_num(s):
    return re.match(r'^(-)?(0x)?[0-9A-Fa-f][0-9A-Fa-f]*$', s) is not None
    
def asm_lines(lines):
    """
    Asm given lines and returns machine codes in binary format. 

    Parameters
    ----------
    lines : list of str
        lines to be assembled.

    Returns
    -------
    _ : bytes
        rv32im machine codes in binary format.
    """
    
    labels = {}  # key: symbol_name, value: offset
    instructions = []
    instrs_with_label = []

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

                    # here we detect the use of label.
                    # if there's no use of label, we can encode it directly.
                    if (spec["type"] in ["b", "i", "s"] \
                        and len(args) == 3 \
                        and not is_num(args[2])):
                        target_label = args[2]
                        instrs_with_label.append((instr_name, len(instructions), target_label, line_num))
                        instructions.append(encoder[spec["type"]](spec, [args[0], args[1], 0]))
                    elif (spec["type"] in ["j", "u"] \
                          and len(args) == 2 \
                          and not is_num(args[1])):
                        target_label = args[1]
                        instrs_with_label.append((instr_name, len(instructions), target_label, line_num))
                        if spec["type"] == "u":
                            instructions.append(encoder[spec["type"]](spec, [args[0], 0]))
                        else: # 
                            instructions.append(encoder[spec["type"]](spec, [args[0], 0]))
                    elif spec["type"] in encoder:
                        instructions.append(encoder[spec["type"]](spec, args))
                    else:
                        # umm, here we got a weird metadata for the instruction ...
                        raise Exception
                elif instr_name in syntax_sugars \
                     and syntax_sugars[instr_name]['arg_num'] == len(args):                    
                    ss_spec = syntax_sugars[instr_name]
                    if len(args) == ss_spec['arg_num'] \
                       and not is_num(args[len(args)-1]):
                        # when the last operand is labelled value
                        target_label = args[len(args)-1]
                        instrs_with_label.append((instr_name, len(instructions), target_label, line_num))                        
                        instructions.extend([0] * syntax_sugars[instr_name]['size'])
                    else:
                        # when the operand is imm
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
    for instr_name, i, target_label, line_num in instrs_with_label:
        if target_label in labels:
            imm = labels[target_label] - i * 4
            if instr_name in instruction_specs:
                spec = instruction_specs[instr_name]
                if spec["type"] in ["b", "i", "s"]:
                    instructions[i] |= encoder[spec["type"]](spec, ["x0", "x0", imm])
                elif spec["type"] in ["j", "u"]: # TODO: is this correct?
                    instructions[i] |= encoder[spec["type"]](spec, ["x0", imm])
                else:
                    exit_with_error("[-] thinking_face")
            elif instr_name in syntax_sugars:
                ss_spec = syntax_sugars[instr_name]
                imm_patches = ss_spec["encoder"](["x0"] * (ss_spec["arg_num"]-1) + [imm])
                for offset in range(0, ss_spec["size"]):
                    instructions[i+offset] |= imm_patches[offset]
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
