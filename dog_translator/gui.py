import tkinter as tk
from tkinter import ttk
from dog_translator import DogTranslator
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DogTranslatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("狗语翻译器")
        self.translator = DogTranslator()
        self.translator.max_duration = 5  # 设置为5秒
        
        # 主录音按钮
        self.record_button = ttk.Button(
            self.root, 
            text="开始录音",
            command=self.toggle_recording
        )
        self.record_button.pack(pady=20)
        
        # 结果显示区域
        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack(pady=10)
        
        # 历史记录按钮
        self.history_button = ttk.Button(
            self.root,
            text="查看历史",
            command=self.show_history
        )
        self.history_button.pack(pady=10)
        
        # 添加进度条
        self.progress = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.progress.pack(pady=10)
        
        # 添加保存按钮
        self.save_button = ttk.Button(
            self.root,
            text="保存录音",
            command=self.save_recording
        )
        self.save_button.pack(pady=10)
        
        # 添加可视化区域
        self.setup_visualization()
        
        self.is_recording = False
        
    def setup_visualization(self):
        """设置声音可视化"""
        from visualizer import AudioVisualizer
        self.visualizer = AudioVisualizer(self.translator, self)
        self.canvas = self.visualizer.get_canvas()
        self.canvas.get_tk_widget().pack(pady=10)
    
    def toggle_recording(self):
        if not self.is_recording:
            self.record_button.config(text="停止录音")
            self.progress["value"] = 0
            self.translator.start_recording()
            self.is_recording = True
            self.update_progress()
            # 开始可视化更新
            self.visualizer.start_animation()
        else:
            self.record_button.config(text="开始录音")
            # 停止可视化更新
            self.visualizer.stop_animation()
            result = self.translator.analyze_bark(self.translator.recording)
            self.show_result(result)
            self.is_recording = False
            self.progress["value"] = 0
    
    def show_result(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "分析结果:\n")
        self.result_text.insert(tk.END, "=" * 30 + "\n\n")
        
        # 显示所有检测到的情绪
        self.result_text.insert(tk.END, "检测到的情绪:\n")
        for emotion, score in result['emotions'].items():
            self.result_text.insert(tk.END, f"- {emotion}: {score:.2f}\n")
        
        self.result_text.insert(tk.END, f"\n主要情绪: {result['primary_emotion'][0]}\n")
        self.result_text.insert(tk.END, f"置信度: {result['primary_emotion'][1]:.2f}\n\n")
        
        self.result_text.insert(tk.END, "建议:\n")
        for suggestion in result['suggestions']:
            self.result_text.insert(tk.END, f"- {suggestion}\n")
    
    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("历史记录")
        
        history = self.translator.get_history()
        history_text = tk.Text(history_window, height=20, width=50)
        history_text.pack(pady=10)
        
        for record in history:
            history_text.insert(tk.END, f"时间: {record['timestamp']}\n")
            history_text.insert(tk.END, f"情绪: {record['primary_emotion'][0]}\n")
            history_text.insert(tk.END, "-" * 40 + "\n")
    
    def save_recording(self):
        """保存录音文件"""
        if self.translator.recording is not None:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")],
                title="保存录音文件"
            )
            if filename:
                self.translator.save_recording(filename)
                self.result_text.insert(tk.END, f"\n录音已保存到: {filename}\n")
    
    def update_progress(self):
        if self.is_recording:
            self.progress["value"] += 2
            if self.progress["value"] < 100:
                self.root.after(100, self.update_progress)
    
    def add_visualization(self):
        """添加声音可视化"""
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()
        
        def update_plot():
            if self.is_recording and self.translator.recording is not None:
                self.ax.clear()
                self.ax.plot(self.translator.recording)
                self.canvas.draw()
                self.root.after(100, update_plot)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("正在启动GUI应用...")
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
    try:
        app = DogTranslatorGUI()
        print("GUI已创建，开始运行...")
        app.run()
    except Exception as e:
        print(f"发生错误: {str(e)}") 