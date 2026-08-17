import psutil
import time
import socket
from utils.logger import logger

class HeartbeatCollector:
    @staticmethod
    def collect():
        """Collect all system data for heartbeat"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_cores = psutil.cpu_count()
            
            # RAM
            mem = psutil.virtual_memory()
            ram_total = round(mem.total / (1024**3), 2)
            ram_used = round(mem.used / (1024**3), 2)
            ram_percent = mem.percent
            
            # Disk (main drive)
            disk = psutil.disk_usage('C:\\')
            disk_total = round(disk.total / (1024**3), 2)
            disk_used = round(disk.used / (1024**3), 2)
            disk_percent = disk.percent
            
            # Network
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            # Uptime
            uptime_seconds = int(time.time() - psutil.boot_time())
            
            # User
            username = psutil.users()[0].name if psutil.users() else 'Unknown'
            
            # Active window
            active_window = 'Unknown'
            try:
                import ctypes
                user32 = ctypes.windll.user32
                hwnd = user32.GetForegroundWindow()
                length = user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                active_window = buff.value or 'Unknown'
            except Exception:
                pass
            
            # Check if game is running
            game_running = False
            game_processes = [
                'steam.exe', 'epicgameslauncher.exe', 'valorant.exe', 'csgo.exe',
                'dota2.exe', 'fortnite.exe', 'minecraft.exe', 'rocketleague.exe',
                'gta5.exe', 'rdr2.exe', 'cod.exe', 'battlefield.exe',
                'overwatch.exe', 'apex.exe', 'pubg.exe', 'roblox.exe',
                'leagueoflegends.exe'
            ]
            try:
                for proc in psutil.process_iter(['name']):
                    try:
                        proc_name = proc.info['name'].lower()
                        for game in game_processes:
                            if game.lower() in proc_name:
                                game_running = True
                                break
                        if game_running:
                            break
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            except Exception:
                pass
            
            # Determine status
            if game_running:
                status = 'gaming'
            elif cpu_percent < 10 and ram_percent < 30:
                status = 'idle'
            else:
                status = 'active'
            
            return {
                'status': status,
                'cpu_percent': cpu_percent,
                'cpu_cores': cpu_cores,
                'ram_total_gb': ram_total,
                'ram_used_gb': ram_used,
                'ram_percent': ram_percent,
                'disk_total_gb': disk_total,
                'disk_used_gb': disk_used,
                'disk_percent': disk_percent,
                'username': username,
                'hostname': hostname,
                'ip': ip,
                'uptime_seconds': uptime_seconds,
                'active_window': active_window,
                'game_running': game_running,
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Error collecting heartbeat: {e}")
            return None