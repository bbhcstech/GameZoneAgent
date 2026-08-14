import webbrowser

class OpenURL:
    def execute(self, payload):
        try:
            url = payload.get('url')
            
            if not url:
                return {'success': False, 'error': 'URL is required'}
            
            # Add https:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return {'success': True, 'message': f'Opened {url}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}