    addi t0, zero, 1
    addi t1, zero, 1
    beq t0, t1, eq
    j neq
eq:
    addi t2, zero, 3
    j ret
neq:
    addi t2, zero, 4
    j ret
ret:
    addi zero, zero, 1 ; nop   
