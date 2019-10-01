register_aliases = {
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
    't6': 31    
}

def register_to_int(s):
    if s in register_aliases:
        return register_aliases[s]
    elif s.startswith('x'):
        return int(s[1:])
    else:
        print("[-] Invalid register name: {}".format(s))
        exit(1)
