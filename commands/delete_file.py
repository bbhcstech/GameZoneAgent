import os

class DeleteFile:
    def execute(self, payload):
        try:
            path = payload.get("path")
            if not path:
                return {"success": False, "error": "Path is required"}
            if not os.path.exists(path):
                return { "success": False, "error": "File not found"}
            os.remove(path)
            return {"success": True, "message": "File deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}