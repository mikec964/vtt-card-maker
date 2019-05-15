#!/usr/bin/env python3

import os
from PIL import Image


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

def cardify(cards, card_size, shadow):
    """Resize, apply white borders and shadow."""
    return

def main():
    deck_path = '/Users/mikec/Documents/gaming/DriveThruRPG/Just Insert Imagination/Pirate cards, renamed'
    dpi = 70
    card_size = (2.5 * dpi, 3.5 * dpi)
    shadow = 7

    cards = getCardList(deck_path)
    print(cards)
    c1 = Image.open(os.path.join(deck_path, cards[0]))
    c1.show()

if __name__ == "__main__":
    main()
