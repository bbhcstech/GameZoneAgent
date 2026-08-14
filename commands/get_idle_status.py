import psutil
import time
import ctypes
from ctypes import wintypes

class GetIdleStatus:
    def __init__(self):
        # Windows API for last input time
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Common game processes
        self.GAME_PROCESSES = [
            'steam.exe', 'epicgameslauncher.exe', 'valorant.exe', 'csgo.exe',
            'dota2.exe', 'fortnite.exe', 'minecraft.exe', 'rocketleague.exe',
            'gta5.exe', 'rdr2.exe', 'cod.exe', 'battlefield.exe',
            'overwatch.exe', 'apex.exe', 'pubg.exe', 'roblox.exe',
            'leagueoflegends.exe'
        ]
    
    def get_last_input_time(self):
        """Get time since last user input in milliseconds"""
        try:
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [
                    ('cbSize', wintypes.UINT),
                    ('dwTime', wintypes.DWORD)
                ]
            
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
            
            if self.user32.GetLastInputInfo(ctypes.byref(lii)):
                tick_count = self.kernel32.GetTickCount()
                idle_ms = tick_count - lii.dwTime
                return idle_ms
            return None
        except:
            return None
    
    def is_game_running(self):
        """Check if any game process is running"""
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    proc_name = proc.info['name'].lower()
                    for game in self.GAME_PROCESSES:
                        if game.lower() in proc_name:
                            return True
                except:
                    continue
            return False
        except:
            return False
    
    def get_active_window(self):
        """Get title of active window"""
        try:
            hwnd = self.user32.GetForegroundWindow()
            length = self.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            self.user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        except:
            return 'Unknown'
    
    def execute(self, payload=None):
        try:
            # Get idle time
            idle_ms = self.get_last_input_time()
            
            if idle_ms is None:
                idle_seconds = 0
            else:
                idle_seconds = idle_ms / 1000
            
            # Check if game is running
            game_running = self.is_game_running()
            
            # Get active window title
            active_window = self.get_active_window()
            
            # Determine status
            if game_running:
                status = 'gaming'
                status_text = '🎮 Gaming'
            elif idle_seconds < 60:  # Less than 1 minute idle
                status = 'active'
                status_text = '🟢 Active'
            elif idle_seconds < 300:  # 1-5 minutes idle
                status = 'idle_short'
                status_text = '🟡 Idle (brief)'
            else:  # More than 5 minutes idle
                status = 'idle_long'
                status_text = '🔴 Idle (extended)'
            
            return {
                'success': True,
                'status': status,
                'status_text': status_text,
                'idle_seconds': round(idle_seconds, 0),
                'idle_minutes': round(idle_seconds / 60, 1),
                'game_running': game_running,
                'active_window': active_window,
                'timestamp': time.time()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}