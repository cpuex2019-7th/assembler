label1:
    addi t0, zero, 1
    j label3
label2:
    li t3, 0x12345678
    addi t1, t1, 2
    j ret
label3:
    addi t1, zero, 3
    j label2
ret:
    add a0, t0, t1
