from PIL import Image
import sys
from dataclasses import dataclass
from typing import List, Tuple
from signal import signal, SIGINT
import time
from rect_generator.rect_finder import rect_finder
from rect_generator.viewer import viewer


def clean_pixel_array(arr):
    '''
    This function is needed because PIL.Image.getdata()
    output depends of the file type
    int -> gif
    (int, int, int) -> rgb -> jpeg
    (int, int, int, int) -> rgba -> png
    '''
    for i in range(len(arr)):
        if arr[i] == 0 or \
            (type(arr[i]) != int and len(arr[i]) == 3 and arr[i] == (0,0,0)) or \
                (type(arr[i]) != int and len(arr[i]) == 4 and arr[i][3] == 0):
            arr[i] = 0
        else:
            arr[i] = 1


def sigint_handler(signal_received, frame):
    ''' quit faster when tkinter is lagging with the draw '''
    print("SIGINT or CTRL-C detected. Bye")
    exit(1)


def main(argc: int, argv: List[str]):
    signal(SIGINT, sigint_handler)

    argc -= 1
    argv = argv[1:]

    if argc != 1:
        sys.exit(f"USAGE: rect_generator spritesheet")
    try:
        print(f"Reading {argv[0]}")
        im = Image.open(argv[0], 'r')
    except:
        sys.exit("Could not read/load image")
    image_width, image_height = im.size
    pixel_values = list(im.getdata())
    print("Cleaning pixels")
    clean_pixel_array(pixel_values)
    print("Searching for rectangles")
    r = rect_finder.RectFinder()
    start_time = time.time()
    all_rects = r.find_rects(pixel_values, image_width, image_height)
    end_time = time.time()
    print(
        f"Found {len(all_rects)} rectangles in {round(end_time-start_time, 3)} s")
    print("Starting gui")
    viewer.run(all_rects, argv[0], image_width, image_height)
    print("Bye")
