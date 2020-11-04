from PIL import Image, ImageTk
from tkinter import Tk, Canvas, Toplevel, Button
import tkinter.messagebox


class Viewver:
    def __init__(self, all_rects, fp, width, height):
        self.fen = Tk()
        self.fen.title(fp + " - " + str(width) + "x" + str(height))
        self.fen.geometry("1280x720")
        self.can = Canvas(self.fen, width=width, height=height, highlightthickness=0, bg="white")
        self.can.pack(fill="both", expand=True)
        self.initial_image = Image.open(fp)
        self.all_rects = all_rects
        self.width = width
        self.height = height
        self.scale_factor = 1
        self.viewx = 0
        self.show_text = False
        self.viewy = 0
        self.selected_rect = None
        self.modify_rect_mode = False
        self.draw_all()

        self.fen.bind_all("<Escape>", self.quit)
        self.fen.bind("<p>", self.zoom_in)
        self.fen.bind("<r>", self.reset_view)
        self.fen.bind("<t>", self.toggle_show_text)
        self.fen.bind("<u>", self.toggle_modif_rect_mode)
        self.fen.bind("<1>", self.handle_click)
        self.fen.bind("<m>", self.zoom_out)
        self.fen.bind("<Right>", self.handle_right)
        self.fen.bind("<Left>", self.handle_left)
        self.fen.bind("<Up>", self.handle_up)
        self.fen.bind("<Down>", self.handle_down)

        self.fen.bind("<Shift-Right>", self.handle_shift_right)
        self.fen.bind("<Shift-Left>", self.handle_shift_left)
        self.fen.bind("<Shift-Up>", self.handle_shift_up)
        self.fen.bind("<Shift-Down>", self.handle_shift_down)

        # DEBUG ONLY
        # self.fen.geometry("800x400+-1000+400")
        # self.scale_factor = 5
        # self.draw_all()
        # ----

        self.fen.mainloop()



    def toggle_modif_rect_mode(self, evt):
        if self.selected_rect != None:
            self.modify_rect_mode = not self.modify_rect_mode
            self.draw_rects()


    def handle_click(self, evt):
        ''' check if click is within a rect '''
        x = evt.x / self.scale_factor
        y = evt.y / self.scale_factor

        offset_x = self.viewx * self.scale_factor
        offset_y = self.viewy * self.scale_factor
        found = False

        for r in self.all_rects:
            if r.x1+offset_x < x and r.x2 + r.x1+offset_x > x and \
                        r.y1+offset_y < y and r.y2 + r.y1 + offset_y > y:
                if r != self.selected_rect:
                    self.modify_rect_mode = False
                    self.selected_rect = r
                    print(r)
                    self.draw_rects()
                else:
                    self.selected_rect = None
                    self.modify_rect_mode = False
                    self.draw_rects()
                found = True

        if not found and self.selected_rect != None:
            self.selected_rect = None
            self.draw_rects()



    def toggle_show_text(self, evt=None):
        self.show_text = not self.show_text
        self.draw_all()


    def reset_view(self, evt=None):
        self.viewx = 0
        self.viewy = 0
        self.scale_factor = 1
        self.show_text = False
        self.draw_all()

    def handle_right(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.x2 += 1
            self.draw_rects()
        else:
            self.viewx -= 40
            self.draw_all()


    def handle_left(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.x1 -= 1
            self.selected_rect.x2 += 1
            self.draw_rects()
        else:
            self.viewx += 40
            self.draw_all()


    def handle_up(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.y1 -= 1
            self.selected_rect.y2 += 1
            self.draw_rects()
        else:
            self.viewy += 40
            self.draw_all()


    def handle_down(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.y2 += 1
            self.draw_rects()
        else:
            self.viewy -= 40
            self.draw_all()


    def handle_shift_right(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.x1 += 1
            self.selected_rect.x2 -= 1
            self.draw_rects()


    def handle_shift_left(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.x2 -= 1
            self.draw_rects()


    def handle_shift_up(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.y2 -= 1
            self.draw_rects()


    def handle_shift_down(self, evt):
        if self.modify_rect_mode:
            self.selected_rect.y1 += 1
            self.selected_rect.y2 -= 1
            self.draw_rects()


    def quit(self, evt=None):
        if tkinter.messagebox.askokcancel(title="Quit", message="Quit ?"):
            self.fen.quit()
            self.fen.destroy()


    def zoom_in(self, evt=None):
        self.scale_factor *= 2
        self.draw_all()


    def zoom_out(self, evt=None):
        new_factor = self.scale_factor / 2
        if new_factor <= 0.1:
            tkinter.messagebox.showerror(title="Error", message="you can't zoom out anymore")
        else:
            self.scale_factor = new_factor
            self.draw_all()


    def draw_rects(self):
        win_width, win_height = self.fen.winfo_width(), self.fen.winfo_height()

        self.can.delete("rect")
        self.can.delete("selected_rect")
        self.can.delete("txt")

        for r in self.all_rects:
            x1 = ((r.x1*self.scale_factor) + (self.viewx*self.scale_factor))
            y1 = ((r.y1*self.scale_factor) + (self.viewy*self.scale_factor))
            if (win_width != 1 and x1 > win_width) or (win_height > 1 and \
                                        y1 > win_height) or x1 < 0 or y1 < 0:
                continue
            x2 = (r.x2 + r.x1 + self.viewx) * self.scale_factor
            y2 = (r.y2 + r.y1 + self.viewy) * self.scale_factor
            if r == self.selected_rect:
                if self.modify_rect_mode:
                    self.can.create_rectangle(x1, y1, x2, y2, tag="selected_rect", outline="green", width=2)
                else:
                    self.can.create_rectangle(x1, y1, x2, y2, tag="selected_rect", outline="red", width=2)
            else:
                self.can.create_rectangle(x1, y1, x2, y2, tag="rect")
            if self.show_text or r == self.selected_rect:
                self.can.create_text(x1+10, y1-10, text=str(r.x1), tag="txt") # nw
                self.can.create_text(x2-10, y1-10, text=str(r.x2), tag="txt") # ne
                self.can.create_text(x1+10, y2+10, text=str(r.y1), tag="txt") # sw
                self.can.create_text(x2-10, y2+10, text=str(r.y2), tag="txt") # se


    def draw_image(self):
        self.can.delete("img")

        self.image = self.initial_image.resize((int(self.width*self.scale_factor), int(self.height*self.scale_factor)), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.can.create_image(self.viewx*self.scale_factor, self.viewy*self.scale_factor, anchor="nw", image=self.photo, tag="img")


    def draw_all(self):
        ''' draw both rects and image '''
        self.draw_image()
        self.draw_rects()


def run(all_rects, fp, width, height):
    Viewver(all_rects, fp, width, height)
