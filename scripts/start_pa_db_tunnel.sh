#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"

read_env_var() {
  local key="$1"
  local file="$2"
  awk -F= -v k="$key" '$1==k {sub($1"=",""); print; exit}' "$file"
}

if [[ -f "${ENV_FILE}" ]]; then
  PA_SSH_USER="${PA_SSH_USER:-$(read_env_var PA_SSH_USER "${ENV_FILE}")}"
  PA_SSH_HOST="${PA_SSH_HOST:-$(read_env_var PA_SSH_HOST "${ENV_FILE}")}"
  PA_DB_REMOTE_HOST="${PA_DB_REMOTE_HOST:-$(read_env_var PA_DB_REMOTE_HOST "${ENV_FILE}")}"
  PA_DB_REMOTE_PORT="${PA_DB_REMOTE_PORT:-$(read_env_var PA_DB_REMOTE_PORT "${ENV_FILE}")}"
  PA_DB_LOCAL_PORT="${PA_DB_LOCAL_PORT:-$(read_env_var PA_DB_LOCAL_PORT "${ENV_FILE}")}"
fi

: "${PA_SSH_USER:?PA_SSH_USER is required in .env (your PythonAnywhere username)}"
: "${PA_DB_REMOTE_HOST:?PA_DB_REMOTE_HOST is required in .env}"
: "${PA_DB_REMOTE_PORT:?PA_DB_REMOTE_PORT is required in .env}"

PA_SSH_HOST="${PA_SSH_HOST:-ssh.pythonanywhere.com}"
PA_DB_LOCAL_PORT="${PA_DB_LOCAL_PORT:-15432}"

echo "Opening SSH tunnel:"
echo "  localhost:${PA_DB_LOCAL_PORT} -> ${PA_DB_REMOTE_HOST}:${PA_DB_REMOTE_PORT}"
echo "  via ${PA_SSH_USER}@${PA_SSH_HOST}"
echo ""
echo "Keep this terminal open while using Django locally."

exec ssh -N \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=60 \
  -o PubkeyAuthentication=no \
  -o PreferredAuthentications=password \
  -L "${PA_DB_LOCAL_PORT}:${PA_DB_REMOTE_HOST}:${PA_DB_REMOTE_PORT}" \
  "${PA_SSH_USER}@${PA_SSH_HOST}"
