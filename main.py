#!/usr/bin/env python
from PIL import Image
import piexif
import glob
import pdb
import logging
import argparse, os
import shutil
from datetime import datetime
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
def rotate_image(path):
    filename = os.path.basename(path)
    dst_dir = "backup"
    src_dir = os.path.dirname(path)
    img = Image.open(path)
    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
        if piexif.ImageIFD.Orientation in exif_dict["0th"]:
            orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
            if(orientation != 1):
                shutil.copy(path, dst_dir)
                logging.info(filename)
            #pdb.set_trace()
            exif_bytes = piexif.dump(exif_dict)
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
            img.save(path, exif=exif_bytes)
def main():
    logging.basicConfig(filename = f"{datetime.strftime(datetime.now(), '%Y-%m-%d')}.log", filemode='w',level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=dir_path)
    parsed_args = parser.parse_args()
    result = []
    for x in os.walk(parsed_args.path):
        for y in glob.glob(os.path.join(x[0], '*.jpg')):
            result.append(y)
    #pdb.set_trace()
    i = 0
    for i in range(len(result)):
        path = result[i]
        rotate_image(path)
if __name__ == '__main__':
    main()
