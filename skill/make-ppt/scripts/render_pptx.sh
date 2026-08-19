#!/usr/bin/env bash
# render_pptx.sh <deck.pptx> <preview_dir> [dpi] [slides]
# Renders every slide, or only a selection such as "3,7-9", to slide-NN.png.
# A partial render preserves unaffected preview files for localized edits.
set -euo pipefail

DECK="$(realpath "$1")"
OUT="$2"
DPI="${3:-140}"
SLIDES="${4:-}"
if [ "$#" -gt 4 ]; then
  echo "ERROR: too many arguments" >&2
  exit 2
fi

mkdir -p "$OUT"
OUT="$(realpath "$OUT")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

has_cmd() { command -v "$1" >/dev/null 2>&1; }

is_macos() { [ "$(uname -s 2>/dev/null)" = "Darwin" ]; }

mac_powerpoint_available() {
  [ -d "/Applications/Microsoft PowerPoint.app" ] ||
    [ -d "$HOME/Applications/Microsoft PowerPoint.app" ] ||
    { has_cmd open && open -Ra "Microsoft PowerPoint" >/dev/null 2>&1; }
}

to_windows_path() {
  if has_cmd cygpath; then
    cygpath -w "$1"
  elif has_cmd wslpath; then
    wslpath -w "$1"
  else
    printf '%s\n' "$1"
  fi
}

to_windows_file_url() {
  if has_cmd cygpath; then
    printf 'file:///%s/lo\n' "$(cygpath -m "$1")"
  elif has_cmd wslpath; then
    printf 'file:///%s/lo\n' "$(wslpath -m "$1")"
  else
    printf 'file://%s/lo\n' "$1"
  fi
}

is_windows_exe() {
  case "$1" in
    *.exe|*.EXE|/mnt/[a-zA-Z]/*|/[a-zA-Z]/*) return 0 ;;
    *) return 1 ;;
  esac
}

print_selected_numbers() {
  if [ -z "$SLIDES" ]; then
    return 0
  fi
  local token start end number
  local parts=()
  IFS=',' read -r -a parts <<< "$SLIDES"
  for token in "${parts[@]}"; do
    token="$(printf '%s' "$token" | tr -d '[:space:]')"
    if [[ "$token" =~ ^([0-9]+)-([0-9]+)$ ]]; then
      start="${BASH_REMATCH[1]}"; end="${BASH_REMATCH[2]}"
      for ((number=start; number<=end; number++)); do printf '%s\n' "$number"; done
    else
      printf '%s\n' "$token"
    fi
  done
}

validate_slide_spec() {
  if [ -z "$SLIDES" ]; then
    return 0
  fi
  local token start end
  local parts=()
  IFS=',' read -r -a parts <<< "$SLIDES"
  for token in "${parts[@]}"; do
    token="$(printf '%s' "$token" | tr -d '[:space:]')"
    if [[ "$token" =~ ^([0-9]+)-([0-9]+)$ ]]; then
      start="${BASH_REMATCH[1]}"; end="${BASH_REMATCH[2]}"
      [ "$start" -ge 1 ] && [ "$start" -le "$end" ] || {
        echo "ERROR: invalid slide range: $token" >&2; exit 2;
      }
    elif [[ "$token" =~ ^[0-9]+$ ]] && [ "$token" -ge 1 ]; then
      :
    else
      echo "ERROR: invalid slide selection: $token" >&2
      exit 2
    fi
  done
}

slide_selected() {
  local number="$1" selected
  if [ -z "$SLIDES" ]; then
    return 0
  fi
  while IFS= read -r selected; do
    [ "$selected" = "$number" ] && return 0
  done < <(print_selected_numbers)
  return 1
}

clear_previews() {
  if [ -z "$SLIDES" ]; then
    rm -f "$OUT"/slide-*.png
  else
    local number
    while IFS= read -r number; do
      rm -f "$OUT/slide-$(printf '%02d' "$number").png"
    done < <(print_selected_numbers)
  fi
}

list_selected_previews() {
  if [ -z "$SLIDES" ]; then
    ls -1 "$OUT"/slide-*.png
  else
    local number path
    while IFS= read -r number; do
      path="$OUT/slide-$(printf '%02d' "$number").png"
      [ -f "$path" ] || return 1
      printf '%s\n' "$path"
    done < <(print_selected_numbers)
  fi
}

page_files() {
  local directory="$1" f page
  for f in "$directory"/rendered-*.png; do
    [ -e "$f" ] || continue
    page="${f##*rendered-}"; page="${page%.png}"
    printf '%08d\t%s\n' "$page" "$f"
  done | sort -n | cut -f2-
}

convert_pdf_to_previews() {
  local pdf="$1" temporary="$2" f
  if ! pdftoppm -png -r "$DPI" "$pdf" "$temporary/rendered"; then
    echo "ERROR: PDF to PNG conversion failed" >&2
    return 3
  fi

  local i=1
  while IFS= read -r f; do
    if slide_selected "$i"; then
      mv "$f" "$OUT/slide-$(printf '%02d' "$i").png"
    fi
    i=$((i+1))
  done < <(page_files "$temporary")
  list_selected_previews
}

require_pdftoppm() {
  if has_cmd pdftoppm; then
    return 0
  fi
  echo "ERROR: pdftoppm not found. Install Poppler:" >&2
  echo "  macOS:   brew install poppler" >&2
  echo "  Debian:  sudo apt install poppler-utils" >&2
  exit 2
}

validate_slide_spec
clear_previews

# ------------------------------------------------------ primary: PowerPoint for macOS
# Launch Services catches App Store and non-standard installations; the explicit paths
# keep detection working when Spotlight/Launch Services metadata is unavailable.
if is_macos && has_cmd osascript && mac_powerpoint_available &&
    [ -f "$SCRIPT_DIR/render_ppt_mac.applescript" ]; then
  require_pdftoppm
  OFFICE_TMP="$HOME/Library/Group Containers/UBF8T346G9.Office/TemporaryItems"
  if [ -d "$OFFICE_TMP" ] && [ -w "$OFFICE_TMP" ]; then
    TMP="$(mktemp -d "$OFFICE_TMP/make-ppt.XXXXXX")"
  else
    TMP="$(mktemp -d)"
  fi
  trap 'rm -rf "$TMP"' EXIT
  PDF="$TMP/rendered.pdf"
  if osascript "$SCRIPT_DIR/render_ppt_mac.applescript" "$DECK" "$PDF" &&
      [ -f "$PDF" ] && convert_pdf_to_previews "$PDF" "$TMP"; then
    exit 0
  fi
  echo "PowerPoint for macOS rendering failed; falling back to LibreOffice." >&2
  rm -rf "$TMP"
  trap - EXIT
fi

# ------------------------------------------------------- primary: PowerPoint for Windows
# Pixel width for the requested DPI on a 13.333" wide slide (13.333 = 40/3).
WIDTH=$(( DPI * 40 / 3 ))
PWSH=""
if ! is_macos; then
  for c in powershell.exe pwsh.exe powershell pwsh; do
    if has_cmd "$c"; then PWSH="$c"; break; fi
  done
fi
if [ -n "$PWSH" ] && [ -f "$SCRIPT_DIR/render_ppt_com.ps1" ]; then
  if is_windows_exe "$PWSH"; then
    PS1="$(to_windows_path "$SCRIPT_DIR/render_ppt_com.ps1")"
    DECK_W="$(to_windows_path "$DECK")"; OUT_W="$(to_windows_path "$OUT")"
  else
    PS1="$SCRIPT_DIR/render_ppt_com.ps1"; DECK_W="$DECK"; OUT_W="$OUT"
  fi
  PS_ARGS=(-NoProfile -ExecutionPolicy Bypass -File "$PS1" -Deck "$DECK_W" -OutDir "$OUT_W" -Width "$WIDTH")
  if [ -n "$SLIDES" ]; then PS_ARGS+=(-Slides "$SLIDES"); fi
  if "$PWSH" "${PS_ARGS[@]}" && list_selected_previews; then
    exit 0
  fi
  echo "PowerPoint COM unavailable — falling back to LibreOffice." >&2
fi

# ---------------------------------------------------------------- fallback: LibreOffice
SOFFICE=""
for c in soffice soffice.exe libreoffice; do
  if has_cmd "$c"; then SOFFICE="$c"; break; fi
done
if [ -z "$SOFFICE" ]; then
  for p in \
    "/mnt/c/Program Files/LibreOffice/program/soffice.exe" \
    "/mnt/c/Program Files (x86)/LibreOffice/program/soffice.exe" \
    "/c/Program Files/LibreOffice/program/soffice.exe" \
    "/c/Program Files (x86)/LibreOffice/program/soffice.exe" \
    "$HOME/AppData/Local/Programs/LibreOffice/program/soffice.exe" \
    "/Applications/LibreOffice.app/Contents/MacOS/soffice" \
    "/usr/bin/soffice" "/usr/local/bin/soffice" "/opt/libreoffice/program/soffice"; do
    if [ -x "$p" ]; then SOFFICE="$p"; break; fi
  done
fi
if [ -z "$SOFFICE" ]; then
  echo "ERROR: no renderer available. Install Microsoft PowerPoint (preferred) or LibreOffice:" >&2
  echo "  Windows: PowerPoint is used automatically if installed" >&2
  echo "  macOS:   install Microsoft PowerPoint, or: brew install --cask libreoffice" >&2
  echo "  Debian:  sudo apt install libreoffice" >&2
  exit 2
fi
require_pdftoppm

# soffice may be either a native Windows app (Git Bash/MSYS/WSL interop) or a Unix app.
if is_windows_exe "$SOFFICE"; then
  TMP="$(mktemp -d "$OUT/.render-tmp.XXXXXX")"
else
  TMP="$(mktemp -d)"
fi
trap 'rm -rf "$TMP"' EXIT
if is_windows_exe "$SOFFICE"; then
  PROFILE_URL="$(to_windows_file_url "$TMP")"
  DECK_ARG="$(to_windows_path "$DECK")"
  OUT_ARG="$(to_windows_path "$TMP")"
else
  PROFILE_URL="file://$TMP/lo"
  DECK_ARG="$DECK"
  OUT_ARG="$TMP"
fi
if ! "$SOFFICE" --headless --norestore --nofirststartwizard --nolockcheck \
        -env:UserInstallation="$PROFILE_URL" \
        --convert-to pdf --outdir "$OUT_ARG" "$DECK_ARG" >/dev/null; then
  echo "ERROR: LibreOffice conversion failed" >&2
  exit 3
fi
PDF="$TMP/$(basename "${DECK%.pptx}").pdf"
[ -f "$PDF" ] || { echo "ERROR: PDF conversion failed" >&2; exit 3; }
convert_pdf_to_previews "$PDF" "$TMP"
