import tkinter as tk
print("tkinter 已导入")

try:
    print("正在创建窗口...")
    root = tk.Tk()
    print("窗口已创建")
    
    root.title("测试窗口")
    root.geometry("300x200")  # 设置窗口大小
    
    print("正在添加标签...")
    label = tk.Label(root, text="如果你看到这个窗口，说明tkinter正常工作")
    label.pack(pady=20)
    
    print("正在启动主循环...")
    root.mainloop()
    print("窗口已关闭")
except Exception as e:
    print(f"发生错误: {str(e)}") 