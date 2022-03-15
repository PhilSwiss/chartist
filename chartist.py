#!/usr/bin/python3
#
# Chartist:
#
# a small tool to generate textscreen-images from bitmap-charsets
#
# Hint: python -m pip install pillow (install PIL on Windows)
#
# last updated by Decca / RiFT on 15.03.2022 19:05
#

# import modules
from PIL import Image
import argparse
import os.path
import sys


# replace argparse-error message with own, nicer help/usage
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("Usage: chartist charsetfile textfile [OPTION...]\n"
              "Generate images from charsets and texts\n"
              "\n"
              "mandatory arguments:\n"
              "  charsetfile        imagefile with chars (e.g.: .png, .jpg, etc.)\n"
              "  textfile           textfile with textline(s) (plain ascii e.g.: .txt)\n"
              "\n"
              "optional arguments:\n"
              "  -s, --size         size of the chars (x or x and y)\n"
              "  -w, --widthtable   textfile with widthtable if chars are not of the same width\n"
              "  -m, --mappingtable textfile with mappingtable if charset is not ascii-relative\n"
              "  -o, --output       outputfile with rendered text (e.g.: .png, .jpg, etc.)\n"
              "  -f, --force        force overwrite of outputfile when it already exist \n"
              "  -r, --resolution   resolution of imagefile with rendered text (x or x and y)\n"
              "  -c, --color        backgroundcolor of imagefile with rendered text (R G B)\n"
              "  -v, --version      show version info\n"
              "  -h, --help         show this help\n"
              "\n"
              "The optional arguments are only needed if autodetection of size, resolution or\n"
              "color does not meet the required needs. The rendered image will only be saved, if\n"
              "an outputfile (-o/--output) is set. Otherwise the image will be shown by the os.\n"
              "The widthtable is just a textfile containing the letters, symbols, etc. and their\n"
              "individual widths one per line and seperated by a tab.\n"
              "The mappingtable is also a textfile containing all letters, symbols, etc. in the\n"
              "same order as they are positioned in the imagefile.\n"
              "\n"
              "examples:\n"
              "  chartist charsetfile.png textfile.txt\n"
              "  chartist chars.gif text.txt -o screen.png\n"
              "  chartist font.tif scroll.txt -s 8 -r 320 256\n"
              "  chartist letters.tif credits.txt -s 16 32 -r 256\n"
              "  chartist fontset.gif phrases.txt -o words.bmp -f\n"
              "  chartist graphic.jpg greets.txt -c 255 127 64 -o out.jpg\n"
              "  chartist charset.png textfile.txt -s 16 38 -m mappingtable.txt\n"
              "  chartist font.png textfile.txt -s 16 16 -w widthtable.txt\n", file=sys.stderr)
        self.exit(1, '%s: ERROR: %s\n' % (self.prog, message))


# set commandline arguments
parser = ArgumentParser(prog='chartist', add_help=False)
parser.add_argument('charset',
                    metavar='charsetfile.png',
                    type=str,
                    help='imagefile with chars')
parser.add_argument('text',
                    metavar='textfile.txt',
                    type=str,
                    help='textfile with textline(s)')
parser.add_argument('-s', '--size',
                    metavar='8',
                    type=int,
                    nargs='+',
                    action='store',
                    help='size of the charset (x or x and y)')
parser.add_argument('-w', '--widthtable',
                    metavar='widthtable.txt',
                    type=str,
                    action='store',
                    help='textfile with width-table')
parser.add_argument('-m', '--mappingtable',
                    metavar='mappingtable.txt',
                    type=str,
                    action='store',
                    help='textfile with mapping-table')
parser.add_argument('-o', '--output',
                    metavar='output.png',
                    type=str,
                    action='store',
                    help='imagefile with rendered text')
parser.add_argument('-f', '--force',
                    action='store_true',
                    help='force overwrite of imagefile')
parser.add_argument('-r', '--resolution',
                    metavar='320',
                    type=int,
                    nargs='+',
                    action='store',
                    help='resolution of imagefile with rendered text  (x or x and y)')
parser.add_argument('-c', '--color',
                    metavar='255',
                    type=int,
                    nargs=3,
                    action='store',
                    help='maincolor of imagefile with rendered text (R G B)')
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s 1.8')
args = parser.parse_args()


# check size argument
if args.size is not None and len(args.size) not in (1, 2):
    parser.error("either give 1 or 2 values for size, not " + str(len(args.size)))


# check resolution argument
if args.resolution is not None and len(args.resolution) not in (1, 2):
    parser.error("either give 1 or 2 values for resolution, not " + str(len(args.resolution)))


# init vars
offsetX = 0
offsetY = 0
locationX = 0
locationY = 0


# get commandline arguments
imageFile = args.charset
textFile = args.text
charArgs = args.size
widthFile = args.widthtable
mappingFile = args.mappingtable
outputFile = args.output
outputForce = args.force
outputRes = args.resolution
colorArgs = args.color


# load image file
try:
    orgImg = Image.open(imageFile)
except Exception as error:
    print("ERROR: " + str(error), file=sys.stderr)
    exit(1)
print("    Charset: " + imageFile)


# get image mode & format
orgMode = orgImg.mode
orgFormat = orgImg.format
orgFormat = '.' + orgFormat.lower()
print("     Format: " + orgFormat + " (" + orgMode + ")")


# get image dimensions
orgSizeX, orgSizeY = orgImg.size
print(" Resolution: " + str(orgSizeX) + " x " + str(orgSizeY))


# get image colors & amount
orgColors = orgImg.convert('RGB').getcolors(maxcolors=(orgSizeX * orgSizeY))
print("     Colors: " + str(len(orgColors)))


# load text file
textLines = []
try:
    with open(textFile) as file:
        for line in file:
            textLines.append(line.rstrip('\n'))
except Exception as error:
    print("ERROR: " + str(error), file=sys.stderr)
    exit(1)


# get amount of textlines
amountLines = len(textLines)
# get lenght of longest textline
longestLine = len(max(textLines, key=len))
print("  Textlines: " + str(amountLines) + " (max. " + str(longestLine) + " chars)")


# get or detect size of chars
if isinstance(charArgs, list):
    charSizeX = charArgs[0]
    if len(charArgs) > 1:
        charSizeY = charArgs[1]
    else:
        charSizeY = charArgs[0]
    print("   Charsize: " + str(charSizeX) + " x " + str(charSizeY))
else:
    if orgSizeX < orgSizeY:
        charSizeX = orgSizeX
        charSizeY = orgSizeX
    else:
        charSizeX = orgSizeY
        charSizeY = orgSizeY
    print("   Charsize: " + str(charSizeX) + " x " + str(charSizeY) + " (auto)")


# get or detect output resolution
if isinstance(outputRes, list):
    newImgX = outputRes[0]
    if len(outputRes) > 1:
        newImgY = outputRes[1]
    else:
        newImgY = outputRes[0]
    print("    Preview: " + str(newImgX) + " x " + str(newImgY))
else:
    # width by longest textline
    newImgX = longestLine * charSizeX
    # height by amount of textlines
    newImgY = amountLines * charSizeY
    print("    Preview: " + str(newImgX) + " x " + str(newImgY) + " (auto)")


# get or generate width-table
widthTable = {}
if isinstance(widthFile, str):
    try:
        with open(widthFile) as file:
            for line in file:
                letter, width = line.split('\t', 1)
                widthTable[letter] = int(width.strip())
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    print("     Widths: " + widthFile + " (" + str(len(widthTable)) + " entries)")
    # fill up width-table if incomplete
    if len(widthTable) < 96:
        for asc in range(32, 128):
            if not chr(asc) in widthTable:
                widthTable[chr(asc)] = charSizeX
        print("     Widths: added missing entries")
else:
    for asc in range(32, 128):
        widthTable[chr(asc)] = charSizeX
    print("     Widths: " + str(charSizeX) + " pixels (auto)")


# get or generate mapping-table
mappingTable = []
if isinstance(mappingFile, str):
    try:
        with open(mappingFile) as file:
            for line in file:
                for char in line.rstrip('\n'):
                    mappingTable.append(char)
    except Exception as error:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
    print("    Mapping: " + mappingFile + " (" + str(len(mappingTable)) + " entries)")
    # fill up mapping-table if incomplete
    if len(mappingTable) < 96:
        for asc in range(32, 128):
            if not chr(asc) in mappingTable:
                mappingTable.append(chr(asc))
        print("    Mapping: added missing chars")
else:
    for asc in range(32, 128):
        mappingTable.append(chr(asc))
    print("    Mapping: ascii-relative (auto)")


# get or detect background color
if isinstance(colorArgs, list):
    backgroundColor = tuple(colorArgs)
    print("    BGcolor: " + str(backgroundColor).replace("(", "").replace(")", ""))
else:
    # get dominant color
    dominantColor = max(orgColors)
    backgroundColor = dominantColor[1]
    print("    BGcolor: " + str(backgroundColor).replace("(", "").replace(")", " (auto)"))


# create new, empty image, but keep mode, colors, palette, etc.
if len(orgMode) > 1:
    # if mode rgb or higher, just set background via rgb-value
    newImg = orgImg.resize((newImgX, newImgY))
    newImg.paste(backgroundColor, (0, 0, newImgX, newImgY))
else:
    # if mode palette or lower, try to map rgb-value...
    pixelsRGB = list(orgImg.convert('RGB').getdata())
    indexRGB = next((index for index, value in enumerate(pixelsRGB) if value == backgroundColor), None)
    # ...to the existing palette
    if indexRGB is not None:
        pixelsPalette = list(orgImg.getdata())
        indexPalette = pixelsPalette[indexRGB]
        newImg = orgImg.resize((newImgX, newImgY))
        newImg.paste(indexPalette, (0, 0, newImgX, newImgY))
    # or create new rgb-image if no match is found
    else:
        newImg = Image.new(mode="RGB", size=(newImgX, newImgY), color=backgroundColor)


# generate text with chars
print("    generating image...")
for line in textLines:
    for letter in line:
        # get char position from mapping-table
        offsetX = (mappingTable.index(letter)) * charSizeX
        # if charset-image is NOT a one-liner, get chars from multiple lines
        if offsetX >= orgSizeX:
            charLine = (offsetX // orgSizeX)
            offsetY = (charSizeY * charLine)
            offsetX = offsetX - (orgSizeX * charLine)
            # if offset is out of bounds, the char was not found
            if offsetY >= orgSizeY:
                print("    ERROR: unmatched char \"" + letter + "\"", file=sys.stderr)
        else:
            offsetY = 0
        # copy char, but only from inbound charset-image
        Tile = orgImg.crop((offsetX, offsetY, min(orgSizeX, (offsetX + charSizeX)), min(orgSizeY, (offsetY + charSizeY))))
        # paste char to new image
        newImg.paste(Tile, (locationX, locationY))
        # count to the next pasting x-position by width of char
        locationX = locationX + widthTable[letter]
    # count to next pasting y-position
    locationY = locationY + charSizeY
    locationX = 0


# show final image when no outputfile
if not isinstance(outputFile, str):
    print("    try to show image...")
    newImg.show()
    print("    done.")
    exit()


# check if output file already exist
def check_file(outputName):
    if not outputForce:
        if os.path.isfile(outputName):
            print("ERROR: file already exist")
            exit(1)
    else:
        return


# save final image to outputfile
print("    try to save: " + str(outputFile))
check_file(outputFile)
try:
    newImg.save(outputFile)
except ValueError as error:
    if 'unknown file extension' in str(error):
        print("    try to save: " + str(outputFile) + str(orgFormat))
        check_file(outputFile + orgFormat)
        try:
            newImg.save(outputFile + orgFormat)
        except Exception as error:
            print("ERROR: " + str(error), file=sys.stderr)
            exit(1)
    else:
        print("ERROR: " + str(error), file=sys.stderr)
        exit(1)
except Exception as error:
    print("ERROR: " + str(error), file=sys.stderr)
    exit(1)


# end message
print("    done.")


# end of code
exit()
