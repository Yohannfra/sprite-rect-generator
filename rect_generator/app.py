from PIL import Image
import sys
from dataclasses import dataclass
from typing import List, Tuple
import time
from rect_generator.rect_finder import rect_finder
from rect_generator.viewer import viewer

def main(argc: int, argv: List[str]):
    argc -= 1
    argv = argv[1:]

    if argc != 1:
        sys.exit(f"USAGE: rect_generator spritesheet")
    try:
        im = Image.open(argv[0], 'r')
    except:
        sys.exit("Could not read/load image")
    image_witdh, image_height = im.size
    pixel_values = list(im.getdata())
    r = rect_finder.RectFinder()
    start_time = time.time()
    all_rects = r.find_rects(pixel_values, image_witdh, image_height)
    end_time = time.time()
    print(
        f"Found {len(all_rects)} rectangles in {round(end_time-start_time, 3)} s")
    viewer.run(all_rects, argv[0], image_witdh, image_height)
