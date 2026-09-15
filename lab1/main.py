import tkinter as tk
from tkinter import filedialog, Label, Button, Scale, Frame
from PIL import ImageTk

import histogram as hist
import image_processor as ip

orig_img = None
curr_img = None
file_path = ""

def show_image(img):
    temp = img.copy()
    temp.thumbnail((700, 700))
    tk_img = ImageTk.PhotoImage(temp)
    lbl_img.config(image=tk_img)
    lbl_img.image = tk_img


def open_file():
    global orig_img, curr_img, file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        orig_img = ip.load_img(file_path)
        curr_img = orig_img.copy()
        s_b.set(0)
        s_c.set(0)
        s_s.set(0)
        show_image(curr_img)


def save_file():
    if curr_img:
        save_path = filedialog.asksaveasfilename(defaultextension=".png")
        if save_path:
            ip.save_img(save_path, curr_img)


def update_filters(_=None):
    global curr_img
    if orig_img:
        curr_img = ip.change_bright(orig_img, s_b.get())
        curr_img = ip.change_contrast(curr_img, s_c.get())
        curr_img = ip.change_saturation(curr_img, s_s.get())
        show_image(curr_img)


def to_gray():
    global curr_img
    if curr_img:
        curr_img = ip.make_gray(curr_img)
        show_image(curr_img)


def rotate():
    global curr_img
    if curr_img:
        curr_img = ip.rotate_img(curr_img)
        show_image(curr_img)


def apply_lin():
    global curr_img
    if curr_img:
        curr_img = ip.lin_corr(curr_img)
        show_image(curr_img)


def apply_nonlin():
    global curr_img
    if curr_img:
        curr_img = ip.nonlin_corr(curr_img)
        show_image(curr_img)


def show_hist():
    if curr_img:
        hist.show_histogram(curr_img)


def print_info():
    if orig_img:
        info_txt = ip.get_info(orig_img, file_path)
        lbl_info.config(text=info_txt)


def print_exif():
    if orig_img:
        exif_txt = ip.get_exif(orig_img)
        lbl_exif.config(text=exif_txt)


def reset():
    global curr_img
    if orig_img:
        curr_img = orig_img.copy()
        s_b.set(0)
        s_c.set(0)
        s_s.set(0)
        show_image(curr_img)


root = tk.Tk()
root.title("обработчик фоток")
root.geometry("1920x1080")

left = Frame(root)
left.pack(side="left", padx=10, pady=10)

right = Frame(root)
right.pack(side="right", expand=True, fill="both", padx=10, pady=10)

Button(left, text="Открыть картинку", command=open_file, width=25).pack(pady=2)
Button(left, text="Сохранить картинку", command=save_file, width=25).pack(pady=2)

s_b = Scale(
    left,
    from_=-100,
    to=100,
    orient="h",
    label="Яркость",
    command=update_filters,
)
s_b.pack(fill="x")
s_c = Scale(
    left,
    from_=-100,
    to=100,
    orient="h",
    label="Контраст",
    command=update_filters,
)
s_c.pack(fill="x")
s_s = Scale(
    left,
    from_=-100,
    to=100,
    orient="h",
    label="Насыщенность",
    command=update_filters,
)
s_s.pack(fill="x")

Button(left, text="В оттенки серого", command=to_gray, width=25).pack(pady=2)
Button(left, text="Поворот 90°", command=rotate, width=25).pack(pady=2)
Button(left, text="Линейная коррекция", command=apply_lin, width=25).pack(
    pady=2
)
Button(left, text="Нелинейная коррекция", command=apply_nonlin, width=25).pack(
    pady=2
)
Button(left, text="Гистограмма", command=show_hist, width=25).pack(pady=2)

Button(left, text="Инфа о файле", command=print_info, width=25).pack(pady=2)
lbl_info = Label(left, text="", justify="left")
lbl_info.pack()

Button(left, text="EXIF", command=print_exif, width=25).pack(pady=2)
lbl_exif = Label(left, text="", justify="left")
lbl_exif.pack()

Button(left, text="Сбросить все", command=reset, width=25).pack(pady=5)

lbl_img = Label(right)
lbl_img.pack()

root.mainloop()