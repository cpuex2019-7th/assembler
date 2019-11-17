#!/usr/bin/env python3
import sys
import struct
import string
import re
from .instructions import instruction_specs
from .encode import encoder
from .constant import CONDITIONAL_JUMP_INSTRS
from .syntax_sugars import syntax_sugar_specs

# utilities for general
def exit_with_error(fmt):
    print(fmt)
    exit(1)

def is_num(s):
    return re.match(r'^(-)?(0x)?[0-9A-Fa-f][0-9A-Fa-f]*$', s) is not None

# utilities for label controll
def get_raw_label(label):
    label_inside = re.match(r"^\%lo\((.*)\)$", label)
    if label_inside is not None:
        return label_inside.groups()[0]
    else:
        return label
    
def label_to_imm(labels, label, current_offset):
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

def has_label(x):
    return x[3] is not None

def is_label_valid(x, labels):
    return has_label(x) and get_raw_label(x[3]) in labels

# utilities for instruction controll
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

# utilities for encoding    
def encode_by_spec(spec, args, line_num):
    try:
        if "encoder" in spec:
            return (spec["encoder"])(spec, args)
        elif "type" in spec:
            return (encoder[spec["type"]])(spec, args)
        else:
            return None
    except OverflowError:
        exit_with_error("[-] overflow occcuerd at {}".format(line_num))
    except IndexError:
        exit_with_error("[-] invalid arguments for {} at {}".format(instr_name,
                                                                    line_num))
        
def quick_encode(lines):
    parsed_instructions = []
    labels = {}
    instructions = []
    
    for line_num, raw_l in map(lambda x: (x[0]+1, x[1]), enumerate(lines)):
        # pre-processing
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
            parsed_instruction = [instr_name,
                                        args,
                                        len(instructions),
                                        target_label,
                                        line_num,
                                        1]
            imm_patches = [0] if has_label(parsed_instruction) else encode_by_spec(spec, args, line_num)
            parsed_instruction[5] = len(imm_patches)
            
            instructions.extend(imm_patches)
            parsed_instructions.append(parsed_instruction)
            
    return parsed_instructions, instructions, labels

def asm_instruction(parsed_instruction, labels = {}):
    instr_name, args, offset, target_label, line_num, current_size = parsed_instruction
    spec = get_spec(instr_name)
    if has_label(parsed_instruction):
        return encode_by_spec(spec,
                              replace_label_by(args,
                                               label_to_imm(labels,
                                                            target_label,
                                                            offset)),
                              line_num)
    else:
        return encode_by_spec(spec, args, line_num)

# utilities for label resolution
def update_instruction_sizes(labelled_instructions, instructions, labels):
    is_size_changed = False
    for i in range(0, len(labelled_instructions)):
        offset = labelled_instructions[i][2]
        current_size = labelled_instructions[i][5]
        imm_patches = asm_instruction(labelled_instructions[i], labels)
        if len(imm_patches) > current_size:
            diff = len(imm_patches) - current_size                
            # update current_size
            labelled_instructions[i][5] = len(imm_patches)
            # update instructions
            for _ in range(0, diff):
                instructions.insert(offset+1, 0)           
            # update labels
            for k in labels.keys():
                if labels[k] > offset:
                    labels[k] += diff
            # update info for all instructions with label references
            for j in range(0, len(labelled_instructions)):
                if labelled_instructions[j][2] > offset:
                    labelled_instructions[j][2] += diff
            # set is_size_changed flag to resolve labels again
            is_size_changed = True
    return labelled_instructions, instructions, labels, is_size_changed

# utilities to output asm
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
    

    # parse lines & quick encode
    ################
    parsed_instructions, instructions, labels = quick_encode(lines)
    
    # resolve instruction sizes
    ################    
    # first, we have to check the existance of labels.
    if any(list(map(lambda x: has_label(x) and not is_label_valid(x, labels),
                    parsed_instructions))):
        instr = next(filter(lambda x: not is_label_valid(x, labels), parsed_instructions))
        target_label = instr[3]
        line_num = instr[4]
        exit_with_error("[-] invalid label found at {}: {}".format(line_num, target_label))

    # second, we have to fix the size of each labelled instruction.
    # here we assume that the bigger the imm is, the more space is used.
    is_size_changed = True
    labelled_instructions = list(filter(has_label, parsed_instructions))
    while is_size_changed:
        labelled_instructions, instructions, labels, is_size_changed = \
            update_instruction_sizes(labelled_instructions, instructions, labels)

    # resolve labels and emit
    ################
    # after fixing the size of instructions, we can patch all the labels with imm!
    for labelled_instruction in labelled_instructions:
        offset = labelled_instruction[2]
        imm_patches = asm_instruction(labelled_instruction, labels)
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

# TODO: make this argument handling rich if needed
def main():
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
