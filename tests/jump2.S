label1:
    addi t1, zero, 0            ; 0
    jal a0, label3              ; 4
label2:
    add t1, t1, a0              ; 8
    jal a0, ret                 ; 12
label3:
    add t1, t1, a0              ; 16
    jal a0, label2              ; 20
ret:
    add a0, t1, a0              ; 24
