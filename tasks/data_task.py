import logging
import shutil
from pathlib import Path

DATA_ROOT = Path("/Users/ashiqurrahman/DE_Projects/airflow29_home/data")
TMP = DATA_ROOT / "tmp"
DEST = DATA_ROOT / "dest"
log = logging.getLogger(__name__)

def make_file(ts_nodash: str):
    TMP.mkdir(parents=True, exist_ok=True)
    p = TMP / f"my_file_{ts_nodash}.txt"
    p.write_text("This is my file, created by python\n")
    log.info("Created %s", p)

def move_it(ts_nodash: str):
    src = TMP / f"my_file_{ts_nodash}.txt"
    DEST.mkdir(parents=True, exist_ok=True)
    dst = DEST / f"my_file_{ts_nodash}.txt"
    shutil.move(str(src), str(dst))
    log.info("Moved %s -> %s", src, dst)
