#!/usr/bin/env python3
"""公開物の版（日付）を、一か所から各ファイルへ反映する。

版は VERSION に YYYY-MM-DD で書く。同じ日に二度出すときは 2026-10-04.2 のように枝番を付ける。
このスクリプトは、その値を次の場所に書き込む。

  index.qmd、method.qmd    前書きの date（HTML と PDF の題名の下に出る）
  deck/deck.yaml           meta.date と、表紙の date（スライドの表紙に出る）

ダウンロードする pptx のファイル名は、scripts/build_deck_link.py が VERSION を読んで決める。

    python3 scripts/apply_version.py            # VERSION の値を反映する
    python3 scripts/apply_version.py 2026-11-01  # VERSION を書き換えてから反映する
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vfile = os.path.join(ROOT, "VERSION")
if len(sys.argv) > 1:
    open(vfile, "w").write(sys.argv[1].strip() + "\n")
version = open(vfile).read().strip()
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}(\.\d+)?", version):
    sys.exit("VERSION は YYYY-MM-DD（必要なら .N の枝番つき）で書く: %r" % version)

def sub(path, pattern, repl, count):
    p = os.path.join(ROOT, path)
    text = open(p, encoding="utf-8").read()
    new, n = re.subn(pattern, repl, text, count=count, flags=re.M)
    if n != count:
        sys.exit("%s: 書き換える箇所が %d 件見つかるはずが %d 件だった" % (path, count, n))
    open(p, "w", encoding="utf-8").write(new)

for doc in ("index.qmd", "method.qmd"):
    sub(doc, r'^date: .*$', 'date: "%s"' % version, 1)
sub("deck/deck.yaml", r'^(\s+)date: ".*"$', r'\1date: "%s"' % version, 2)
print("version:", version)
