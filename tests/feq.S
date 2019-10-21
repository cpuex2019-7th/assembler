    li t1, 0x3f666666           ; 0.9
    fmvwx ft1, t1
    li t2, 0x40400000           ; 3.0
    fmvwx ft2, t2        
    feq t0, ft1, ft2            ; t0 should be 0

    li t2, 0x3f666666           ; 0.9
    fmvwx ft2, t2        
    feq t1, ft1, ft2            ; t1 should be 1

    slli t0, t0, 1              ; scale up
    add a0, t0, t1              ; should be 1
