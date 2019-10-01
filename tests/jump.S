label1:
    addi t0, zero, 1
    j label3
label2:
    addi t1, zero, 2
    j ret
label3:
    addi t1, zero, 3
    j label2
ret:
    addi zero, zero, 0
