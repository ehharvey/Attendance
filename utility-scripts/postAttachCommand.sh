#!/usr/bin/env bash

git-credential-manager-core configure
git config pull.ff only
git config credential.credentialStore plaintext

./utility-scripts/configure-git.py


printf "\n\n\n\n\n\n\n\n\n\n"
echo "################################"
echo "#                              #"
echo "#            ALERT             #"
echo "#                              #"
echo "################################"
git push --dry-run