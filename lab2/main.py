from tkinter import Tk, Frame, Button, Label, Text, Entry, END, filedialog, messagebox
from PIL import Image, ImageTk
import image_processor as ip

orig_img = None
curr_img = None


def show_img(img):
    if img is None:
        return
    display_copy = img.copy()
    display_copy.thumbnail((720, 720))
    tk_img = ImageTk.PhotoImage(display_copy)
    lbl_img.config(image=tk_img)
    lbl_img.image = tk_img


def open_file():
    global orig_img, curr_img
    path = filedialog.askopenfilename(
        filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if path:
        orig_img = Image.open(path).convert("RGB")
        orig_img.thumbnail((900, 900))
        curr_img = orig_img.copy()
        show_img(curr_img)


def save_file():
    if curr_img is None:
        return
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
    )
    if path:
        save_copy = curr_img
        if path.lower().endswith((".jpg", ".jpeg")) and save_copy.mode == "RGBA":
            save_copy = save_copy.convert("RGB")
        save_copy.save(path)


def run_morph(op_name):
    global curr_img
    if curr_img is None:
        return
    try:
        kernel_text = txt_morph_kernel.get("1.0", END)
        curr_img = ip.apply_morphology(curr_img, op_name, kernel_text)
        show_img(curr_img)
    except Exception as e:
        messagebox.showerror("Ошибка матрицы", f"Проверьте ввод структурного элемента:\n{e}")


def run_sharpen():
    global curr_img
    if curr_img is None:
        return
    curr_img = ip.sharpen_img(curr_img)
    show_img(curr_img)


def run_motion_blur():
    global curr_img
    if curr_img is None:
        return
    curr_img = ip.motion_blur_img(curr_img, size=11)
    show_img(curr_img)


def run_emboss():
    global curr_img
    if curr_img is None:
        return
    curr_img = ip.emboss_img(curr_img)
    show_img(curr_img)


def run_custom_filter():
    global curr_img
    if curr_img is None:
        return
    try:
        kernel_text = txt_custom_kernel.get("1.0", END)
        curr_img = ip.custom_filter_img(curr_img, kernel_text)
        show_img(curr_img)
    except Exception as e:
        messagebox.showerror("Ошибка матрицы", f"Проверьте ввод пользовательской матрицы:\n{e}")


def run_median():
    global curr_img
    if curr_img is None:
        return
    try:
        ksize = int(ent_median.get())
        curr_img = ip.median_filter_img(curr_img, ksize=ksize)
        show_img(curr_img)
    except Exception as e:
        messagebox.showerror("Ошибка параметра", f"Введите целое нечетное число >= 3:\n{e}")


def reset_all():
    global curr_img
    if orig_img is not None:
        curr_img = orig_img.copy()
        show_img(curr_img)


root = Tk()
root.title("Лабораторная работа №2 — Морфологические преобразования")
root.geometry("1050x740")

left = Frame(root, padx=10, pady=10)
left.pack(side="left", fill="y")

right = Frame(root, padx=10, pady=10)
right.pack(side="right", expand=True, fill="both")

f_files = Frame(left)
f_files.pack(pady=2)
Button(f_files, text="Открыть", width=12, command=open_file).grid(row=0, column=0, padx=2)
Button(f_files, text="Сохранить", width=12, command=save_file).grid(row=0, column=1, padx=2)

Label(left, text="Структурный элемент (матрица):").pack(pady=(6, 0))
txt_morph_kernel = Text(left, height=4, width=26)
txt_morph_kernel.insert("1.0", "1 1 1 1 1\n1 1 1 1 1\n1 1 1 1 1\n1 1 1 1 1\n1 1 1 1 1")
txt_morph_kernel.pack(pady=2)

f_morph = Frame(left)
f_morph.pack(pady=2)
Button(f_morph, text="Эрозия", width=12, command=lambda: run_morph("erosion")).grid(row=0, column=0, padx=2, pady=1)
Button(f_morph, text="Дилатация", width=12, command=lambda: run_morph("dilation")).grid(row=0, column=1, padx=2, pady=1)
Button(f_morph, text="Открытие", width=12, command=lambda: run_morph("opening")).grid(row=1, column=0, padx=2, pady=1)
Button(f_morph, text="Закрытие", width=12, command=lambda: run_morph("closing")).grid(row=1, column=1, padx=2, pady=1)
Button(f_morph, text="Градиент", width=12, command=lambda: run_morph("gradient")).grid(row=2, column=0, padx=2, pady=1)
Button(f_morph, text="Цилиндр", width=12, command=lambda: run_morph("tophat")).grid(row=2, column=1, padx=2, pady=1)
Button(f_morph, text="Чёрная шляпа", width=26, command=lambda: run_morph("blackhat")).grid(row=3, column=0, columnspan=2, pady=1)

Label(left, text="Фильтры и эффекты:").pack(pady=(6, 0))
Button(left, text="Повышение резкости", width=26, command=run_sharpen).pack(pady=1)
Button(left, text="Размытие в движении", width=26, command=run_motion_blur).pack(pady=1)
Button(left, text="Тиснение", width=26, command=run_emboss).pack(pady=1)

Label(left, text="Пользовательская матрица:").pack(pady=(6, 0))
txt_custom_kernel = Text(left, height=3, width=26)
txt_custom_kernel.insert("1.0", "-1 -1 -1\n-1  9 -1\n-1 -1 -1")
txt_custom_kernel.pack(pady=2)
Button(left, text="Применить свою матрицу", width=26, command=run_custom_filter).pack(pady=1)

f_med = Frame(left)
f_med.pack(pady=(6, 2))
Label(f_med, text="Радиус медианы:").grid(row=0, column=0, padx=2)
ent_median = Entry(f_med, width=6, justify="center")
ent_median.insert(0, "5")
ent_median.grid(row=0, column=1, padx=2)
Button(left, text="Медианная фильтрация", width=26, command=run_median).pack(pady=1)

Button(left, text="Сбросить все", width=26, command=reset_all).pack(pady=(8, 2))

lbl_img = Label(right)
lbl_img.pack(expand=True)

root.mainloop()
