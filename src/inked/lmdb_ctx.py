import logging
import time
from pathlib import Path
from typing import Any, Dict

import lmdb

from .utils import pil_to_bytes

logger = logging.getLogger()


class LMDBMaker(object):
    """A context manager wrapper for batching image-label pairs into an lmdb file"""

    def __init__(self, path: Path):
        self.path = path
        self.path.mkdir(parents=True, exist_ok=True)
        self.cache: Dict[Any, Any] = {}
        self.cnt = 1
        self.batch_size = 1_000
        self.map_size = 1_000_000_000_000  # 1_000_000 is 1MB

    def __enter__(self):
        """Creates a lmdb environment and starts a timer"""
        logger.info("Creating Environment")
        self.start_time = time.time()
        self.env = lmdb.open(str(self.path), map_size=self.map_size)
        return self

    def _write_to_cache(self):
        """Writes out the cached content to disk using the lmdb environment"""
        with self.env.begin(write=True) as txn:
            for k, v in self.cache.items():
                txn.put(k, v)
            self.cache = {}

    def append(self, label: str, img: bytes):
        """Adds in the label and image into cache, then batches the saving to disk"""
        self.cache[f"image-{self.cnt:09d}".encode()] = pil_to_bytes(img)
        self.cache[f"label-{self.cnt:09d}".encode()] = label.encode()
        if self.cnt % self.batch_size == 0:
            self._write_to_cache()
        self.cnt += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Writes out the final cached batch out to the LMDB and finishes the timer"""
        self._write_to_cache()
        self.env.close()
        logger.info(f"Created {self.cnt} entries in {round(time.time()-self.start_time,2)} seconds")
