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


class Node:
    def __init__(self, key, value, color, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.color = color  
        self.parent = parent
        self.left = left
        self.right = right

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, None, False)
        self.root = self.TNULL

    def insert(self, key, value):
        node = Node(key, value, True, None, self.TNULL, self.TNULL)
        parent = None
        temp = self.root
        
        while temp != self.TNULL:
            parent = temp
            if node.key < temp.key:
                temp = temp.left
            else:
                temp = temp.right
        
        node.parent = parent
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        
        if node.parent is None:
            node.color = False
            return
        
        if node.parent.parent is None:
            return
        
        self.fix_insert(node)

    def fix_insert(self, k):
        while k.parent.color == True:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == True:
                    u.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = False
                    k.parent.parent.color = True
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                
                if u.color == True:
                    u.color = False
                    k.parent.color = False
                    k.parent.parent.color = True
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = False
                    k.parent.parent.color = True
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = False

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y


def read_excel_and_compare(file_path, bplus_tree, redblack_tree):
    df = pd.read_excel(file_path)  
    
    start_time_bplus = time.time()  
    for _, row in df.iterrows(): 
        key = row[0]  
        value = row[1:]  
        bplus_tree.insert(key, value)
    end_time_bplus = time.time() 
    
    start_time_rb = time.time()  
    for _, row in df.iterrows(): 
        key = row[0]  
        value = row[1:] 
        redblack_tree.insert(key, value)
    end_time_rb = time.time()  
    
    time_bplus = end_time_bplus - start_time_bplus 
    time_rb = end_time_rb - start_time_rb  
    
    return time_bplus, time_rb


def load_file_and_process():
    file_path = filedialog.askopenfilename()
    if file_path:
        bplus_tree = BPlusTree(max_keys=4)
        redblack_tree = RedBlackTree()
        time_bplus, time_rb = read_excel_and_compare(file_path, bplus_tree, redblack_tree)
        result_label.config(text=f"B+ Tree: {time_bplus:.6f} segundos\nRubro-Negra: {time_rb:.6f} segundos")
        messagebox.showinfo("Tempo de Execução", f"B+ Tree: {time_bplus:.6f} segundos\nRubro-Negra: {time_rb:.6f} segundos")

# Interface gráfica
root = tk.Tk()
root.title("FIFA - Comparação de Árvores B+ e Rubro-Negra")


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
