#!/usr/bin/env python3
"""プレビューが最新の内容を出しているかを確かめる。

配信中の HTML を取得し、ソースの地の文がすべて含まれるかを照合する（scripts/freshness.py）。
タイムスタンプや HTTP 200 では、古い内容のまま配信されている状態を見抜けないため、中身で判定する。
"""
import os, sys, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freshness
base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:4455"
base = base.rsplit("/", 1)[0] if base.endswith(".html") else base.rstrip("/")
bad = 0
for page in freshness.SOURCES:
    try:
        h = urllib.request.urlopen(f"{base}/{page}", timeout=30).read().decode("utf-8")
    except Exception as e:
        print(f"取得できない: {base}/{page} ({e})"); sys.exit(2)
    if 'quarto-render-error' in h[:4000]:
        bad += 1; print(f"描画エラー: {page} はエラーページを返している（監視が自動で起動し直す。1 分ほど待つ）"); continue
    miss, total = freshness.missing_lines(h, page)
    if miss:
        bad += 1
        print(f"古い内容の可能性: {page} で {len(miss)}/{total} 項目が配信中の HTML にない")
        for l in miss[:5]: print("  -", l[:60])
    else:
        print(f"最新: {page} は {total} 項目（地の文、表のセル、ID）がすべて配信中の HTML にある")
if bad: print("対処: 数十秒待って再確認する。直らなければ make preview-fresh")
sys.exit(1 if bad else 0)
