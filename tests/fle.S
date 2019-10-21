    li t1, 0x3f666666           ; 0.9
    fmvwx ft1, t1
    li t2, 0x40400000           ; 3.0
    fmvwx ft2, t2        
    fle t0, ft1, ft2            ; 0.9 <= 3.0 ... t0 should be 1

    li t2, 0x3f666666           ; 0.9
    fmvwx ft2, t2        
    fle t1, ft1, ft2            ; 0.9 <= 0.9 ... t1 should be 1

    li t2, 0x3dcccccd           ; 0.1
    fmvwx ft2, t2        
    fle t2, ft1, ft2            ; 0.9 > 0.1 ... t1 should be 0    

    slli t0, t0, 2              ; scale up
    slli t1, t1, 1              ; scale up
    add a0, t0, t1
    add a0, a0, t2              ; should be 6
