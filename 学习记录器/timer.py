import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
from PIL import Image, ImageTk

# 文件名用于存储学习时间记录
RECORD_FILE = 'study_time_records.json'

def load_records():
    """加载学习时间记录"""
    try:
        with open(RECORD_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_records(records):
    """保存学习时间记录"""
    with open(RECORD_FILE, 'w') as file:
        json.dump(records, file, indent=4)

class StudyTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("学习时间记录器")
        
        # 设置窗口大小
        self.root.geometry('800x600')

        # 加载背景图片
        self.background_image_path = 'background.jpg'
        try:
            self.background_image = ImageTk.PhotoImage(Image.open(self.background_image_path))
            self.background_label = tk.Label(root, image=self.background_image)
            self.background_label.place(relwidth=1, relheight=1)
        except FileNotFoundError:
            messagebox.showerror("错误", f"未找到背景图片: {self.background_image_path}")
            self.root.destroy()
            return

        self.start_time = None

        # 使用 ttk 样式
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 12), padding=10)
        style.configure("TLabel", font=('Helvetica', 14), background="#000000", foreground="#FFFFFF")

        self.start_button = ttk.Button(root, text="开始学习", command=self.start_study, style="TButton")
        self.start_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.end_button = ttk.Button(root, text="结束学习", command=self.end_study, style="TButton")
        self.end_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.history_button = ttk.Button(root, text="查看历史记录", command=self.show_history, style="TButton")
        self.history_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        self.status_label = ttk.Label(root, text="点击 '开始学习' 开始记录时间", style="TLabel")
        self.status_label.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def start_study(self):
        """记录开始学习的时间"""
        self.start_time = datetime.now()
        self.status_label.config(text=f"学习开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        messagebox.showinfo("提示", "学习开始时间已记录")

    def end_study(self):
        """记录结束学习的时间并保存"""
        if self.start_time is None:
            messagebox.showwarning("警告", "请先点击 '开始学习'")
            return

        end_time = datetime.now()
        duration = end_time - self.start_time
        self.status_label.config(text=f"学习结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n本次学习时长: {duration}")

        record = {
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': str(duration)
        }
        records = load_records()
        records.append(record)
        save_records(records)

        messagebox.showinfo("提示", "学习时间已记录")
        self.start_time = None

    def show_history(self):
        """显示历史学习时间记录"""
        records = load_records()
        if not records:
            messagebox.showinfo("提示", "没有历史记录")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("历史记录")
        history_window.geometry('600x400')

        history_text = tk.Text(history_window)
        history_text.pack(expand=True, fill='both')

        for record in records:
            start_time = record['start_time']
            end_time = record['end_time']
            duration = record['duration']
            history_text.insert(tk.END, f"开始时间: {start_time}\n结束时间: {end_time}\n时长: {duration}\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyTimerApp(root)
    root.mainloop()