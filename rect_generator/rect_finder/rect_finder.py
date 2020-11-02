from rect_generator.data.data import Pixel, Rect
from typing import List

class RectFinder:
    def __init__(self):

        pass


    def get_adjacents_pixels(self, pixel_values, width: int, height: int, y: int, x: int):
        arr_all_pixels = []
        to_visit = []

        to_visit.append(Pixel(y, x))

        while to_visit != []:
            pix = to_visit.pop()
            arr_all_pixels.append(pix)
            pixel_values[width * (y) + (x)] = 0
            x = pix.x
            y = pix.y

            if y > 0 and pixel_values[width * (y-1) + (x)] != 0: # N
                to_visit.append(Pixel(y-1, x))
            if y < height-1 and pixel_values[width * (y+1) + (x)] != 0: # S
                to_visit.append(Pixel(y+1, x))
            if x > 0 and pixel_values[width * (y) + (x-1)] != 0: # W
                to_visit.append(Pixel(y, x-1))
            if x < width-1 and pixel_values[width * (y) + (x+1)] != 0: # E
                to_visit.append(Pixel(y, x+1))

            if y > 0 and x < width-1 and pixel_values[width * (y-1) + (x+1)] != 0: # NE
                to_visit.append(Pixel(y-1, x+1))
            if y < height-1 and x < width-1 and pixel_values[width * (y+1) + (x+1)] != 0: # SE
                to_visit.append(Pixel(y+1, x+1))
            if x > 0 and y > 0 and pixel_values[width * (y-1) + (x-1)] != 0: # NW
                to_visit.append(Pixel(y-1, x-1))
            if y < height-1 and x > 0 and pixel_values[width * (y+1) + (x-1)] != 0: # SW
                to_visit.append(Pixel(y+1, x-1))
        return arr_all_pixels


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


    def rect_contains(self, r1, r2) -> bool:
        return (r2.x1+r2.x2) < (r1.x1+r1.x2) and \
                                (r2.x1) > (r1.x1) and \
                                    (r2.y1) > (r1.y1) and \
                                        (r2.y1+r2.y2) < (r1.y+r1.h)


    def merge_rects(self, all_rects):
        clean_rects = []
        current = None

        return all_rects
        for r in all_rects:
            current = r
            # if
        return clean_rects


    def find_rects(self, pixel_values, image_witdh: int, image_height: int) -> List[Rect]:
        all_rects = []
        for y in range(image_height):
            for x in range(image_witdh):
                if pixel_values[image_witdh * y + x] != 0:
                    shape = self.get_adjacents_pixels(pixel_values, image_witdh, image_height, y, x)
                    x1,y1,x2,y2 = self.get_rect_bounds(shape, image_witdh, image_height)
                    min_size = 0
                    if not (x1 < min_size or x2 < min_size or y1 < min_size or y2 < min_size):
                        all_rects.append(Rect(x1,y1,x2,y2))
                    else:
                        pass
        return self.merge_rects(all_rects)
