import hashlib
import subprocess
from manimlib.imports import *

class CodeMobject(Code):
    CONFIG = {
        "language": "py",
        "tab_width": 2,
        "font": "Consolas",
        "insert_line_no": False,
    }

    def get_output(self, filepath):
        return subprocess.Popen(
            ["python", filepath], stdout=subprocess.PIPE).communicate()[0]

    def code_hash(self, code):
        id_str = str(code)
        hasher = hashlib.sha256()
        hasher.update(id_str.encode())
        # Truncating at 16 bytes for cleanliness
        return hasher.hexdigest()[:16]

    def generate_code_file(self, code):
        result = os.path.join(consts.MEDIA_DIR, "code", self.code_hash(code) + ".py")
        if not os.path.exists(result):
            first_line = code.split('\n')[0]
            print(f"Writing '{first_line}...' to '{result}''")
            with open(result, "w", encoding="utf-8") as outfile:
                outfile.write(code)
        self.output = self.get_output(result) if self.execute else ""
        return result

    def __init__(self, *code_string, **kwargs):
        # digest_config(self, kwargs)
        self.execute = kwargs.pop("execute", False)
        self.code_file = self.generate_code_file('\n'.join(code_string))
        super().__init__(self.code_file, **kwargs)
        self.center()
