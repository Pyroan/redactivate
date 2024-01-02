'''Attempts to automatically redact specific phrases from pictures of text.
Designed for discord screenshots but honestly this version could be used for anything.
ALWAYS check the output before sharing anything that's supposed to be redacted.
Please.
'''
import argparse

from PIL import Image, ImageDraw

from ocr import OCRData

PALETTE = ['#ff00ff', '#00ffff', '#ffff00']


def highlight_phrase(draw: ImageDraw, phrase: str, ocrdata: OCRData, color: str = '#ff00ff', padding: int = 0, threshold: int = 0, debug: bool = False):
    phrase = phrase.strip().split()
    instances = ocrdata.fuzzysearch(phrase, threshold=threshold)
    for i in instances:
        x0, y0, _, _ = ocrdata.bbox(i)
        x1, y1, w1, h1 = ocrdata.bbox(i+len(phrase)-1)
        x0 -= padding
        y0 -= padding
        x1 += w1 + padding
        y1 += h1 + padding
        if debug:
            draw.rectangle([(x0, y0), (x1, y1)], outline=color)
        else:
            draw.rectangle([(x0, y0), (x1, y1)], fill=color)


parser = argparse.ArgumentParser(
    prog='redactivate', description="redacts screenshots and such")
parser.add_argument('imagepath')
parser.add_argument('phrases', nargs='+')
parser.add_argument('-d', '--debug', action='store_true',
                    help='highlight the phrases instead of redacting them')
parser.add_argument('-t', '--threshold', default=3, type=int,
                    help='how forgiving to make the search algorithm (3 by default)')
args = parser.parse_args()

with Image.open(args.imagepath) as img:
    draw = ImageDraw.Draw(img)
    data = OCRData.from_image(img, config=r'--psm 6')

    for i, p in enumerate(args.phrases):
        highlight_phrase(
            draw, p, data, PALETTE[i], 2, args.threshold, args.debug)
    img.show()
