#!/usr/bin/env python3

from PIL import Image, ImageTk
import sys
from tkinter import Tk, Canvas
from dataclasses import dataclass
from typing import List

@dataclass
class Pixel:
    x: int
    y: int

@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int

g_pixel_values: List[Pixel] = [] # this is a global to avoid stackoverflow on big images

class Viewver:
    def __init__(self, all_rects, fp, width, height):
        self.fen = Tk()
        self.fen.title(fp + " - " + str(width) + "x" + str(height))
        self.can = Canvas(self.fen, width=width, height=height, highlightthickness=0)
        self.can.pack(fill="both", expand=True)
        self.image = Image.open(fp)
        self.all_rects = all_rects
        self.width = width
        self.height = height
        self.scale_factor = 1
        self.viewx = 0
        self.show_text = False
        self.viewy = 0
        self.draw()

        self.fen.bind_all("<Escape>", self.quit)
        self.fen.bind_all("<p>", self.zoom_in)
        self.fen.bind_all("<r>", self.reset_view)
        self.fen.bind_all("<t>", self.toggle_show_text)
        self.fen.bind_all("<m>", self.zoom_out)
        self.fen.bind_all("<Right>", self.move_right)
        self.fen.bind_all("<Left>", self.move_left)
        self.fen.bind_all("<Up>", self.move_up)
        self.fen.bind_all("<Down>", self.move_down)

        self.fen.mainloop()


    def toggle_show_text(self, evt=None):
        self.show_text = not self.show_text
        self.draw()


    def reset_view(self, evt=None):
        self.viewx = 0
        self.viewy = 0
        self.scale_factor = 1
        self.show_text = False
        self.draw()

    def move_right(self, evt=None):
        self.viewx -= 40
        self.draw()


    def move_left(self, evt=None):
        self.viewx += 40
        self.draw()


    def move_up(self, evt=None):
        self.viewy += 40
        self.draw()


    def move_down(self, evt=None):
        self.viewy -= 40
        self.draw()


    def quit(self, evt=None):
        self.fen.quit()
        self.fen.destroy()


    def zoom_in(self, evt=None):
        self.scale_factor += 1
        self.draw()


    def zoom_out(self, evt=None):
        if self.scale_factor > 0:
            self.scale_factor -= 1
        self.draw()


    def draw(self):
        win_width, win_height = self.fen.winfo_width(), self.fen.winfo_height()

        self.can.delete("all")
        self.image = self.image.resize((self.width*self.scale_factor, self.height*self.scale_factor), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.can.create_image(self.viewx*self.scale_factor, self.viewy*self.scale_factor, anchor="nw", image=self.photo)
        for r in self.all_rects:
            x1 = ((r.x1*self.scale_factor) + (self.viewx*self.scale_factor))
            y1 = ((r.y1*self.scale_factor) + (self.viewy*self.scale_factor))
            if (win_width != 1 and x1 > win_width) or (win_height > 1 and y1 > win_height):
                continue
            if x1 < 0 or y1 < 0:
                continue
            x2 = (r.x2 + r.x1 + self.viewx) * self.scale_factor
            y2 = (r.y2 + r.y1 + self.viewy) * self.scale_factor
            self.can.create_rectangle(x1, y1, x2, y2)
            if self.show_text:
                self.can.create_text(x1+10, y1-10, text=str(r.x1)) # nw
                self.can.create_text(x2-10, y1-10, text=str(r.x2)) # ne
                self.can.create_text(x1+10, y2+10, text=str(r.y1)) # sw
                self.can.create_text(x2-10, y2+10, text=str(r.y2)) # se


class RectFinder:
    def __init__(self):
        pass


    def get_adjacents_pixels(self, width: int, height: int, y: int, x: int) -> List[Pixel]:
        global g_pixel_values
        arr = []

        if g_pixel_values[(width * y) + x] == 0:
            return []

        arr.append(Pixel(x, y))
        g_pixel_values[(width * y) + x] = 0

        if y > 0 and g_pixel_values[width * (y-1) + (x)] != 0: # N
            arr += self.get_adjacents_pixels(width, height, y-1, x)
        if y < height-1 and g_pixel_values[width * (y+1) + (x)] != 0: # S
            arr += self.get_adjacents_pixels(width, height, y+1, x)
        if x > 0 and g_pixel_values[width * (y) + (x-1)] != 0: # W
            arr += self.get_adjacents_pixels(width, height, y, x-1)
        if x < width-1 and g_pixel_values[width * (y) + (x+1)] != 0: # E
            arr += self.get_adjacents_pixels(width, height, y, x+1)

        if y > 0 and x < width-1 and g_pixel_values[width * (y-1) + (x+1)] != 0: # NE
            arr += self.get_adjacents_pixels(width, height, y-1, x+1)
        if y < height-1 and x < width-1 and g_pixel_values[width * (y+1) + (x+1)] != 0: # SE
            arr += self.get_adjacents_pixels(width, height, y+1, x+1)
        if x > 0 and y > 0 and g_pixel_values[width * (y-1) + (x-1)] != 0: # NW
            arr += self.get_adjacents_pixels(width, height, y-1, x-1)
        if y < height-1 and x > 0 and g_pixel_values[width * (y+1) + (x-1)] != 0: # SW
            arr += self.get_adjacents_pixels(width, height, y+1, x-1)
        return arr


    def get_rect_bounds(self, shape, image_witdh, image_height):
        ymin = image_height
        xmin = image_witdh
        ymax = 0
        xmax = 0
        for pixel in shape:
            if pixel.y < ymin:
                ymin = pixel.y
            elif pixel.y > ymax:
                ymax = pixel.y
            if pixel.x < xmin:
                xmin = pixel.x
            elif pixel.x > xmax:
                xmax = pixel.x
        return xmin, ymin, (xmax-xmin+1), (ymax-ymin+1)


    def find_rects(self, image_witdh: int, image_height: int) -> List[Rect]:
        global g_pixel_values
        already_visited = []
        all_rects = []

        for y in range(image_height):
            for x in range(image_witdh):
                if g_pixel_values[image_witdh * y + x] != 0 and (y, x) not in already_visited: # non transparent pixel
                    shape = self.get_adjacents_pixels(image_witdh, image_height, y, x)
                    x1,y1,x2,y2 = self.get_rect_bounds(shape, image_witdh, image_height)
                    min_size = 0
                    if not (x1 < min_size or x2 < min_size or y1 < min_size or y2 < min_size):
                        # all_rects.append([x1,y1,x2,y2])
                        all_rects.append(Rect(x1,y1,x2,y2))
                    else:
                        # print(x1, y1, x2, y2)
                        pass
                    already_visited += shape
        return all_rects


def main(argc: int, argv: List[str]):
    global g_pixel_values

    bin_name = argv[0]
    argc -= 1
    argv = argv[1:]

    if argc != 1:
        sys.exit(f"USAGE: {bin_name} spritesheet")
    try:
        im = Image.open(argv[0], 'r')
    except:
        sys.exit("Could not read/load image")
    image_witdh, image_height = im.size
    g_pixel_values = list(im.getdata())
    r = RectFinder()
    all_rects = r.find_rects(image_witdh, image_height)
    # print(all_rects)
    Viewver(all_rects, argv[0], image_witdh, image_height)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
