import psutil
import socket
import time

class HeartbeatData:
    @staticmethod
    def collect():
        """Collect system data for heartbeat"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_cores = psutil.cpu_count()
            
            # RAM
            mem = psutil.virtual_memory()
            ram_total = round(mem.total / (1024**3), 2)
            ram_used = round(mem.used / (1024**3), 2)
            ram_percent = mem.percent
            
            # Disk
            disk = psutil.disk_usage('/')
            disk_total = round(disk.total / (1024**3), 2)
            disk_used = round(disk.used / (1024**3), 2)
            disk_percent = disk.percent
            
            # System
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            uptime_seconds = int(time.time() - psutil.boot_time())
            
            # User
            username = psutil.users()[0].name if psutil.users() else 'Unknown'
            
            # Status
            if cpu_percent < 10 and ram_percent < 30:
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
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            return None