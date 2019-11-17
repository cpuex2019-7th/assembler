#!/usr/bin/env python3
import sys
import struct
import string
import re
from .instructions import instruction_specs
from .encode import encoder
from .constant import CONDITIONAL_JUMP_INSTRS
from .syntax_sugars import syntax_sugar_specs

def exit_with_error(fmt):
    print(fmt)
    exit(1)

def is_num(s):
    return re.match(r'^(-)?(0x)?[0-9A-Fa-f][0-9A-Fa-f]*$', s) is not None

def get_label(label):
    label_inside = re.match(r"^\%lo\((.*)\)$", label)
    if label_inside is not None:
        return label_inside.groups()[0]
    else:
        return label
    
def get_label_imm(labels, label, current_offset):
    label_inside = re.match(r"^\%lo\((.*)\)$", label)
    if label_inside is not None:
        label = label_inside.groups()[0]
        return labels[label] * 4
    else:
        return (labels[label] - current_offset) * 4

def replace_label_by(args, imm):
    return args[:-1] + [imm]

def get_label_in_args(spec, args):
    if(spec["type"] in ["b", "i", "s"] \
       and len(args) == 3 \
       and not is_num(args[2])):
        return args[2]
    elif (spec["type"] in ["j", "u"] \
          and len(args) == 2 \
          and not is_num(args[1])):
        return args[1]
    elif ('arg_num' in spec \
          and len(args) == spec['arg_num'] \
          and not is_num(args[len(args)-1])):
        return args[len(args)-1]    
    else:
        return None

def is_instr(instr_name):
    return instr_name in instruction_specs

def is_syntax_sugar(instr_name):
    return instr_name in syntax_sugar_specs

def get_spec(instr_name):
    if is_instr(instr_name):
        return instruction_specs[instr_name]
    elif is_syntax_sugar(instr_name):
        return syntax_sugar_specs[instr_name]
    else:
        return None
    
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

    # parse lines
    ################
    for index, raw_l in enumerate(lines):
        # pre-processing
        line_num = index + 1    
        stripped_line = raw_l.strip().split(';')[0].strip()
        if stripped_line == '':
            continue        
        components = list(map(lambda y: y.strip(), stripped_line.split()))

        # if the line describes ...
        if components[0].endswith(':'):
            # labels
            label = components[0] [:-1]
            offset = len(instructions)
            if label in labels:
                exit_with_error("[-] label name duplicated: {}".format(label))
            labels[label] = offset            
        else:
            # instructions            
            instr_name = components[0]
            args = list(map(lambda x: x.strip(), ' '.join(components[1:]).split(',')))
            spec = get_spec(instr_name)
            if spec is None:
                exit_with_error("[-] instruction not found at {}: {}".format(line_num,
                                                                             instr_name))
            target_label = get_label_in_args(spec, args)
            try:
                if target_label != None:
                    instrs_with_label.append([instr_name,
                                              args,
                                              len(instructions),
                                              target_label,
                                              line_num])
                    instructions.append(0)
                elif is_instr(instr_name):
                    instructions.append(encoder[spec["type"]](spec, args))
                elif is_syntax_sugar(instr_name): 
                    instructions.extend(syntax_sugar_specs[instr_name]['encoder'](args))                    
            except OverflowError:
                exit_with_error("[-] overflow occcuerd at {}".format(line_num))
            except IndexError:
                exit_with_error("[-] invalid arguments for {} at {}".format(instr_name,
                                                                            line_num))
    # resolve instruction sizes
    ################
    # here we assume that the bigger the imm is, the more space is used.

    # first, we have to check the existance of labels.
    for instr_with_label in instrs_with_label:
        instr_name, args, offset, target_label, line_num = instr_with_label
        if get_label(target_label) not in labels:
            exit_with_error("[-] invalid label found at {}: {}".format(line_num, target_label))
            
    # second, we have to fix the size of each syntax sugars.
    syntax_sugars = list(map(lambda x: x + [1], filter(lambda x: is_syntax_sugar(x[0]), instrs_with_label)))
    overflow = True
    while overflow:
        print(labels)
        overflow = False
        for i in range(0, len(syntax_sugars)):
            instr_name, args, offset, target_label, line_num, current_size = syntax_sugars[i]
            spec = get_spec(instr_name)
            imm = get_label_imm(labels, target_label, offset)
            args = replace_label_by(args, imm)
            imm_patches = spec["encoder"](args)
            if len(imm_patches) > current_size:
                diff = len(imm_patches) - current_size                
                for _ in range(0, diff):
                    instructions.insert(offset+1, 0)
                # update current_size
                syntax_sugars[i][5] = len(imm_patches)
                # update labels
                for k in labels.keys():
                    if labels[k] > offset:
                        labels[k] += diff
                # update offset of syntax sugars
                for j in range(0, len(syntax_sugars)):
                    if syntax_sugars[j][2] > offset:
                        syntax_sugars[j][2] += diff
                # update info for all instructions with label references
                for j in range(0, len(instrs_with_label)):
                    if instrs_with_label[j][2] > offset:
                        instrs_with_label[j][2] += diff
                # set overflow flag to resolve labels again
                overflow = True
                
    # resolve labels and emit
    ################
    # after fixing the size of instructions, we can patch all the labels with imm!
    for instr_with_label in instrs_with_label:
        instr_name, args, offset, target_label, line_num = instr_with_label
        if get_label(target_label) in labels:
            spec = get_spec(instr_name)
            imm = get_label_imm(labels, target_label, offset)
            args = replace_label_by(args, imm)
            if is_instr(instr_name):
                instructions[offset] |= encoder[spec["type"]](spec, args)
            else:
                imm_patches = spec["encoder"](args)
                for j in range(0, len(imm_patches)):
                    instructions[offset+j] |= imm_patches[j]
            
    # pack all instructions
    ################
    assembled_code = b''.join([struct.pack('<I', instr) for instr in instructions])
    return assembled_code, labels

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

    mcode, labels = asm_files(sys.argv[2:])
    with open(sys.argv[1], 'wb') as f:
        f.write(mcode)
    with open(sys.argv[1] + '.symbols', 'w') as f:
        f.write('\n'.join(map(lambda x: '{} {}'.format(x[0], str(4 * x[1])), labels.items())))
        
if __name__ == '__main__':
    main()
