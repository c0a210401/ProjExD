import tkinter as tk
import tkinter.messagebox as tkm

if __name__ ==  "__main__":
    root = tk.Tk()
    root.title("tk")

    def button_click(event):
        btn = event.widget
        txt = btn["text"]
        entry.insert(tk.END, txt)
        tkm.showinfo(txt, f"[{txt}]ボタンが押されました")

    def Plus(event):
        btn = event.widget
        txt = btn["text"]
        form = entry.get()
        if "+" in form[-1]:
            tkm.showinfo("エラー", f"記号は連続できません")
        else:
            entry.insert(tk.END, txt)
            tkm.showinfo(txt, f"[{txt}]ボタンが押されました")

    def Equal(event):
        btn = event.widget
        txt = btn["text"]
        ans = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, ans)
        tkm.showinfo("結果", f"[{txt}]ボタンが押されました 計算完了")
    
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

    button_plus = tk.Button(root, text="+", font=("Times New Roman", 30), height=2, width=4, command=Plus)
    button_plus.grid(row=4, column=1)
    button_plus.bind("<1>", Plus)

    button_equ = tk.Button(root, text="=", font=("Times New Roman", 30), height=2, width=4, command=Equal)
    button_equ.grid(row=4, column=2)
    button_equ.bind("<1>", Equal)

    root.mainloop()