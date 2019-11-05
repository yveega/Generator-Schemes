import sys
import random
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageDraw, ImageTk
types_of_els = ["resister", "battery", "switch", "lamp", "lamp", "lamp", "lamp", "switch"]
EL_SIZE = 100
TAB = 5
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


def make_field(sch):
    min_x = float("INF")
    min_y = float("INF")
    max_x = -float("INF")
    max_y = -float("INF")
    for cell in sch.keys():
        if cell[0] < min_x:
            min_x = cell[0]
        if cell[0] > max_x:
            max_x = cell[0]
        if cell[1] < min_y:
            min_y = cell[1]
        if cell[1] > max_y:
            max_y = cell[1]
    res = [["- 0 0 0 0"] * (max_y - min_y + 1) for _ in range(max_x - min_x + 1)]
    for cell in sch.keys():
        if sch[cell][0] == -1:
            el = '-'
        elif sch[cell][0] == -2:
            el = '+'
        else:
            el = els[sch[cell][0]][0]
        w1 = ' 1' if sch[cell][1] else ' 0'
        w2 = ' 1' if sch[cell][2] else ' 0'
        w3 = ' 1' if sch[cell][3] else ' 0'
        w4 = ' 1' if sch[cell][4] else ' 0'
        res[cell[0] - min_x][cell[1] - min_y] = el + w1 + w2 + w3 + w4
    return res


def print_in_file(name, field):
    with open(name, "w") as fo:
        for line in field:
            print('\t'.join(line), file=fo)


def merge_schemes(sch1, sch2):
    field1 = make_field(sch1)
    field2 = make_field(sch2)
    res = []
    TAB = ["- 0 0 0 0"]
    line = 0
    while line < min(len(field1), len(field2)):
        res.append(field1[line] + TAB + field2[line])
        line += 1
    while line < len(field1):
        res.append(field1[line])
        line += 1
    while line < len(field2):
        res.append(TAB * (len(field1[0]) + 1) + field2[line])
        line += 1
    return res


def conns(x1, y1, x2, y2):
    if x1 == x2 and y1 == y2:
        return False, False, False, False
    if x1 == x2 + 1:
        return True, False, False, False
    if x1 == x2 - 1:
        return False, False, True, False
    if y1 == y2 + 1:
        return False, False, False, True
    if y1 == y2 - 1:
        return False, True, False, False


def randomise(k_els):
    global els, saved_conns
    els = [random.choice(types_of_els) for _ in range(k_els)]
    saved_conns = [set()]
    for n in range(len(els) - 1):
        one = len(saved_conns) - 1
        two = random.randint(0, len(saved_conns) - 1)
        if two == len(saved_conns) - 1:
            two += 1
            saved_conns.append(set())
        els[n] = (els[n], one, two)
        saved_conns[one].add(n)
        saved_conns[two].add(n)
    els[-1] = (els[-1], 0, len(saved_conns) - 1)
    saved_conns[0].add(len(els) - 1)
    saved_conns[-1].add(len(els) - 1)


def change():
    if random.random() > 0.5:
        new_el = random.choice(types_of_els)
        num_change = random.randint(0, len(els) - 1)
        while new_el == els[num_change][0]:
            new_el = random.choice(types_of_els)
        els[num_change] = (new_el, els[num_change][1], els[num_change][2])


def up(scheme, group, x, y, straight):
    return (x - 1, y) not in used and go(scheme, group, x - 1, y, x, y, straight + 1)


def down(scheme, group, x, y, straight):
    return (x + 1, y) not in used and go(scheme, group, x + 1, y, x, y, straight + 1)


def right(scheme, group, x, y, straight):
    return (x, y + 1) not in used and go(scheme, group, x, y + 1, x, y, straight + 1)


def left(scheme, group, x, y, straight):
    return (x, y - 1) not in used and go(scheme, group, x, y - 1, x, y, straight + 1)


def go(scheme, group, x, y, x_last, y_last, straight=0):
    if straight > 7:
        # print("ESC1")
        return False
    if len(connections[group]) == 0:  # end of part of scheme
        # print("ESC2")
        return False
    used.add((x, y))
    c = conns(x, y, x_last, y_last)
    # print(x, y, 'from', x_last, y_last, ':', c, connections[group])
    # if (x, y) in scheme:
    #     print(scheme[(x, y)])
    if (x, y) not in scheme and (2 * x_last - x, 2 * y_last - y) not in scheme and (
        len(connections[group] - placed.keys()) > 0
    ) and not (
        x == x_last and y == y_last  # place element
    ):
        scheme[(x, y)] = ((connections[group] - placed.keys()).pop(), c[0], c[1], c[2], c[3])
        connections[group].remove(scheme[(x, y)][0])
        placed[scheme[(x, y)][0]] = (x, y)
        used.remove((x, y))
        return True
    elif (x, y) not in scheme:  # place wire
        now = [-1, c[0], c[1], c[2], c[3]]
        use_cell = False
        dirs = [up, right, down, left]
        num_dirs = {up: 1, right: 2, down: 3, left: 4}
        for _ in range(4):
            dir1 = random.choice(dirs)
            if dir1(scheme, group, x, y, straight):
                now[num_dirs[dir1]] = True
                use_cell = True
            dirs.remove(dir1)
        used.remove((x, y))
        if use_cell:
            scheme[(x, y)] = tuple(now)
            return True
        else:
            return False
    elif scheme[(x, y)][0] >= 0 and scheme[(x, y)][0] in connections[group] and (
            (scheme[(x, y)][1] or scheme[(x, y)][3]) == (c[0] or c[2])  # connect with placed earlier element
    ):
        now = scheme[(x, y)]
        connections[group].remove(now[0])
        scheme[(x, y)] = (now[0], now[1] or c[0], now[2] or c[1], now[3] or c[2], now[4] or c[3])
        used.remove((x, y))
        return True
    elif scheme[(x, y)][0] == -1:  # place + on wire
        now = scheme[(x, y)]
        if ((c[0] or c[2]) and not (now[1] or now[3])) or ((c[1] or c[3]) and not (now[2] or now[4])):
            if (2 * x - x_last, 2 * y - y_last) not in used and \
                    go(scheme, group, 2 * x - x_last, 2 * y - y_last, x, y, straight + 1):
                scheme[(x, y)] = (-2, True, True, True, True)
                used.remove((x, y))
                return True
            else:
                used.remove((x, y))
                # print("ESC3")
                return False
        else:
            used.remove((x, y))
            # print("ESC4")
            return False
    else:  # if can't use this cell
        used.remove((x, y))
        # print("ESC5")
        return False


def generate(scheme):
    global placed, used, connections
    created = False
    while not created:
        err = True
        scheme.clear()
        for i in scheme:
            del scheme[i]
        used = set()
        connections = []
        for i in saved_conns:
            connections.append(i.copy())
        placed = dict()
        START_C = random.randint(0, len(connections) - 1)
        # print('>>>>>>>>', START_C)
        # for cell in scheme:
        # print(cell, scheme[cell])
        go(scheme, START_C, 0, 0, 0, 0)
        placed_conns = {START_C}
        for i in range(len(connections)):
            start_el = -1
            for el in placed:
                if els[el][1] not in placed_conns or els[el][2] not in placed_conns:
                    start_el = el
                    break
            if start_el == -1:
                created = False
                break
            if els[start_el][1] not in placed_conns:
                # print('>>>>>>>', els[start_el][1])
                if scheme[placed[start_el]][1]:  # if up
                    if not go(scheme, els[start_el][1], placed[start_el][0] + 1, placed[start_el][1],
                              placed[start_el][0] + 1, placed[start_el][1]):
                        err = False
                        continue
                    placed_conns.add(els[start_el][1])
                elif scheme[placed[start_el]][2]:  # if right
                    if not go(scheme, els[start_el][1], placed[start_el][0], placed[start_el][1] - 1,
                              placed[start_el][0], placed[start_el][1] - 1):
                        err = False
                        break
                    placed_conns.add(els[start_el][1])
                elif scheme[placed[start_el]][3]:  # if down
                    if not go(scheme, els[start_el][1], placed[start_el][0] + 1, placed[start_el][1],
                              placed[start_el][0] + 1, placed[start_el][1]):
                        err = False
                        break
                    placed_conns.add(els[start_el][1])
                elif scheme[placed[start_el]][4]:  # if left
                    if not go(scheme, els[start_el][1], placed[start_el][0], placed[start_el][1] + 1,
                              placed[start_el][0], placed[start_el][1] + 1):
                        err = False
                        break
                    placed_conns.add(els[start_el][1])
                if len(connections[els[start_el][1]]) > 0:
                    err = False
                    break
            elif els[start_el][2] not in placed_conns:
                # print('>>>>>>>>', els[start_el][2])
                if scheme[placed[start_el]][1]:  # if up
                    if not go(scheme, els[start_el][2], placed[start_el][0] + 1, placed[start_el][1],
                              placed[start_el][0] + 1, placed[start_el][1]):
                        err = False
                        break
                    placed_conns.add(els[start_el][2])
                elif scheme[placed[start_el]][2]:  # if right
                    if not go(scheme, els[start_el][2], placed[start_el][0], placed[start_el][1] - 1,
                              placed[start_el][0], placed[start_el][1] - 1):
                        err = False
                        break
                    placed_conns.add(els[start_el][2])
                elif scheme[placed[start_el]][3]:  # if down
                    if not go(scheme, els[start_el][2], placed[start_el][0] + 1, placed[start_el][1],
                              placed[start_el][0] + 1, placed[start_el][1]):
                        err = False
                        break
                    placed_conns.add(els[start_el][2])
                elif scheme[placed[start_el]][4]:  # if left
                    if not go(scheme, els[start_el][2], placed[start_el][0], placed[start_el][1] + 1,
                              placed[start_el][0], placed[start_el][1] + 1):
                        err = False
                        break
                    placed_conns.add(els[start_el][2])
                if len(connections[els[start_el][2]]) > 0:
                    err = False
                    break
        if err:
            created = True


def draw_pare(k_els):
    global scheme1, scheme2
    randomise(k_els)
    # print(els)
    # print(saved_conns)
    scheme1 = dict()
    scheme2 = dict()
    generate(scheme1)
    change()
    generate(scheme2)
    return merge_schemes(scheme1, scheme2)


def dir_name(path):
    res = ''
    for c in path[::-1]:
        if c == '/':
            return res
        res = c + res
    return res


def choose_directory():
    global directory, choosed, l_dir
    directory = fd.askdirectory()
    l_dir = Label(r, text=dir_name(directory), font=("Comic Sans", 15), bg="#ffdddd", fg="#aa00ff")
    b_choose.destroy()
    l_dir.grid(row=0, column=1, sticky=W, pady=10, padx=5)
    choosed = True
    r.update()


def run():
    if not choosed:
        mb.showerror("Ошибка", "Выберите файл")
        return
    q = int(que.get())
    k = int(k_els.get())
    label1.destroy()
    label2.destroy()
    label3.destroy()
    l_dir.destroy()
    que.destroy()
    b_work.destroy()
    k_els.destroy()
    l_process = Label(r, text="Генерация: 0 из " + str(q), font=("Comic Sans", 15, "bold"), bg="#ffdddd", fg="purple")
    c = Canvas(r, width=1000, height=40, bg="#ddffdd")
    l_process.grid(row=0, column=0, padx=10, pady=5, sticky=W)
    c.grid(row=1, column=0, padx=10, pady=5)
    r.update()
    for i in range(q):
        im = draw(draw_pare(k))
        im.save(directory + '/' + str(i + 1) + ".png")
        l_process['text'] = "Генерация: " + str(i + 1) + " из " + str(q)
        c.create_rectangle(0, 0, int(1000 / q * (i + 1)), 40, fill="#0000dd")
        r.update()
    r.destroy()



r = Tk()
r.title("Генератор заданий")
r['bg'] = "#ffdddd"
label1 = Label(r, text="Папка для сгенерированных заданий:", font=("Comic Sans", 15, "bold"), bg="#ffdddd", fg="#ff00aa")
b_choose = Button(r, text="Выбрать", font=("Comic Sans", 15, "bold"), bg="#ffccff", fg="blue",
                  activeforeground="blue", activebackground="#ffd8ff", command=choose_directory)
label2 = Label(r, text="Количество заданий:", font=("Comic Sans", 15, "bold"), bg="#ffdddd", fg="#ff00aa")
que = Spinbox(r, width=10, from_=1, to=1000, font=("Comic Sans", 15))
label3 = Label(r, text="Количество элементов в схемах:", font=("Comic Sans", 15, "bold"), bg="#ffdddd", fg="#ff00aa")
k_els = Spinbox(r, width=10, from_=1, to=10, font=("Comic Sans", 15))
b_work = Button(r, text="Сгенерировать", font=("Comic Sans", 20, "bold"), bg="#ffffcc", fg="orange",
                  activeforeground="orange", activebackground="#ffffd8", command=run)
label1.grid(row=0, column=0, sticky=W, pady=10, padx=5)
b_choose.grid(row=0, column=1, sticky=W, pady=10, padx=5)
label2.grid(row=1, column=0, sticky=W, pady=10, padx=5)
que.grid(row=1, column=1, sticky=W, pady=10, padx=5)
label3.grid(row=2, column=0, sticky=W, pady=10, padx=5)
k_els.grid(row=2, column=1, sticky=W, pady=10, padx=5)
b_work.grid(row=3, column=0, columnspan=2, pady=10, padx=5)
choosed = False


r.mainloop()
