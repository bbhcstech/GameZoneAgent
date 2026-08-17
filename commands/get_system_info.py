import platform
import socket
import time
import uuid

import psutil


class GetSystemInfo:
    def execute(self, payload=None):
        try:
            # CPU
            cpu_info = {
                "model": platform.processor() or "Unknown",
                "cores": psutil.cpu_count(logical=False) or psutil.cpu_count(),
                "logical_cores": psutil.cpu_count(logical=True),
                "usage": psutil.cpu_percent(interval=1),
            }

            # RAM
            mem = psutil.virtual_memory()
            ram_info = {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "used_gb": round(mem.used / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "usage_percent": mem.percent,
            }

            # Disks
            disks = []

            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)

                    disks.append({
                        "drive": partition.device,
                        "mount": partition.mountpoint,
                        "total_gb": round(usage.total / (1024 ** 3), 2),
                        "used_gb": round(usage.used / (1024 ** 3), 2),
                        "free_gb": round(usage.free / (1024 ** 3), 2),
                        "usage_percent": usage.percent,
                    })

                except (PermissionError, OSError):
                    continue

            # GPU
            gpu_name = "Unknown"

            try:
                import subprocess

                result = subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        "(Get-CimInstance Win32_VideoController).Name"
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                gpu_lines = [
                    line.strip()
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]

                if gpu_lines:
                    gpu_name = gpu_lines[0]

            except (subprocess.SubprocessError, OSError):
                pass

            # Network
            hostname = socket.gethostname()

            try:
                ip_address = socket.gethostbyname(hostname)
            except socket.error:
                ip_address = "Unknown"

            # MAC address
            try:
                mac_int = uuid.getnode()

                mac = ":".join(
                    f"{(mac_int >> shift) & 0xff:02x}"
                    for shift in range(40, -1, -8)
                )

            except Exception:
                mac = "Unknown"

            # Uptime
            boot_time = psutil.boot_time()
            uptime_seconds = int(time.time() - boot_time)

            # System
            system_info = {
                "os": platform.system(),
                "version": platform.version(),
                "release": platform.release(),
                "hostname": hostname,
                "ip": ip_address,
                "mac": mac,
                "uptime_seconds": uptime_seconds,
                "uptime_hours": round(uptime_seconds / 3600, 1),
            }

            # User
            users = psutil.users()

            user_info = {
                "username": users[0].name if users else "Unknown"
            }

            return {
                "success": True,
                "cpu": cpu_info,
                "ram": ram_info,
                "gpu": {
                    "name": gpu_name
                },
                "disks": disks,
                "system": system_info,
                "user": user_info,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }