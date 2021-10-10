#!/usr/bin/env bash

set -eufo pipefail

src="$1"

echo "Resizing $src"
convert -resize x3040 -filter Lanczos "$src" "$src.tmp1"
echo "Converting $src to WebP"
cwebp -q 95 "$src.tmp1" -o "$(dirname "$src")/$(basename "$(basename "$src" .png)" .jpg).webp" &
wait

rm -f "$src" "$src.tmp1"
