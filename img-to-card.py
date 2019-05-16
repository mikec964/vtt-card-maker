#!/usr/bin/env python3

import os
from PIL import Image

deck_path = '/Users/mikec/Documents/gaming/DriveThruRPG/Just Insert Imagination/Pirate cards, renamed'
dpi = 70
card_size = (2.5 * dpi, 3.5 * dpi)
shadow = 7


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

    card_l1 = Image.open('00 poker card border.png')
    card_src = Image.open(os.path.join(deck_path, cards[0]))
    card_src = card_src.resize((151, 225))  # fit inside inner border
    # place inside on white card bg
    card_l1.paste(card_src, (12, 10))
    # round corners of inside image
    card_l1.paste(Image.open('00 poker card border.png'), (0,0), Image.open('00 poker card border.png'))
    card_l1.show()
    return

def main():
    cards = getCardList(deck_path)
    print(cards)
    c1 = Image.open(os.path.join(deck_path, cards[0]))
    c1.show()

    cardify(cards, card_size, 0)

if __name__ == "__main__":
    main()
