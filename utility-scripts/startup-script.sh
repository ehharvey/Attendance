#! /bin/sh

TEMP_FILE="$(mktemp)" &&

pip install -r ./requirements.txt &&

wget -O "$TEMP_FILE" https://github.com/GitCredentialManager/git-credential-manager/releases/latest/download/gcm-linux_amd64.2.0.785.deb &&
sudo dpkg -i "$TEMP_FILE"

rm -f "$TEMP_FILE"