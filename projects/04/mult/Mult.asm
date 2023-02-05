// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
  @sum
  M=0
  @R2
  M=0
(LOOP)
  //JMP if RAM[0] == 0
  @R0
  D=M
  @STOP
  D;JEQ
  // sum = sum + RAM[1]
  @sum
  D=M
  @R1
  D=D+M
  @sum 
  M=D
  //RAM[2] = sum
  @R2
  M=D
  // RAM[0] = RAM[0] - 1
  @R0
  D=M
  M=D-1
  @LOOP
  0;JMP
(STOP)
  @STOP
  0;JMP
 
