register_aliases = {
    # integer
    'zero': 0,
    'ra': 1,
    'sp': 2,
    'gp': 3,
    'tp': 4,
    't0': 5,
    't1': 6,
    't2': 7,
    's0': 8,
    'fp': 8, # note: this duplication is intended.
    's1': 9,
    'a0': 10,
    'a1': 11,
    'a2': 12,
    'a3': 13,
    'a4': 14,
    'a5': 15,
    'a6': 16,
    'a7': 17,
    's2': 18,
    's3': 19,
    's4': 20,
    's5': 21,
    's6': 22,
    's7': 23,
    's8': 24,
    's9': 25,
    's10': 26,
    's11': 27,
    't3': 28,
    't4': 29,
    't5': 30,
    't6': 31,

    # floati
    'ft0': 0,
    'ft1': 1,
    'ft2': 2,
    'ft3': 3,
    'ft4': 4,
    'ft5': 5,
    'ft6': 6,
    'ft7': 7,
    
    'fs0': 8,
    'fs1': 9,
    
    'fa0': 10,
    'fa1': 11,
    'fa2': 12,
    'fa3': 13,
    'fa4': 14,
    'fa5': 15,
    'fa6': 16,
    'fa7': 17,

    'fs2': 18,
    'fs3': 19,
    'fs4': 20,
    'fs5': 21,
    'fs6': 22,
    'fs7': 23,
    'fs8': 24,
    'fs9': 25,
    'fs10': 26,
    'fs11': 27,

    'ft8': 28,
    'ft9': 29,
    'ft10': 30,
    'ft11': 31,
}

def register_to_int(s):
    if s in register_aliases:
        return register_aliases[s]
    elif s.startswith('x') or s.startswith('f'):
        return int(s[1:])
    else:
        print("[-] Invalid register name: {}".format(s))
        exit(1)
