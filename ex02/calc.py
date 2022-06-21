import tkinter as tk
import tkinter.messagebox as tkm

if __name__ ==  "__main__":
    root = tk.Tk()
    root.title("tk")
    root.geometry("300x570")

    def button_click(event):
        btn = event.widget
        txt = btn["text"]
        tkm.showinfo(txt, f"[{txt}]ボタンが押されました")
    
    r,c = 1,0
    for text in range(9, -1, -1):
        btn = tk.Button(root, text = f"{text}", height=2, width=4, font=("Times New Roman", 30))
        btn.bind("<1>", button_click)
        btn.grid(row=r, column=c)
        c += 1
        if (text -1)%3 == 0:
            r += 1
            c = 0

    entry = tk.Entry(justify=tk.RIGHT, width=10, font=("Times New Roman", 40))
    entry.grid(row=0, column=0, columnspan=3)

    root.mainloop()