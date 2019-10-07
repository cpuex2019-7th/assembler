    addi t0, zero, 0                ; loop index
    addi t1, zero, 26               ; loop count
    li t2, 0x7f000000               ; uart addr
loop:
    lb t3, t2, 0                ; t3 <- *(uart addr)
    sb t3, t2, 0
    addi t0, t0, 1
    blt t0, t1, loop
ret:
    addi a0, zero, 1
