import re
import sys

from code import Code
from parser import Parser, Instruction
from symbol import Symbol

SYMBOL_PATTERN = re.compile(r'(?P<number>[0-9]+)|(?P<symbol>[0-9a-zA-Z_\.\$:]+)')


def main(path):
    p = Parser(path)
    c = Code()
    s = Symbol()
    outpath = path.split('.')[0] + '.hack'

    current_line = 0
    while p.hasMoreLines():
        p.advance()
        match p.instructionType():
            case Instruction.A | Instruction.C:
                current_line += 1
            case Instruction.L:
                symbol = p.symbol()
                s.addEntry(symbol, current_line)
    p.reset()

    next_available_ram = 16
    with open(outpath, 'w') as o:
        while p.hasMoreLines():
            p.advance()
            current_instruction = p.instructionType()

            match current_instruction:
                case Instruction.A:
                    symbol = p.symbol()
                    m = SYMBOL_PATTERN.match(symbol)
                    if m.group('number'):  # @xxx
                        address = symbol
                    elif m.group('symbol'):  # (xxx)
                        if s.contains(symbol):
                            address = s.getAddress(symbol)
                        else:
                            s.addEntry(symbol, next_available_ram)
                            next_available_ram += 1
                            address = s.getAddress(symbol)
                    o.write(f'{int(address):016b}\n')

                case Instruction.C:
                    dest = c.dest(p.dest())
                    comp = c.comp(p.comp())
                    jump = c.jump(p.jump())
                    o.write(f'111{comp}{dest}{jump}\n')


if __name__ == '__main__':
    main(sys.argv[1])
