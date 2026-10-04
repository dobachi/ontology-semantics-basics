#!/usr/bin/env python3
"""調査報告の HTML に埋め込む、説明ペーパー（pptx）のダウンロードリンクを作る。

調査報告の HTML は 1 ファイルで完結する（embed-resources）。別ファイルへのリンクにすると、
HTML だけを渡したときに切れる。そこで pptx を base64 にして HTML の中に埋め込み、
リンクを押すとその場で保存できるようにする。あわせて、PDF へのリンクも作る。PDF は、版の入ったファイル名で
HTML の隣に置かれる。出力は _deck_download.qmd（調査報告用）と _method_download.qmd（前提文書用）。保存されるファイル名には、VERSION の版（日付）が入る。出力は _deck_download.qmd で、index.qmd が
取り込む。HTML のときだけ表示され、PDF には出ない。

    python3 scripts/build_deck_link.py     # deck/ontology-semantics-intro.pptx -> _deck_download.qmd
"""
import base64, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "deck", "ontology-semantics-intro.pptx")
OUT = os.path.join(ROOT, "_deck_download.qmd")
MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"

version = open(os.path.join(ROOT, "VERSION")).read().strip()
# PDF は、版の入ったファイル名で公開する（公開の処理が、この名前で HTML の隣に置く）
PDF_INDEX = "ontology-semantics-basics-%s.pdf" % version
PDF_METHOD = "ontology-semantics-basics-method-%s.pdf" % version
pdf_link = '<p><a href="%s">%s（PDF、%s 版）をダウンロード</a></p>\n'

body = ('::: {.content-visible when-format="html"}\n```{=html}\n'
        + pdf_link % (PDF_INDEX, "この調査報告", version) + '```\n:::\n\n')
if os.path.exists(SRC):
    from zipfile import ZipFile
    with ZipFile(SRC) as z:
        slides = len([n for n in z.namelist() if n.startswith("ppt/slides/slide") and n.endswith(".xml")])
    name = "ontology-semantics-intro-%s.pptx" % version
    data = base64.b64encode(open(SRC, "rb").read()).decode("ascii")
    size = os.path.getsize(SRC) / 1e6
    body += ('::: {.content-visible when-format="html"}\n'
            '初めて読む人向けの説明ペーパーもある。\n\n```{=html}\n'
            '<p><a download="%s" href="data:%s;base64,%s">'
            '説明ペーパー（PowerPoint、%s 版、%d 枚、%.1f MB）をダウンロード</a></p>\n```\n:::\n'
            % (name, MIME, data, version, slides, size))
open(OUT, "w", encoding="utf-8").write(body)
open(os.path.join(ROOT, "_method_download.qmd"), "w", encoding="utf-8").write(
    '::: {.content-visible when-format="html"}\n```{=html}\n'
    + pdf_link % (PDF_METHOD, "この文書", version) + '```\n:::\n')
print("deck link:", "embedded %d bytes" % len(body) if body else "deck not found; link omitted")
