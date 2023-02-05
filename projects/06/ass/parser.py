import re
from enum import Enum


class Instruction(Enum):
    A = 1
    C = 2
    L = 3


A_COMMAND_PATTERN = re.compile(r'@(?P<symbol>[0-9a-zA-Z_\.\$:]+)')
C_COMMAND_PATTERN = re.compile(r'(?:(?P<dest>A?M?D?)=)?(?P<comp>[^;]+)(?:;(?P<jmp>.+))?')
L_COMMAND_PATTERN = re.compile(r'\((?P<label>[0-9a-zA-Z_\.\$:]+)\)')


class Parser:

    def __init__(self, path):
        self.hack = open(path)
        self.path = path
        self.current_instruction = None

    def reset(self):
        self.hack.seek(0)

    def hasMoreLines(self) -> str:
        cur_pos = self.hack.tell()
        has_more_lines = bool(self.hack.readline())
        self.hack.seek(cur_pos)
        return has_more_lines

    def advance(self):
        line = ''
        while line == '':
            line = self.hack.readline().split('//')[0].strip()
            self.current_instruction = line

    def instructionType(self) -> Instruction:
        if A_COMMAND_PATTERN.match(self.current_instruction):
            return Instruction.A
        elif L_COMMAND_PATTERN.match(self.current_instruction):
            return Instruction.L
        elif C_COMMAND_PATTERN.match(self.current_instruction):
            return Instruction.C

    def symbol(self) -> str:
        match self.instructionType():
            case Instruction.A:
                return A_COMMAND_PATTERN.match(self.current_instruction).group('symbol')
            case Instruction.L:
                return L_COMMAND_PATTERN.match(self.current_instruction).group('label')

    def dest(self) -> str:
        return C_COMMAND_PATTERN.match(self.current_instruction).group('dest')

    def comp(self) -> str:
        return C_COMMAND_PATTERN.match(self.current_instruction).group('comp')

    def jump(self) -> str:
        return C_COMMAND_PATTERN.match(self.current_instruction).group('jmp')

