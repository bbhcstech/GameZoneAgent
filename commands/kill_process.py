import psutil

class KillProcess:
    def execute(self, payload):
        try:
            target = payload.get('target')  # '1234' or 'notepad.exe'
            
            if target.isdigit():
                proc = psutil.Process(int(target))
            else:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == target.lower():
                        break
                else:
                    return {'success': False, 'error': f'Process {target} not found'}
            
            proc.terminate()
            return {'success': True, 'pid': proc.pid}
            
        except psutil.NoSuchProcess:
            return {'success': False, 'error': 'Process no longer exists'}
        except psutil.AccessDenied:
            return {'success': False, 'error': 'Access denied - run as admin'}
        except Exception as e:
            return {'success': False, 'error': str(e)}