import psutil

class GetProcesses:
    def execute(self, payload=None):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': round(proc.info['cpu_percent'] or 0, 1),
                        'memory': round(proc.info['memory_percent'] or 0, 1)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage (highest first)
            processes.sort(key=lambda x: x['cpu'], reverse=True)
            
            return {
                'success': True,
                'count': len(processes),
                'processes': processes[:50]  # Top 50 processes
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}