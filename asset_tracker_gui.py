import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# 数据文件路径
DATA_FILE = "transactions.csv"

def load_data():
    """加载交易记录数据"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["date", "account", "amount", "type", "description", "category"])

def save_data(data):
    """保存交易记录数据"""
    data.to_csv(DATA_FILE, index=False)

class AssetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("资产记录程序")
        self.root.geometry("900x600")
        self.data = load_data()

        # 创建选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 添加交易记录选项卡
        self.add_transaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_transaction_frame, text="添加交易记录")

        # 查看交易记录选项卡
        self.view_records_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_records_frame, text="查看交易记录")

        # 统计和报告选项卡
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="统计和报告")

        # 设置各选项卡的内容
        self.setup_add_transaction_tab()
        self.setup_view_records_tab()
        self.setup_stats_tab()

    def setup_add_transaction_tab(self):
        """设置添加交易记录选项卡"""
        frame = self.add_transaction_frame

        # 日期输入
        ttk.Label(frame, text="日期 (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # 账户选择
        ttk.Label(frame, text="账户:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.account_var = tk.StringVar()
        account_combo = ttk.Combobox(frame, textvariable=self.account_var)
        account_combo['values'] = ("微信", "邮政储蓄", "建设银行", "支付宝", "校园e网通")
        account_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # 金额输入
        ttk.Label(frame, text="金额:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # 交易类型选择
        ttk.Label(frame, text="交易类型:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(frame, textvariable=self.type_var)
        type_combo['values'] = ("收入", "支出")
        type_combo.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        # 描述输入
        ttk.Label(frame, text="描述:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.description_entry = ttk.Entry(frame)
        self.description_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        # 类别输入
        ttk.Label(frame, text="类别:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_entry = ttk.Entry(frame)
        self.category_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        # 添加按钮
        add_button = ttk.Button(frame, text="添加记录", command=self.add_transaction)
        add_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

    def setup_view_records_tab(self):
        """设置查看交易记录选项卡"""
        frame = self.view_records_frame

        # 显示交易记录的树状视图
        self.tree = ttk.Treeview(frame, columns=("date", "account", "amount", "type", "description", "category"),
                                 show="headings")
        self.tree.heading("date", text="日期")
        self.tree.heading("account", text="账户")
        self.tree.heading("amount", text="金额")
        self.tree.heading("type", text="类型")
        self.tree.heading("description", text="描述")
        self.tree.heading("category", text="类别")

        self.tree.column("date", width=100)
        self.tree.column("account", width=100)
        self.tree.column("amount", width=80)
        self.tree.column("type", width=60)
        self.tree.column("description", width=200)
        self.tree.column("category", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 刷新按钮
        refresh_button = ttk.Button(frame, text="刷新记录", command=self.refresh_records)
        refresh_button.pack(pady=10)

        # 按月份筛选
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill=tk.X, pady=10)

        ttk.Label(filter_frame, text="年份:").grid(row=0, column=0, padx=5, pady=5)
        self.year_var = tk.StringVar()
        year_combo = ttk.Combobox(filter_frame, textvariable=self.year_var)
        year_combo['values'] = tuple(str(year) for year in range(2020, datetime.now().year + 1))
        year_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="月份:").grid(row=0, column=2, padx=5, pady=5)
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(filter_frame, textvariable=self.month_var)
        month_combo['values'] = tuple(str(month) for month in range(1, 13))
        month_combo.grid(row=0, column=3, padx=5, pady=5)

        filter_button = ttk.Button(filter_frame, text="筛选", command=self.filter_records)
        filter_button.grid(row=0, column=4, padx=5, pady=5)

        reset_button = ttk.Button(filter_frame, text="重置", command=self.refresh_records)
        reset_button.grid(row=0, column=5, padx=5, pady=5)

    def setup_stats_tab(self):
        """设置统计和报告选项卡"""
        frame = self.stats_frame

        # 按账户统计
        ttk.Button(frame, text="按账户统计", command=self.calculate_total_by_account).pack(pady=10)

        # 生成月度报告
        report_frame = ttk.Frame(frame)
        report_frame.pack(fill=tk.X, pady=10)

        ttk.Label(report_frame, text="年份:").grid(row=0, column=0, padx=5, pady=5)
        self.report_year_var = tk.StringVar()
        year_combo = ttk.Combobox(report_frame, textvariable=self.report_year_var)
        year_combo['values'] = tuple(str(year) for year in range(2020, datetime.now().year + 1))
        year_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(report_frame, text="月份:").grid(row=0, column=2, padx=5, pady=5)
        self.report_month_var = tk.StringVar()
        month_combo = ttk.Combobox(report_frame, textvariable=self.report_month_var)
        month_combo['values'] = tuple(str(month) for month in range(1, 13))
        month_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(report_frame, text="生成报告", command=self.generate_monthly_report).grid(row=0, column=4, padx=5, pady=5)

        # 可视化按钮
        ttk.Button(frame, text="可视化交易记录", command=self.visualize_transactions).pack(pady=10)

        # 导出和导入
        export_import_frame = ttk.Frame(frame)
        export_import_frame.pack(fill=tk.X, pady=10)

        ttk.Button(export_import_frame, text="导出数据", command=self.export_data).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(export_import_frame, text="导入数据", command=self.import_data).grid(row=0, column=1, padx=5, pady=5)

        # 显示统计结果的文本框
        self.stats_text = tk.Text(frame, height=10, width=80)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 用于显示图表的画布
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def add_transaction(self):
        """添加交易记录"""
        date = self.date_entry.get()
        account = self.account_var.get()
        amount_str = self.amount_entry.get()
        transaction_type = self.type_var.get()
        description = self.description_entry.get()
        category = self.category_entry.get()

        # 验证输入
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("错误", "日期格式不正确，请使用 YYYY-MM-DD 格式!")
            return

        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("错误", "金额必须是数字!")
            return

        if transaction_type not in ["收入", "支出"]:
            messagebox.showerror("错误", "交易类型必须是 '收入' 或 '支出'!")
            return

        # 添加记录
        new_record = pd.DataFrame({
            "date": [date],
            "account": [account],
            "amount": [amount],
            "type": [transaction_type],
            "description": [description],
            "category": [category]
        })

        self.data = pd.concat([self.data, new_record], ignore_index=True)
        save_data(self.data)
        messagebox.showinfo("成功", "交易记录已添加成功!")
        self.refresh_records()

    def refresh_records(self):
        """刷新交易记录显示"""
        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 重新加载数据
        self.data = load_data()

        # 插入数据到树状视图
        for _, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=(row["date"], row["account"], row["amount"],
                                                row["type"], row["description"], row["category"]))

    def filter_records(self):
        """按月份筛选交易记录"""
        year_str = self.year_var.get()
        month_str = self.month_var.get()

        if not year_str or not month_str:
            messagebox.showerror("错误", "请选择年份和月份!")
            return

        try:
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            messagebox.showerror("错误", "年份和月份必须是数字!")
            return

        # 筛选数据
        filtered_data = self.data.copy()
        filtered_data["date"] = pd.to_datetime(filtered_data["date"])
        filtered_data = filtered_data[(filtered_data["date"].dt.year == year) & (filtered_data["date"].dt.month == month)]

        # 清空树状视图
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 插入筛选后的数据
        for _, row in filtered_data.iterrows():
            self.tree.insert("", tk.END, values=(row["date"], row["account"], row["amount"],
                                                row["type"], row["description"], row["category"]))

    def calculate_total_by_account(self):
        """按账户统计总金额"""
        if self.data.empty:
            messagebox.showinfo("提示", "暂无记录!")
            return

        # 按账户分组计算总收入和总支出
        grouped = self.data.groupby(["account", "type"])["amount"].sum().unstack(fill_value=0)

        # 清空统计文本框
        self.stats_text.delete(1.0, tk.END)

        # 显示统计结果
        self.stats_text.insert(tk.END, "===== 按账户统计 =====\n")
        self.stats_text.insert(tk.END, str(grouped))
        self.stats_text.insert(tk.END, "\n=====================\n")

        # 绘制柱状图
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        grouped.plot(kind="bar", ax=ax)
        ax.set_title("各账户收入与支出对比")
        ax.set_xlabel("账户")
        ax.set_ylabel("金额")
        self.canvas.draw()

    def generate_monthly_report(self):
        """生成月度报告"""
        if self.data.empty:
            messagebox.showinfo("提示", "暂无记录!")
            return

        year_str = self.report_year_var.get()
        month_str = self.report_month_var.get()

        if not year_str or not month_str:
            messagebox.showerror("错误", "请选择年份和月份!")
            return

        try:
            year = int(year_str)
            month = int(month_str)
        except ValueError:
            messagebox.showerror("错误", "年份和月份必须是数字!")
            return

        # 筛选数据
        filtered_data = self.data.copy()
        filtered_data["date"] = pd.to_datetime(filtered_data["date"])
        filtered_data = filtered_data[(filtered_data["date"].dt.year == year) & (filtered_data["date"].dt.month == month)]

        if filtered_data.empty:
            messagebox.showinfo("提示", f"{year}年{month}月暂无记录!")
            return

        # 计算总收入和总支出
        income = filtered_data[filtered_data["type"] == "收入"]["amount"].sum()
        expense = filtered_data[filtered_data["type"] == "支出"]["amount"].sum()
        net_income = income - expense

        # 清空统计文本框
        self.stats_text.delete(1.0, tk.END)

        # 显示报告
        self.stats_text.insert(tk.END, f"===== {year}年{month}月报告 =====\n")
        self.stats_text.insert(tk.END, f"总收入: {income:.2f}\n")
        self.stats_text.insert(tk.END, f"总支出: {expense:.2f}\n")
        self.stats_text.insert(tk.END, f"净收入: {net_income:.2f}\n")
        self.stats_text.insert(tk.END, "==============================\n")

    def visualize_transactions(self):
        """可视化交易记录"""
        if self.data.empty:
            messagebox.showinfo("提示", "暂无记录!")
            return

        # 按账户和交易类型分组
        grouped = self.data.groupby(["account", "type"])["amount"].sum().unstack(fill_value=0)

        # 绘制柱状图
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        grouped.plot(kind="bar", ax=ax)
        ax.set_title("各账户收入与支出对比")
        ax.set_xlabel("账户")
        ax.set_ylabel("金额")
        self.canvas.draw()

    def export_data(self):
        """导出交易记录到 CSV 文件"""
        if self.data.empty:
            messagebox.showinfo("提示", "暂无记录!")
            return

        filename = "transactions_export.csv"
        self.data.to_csv(filename, index=False)
        messagebox.showinfo("成功", f"数据已导出到 {filename}!")

    def import_data(self):
        """从 CSV 文件导入交易记录"""
        filename = "transactions_import.csv"
        try:
            imported_data = pd.read_csv(filename)
            self.data = pd.concat([self.data, imported_data], ignore_index=True)
            save_data(self.data)
            messagebox.showinfo("成功", f"已导入 {len(imported_data)} 条记录!")
            self.refresh_records()
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssetTrackerApp(root)
    root.mainloop()