import tkinter as tk
import tkinter.messagebox as tkm
import math

if __name__ ==  "__main__":
    root = tk.Tk()
    root.title("tk")

    def button_click(event):
        btn = event.widget
        txt = btn["text"]
        entry.insert(tk.END, txt)

    def Symbol(event):
        btn = event.widget
        txt = btn["text"]
        form = entry.get()[-1]
        if "+" in form or "-" in form or "*" in form or "/" in form:
            tkm.showinfo("エラー", "記号は連続できません")
        else:
            entry.insert(tk.END, txt)

    def Equal(event):
        btn = event.widget
        txt = btn["text"]
        ans = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(tk.END, ans)
        tkm.showinfo("結果", f"[{txt}]ボタンが押されました 計算完了")

    def Convert(event):
        num = entry.get()
        if "+" in num or "-" in num or "*" in num or "/" in num:
            tkm.showinfo("エラー", "計算し終えてください")
        else:
            try:
                new_num = int(num)
                entry.delete(0, tk.END)
                entry.insert(tk.END, float(new_num))
            except ValueError:
                new_num = float(num)
                entry.delete(0, tk.END)
                entry.insert(tk.END, int(new_num))
            
    def All_clear(event):
        entry.delete(0, tk.END)

    def one_clear(event):
        l = len(entry.get())
        entry.delete(l-1, tk.END)

    def kai(event):
        try:
            num = int(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, math.factorial(num))
            math.factorial(5)
        except ValueError:
            tkm.showinfo("エラー", "整数のみでしか計算できません")

    r,c = 2,0
    for text in [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]:
        btn = tk.Button(root,
                        text=f"{text}",
                        height=1,
                        width=4,
                        font=("Times New Roman", 30)
                        )
        btn.bind("<1>", button_click)
        if text == 0:
            c = 1
        btn.grid(row=r, column=c)
        c += 1
        if c == 3:
            r += 1
            c = 0
    
    r_s,c_s  = 1,4
    for word in ["+", "-", "*", "/"]: 
        sym = tk.Button(root, 
                        text=f"{word}", 
                        height=1,
                        width=4,
                        font=("Times New Roman", 30)
                        )
        sym.bind("<1>", Symbol)
        sym.grid(row=r_s, column=c_s)
        r_s += 1
    
    entry = tk.Entry(justify=tk.RIGHT, width=10, font=("Times New Roman", 40))
    entry.grid(row=0, column=0, columnspan=5)

    button_equ = tk.Button(root, text="=", height=1, width=4, font=("Times New Roman", 30))
    button_equ.grid(row=5, column=4)
    button_equ.bind("<1>", Equal)

    button_oclear = tk.Button(root, text="x!", height=1, width=4, font=("Times New Roman", 30))
    button_oclear.grid(row=5, column=0)
    button_oclear.bind("<1>", kai)

    button_con = tk.Button(root, text="i/f", height=1, width=4, font=("Times New Roman", 30))
    button_con.grid(row=5, column=2)
    button_con.bind("<1>", Convert)

    button_oclear = tk.Button(root, text="c", height=1, width=4, font=("Times New Roman", 30))
    button_oclear.grid(row=1, column=1)
    button_oclear.bind("<1>", one_clear)

    button_clear = tk.Button(root, text="All", height=1, width=4, font=("Times New Roman", 30))
    button_clear.grid(row=1, column=2)
    button_clear.bind("<1>", All_clear)

    root.mainloop()