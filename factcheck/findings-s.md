# S: データスペース章・未確認事項の再調査（独立検証）
判定: 16 件。Verified 14、Mostly Accurate 1（S-15）、Misleading 1（S-16）。架空出典なし。
指摘:
- S-16【要修正・考察】「IDS は当初、独自の包括的なオントロジーを持っていた／DSP は既存 W3C 語彙の再利用に移った」は対比が過大。IDS インフォメーションモデル自体が ODRL と DCAT(-AP) を取り込んでいる（ontology.ttl に odrl 接頭辞、Contract は odrl:Policy のサブクラス、Resource は odrl:Asset のサブクラスで DCAT-AP 1.1 を参照）。DSP は "This is done implicitly by the use of the JSON schemas and JSON-LD-contexts"。
- S-15 サマリ 4「データスペースは Web 標準系の語彙を再利用」は DSP からの一般化しすぎ。SAMM は W3C 語彙ではなく ESMF 独自のメタモデル。
- E2 書誌 semic_dcatap_301 の year=2024 は誤り。原文 "This application profile has the status SEMIC Recommendation published at 2025-10-27."
- S-14 2 仕様の名称: Eclipse Dataspace Protocol、Eclipse Dataspace Decentralised Claims Protocol
- S-13 IPA ページ: 公開日 2026年4月1日、最終更新日 2026年5月1日
- S-03 IDS リポジトリ最終 push 2023-12-15。README に後継の記載なし
新たに確認できた一次情報:
- IEC 63278-1:2023 https://webstore.iec.ch/en/publication/65628 "Publication date 2023-12-14 Edition 1.0"
- schema.org 公開: https://developers.google.com/search/blog/2011/06/introducing-schemaorg-search-engines "Thursday, June 02, 2011" "Today we're announcing schema.org, a new initiative from Google, Bing and Yahoo! to create and support a common set of schemas for structured data markup on web pages."
- DSP の ISO 段階（ISO 本体は 403。各国機関の写し）: https://iss.rs/en/project/show/iso:proj:93502 "ISO/IEC DIS 26450 ... Current stage: 40.99 ... DIS approved for registration as FDIS Sep 15, 2026"; https://www.dinmedia.de/en/draft-standard/iso-iec-dis-26450/400043453 "ISO/IEC DIS 26450:2026-02"
依然未確認: ISO/IEC 11179-1、ISO 15926-1、Wikidata 公開日
