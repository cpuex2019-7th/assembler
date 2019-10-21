    li t1, 0x3f666666           ; 0.9
    fmvwx ft1, t1
    
    li sp, 0
    fsw ft1, sp, 0
    
    lw a0, sp, 0                ; a0 should be 0x3f666666
