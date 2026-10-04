#!/usr/bin/env python3
"""リリースの説明文を、改変履歴（_changelog.qmd）の該当する版の行から作る。

版は VERSION から読む。引数で指定してもよい。改変履歴にその版の行がなければ、
終了コード 1 で止まる。版を出す前に改変履歴を書き忘れるのを防ぐためである。

    python3 scripts/release_notes.py            # VERSION の版
    python3 scripts/release_notes.py 2026-11-01
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
version = sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(ROOT, "VERSION")).read().strip()
for line in open(os.path.join(ROOT, "_changelog.qmd"), encoding="utf-8"):
    m = re.match(r"\|\s*%s\s*\|\s*(.*?)\s*\|\s*$" % re.escape(version), line)
    if m:
        items = [s.strip() for s in re.split(r"。\s*", m.group(1)) if s.strip()]
        print("%s 版\n" % version)
        for it in items:
            print("- %s" % it)
        print("\n調査報告: https://dobachi.github.io/ontology-semantics-basics/")
        print("この版の調査報告、前提文書、説明ペーパーを添付している。")
        sys.exit(0)
sys.exit("改変履歴（_changelog.qmd）に %s の行がない。版を出す前に書くこと" % version)
