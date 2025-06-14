# coding: utf-8
import tkinter as tk
from tkinter import filedialog, messagebox
from main import SJNMDJW

class HandwriteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("手写效果生成器")

        # 文本输入区域
        self.text_label = tk.Label(root, text="请输入文本：")
        self.text_label.pack(pady=10)
        self.text_input = tk.Text(root, height=10, width=50)
        self.text_input.pack(pady=5)

        # 输出路径选择
        self.output_label = tk.Label(root, text="输出路径：")
        self.output_label.pack(pady=10)
        self.output_path = tk.StringVar()
        self.output_entry = tk.Entry(root, textvariable=self.output_path, width=40)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.browse_button = tk.Button(root, text="浏览", command=self.browse_output_path)
        self.browse_button.pack(side=tk.LEFT)
        # 输入文件名
        self.file_name_label = tk.Label(root, text="文件名：")
        self.file_name_label.pack(side=tk.LEFT, padx=5)
        self.file_name_text = tk.StringVar()
        self.file_name_entry = tk.Entry(root, textvariable=self.file_name_text, width=20)
        self.file_name_entry.pack(side=tk.LEFT)


        # 生成按钮
        self.generate_button = tk.Button(root, text="生成手写图片", command=self.generate_handwrite)
        self.generate_button.pack(pady=20)

    def browse_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def generate_handwrite(self):
        text = self.text_input.get("1.0", tk.END).strip()
        output_path = self.output_path.get()
        file_name = self.file_name_text.get()
        if not file_name:
            messagebox.showerror("错误", "请输入文件名！")
            return
        if not file_name.endswith('.png'):
            file_name += '.png'
        if not text:
            messagebox.showerror("错误", "请输入有效文本！")
            return
        if not output_path:
            messagebox.showerror("错误", "请选择输出路径！")
            return

        try:
            sjnmdjw = SJNMDJW(outputPath=output_path,outputFileName=file_name)
            sjnmdjw.create_template(text=text).save_image().save_replace_item()
            messagebox.showinfo("成功", "手写图片生成成功！")
        except Exception as e:
            messagebox.showerror("错误", f"生成失败：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HandwriteGUI(root)
    root.mainloop()