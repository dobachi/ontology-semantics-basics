# ファクトチェック 第 2 ラウンド：1〜5 章（はじめに〜歴史の系譜）

- 実施日: 2026-10-04
- 対象: `index.qmd` の「# はじめに」から「# 歴史の系譜」の末尾まで（`git diff 4ea8e8e -- index.qmd` の追加分が中心）、および図 `el-intro` `el-triangle` `el-triangle-steps` `el-spectrum` `el-why-now` `el-ladder` `el-off-ladder` `el-ladder-streams` `lineage`（SVG のラベル文字列と線の座標を読んだ）
- 方法: 出典の原文を独立に照合した。キャッシュ済みの原文（`ug.pdf`、`mcg.html`、`rfc3444.txt`、`r/om3.txt`、`r/ont_a.html`、`r/gif.txt`、`eif.txt`、`r_03-layers.txt`、`studer.pdf`、`spancache/`）に加え、W3C、Google Patents、Crossref、dbt Labs のページを再取得した
- 判定: Inaccurate / Misleading / Unsupported / Inconsistent / OK-but-note
- 本文、図、台帳は編集していない

## 指摘（重い順）

### F-01 Misleading（中）：Ogden と Richards の三角形の頂点は「概念」ではない

- 場所: 「四つの言葉をひとことで」
  > Ogden と Richards は 1923 年の著書で、記号、概念、対象の三つを三角形の頂点に置いた。
  
  同じ言い方が `figures/el-triangle.svg`（頂点ラベル「概念」）、図の題（「三角形は Ogden と Richards（1923）の図をもとに筆者が作成した」）、@tbl-axes（「記号、概念、対象の三つ」「出どころ Ogden と Richards」）にもある。
- 証拠: 原典の図の頂点は SYMBOL、THOUGHT OR REFERENCE、REFERENT である。
  > "THOUGHT OR REFERENCE … SYMBOL Stands for REFERENT (an imputed relation)"
  
  本文も "Between a thought and a symbol causal relations hold." "Between the Thought and the Referent there is also a relation" と thought で書く。さらに原典は concept という語の使用を批判している。
  > "the use of the term ‘ concept ’ is particularly unfortunate in such an analysis"
  
  出典: https://archive.org/download/bwb_W9-COP-402/bwb_W9-COP-402_djvu.txt
- 補足: 台帳 C-170 が照合しているのは「記号と対象は直接つながらない」だけで、頂点の名前は照合されていない。「概念」は後世の教科書的な読み替えである。
- 修正案: 「記号（Symbol）、思考または指示（Thought or Reference）、指示対象（Referent）の三つを三角形の頂点に置いた。この報告書では、二つ目を『概念』、三つ目を『対象』と読み替える（筆者の読み替え）」。図の題にも「頂点の『概念』は原典の Thought or Reference を筆者が読み替えた」と添える。

### F-02 Misleading（中）：連続体は「機械に何ができるか」に答えない、という記述が原典と合わない

- 場所: 「考察：なぜ独自の軸を加えたのか」
  > 意味の三角形は言葉が何を扱うかを示し、連続体は成果物がどれだけ形式的かを示す。どちらも「機械はそれで何ができるのか」には直接答えない。
  
  関連: @tbl-spectrum-vs-ladder の「並べる基準：意味の指定の量と、形式性の度合い」、「連続体は成果物がどれだけ形式的かを見ており」。
- 証拠: Uschold と Gruninger は、同じ文の中で自動推論への支援も増すと述べている。
  > "As we move along the continuum, the amount of meaning specified and the degree of formality increases (thus reducing ambiguity); there is also increasing support for automated reasoning."
  
  出典: https://sigmodrecord.org/?smd_process_download=1&download_id=5095 （p.59）。図 2 の右端の群の名前も "Formal Ontologies & Inference" である。McGuinness も、スペクトラムの各点で何ができるかを述べている（"Strict subclass hierarchies are necessary for exploitation of inheritance."）。
- 修正案: 「連続体も、進むほど自動推論への支援が増すと述べている [@uschold_gruninger_2004]。ただし並べているのは成果物の種類であり、機械にできることを段として分けてはいない」のように、原典が推論に触れていることを認めたうえで差を述べる。@tbl-spectrum-vs-ladder の「並べる基準」にも「自動推論への支援も増すとされる」を足す。本文で引用した文も後半（自動推論）を省いていることを明示するとよい。

### F-03 Inconsistent（中）：「2 段目から 4 段目の技術は、すべて Web 標準系に属する」が同じ表と矛盾する

- 場所: 「意味の 4 段階と四本の流れの関係」読み取れる点の 1
  > 段を上がるのは Web 標準系である。2 段目から 4 段目の技術は、すべて Web 標準系に属する。
- 証拠（文書内）: 直前の @tbl-ladder-streams は知識表現系を「4 段目」に対応させ、「上位オントロジーは 4 段目で書かれる中身にあたる」とする。直後の点 2 は「4 段目には二つの流れが関わる」と書く。「はじめに」の @tbl-streams も、知識表現系で得られるものを「書かれていないことを、定義から導ける」（4 段目の能力そのもの）とする。年表では BFO（ISO/IEC 21838-2）、Cyc、KL-ONE、記述論理が知識表現系である。
- 修正案: 「@tbl-ladder に挙げた 2 段目から 4 段目の代表的な技術（RDF、SKOS、RDF Schema、OWL）は、いずれも Web 標準系の仕様である」と範囲を限定する。

### F-04 Unsupported（中）：「はじめに」の AI についての記述に出典も考察の明示もない

- 場所: 「何が問題なのか」
  > 最近の AI も、列の名前から同じものだと推測できるかもしれない。ただしそれは推測である。同じデータを渡しても毎回同じ答えになるとは限らず、外れたときにそれと気づく手がかりもない。
  
  「なぜ今これが話題になるのか」
  > AI は文脈から意味を推測できるが、最初の節で見たとおり、その推測は外れることがあり、毎回同じになるとも限らない。だからこそ、意味をあらかじめ定義して AI に渡しておく必要がある。
  
  `el-why-now.svg` にも「推測は外れることがあり、毎回同じとも限らない」とある。
- 証拠: どちらの段落にも引用がない。冒頭の注記は「事実の記述には出典を付けた。筆者の解釈は『考察』と明示した節と段落に分けて書いた」と約束しているが、この章は考察と明示されていない。「最初の節で見たとおり」は、出典のない自分の記述を根拠にしている。「外れたときにそれと気づく手がかりもない」は断定が強い。直前で引いた Databricks の記事が述べるのは「一度定義すれば同じ定義で動く」ことで、AI の推測が不安定だとは述べていない（"Define governed metrics, dimensions, and rules once at the data layer so every dashboard, SQL query, notebook, and AI agent works from the same trusted definitions." https://www.databricks.com/blog/redefining-semantics-data-layer-future-bi-and-ai ）。
- 修正案: 出典を付けるか、「〜と考えられる」「筆者の見方では」と明示する。使える一次情報の例として、Apache Ossie のブログ "When a human analyst or an AI agent runs a query, they shouldn't have to guess which definition is correct."（https://ossie.apache.org/updates/ossie-enters-apache-incubator/ ）がある。これも当事者の説明である旨を添える。「必要がある」は「必要があると考えられる」に改める。

### F-05 Inconsistent（中）：SHACL と XML Schema の扱いが表の間で食い違う

- 場所: @tbl-off-ladder
  > SHACL ｜ 新しい段ではなく、検査という 1 段目と同じ役割を担う（「4 段階には入らない」技術として列挙）
  
  @tbl-ladder-streams
  > 1 段目にあたる検査（XML Schema、SHACL）と、段の外の DCAT も含む
- 証拠（文書内）: 前者は SHACL を「段の外」とし、後者は SHACL を「1 段目にあたる」とし、同じ文で DCAT だけを「段の外」と呼ぶ。XML Schema は @tbl-ladder で 1 段目の代表的な技術そのものである。SHACL が段の中か外かが読み手に決められない。
- 修正案: @tbl-ladder-streams を「1 段目の XML Schema と、段の外にある SHACL（役割は 1 段目と同じ）および DCAT も含む」とする。

### F-06 Inconsistent（中）：Palantir の Ontology と段の関係が、図の題、図の矢印、表で違う

- 場所: @fig-el-off-ladder の題
  > Palantir の Ontology は、2 段目に相当する機能と、3 段目の一部にあたる機能を持つ。
- 証拠（文書内）: 同じ図の箱のラベルは「独自の形式で 1、2 段目に相当。3 段目は一部」、@tbl-off-ladder は「1、2 段目に相当する機能を持つ」、@tbl-palantir-ladder は 1 段目を「備える」とする。一方 `el-off-ladder.svg` の Palantir の箱から出る矢印は 2 本だけで、2 段目（ラベル「相当」）と 3 段目（ラベル「一部」）を指し、1 段目への矢印はない。
- 修正案: 題を「1、2 段目に相当する機能と、3 段目の一部にあたる機能を持つ」に直し、図に 1 段目への矢印を足す。足さないなら、題で「矢印は 2 段目と 3 段目だけを描いた」と断る。

### F-07 Misleading（中）：年表の図の「KL-ONE 1985」は、KL-ONE が Cyc 着手より後に見える

- 場所: `figures/lineage.svg` の知識表現系「Cyc 着手 1984」「KL-ONE 1985」。本文「年は @tbl-timeline の出典による」。
- 証拠: 1985 年は概説論文の掲載年であり、KL-ONE の成立年ではない。同論文の要旨は次のとおり。
  > "KL‐ONE is a system for representing knowledge in Artificial Intelligence programs. It has been developed and refined over a long period and has been used in both basic research and implemented knowledge‐based systems in a number of places in the AI community."
  
  出典: Brachman & Schmolze 1985、https://doi.org/10.1207/s15516709cog0902_1 （Crossref の要旨、発行 1985 年 4 月）。@tbl-timeline は「KL-ONE の概説論文が…掲載」と正しく書いているが、図のラベルにはその限定がない。
- 修正案: 図のラベルを「KL-ONE の概説論文 1985」にする。題か本文に「図の年は出典の発行年であり、技術の成立年ではないものがある」と添える。

### F-08 Inconsistent / Misleading（低〜中）：3 段目（SKOS）を「オントロジー」に対応させる表と、ほかの記述、SKOS の仕様

- 場所: @tbl-triangle-steps「3 段目 ｜ … ｜ オントロジー」。一方「考察：意味の 4 段階」
  > 知識工学と Web 標準の用法は 4 段目にあたる。
- 証拠（文書内）: オントロジーという語が、ある表では 3 段目と 4 段目、本文では 4 段目だけに対応する。@tbl-spectrum-vs-ladder の周辺では 3 段目を「シソーラスにあたる」としている。
- 証拠（出典）: SKOS Reference は、シソーラスと形式的なオントロジーを別物としている。
  > "SKOS is not a formal knowledge representation language. … A thesaurus or classification scheme is of a completely different nature, and does not assert any axioms or facts."
  
  出典: https://www.w3.org/TR/2009/REC-skos-reference-20090818/ 。@tbl-ladder の 3 段目の例「ボルトは締結部品の一種だと分かる」も、SKOS の広い狭いの関係を「一種」（クラスの包含）として読ませるおそれがある。
- 修正案: @tbl-triangle-steps の 3 段目を「統制語彙、シソーラス（広い意味ではオントロジーと呼ばれることもある）」とする。例は「ボルトは締結部品より狭い語だとたどれる」にする。W3C の「明確な区分はない」という説明 [@w3c_ontologies_page] を参照させるとよい。

### F-09 Inconsistent（低）：`el-why-now.svg` の B 社の列名が本文と違う

- 場所: `figures/el-why-now.svg`「B 社 vendor_code」
- 証拠（文書内）: 本文は「A 社は `supplier_id`、B 社は『仕入先コード』、C 社は `vendor`」、`el-intro.svg` も B 社は「仕入先コード」である。`vendor_code` は本文に出てこない。
- 修正案: 図の B 社を「仕入先コード」にそろえる。

### F-10 Inconsistent（低）：「四つの言葉」は題名にある言葉ではない

- 場所: 「四つの言葉をひとことで」
  > この報告書の題名にある言葉を、まず大づかみに押さえておく。
- 証拠（文書内）: 題名は「オントロジー・セマンティクス・データモデル標準化の基礎調査」で、言葉は三つである。冒頭の注記とエグゼクティブサマリも三語で書く。節が説明するのは、データモデル、セマンティクス、オントロジー、データモデル標準化の四つである。@tbl-axes の三角形の行は三つ（データモデル、セマンティクス、オントロジー）しか挙げない。
- 修正案: 「題名にある三つの言葉と、その前提になる『データモデル』を」とする。

### F-11 Misleading（低）：「共有」と「形式的」を加えたのは Studer らだ、と読める

- 場所: エグゼクティブサマリ 発見 1
  > Studer らがこれに「共有」と「形式的」を加えて改めた [@studer_1998]。
- 証拠: Studer らは、自分たちの定義を Gruber（1993）と Borst（1997）の定義にもとづくと書いている。
  > "one that characterises best, in our opinion, the essence of an ontology is based on the related definitions in ([74], [22]): An ontology is a formal, explicit specification of a shared conceptualisation."
  
  [74] は Gruber 1993、[22] は "W. N. Borst, Construction of Engineering Ontologies, PhD Thesis, University of Twente, 1997" である。出典: https://publikationen.bibliothek.kit.edu/189497/3003 。「用語の整理」の「先行する定義を踏まえたものである」とも温度差がある。4ea8e8e の時点の文（「…とした」）にはこの含みがなかった。
- 修正案: 「Studer らは、Gruber と Borst の定義を踏まえて『共有された概念化の、形式的で明示的な仕様』とした」。

### F-12 Unsupported（低）：「セマンティック」の語の指すものの違いを、事実として書いている

- 場所: 「歴史は四本の流れに分けると見通しがよい」
  > 同じ「セマンティック」という言葉も、Web 標準系では組織をまたぐ意味の共有を、分析系では指標の計算方法の統一を指す。
- 証拠（文書内）: 引用がない。エグゼクティブサマリでは同じ内容が「考察にもとづく示唆」に置かれ、「考えられる」と書かれている。
- 修正案: 「…を指すことが多いと考えられる（@sec-compare）」とする。

### F-13 Inconsistent（低）：階段の図と「1 段目は独立」という本文

- 場所: @fig-el-ladder の題「段を上がるごとに、機械が意味についてできることが増える」、図内「機械に渡す意味が増える」。本文
  > 2 段目から 4 段目は積み上がる。… 1 段目の検査は、これらとは独立している。
- 証拠（文書内）: 図は 1 段目を土台にした一続きの階段で、本文は 1 段目を別系統とする。@fig-el-triangle-steps の題「段を上がるとは、記号の側だけを決めていた状態から…進むこと」も 1 段目を出発点とする。
- 修正案: @fig-el-ladder の題に「1 段目は 2 段目以上の前提ではない。並べる順は、機械に渡す意味の量による」と添える。

## OK-but-note

| 番号 | 場所 | 内容 |
|---|---|---|
| N-01 | 「語彙とオントロジー」 | 原文は "more complex, and possibly quite formal collection of terms"。「複雑で形式的なもの」は possibly を落としている。「複雑で、場合によってはかなり形式的なもの」が近い |
| N-02 | `el-spectrum.svg` | 四つの群の名前は原典の図 2 と合う（Glossaries & Data dictionaries / Thesauri, Taxonomies / MetaData, XML Schemas, & Data Models / Formal Ontologies & Inference）。ただし「広い語と狭い語」「言い換え」「自然言語による説明」は原典の図にない筆者の説明。4 つ目の群は原典では "& Inference" が付く。原典は "Description Logics (OWL-DL)"。原典では XML DTDs が Principled, informal hierarchies より左にあり、群は一部で入り組む |
| N-03 | @tbl-axes「用語集からオントロジーまで」 | 原典は全体を "a kind of continuum of kinds of ontologies" と呼ぶ（用語だけのものも広い意味のオントロジー）。脚注 4 で狭い意味に限ると断っている。「意味の指定の強さによる連続体」という名前は筆者の命名 |
| N-04 | `ogden_richards_1923` | 照合した Internet Archive の本は第 8 版以降の再刊（Harcourt, Brace & World。同社名は 1960 年以降）。1923 年初版そのものではない。bib の publisher と year の組み合わせに注意書きがほしい |
| N-05 | `el-triangle.svg` の辺 | 「表す」「指す」は原典の Symbolises、Refers to に対応する。底辺の「直接にはつながらない」は原典の図では "Stands for (an imputed relation)" |
| N-06 | RFC 3444 | 要約は原文と合う。RFC 3444 は Informational で、ネットワーク管理の文脈（"model managed objects at a conceptual level"）の文書である |
| N-07 | 年表「2012 年 12 月 11 日 OWL 2 第 2 版」 | 日付は正しい。OWL 2 の最初の勧告は 2009 年 10 月 27 日（同文書 "since the Recommendation of 27 October 2009"）。OWL 2 が 2012 年に始まったと読まれないよう一言ほしい |
| N-08 | 年表の並び | IEC 63278-1:2023（bib では 12 月）が「2023 年 11 月」の Power BI の行より前にある |
| N-09 | エグゼクティブサマリ 示唆 1 | 4ea8e8e では「考えられる」付きだった。現行は「整理しやすい」と言い切り。見出しが「考察にもとづく示唆」なので許容範囲 |
| N-10 | 「データモデル標準化」 | 「そろえるのは、まずデータの形である [@digital_agency_gif_outline_2025; @iec_63278_1_2023]」。二つの出典はデータモデルと AAS の構造を定義するが、「まず形」という順序づけは筆者の解釈 |

## 確認して正しかったもの

| 項目 | 照合結果 |
|---|---|
| O&R「記号と対象は直接にはつながらない」 | "Symbol and Referent, that is to say, are not connected directly" |
| U&G の連続体の要約、四つの群、シソーラスがスキーマより手前 | 本文 p.59 と図 2 で確認 |
| McGuinness「オントロジー・スペクトラム」 | "Figure 2: An Ontology Spectrum"。脚注に AAAI '99 のパネル（Gruninger、Uschold ら）由来とある |
| RFC 3444 の三点 | "at a conceptual level, independent of any specific implementations or protocols" / "lower level of abstraction and include many details" / "multiple DMs can be derived from a single IM" |
| W3C「明確な区分はない」 | "There is no clear division between what is referred to as “vocabularies” and “ontologies”." |
| Snowflake OSI（2025-09-23、狙い） | "September 23, 2025" / "ensuring consistent business logic across AI and business intelligence (BI) applications" |
| Databricks（2026-04-02、一度定義） | "Define governed metrics, dimensions, and rules once at the data layer so every dashboard, SQL query, notebook, and AI agent works from the same trusted definitions." |
| GIF のデータモデルの説明 | 「データの構造や項目などに加え、データとデータの関係性を定義したもの。」 |
| EIF の 4 層、意味的相互運用性の定義 | "four layers of interoperability: legal, organisational, semantic and technical" ほか |
| ODS-RAM の 4 レイヤ、意味に関するメタデータ、OWA | GitBook 3. レイヤの本文で確認 |
| IPA ガイドの対応づけ（マッピング） | 「共通フォーマットに変換（マッピングと呼ぶ）する仕組み」 |
| OWL 2004「内容を処理」「記述論理が形式的な基礎」 | "process the content of information" / "the logics that form the formal foundation of OWL" |
| OWL 2「形式的に定義された意味」 | "an ontology language for the Semantic Web with formally defined meaning" |
| Ossie「両方のためのオープン仕様」、2026-07-10 | "Ossie is an open specification for both semantic layer and ontology." |
| Ossie インキュベーション開始 2026-06-22 | "2026-06-22 Project enters incubation." |
| Business Objects の特許（1991 年出願、優先日 11 月 27 日、要点） | Google Patents: priorityDate と filingDate が 1991-11-27、公開 1996-09-10。要旨 "without knowing the relational structure or the structure query language (SQL)" |
| KL-ONE 概説論文 1985 年 4 月 | Crossref の発行年月 |
| dbt Labs MetricFlow 2025-10-14 | datePublished 2025-10-14、"PHILADELPHIA, October 14, 2025" |
| Eclipse 2025-12-02 | "BRUSSELS – 2 December 2025" |
| OSI 仕様 2026-01-27、Apache 2 | "Jan 27, 2026" / "available via an Apache 2 licensed Git repository" |
| RDF 1.2 勧告候補 2026-04-07 | "Candidate Recommendation Snapshot 07 April 2026"（2026-10-04 に再取得） |
| 年表と `lineage.svg` の年の一致 | 図の 19 件すべてが年表の年と一致 |
| `el-ladder` `el-ladder-streams` `el-triangle-steps` と @tbl-ladder、@tbl-triangle-steps の段の名前と番号 | 一致。`el-ladder-streams` の色は 1 段目がデータベース系、2〜4 段目が Web 標準系で表と合う |
| `el-off-ladder` の DCAT、SHACL、セマンティックレイヤの矢印 | それぞれ 2 段目、1 段目、1 段目を指し、表と合う |
| 「五つの軸」「先行する二つの軸」「四本の流れ」などの数 | 表の行数と一致（F-10 を除く） |

## 確認できなかったもの

- 年表のうち今回再取得しなかった行（Codd 1970 年 6 月、Chen 1976 年 3 月、Lenat 1984 年、Gruber 1993 年、RDF 1999-02-22、Gene Ontology 2000 年 5 月、Scientific American 2001 年 5 月、XML Schema 2001-05-02、OWL 2004-02-10、SPARQL 2008-01-15、SKOS 2009-08-18、schema.org 2011-06-02、ナレッジグラフ 2012-05-16、DCAT と JSON-LD 2014-01-16、RDF 1.1 2014-02-25、SHACL 2017-07-20、JSON-LD 1.1 2020-07-16、ISO/IEC 21838-2:2021、IEC 63278-1:2023、Power BI 2023 年 11 月、GraphRAG 2024-02-13、ISO/IEC 39075:2024、DCAT 3 2024-08-22）。いずれも 4ea8e8e より前からある行で、URL に含まれる日付や台帳の記録と矛盾はなかったが、今回は原文で独立に再照合していない。
- 「4 段目にあたる推論は、公式文書に見当たらない」（Palantir）。不在の主張であり、公式文書の全体は調べていない。
- Ogden と Richards の 1923 年初版そのものの図（照合したのは後の版の OCR テキスト。図の辺のラベルは OCR が一部欠けている）。
- 「日本の ODS のオープンソース実装も、この用法で『ODS オントロジー』を定義している」「設計思想として開世界仮説を前提に置き、オープンソース実装は OWL で書いたオントロジーと SAMM を使う」。根拠は対象範囲外の @sec-ds-jp にあり、今回は原文を照合していない（ODS-RAM の L4 が OWA を採用することだけ確認した）。
