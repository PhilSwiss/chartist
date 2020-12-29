![Chartist Logo](https://repository-images.githubusercontent.com/320932478/eb66cf80-49f9-11eb-8430-46f8d50ad519)

Chartist
========

Commandline tool to generate images from charsets and texts.

While [pixeling](http://grafx2.chez.com/) a [font](http://janeway.exotica.org.uk/search.php?what=0&special=&query=&cat=1630&show=128&tags=&effects=&gfxstyles=&collection_category=0&collection=&year=all&soundformat=&bitplanes=0&gfxsize=0&country=&more=hide) (also known as *charset*) for a [demoscene](https://en.wikipedia.org/wiki/Demoscene) production, it would be nice to know how it will look, using the final text.

It's very common, that some letters looking good in the font itself, but not when used in a real text, consisting of different words and phrases.

To check, if the letters of the font work nicely together, you can cut'n'paste them one by one to form a complete textpage, which can take hours. Or you can use a tool to do the same job in a few seconds: **Chartist**

Chartist reads your graphicsfile with the letters (the font/charset), your textfile with all those words/phrases and will output a new graphicsfile, showing your text by using your pixeled letters, simple as that.

Information
========
Pixeled fonts are often used in demos for [Retrocomputers](https://en.wikipedia.org/wiki/Retrocomputing) like [Amiga](https://en.wikipedia.org/wiki/Amiga), [Atari ST](https://en.wikipedia.org/wiki/Atari_ST), [Commodore 64](https://en.wikipedia.org/wiki/Commodore_64), etc.

From [Wikipedia](https://en.wikipedia.org/wiki/Demoscene): 

> The demoscene is a computer art subculture that specializes in producing demos, which are audio-visual presentations that run in real-time on a computer. The main goal of a demo is to show off programming, artistic, and musical skills.

Those fonts are often starting with the **SPACE**-Symbol (*Pos. 32*) and ending with the **Z**-Letter (*Pos. 90*) of the [ASCII-Table](https://en.wikipedia.org/wiki/ASCII#Character_set). If your font is not ordered this *ascii-relative* way, you can simply create a [mapping table](https://github.com/PhilSwiss/chartist/blob/master/font-mappingtable.txt) with the correct order.

Most of those fonts have a fixed size, e.g. **8** by **8** pixels, **16** by **16** pixels and so on. But some symbols like the **.** (dot) or the **,** (comma) look a bit lost when placed in such a grid. To avoid this, you can create a [width table](https://github.com/PhilSwiss/chartist/blob/master/font-widthtable.txt) to define letters or symbols with a smaller width.

The **background color** is simply *auto-detected* by looking which color is used by the majority of the pixels in the font-image. But you can set it manually, if the wrong color is choosen.

The **size** of the letters is *auto-detected* by the height (*y-axis*) of the font-image. If it does not work, you can also set this value manually, expecially when the letters are arranged in multiple lines instead of one, single line.


Requirements
=============

- Python (3.5, 3.6, 3.7, 3.8, 3.9) - https://www.python.org/
- Pillow (Python Imaging Library) - https://pypi.org/project/Pillow/


Installation
=============
If missing, **Pillow** can be installed using **pip**.

Linux: 

    $ pip install pillow
Windows:

    $ python -m pip install pillow


Quickstart
==========

**Chartist** is easy to use and really straightforward to generate a fontpage.
Just run `chartist` using the provided font and the test text:

    $ chartist.py font-oneliner-asciirelative.png testtext.txt

    The generated image should be displayed by the default imageviewer of the operating system.

Write the generated image to disk:

    $ chartist.py font-oneliner-asciirelative.png testtext.txt -o fontpage.gif
	
	The submited filetype ".gif" sets the format of the output file.

Force resolution of generated image:

    $ chartist.py font-oneliner-asciirelative.png testtext.txt -r 320 256

    Otherwise the resolution is calculated by the size of the chars and the amount of text.

Render a non ascii-relative font by using a mapping table:

    $ chartist.py font-oneliner-nonasciirelative.png testtext.txt -m font-mappingtable.txt

    Because the order of the font is assumed as ascii-relative by default.

You can also use fonts which are spread over multiple lines:

    $ chartist.py font-multiline-asciirelative.png testtext.txt -s 16 16

    In this case, you have to submit the size of the chars, because autodetection will not work.

Render a proportional font (some letters have different widths) by using a width table:

    $ chartist.py font-oneliner-asciirelative-flexwidth.png testtext.txt -w font-widthtable.txt

    By default the widths of the chars/letters are of a fixed size.


Commandline options
===================

    $ chartist.py --help

    Usage: chartist charsetfile textfile [OPTION...]
    Generate images from charsets and texts
    
    mandatory arguments:
       charsetfile        imagefile with chars (e.g.: .png, .jpg, etc.)
       textfile           textfile with textline(s) (plain ascii e.g.: .txt)

    optional arguments:
       -s, --size         size of the chars (x or x and y)
	   -w, --widthtable   textfile with widthtable if chars are not of the same width
	   -m, --mappingtable textfile with mappingtable if charset is not ascii-relative
       -o, --output       outputfile with rendered text (e.g.: .png, .jpg, etc.)
       -r, --resolution   resolution of imagefile with rendered text (x or x and y)
       -c, --color        backgroundcolor of imagefile with rendered text (R G B)
       -v, --version      show version info
       -h, --help         show this help

    The optional arguments are only needed if autodetection of size, resolution or
    color doesnt meet the required needs. The rendered image will only be saved, if
    an outputfile (-o/--output) is set. Otherwise the image will be shown by the os.
	The widthtable is just a textfile containing the letters, symbols, etc. and their
    individual widths one per line and seperated by a tab.
    The mappingtable is just a textfile containing all letters, symbols, etc. in the
    same order as they are positioned in the imagefile.

    examples:
       chartist charsetfile.png textfile.txt
       chartist chars.gif text.txt -o screen.png
       chartist font.tif scroll.txt -s 8 -r 320 256
       chartist letters.tif credits.txt -s 16 32 -r 256
       chartist graphic.jpg greets.txt -c 255 127 64 -o out.jpg
       chartist charset.png textfile.txt -s 16 38 -l mappingtable.txt
       chartist font.png textfile.txt -s 16 16 -w widthtable.txt

Files
=====

* chartist.py (the commandlinetool itself)
* font-oneliner-asciirelative.png (a simple pixeled font/charset in ascii-relative order)
* font-oneliner-nonrelative.png (the same font/charset in a non ascii-relative order, see mappingtable)
* font-oneliner-asciirelative-flexwidth.png (the same font/charset with flexible/proportional widths, see widthtable)
* font-multiline-asciirelative.png (the same font/charset spread over multiple lines)
* font-mappingtable.txt (example of a mappingtable for the non ascii-relative font/charset)
* font-widthtable.txt (example of a widthtable for the flexwidth font/charset)


Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them to the issue tracker at https://github.com/PhilSwiss/chartist/issues


Contributing
============

Development of `chartist` happens at GitHub: https://github.com/PhilSwiss/chartist
