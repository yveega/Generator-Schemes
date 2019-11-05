from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageTk

EL_SIZE = 100
TAB = 5
WIRE_WIDTH = 6
h_or_v_els = {"battery", "switch", "resister"}
tri_els = {"transistor"}
one_els = {"contact+", "contact-"}


class Cell:
    def __init__(self, s, row, column):
        data_cell = s.split()
        print(data_cell)
        self.is_el = data_cell[0] != '-'
        self.up = bool(int(data_cell[1]))
        self.right = bool(int(data_cell[2]))
        self.down = bool(int(data_cell[3]))
        self.left = bool(int(data_cell[4]))
        if self.is_el:
            if data_cell[0] in h_or_v_els:
                if self.up or self.down:
                    self.img_name = "Im_el/" + data_cell[0] + "/v.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/h.png"
            elif data_cell[0] in tri_els:
                if not self.up:
                    self.img_name = "Im_el/" + data_cell[0] + "/u.png"
                elif not self.right:
                    self.img_name = "Im_el/" + data_cell[0] + "/r.png"
                elif not self.left:
                    self.img_name = "Im_el/" + data_cell[0] + "/l.png"
                else:
                    self.img_name = "Im_el/" + data_cell[0] + "/d.png"
            elif data_cell[0] in one_els:
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
            print(self.img_name)
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


def draw(scheme):
    cells = []
    for i in range(len(scheme)):
        for j in range(len(scheme[i])):
            cells.append(Cell(scheme[i][j], j, i))
    W = len(scheme[0]) * (EL_SIZE + TAB * 2)
    H = len(scheme) * (EL_SIZE + TAB * 2)
    im = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for el in cells:
        el.draw_on_image(draw, im)
    del draw
    return im


def read_from_file(file):
    with open(file, 'r') as fi:
        data = []
        for line in fi:
            data.append(line.strip().split('\t'))
    return data


def save():
    filename = fd.asksaveasfilename(filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    im.save(filename)


def work():
    global ph_im, im
    filename = fd.askopenfilename(filetypes=(("TXT files", "*.txt"), ("All files", "*.*")))
    scheme = read_from_file(filename)
    for line in scheme:
        print('  '.join(line))
    b_open.destroy()
    label.destroy()
    im = draw(scheme)
    ph_im = ImageTk.PhotoImage(im)
    picture = Label(r, image=ph_im)
    picture.pack(padx=20, pady=20)
    b_save = Button(r, text="Экспорт в PNG", font=("Comic Sans", 19, "bold"), bg="#ffdddd", fg="orange",
                    activebackground="#ffe8e8", activeforeground="orange", command=save)
    b_save.pack(side=LEFT, padx=20, pady=20)
    r.update()


###################################################
# main code

r = Tk()
r.title("Электрические схемы")
r['bg'] = "#ffddff"
label = Label(r, text="Выберите файл с электрической схемой", font=("Comic Sans", 15, "bold"), bg="#ffddff", fg="blue")
b_open = Button(r, text="Открыть", font=("Comic Sans", 19, "bold"), bg="#ddddff", fg="purple",
                activebackground="#e8e8ff", activeforeground="purple", command=work)
label.pack(padx=20, pady=20)
b_open.pack(padx=20, pady=20)

r.mainloop()
