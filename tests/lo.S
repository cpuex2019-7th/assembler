main:
    li a0, %lo(hoge)
    jalr zero, ra, 0
hoge:
    jalr zero, ra, 0

