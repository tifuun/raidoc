#!/bin/sh

rm -rf fontawesome*
rm -rf doc/fontawesome*
wget https://use.fontawesome.com/releases/v6.6.0/fontawesome-free-6.6.0-web.zip
unzip fontawesome-free-6.6.0-web.zip 
mv fontawesome-free-6.6.0-web doc/fontawesome

exit 0

