from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
import requests
from io import BytesIO
from tkinter.filedialog import asksaveasfilename as saveAs
import pyperclip
from urllib.parse import urlparse


class Paint(object):

    DEFAULT_COLOR = 'red'

    def __init__(self):

        WIDTH = 454
        HEIGHT = 643

        self.root = Tk()
        self.root.attributes('-fullscreen', True)

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.text_button = Button(
            self.root, text='Text', command=self.use_text)
        self.text_button.grid(row=0, column=1)

        self.color_button = Button(
            self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(
            self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.save_button = Button(
            self.root, text='Save', command=self.save)
        self.save_button.grid(row=0, column=4)

        self.open_button = Button(
            self.root, text='Open', command=self.open)
        self.open_button.grid(row=0, column=5)

        self.choose_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.set(6)
        self.choose_size_button.grid(row=0, column=6)

        self.open()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.text_on = True
        self.active_button = self.text_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind("<Button-1>", self.textstart)
        self.c.bind("<Key>", self.keypress)

    def save(self):
        filename = saveAs(title="Save image as...", filetype=(
            ("PNG images", "*.png"), ("JPEG images", "*.jpg"), ("GIF images", "*.gif")))
        self.c.postscript(file=filename + '.eps')
        img = Image.open(filename + '.eps')
        img.save(filename + '.png', "png")

    def open(self):

        WIDTH = 454
        HEIGHT = 643

        url = pyperclip.paste()
        result = urlparse(url)
        if not(all([result.scheme, result.netloc, result.path])):
            url = 'http://www.megaworkbook.com/images/content/Maths/CountAndWrite/Count_And_Write_10.png'

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        img.save("new.png")
        bgi = PhotoImage(file="new.png")

        self.c = Canvas(self.root, bg='white',
                        width=WIDTH, height=HEIGHT)
        self.c.grid(row=1, columnspan=5)

        self.c.create_image(0, 0, anchor=NW, image=bgi)

        self.setup()
        self.root.mainloop()

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_text(self):
        self.activate_button(self.text_button, text_mode=True)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False, text_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode
        self.text_on = text_mode

    def keypress(self, event):
        if(self.old_x > 0 and event.char.isprintable()):
            paint_color = 'white' if self.eraser_on else self.color
            self.c.create_text(self.old_x, self.old_y,
                               anchor=W, text=event.char, font=("Purisa", self.line_width*3), fill=paint_color)
            self.old_x += self.line_width*3

    def textstart(self, event):
        if(self.text_on):
            self.old_x = event.x
            self.old_y = event.y
        self.c.focus_set()

    def paint(self, event):
        if(self.text_on):
            print((event.x, event.y))
        else:
            self.line_width = self.choose_size_button.get()
            paint_color = 'white' if self.eraser_on else self.color
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        if(self.text_on == False):
            self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()
