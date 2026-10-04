#!/usr/bin/env python3
"""調査報告の HTML に埋め込む、説明ペーパー（pptx）のダウンロードリンクを作る。

調査報告の HTML は 1 ファイルで完結する（embed-resources）。別ファイルへのリンクにすると、
HTML だけを渡したときに切れる。そこで pptx を base64 にして HTML の中に埋め込み、
リンクを押すとその場で保存できるようにする。保存されるファイル名には、VERSION の版（日付）が入る。出力は _deck_download.qmd で、index.qmd が
取り込む。HTML のときだけ表示され、PDF には出ない。

    python3 scripts/build_deck_link.py     # deck/ontology-semantics-intro.pptx -> _deck_download.qmd
"""
import base64, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deck", "ontology-semantics-intro.pptx")
OUT = os.path.join(ROOT, "_deck_download.qmd")
MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

body = ""
if os.path.exists(SRC):
    from zipfile import ZipFile
    with ZipFile(SRC) as z:
        slides = len([n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
    version = open(os.path.join(ROOT, "VERSION")).read().strip()
    name = "ontology-semantics-intro-%s.pptx" % version
    data = base64.b64encode(open(SRC, "rb").read()).decode("ascii")
    size = os.path.getsize(SRC) / 1e6
    body = ('::: {.content-visible when-format="html"}\n'
            '初めて読む人向けの説明ペーパーもある。\n\n```{=html}\n'
            '<p><a download="%s" href="data:%s;base64,%s">'
            '説明ペーパー（PowerPoint、%s 版、%d 枚、%.1f MB）をダウンロード</a></p>\n```\n:::\n'
            % (name, MIME, data, version, slides, size))
open(OUT, "w", encoding="utf-8").write(body)
print("deck link:", "embedded %d bytes" % len(body) if body else "deck not found; link omitted")
