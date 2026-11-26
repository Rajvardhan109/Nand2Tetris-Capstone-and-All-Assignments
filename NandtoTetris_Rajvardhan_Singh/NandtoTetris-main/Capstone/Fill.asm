(LOOP)
    @KBD
    D=M
    @BLACK
    D;JNE
    @color
    M=0
    @FILL
    0;JMP

(BLACK)
    @color
    M=-1

(FILL)
    @SCREEN
    D=A
    @pos
    M=D

(DRAW)
    @color
    D=M
    @pos
    A=M
    M=D
    @pos
    D=M+1
    M=D
    @KBD
    D=A-D
    @DRAW
    D;JGT
    @LOOP
    0;JMP


