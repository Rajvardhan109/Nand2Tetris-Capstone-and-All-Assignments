// Box.asm for K = 27 (Roll No: 2501010127)
// Start Row = 27 (Address = 16384 + 32*27 = 17248)
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
    @17248
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