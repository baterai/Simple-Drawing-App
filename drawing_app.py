import time
from tkinter import *
from tkinter import filedialog
import PIL.ImageGrab as ImageGrab
from tkinter import colorchooser, messagebox

window = Tk()

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

m_width = 1000
m_height = 600

c_width = 900
c_height = 500

window.title('draiwing app')
window.geometry("%dx%d" % (width, height))
window.minsize(m_width, m_height)

canvas = Canvas(window, width=c_width, height=c_height, bg='white')
canvas.pack()

def select_brush():
    global selected_colour
    selected_colour = priveous_colour

def change_brush_size(value):
    global brush_size
    brush_size = int(value)

def select_brush_size():
    brush_window = Toplevel(window)
    brush_window.title('brush size')
    brush_window.geometry('400x100')

    brush_size_label = Label(brush_window, text="Brush Size")
    brush_size_label.pack()

    brush_size_slider = Scale(brush_window, from_=1, to=25, orient=HORIZONTAL, command=change_brush_size)
    brush_size_slider.set(brush_size)
    brush_size_slider.pack()

def selected_eraser():
    global priveous_colour, selected_colour
    priveous_colour = selected_colour
    selected_colour = background_colour

def select_eraser_size():
    eraser_window = Toplevel(window)
    eraser_window.title('eraser size')
    eraser_window.geometry('400x100')

    eraser_size_label = Label(eraser_window, text="Eraser Size")
    eraser_size_label.pack()

    eraser_size_slider = Scale(eraser_window, from_=1, to=25, orient=HORIZONTAL, command=change_brush_size)
    eraser_size_slider.set(brush_size)
    eraser_size_slider.pack()

def select_colour():
    global priveous_colour, selected_colour
    
    colour = colorchooser.askcolor(title='Select Colour')[1]
    if colour:
        selected_colour = colour
        priveous_colour = colour

def clear_canvas():
    canvas.delete('all')

def save_canvas():
    filepath = filedialog.asksaveasfilename(defaultextension=' .png')

    time.sleep(1.0)
    
    x1 = window.winfo_rootx() + canvas.winfo_x()
    y1 = window.winfo_rooty() + canvas.winfo_y()

    x2 = x1 + canvas.winfo_width()
    y2 = y1 + canvas.winfo_height()

    if filepath:
        canvas.postscript(file=filepath, colormode='color')
        ImageGrab.grab().crop((x1,y1,x2,y2)).save(filepath)

def change_canvas_size():
    global c_height, c_width

    try:
        c_height = int(entry.get())
    except ValueError:
        messagebox.showerror("Error", f"Invalid width was entered defaulting to current height: {c_height}.")

    try:
        c_width = int(entry2.get())
    except ValueError:
        messagebox.showerror("Error", f"Invalid width was entered defaulting to current width: {c_width}.")

    canvas.config(height=c_height, width=c_width)


def canvas_size():
    global entry, entry2, c_width, c_height

    Size_window = Toplevel(window)
    Size_window.title('canvas size')
    Size_window.geometry('400x180')

    entry = Label(Size_window, text="canvas height")
    entry.pack()
    entry = Entry(Size_window, width=10)
    entry.pack()
    entry.insert(0, c_height)

    entry2 = Label(Size_window, text="canvas width")
    entry2.pack()
    entry2 = Entry(Size_window, width=10)
    entry2.pack()
    entry2.insert(0, c_width)

    button = Button(Size_window, text="confirm", width=10, command=change_canvas_size)
    button.pack()
    


menu_bar = Menu(window)

brush_menu = Menu(menu_bar, tearoff=0)
brush_menu.add_command(label="select brush", command=select_brush)
brush_menu.add_command(label="select brush size", command=select_brush_size)

colour_menu = Menu(menu_bar, tearoff=0)
colour_menu.add_command(label="select colour", command=select_colour)


eraser_menu = Menu(menu_bar, tearoff=0)
eraser_menu.add_command(label="select eraser", command=selected_eraser)
eraser_menu.add_command(label="select eraser size", command=select_eraser_size)

clear_menu = Menu(menu_bar, tearoff=0)
clear_menu.add_command(label="Clear canvas", command=clear_canvas)

canvas_menu = Menu(menu_bar, tearoff=0)
canvas_menu.add_command(label="save canvas", command=save_canvas)
canvas_menu.add_command(label="canvas size", command=canvas_size)

menu_bar.add_cascade(label='Brush', menu=brush_menu)
menu_bar.add_cascade(label='Colour', menu=colour_menu)
menu_bar.add_cascade(label='Eraser', menu=eraser_menu)
menu_bar.add_cascade(label='Clear', menu=clear_menu)
menu_bar.add_cascade(label='Canvas', menu=canvas_menu)

window.config(menu=menu_bar)



drawing = False

brush_size = 2
selected_colour = 'black'
priveous_colour = 'black'
background_colour = 'white'
last_x = 0
last_y = 0

def start_drawing(event):
    global drawing, last_x, last_y
    drawing = True
    last_x = event.x
    last_y = event.y
    

def draw(event):
    global drawing, last_x, last_y
    x = event.x
    y = event.y
    if drawing:
        canvas.create_oval((x - brush_size / 2, y - brush_size / 2, x + brush_size / 2, y + brush_size / 2), fill=selected_colour, outline=selected_colour)
        canvas.create_line(last_x, last_y, x, y, width=brush_size, fill=selected_colour)
        last_x = x 
        last_y = y 
    

def stop_drawing():
    global drawing
    drawing = False

canvas.bind('<Button-1>', start_drawing)
canvas.bind('<B1-Motion>', draw)
canvas.bind('<ButtonRelease-1>', stop_drawing)

window.mainloop()