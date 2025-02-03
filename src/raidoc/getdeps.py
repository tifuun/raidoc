"""Dependency downloader for raidoc"""

from pathlib import Path
import urllib.request
from hashlib import sha256
from zipfile import ZipFile
from sys import stderr

def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def getdeps(source: Path, target: Path):
    for path in (source).rglob('*.url'):
        download_dest = target / (path.with_suffix('').name)

        if download_dest.exists():
            eprint(f'Skipping {download_dest}...')
            continue

        url = path.read_text()

        eprint(f'Downloading {download_dest} from {url}...')
        urllib.request.urlretrieve(url, download_dest)

        hash_file = path.with_suffix('.sha256')

        sha256_actual = sha256(download_dest.read_bytes()).hexdigest()

        if not hash_file.exists():
            eprint("Hashfile missing, creating.")
            hash_file.write_text(sha256_actual)

        else:
            sha256_expected = hash_file.read_text().strip()

            if sha256_expected == sha256_actual:
                eprint("hash OK")

            else:
                eprint("Hash mismatch.")
                exit(1)

