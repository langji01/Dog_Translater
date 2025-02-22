import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class AudioVisualizer:
    def __init__(self, translator, gui):
        self.translator = translator
        self.gui = gui
        self.setup_plot()
        self.animation = None
        
    def setup_plot(self):
        """设置声音可视化图表"""
        self.fig, (self.wave_ax, self.freq_ax) = plt.subplots(2, 1, figsize=(8, 6))
        self.wave_line, = self.wave_ax.plot([], [], lw=2)
        self.freq_line, = self.freq_ax.plot([], [], lw=2)
        
        # 设置坐标轴
        self.wave_ax.set_title('声波形态')
        self.wave_ax.set_ylim(-1, 1)
        self.freq_ax.set_title('频率分布')
        
        # 创建画布
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.gui.root)

    def update_plot(self, frame):
        """更新声音可视化"""
        if self.translator.recording is not None:
            # 更新波形图
            data = self.translator.recording.flatten()
            self.wave_line.set_data(range(len(data)), data)
            self.wave_ax.set_xlim(0, len(data))
            
            # 更新频谱图
            freq_data = np.abs(np.fft.fft(data))
            self.freq_line.set_data(range(len(freq_data)), freq_data)
            self.freq_ax.set_xlim(0, len(freq_data))
            
        return self.wave_line, self.freq_line 

    def start_animation(self):
        """开始动画"""
        self.animation = FuncAnimation(
            self.fig, self.update_plot,
            interval=100,  # 每100ms更新一次
            blit=True
        )

    def stop_animation(self):
        """停止动画"""
        if self.animation:
            self.animation.event_source.stop()

    def get_canvas(self):
        """获取画布"""
        return self.canvas 