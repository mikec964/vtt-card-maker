#!/usr/bin/env python3

import os
from PIL import Image

deck_path = '/Users/mikec/Documents/gaming/DriveThruRPG/Just Insert Imagination/Pirate cards, renamed'
dpi = 70
card_size = (2.5 * dpi, 3.5 * dpi)
# art_size = (2.25 * dpi, 3.25 * dpi)
art_size = (151, 225)
# art_offset = (0.125 * dpi, 0.125 * dpi)
art_offset = (12, 10)
shadow = 4


def getCardList(deck_path):
    """Return list of card file names.

    Return list of image file names,
    given a folder.
    """
    files = os.listdir(deck_path)
    jpgs = []
    for f in files:
        try:
            with Image.open(os.path.join(deck_path, f)) as im:
                jpgs.append(f)
        except IOError:
            pass
    return jpgs


def cardify(card_name):
    """Resize, apply white borders and shadow."""

    # stack images:
    # 3. outer border with shadow
    # 2. card art
    # 1. inner border with center hole
    outer = Image.open('00 poker card shadow.png')
    art = Image.open(os.path.join(deck_path, card_name))
    art = art.resize(art_size)  # fit inside inner border
    # place inside on white card bg
    outer.paste(art, art_offset)
    # round corners of inside image
    inner = Image.open('00 poker card shadow.png')
    outer.paste(inner, (0,0), inner)
    return outer


def tilt(card):
    """Apply -1 to +1 degree rotation to cards"""

    tilted = card.rotate(1)
    tilted.show()
    return tilted


def main():
    card_names = getCardList(deck_path)
    print(card_names)

    card = cardify(card_names[0])
    card.show()
    # card = tilt(card)
    # card.show()


if __name__ == "__main__":
    main()
