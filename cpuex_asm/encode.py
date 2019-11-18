from .registers import register_to_int
from .instructions import instruction_specs
from .utils import to_int, bit_to_int, int_to_bit
        
# rd, rs1, rs2 
def encode_r(spec, args, options):
    if ("rs2" in spec and len(args) == 2) or ("rs2" not in spec and len(args) == 3):
        rd = register_to_int(args[0])
        rs1 = register_to_int(args[1])
        rs2 = spec["rs2"] if "rs2" in spec else register_to_int(args[2])
        return [
            spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (spec["funct7"] << 25) | (spec["rs2"] if "rs2" in spec else 0)
        ]
    else:
        raise IndexError


# rd, rs1, imm
def encode_i(spec, args, options):
    if len(args) != 3:
        raise IndexError
    rd = register_to_int(args[0])
    rs1 = register_to_int(args[1])
    imm = int_to_bit(args[2], 12)
    return [
        spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (imm << 20) | ((spec["funct7"] << 25) if "func7" in spec else 0)
    ]

# rs1, rs2, imm
def encode_b(spec, args, options):
    if len(args) != 3:
        raise IndexError

    try:
        rs1 = register_to_int(args[0])
        rs2 = register_to_int(args[1])
        imm = int_to_bit(args[2], 13)
    
        imm11 = (imm & (0b1 << 11)) >> 11
        imm4to1 = (imm & 0b11110) >> 1
        imm10to5 = (imm & 0b11111100000) >> 5
        imm12 = (imm & (0b1 << 12)) >> 12
        return [
            spec["opcode"] | (imm11 << 7) | (imm4to1 << 8) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm10to5 << 25) | (imm12 << 31)
        ]
    except OverflowError:
        print("Long jump!", spec, args, options)
        # li x31, (pc + imm)
        # op rs1, rs2, +8
        # jal zero, 8
        # jalr zero, x31, 0
        # ...        
        imm_32 = int_to_bit(to_int(args[2])+to_int(options["pc"])*4, 32)
        imm_addi = bit_to_int(imm_32 & 0xFFF, 12)
        imm_lui = bit_to_int((imm_32-imm_addi) & 0xFFFFF000, 32) >> 12        
        lui_spec = instruction_specs["lui"]
        addi_spec = instruction_specs["addi"]    
        jal_spec = instruction_specs["jal"]
        jalr_spec = instruction_specs["jalr"]
        return encoder[lui_spec["type"]](lui_spec, ["x30", imm_lui], {}) + \
            encoder[addi_spec["type"]](addi_spec, ["x30", "x30", imm_addi], {}) +\
            encoder[spec["type"]](spec, args[:2] + [8], {}) + \
            encoder[jal_spec["type"]](jal_spec, ["x0", 8], {}) + \
            encoder[jalr_spec["type"]](jalr_spec, ["x0", "x30", 0], {})
        

# rs2, rs1, imm
def encode_s(spec, args, options):
    if len(args) != 3:
        raise IndexError    
    # s* hoge, foo, bar
    # should be interpreted as
    # s* rs2, rs1, imm 
    # (rs1+imm <- rs2)
    rs2 = register_to_int(args[0])
    rs1 = register_to_int(args[1])
    imm = int_to_bit(args[2], 12)
    imm4to0 = imm & 0b11111
    imm11to5 = (imm & 0b111111100000) >> 5
    return [
        spec["opcode"] | (imm4to0 << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm11to5 << 25)
    ]

# rd, imm
# imm will be sll-ed by 12 
def encode_u(spec, args, options):
    if len(args) != 2:
        raise IndexError
    rd = register_to_int(args[0])
    imm = int_to_bit(args[1], 20) << 12
    return [
        spec["opcode"] | (rd << 7) | (imm & 0xFFFFF000)
    ]

# rd, imm
def encode_j(spec, args, options):
    if len(args) != 2:
        raise IndexError
    rd = register_to_int(args[0])
    imm = int_to_bit(args[1], 21)
    imm19to12 = (imm &  0b11111111000000000000) >> 12
    imm11 = (imm & 0b100000000000) >> 11
    imm10to1 = (imm & 0b11111111110) >> 1
    imm20 = (imm & (0b1 << 20)) >> 20
    return [
        spec["opcode"] | (rd << 7) | (imm19to12 << 12) | (imm11 << 20) | (imm10to1 << 21) | (imm20 << 31)
    ]

encoder = {
    "r": encode_r,
    "i": encode_i,
    "b": encode_b,
    "s": encode_s,
    "u": encode_u,
    "j": encode_j,
}
