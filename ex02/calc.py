import tkinter as tk
if __name__ ==  "__main__":
    root = tk.Tk()
    root.title("tk")
    root.geometry("300x500")

    r,c = 0,0
    for text in range(9, -1, -1):
        btn = tk.Button(root, text = f"{text}", height=2, width=4, font=("Times New Roman", 30))
        btn.grid(row=r, column=c)
        c += 1
        if (text -1)%3 == 0:
            r += 1
            c = 0
            
    root.mainloop()