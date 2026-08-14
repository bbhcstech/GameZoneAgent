import subprocess


class ExecutePowerShell:
    @staticmethod
    def run(command):
        try:
            result = subprocess.run(
                ["powershell", "-Command", command],
                capture_output=True,
                text=True,
                shell=True,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
            }

        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
            }