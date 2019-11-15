from tkinter import *
from PIL import Image, ImageDraw, ImageTk, ImageFont


def load_base():
    global EL_SIZE, TAB, WIRE_WIDTH, el_types
    with open("Im_el/elements.txt", "r") as fo:
        data = []
        for line in fo:
            data.append(tuple(line.split()))
    EL_SIZE = int(data[0][1])
    TAB = int(data[1][1])
    WIRE_WIDTH = int(data[2][1])
    el_types = dict(data[3:])


class Cell:
    def __init__(self, s, row, column):
        data_cell = s.split()
        self.is_el = data_cell[0] != '-'
        self.up = bool(int(data_cell[1]))
        self.right = bool(int(data_cell[2]))
        self.down = bool(int(data_cell[3]))
        self.left = bool(int(data_cell[4]))
        if self.is_el:
            if el_types[data_cell[0]] == '2':
                if self.up or self.down:
                    self.img_name = "Im_el/" + data_cell[0] + "/v.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/h.png"
            elif el_types[data_cell[0]] == '3':
                if not self.up:
                    self.img_name = "Im_el/" + data_cell[0] + "/u.png"
                elif not self.right:
                    self.img_name = "Im_el/" + data_cell[0] + "/r.png"
                elif not self.left:
                    self.img_name = "Im_el/" + data_cell[0] + "/l.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/d.png"
            elif el_types[data_cell[0]] == '1':
                if self.up:
                    self.img_name = "Im_el/" + data_cell[0] + "/u.png"
                elif self.right:
                    self.img_name = "Im_el/" + data_cell[0] + "/r.png"
                elif self.left:
                    self.img_name = "Im_el/" + data_cell[0] + "/l.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/d.png"
            else:
                self.img_name = "Im_el/" + data_cell[0] + ".png"
        self.x = row * (EL_SIZE + 2 * TAB) + TAB
        self.y = column * (EL_SIZE + 2 * TAB) + TAB

    def draw_on_image(self, imdraw, im):
        if self.is_el:
            if self.up:
                imdraw.line([self.x + EL_SIZE // 2, self.y - 1, self.x + EL_SIZE // 2,
                                   self.y - TAB - 1], fill="black", width=WIRE_WIDTH)
            if self.right:
                imdraw.line([self.x + EL_SIZE, self.y + EL_SIZE // 2 - 1, self.x + EL_SIZE + TAB,
                                   self.y + EL_SIZE // 2 - 1], fill="black", width=WIRE_WIDTH)
            if self.down:
                imdraw.line([self.x + EL_SIZE // 2 - 1, self.y + EL_SIZE, self.x + EL_SIZE // 2 - 1,
                                   self.y + EL_SIZE + TAB], fill="black", width=WIRE_WIDTH)
            if self.left:
                imdraw.line([self.x - 1, self.y + EL_SIZE // 2, self.x - TAB - 1,
                                   self.y + EL_SIZE // 2], fill="black", width=WIRE_WIDTH)
            img = Image.open(self.img_name)
            im.paste(img, (self.x, self.y))
        else:
            if self.up:
                imdraw.line([self.x + EL_SIZE // 2, self.y + EL_SIZE // 2 + WIRE_WIDTH // 2 - 1, self.x + EL_SIZE // 2,
                                   self.y - TAB - 1], fill="black", width=WIRE_WIDTH)
            if self.right:
                imdraw.line([self.x + EL_SIZE // 2 - WIRE_WIDTH // 2, self.y + EL_SIZE // 2 - 1, self.x + EL_SIZE + TAB,
                                   self.y + EL_SIZE // 2 - 1], fill="black", width=WIRE_WIDTH)
            if self.down:
                imdraw.line([self.x + EL_SIZE // 2 - 1, self.y + EL_SIZE // 2 - WIRE_WIDTH // 2, self.x + EL_SIZE / 2 - 1,
                                   self.y + EL_SIZE + TAB], fill="black", width=WIRE_WIDTH)
            if self.left:
                imdraw.line([self.x + EL_SIZE // 2 + WIRE_WIDTH // 2 - 1, self.y + EL_SIZE // 2, self.x - TAB - 1,
                                   self.y + EL_SIZE // 2], fill="black", width=WIRE_WIDTH)


def draw(scheme, num=''):
    cells = []
    for i in range(len(scheme)):
        for j in range(len(scheme[i])):
            cells.append(Cell(scheme[i][j], j, i))
    W = len(scheme[0]) * (EL_SIZE + TAB * 2)
    H = len(scheme) * (EL_SIZE + TAB * 2)
    im = Image.new("RGB", (W, H), (255, 255, 255))
    im_draw = ImageDraw.Draw(im)
    for el in cells:
        el.draw_on_image(im_draw, im)
    font = ImageFont.truetype("UbuntuMono-B.ttf", 25)
    im_draw.text([5, 5], str(num), fill="black", align="right", font=font)
    del im_draw
    return im