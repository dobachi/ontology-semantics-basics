# ファクトチェック 第 2 ラウンド：6〜9 章（技術要素の解説〜米国企業の近年の取り組み）

- 実施日: 2026-10-04
- 対象: `_elements.qmd`（6 章の全体と `examples/` の例）、`index.qmd` の「# データモデルとメタデータの標準化」「# ドメインオントロジーと業界標準」「# 米国企業の近年の取り組み」（`git diff 4ea8e8e -- index.qmd _elements.qmd` の追加分が中心）。図は `el-palantir` `el-two-streams` `el-domain-map` `ext-wikidata-datamodel.png`（画像を目視）と、6 章が使う `el-*.svg` 19 枚（SVG の文字列と線の座標を読んだ）。作業中に追加された図 `el-datamodel-map.svg` `el-ossie-timeline.svg`（7 章と 9 章が埋め込む）も読んだ
- 方法: 出典の URL を独立に再取得し（58 件、すべて HTTP 200）、原文と照合した。Palantir は、サイトマップから Ontology 関連の公式文書 184 ページを取得して全文検索した。`examples/validate.py` を、最新の `ossie-schema.json`（apache/ossie main と一致）を渡して実行した
- 判定: Inaccurate / Misleading / Unsupported / Inconsistent / OK-but-note
- 本文、図、例、台帳は編集していない。`quarto` と `make` は実行していない

## 指摘（重い順）

### F-01 Inconsistent（中）：Ossie が近づく相手について、コラムと図と考察が食い違う

- 場所 A: 「Open Semantic Interchange から Apache Ossie へ」の考察
  > ただし、ロードマップが先例として挙げるのは Palantir のような製品のオントロジーであり、RDF や OWL ではない。近づいている相手は、知識表現系や Web 標準系というより、製品としてのオントロジーだと考えられる。
- 場所 B: コラム「分析系はなぜ別の流れとして現れたのか」の「いまは近づいている」
  > Apache Ossie のオントロジー仕様は、概念や関係を、既存の RDF や OWL の語彙の定義に関連づけられるようにしている [@ossie_ontology_spec]。
  
  `figures/el-two-streams.svg` も、分析系と Web 標準系の間に「オントロジー仕様が RDF、OWL の語彙に関連づく」と書き、図の題は「近年になって両者が近づいている」とする。
- 証拠: どちらの事実も原文にある。ロードマップは Palantir と Legend だけを挙げる。
  > "Many semantic representations (e.g., Palantir, Goldman Sachs Legend) use ontologies to define meaning"
  
  https://raw.githubusercontent.com/apache/ossie/main/ROADMAP.md
  
  一方、オントロジー仕様は RDF と OWL を名指ししている。
  > "To relate a concept or relationship to a definition outside the ontology, for instance a class or property in an existing RDF or OWL vocabulary, it can carry an optional `iri` field that holds a globally unique identifier."
  
  https://raw.githubusercontent.com/apache/ossie/main/ontology/ontology.md
- 問題: 場所 A は、報告書自身が場所 B で引いている事実（`iri` による RDF、OWL の語彙への関連づけ）に触れずに、「相手は Web 標準系ではない」と結論している。同じ章の中で結論が逆を向く。
- 修正案: 場所 A を「ロードマップが先例として挙げるのは Palantir のような製品のオントロジーである。一方、オントロジー仕様は `iri` 項目で、概念や関係を既存の RDF や OWL の語彙に関連づけられるようにしている [@ossie_ontology_spec]。書式は独自の YAML で、製品のオントロジーに近い。識別子の面では Web 標準系にもつながる、と考えられる」のように、両方を並べる。

### F-02 Inconsistent（中）：調達品の定義が、OWL の例と、図・コメント・表で違う

- 場所: 6 章「OWL」の具体例のコメント
  > `# 「供給者が 1 つ以上ある製品」を「調達品」と定義する`
  
  6 章「KL-ONE と記述論理」
  > OWL の項に、同じ定義を OWL で書いた例がある。
  
  `figures/el-dl.svg` は「調達品 ＝ 製品であり、供給者を 1 つ以上持つもの」「P-100 は製品である」と書く。@tbl-ladder の 4 段目も「供給者を持つ製品は調達品だと…導ける」。
- 証拠: `examples/owl.ttl`（本文の例と同一）の定義に「製品」は出てこない。
  ```turtle
  ex:ProcuredItem  a owl:Class ;
      owl:equivalentClass [
          a owl:Restriction ;
          owl:onProperty      ex:suppliedBy ;
          owl:someValuesFrom  ex:Supplier
      ] .
  ```
  これは「`ex:suppliedBy` の値に Supplier を 1 つ以上持つもの」であり、製品に限らない。`figures/el-rdfs-owl.svg` は「ex:ProcuredItem ＝ ex:suppliedBy の値に Supplier を 1 つ以上持つもの（OWL）」と、コードどおりに書いている。つまり、コードと `el-rdfs-owl` は「製品」なし、コメントと `el-dl` と @tbl-ladder は「製品」ありである。「同じ定義」ではない。
- 修正案（どちらか）:
  1. 例を図に合わせる。
     ```turtle
     ex:ProcuredItem  a owl:Class ;
         owl:equivalentClass [
             a owl:Class ;
             owl:intersectionOf ( ex:Product
                 [ a owl:Restriction ;
                   owl:onProperty      ex:suppliedBy ;
                   owl:someValuesFrom  ex:Supplier ] )
         ] .
     ```
     このとき P-100 が製品であることは、RDF Schema の例の `ex:Part rdfs:subClassOf ex:Product` から導かれる、と一文添える。`el-rdfs-owl.svg` の文言も「製品であり、…」に直す。
  2. 文言をコードに合わせる。コメントを「供給者が 1 つ以上あるものを調達品と定義する」、`el-dl.svg` を「調達品 ＝ 供給者を 1 つ以上持つもの」に直し、「P-100 は製品である」の行を外す。

### F-03 Unsupported（中）：「課題は一貫して、指標の定義をそろえること」は 1991 年の特許からは言えない

- 場所: コラムの見出しと `figures/el-two-streams.svg` の帯
  > **課題は一貫して、指標の定義をそろえることだった**
  
  図では、この帯が「1991 年 Business Objects の特許」から「2026 年 Apache Ossie」までを覆う。関連: 「分析系のセマンティックレイヤは、RDF より前に始まっている。Business Objects の特許は…」
- 証拠: 特許が掲げる課題は、利用者が業務の言葉で問い合わせられることであり、指標の定義の統一ではない。
  > "allows information system end users to access (query) relational databases without knowing the relational structure or the structure query language (SQL)"
  
  > "Instead of presenting a user with data organized in a computer-oriented way (columns, rows, tables, joins), the user sees information through terms that he is familiar with in his daily business."
  
  https://patents.google.com/patent/US5555403A/en
  
  また、特許の本文と請求項に "semantic layer" という語はない。使われるのは "semantically dynamic objects" "business objects" "universe" である。ページ内の "semantic layer" 5 か所は、すべて後年の引用特許の題名である（例: "Deduction of analytic context based on text and semantic layer", 2008 年）。
- 問題: 「指標の定義をそろえる」を裏づける出典は 2021 年以降の 4 件（Stancil、dbt Labs、OSI 発表文、Ossie README）だけである。1991 年まで「一貫して」と言う根拠がない。この特許をセマンティックレイヤの起点とみなす点も、出典の言葉ではなく筆者の位置づけである。
- 修正案: 見出しと図の帯を「2021 年以降の課題は、指標の定義をそろえること」に狭める。1991 年については「課題は、利用者が表の構造や SQL を知らなくても、業務の言葉で問い合わせられることだった」と書き分ける。「分析系のセマンティックレイヤは、RDF より前に始まっている」は「のちにセマンティックレイヤと呼ばれる仕組みの原型は、RDF より前にある（筆者の位置づけ。特許自体はこの語を使っていない）」とする。

### F-04 Unsupported（低〜中）：「主キーは一意でなければならない」が、引用した 2 ページにない

- 場所: @tbl-palantir-ladder の 1 段目
  > 必須プロパティは、値を持たなければならないプロパティである。値型は、検証の制約を伴う。主キーは一意でなければならない … [@palantir_required_properties; @palantir_value_types]
- 証拠: 引用された 2 ページ（required-properties、value-types-overview）には "primary key" も "unique" も出てこない（全文検索で 0 件）。記述そのものは別のページにある。
  > "The primary key is the property that acts as a unique identifier for each instance of an object type, meaning that each row in the backing datasources must have a different value for this property."
  
  https://www.palantir.com/docs/foundry/object-link-types/property-metadata/
- 補足: 台帳にも、この文に対応する主張の行がない（C-127、C-128 は必須プロパティと値型のみ）。
- 修正案: 上の URL を文献に加えて引用する。台帳にも行を足す。

### F-05 Misleading（低〜中）：SNOMED CT を「用語、製品データ」の段だけに置くと、出典の自己記述と合わない

- 場所: `figures/el-domain-map.svg`。行の説明は「オントロジー：概念と関係を定義」「用語、製品データ：言葉や項目をそろえる」。SNOMED CT は後者にだけ置かれている。
- 証拠: 引用されている同じページが、概念と関係による論理的な定義を述べている。
  > "The core component types in SNOMED CT are concepts, descriptions and relationships."
  
  > "Relationships are used to logically define the meaning of a concept in a way that can be processed by a computer."
  
  https://www.snomed.org/what-is-snomed-ct
  
  同じページは "the most comprehensive, multilingual clinical healthcare terminology in the world" とも言うので、「用語」は誤りではない。ただし図の 1 行目の基準（概念と関係を定義）にも当てはまる。
- ほかの配置の確認結果:
  - ECLASS（用語、製品データ）: 妥当。"With ECLASS, product master data can be exchanged digitally across all borders" https://eclass.eu/en/eclass-standard/introduction
  - AAS（交換の仕様）: 妥当。"The purpose of the Asset Administration Shell is to enable two or more software applications to exchange information" https://webstore.iec.ch/en/publication/65628
  - HL7 FHIR（交換の仕様）: 妥当。"FHIR is a standard for health care data exchange" https://hl7.org/fhir/
  - CFIHOS（交換の仕様）: おおむね妥当。ただし標準は用語の資産も含む。"Specifications, Guidelines, Reference Data Library and supporting templates that comprise CFIHOS standard v2.0" https://www.jip36-cfihos.org/
  - NIEM（交換の仕様）: おおむね妥当。ただし中身はデータモデルを含む。"The framework includes a reference data model for objects, properties, and relationships; and a set of technical specifications for using and extending the data model in information exchanges." https://niemopen.org/news/niem-a-new-open-project-18-years-in-the-making/
  - FIBO、Gene Ontology、OBO Foundry、IOF（オントロジー）: 妥当。
- 修正案: SNOMED CT の箱を 1 行目と 2 行目にまたがらせるか、図の注に「SNOMED CT は概念と関係による定義も持つ。CFIHOS と NIEM は参照データやデータモデルも含む」と添える。本文には「境目もはっきりしたものではない」とあるので、例を一つ挙げるだけでも足りる。

### F-06 Misleading（低）：「改称後のブログ記事の説明に ontology が加わった」

- 場所: 「Open Semantic Interchange から Apache Ossie へ」の考察
  > 改称後のブログ記事の説明に「ontology」が加わったことは、分析系が意味の定義へ範囲を広げている兆候と考えられる。
- 証拠: オントロジーは改称より前から活動の範囲にある。2026 年 4 月の更新は、作業部会の一つに挙げている。
  > "Ontology Representation — Modeling relationships, hierarchies, and domain knowledge"
  
  https://ossie.apache.org/updates/osi-april-2026-community-update/
  
  7 月の記事自身も、変わったのは名前だけだと述べている。
  > "If you've been following the Open Semantic Interchange project — the open specification for semantic layer and ontology — there's an important update." "The spec, the community, and the mission haven't changed"
  
  https://ossie.apache.org/updates/ossie-enters-apache-incubator/
- 修正案: 「2026 年 1 月の告知は対象をデータセット、指標、ディメンション、関係、文脈としていた [@snowflake_osi_spec_2026]。4 月の更新にはオントロジー表現の作業部会があり [@ossie_update_2026_04]、7 月の記事は仕様の説明そのものに ontology を入れた。範囲が広がっている兆候と考えられる」。`el-ossie-timeline.svg` は「説明は出どころによって違う」としており、こちらは正確である。

### F-07 Inconsistent（低）：7 章の図 `el-datamodel-map.svg` の段の割り当てが、4 章と 6 章の記述と合わない

- 場所: `figures/el-datamodel-map.svg`（@fig-el-datamodel-map、4ea8e8e より後に追加）。左の列「形をそろえる」に「意味の 4 段階の 1 段目」、右の列「言葉をそろえる」に「意味の 4 段階の 2 段目」と書く。
- 証拠（報告書の中の記述）:
  - @tbl-off-ladder は「DCAT、ダブリンコア」を「4 段階に入らない」技術とし、2 段目は「関係する段」としている。図は、ダブリンコアを 2 段目そのものに置く。
  - 1 段目は @tbl-ladder で「形を検査できる」である。図の左の列には実体関連モデルがあるが、6 章は「図は人が読むためのものである。図そのものを機械が解釈して推論することは想定していない」と書く。機械が検査する段に置くのと合わない。MOF も、@tbl-ladder の代表的な技術に入っていない。
- 修正案: 列の添え書きを「1 段目に関係する」「2 段目に関係する」にゆるめる。または実体関連モデルと MOF を「設計の段階」として 1 段目の外に分ける。

## 注記（OK-but-note）

| # | 場所 | 注記 | 証拠 |
|---|---|---|---|
| N-1 | @tbl-palantir-ladder 4 段目「派生プロパティは…実行時に計算される」 | 派生プロパティはベータ版である。表に「ベータ版」と添えるとよい | "Derived properties are in the beta phase of development and may not be available on your enrollment." https://www.palantir.com/docs/foundry/ontology/derived-properties/ |
| N-2 | 「Business Objects の特許は 1991 年を優先日とし」 | 日付は合う（優先日、出願日とも 1991-11-27、公開 1996-09-10）。ただし Google Patents は優先日を推定と断っている。米国出願日が同じ日なので「1991 年 11 月 27 日に出願」と書くほうが堅い | "The priority date is an assumption and is not a legal conclusion." https://patents.google.com/patent/US5555403A/en |
| N-3 | 7 章「共通語彙基盤 [@imi_ipa]」 | サイトが URL の廃止を予告している。代替 URL を文献の note に控えるとよい | 「IMIのドメイン移行と現URLの廃止についてを公開しました。 2025年12月11日」 https://imi.go.jp/ |
| N-4 | 6 章 SKOS の例 `skos:altLabel "ねじ"@ja`（ボルト） | SKOS としては正しく通る。ただし「ねじ」はボルトの言い換えではなく、より広い語である。言い換えの例なら「六角ボルト」に対する「六角頭ボルト」などが無難 | 例の題材の問題で、仕様上の誤りではない |
| N-5 | @tbl-osi「2026-01-27 仕様の最初の版を…公開」 | 日付は記事の表示どおり（"Jan 27, 2026"。メタデータの datePublished は 2026-01-28T22:22Z）。7 月の記事は、リポジトリの公開を 2025 年 11 月としている。矛盾ではないが、「最初の版の公開」と「リポジトリの公開」は別の時点である | "Since the repository opened in November 2025" https://ossie.apache.org/updates/ossie-enters-apache-incubator/ |
| N-6 | `figures/el-upper-ontology.svg`「下の層は上の層の用語を特殊化して使う」「例: 金融、生命科学、製造」 | 本文の「すべての領域オントロジーが、特定の上位オントロジーにもとづいて作られているわけではない」と並べると、図だけ読む人には FIBO なども BFO の下にあると読める。図の注に同じ断りを入れるとよい | 報告書の本文との比較 |
| N-7 | 「2021 年には…一か所で決めるという考え方が提唱された」 | 記事の日付は 2021-04-22 で合う。記事の追記によれば、Airbnb は同じ時期に社内の指標レイヤ Minerva を公表している。「提唱」は Stancil の発明という意味ではない | "Shortly after this post came out, Airbnb published an article about Minerva, their internal metrics layer." https://benn.substack.com/p/metrics-layer |
| N-8 | 6 章「リポジトリには…オントロジーの仕様もある」 | 事実（`ontology/ontology.md` は main にあり、版は 0.2.0.dev0）。ただし README の「What's in this repository」は `ontology/` を挙げていない | https://raw.githubusercontent.com/apache/ossie/main/README.md |

## 確認して正しかったもの

| 対象 | 確認した内容 | 結果 |
|---|---|---|
| `el-palantir.svg` と本文 | 公式の図（airline-ontology.png）と照合。5 つのオブジェクト型、7 本のリンクの名前と向き（Flight→Airport の Departed From / Arrived To、Flight→Delay、Flight→Airline の Operated By、Flight→Aircraft の Flown By、Airport→Airline の Hub For、Aircraft→Airline の Owned By）、プロパティの例、オブジェクトの例 | すべて一致 |
| Palantir の引用と表 | 定義の引用文、semantic / kinetic elements、必須プロパティ、値型、MDO と主キーによる結合、インターフェースの拡張と継承、派生プロパティ、関数の言語、型リファレンスの RDF・OWL・XSD、JSON の書き出しと注意書き、共有プロパティ、「not a "semantic layer"」 | 原文どおり（F-04、N-1 を除く） |
| 「RDF と OWL に触れるのはこの一文だけ」「推論の記述は見当たらない」 | 184 ページを全文検索（RDF、OWL、SPARQL、SKOS、SHACL、inference、reasoner、entail、subclass、taxonomy など） | 該当は型リファレンスの一文だけ。inference は機械学習モデルの文脈のみ。記述と合う |
| Wikidata の図 | 作者 Charlie Kritschmar (WMDE)、2016-06-21、CC0 1.0。日本語のラベルは原ファイルに含まれる翻訳。本文の説明（修飾子、情報源） | 一致 |
| 7 章 | Codd 1970、Chen 1976、MOF の説明、XML Schema 2001-05-02、JSON Schema の説明、ダブリンコアの由来、ISO 15836 の 2003 年と 2017 年、schema.org の 2011-06-02 と創設企業、共通語彙基盤 | 一致 |
| @tbl-domain | 12 行の自己記述、CCO の「eleven ontologies」（develop の README、列挙も 11 件）、ISO/IEC 21838-2:2021、IEC 63278-1:2023 | 一致 |
| 知識グラフ | Google 2012-05-16 と「things, not strings」、Wikidata の自己記述、ISO/IEC 39075:2024、Neo4j の説明と日付、GraphRAG 2024-02-13 | 一致 |
| 分析系 | Looker、Power BI の改称と 2023 年 11 月、Databricks 2026-04-02、dbt MetricFlow の Apache 2.0、AtScale の説明 | 一致 |
| コラム | Stancil（2021-04-22、"centralized clearing house"）、dbt Labs の説明、OSI 発表文の "consistent business logic"、README の KPI の記述、Hogan の批判と SQL:2016 の反論（Semantic Web 11(1), 2020）、Anadiotis（2024-07-08） | 一致 |
| @tbl-osi と引用 | 2025-09-23、2026-01-27、2026-04-28（Oracle、Cloudera、Dremio）、2026-06-22、2026-07-10、ブログ記事の引用文、Incubator のステータスページの説明、ロードマップの記述 | 一致 |
| `el-two-streams.svg` | 年（1999、2004、2009、2017、1991、2021、2025、2026） | @tbl-timeline と一致 |
| 6 章の W3C の表 | 8 標準の勧告日 | 一致 |
| 6 章の例 | `validate.py` で関係モデル、指標の SQL、Turtle 7 本、JSON-LD（部品の 4 つの文と一致）、SPARQL、SHACL（適合と違反 2 件）、JSON Schema、Ossie の YAML（最新のスキーマに適合）。本文の例は `examples/` と同一 | すべて OK |
| 6 章の技術的な説明 | RDF、RDF Schema（domain と range は推論）、OWL（開世界、欠けたデータを誤りとしない）、SKOS、SHACL、SPARQL、JSON-LD（小数は xsd:double、Turtle の小数は xsd:decimal）、DCAT、JSON Schema、GQL（`//` のコメント、INSERT、MATCH は規格の構文にある）、記述論理 | 誤りなし（F-02 を除く） |
| 6 章の図 19 枚 | ラベルと本文、例との対応 | 一致（F-02 の `el-dl`、N-6 を除く） |

## 確認できなかったもの

- ISO/IEC 39075:2024、ISO/IEC 21838-2:2021、IEC 63278-1:2023 の規格本文。販売ページの概要だけを見た。
- GQL の例の実行。処理系がなく、構文は知識にもとづいて読んだだけである（報告書も未検証と明記している）。
- Codd、Chen、Brachman、Lenat、Guarino、Ashburner の論文と、Hogan らの「Knowledge Graphs」の原文。今回は再取得していない。書誌と年は既知の情報と合う。
- 6 章の「使われている場所」のうち、4ea8e8e より前からある記述（Gaia-X、IDS、ODS、DSSC、データスペースプロトコル）。台帳の照合結果を見ただけで、再取得していない。SAMM の SHACL だけはキャッシュで確認した。
- Palantir の「およそ 180 ページ」という数。筆者がどのページを検索したかは分からない。こちらで取得できた 184 ページでは、結論は同じだった。
- Anadiotis の記事の観察が、筆者自身のものか、取材相手（Cube の Keydunov）の発言の要約か。地の文にあるが、前後は発言の紹介である。
