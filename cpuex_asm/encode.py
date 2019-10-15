from .registers import register_to_int

def to_int(s):
    if isinstance(s, int):
        return s
    return int(s[2:], 16) if s.startswith("0x") else int(s)

def bit_to_int(s, bitwidth):
    if s < 2 ** (bitwidth-1):
        return s
    else:
        return s - 2 ** bitwidth
    
def int_to_bit(s, bitwidth):
    # here we assume MSB is for sign
    s = to_int(s) 
    if 0 <= s:
        if s < 2 ** (bitwidth-1):
            return s
        else:
            raise OverflowError
    else: # s is a negative number
        if 0 <= 2 ** (bitwidth-1) + s:
            return 2 ** bitwidth + s
        else:
            raise OverflowError
        
# rd, rs1, rs2 
def encode_r(spec, args):
    if ("rs2" in spec and len(args) == 2) or ("rs2" not in spec and len(args) == 3):
        rd = register_to_int(args[0])
        rs1 = register_to_int(args[1])
        rs2 = register_to_int(args[2])
        return spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (spec["funct7"] << 25) | (spec["rs2"] if "rs2" in spec else 0)
    else:
        raise IndexError


# rd, rs1, imm
def encode_i(spec, args):
    if len(args) != 3:
        raise IndexError
    rd = register_to_int(args[0])
    rs1 = register_to_int(args[1])
    imm = int_to_bit(args[2], 12)
    return spec["opcode"] | (rd << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (imm << 20) | ((spec["funct7"] << 25) if "func7" in spec else 0)

# rs1, rs2, imm
def encode_b(spec, args):
    if len(args) != 3:
        raise IndexError
    
    rs1 = register_to_int(args[0])
    rs2 = register_to_int(args[1])
    imm = int_to_bit(args[2], 13)
    
    imm11 = (imm & (0b1 << 11)) >> 11
    imm4to1 = (imm & 0b11110) >> 1
    imm10to5 = (imm & 0b11111100000) >> 5
    imm12 = (imm & (0b1 << 12)) >> 12
    return spec["opcode"] | (imm11 << 7) | (imm4to1 << 8) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm10to5 << 25) | (imm12 << 31)

# rs2, rs1, imm
def encode_s(spec, args):
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
    return spec["opcode"] | (imm4to0 << 7) | (spec["funct3"] << 12) | (rs1 << 15) | (rs2 << 20) | (imm11to5 << 20)    

# rd, imm
# imm will be sll-ed by 12 
def encode_u(spec, args):
    if len(args) != 2:
        raise IndexError
    rd = register_to_int(args[0])
    imm = int_to_bit(args[1], 20) << 12
    return spec["opcode"] | (rd << 7) | (imm & 0xFFFFF000)

# rd, imm
def encode_j(spec, args):
    if len(args) != 2:
        raise IndexError
    rd = register_to_int(args[0])
    imm = int_to_bit(args[1], 21)
    imm19to12 = (imm &  0b11111111000000000000) >> 12
    imm11 = (imm & 0b100000000000) >> 11
    imm10to1 = (imm & 0b11111111110) >> 1
    imm20 = (imm & (0b1 << 20)) >> 20
    return spec["opcode"] | (rd << 7) | (imm19to12 << 12) | (imm11 << 20) | (imm10to1 << 21) | (imm20 << 31)

encoder = {
    "r": encode_r,
    "i": encode_i,
    "b": encode_b,
    "s": encode_s,
    "u": encode_u,
    "j": encode_j,
}
