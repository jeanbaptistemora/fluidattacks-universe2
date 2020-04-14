# Decrypt

```sh
echo "${ENCRYPTION_KEY}" \
  | gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt secrets/development.sh.asc \
    > secrets/development.sh

echo "${ENCRYPTION_KEY_PROD}" \
  | gpg \
      --batch \
      --passphrase-fd 0 \
      --decrypt secrets/production.sh.asc \
    > secrets/production.sh
```

# Encrypt

```sh
echo "${ENCRYPTION_KEY}" \
  | gpg --symmetric \
        --cipher-algo AES256 \
        --digest-algo SHA512 \
        --passphrase-fd 0 \
        --armor \
        --batch \
        --yes \
      secrets/development.sh

echo "${ENCRYPTION_KEY_PROD}" \
  | gpg --symmetric \
        --cipher-algo AES256 \
        --digest-algo SHA512 \
        --passphrase-fd 0 \
        --armor \
        --batch \
        --yes \
      secrets/production.sh
```
