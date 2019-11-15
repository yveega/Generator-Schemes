from DrawScheme import *
from tkinter import *
from tkinter import filedialog as fd


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

load_base()
r = Tk()
r.title("Электрические схемы")
r['bg'] = "#ffddff"
label = Label(r, text="Выберите файл с электрической схемой", font=("Comic Sans", 15, "bold"), bg="#ffddff", fg="blue")
b_open = Button(r, text="Открыть", font=("Comic Sans", 19, "bold"), bg="#ddddff", fg="purple",
                activebackground="#e8e8ff", activeforeground="purple", command=work)
label.pack(padx=20, pady=20)
b_open.pack(padx=20, pady=20)

r.mainloop()
