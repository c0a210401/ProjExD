import tkinter as tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym

def key_up(event):
    global key
    key = ""

def main_proc():
    global cx, cy, mx, my, tori
    mas_d = {
        ""     : [0, 0],
        "Up"   : [0, -1],
        "Down" : [0, +1],
        "Left" : [-1, 0],
        "Right": [+1, 0],
    }
    try:
        if maze[my+mas_d[key][1]][mx+mas_d[key][0]] == 0:
            my, mx = my+mas_d[key][1], mx+mas_d[key][0]
    except:
        pass
    cx, cy = mx*100+50, my*100+50
    bunsin()
    if my == 7 and mx == 13:
        tori = tk.PhotoImage(file="fig/6.png")
        canvas.create_image(cx, cy, image=tori, tag="tori")
    canvas.coords("tori", cx, cy)
    root.after(100, main_proc)

def sandg():
    global cx, cy
    canvas.create_rectangle(100, 100, 100+100, 100+100, 
            fill="blue")

    canvas.create_rectangle(1300, 700, 1300+100, 700+100, 
            fill="red")

def bunsin():
    sandg()
    canvas.create_image(cx, cy, image=tori, tag="tori")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")

    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()
    maze = mm.make_maze(15, 9)
    mm.show_maze(canvas, maze)

    tori = tk.PhotoImage(file="fig/8.png")
    mx, my = 1, 1
    cx, cy = mx*100+50, my*100+50
    canvas.create_image(cx, cy, image=tori, tag="tori")
    
    key = ""

    root.bind("<KeyPress>", key_down)
    root.bind("<KeyRelease>", key_up)
    main_proc()

    root.mainloop()