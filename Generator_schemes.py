from tkinter import *
EL_SIZE = 100
TAB = 25
WIRE_WIDTH = 6
h_or_v_els = {"battery", "switch", "resister"}


class Cell:
    def __init__(self, s, row, column):
        data_cell = s.split()
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
            else:
                self.img_name = "Im_el/" + data_cell[0] + ".png"
        self.x = row * (EL_SIZE + 2 * TAB) + TAB
        self.y = column * (EL_SIZE + 2 * TAB) + TAB

    def drow(self, canvas):
        if self.is_el:
            if self.up:
                canvas.create_line(self.x + EL_SIZE // 2, self.y, self.x + EL_SIZE // 2,
                                   self.y - TAB, fill="black", width=WIRE_WIDTH)
            if self.right:
                canvas.create_line(self.x + EL_SIZE, self.y + EL_SIZE // 2, self.x + EL_SIZE + TAB,
                                   self.y + EL_SIZE // 2, fill="black", width=WIRE_WIDTH)
            if self.down:
                canvas.create_line(self.x + EL_SIZE / 2, self.y + EL_SIZE, self.x + EL_SIZE / 2,
                                   self.y + EL_SIZE + TAB, fill="black", width=WIRE_WIDTH)
            if self.left:
                canvas.create_line(self.x, self.y + EL_SIZE // 2, self.x - TAB,
                                   self.y + EL_SIZE // 2, fill="black", width=WIRE_WIDTH)
            self.img = PhotoImage(file=self.img_name)
            canvas.create_image(self.x, self.y, anchor=NW, image=self.img)
        else:
            if self.up:
                canvas.create_line(self.x + EL_SIZE // 2, self.y + EL_SIZE // 2 + WIRE_WIDTH // 2, self.x + EL_SIZE // 2,
                                   self.y - TAB, fill="black", width=WIRE_WIDTH)
            if self.right:
                canvas.create_line(self.x + EL_SIZE // 2 - WIRE_WIDTH // 2, self.y + EL_SIZE // 2, self.x + EL_SIZE + TAB,
                                   self.y + EL_SIZE // 2, fill="black", width=WIRE_WIDTH)
            if self.down:
                canvas.create_line(self.x + EL_SIZE // 2, self.y + EL_SIZE // 2 - WIRE_WIDTH // 2, self.x + EL_SIZE / 2,
                                   self.y + EL_SIZE + TAB, fill="black", width=WIRE_WIDTH)
            if self.left:
                canvas.create_line(self.x + EL_SIZE // 2 + WIRE_WIDTH // 2, self.y + EL_SIZE // 2, self.x - TAB,
                                   self.y + EL_SIZE // 2, fill="black", width=WIRE_WIDTH)


with open("sch2.txt", 'r') as fi:
    data = []
    for line in fi:
        data.append(line.strip().split('\t'))

scheme = []

for i in range(len(data)):
    for j in range(len(data[i])):
        scheme.append(Cell(data[i][j], j, i))

r = Tk()
c = Canvas(r, width=1000, height=1000, bg="white")

els = []

for el in scheme:
    el.drow(c)

c.pack()
r.mainloop()
