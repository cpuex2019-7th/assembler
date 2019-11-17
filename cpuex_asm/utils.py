def to_int(s):
    if isinstance(s, int):
        return s
    return int(s[2:], 16) if s.startswith("0x") else int(s)

def bit_to_int(s, bitwidth):    
    return s if s < 2 ** (bitwidth-1) else s - 2 ** bitwidth
    
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
