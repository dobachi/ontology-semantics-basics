# ファクトチェック 第 2 回：データスペースとの接点、体系化の試み、確認できなかった点、用語集、method.qmd

- 実施日: 2026-10-04
- 対象: `index.qmd` の「データスペースとの接点」「考察：体系化の試み」「確認できなかった点と留意事項」「付録 A：用語集」、`method.qmd`、図 `el-dsp-norm.svg` `el-dsp-ods.svg` `el-eif.svg` `el-ods-oss.svg` `el-map.svg`
- 方法: `git diff 4ea8e8e` で追加分を特定し、出典の URL を 2026-10-04 に取得し直して原文と突き合わせた。台帳や本文の記述は根拠にしていない。GitHub は raw ファイル、API、コード検索を使った。IPA の PDF は左右の段を分けて抽出して読んだ。
- 判定の区分: Inaccurate（不正確）/ Misleading（誤解を招く）/ Unsupported（出典が支えていない）/ Inconsistent（文書内で食い違う）/ OK-but-note（正しいが注記を勧める）

## 指摘

### F-1 データスペースプロトコル 2024-1 の「規範」 — Misleading

- 場所: 「データスペースプロトコルの成り立ち」
  - @tbl-dsp-norm の行「データスペースプロトコル 2024-1 | データは、JSON Schema と SHACL のシェイプの両方に従う」
  - 考察の文「IDS-RAM ではオントロジーが、2024-1 版では JSON Schema と SHACL の両方が、2025-1 版では JSON Schema だけが、その役を担う。」
  - `figures/el-dsp-norm.svg` の箱「2024-1 版／規範: JSON Schema と SHACL のシェイプの両方」
- 証拠:
  1. 引用元の文は、バージョン応答という一つのデータオブジェクトについての文である。メッセージ全般の規定ではない。
     > "This data object must comply to the [JSON Schema](schema/version-schema.json) and the [SHACL Shape](shape/version-shape.ttl)."
     https://raw.githubusercontent.com/International-Data-Spaces-Association/ids-specification/2024-1/common/common.protocol.md
  2. その文が指す SHACL ファイルは、2024-1 のタグで 0 バイトである（HTTP 200、0 bytes）。
     https://raw.githubusercontent.com/International-Data-Spaces-Association/ids-specification/2024-1/common/shape/version-shape.ttl
     同じ点を指摘した issue がある: "common/common.protocol.md: Link to SHACL Shape points to empty file"（2024-09-30）https://github.com/eclipse-dataspace-protocol-base/DataspaceProtocol/issues/35
  3. 本文が次の段落で引く提案自身が、当時の仕様はスキーマ技術を規範として使っていないと述べている。表の「規範」と食い違う。
     > "the specification does not **normatively** use a schema technology to define message types. Instead, it includes JSON Schema and Turtle files. The specification, however, mandates messages to be in JSON-LD compact form."
     https://api.github.com/repos/eclipse-dataspace-protocol-base/DataspaceProtocol/issues/25
  4. 2024-1 の各メッセージ型は、表の「Schema」欄に TTL Shape と JSON Schema へのリンクを並べるだけである。規範として義務づけているのは JSON-LD の compact 形式である。
     > "All messages must be serialized in JSON-LD compact form as specified in the JSON-LD 1.1 Processing Algorithms and API"
     https://raw.githubusercontent.com/International-Data-Spaces-Association/ids-specification/2024-1/catalog/catalog.protocol.md
- 修正案: 表の行を「メッセージは JSON-LD の compact 形式で直列化しなければならない。JSON Schema と SHACL のシェイプ（Turtle）は添付されるが、メッセージ型を規範的に定めるものとはされていない。バージョン応答だけは両方に従うと書かれている」に改める。出典に `dsp_issue_25` と 2024-1 の catalog.protocol.md を足す。図の箱は「規範: JSON-LD の compact 形式／JSON Schema と SHACL は添付」、下の段は「JSON-LD の処理が必須」などに改める。考察の文も「2024-1 版では JSON-LD の処理が必須で、スキーマは規範ではなかった」に合わせる。

### F-2 ODS が「4 段目を規範に置く」 — Unsupported、かつ Inconsistent

- 場所:
  - 「考察：データスペースプロトコルと ODS の違い」の文「ODS は、2 段目と 4 段目を規範に置いている [@ods_odp_metadata_exchange; @ipa_why_ods_2026]。」
  - `figures/el-dsp-ods.svg` の ODS 行 4 段目「規範／RDF Schema、OWL」（黒塗り）
  - `figures/el-map.svg` の ODS 行 4 段目「OWL／規範」
  - 「考察：体系化の試み」の箇条書き「データスペースプロトコルは 1 段目、ODS は 2 段目と 4 段目である」
- 証拠:
  1. 規定要件（Normative Requirements）を持つ ODP の仕様が shall で求めるのは RDF だけである。OWL、RDF Schema、推論の語は出てこない。
     > "shall: メタデータは、RDFで表現されなければならない。"
     https://open-dataspaces.gitbook.io/ods-docs/jp/odp/fandamentarupurotokoru/metadtaekusuchenjil4/protocol.md
     英語版の ODS-RAM 02〜05 章、ODP の overview、Metadata Exchange（protocol と binding）、Discovery and Search（protocol と binding）の 9 ページを `OWL|RDFS|RDF Schema|SHACL|reasoner|reasoning|inference` で検索した。該当は binding の JSON-LD 例にある `rdfs` の接頭辞宣言 2 行だけだった。
  2. OWL の根拠である IPA の文書は、自らを設計思想を示す文書と位置づけている。規範文書ではない。
     > "本書は…「Open Data Spaces（ODS）」の設計思想、そしてその中核となるアーキテクチャパラダイムを提示するものである。"
     > "Web Ontology Language（OWL）により妥当性や排他性といった制約を定義する"
     https://www.ipa.go.jp/digital/architecture/documents/rcu1hd000000chgw-att/WhyOpenDataspaces_jp.pdf
  3. オープンソース実装も OWL の制約を使っていない。open-dataspaces 組織を GitHub のコード検索で調べると、`owl:disjointWith` は 0 件、`owl:Restriction` は 0 件である。`ods.ttl` は `owl:Class`、`rdfs:subClassOf`、プロパティ宣言だけからなる。
  4. 文書内の食い違い: @tbl-eu-jp の「規範に置くもの」の行は、ODS について「RDF。メタデータは RDF で表現しなければならない」だけを挙げる。OWL は「オントロジー」の行にあり、規範とは書いていない。同じ節の最後の段落も「設計思想として明示している」と書く。
- 修正案: 本文を「ODS は 2 段目（RDF）を規範に置く [@ods_odp_metadata_exchange]。4 段目（RDF Schema、OWL）は、設計思想の文書が採用を述べている [@ipa_why_ods_2026]。規定要件としての記述は、調査した仕様では確認できなかった」に改める。二つの図の 4 段目は黒塗りをやめ、「設計思想で採用」のような別の凡例にする。「体系化の試み」の箇条書きは「ODS は 2 段目。4 段目は設計思想で採用」とする。同じ箇条書きの一つ目「2 段目より上を規範に置く取り組みは、組織をまたぐ側に集まっている」は、根拠が ODS の 2 段目だけになるので言い方を弱める。

### F-3 調査日、アクセス日、原文照合日 — Inaccurate

- 場所:
  - `method.qmd`「調査は 2026 年 10 月 2 日に実施した。」と、文書の `date: 2026-10-02`
  - `research/ledger.md` の Accessed 列（125 件すべて 2026-10-02）
  - `_bib/bibliography.bib` の `urldate = {2026-10-02}` と note の「原文照合日 2026-10-02」（例: `ipa_why_ods_2026`、`dsp_readme_2025`、`ods_oss_*`）
- 証拠:
  1. `research/build_ledger.py` の 315 行目は、アクセス日を全行に固定で書き込んでいる: `out.append(f"| {i} | {esc(n)} | {u} | {t} | 2026-10-02 | {q} |")`
  2. 4ea8e8e（2026-10-03 02:46）の時点の `method.qmd` は「出典 85 件と主張 106 件」である。S-86 以降の 40 件は、2026-10-03 22:07（4466634）、23:22（03747f5）、23:36（57de700）、2026-10-04 00:30（ebbe00d）のコミットで加わった。
  3. `method.qmd` 自身が @tbl-mapping で「8 リポジトリ（2026-10-03 時点の main ブランチ）」と書いている。
- 修正案: 台帳のアクセス日を出典ごとに持たせ、S-86 以降を実際の取得日（2026-10-03）にする。bib の `urldate` と note も合わせる。`method.qmd` は「調査は 2026 年 10 月 2 日から 3 日に実施した」とする。プロジェクトの「日付には証跡を付ける」という方針にかかわる。

### F-4 照合ツールで不一致となった件数 — Inconsistent

- 場所: `method.qmd`「文字列照合では、2 件が照合ツールで不一致となった。」
- 証拠: `research/ledger.md` の「検証の記録」は不一致を C-05 と C-30 の 2 件とする。一方、同じ台帳の C-147 と C-148 の Status は「照合ツールでは不一致。筆者が PDF を取得し…目視で確認」である。`method.qmd` の @tbl-mapping も「C-147 と C-148 は照合ツールで不一致となった」と書く。合わせて 4 件である。
- 修正案: 「4 件（C-05、C-30、C-147、C-148）が照合ツールで不一致となった。いずれも原文に該当文があることを目視で確認した」に改める。台帳の「検証の記録」にも追補分を足す。

### F-5 ODS の 4 段目に置く技術の名前 — Inconsistent

- 場所: `figures/el-dsp-ods.svg` は ODS の 4 段目を「RDF Schema、OWL」とする。`figures/el-map.svg` は「OWL」だけである。@tbl-eu-jp は「OWL で制約を定義する」と書く。
- 証拠: 二つの SVG の text 要素の比較。出典は RDF Schema と OWL を分けて述べている: "RDF Schema（RDFS）により語彙と構造を与え、Web Ontology Language（OWL）により妥当性や排他性といった制約を定義する"（Why Open Dataspaces、26 ページ）。
- 修正案: F-2 の修正と合わせて、二つの図の表記をそろえる。

### F-6 IDS-RAM 4.0 をプロトコルの版の列に置いていること — Misleading

- 場所: 「何を規範とするかは、プロトコルの版の間で変わった。」の直後の @tbl-dsp-norm の 1 行目「IDS-RAM 4.0」。考察の文「IDS-RAM ではオントロジーが…その役を担う」（その役とは、メッセージが正しいかどうかを判定する役）。
- 証拠:
  1. IDS-RAM 4.0 はプロトコルの版ではない。図 `el-dsp-norm.svg` は「IDSA の先行する別の仕様」と正しく分けているが、本文の導入文は分けていない。
  2. 出典が「唯一の規範」と述べるのは、インフォメーションモデルの三つの表現（概念、宣言、プログラム）のうちどれが規範かである。メッセージの検査ではない。検査は SHACL で行うと書いてある。
     > "Among the different representations, the Declarative Representation (IDS Vocabulary) is the only normative specification of the Information Model."
     > "additionally, descriptions of Digital Resources can be validated against SHACL shapes that express syntactic and semantic conditions."
     https://raw.githubusercontent.com/International-Data-Spaces-Association/IDS-RAM_4_0/main/documentation/3_Layers_of_the_Reference_Architecture_Model/3_3_Information_Layer/3_3_InformationLayer.md
- 修正案: 導入文を「何を規範とするかは、IDS-RAM とデータスペースプロトコルの各版とで違う」に改める。考察は「IDS-RAM ではオントロジーがインフォメーションモデルの規範であり、記述の検査には SHACL のシェイプを使うとされていた」とする。

### F-7 図の出典の表で、欧州相互運用性フレームワークの扱いの理由 — Inconsistent

- 場所: `method.qmd` @tbl-figures の 2 行目「原典の図は転載していない。原典の著作権や利用条件を確認できなかったか、著作権があるためである」。該当する図に欧州相互運用性フレームワークを含む。
- 証拠: 直後の段落は「出典を示せば複製を認めると記している。原典の図は英語なので、日本語で描き直し」と、別の理由を述べる。冊子の記載は "Reproduction is authorised provided the source is acknowledged."（https://ec.europa.eu/isa2/sites/default/files/eif_brochure_final.pdf の 2 ページ）。IPA の文書（CC BY 4.0）についても同じことが言える。
- 修正案: 表の「扱い」を「利用条件を確認できなかったもの、著作権があるもの、原典が英語のもの（欧州相互運用性フレームワーク）を描き直した」とする。または、欧州相互運用性フレームワークを別の行に分ける。

### F-8 DCAT と ODRL の扱いの語と、その出典 — Inconsistent（軽微）

- 場所: サマリと @tbl-dataspace-intl は「再利用」と書く。@tbl-eu-jp、`el-dsp-ods.svg`、`el-map.svg`、本文「2 段目の語彙は参照にとどめている [@dsp_2025_common]」は「参照」と書く。
- 証拠: 引用された common.protocol.md に DCAT と ODRL の語は出てこない。根拠になるのは次の二つである。
  > "The Catalog Protocol reuses properties from the DCAT and ODRL vocabularies with restrictions defined in this specification. This is done implicitly by the use of the JSON schemas and JSON-LD-contexts"（catalog.protocol.md）
  > "this specification is leveraging Profiles of the original definitions rather than the complete original expressiveness. … They are not separate artifacts but implicitly contained in the JavaScript Object Notation (JSON) schemas"（https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/common/introduction.md）。この文書で DCAT と ODRL は `[[?vocab-dcat-3]]`、`[[?odrl-model]]` と、参考（informative）の参照として書かれている。
- 修正案: 語を「プロファイルとして再利用する（規範は JSON Schema の側にある）」にそろえる。「参照にとどめている」の文の出典を `dsp_2025_catalog` に替えるか、introduction.md を出典に加える。

### F-9 MCP の説明と「言語モデル」の箱 — Unsupported（軽微）

- 場所: 「MCP は、言語モデルに外部の道具を使わせるための仕組みである。」（出典なし）。`el-ods-oss.svg` の箱「言語モデル／MCP ツールを道具として使う」。
- 証拠: 引用された README は「チャットUIとバックエンドサービス…を連携するMCPサーバ」「MCPツールとして公開します」と書く。言語モデルや LLM の語はない（`LLM|言語モデル` の検索で 0 件）。言語モデルとの関係を示すのは、リポジトリの説明文 "LLM chat interface and MCP server for UASL" である（https://api.github.com/orgs/open-dataspaces/repos）。
- 修正案: MCP の説明に出典を付ける（Model Context Protocol の公式仕様）。図の出典に、リポジトリの説明文を足す。用語集に MCP を加える。

### F-10 節と主張の対応表の漏れ — Inconsistent（軽微）

- 場所: `method.qmd` @tbl-mapping
- 証拠: 表の ID を機械的に集めると、C-109、C-139、C-140、C-168、C-169、C-178、C-179 がどの行にもない。C-178 は図 @fig-el-eif の根拠で、C-179 は `method.qmd` の「図の出典と利用条件」の根拠である。「考察：データスペースプロトコルと ODS の違い」の行は C-69, C-70, C-102, C-106, C-115, C-124 を挙げるが、同節の本文は開世界仮説、OWL、閉世界的な検証（C-151、C-152、C-154、C-155）を使っている。
- 修正案: 「欧州」の行に C-72、C-73、C-178 を、「図の出典と利用条件」に C-179 を、「違い」の行に C-151、C-152、C-154、C-155 を足す。残りの 5 件は該当する節の行に足す。

## 正しいが注記を勧める点（OK-but-note）

| 番号 | 場所 | 内容 |
|---|---|---|
| N-1 | `el-ods-oss.svg` の「クローラ → カタログ」 | README では、分散カタログがクローラのサービスそのものである。格納先は「キャッシュ（GraphDB）」と書かれている。「カタログ／収集した RDF データを格納」の箱は「キャッシュ（GraphDB）」とするほうが原文に近い。矢印の向きはデータの流れとしては正しい（クローラが SPARQL の CONSTRUCT を発行して取得する）。 |
| N-2 | @tbl-ods-concept の 5 行目「代わりに、二段階の問い合わせを導入する」 | 原文は、不足の検出には「SHACL などの閉世界的検証の導入が必要であるが、CWA の強制は…相いれない。このトレードオフを解決するために…二段階のクエリ概念を導入」と書く。35 ページでは「限定された境界における CWA 的な検証を選択肢として導入することは排除しない」とも書く。「代わりに」より「この折り合いをつけるために」が近い。4 行目は、原文の「RDF 及び RDF*」から RDF* を落としている。 |
| N-3 | @tbl-ods-oss「W3C 標準の語彙を組み合わせて」 | README の表現どおりである。ただし README が挙げる `hydra:` は W3C のコミュニティグループの草案で、`dcterms:` は DCMI の語彙である。「README は W3C 標準の語彙と呼んでいる」と書くと安全である。 |
| N-4 | @tbl-eu-jp「問い合わせ｜仕様の対象外」 | 原文は "A Catalog Service may support Catalog queries or filter expressions as an implementation-specific feature." である。「実装依存（仕様は定めない）」が正確である。 |
| N-5 | 2025-1 版 | 2025-1 には正誤版の 2025-1-err1（2025-11-12）と 2025-1-err2（2026-09-11）が出ている。ISO の案件記録には "Adopted from DSP v1.0.0" とある。本文は 2025-1 のタグを引いており、誤りではない。 |
| N-6 | 「二層」の語 | @tbl-ods-concept では Ontology Product と Data Product の二層を指す。ODS のオープンソース実装の考察と `el-ods-oss.svg` の見出しでは、ODS オントロジーと領域のオントロジーの二層を指す。後者は筆者の整理なので、図の見出しを「二種類のオントロジー（筆者の整理）」などに変えると混同を避けられる。 |
| N-7 | `el-eif.svg` | 4 層、横断する要素、背景となる層の構成と並び順は、原典の図 3 と合っている。原典では「Integrated Public Service Governance」が 4 層に重なる縦の帯だが、描き直した図では 4 層の右に並んでいる。 |
| N-8 | `method.qmd`「プロトコルの開発者の一人が…」 | issue 44 の原文は "not only in the wrong namespace but also assumes definitions that are not inline with DSP-terminology and thus not salvageable in my opinion" で、内容は合っている。発言者（arnoweiss）が開発者であることは、issue からは分からない。「issue の起票者」とするのが安全である。 |
| N-9 | 用語集 | この章で初めて出る ODRL、SPARQL、MCP、開世界仮説と閉世界仮説、データスペースプロトコルが用語集にない。 |

## 確認して正しかった点

| 対象 | 確認した内容 | 結果 |
|---|---|---|
| 2025-1 common | "All protocol Messages are normatively defined by a [[json-schema]]"、JSON-LD 1.1、JSON か JSON-LD かは実装が選べる | 一致 |
| 2025-1 catalog | DCAT と ODRL の再利用、"implicitly by the use of the JSON schemas and JSON-LD-contexts" | 一致 |
| dspace.jsonld | `"dspace": "https://w3id.org/dspace/2025/1/"` | 一致 |
| 2025-1 README | 0.8 と 2024-1 は IDSA の管理下で開発。2024-1 が Eclipse への最初の寄贈 | 一致 |
| v0.8 README | DCAT のカタログ、ODRL のポリシー。Working Draft 2023-02-01 | 一致 |
| issue 25 | 2024-09-16 起票、Jim Marino。規範的なスキーマ技術の不使用、JSON-LD 処理の任意化、複雑さが相互運用性を妨げる。2025-01-16 に completed で終了 | 一致 |
| 2025-1 の公開日（method） | GitHub のリリース 2025-08-29 | 一致 |
| Eclipse の発表 | 2025-12-02、ISO/IEC JTC1 の PAS、2 仕様の名称、作業グループの名称 | 一致 |
| ISO/IEC DIS 26450 | 段階 40.99、"DIS approved for registration as FDIS"、2026-09-15。各国機関による掲載 | 一致 |
| IDS-RAM 4.0 | "the only normative specification of the Information Model" | 一致（F-6 の注意つき） |
| IDS インフォメーションモデル | RDFS/OWL オントロジー、archived: true、`rdfs:subClassOf odrl:Policy`、DCAT-AP 1.1 | 一致 |
| Gaia-X 24.04 | "W3C Verifiable Credentials with claims expressed in RDF" | 一致 |
| Catena-X CX-0003、SAMM | "must adhere to the Semantic Aspect Meta Model"、RDF と Turtle と SHACL | 一致 |
| DCAT-AP 3.0.1 | "SEMIC Recommendation published at 2025-10-27" | 一致 |
| DSSC ブループリント | "including vocabularies, ontologies, application profiles, schema specifications" | 一致 |
| 欧州相互運用性フレームワーク | 4 層、横断する要素、背景となる層、意味的相互運用性の定義、複製の許諾 | 一致 |
| ODS-RAM 3 章 | 4 レイヤの名称、L4 の要求、L4 は OWA、L1 は CWA を選択的に採用 | 一致 |
| ODP メタデータエクスチェンジ | RDF の shall、SPARQL 取得、JSON-LD は should | 一致 |
| Why Open Dataspaces | データモデルと情報モデルの分離、Data Product と Ontology Product、OWA と CWA の二層、スキーマフレキシブル、RDF と RDFS と OWL、意味の所在をコードから論理体系へ、選択的な厳格性、OSI の呼称、CC BY 4.0 | 一致 |
| ods.ttl | owl:Ontology、題、説明文、`ods:DataExchangeService a owl:Class` | 一致 |
| SDK for Semantics README | SAMM をベース、REST API の定義手段がないための拡張 | 一致 |
| uasl-core-2026-01-06.ttl、組織の README | `:Uasl rdf:type owl:Class`、UASL の展開形、DADC が中立的な組織 | 一致 |
| L4-sparql-server-sample | Fuseki に対して SPARQL を実行する REST API | 一致 |
| L4-crawler-service | 複数のドメインアプリケーションの SPARQL エンドポイントから収集して格納 | 一致 |
| L4-uasl-chat-server | SAMM アスペクトモデルと API 定義から MCP ツールを生成 | 一致 |
| SHACL が見つからないこと | 組織全体のコード検索で `NodeShape` は 0 件、`shacl` は pnpm-lock.yaml の 1 件 | 一致 |
| セマンティクス関連のリポジトリ数 | L4- の 7 件と SDK-for-semantics で 8 件 | 一致 |
| method の件数 | 出典 125、主張 179、T1 88、T2 33、T3 4、81+15+83=179、推論 I-01〜I-06 | 一致 |
| Wikidata の図 | Commons の API で CC0、作者 Charlie Kritschmar (WMDE) | 一致 |
| 図と表の段の対応 | データスペースプロトコル（1 段目が規範、2 段目が参照）、Palantir（1、2 段目を備える、3 段目は一部、4 段目なし）、データベース（1 段目）、セマンティックレイヤ（段の外）、Web 標準（1〜4 段目）は、`el-map.svg`、`el-dsp-ods.svg`、`el-dsp-norm.svg`、@tbl-ladder-streams、@tbl-palantir-ladder、@tbl-off-ladder、@tbl-eu-jp、本文で一致。食い違いは F-2、F-5、F-8 だけ | 一致 |
| 用語集 | DCAT 第 3 版 2024-08-22、SAMM、ODS-RAM の展開形、OSI | 一致 |

## 確認できなかった点

- ODS の日本語版 GitBook の全ページ。OWL や推論を規定要件とする記述がないことは、英語版の 9 ページの検索による（F-2）。開発者向けガイドと入門ガイドは検索していない。
- GitHub のコード検索は、索引の対象外のファイル（大きなファイル、フォーク）を返さない。SHACL と OWL の制約が「ない」ことは、この範囲での結果である。
- 2025-1 の候補版（RC1〜RC4）のどれで JSON Schema が初めて規範になったか。`method.qmd` も未確認としている。
- Palantir、分析系、技術要素の章は、この回の対象外である。@tbl-palantir-ladder と @tbl-ladder-streams は、図との整合だけを見た。出典との照合はしていない。
- 用語集のうち、4ea8e8e より前からある行（MOF、BFO、GQL など）は、出典を取得し直していない。
