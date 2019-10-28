from .encode import bit_to_int, int_to_bit, encoder
from .instructions import instruction_specs

def encode_ss_j(args):    
    if len(args) != 1:
        raise IndexError
    jal_spec = instruction_specs["jal"]
    return [encoder[jal_spec["type"]](jal_spec, ["x0", args[0]])]

def encode_ss_li(args):
    if len(args) != 2:
        raise IndexError
    rd = args[0]
    imm_32 = int_to_bit(args[1], 32)
    imm_addi = bit_to_int(imm_32 & 0xFFF, 12)
    imm_lui = bit_to_int((imm_32-imm_addi) & 0xFFFFF000, 32) >> 12
    lui_spec = instruction_specs["lui"]
    addi_spec = instruction_specs["addi"]
    return [
        encoder[lui_spec["type"]](lui_spec, [rd, imm_lui]),
        encoder[addi_spec["type"]](addi_spec, [rd, rd, imm_addi])
    ]

def encode_ss_liu(args):
    if len(args) != 2:
        raise IndexError
    lui_spec = instruction_specs["lui"]
    return [encoder[lui_spec["type"]](lui_spec, args)]

syntax_sugars = {
    "j": {
        "arg_num": 1,
        "encoder": encode_ss_j,
        "size": 1,
    },
    "li": {
        "arg_num": 2,        
        "encoder": encode_ss_li,
        "size": 2,
    },
    "liu": {
        "arg_num": 2,
        "encoder": encode_ss_liu,
        "size": 1,
    }
}
