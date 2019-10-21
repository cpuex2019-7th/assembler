    li t1, 0x3f666666           ; 0.9
    sw t1, sp, 0
    
    flw ft0, sp, 0
    fmvxw a0, ft0               ; a0 should be 0x3f666666
