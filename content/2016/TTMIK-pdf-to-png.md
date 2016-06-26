Title: Converting TTMIK lessons from PDF to PNG files
Slug: TTMIK-pdf-to-png
Date: 2016-06-20 12:44
Tags: Anki, Korean, converting pdf to png, TTMIK, Python
Author: Laurens

I didn't just [scrape all TTMIK lessons]({filename}/2016/TTMIK-web-crawling.md) for archival purposes. What I really wanted is a structured way for me to study the lessons. I found that reading lessons without reviewing them regularly did not stick. If only there was a way to have some sorted of spaced repetition algorithm, perhaps something like [Anki](www.ankisrs.net)...

# Porting TTMIK content to Anki
One of the problems with the PDF files is that Anki and/or AnkiDroid do not have native support for PDF files. My initial solution was just to have little notes that referred to lessons, and I would have to pull the lesson on screen using some media device myself. Clearly, this was bothering as sometimes I just want to quickly review a lesson when a short timeslot becomes available during the day (yes, a toilet session is one of them). Luckily enough Anki does have image support which we can depend on.

The Python script at the bottom of this post serves to convert the PDF files of the lessons to PNG images. I have not used this script in a while and I might have broken it in the meantime. I highly doubt anyone will ever need it again as I will simply post the output myself. If someone out there happens to need this, please note that [ghostscript](http://www.ghostscript.com/download/gsdnld.html) is required.

### The python script
```python
import fnmatch
import os
import subprocess
import traceback
from PIL import Image, ImageChops
from math import ceil, floor
import sys


def gs_pdf_to_png(pdffilepath, output, resolution):
    """Converts a pdf to a png image
    """
    GHOSTSCRIPTCMD = "C:\\Program Files (x86)\\gs\\gs9.18\\bin\\gswin32.exe"
    if not os.path.isfile(pdffilepath):
        print("'%s' is not a file. Skip." % pdffilepath)
    pdfname, ext = os.path.splitext(pdffilepath)

    try:
        # Change the "-rXXX" option to set the PNG's resolution.
        # http://ghostscript.com/doc/current/Devices.htm#File_formats
        # For other commandline options see
        # http://ghostscript.com/doc/current/Use.htm#Options
        arglist = [GHOSTSCRIPTCMD,
                   "-dBATCH",
                   "-dNOPAUSE",
                   "-sOutputFile=" + output + "-%03d.png",
                   "-sDEVICE=png16m",
                   "-r%s" % resolution,
                   pdffilepath]
        print("Running command:\n%s" % ' '.join(arglist))
        sp = subprocess.Popen(
            args=arglist,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except OSError:
        sys.exit("Error executing Ghostscript ('%s'). Is it in your PATH?" %
                 GHOSTSCRIPTCMD)
    except:
        print("Error while running Ghostscript subprocess. Traceback:")
        print("Traceback:\n%s" % traceback.format_exc())

    stdout, stderr = sp.communicate()
    print("Ghostscript stdout:\n'%s'" % stdout)
    if stderr:
        print("Ghostscript stderr:\n'%s'" % stderr)


def merge_images(indexstr):
    """Merge documents in PNG format that include a header and footer.

    The header and footer are removed and are only added at the top and bottom of
    the merged image.
    """
    pngimgs = fnmatch.filter(os.listdir('.'), indexstr + '-*.png')
    width, height = Image.open(pngimgs[0]).size

    # In TTMIK lessons both the header and footer are each 10% of the height.
    # First save a copy of the header and footer.
    footer = Image.open(pngimgs[0]).crop((0, floor(height * 0.9), width, height))
    header = Image.open(pngimgs[0]).crop((0, 0, width, floor(height * 0.1)))

    # Create a list of images that will be merged. Starting with the header and
    # ending with the footer.
    images = [header]
    for i in range(len(pngimgs)):
        im = Image.open(pngimgs[i])
        im = im.crop((0, ceil(height * 0.1), width, ceil(height * 0.9)))
        images.append(crop_whitespace(im))
    images.append(footer)

    # Now merge the images
    total_height = sum([im.size[1] for im in images])
    new_im = Image.new('RGB', (width, total_height))
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += im.size[1]
    new_im.save(indexstr + '.png')


def crop_whitespace(image):
    """Remove surrounding empty space around an image.

    This implemenation assumes that the surrounding space has the same colour
    as the top leftmost pixel.
    """
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    print(bbox)
    if not bbox:
        return image
    return image.crop((0, 0, image.size[0], bbox[3]))


def delete_cache(indexstr):
    pngimgs = fnmatch.filter(os.listdir('.'), indexstr + '-*.png')
    for f in pngimgs:
        os.remove(f)


if __name__ == "__main__":
    os.chdir('C:\mydir')

    # First check where to start (in case process was interrupted previously)
    index = 1
    finishedimgs = fnmatch.filter(os.listdir('.'), '*.png')
    while '%03d.png' % index in finishedimgs:
        index += 1
    indexstr = '%03d' % index

    # Set the first PDF file we want to start with. Assumes that the PDF files start
    # with the prefix TTMIK xxx
    pdffile = fnmatch.filter(os.listdir('.'), 'TTMIK ' + indexstr + '*.pdf')[0]

    while len(pdffile) > 0:
        gs_pdf_to_png(pdffile, indexstr, 300)
        merge_images(indexstr)
        delete_cache(indexstr)

        index += 1
        indexstr = '%03d' % index
        pdffile = fnmatch.filter(os.listdir('.'), 'TTMIK ' + indexstr + '*.pdf')[0]

```
# The result: a TTMIK deck!
I have run the script and gathered the images. One example of a lesson looks like this after conversion:
> ![TTMIK lesson](https://ankiweb.net/shared/mpreview/816509991/0.png)

For my and your convenience I added all the images to a Anki deck and added some metadata. You can just grab this Anki deck and start studying the *talk to me in korean* lessons with discipline and efficiency! [Just grab it here](https://ankiweb.net/shared/info/816509991)
