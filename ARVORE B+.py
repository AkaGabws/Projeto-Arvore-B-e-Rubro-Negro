import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

class BPlusTree:
    def __init__(self, max_keys=3):
        self.root = BPlusTreeNode(is_leaf=True)
        self.max_keys = max_keys

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.max_keys:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i][0]:
                i += 1
            node.keys.insert(i, (key, value))
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i][0]:
                i += 1
            if len(node.children[i].keys) == self.max_keys:
                self.split_child(node, i)
                if key > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def split_child(self, parent, index):
        child = parent.children[index]
        new_child = BPlusTreeNode(is_leaf=child.is_leaf)
        
        parent.keys.insert(index, child.keys[self.max_keys // 2])
        parent.children.insert(index + 1, new_child)
        
        new_child.keys = child.keys[self.max_keys // 2 + 1:]
        child.keys = child.keys[:self.max_keys // 2]
        
        if not child.is_leaf:
            new_child.children = child.children[self.max_keys // 2 + 1:]
            child.children = child.children[:self.max_keys // 2 + 1]


def read_excel_to_bplus_tree(file_path, bplus_tree):
    df = pd.read_excel(file_path)  
    
    start_time = time.time()  
    
    for _, row in df.iterrows():  
        key = row[0]  
        value = row[1:]  
        bplus_tree.insert(key, value)
    
    end_time = time.time()  
    
    return end_time - start_time  


def load_file_and_process():
    file_path = filedialog.askopenfilename()
    if file_path:
        bplus_tree = BPlusTree(max_keys=4)
        time_taken = read_excel_to_bplus_tree(file_path, bplus_tree)
        result_label.config(text=f"Resultado: Tempo para ler e inserir os dados: {time_taken:.6f} segundos")
        messagebox.showinfo("Tempo de Execução", f"Tempo para ler e inserir os dados: {time_taken:.6f} segundos")


root = tk.Tk()
root.title("FIFA - Inserção de Dados na Árvore B+")


root.geometry("400x500")
root.configure(bg="#2d2d2d")  


style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12), padding=10)


frame = ttk.Frame(root, padding="10 10 10 10", style="TFrame")
frame.pack(expand=True)


header_label = tk.Label(root, text="FIFA23", font=("Helvetica", 24, "bold"), bg="#2d2d2d", fg="white")
header_label.pack(pady=10)

sub_header_label = tk.Label(root, text="Insira a planilha com dados FIFA!", font=("Helvetica", 12), bg="#2d2d2d", fg="white")
sub_header_label.pack(pady=5)


icon_label = tk.Label(root, text="⚽", font=("Helvetica", 64), bg="#2d2d2d")
icon_label.pack(pady=10)


load_button = tk.Button(root, text="Carregar Planilha", font=("Helvetica", 12), bg="#28a745", fg="white", command=load_file_and_process)
load_button.pack(pady=20)


result_label = tk.Label(root, text="Resultado: Tempo não calculado", font=("Helvetica", 10), bg="#2d2d2d", fg="white")
result_label.pack(pady=10)

root.mainloop()
