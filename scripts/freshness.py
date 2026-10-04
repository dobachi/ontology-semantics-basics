#!/usr/bin/env python3
"""出力 HTML がソースの本文に追いついているかを、中身で判定する。

ソースから地の文の行、表のセル、節・図・表の ID を抜き出し、HTML に含まれるかを調べる。
地の文だけでは、表や図だけを書き換えた編集を見逃した。
タイムスタンプでは判定しない。描画の途中で届いた編集が取りこぼされると、
出力の時刻は新しいのに中身が古い、という状態になるためである。
"""
import html, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = {"index.html": ["index.qmd", "_elements.qmd"], "method.html": ["method.qmd"]}
_SKIP = re.compile(r"[@`\[\]*|{}<>\"\\]|^\s*(#|-|!|:|\d+\.|>|```|---)")

def plain_lines(qmd_text):
    """Markdown 記法や引用を含まない、照合に使える地の文の行だけを返す。"""
    out, in_code, in_front = [], False, False
    for i, line in enumerate(qmd_text.split("\n")):
        s = line.strip()
        if i == 0 and s == "---": in_front = True; continue
        if in_front:
            if s == "---": in_front = False
            continue
        if s.startswith("```"): in_code = not in_code; continue
        if in_code or len(s) < 25 or _SKIP.search(s): continue
        out.append(s)
    return out

def table_cells(qmd_text):
    """表のセルのうち、Markdown 記法や引用を含まない、照合に使える文字列を返す。"""
    out = []
    for line in qmd_text.split("\n"):
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("|-: "): continue
        for cell in s.strip("|").split("|"):
            c = cell.strip()
            if len(c) >= 12 and not re.search(r"[@`\[\]*{}<>\"\\]", c): out.append(c)
    return out

def anchor_ids(qmd_text):
    """節、図、表の ID。図や表だけを足した編集を見逃さないために照合する。"""
    return sorted(set(re.findall(r"\{#((?:sec|fig|tbl)-[A-Za-z0-9_-]+)", qmd_text)))

def html_text(h):
    h = re.sub(r"<script.*?</script>|<style.*?</style>", "", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h)))

def missing_lines(html_str, page="index.html"):
    """ソースにあって配信中の HTML にないものを返す。地の文、表のセル、節・図・表の ID を照合する。"""
    text = html_text(html_str)
    src = ""
    for f in SOURCES[page]:
        with open(os.path.join(ROOT, f), encoding="utf-8") as fh:
            src += fh.read() + "\n"
    items = plain_lines(src) + table_cells(src)
    miss = [l for l in items if re.sub(r"\s+", " ", l) not in text]
    ids = anchor_ids(src)
    miss += [f"ID: {i}" for i in ids if f'id="{i}"' not in html_str]
    return miss, len(items) + len(ids)
