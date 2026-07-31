#!/usr/bin/env bash
# run_python.sh <script.py> [args...]
# Run a Python 3 script with the first WORKING interpreter.
# Why this exists: on Windows the Microsoft Store ships a fake `python3` shim that
# sits on PATH and exits 49 without running anything. WSL may also expose a Linux
# Python that lacks the Windows-side presentation dependencies. Detection must
# execute the interpreter and prefer Windows Python when it is visible.
set -euo pipefail

PY=""
for c in python.exe py.exe python3 python py; do
  if v="$("$c" -c 'import sys;print(sys.version_info[0])' 2>/dev/null | tr -d '\r')" && [ "$v" = "3" ]; then
    PY="$c"; break
  fi
done

if [ -z "$PY" ]; then
  echo "ERROR: no working Python 3 interpreter found (tried python.exe, py.exe, python3, python, py)." >&2
  echo "  Install Python 3 and ensure it is on PATH, then retry." >&2
  exit 1
fi

is_windows_python() {
  case "$PY" in
    *.exe|*.EXE) return 0 ;;
    *) return 1 ;;
  esac
}

path_like() {
  case "$1" in
    */*|*\\*) return 0 ;;
    *) [ -e "$1" ] ;;
  esac
}

to_windows_path() {
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  elif command -v wslpath >/dev/null 2>&1; then
    wslpath -w "$1"
  else
    printf '%s\n' "$1"
  fi
}

convert_path_arg() {
  local arg="$1"
  if ! path_like "$arg"; then
    printf '%s\n' "$arg"
    return
  fi

  local abs=""
  if [ -e "$arg" ]; then
    abs="$(realpath "$arg")"
  else
    local dir base
    dir="$(dirname "$arg")"
    base="$(basename "$arg")"
    if [ -d "$dir" ]; then
      abs="$(cd "$dir" && pwd)/$base"
    fi
  fi

  if [ -n "$abs" ]; then
    to_windows_path "$abs"
  else
    printf '%s\n' "$arg"
  fi
}

if is_windows_python && [ "${1:-}" != "-c" ]; then
  args=()
  for arg in "$@"; do
    args+=("$(convert_path_arg "$arg")")
  done
  exec "$PY" "${args[@]}"
fi

exec "$PY" "$@"
