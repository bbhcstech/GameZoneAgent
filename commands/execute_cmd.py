import subprocess

class ExecuteCMD:
    def execute(self, payload):
        try:
            command = payload.get('command')
            
            if not command:
                return {'success': False, 'error': 'Command is required'}
            
            result = subprocess.run(
                ['cmd', '/c', command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timed out after 30s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}