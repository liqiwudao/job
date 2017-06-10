#!/usr/bin/env python
# -*- coding: utf-8
from __future__ import print_function

import os, sys
import random
from PIL import Image
import imghdr
import base64


def ResizeImage(filein, fileout, width, height, i_type):
    img = Image.open(filein)
    out = img.resize((width, height), Image.ANTIALIAS)  # resize image with high-quality
    imgType = imghdr.what(filein)
    out.save(fileout, i_type)


def base64_img(data):
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    imgdata = base64.b64decode(data)
    return imgdata

# if __name__ == "__main__":
#     for infile in sys.argv[1:]:
#         try:
#             if 'jpg' in infile:
#                 pass
#             else:
#                 continue
#             fileout = '../bak/%s.jpg'%(random.randint(123123132, 9999999999))
#             width = 1193
#             height = 570
#             i_type = 'jpeg'
#             ResizeImage(infile, fileout, width, height, i_type)
#             im = Image.open(infile)
#             im.thumbnail(size)
#             im.save(outfile, "JPEG")
# except IOError:
#     print("cannot create thumbnail for", infile)
