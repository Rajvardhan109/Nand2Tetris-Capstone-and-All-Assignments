// Box.asm for K = 32 (Roll No: 2501010132)
// Start Row = 32 (Address = 16384 + 32*32 = 17408)
// Height = 20 rows, Width = 64 pixels (4 words per row)

(LOOP)
    @KBD
    D=M
    @SET_BLACK
    D;JNE

    @color
    M=0
    @DRAW_INIT
    0;JMP

(SET_BLACK)
    @color
    M=-1

(DRAW_INIT)
    @17408
    D=A
    @addr
    M=D

    @20
    D=A
    @rows
    M=D

(ROW_LOOP)
    @rows
    D=M
    @LOOP
    D;JEQ

    // Word 0
    @color
    D=M
    @addr
    A=M
    M=D

    // Word 1
    @color
    D=M
    @addr
    A=M+1
    M=D

    // Word 2
    @color
    D=M
    @addr
    A=M+1
    A=A+1
    M=D

    // Word 3
    @color
    D=M
    @addr
    A=M+1
    A=A+1
    A=A+1
    M=D

    // Next row (+32)
    @32
    D=A
    @addr
    M=D+M

    @rows
    M=M-1

    @ROW_LOOP
    0;JMP