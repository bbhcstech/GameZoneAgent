from services.api_service import ApiService
import os


class ShowQR:
    def execute(self, payload=None):
        try:
            qr_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "assets",
                "qrcode.png"
            )

            if not os.path.exists(qr_path):
                return {
                    "success": False,
                    "error": "Payment QR image not found"
                }

            upload_result = ApiService().upload_qr(qr_path)

            if not upload_result or not upload_result.get("success"):
                return {
                    "success": False,
                    "error": "Failed to upload QR image"
                }

            os.startfile(qr_path)

            return {
                "success": True,
                "message": "Payment QR displayed",
                "qr_url": upload_result["url"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }