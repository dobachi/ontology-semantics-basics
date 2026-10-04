# 調査計画: オントロジー・セマンティクス・データモデル標準化の体系化

- 日付: 2026-10-02
- 深さ: Standard（サブ質問 7、各リトリーバ検索上限 6、日付・数値・定義の主要クレームを盲検検証）
- 目的: 初心者向け説明ペーパー（pptx）の土台となる基礎調査レポート（Quarto）
- 言語: 日本語（引用スパンは原語）
- 情報源制約: T1（標準文書・学術論文・公式仕様）/T2（ベンダ公式）優先。T3 は補助、T4 不可

## サブ質問
1. SQ1 歴史: 哲学的オントロジー → 知識表現（KL-ONE, Cyc, Gruber 1993 定義, Ontolingua, KIF）→ Semantic Web 構想（Berners-Lee 2001）。各節目の年と一次資料
2. SQ2 W3C 標準スタック: RDF（1999/2004/2014）, RDFS, OWL（2004）, OWL 2（2009/2012）, SKOS（2009）, SPARQL（2008/2013）, SHACL（2017）, JSON-LD（2014/2020）。勧告日・位置づけ・用途
3. SQ3 データモデル標準化の系譜: ER（Chen 1976）, 関係モデル（Codd 1970）, ISO/IEC 11179（メタデータレジストリ）, ISO 15926, UML/MOF（OMG）, XML Schema, JSON Schema, Schema.org（2011）, DCAT（2014/2020/2024）, Dublin Core（1995/ISO 15836）
4. SQ4 米国系の近年の取り組み（分析系セマンティックレイヤ）: Open Semantic Interchange（OSI, Snowflake 2025-09）, dbt Semantic Layer/MetricFlow, Databricks Unity Catalog Metric Views, Cube, LookML, AtScale, Microsoft Power BI/Fabric semantic model。各発表日・参加企業・仕様の形（YAML 等）・Linux Foundation 移管の有無
5. SQ5 米国系の近年の取り組み（オントロジー製品/知識グラフ）: Palantir Ontology, Google Knowledge Graph（2012）, Schema.org, Wikidata（2012）, Amazon Neptune/Microsoft Graph, ISO/IEC 39075 GQL（2024）, Property Graph vs RDF, Enterprise Knowledge Graph, GraphRAG / LLM 連携（Ontology + LLM）
6. SQ6 ドメインオントロジー・業界標準: FIBO（金融）, Gene Ontology/SNOMED CT/HL7 FHIR（医療）, ISO 15926/CFIHOS（プロセス産業）, Asset Administration Shell / ECLASS（製造, Industrie 4.0）, BFO（ISO/IEC 21838）, Common Core Ontologies（米 DoD）, 米国 DoD/IC の semantic 取り組み
7. SQ7 データスペースとの接点: IDS Information Model（RDF/OWL）, DCAT-AP, DSP（Dataspace Protocol, Eclipse/ISO 化）, Gaia-X Self-Description（JSON-LD/SHACL）, Catena-X semantic models（SAMM/ESMF, BAMM）, EU Data Act・Simpl における「セマンティック相互運用性」、ODS-RAM での扱い

## 成果物
- research/ledger.md（Source Register + Claim Ledger）
- docs/ 配下 Quarto 本文、_bib/bibliography.bib
