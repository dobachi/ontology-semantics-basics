# プレビューは変更監視つきで起動する。手順と背景は README.md の「プレビュー」を参照。
HOST  ?= localhost
PORT  ?= 4455
PY    ?= python3
CACHE := $(CURDIR)/.cache

.PHONY: version release assets html pdf preview preview-fresh preview-stop check-preview validate deck clean

# 生成物（図、技術要素の章）を作り直す
assets:
	@for f in figures/build_*.py; do $(PY) $$f >/dev/null || exit 1; done
	@$(PY) examples/build_chapter.py >/dev/null
	@$(PY) scripts/build_deck_link.py >/dev/null
	@echo "assets: 図と _elements.qmd を再生成した"

# 一回だけビルドする（プレビュー稼働中は使わない。出力先を取り合う）
html: assets
	XDG_CACHE_HOME=$(CACHE) quarto render --to html

# PDF を作る。調査報告（index.pdf）と前提文書（method.pdf）は別々のファイルになる。
# プレビュー稼働中でも使えるよう、ソースを作業用ディレクトリに写してそこでビルドする
# （同じ場所で render すると、プレビューと出力先を取り合う）
PDF_BUILD := $(CURDIR)/.build-pdf
pdf: assets
	rm -rf $(PDF_BUILD) && mkdir -p $(PDF_BUILD) pdf
	cp -r index.qmd method.qmd _elements.qmd _deck_download.qmd _method_download.qmd _changelog.qmd _quarto.yml _bib figures templates $(PDF_BUILD)/
	@# 図は先に PDF へ変換し、本文の参照も .pdf に書き換える。quarto に変換を任せると、
	@# 図の 1 枚が不完全なファイルになってビルドが落ちることがあった
	@# 図の文字は輪郭に変える（gs -dNoOutputFonts）。そのままだと図ごとに書体が埋め込まれ、
	@# 全体で 30MB 近くになる。輪郭にすると数 MB に収まる。図の中の文字は検索できなくなる
	cd $(PDF_BUILD) && for f in figures/*.svg; do \
	  rsvg-convert -f pdf $$f -o $${f%.svg}.raw.pdf || exit 1; \
	  gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dNoOutputFonts -sOutputFile=$${f%.svg}.pdf $${f%.svg}.raw.pdf || exit 1; \
	  rm -f $${f%.svg}.raw.pdf; done
	cd $(PDF_BUILD) && sed -i -E 's#\(figures/([A-Za-z0-9_-]+)\.svg\)#(figures/\1.pdf)#g' index.qmd method.qmd _elements.qmd
	cd $(PDF_BUILD) && XDG_CACHE_HOME=$(PDF_BUILD)/.cache quarto render --to pdf
	cp $(PDF_BUILD)/_output/index.pdf pdf/ontology-semantics-basics.pdf
	cp $(PDF_BUILD)/_output/method.pdf pdf/ontology-semantics-basics-method.pdf
	@ls -la pdf/*.pdf

# 変更監視つきプレビュー。生成スクリプトの監視、描画の取りこぼしの回復、
# 描画エラー時の再起動を、quarto preview と同時に動かす（scripts/preview.sh）
preview: assets
	@HOST=$(HOST) PORT=$(PORT) CACHE=$(CACHE) PY=$(PY) scripts/preview.sh

# 古い内容のまま更新されなくなったときの復旧
# 停止のパターンは先頭の 1 文字を [ ] で囲む。囲まないと、この行を実行するシェル自身に一致して止まる
preview-fresh: preview-stop
	rm -rf _output .quarto $(CACHE)
	$(MAKE) preview

preview-stop:
	-@pkill -f "[s]cripts/preview.sh" ; pkill -f "[q]uarto.js preview .*--port $(PORT)" ; pkill -f "[s]cripts/watch_assets.py" ; sleep 2

# 配信中の内容が最新かを中身で確かめる
check-preview:
	@$(PY) scripts/check_preview.py http://$(HOST):$(PORT)

# コード例を処理系で検証する（rdflib, pyshacl, jsonschema, pyyaml が必要）
validate:
	$(PY) examples/validate.py $(if $(OSSIE_SCHEMA),--ossie-schema $(OSSIE_SCHEMA))

# 説明ペーパー（pptx）を作る。pptx-build スキルの assets ディレクトリを PPTX_BUILD に指定する
# （python-pptx と PyYAML が必要）
PPTX_BUILD ?= $(HOME)/Sources/claude-skills-marketplace/plugins/pptx-build/skills/pptx-build/assets
# 公開物の版（日付）を変える。VERSION を書き換え、各文書とスライドに反映し、スライドを作り直す。
#   make version V=2026-11-01
version:
	$(PY) scripts/apply_version.py $(V)
	$(MAKE) deck PY=$(PY)

# 版を公開する。改変履歴にその版の行があることを確かめ、タグを付けて push する。
# タグが届くと、GitHub Actions がリリースを作り、その版の HTML と pptx を添える。
release:
	@test -z "$$(git status --porcelain)" || (echo "未コミットの変更がある。先にコミットすること"; exit 1)
	@$(PY) scripts/release_notes.py >/dev/null
	git push origin main
	git tag -a v$$(cat VERSION) -m "$$(cat VERSION) 版"
	git push origin v$$(cat VERSION)

deck: assets
	$(PY) deck/build_figures.py
	cd deck && $(PY) $(PPTX_BUILD)/validate_deck.py deck.yaml | tail -3
	$(PY) deck/template/build_template.py
	cd deck && $(PY) $(PPTX_BUILD)/build_deck.py deck.yaml -o ontology-semantics-intro.pptx --template template/simple.pptx
	cd deck && $(PY) $(PPTX_BUILD)/audit_pptx.py ontology-semantics-intro.pptx | tail -2
	@$(PY) scripts/build_deck_link.py

clean:
	rm -rf _output .quarto $(CACHE) $(PDF_BUILD)
