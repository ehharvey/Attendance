#! /bin/sh

TEMP_FILE="$(mktemp)" &&

pip install -r ./requirements.txt &&

wget -O "$TEMP_FILE" https://github.com/GitCredentialManager/git-credential-manager/releases/latest/download/gcm-linux_amd64.2.0.785.deb &&
sudo dpkg -i "$TEMP_FILE" &&
git-credential-manager-core configure
git config pull.ff only
git config credential.credentialStore plaintext

./utility-scripts/configure-git.py


rm -f "$TEMP_FILE"