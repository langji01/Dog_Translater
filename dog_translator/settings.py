import json

class Settings:
    def __init__(self):
        self.default_settings = {
            'recording_duration': 5,
            'sample_rate': 44100,
            'high_freq_threshold': 1000,
            'high_volume_threshold': 0.01,
            'freq_std_threshold': 1000,
            'volume_change_threshold': 0.01
        }
        self.load_settings()
        
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = self.default_settings
            self.save_settings()
            
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=4) 