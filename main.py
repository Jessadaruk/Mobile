# -*- coding: utf-8 -*-
import os, urllib.request, tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "train.csv")
URL = "https://raw.githubusercontent.com/koushik2299/Mobile-Price-Classification/main/train.csv"

FEATURES = ["battery_power","ram","int_memory","mobile_wt","n_cores","pc","talk_time"]
LABELS = ["แบตเตอรี่ (mAh)","RAM (MB)","หน่วยความจำ (GB)","น้ำหนัก (กรัม)",
          "จำนวน Core CPU","กล้องหลัง (MP)","เวลาสนทนา (ชม.)"]
PRICE = {0:"ราคาต่ำ",1:"ราคาปานกลาง",2:"ราคาสูง",3:"ราคาสูงมาก"}

# โหลด Dataset
if not os.path.exists(CSV):
    try:
        urllib.request.urlretrieve(URL, CSV)
    except:
        messagebox.showerror("ผิดพลาด","ดาวน์โหลด Dataset ไม่สำเร็จ")
        raise SystemExit

df = pd.read_csv(CSV)
X = df[FEATURES]
y = df["price_range"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def predict():
    try:
        values = []
        for i, f in enumerate(FEATURES):
            text = entries[f].get().strip()
            if not text:
                raise ValueError(f"กรุณากรอก {LABELS[i]}")
            value = float(text)
            if value < 0:
                raise ValueError("ค่าต้องไม่ติดลบ")
            values.append(value)

        k = int(k_var.get())
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(X_train, y_train)

        data = pd.DataFrame([values], columns=FEATURES)
        result = int(model.predict(scaler.transform(data))[0])
        acc = accuracy_score(y_test, model.predict(X_test)) * 100

        result_var.set(f"{result} : {PRICE[result]}")
        acc_var.set(f"Accuracy = {acc:.2f}% | k = {k}")

    except ValueError as e:
        messagebox.showwarning("ข้อมูลไม่ถูกต้อง", str(e))

def random_data():
    row = df.sample(1).iloc[0]
    for f in FEATURES:
        entries[f].delete(0, tk.END)
        entries[f].insert(0, row[f])
    real = int(row["price_range"])
    sample_var.set(f"คำตอบจริง: {real} : {PRICE[real]}")

def clear():
    for e in entries.values():
        e.delete(0, tk.END)
    result_var.set("ยังไม่ได้ทำนาย")
    acc_var.set("")
    sample_var.set("")

# GUI
root = tk.Tk()
root.title("Mobile Price kNN")
root.geometry("1180x680")
root.configure(bg="#f4f2fb")

header = tk.Frame(root, bg="#5b45b5", height=78)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header,text="📱 Mobile Price kNN Classifier",
         font=("Tahoma",22,"bold"),bg="#5b45b5",fg="white").pack(anchor="w",padx=25,pady=(13,0))
tk.Label(header,text=f"ทำนายระดับราคามือถือด้วย kNN | Dataset {len(df):,} แถว",
         font=("Tahoma",10),bg="#5b45b5",fg="white").pack(anchor="w",padx=27)

body = tk.Frame(root,bg="#f4f2fb")
body.pack(fill="both",expand=True,padx=15,pady=15)

left = tk.Frame(body,bg="white",padx=18,pady=14)
left.pack(side="left",fill="y",padx=(0,12))
tk.Label(left,text="กรอกสเปกมือถือ",font=("Tahoma",15,"bold"),bg="white").grid(
    row=0,column=0,columnspan=2,sticky="w",pady=(0,10))

entries = {}
for i,f in enumerate(FEATURES):
    tk.Label(left,text=LABELS[i],font=("Tahoma",10),bg="white").grid(
        row=i+1,column=0,sticky="w",pady=5)
    e = tk.Entry(left,width=18,font=("Tahoma",10))
    e.grid(row=i+1,column=1,padx=(12,0),pady=5)
    entries[f] = e

tk.Label(left,text="จำนวนเพื่อนบ้าน (k)",font=("Tahoma",10,"bold"),bg="white").grid(
    row=8,column=0,sticky="w",pady=(12,5))
k_var = tk.StringVar(value="5")
ttk.Combobox(left,textvariable=k_var,values=[1,3,5,7,9,11],
             state="readonly",width=8).grid(row=8,column=1,sticky="w",padx=(12,0),pady=(12,5))

buttons = tk.Frame(left,bg="white")
buttons.grid(row=9,column=0,columnspan=2,pady=12)
tk.Button(buttons,text="ทำนาย",command=predict,bg="#5b45b5",fg="white",
          font=("Tahoma",10,"bold"),width=10).pack(side="left",padx=3)
tk.Button(buttons,text="สุ่ม",command=random_data,width=9).pack(side="left",padx=3)
tk.Button(buttons,text="ล้าง",command=clear,width=8).pack(side="left",padx=3)

result_var = tk.StringVar(value="ยังไม่ได้ทำนาย")
acc_var = tk.StringVar()
sample_var = tk.StringVar()

tk.Label(left,textvariable=result_var,font=("Tahoma",16,"bold"),fg="#23753b",
         bg="#eef9f1",width=30,pady=10).grid(row=10,column=0,columnspan=2,pady=5)
tk.Label(left,textvariable=acc_var,font=("Tahoma",9),bg="white").grid(row=11,column=0,columnspan=2)
tk.Label(left,textvariable=sample_var,font=("Tahoma",9),bg="white").grid(row=12,column=0,columnspan=2,pady=4)
tk.Label(left,text="0=ต่ำ | 1=ปานกลาง | 2=สูง | 3=สูงมาก",
         font=("Tahoma",8),fg="#777",bg="white").grid(row=13,column=0,columnspan=2,pady=5)

right = tk.Frame(body,bg="white",padx=10,pady=10)
right.pack(side="right",fill="both",expand=True)
tk.Label(right,text=f"Training Dataset ({len(df):,} records)",
         font=("Tahoma",14,"bold"),bg="white").pack(anchor="w",pady=(0,8))

cols = FEATURES + ["price_range"]
names = ["Battery","RAM","Memory","Weight","Cores","Camera","Talk","Price"]
frame = tk.Frame(right)
frame.pack(fill="both",expand=True)

tree = ttk.Treeview(frame,columns=cols,show="headings")
for c,n in zip(cols,names):
    tree.heading(c,text=n)
    tree.column(c,width=75,anchor="center")

sy = ttk.Scrollbar(frame,orient="vertical",command=tree.yview)
sx = ttk.Scrollbar(frame,orient="horizontal",command=tree.xview)
tree.configure(yscrollcommand=sy.set,xscrollcommand=sx.set)
tree.grid(row=0,column=0,sticky="nsew")
sy.grid(row=0,column=1,sticky="ns")
sx.grid(row=1,column=0,sticky="ew")
frame.rowconfigure(0,weight=1)
frame.columnconfigure(0,weight=1)

for _,row in df[cols].iterrows():
    tree.insert("","end",values=[row[c] for c in cols])

tk.Label(root,text="Dataset: Mobile Price Classification — Abhishek Sharma (Kaggle)",
         font=("Tahoma",8),bg="#f4f2fb",fg="#777").pack(pady=(0,7))

root.mainloop()
