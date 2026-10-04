# オントロジー・セマンティクス・データモデル標準化の基礎調査

オントロジー、セマンティクス、データモデル標準化の概念を、古典的な研究から近年の米国企業の取り組み（Open Semantic Interchange、現 Apache Ossie など）まで体系的に整理する調査である。
初心者向けの説明ペーパー（pptx）も含む。

## 公開先

| 内容 | URL |
|---|---|
| 調査報告 | <https://dobachi.github.io/ontology-semantics-basics/> |
| 前提文書（調査の方法と検証の記録） | <https://dobachi.github.io/ontology-semantics-basics/method.html> |
| リポジトリ | <https://github.com/dobachi/ontology-semantics-basics> |

説明ペーパー（pptx）は、調査報告の冒頭のリンクからダウンロードできる。ファイル名に版が入る。

## 版

公開物の版は日付で表す。`VERSION` に `YYYY-MM-DD` で書く。同じ日に二度出すときは `.2` のように枝番を付ける。

```bash
make version V=2026-11-01 PY=<python>   # VERSION を書き換え、文書とスライドに反映する
```

版は次の場所に出る。調査報告と前提文書の題名の下、調査報告の冒頭の囲み、スライドの表紙、ダウンロードする pptx のファイル名（`ontology-semantics-intro-<版>.pptx`）。公開した版には、同じ名前の Git のタグ（`v<版>`）を付ける。タグを push すると、GitHub Actions がリリースを作り、その版の調査報告と前提文書の HTML、説明ペーパーの pptx を添える（`.github/workflows/release.yml`）。

版を出す手順は次のとおりである。

```bash
make version V=2026-11-01 PY=<python>   # 版を反映する
# _changelog.qmd の先頭に、その版の行を足す（調査報告の末尾の「改変履歴」になる）
git commit -am "..."                    # コミットする
make release PY=<python>                # タグを付けて push する。リリースは自動で作られる
```

改変履歴にその版の行がないと、`make release` は止まる。

`main` に push すると、GitHub Actions が HTML を作り直して公開する（`.github/workflows/pages.yml`）。

## 状態

- 2026-10-02: 基礎調査の第 1 版を作成。
- 2026-10-02: 全体のファクトチェックを実施し、本文を修正（`fact-check-report.md`）。
- 2026-10-02: 調査報告（`index.qmd`）と前提文書（`method.qmd`）に分割。

- 2026-10-03: 初心者向けの説明ペーパー（`deck/ontology-semantics-intro.pptx`、29 枚）の第 1 版を作成。
- 2026-10-04: 説明ペーパーを、調査報告の構成と図に合わせて作り直した（43 枚、8 部）。
- 2026-10-04: 説明ペーパーを、独自テンプレートへの流し込みに切り替えた。見た目はスライドマスタが決める。pptx-build 2.7.0 以降が要る。
- 2026-10-04: Open Knowledge Format を追加。課題から選ぶ木と四つの問いを追加。説明ペーパーは 48 枚。
- 2026-10-04: 公開リポジトリ `dobachi/ontology-semantics-basics` に移し、GitHub Pages で公開した。

## 構成

| パス | 内容 |
|---|---|
| `index.qmd` | 調査報告（読者向け。作業上の記述を含めない） |
| `_elements.qmd` | 「技術要素の解説」の章。`examples/build_chapter.py` が生成し、`index.qmd` が取り込む。直接編集しない |
| `examples/` | 章に載せたコード例と検証スクリプト（`validate.py`） |
| `figures/el-*.svg` | 技術要素の図（`figures/build_elements.py` が生成） |
| `deck/deck.yaml` | 説明ペーパーの仕様。内容はここを編集する |
| `deck/ontology-semantics-intro.pptx` | 説明ペーパー（`make deck` が生成） |
| `deck/build_figures.py` | スライド用の図を用意する。年表だけは文字を大きくした専用版を描く |
| `scripts/build_deck_link.py` | 説明ペーパーを調査報告の HTML に埋め込むリンク（`_deck_download.qmd`、Git 管理外）を作る。`make assets` と `make deck` が呼ぶ |
| `deck/template/build_template.py` | 説明ペーパーの独自テンプレート `simple.pptx` を作る。見た目（書体、色、位置）はここで決める |
| `deck/template/simple.pptx` | 上のスクリプトの生成物。スライドマスタ 1 つとレイアウト 8 つ。PowerPoint で直接編集してもよい |
| `figures/ext-wikidata-datamodel.png` | Wikimedia Commons の図（CC0）。生成物ではなく、取得した素材 |
| `figures/lineage.svg` | 四本の系譜の年表図（`figures/build_lineage.py` が生成） |
| `method.qmd` | 調査の前提と検証の記録（調査方法、出典の区分、検証結果、節と台帳の対応、pptx の構成案） |
| `_bib/bibliography.bib` | 参考文献（`research/build_bib.py` が生成） |
| `research/plan.md` | 調査計画（7 つの小問） |
| `research/ledger.md` | 出典台帳。出典 133 件、主張 210 件、検証結果、推論の一覧 |
| `fact-check-report.md` | ファクトチェック報告書 |
| `factcheck/` | リンク検査の結果と検証担当ごとの控え |
| `research/build_ledger.py` | 台帳の正。出典と主張はここを編集する |
| `research/status.json` | 盲検検証の判定 |
| `research/raw-sq*.tsv` | 収集担当が返した引用の控え |
| `research/verify-batch-*.md` | 盲検検証に渡した入力 |

## ビルド

```bash
make html      # _output/index.html と _output/method.html
make pdf       # pdf/ に 2 つの PDF（調査報告と前提文書を別々に）
```

## 台帳と参考文献の更新

```bash
python3 research/build_ledger.py   # ledger.md を再生成
python3 research/build_bib.py      # _bib/bibliography.bib を再生成
```

## 執筆上の約束

- 調査報告には、台帳の ID、作業手順、検証の経緯、次の作業の計画を書かない。それらは `method.qmd` に書く。
- 調査報告の事実記述は台帳の主張に対応させる。対応は `method.qmd` の「節と主張の対応」表で管理する。対応する主張がない記述は「考察」に置く。
- 日付は一次情報で確認できたものだけを書く。確認できなかった項目は調査報告の「確認できなかった点と留意事項」に列挙する。

## PDF

```bash
make pdf
```

調査報告と前提文書を、別々の PDF として `pdf/` に出力する。

| ファイル | 内容 |
|---|---|
| `pdf/ontology-semantics-basics.pdf` | 調査報告 |
| `pdf/ontology-semantics-basics-method.pdf` | 調査の前提と検証の記録 |

ソースを作業用ディレクトリ（`.build-pdf/`）に写してビルドするので、プレビューの稼働中でも実行できる。`pdf/` と `.build-pdf/` は Git の管理対象外である。lualatex、Noto CJK フォント、rsvg-convert が必要。

## 説明ペーパー

```bash
make deck PY=<python-pptx の入った python>
```

`deck/deck.yaml` から pptx を作る。生成には pptx-build スキルを使う（場所は `PPTX_BUILD` で指定）。pptx を直接編集すると、次の生成で上書きされる。

## プレビュー

変更監視つきで起動する。

```bash
make preview                    # http://localhost:4455/
make preview HOST=<アドレス>     # 別の端末から見る場合（Tailscale のアドレスなど）
make check-preview              # 配信中の内容が最新かを、地の文で照合する
make preview-fresh              # 古い内容のまま直らないときの復旧
```

`make preview` は、次の三つを quarto preview と同時に動かす（`scripts/preview.sh` と `scripts/watch_assets.py`）。

- **生成物の再生成**: 図のスクリプト（`figures/build_*.py`）と、章の元になる `examples/` を監視し、変わったら作り直す。quarto preview 自身はこれらを監視しない。
- **描画の取りこぼしの回復**: quarto preview は、描画の途中で届いた編集を取りこぼすことがある。出力の時刻は新しいのに中身が古い、という状態になる。監視が出力の中身を調べ、ソースに追いついていなければ描画をやり直させる。

- **描画エラーからの再起動**: quarto の内部キャッシュが壊れると、全ページが「Bad resource ID」のエラーページになる。監視がこれを検知して quarto preview を止め、キャッシュを消して起動し直す。回復には 1 分ほどかかる。

注意点は次のとおり。

- プレビュー稼働中に `make html` や `quarto render` を実行しない。出力先を取り合って失敗する。
- 編集が反映されたかは `make check-preview` で確かめる。タイムスタンプや HTTP 200 では判定できない。
- `_elements.qmd` と `figures/*.svg` は生成物である。直接編集せず、生成元を直す。
