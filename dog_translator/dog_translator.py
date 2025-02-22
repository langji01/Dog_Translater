from datetime import datetime
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

class DogTranslator:
    def __init__(self):
        self.sample_rate = 44100  # 采样率
        self.max_duration = 5     # 改为5秒，更合理的长度
        self.recording = None     # 存储录音数据
        self.analysis_history = [] # 历史记录
        
        # 添加分析阈值常量
        self.HIGH_FREQ_THRESHOLD = 1000  # 高频阈值
        self.HIGH_VOLUME_THRESHOLD = 0.01 # 高音量阈值
        self.FREQ_STD_THRESHOLD = 1000   # 频率标准差阈值
        self.VOLUME_CHANGE_THRESHOLD = 0.01 # 音量变化阈值

    def start_recording(self):
        """开始录音"""
        try:
            print("准备开始录音...")
            # 列出可用的音频设备
            print("\n可用的音频设备:")
            print(sd.query_devices())
            
            # 获取默认设备信息
            device_info = sd.query_devices(None, 'input')
            print(f"\n使用的录音设备: {device_info['name']}")
            
            num_samples = int(self.max_duration * self.sample_rate)
            print(f"预计录音时长: {self.max_duration}秒")
            
            print("\n请发出声音...")
            self.recording = sd.rec(
                num_samples,
                samplerate=self.sample_rate,
                channels=1,
                blocking=True
            )
            print("录音完成")
            return True
        except Exception as e:
            print(f"录音出错: {str(e)}")
            return False
            
    def stop_recording(self):
        """停止录音"""
        if self.recording is not None:
            sd.stop()
            return True
        return False
    
    def analyze_bark(self, audio_data):
        """分析狗叫声"""
        # 添加实际的声音特征分析
        if audio_data is not None and len(audio_data) > 0:  # 确保有录音数据
            print(f"录音数据长度: {len(audio_data)} 采样点")
            print(f"平均音量: {np.mean(np.abs(audio_data)):.4f}")
            
            # 计算音频特征
            frequencies = np.fft.fft(audio_data)
            # 计算音量
            volume = np.mean(np.abs(audio_data))
            # 计算持续时间
            duration = len(audio_data) / self.sample_rate
            
            print(f"音频持续时间: {duration:.2f} 秒")
            
            # 基于特征判断情绪
            emotions = self._analyze_features(frequencies, volume, duration)
        else:
            print("没有检测到有效的录音数据，使用默认值")
            emotions = {
                "happy": 0.7,
                "hungry": 0.2,
                "anxious": 0.1
            }
        
        result = {
            "timestamp": datetime.now(),
            "emotions": emotions,
            "primary_emotion": max(emotions.items(), key=lambda x: x[1]),
            "confidence": 0.85,
            "suggestions": self._get_suggestions(emotions)
        }
        
        self.analysis_history.append(result)
        return result
    
    def _analyze_features(self, frequencies, volume, duration):
        """改进的声音特征分析"""
        emotions = {}
        
        # 添加更多声音特征分析
        frequency_mean = np.mean(np.abs(frequencies))
        frequency_std = np.std(np.abs(frequencies))
        volume_changes = np.diff(np.abs(self.recording.flatten()))
        volume_change_mean = np.mean(volume_changes)
        
        print(f"\n声音特征分析:")
        print(f"频率平均值: {frequency_mean:.2f}")
        print(f"频率标准差: {frequency_std:.2f}")
        print(f"音量变化平均值: {volume_change_mean:.4f}")
        
        # 基于更多特征的情绪判断
        if frequency_mean > self.HIGH_FREQ_THRESHOLD and volume_change_mean > self.VOLUME_CHANGE_THRESHOLD:
            print("检测到高频率和大音量变化 -> 兴奋/开心")
            emotions["excited"] = 0.9
            emotions["happy"] = 0.7
        elif frequency_std > self.FREQ_STD_THRESHOLD and volume > self.HIGH_VOLUME_THRESHOLD:
            print("检测到频率波动和高音量 -> 焦虑/警觉")
            emotions["anxious"] = 0.8
            emotions["alert"] = 0.6
        elif frequency_mean < self.HIGH_FREQ_THRESHOLD/2 and volume < self.HIGH_VOLUME_THRESHOLD/2:
            emotions["calm"] = 0.8
            emotions["sleepy"] = 0.6
        elif volume_change_mean > self.VOLUME_CHANGE_THRESHOLD*2:
            emotions["playful"] = 0.85
            emotions["happy"] = 0.7
        
        # 如果没有检测到明显情绪，添加默认值
        if not emotions:
            emotions["neutral"] = 0.5
        
        return emotions
    
    def _get_suggestions(self, emotions):
        """根据情绪生成建议"""
        suggestions = []
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        emotion_suggestions = {
            "happy": ["狗狗心情不错，可以和它玩耍互动", "可以给它最喜欢的玩具"],
            "excited": ["狗狗很兴奋，可以带它出去散步", "可以和它玩投球游戏"],
            "anxious": ["狗狗可能感到焦虑，多给予安抚和陪伴", "检查周围环境是否有让它紧张的因素"],
            "alert": ["狗狗处于警觉状态，查看是否有异常情况", "确保环境安全"],
            "calm": ["狗狗很放松，是互动的好时机", "可以进行一些轻松的训练"],
            "sleepy": ["狗狗有点困了，可以让它休息", "确保它有舒适的睡觉区域"],
            "playful": ["狗狗想要玩耍，陪它玩一会儿", "拿出它喜欢的玩具"],
            "neutral": ["狗狗情绪平静", "保持正常的日常活动"],
            "hungry": ["狗狗可能饿了，检查是否到喂食时间", "确保食物和水都充足"]
        }
        
        if primary_emotion in emotion_suggestions:
            suggestions.extend(emotion_suggestions[primary_emotion])
        else:
            suggestions.append("继续观察狗狗的状态")
        
        return suggestions
    
    def get_history(self, start_date=None, end_date=None):
        """获取历史记录"""
        if not (start_date or end_date):
            return self.analysis_history
            
        filtered_history = [
            record for record in self.analysis_history
            if (not start_date or record["timestamp"] >= start_date) and
               (not end_date or record["timestamp"] <= end_date)
        ]
        return filtered_history
    
    def export_report(self, format="txt"):
        """导出分析报告"""
        if format == "txt":
            report = "狗语翻译分析报告\n"
            report += "=" * 20 + "\n\n"
            
            for record in self.analysis_history:
                report += f"时间: {record['timestamp']}\n"
                report += f"主要情绪: {record['primary_emotion'][0]} (置信度: {record['primary_emotion'][1]:.2f})\n"
                report += f"建议: {record['suggestions'][0]}\n"
                report += "-" * 20 + "\n"
            
            with open("dog_analysis_report.txt", "w", encoding="utf-8") as f:
                f.write(report)
            return True
        
        return False
    
    def save_recording(self, filename):
        """保存录音到文件"""
        if self.recording is not None:
            wav.write(filename, self.sample_rate, self.recording)
            return True
        return False

# 删除文件末尾的这个函数
def test_full_features():
    translator = DogTranslator()
    
    # 将录音时长设置为5秒
    translator.max_duration = 5  # 添加这行
    
    print("开始录音测试（5秒）...")
    translator.start_recording()
    print("录音结束")
    
    # ... 其余代码保持不变 ... 