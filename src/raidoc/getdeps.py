"""Dependency downloader for raidoc"""

from pathlib import Path
import urllib.request
from hashlib import sha256
from zipfile import ZipFile
from sys import stderr

class CustomURLOpener(urllib.request.FancyURLopener):
    """
    FancyURLopener with browser-like user agent.

    fontawesome.com maintainers for some reason but a user
    agent filter on their releases endpoint,
    so we have to perform this incantation to download
    things from there.
    """
    version = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

opener = CustomURLOpener()

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
        opener.retrieve(url, download_dest)

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

    for path in (target).rglob('*.zip'):
        extract_path = path.with_suffix('')

        if extract_path.exists():
            eprint(f'{path} already extracted')
        else:
            eprint(f'Extracting {path}')
            # FIXME prevent zipslip!!
            with ZipFile(path) as zip:
                zip.extractall(extract_path)

