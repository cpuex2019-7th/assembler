    ;;  Initialization
    li t0, 0x44434241	
    li t1, 0x44434241
    li sp, 0x7F000000

    ;; read in bin and &hex
    sb t0, sp, 0
    sb t1, sp, 4    

    sh t0, sp, 8
    sh t1, sp, 16    

    sw t0, sp, 24
