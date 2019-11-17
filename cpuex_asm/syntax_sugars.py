from .utils import bit_to_int, int_to_bit
from .encode import encoder
from .instructions import instruction_specs

def encode_ss_j(spec, args, options):    
    if len(args) != 1:
        raise IndexError
    jal_spec = instruction_specs["jal"]
    return encoder[jal_spec["type"]](jal_spec, ["x0", args[0]], {})

def encode_ss_li(spec, args, options):
    if len(args) != 2:
        raise IndexError
    rd = args[0]
    try:
        imm = int_to_bit(args[1], 12)
        addi_spec = instruction_specs["addi"]
        return encoder[addi_spec["type"]](addi_spec, [rd, "x0", imm], {})
    except OverflowError:
        imm_32 = int_to_bit(args[1], 32)
        imm_addi = bit_to_int(imm_32 & 0xFFF, 12)
        imm_lui = bit_to_int((imm_32-imm_addi) & 0xFFFFF000, 32) >> 12
        lui_spec = instruction_specs["lui"]
        addi_spec = instruction_specs["addi"]
        return encoder[lui_spec["type"]](lui_spec, [rd, imm_lui], {}) + \
            encoder[addi_spec["type"]](addi_spec, [rd, rd, imm_addi], {})

def encode_ss_liu(spec, args, options):
    if len(args) != 2:
        raise IndexError
    lui_spec = instruction_specs["lui"]
    return encoder[lui_spec["type"]](lui_spec, args)

syntax_sugar_specs = {
    "j": {
        "arg_num": 1,
        "type": "j",
        "encoder": encode_ss_j,
    },
    "li": {
        "arg_num": 2,        
        "type": "i",
        "encoder": encode_ss_li,
    },
    "liu": {
        "arg_num": 2,
        "type": "i",
        "encoder": encode_ss_liu,
    },
}
