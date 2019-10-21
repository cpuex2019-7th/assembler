    li t1, 1068708659           ; 1.4
    fmvwx ft1, t1               

    fcvtws t1, ft1              ; t1 should be 1

    li t2, 1080452710           ; 3.6
    fmvwx ft2, t2
    
    fcvtws t2, ft2              ; t1 should be 4

    add a0, t1, t2             ; a0 = t1 + t2, a0 should be 5
