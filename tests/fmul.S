    li t1, 0x3f666666           ; 0.9
    fmvwx ft1, t1
    li t2, 0x40400000           ; 3.0
    fmvwx ft2, t2    
    
    fmul ft0, ft1, ft2          ; 2.7
    fmvxw a0, ft0
