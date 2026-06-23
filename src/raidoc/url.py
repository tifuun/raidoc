"""URL opener/downloader for getdep.py module"""

import urllib.request
import sys

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

if sys.version_info.minor < 14:
    class CustomURLOpener(urllib.request.FancyURLopener):
        """
        FancyURLopener with browser-like user agent.

        fontawesome.com maintainers for some reason but a user
        agent filter on their releases endpoint,
        so we have to perform this incantation to download
        things from there.
        """
        version = USER_AGENT

    opener = CustomURLOpener()

    def urlget(url, download_dest):
        return opener.retrieve(url, download_dest)

else:
    def urlget(url, download_dest):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', USER_AGENT)
        with urllib.request.urlopen(req) as remote:
            with download_dest.open('wb') as local:
                local.write(remote.read())

