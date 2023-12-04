import tkinter as tk
import customtkinter as ctk
import ast
import operator

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

opdict = {ast.Add: operator.add, ast.Sub: operator.sub, ast.USub: operator.neg, ast.Mult: operator.mul,
             ast.Div: operator.truediv, ast.Pow: operator.pow}
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

def calculate():
    try:
        tree = ast.parse(entry.get(), mode='eval').body
        result = evaluate(tree)
        historyline = f"{entry.get()} = {result}"
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        history_label = ctk.CTkLabel(history_frame, text=historyline)
        history_label.pack()

    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")


def evaluate(tree):
    if isinstance(tree, ast.Num):
        return tree.n
    elif isinstance(tree, ast.BinOp):
        return opdict[type(tree.op)](evaluate(tree.left), evaluate(tree.right))


def cancel():
    entry.delete(0, ctk.END)
    entry.insert(0, "")


root = ctk.CTk()
root.geometry("400x720")
root.title("Calculator")
entry = ctk.CTkEntry(root, height=80, width=350, font=("Roboto", 20))
entry.grid(row=0, column=0, columnspan=4)

row_val = 1
col_val = 0

for button in buttons:
    ctk.CTkButton(root, text=button, font=("Roboto", 26), width=80, height=60, border_width=1, border_color="white", hover_color="#6b84ff", command=lambda b=button: entry.insert(tk.END, b)
    if b != '=' else calculate()).grid(row=row_val, column=col_val, sticky="ew", padx=10, pady=10)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

cButton = ctk.CTkButton(root, text="C", font=("Roboto", 26), width=80, height=30, border_width=1,
                      border_color="white", hover_color="#6b84ff", command=cancel).grid(row=row_val, column=col_val, sticky="ew", padx=10, pady=10, columnspan=4)

history_frame = ctk.CTkScrollableFrame(root, width=300, label_text="Historique")
history_frame.grid(row=row_val+1, column=col_val, columnspan=4)

root.mainloop()