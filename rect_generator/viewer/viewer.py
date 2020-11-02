from PIL import Image, ImageTk
from tkinter import Tk, Canvas


class Viewver:
    def __init__(self, all_rects, fp, width, height):
        self.fen = Tk()
        # self.fen.geometry("100x100+-1000+400")
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
        if self.scale_factor > 1:
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
            if (win_width != 1 and x1 > win_width) or (win_height > 1 and \
                                        y1 > win_height) or x1 < 0 or y1 < 0:
                continue
            x2 = (r.x2 + r.x1 + self.viewx) * self.scale_factor
            y2 = (r.y2 + r.y1 + self.viewy) * self.scale_factor
            self.can.create_rectangle(x1, y1, x2, y2)
            if self.show_text:
                self.can.create_text(x1+10, y1-10, text=str(r.x1)) # nw
                self.can.create_text(x2-10, y1-10, text=str(r.x2)) # ne
                self.can.create_text(x1+10, y2+10, text=str(r.y1)) # sw
                self.can.create_text(x2-10, y2+10, text=str(r.y2)) # se


def run(all_rects, fp, width, height):
    Viewver(all_rects, fp, width, height)
