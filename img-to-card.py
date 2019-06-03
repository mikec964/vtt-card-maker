#!/usr/bin/env python3

import os
from PIL import Image
import random
import sys

dpi = 70
card_size = (2.5 * dpi, 3.5 * dpi)
# art_size = (2.25 * dpi, 3.25 * dpi)
art_size = (151, 225)
# art_offset = (0.125 * dpi, 0.125 * dpi)
art_offset = (12, 10)
shadow = 4


def getCardList(src_path):
    """Return list of card file names.

    Return list of image file names,
    given a folder.
    """
    files = os.listdir(src_path)
    jpgs = []
    for f in files:
        try:
            with Image.open(os.path.join(src_path, f)) as im:
                jpgs.append(f)
        except IOError:
            pass
    return jpgs


def cardify(src_path, card_name):
    """Resize, apply white borders and shadow."""

    # stack images:
    # 3. outer border with shadow
    # 2. card art
    # 1. inner border with center hole
    outer = Image.open('00 poker card shadow.png')
    art = Image.open(os.path.join(src_path, card_name))
    art = art.resize(art_size)  # fit inside inner border
    # place inside on white card bg
    outer.paste(art, art_offset)
    # round corners of inside image
    inner = Image.open('00 poker card shadow.png')
    outer.paste(inner, (0,0), inner)
    return outer


def tilt(card):
    """Apply -1 to +1 degree rotation to cards"""

    degrees = random.randint(-10, 10) / 10
    print(degrees)
    tilted = card.rotate(degrees, expand=1)
    return tilted


def main():
    random.seed(None)
    sources = sys.argv[1:]
    for src_path in sources:
        dest_path = os.path.split(src_path)[1] + ' with VTT border'
        print(f'src_path = {src_path}, dest_path = {dest_path}')
        card_names = getCardList(src_path)
        try:
            os.mkdir(dest_path)
        # except Exception as e:
        #     raise
        # else:
        #     pass
        finally:
            pass
    
        for src_card in card_names:
            print(src_card)
            card = cardify(src_path, src_card)
            (card_name, ext) = os.path.splitext(src_card)
            card_name = card_name + '.png'
            print(f"{src_card} saved as {card_name}")
            card.save(os.path.join(dest_path, card_name), 'PNG', optimize=True)
            # card.show()
            # card = tilt(card)
            # card.show()


if __name__ == "__main__":
    main()
