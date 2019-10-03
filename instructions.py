instruction_specs = {
    # rv32i
    "lui" : {
        "type": "u",
        "opcode": 0b0110111,
    },
    "auipc" : {
        "type": "u",
        "opcode": 0b0010111,
    },
    "jal" : {
        "type": "j",
        "opcode": 0b1101111,
    },
    "jalr" : {
        "type": "i",
        "opcode": 0b1100111,
        "funct3": 0b000,        
    },
    "beq" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b000,        
    },
    "bne" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b001,        
    },
    "blt" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b100,        
    },
    "bgt" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b101,        
    },
    "bltu" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b110,        
    },
    "bgeu" : {
        "type": "b",
        "opcode": 0b1100011,
        "funct3": 0b111,        
    },
    "lb" : {
        "type": "i",
        "opcode": 0b0000011,
        "funct3": 0b000,        
    },
    "lh" : {
        "type": "i",
        "opcode": 0b0000011,
        "funct3": 0b001,        
    },
    "lw" : {
        "type": "i",
        "opcode": 0b0000011,
        "funct3": 0b010,        
    },
    "lbu" : {
        "type": "i",
        "opcode": 0b0000011,
        "funct3": 0b100,        
    },
    "lhu" : {
        "type": "i",
        "opcode": 0b0000011,
        "funct3": 0b100,        
    },
    "sb" : {
        "type": "s",
        "opcode": 0b0100011,
        "funct3": 0b000,        
    },
    "sh" : {
        "type": "s",
        "opcode": 0b0100011,
        "funct3": 0b001,        
    },
    "sw" : {
        "type": "s",
        "opcode": 0b0100011,
        "funct3": 0b010,        
    },
    "addi" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b000,        
    },
    "sltii" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b010,        
    },
    "sltiu" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b011,        
    },
    "xori" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b100,        
    },
    "ori" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b110,        
    },
    "andi" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b111,        
    },
    "slli" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b001,        
        "funct7": 0b0000000,
    },
    "srli" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b101,        
        "funct7": 0b0000000,
    },
    "srai" : {
        "type": "i",
        "opcode": 0b0010011,
        "funct3": 0b101,
        "funct7": 0b0100000,
    },
    "add" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b000,
        "funct7": 0b0000000,
    },
    "sub" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b000,
        "funct7": 0b0100000,
    },
    "sll" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b001,
        "funct7": 0b0000000,
    },
    "slt" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b010,
        "funct7": 0b0000000,
    },
    "sltu" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b011,
        "funct7": 0b0000000,
    },
    "xor" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b100,
        "funct7": 0b0000000,
    },
    "srl" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b101,
        "funct7": 0b0000000,
    },
    "sra" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b101,
        "funct7": 0b0100000,
    },
    "or" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b110,
        "funct7": 0b0000000,
    },
    "and" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b111,
        "funct7": 0b0000000,
    },

    # rv32m
    "mul" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b000,
        "funct7": 0b0000001,
    },
    "mulh" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b001,
        "funct7": 0b0000001,
    },
    "mulhsu" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b010,
        "funct7": 0b0000001,
    },
    "mulhu" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b011,
        "funct7": 0b0000001,
    },
    "div" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b100,
        "funct7": 0b0000001,
    },
    "divu" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b101,
        "funct7": 0b0000001,
    },
    "rem" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b110,
        "funct7": 0b0000001,
    },
    "remu" : {
        "type": "r",
        "opcode": 0b0110011,
        "funct3": 0b111,
        "funct7": 0b0000001,
    },    
}
