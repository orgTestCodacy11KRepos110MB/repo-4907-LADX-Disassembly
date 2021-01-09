#!/usr/bin/env python3
#
# Decode or encode BG tilemap data using the ZLADX encoding format
#
# Usage:
#  tools/convert_background.py decode marin_beach.tilemap.encoded
#  tools/convert_background.py decode marin_beach.tilemap.encoded --output marin_beach.tilemap
#  tools/convert_background.py encode marin_beach-modified.tilemap --output marin_beach.tilemap.encoded

import sys
import argparse
from textwrap import wrap
from lib.background_coder import BackgroundCoder

def write_result(bytes, outfile, wrap_count=None):
    """
    Write as a sequence of bytes if the outfile is binary,
    but as wrapped hexadecimal values if printing on stdout.
    """
    if 'b' in outfile.mode:
        outfile.write(bytes)
    else:
        text = bytes.hex()
        if wrap_count:
            text = "\n".join(wrap(text, wrap_count))
        outfile.write(text + "\n")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    options_parser = argparse.ArgumentParser(add_help=False)
    options_parser.add_argument('--output', '-o', type=str, metavar='outfile', action='store', help='file to write the output to')
    options_parser.add_argument('--wrap', '-w', type=int, metavar='char_count', default=40, action='store', help='wrap the stdout output to a number of characters (40 by default; 0 to disable)')

    operations_subparser = arg_parser.add_subparsers(title='commands', dest='command', required=True)
    decoding_parser = operations_subparser.add_parser('decode',  parents=[options_parser], help='convert a tilemap encoded with the ZLADX format to a raw tilemap')
    decoding_parser.add_argument('infile', type=str, help='encoded tilemap file to decode')
    encoding_parser = operations_subparser.add_parser('encode',  parents=[options_parser], help='convert a raw tilemap to the encoded ZLADX format')
    encoding_parser.add_argument('infile', type=str, help='raw tilemap file to encode')

    args = arg_parser.parse_args()

    infile = open(args.infile, 'rb')
    data = infile.read()
    infile.close()

    outfile = (args.output and open(args.output, 'wb')) or sys.stdout
    result = bytearray()

    if args.command == 'decode':
        tilemap_bytes = BackgroundCoder.decode(data)
        for address in sorted(tilemap_bytes):
            result.append(tilemap_bytes[address])
        write_result(result, outfile, wrap_count=args.wrap)

    elif args.encode:
        # TODO: allow to specify the tilemap location and width from command-line argument
        # (For now defaults of location=0x9800 and width=20 are assumed.)
        result = BackgroundCoder.encode(data)
        write_result(result, outfile, wrap_count=args.wrap)

    outfile.close()

