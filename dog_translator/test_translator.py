from dog_translator import DogTranslator
import time

def test_recording():
    translator = DogTranslator()
    
    print("开始录音测试（5秒）...")
    translator.start_recording()
    
    # 录制5秒
    time.sleep(5)
    
    translator.stop_recording()
    print("录音结束")
    
    # 测试分析功能
    result = translator.analyze_bark(translator.recording)
    print("\n分析结果:")
    print(f"主要情绪: {result['primary_emotion'][0]} (置信度: {result['primary_emotion'][1]:.2f})")
    print(f"建议: {result['suggestions'][0]}")
    
    # 测试历史记录
    history = translator.get_history()
    print(f"\n历史记录数量: {len(history)}")

def test_full_features():
    translator = DogTranslator()
    
    # 设置录音时长为5秒
    translator.max_duration = 5
    expected_samples = int(5 * translator.sample_rate)
    
    print(f"预期录音时长: {translator.max_duration}秒")
    print(f"预期采样点数: {expected_samples}")
    
    print("\n开始录音测试...")
    translator.start_recording()
    
    # 验证录音长度
    if translator.recording is not None:
        actual_samples = len(translator.recording)
        print(f"\n实际采样点数: {actual_samples}")
        print(f"实际录音时长: {actual_samples/translator.sample_rate:.2f}秒")
    
    # 保存录音
    translator.save_recording("test_bark.wav")
    
    # 分析并显示结果
    result = translator.analyze_bark(translator.recording)
    print("\n详细分析结果:")
    for emotion, score in result["emotions"].items():
        print(f"{emotion}: {score:.2f}")
    print(f"\n建议: {result['suggestions'][0]}")
    
    # 导出报告
    translator.export_report()
    print("\n报告已导出到 dog_analysis_report.txt")

if __name__ == "__main__":
    test_full_features() 