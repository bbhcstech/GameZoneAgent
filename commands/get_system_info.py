import psutil
import platform
import socket
import time

class GetSystemInfo:
    def execute(self, payload=None):
        try:
            # CPU Info
            cpu_info = {
                'model': platform.processor() or 'Unknown',
                'cores': psutil.cpu_count(),
                'usage': psutil.cpu_percent(interval=1)
            }
            
            # Memory Info
            mem = psutil.virtual_memory()
            ram_info = {
                'total_gb': round(mem.total / (1024**3), 2),
                'used_gb': round(mem.used / (1024**3), 2),
                'available_gb': round(mem.available / (1024**3), 2),
                'usage_percent': mem.percent
            }
            
            # Disk Info
            disks = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks.append({
                        'drive': partition.device,
                        'mount': partition.mountpoint,
                        'total_gb': round(usage.total / (1024**3), 2),
                        'used_gb': round(usage.used / (1024**3), 2),
                        'free_gb': round(usage.free / (1024**3), 2),
                        'usage_percent': usage.percent
                    })
                except:
                    continue
            
            # GPU Info (simple - just get name from Windows)
            gpu_name = 'Unknown'
            try:
                import subprocess
                result = subprocess.run(
                    ['wmic', 'path', 'win32_videocontroller', 'get', 'name'],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    gpu_name = lines[1].strip()
            except:
                pass
            
            # Network Info
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            
            # Get MAC address
            mac = 'Unknown'
            try:
                import uuid
                mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                               for elements in range(0, 2*6, 2)][::-1])
            except:
                pass
            
            # System Info
            system_info = {
                'os': platform.system(),
                'version': platform.version(),
                'release': platform.release(),
                'hostname': hostname,
                'ip': ip_address,
                'mac': mac,
                'uptime_seconds': int(time.time() - psutil.boot_time()),
                'uptime_hours': round((time.time() - psutil.boot_time()) / 3600, 1)
            }
            
            # User Info
            user_info = {
                'username': psutil.users()[0].name if psutil.users() else 'Unknown'
            }
            
            return {
                'success': True,
                'cpu': cpu_info,
                'ram': ram_info,
                'gpu': {'name': gpu_name},
                'disks': disks,
                'system': system_info,
                'user': user_info
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}