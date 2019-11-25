from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
# from tkinter import Image as tkImage
from PIL import Image, ImageTk
import os
import DrawScheme
FONT = ("Comic Sans", 15, "bold")


def save_new_el():
    if img == -1:
        mb.showerror("Ошибка", "Выберите изображение")
        return
    if e_name.get() == '':
        mb.showerror("Ошибка", "Введите имя элемента")
        return
    if e_name.get() in DrawScheme.el_types:
        mb.showerror("Ошибка", "Элемент с таким именем уже существует")
        return
    type_el = int(up) + int(right) + int(down) + int(left)
    if type_el == 3:
        if not up:
            dirs = ['u', 'r', 'd', 'l']
        elif not right:
            dirs = ['r', 'd', 'l', 'u']
        elif not down:
            dirs = ['d', 'l', 'u', 'r']
        else:
            dirs = ['l', 'u', 'r', 'd']
    elif type_el == 1:
        if up:
            dirs = ['u', 'r', 'd', 'l']
        elif right:
            dirs = ['r', 'd', 'l', 'u']
        elif down:
            dirs = ['d', 'l', 'u', 'r']
        else:
            dirs = ['l', 'u', 'r', 'd']
    elif type_el == 2:
        if up or down:
            dirs = ['v', 'h']
        else:
            dirs = ['h', 'v']
    else:
        dirs = ['0']
    if len(dirs) > 1:
        os.mkdir(os.getcwd() + "/Im_el/" + e_name.get())
        for i in range(len(dirs)):
            img.rotate(-90 * i).save("Im_el/" + e_name.get() + '/' + dirs[i] + '.png')
    else:
        img.save("Im_el/" + e_name.get() + '.png')
    DrawScheme.el_types[e_name.get()] = type_el
    with open("Im_el/elements.txt", "a") as fo:
        print(e_name.get() + ' ' + str(type_el), file=fo)
    r_add.destroy()


def up_change():
    global up
    up = not up
    b_up['bg'] = "darkblue" if up else "#ddddff"
    b_up['activebackground'] = "darkblue" if up else "#ddddff"


def right_change():
    global right
    right = not right
    b_right['bg'] = "darkblue" if right else "#ddddff"
    b_right['activebackground'] = "darkblue" if right else "#ddddff"


def down_change():
    global down
    down = not down
    b_down['bg'] = "darkblue" if down else "#ddddff"
    b_down['activebackground'] = "darkblue" if down else "#ddddff"


def left_change():
    global left
    left = not left
    b_left['bg'] = "darkblue" if left else "#ddddff"
    b_left['activebackground'] = "darkblue" if left else "#ddddff"


def name(path):
    res = ''
    for c in path[::-1]:
        if c == '/':
            return res
        res = c + res
    return res


def select():
    filename = fd.askopenfilename(filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    global img, tk_img
    img = Image.open(filename)
    tk_img = PhotoImage(file=filename)
    picture = Label(r_add, image=tk_img)
    picture.grid(row=2, column=1)
    select_im.destroy()


def add_el():
    global r_add, up, down, right, left, b_up, b_down, b_right, b_left, select_im, img, e_name
    img = -1
    r_add = Toplevel()
    r_add.title("Добавление элемента")
    r_add['bg'] = "lightblue"
    label = Label(r_add, text="Выберите изображние и отметьте стороны с соединением",
                  bg="lightblue", font=FONT, wraplength=280)
    select_im = Button(r_add, text="Выбрать\nФормат:.png\nРазмер:\n100x100px", command=select, bg="gray80", activebackground="gray85",
                       fg="red", activeforeground="red", font=FONT, width=10, height=6)
    b_up = Button(r_add, text='', bg="#ddddff", activebackground="#ddddff",
                  width=15, height=2, command=up_change)
    b_right = Button(r_add, text='', bg="#ddddff", activebackground="#ddddff",
                  width=2, height=10, command=right_change)
    b_left = Button(r_add, text='', bg="#ddddff", activebackground="#ddddff",
                  width=2, height=10, command=left_change)
    b_down = Button(r_add, text='', bg="#ddddff", activebackground="#ddddff",
                  width=15, height=2, command=down_change)
    label2 = Label(r_add, text="Имя:", font=FONT, bg="lightblue")
    e_name = Entry(r_add, width=24)
    b_add = Button(r_add, text="Добавить", bg="orange", activebackground="#ffaf00", font=FONT, command=save_new_el)
    up, right, left, down = False, False, False, False
    label.grid(row=0, column=0, columnspan=3, padx=20, pady=10)
    b_up.grid(row=1, column=1)
    b_down.grid(row=3, column=1)
    b_left.grid(row=2, column=0, sticky=E)
    b_right.grid(row=2, column=2, sticky=W)
    select_im.grid(row=2, column=1)
    label2.grid(row=4, column=0, sticky=W)
    e_name.grid(row=4, column=1, columnspan=2, sticky=W)
    b_add.grid(row=6, column=0, columnspan=3, sticky=N+S+W+E, padx=20, pady=10)
    r_add.mainloop()


def save():
    with open("Im_el/elements.txt", 'w') as fo:
        print("ELEMENT_SIZE", scale_size.get(), file=fo)
        print("TAB", scale_tab.get() // 2, file=fo)
        print("WIRE_WIDTH", DrawScheme.WIRE_WIDTH, file=fo, end='')
        for i, j in DrawScheme.el_types.items():
            print('\n' + i, j, end='', file=fo)


DrawScheme.load_base()
r = Tk()
r.title("Настройки рисования схем")
r['bg'] = "#ddffff"
l1 = Label(r, text="Настройки рисования схемы", font=FONT, bg="#ddffff")
l_el_size = Label(r, text="Размер изображения элемента в пикселях", font=FONT, bg="#ddffff", fg="blue")
l_tab = Label(r, text="Длина соединения между элементами в пикселях", font=FONT, bg="#ddffff", fg="blue")
scale_size = Scale(r, from_=40, to=300, bg="#ddffff", tickinterval=20, orient=HORIZONTAL, length=600)
scale_size.set(DrawScheme.EL_SIZE)
scale_tab = Scale(r, from_=0, to=30, bg="#ddffff", orient=HORIZONTAL, length=600, resolution=2)
scale_tab.set(DrawScheme.TAB * 2)
f1 = Frame(r, bg="#ddffff")
b_new_el = Button(f1, text="Добавить элемент", font=FONT, bg="#eeffee", activebackground="#f0fff0", command=add_el)
b_save = Button(f1, text="Сохранить", font=FONT, bg="#ffeeee", activebackground="#fff0f0", command=save)
l1.pack(padx=20, pady=10)
l_el_size.pack(padx=20, pady=5)
scale_size.pack(padx=20, pady=5)
l_tab.pack(padx=20, pady=5)
scale_tab.pack(padx=20, pady=5)
f1.pack(padx=20)
b_save.pack(padx=5, pady=10, side=LEFT)
b_new_el.pack(padx=5, pady=10, side=RIGHT)

r.mainloop()
