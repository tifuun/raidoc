"""Dependency downloader for raidoc"""

from pathlib import Path
from shutil import copy
from hashlib import sha256
from zipfile import ZipFile
from sys import stderr

from raidoc.url import urlget


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def getdeps(source: Path, target: Path, cachedir: Path | None = None):
    if cachedir is not None:
        cachedir.mkdir(exist_ok=True, parents=True)

    for path in (source).rglob('*.url'):
        download_dest = target / (path.with_suffix('').name)

        if download_dest.exists():
            eprint(f'Skipping {download_dest}...')
            continue

        if cachedir is None:
            eprint(f"Cache is disabled...")
        else:
            cache_file = cachedir / (path.with_suffix('').name)
            if cache_file.exists():
                eprint(f"Using cached {cache_file}.")
                copy(cache_file, download_dest)
                continue
            pass

        url = path.read_text()

        eprint(f'Downloading {download_dest} from {url}...')
        urlget(url, download_dest)

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

        if cachedir is not None:
            eprint(f"Saving to cachefile: {cache_file}.")
            copy(download_dest, cache_file)

    for path in (target).rglob('*.zip'):
        extract_path = path.with_suffix('')

        if extract_path.exists():
            eprint(f'{path} already extracted')
        else:
            eprint(f'Extracting {path}')
            # FIXME prevent zipslip!!
            with ZipFile(path) as zip:
                zip.extractall(extract_path)

