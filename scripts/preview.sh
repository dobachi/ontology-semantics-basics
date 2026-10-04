#!/bin/bash
# 変更監視つきプレビューを起動する。make preview から呼ばれる。
#
# 描画は HTML だけにする（--render html）。指定しないと PDF まで作ろうとして配信が止まる。
#
# quarto preview が終了したら、キャッシュを消して起動し直す。
# 監視（watch_assets.py）は、配信がエラーページになったのを検知すると quarto preview を止める。
# その結果ここに戻ってきて、きれいな状態から立ち上がり直す。
set -u
HOST="${HOST:-localhost}"; PORT="${PORT:-4455}"; CACHE="${CACHE:-$PWD/.cache}"; PY="${PY:-python3}"
export PREVIEW_URL="http://$HOST:$PORT"
export PREVIEW_KILL_PATTERN="[q]uarto.js preview .*--port $PORT"

"$PY" scripts/watch_assets.py & WATCH=$!
cleanup() { kill "$WATCH" 2>/dev/null; pkill -f "$PREVIEW_KILL_PATTERN" 2>/dev/null; exit 0; }
trap cleanup INT TERM
trap 'kill "$WATCH" 2>/dev/null' EXIT

while true; do
  XDG_CACHE_HOME="$CACHE" quarto preview --render html --host "$HOST" --port "$PORT" --no-browser
  echo "[preview] quarto preview が終了した。キャッシュを消して起動し直す"
  rm -rf "$CACHE" .quarto
  sleep 2
done
