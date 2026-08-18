import ctypes
import threading
import time

class SendPopup:
    def execute(self, payload):
        try:
            message = payload.get('message', '')
            title = payload.get('title', 'Game Zone')
            message_type = payload.get('type', 'info')

            if not message:
                return {'success': False, 'error': 'Message is required'}

            icon_map = {    
                'info': 0x40,
                'warning': 0x30,
                'error': 0x10
            }

            icon = icon_map.get(message_type, 0x40)

            flags = (
                icon |
                0x00010000 |  # MB_SETFOREGROUND
                0x00040000 |  # MB_SYSTEMMODAL
                0x00000004    # Yes/No
            )

            result = ctypes.windll.user32.MessageBoxW(
                0,
                message,
                title,
                flags
            )

            choice = 'yes' if result == 6 else 'no'

            return {
                'success': True,
                'message': 'Popup displayed successfully',
                'displayed_message': message,
                'title': title,
                'type': message_type,
                'choice': choice,
                'session_id': payload.get('session_id'),
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }