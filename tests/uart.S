    ;;  Initialization
    addi t0, zero, 0x41    
    li sp, 0x7F000000

    ;; read in bin and &hex
loop:   
    sb t0, sp, 4    
    j loop
