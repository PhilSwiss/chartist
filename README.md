Chartist
========

Commandline tool to generate images from charsets and texts. For more information on these topics:

* [Demoscene](https://en.wikipedia.org/wiki/Demoscene) (article explaning the demoscene) © Wikipedia
* [Bitmapfonts](https://en.wikipedia.org/wiki/Computer_font) (article also explaning bitmap fonts) © Wikipedia
* [Pixelfonts](http://janeway.exotica.org.uk/search.php?what=0&special=&query=&cat=1630&show=128&tags=&effects=&gfxstyles=&collection_category=0&collection=&year=all&soundformat=&bitplanes=0&gfxsize=0&country=&more=hide) (pixel fonts from various demoscene productions) © Kestra Bitworld
* [GrafX2](http://grafx2.chez.com) (tool for creating and editing bitmap/pixel images and fonts)
* [Paint.net](https://www.getpaint.net) (another tool for working with pixel images and fonts)


Requirements:
=============

- Python (3.5, 3.6, 3.7, 3.8, 3.9) - https://www.python.org/
- Pillow (Python Imaging Library) - https://pypi.org/project/Pillow/


Installation:
=============
If missing, **Pillow** can be installed using **pip**.
Linux: 

    $ pip install pillow
Windows:

    $ python -m pip install pillow


Quickstart
==========

**Chartist** is easy to use and really straightforward to generate a fontpage.
Just run `chartist` using the provided font and the test text: ::

    $ chartist.py font-oneliner-asciirelative.png testtext.txt

The generated image should be displayed by the default imageviewer of the operating system.

Write the generated image to disk: ::

    $ chartist.py font-oneliner-asciirelative.png testtext.txt fontpage.png

Force resolution of generated image:  ::

    $ chartist.py font-oneliner-asciirelative.png testtext.txt -r 320 256

Otherwise the resolution is calculated by the size of the chars and the amount of text.


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
	   -m, --mappingtable textfile with mappingtable if charset is not ascii-relative
       -o, --output       outputfile with rendered text (e.g.: .png, .jpg, etc.)
       -r, --resolution   resolution of imagefile with rendered text (x or x and y)
       -c, --color        backgroundcolor of imagefile with rendered text (R G B)
       -v, --version      show version info
       -h, --help         show this help

    The optional arguments are only needed if autodetection of size, resolution or
    color doesnt meet the required needs. The rendered image will only be saved, if
    an outputfile (-o/--output) is set. Otherwise the image will be shown by the os.
    The mappingtable is just a textfile containing all letters, symbols, etc. in the
    same order as they are positioned in the imagefile.

    examples:
       chartist charsetfile.png textfile.txt
       chartist chars.gif text.txt -o screen.png
       chartist font.tif scroll.txt -s 8 -r 320 256
       chartist letters.tif credits.txt -s 16 32 -r 256
       chartist graphic.jpg greets.txt -c 255 127 64 -o out.jpg
       chartist charset.png textfile.txt -s 16 38 -l mappingtable.txt


Files
=====

* chartist.py (the commandlinetool itself)
* font-oneliner-asciirelative.png (a simple pixeled font/charset in ascii-relative order)
* font-oneliner-nonrelative.png (the same font/charset in a non ascii-relative order, see mappingtable)
* font-mappingtable.txt (example of a mappingtable for the non ascii-relative font/charset)


Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them to the issue tracker at https://github.com/PhilSwiss/chartist/issues


Contributing
============

Development of `chartist` happens at GitHub: https://github.com/PhilSwiss/chartist
