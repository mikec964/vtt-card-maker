#!/usr/bin/env python3

import os, errno
from PIL import Image
import random
import sys

class vttCards():
    """Creates a deck of cards optimized for VTT

    Inputs:
        * folder with card art, jokers, and deck back
    """

    def __init__(self, source_path):
        self.ppi = 72
        self.card_size = (2.5 * self.ppi, 3.5 * self.ppi)
        self.art_size = (151, 225)
        self.art_offset = (int(0.125 * self.ppi), int(0.125 * self.ppi))
        self.shadow = 4
        self.card_template = 'resources/poker card shadow.png'
        self.source_folder = source_path
        self.output_folder = self.source_folder + ' for Roll20'
        try:
            os.mkdir(self.output_folder)
        except Exception as e:
            if e.errno != errno.EEXIST:
                raise
        return

    def card_list(self):
        """Return list of card file names."""

        files = os.listdir(self.source_folder)
        jpgs = []
        for f in files:
            try:
                with Image.open(os.path.join(self.source_folder, f)) as im:
                    jpgs.append(f)
            except IOError:
                pass
        return jpgs

    def cardify(self, card_name):
        """Resize, apply white borders and shadow."""

        # stack images:
        # bottom layer: outer border with shadow
        outer = Image.open(self.card_template)
        # middle layer: card art
        art = Image.open(os.path.join(self.source_folder, card_name))
        art = art.resize(self.art_size)  # fit inside inner border
        outer.paste(art, self.art_offset)
        # top layer: inner border with center hole
        inner = Image.open(self.card_template)
        # round corners of inside image
        outer.paste(inner, (0,0), inner)
        return outer

    def tilt(self, card):
        """Apply -1.0 to +1.0 degree rotation to cards"""

        degrees = random.randint(-10, 10) / 10
        print(degrees)
        tilted = card.rotate(degrees, expand=1, resample=Image.BICUBIC)
        return tilted

    def save_cards(self):
        for src_card in self.card_list():
            print(src_card)
            card = self.cardify(src_card)
            card = self.tilt(card)
            (card_name, ext) = os.path.splitext(src_card)
            card_name = card_name + '.png'
            print(f"{src_card} saved as {card_name}")
            card.save(os.path.join(self.output_folder, card_name), 'PNG', optimize=True)
            # card.show()
        return

    def nameForRoll20(self, card_name):
        """Rename to meet Roll20 sorting requirements.

        c,d,h,s become ' of Clubs'
        10 becomes 'Ten'
        a,j,q,k become Ace, Jack, Queen, King
        j1,j2 become joker

        reference: https://ambitiouswithcards.com/new-deck-order/
        New Deck Order is TOP A-KH, A-KC, K-AD, K-AS, J2, J1 FACE
        red joker (J1) is the larger or more colorful one
        black joker is monochrome, and of lower rank
        """

        pass

def main():
    random.seed(None)
    source = sys.argv[1]
    print(f'param1= {source}')
    my_deck = vttCards(source)
    print(f'source = {my_deck.source_folder}, dest = {my_deck.output_folder}')
    print(my_deck.card_list())
    my_deck.save_cards()


if __name__ == "__main__":
    main()
