#!/usr/bin/env python3
import argparse
import sys
import pathlib
from typing import List
from enum import Enum


# This is a farily simple exercise. If you'd like to code this yourself or are simply curious,
# check: https://en.wikipedia.org/wiki/List_of_Nintendo_64_ROM_file_formats
    # https://jul.rustedlogic.net/thread.php?id=11769
class RomType(Enum):
    INVALID = 0
    N64 = 1
    Z64 = 2
    V64 = 3

class N64Rom:
    n64head = bytes([0x40, 0x12, 0x37, 0x80])
    z64head = bytes([0x80, 0x37, 0x12, 0x40])
    v64head = bytes([0x37, 0x80, 0x40, 0x12])

    def __init__(self, filePath:str) -> None:
        self.path = pathlib.Path(filePath)
        with open(filePath, "a+") as f: pass # create file if doesn't exist
        with open(filePath, 'rb') as f:
            self.buffer = bytearray(f.read())
        self.extension = self.path.suffix

    @property
    def size(self) -> int:
        return self.path.stat().st_size
    @property
    def magic(self) -> RomType:
        if self.buffer.startswith(self.n64head):
            return RomType.N64
        if self.buffer.startswith(self.z64head):
            return RomType.Z64
        if self.buffer.startswith(self.v64head):
            return RomType.V64
        return RomType.INVALID

    # Various methods that help with decryption
    @staticmethod
    def bytesSwap(input:bytearray, a:int, b:int) -> bytearray:
        tmp = input[a]
        input[a] = input[b]
        input[b] = tmp
        return input
    @staticmethod
    def byteSwapTwo(buffer) -> List:
        for i in range(0, len(buffer), 2):
            N64Rom.bytesSwap(buffer, i, i+1)
        return buffer
    @staticmethod
    def byteSwapFour(buffer) -> List:
        for i in range(0, len(buffer), 4):
            N64Rom.bytesSwap(buffer, i, i+3)
            N64Rom.bytesSwap(buffer, i+1, i+2)
        return buffer


def parse_args(argv: List[str]) -> argparse.Namespace:
    args = argparse.ArgumentParser(
            prog='N64RomConverter',
            usage='%(prog)s -i [FILE] -o [FILE]',
            description='A short python script for converting between n64 rom types [n64, z64, v64]'
    )
    args.add_help = True

    args.add_argument('--input', '-i', required=True, help='The file that needs to be converted', type=str)
    args.add_argument('--output', '-o', required=True, help='The destination file', type=str)

    return args.parse_args(argv)

def main(argv: List[str]) -> None:
    opts = parse_args(argv)

    inRom = N64Rom(opts.input)
    outRom = N64Rom(opts.output)

    if inRom.size > 134217728:
        print('Maximum file size is 128mb. No n64 rom should exceed this size. Is this a valid dump?')
        print('If this is some weird rom hack, then, please comment out this section of code')
        sys.exit(1)
    if inRom.size == 0:
        print(f'{inRom.path.name} does not exist or is empty.')
        with open(inRom.path.name) as f:
            f.truncate(0)
        sys.exit(1)

    match inRom.magic:
        case RomType.N64:
            if outRom.extension == '.z64':
                N64Rom.byteSwapFour(inRom.buffer)
            if outRom.extension == '.v64':
                N64Rom.byteSwapTwo(N64Rom.byteSwapFour(inRom.buffer))
        case RomType.Z64:
            if outRom.extension == '.n64':
                N64Rom.byteSwapFour(inRom.buffer)
            if outRom.extension == '.v64':
                N64Rom.byteSwapTwo(inRom.buffer)
        case RomType.V64:
            if outRom.extension == '.n64':
                N64Rom.byteSwapFour(N64Rom.byteSwapTwo(inRom.buffer))
            if outRom.extension == '.z64':
                N64Rom.byteSwapTwo(inRom.buffer)
        case RomType.INVALID:
            print("Judging by the magic bytes, it isn't a valid Nintendo64 Rom")
            sys.exit(1)

    outRom.path.write_bytes(inRom.buffer)

if __name__ == "__main__":
    main(sys.argv[1:])
