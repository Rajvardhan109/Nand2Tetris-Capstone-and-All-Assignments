// Box.asm for K = 132 (Roll No: 2501010132)
// Start Row = 132 (Address = 16384 + 32*132 = 20608)
// Height = 20 rows, Width = 16 pixels (1 word per row)

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
    @20608
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

    // Word 0 (16 pixels)
    @color
    D=M
    @addr
    A=M
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