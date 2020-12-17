#!/usr/bin/python3
#
# Chartist:
#
# a small tool to generate textscreen-images from ascii-relative charsets
#
# Hint: python -m pip install pillow (install PIL on Windows)
#
# last updated on 04.06.2020 22:50
#

# import modules
from PIL import Image
import argparse
import sys
import os

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
                  "  -m, --mappingtable textfile with mappingtable if charset is not ascii-relative\n"
                  "  -o, --output       outputfile with rendered text (e.g.: .png, .jpg, etc.)\n"
                  "  -r, --resolution   resolution of imagefile with rendered text (x or x and y)\n"
                  "  -c, --color        backgroundcolor of imagefile with rendered text (R G B)\n"
                  "  -v, --version      show version info\n"
                  "  -h, --help         show this help\n"
                  "\n"
                  "The optional arguments are only needed if autodetection of size, resolution or\n"
                  "color doesnt meet the required needs. The rendered image will only be saved, if\n"
                  "an outputfile (-o/--output) is set. Otherwise the image will be shown by the os.\n"
                  "The mappingtable is just a textfile containing all letters, symbols, etc. in the\n"
                  "same order as they are positioned in the imagefile.\n"
                  "\n"
                  "examples:\n"
                  "  chartist charsetfile.png textfile.txt\n"
                  "  chartist chars.gif text.txt -o screen.png\n"
                  "  chartist font.tif scroll.txt -s 8 -r 320 256\n"
                  "  chartist letters.tif credits.txt -s 16 32 -r 256\n"
                  "  chartist graphic.jpg greets.txt -c 255 127 64 -o out.jpg\n"        
                  "  chartist charset.png textfile.txt -s 16 38 -l mappingtable.txt\n", file=sys.stderr)
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
parser.add_argument('-v','--version', action='version', version='%(prog)s 1.2')
args = parser.parse_args()

# check size argument
if args.size is not None and len(args.size) not in (1, 2):
    parser.error("either give 1 or 2 values for size, not " + str(len(args.size)))

# check resolution argument
if args.resolution is not None and len(args.resolution) not in (1, 2):
    parser.error("either give 1 or 2 values for resolution, not " + str(len(args.resolution)))

# init vars
line = 0
string = 0
letter = 0
charSize = 0
offsetX = 0
offsetY = 0
locationX = 0
locationY = 0

# get commandline arguments
imageFile = args.charset
textFile = args.text
charArgs = args.size
mappingFile = args.mappingtable
outputFile = args.output
outputRes = args.resolution
colorArgs = args.color

# load image file
try:
      orgImg = Image.open(imageFile)
except Exception as error:
      print ( "ERROR: " + str(error), file=sys.stderr)
      exit(1)
print ("    Charset: " + imageFile)

# get image format
orgFormat = orgImg.format
orgFormat = '.' + orgFormat.lower()
print ("     Format: " + orgFormat)

# get image dimensions
orgSizeX, orgSizeY = orgImg.size
print (" Resolution: " + str(orgSizeX) + " x " + str(orgSizeY))

# load text file
textLines = []
try:
    with open(textFile) as file:
        for line in file:
            textLines.append(line.rstrip('\n'))
except Exception as error:
      print ( "ERROR: " + str(error), file=sys.stderr)
      exit(1)
    
# get amount of textlines
amountLines = len(textLines)
# get lenght of longest textline
longestLine = len(max(textLines, key=len))
print ("  Textlines: " + str(amountLines) + " (max. " + str(longestLine) + " chars)")

# get or detect size of chars
if isinstance(charArgs, list):
    charSizeX = charArgs[0]
    if len(charArgs) > 1: 
        charSizeY = charArgs[1]
    else:
        charSizeY = charArgs[0]
    print ("   Charsize: " + str(charSizeX) + " x " + str(charSizeY))
else:
    if orgSizeX < orgSizeY:
        charSizeX = orgSizeX
        charSizeY = orgSizeX
    else:
        charSizeX = orgSizeY
        charSizeY = orgSizeY
    print ("   Charsize: " + str(charSizeX) + " x " + str(charSizeY) + " (auto)")

# get or detect output resolution
if isinstance(outputRes, list):
      newImgX = outputRes[0]
      if len(outputRes) > 1:
            newImgY = outputRes[1]
      else:
            newImgY = outputRes[0]
      print ("    Preview: "  + str(newImgX) + " x " + str(newImgY) )

else:
      # width by longest textline
      newImgX = longestLine * charSizeX
      # height by amount of textlines
      newImgY = amountLines * charSizeY
      print ("    Preview: "  + str(newImgX) + " x " + str(newImgY) + " (auto)")

# get or generate mapping-table
mappingTable = []
if isinstance(mappingFile, str):
    try:
        with open(mappingFile) as file:
            for line in file:
                for char in line.rstrip('\n'):
                    mappingTable.append(char)
    except Exception as error:
      print ( "ERROR: " + str(error), file=sys.stderr)
      exit(1)
    print ("    Mapping: " + mappingFile + " (" + str(len(mappingTable)) + " entries)")
else:
    for asc in range(32, 128):
        mappingTable.append(chr(asc))
    print ("    Mapping: ascii-relative (auto)")
    
# get or detect dominant color
if isinstance(colorArgs, list):
      dominantColor = tuple(colorArgs) 
      print ("    BGcolor: " + str(dominantColor).replace("(","").replace(")", ""))
else:
      rgbImg = orgImg.convert('RGB')
      indexColor = max(rgbImg.getcolors(orgSizeX * orgSizeY))
      dominantColor = indexColor[1]
      print ("    BGcolor: " + str(dominantColor).replace("(","").replace(")", " (auto)"))

# create new, empty image
newImg = Image.new(mode = "RGB", size = (newImgX, newImgY), color = dominantColor )

# generate text with chars
print ("    generating image...")
while string < amountLines:
    textString = textLines[string] 
    while letter < len(textString):
        # get char position from mapping-table
        if textString[letter] in mappingTable:
            offsetX = (mappingTable.index(textString[letter])) * charSizeX
        else:
            # set out of bounds to skip char
            offsetX = orgSizeX
            offsetY = orgSizeY
        # if charset-image is NOT a one-liner, get chars from multiple lines
        if offsetX >= orgSizeX:
            charLine = (offsetX // orgSizeX)
            offsetY = (charSizeY * charLine)
            offsetX = offsetX - (orgSizeX * charLine)
            # if ofset is out of bounds, the char was not found
            if offsetY >= orgSizeY:
                print ("    ERROR: unmatched char \"" + textString[letter] + "\"", file=sys.stderr)
        else:
            offsetY = 0
        # copy char from charset-image
        Tile = orgImg.crop((offsetX, offsetY, (offsetX + charSizeX), (offsetY + charSizeY)))
        # paste char to new image
        newImg.paste(Tile, (locationX, locationY))
        # count to the next pasting position
        locationX = locationX + charSizeX
        # count to the next letter in text
        letter = letter + 1
        
    locationY =  locationY + charSizeY
    locationX = 0
    string = string + 1
    letter = 0

# show final image when no outputfile
if not isinstance(outputFile, str):
      print ("    try to show image...")
      newImg.show()
      print ("    done.")
      exit()

# save final image to outputfile
try:
      print ("    try to save: " + str(outputFile))
      newImg.save(outputFile)
except ValueError as error:
      if 'unknown file extension' in str(error):
            try:
                  print ("    try to save: " + str(outputFile) + str(orgFormat))
                  newImg.save(outputFile + orgFormat)
            except Exception as error:
                  print ( "    ERROR: " + str(error), file=sys.stderr)
                  exit(1)      
      else:
            print ( "    ERROR: " + str(error), file=sys.stderr)
            exit(1)      
except Exception as error:
      print ( "    ERROR: " + str(error), file=sys.stderr)
      exit(1)
      
# end message
print ("    done.")

# end of code
exit()
