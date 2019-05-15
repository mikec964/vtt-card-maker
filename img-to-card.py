#!/usr/bin/env python3

from PIL import Image
import os


def getCardList(deck_path):
    """Return list of .jpg files."""
    files = os.listdir(deck_path)
    jpgs = []
    for f in files:
        if f.endswith('.jpg'):
            jpgs.append(f)
    return jpgs


def main():
    deck_path = '/Users/mikec/Documents/gaming/DriveThruRPG/Just Insert Imagination/Pirate cards, renamed'
    cards = getCardList(deck_path)
    print(cards)
    c1 = Image.open(os.path.join(deck_path, cards[1]))
    c1.show()

if __name__ == "__main__":
    main()

