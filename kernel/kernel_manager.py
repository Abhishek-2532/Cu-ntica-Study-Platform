import sys
import queue
import re
from jupyter_client import KernelManager

try:
    from ansi2html import Ansi2HTMLConverter
    conv = Ansi2HTMLConverter(inline=True)
    def ansi_to_html(text):
        return conv.convert(text, full=False)
except ImportError:
    def ansi_to_html(text):
        # Fallback simple escape/strip if ansi2html not installed
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return f"<pre>{ansi_escape.sub('', text)}</pre>"


class NotebookKernel:
    def __init__(self):
        self.km = KernelManager()
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready(timeout=10)
        self.execution_count = 0

    def execute(self, code, timeout=30):
        self.execution_count += 1
        msg_id = self.kc.execute(code)

        outputs = []
        error_msg = None
        status = "ok"

        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=timeout)
            except queue.Empty:
                error_msg = "Execution timed out."
                status = "error"
                break

            if msg.get("parent_header", {}).get("msg_id") != msg_id:
                continue

            msg_type = msg["msg_type"]
            content = msg["content"]

            if msg_type == "stream":
                text = content.get("text", "")
                name = content.get("name", "stdout")
                outputs.append({
                    "type": "stream",
                    "name": name,
                    "text": text
                })

            elif msg_type in ("execute_result", "display_data"):
                data = content.get("data", {})
                
                # Check rich MIME types in order of preference
                if "image/png" in data:
                    outputs.append({
                        "type": "image",
                        "mime": "image/png",
                        "data": f"data:image/png;base64,{data['image/png']}"
                    })
                elif "image/jpeg" in data:
                    outputs.append({
                        "type": "image",
                        "mime": "image/jpeg",
                        "data": f"data:image/jpeg;base64,{data['image/jpeg']}"
                    })
                elif "image/svg+xml" in data:
                    outputs.append({
                        "type": "svg",
                        "data": data["image/svg+xml"]
                    })
                elif "text/html" in data:
                    outputs.append({
                        "type": "html",
                        "data": data["text/html"]
                    })
                elif "application/json" in data:
                    outputs.append({
                        "type": "json",
                        "data": data["application/json"]
                    })
                elif "text/plain" in data:
                    outputs.append({
                        "type": "text",
                        "data": data["text/plain"]
                    })

            elif msg_type == "error":
                status = "error"
                ename = content.get("ename", "Error")
                evalue = content.get("evalue", "")
                traceback_lines = content.get("traceback", [])
                raw_tb = "\n".join(traceback_lines) if traceback_lines else f"{ename}: {evalue}"
                formatted_tb = ansi_to_html(raw_tb)
                
                error_msg = f"{ename}: {evalue}"
                outputs.append({
                    "type": "error",
                    "ename": ename,
                    "evalue": evalue,
                    "raw": raw_tb,
                    "html": formatted_tb
                })

            elif msg_type == "status":
                if content.get("execution_state") == "idle":
                    break

        return {
            "execution_count": self.execution_count,
            "outputs": outputs,
            "error": error_msg,
            "status": status
        }

    def restart(self):
        try:
            self.kc.stop_channels()
            self.km.restart_kernel(now=True)
            self.kc = self.km.client()
            self.kc.start_channels()
            self.kc.wait_for_ready(timeout=10)
            self.execution_count = 0
            return True
        except Exception as e:
            return False

    def interrupt(self):
        try:
            self.km.interrupt_kernel()
            return True
        except Exception:
            return False

    def shutdown(self):
        try:
            self.kc.stop_channels()
            self.km.shutdown_kernel()
        except Exception:
            pass