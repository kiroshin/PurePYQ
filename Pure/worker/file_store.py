#  file_store.py
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.
import os
import re

_PATTERN_ILLEGAL_FILENAME = re.compile(r'^[ .]|[/<>:\"\\|?*]+|[ .]$')


class FileStore:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    def set_cache_file(self, filename: str, data: bytes) -> str:
        fn = _PATTERN_ILLEGAL_FILENAME.sub('_', filename)
        target_path = os.path.join(self.cache_path, fn)
        with open(target_path, "wb") as f:
            f.write(data)
        return target_path

    def get_cache_path(self, filename: str) -> str | None:
        fn = _PATTERN_ILLEGAL_FILENAME.sub('_', filename)
        target_path = os.path.join(self.cache_path, fn)
        if os.path.isfile(target_path):
            return target_path
        return None

    def clear_cache_file(self):
        if os.path.exists(self.cache_path):
            # listdir 로 뽑아내서 dir 을 붙이는 것과 동일
            for file in os.scandir(self.cache_path):
                if not file.name.endswith(".log"):
                    os.remove(file.path)
