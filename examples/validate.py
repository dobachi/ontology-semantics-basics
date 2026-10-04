#!/usr/bin/env python3
"""examples/ の例を処理系に通して検証する。必要: rdflib, pyshacl, jsonschema, pyyaml。
Ossie の検証には ossie-schema.json が必要（apache/ossie の core-spec/ から取得し、--ossie-schema で渡す）。"""
import json, sqlite3, sys, os, argparse
import rdflib, pyshacl, jsonschema, yaml
ap = argparse.ArgumentParser(); ap.add_argument("--ossie-schema"); a = ap.parse_args()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ok = True
def report(name, passed, detail=""):
    global ok; ok &= passed; print(f"{'OK  ' if passed else 'FAIL'} {name} {detail}")
# 関係モデル
con = sqlite3.connect(":memory:"); con.executescript(open("relational.sql").read().split("SELECT")[0])
rows = con.execute("SELECT" + open("relational.sql").read().split("SELECT")[1]).fetchall()
report("relational.sql", rows == [("六角ボルト M8", "東和精工")], str(rows))
# 指標とディメンションの例
mrows = con.execute(open("metric.sql").read()).fetchall()
report("metric.sql", mrows == [("東和精工", 1)], str(mrows))
# RDF 系の構文
graphs = {}
for f in ["data.ttl", "rdfs.ttl", "owl.ttl", "skos.ttl", "shapes.ttl", "data-invalid.ttl", "dcat.ttl"]:
    g = rdflib.Graph(); g.parse(f, format="turtle"); graphs[f] = g; report(f, len(g) > 0, f"{len(g)} triples")
# JSON-LD が data.ttl の部品と同じトリプルになるか
j = rdflib.Graph(); j.parse("data.jsonld", format="json-ld")
part = {t for t in graphs["data.ttl"] if str(t[0]).endswith("P-100")}
report("data.jsonld", set(j) == part, f"{len(j)} triples, data.ttl の部品と一致={set(j) == part}")
# SPARQL
res = [(str(r[0]), str(r[1])) for r in graphs["data.ttl"].query(open("query.rq").read())]
report("query.rq", res == [("六角ボルト M8", "東和精工")], str(res))
# SHACL
c1, _, _ = pyshacl.validate(graphs["data.ttl"], shacl_graph=graphs["shapes.ttl"])
c2, rg, _ = pyshacl.validate(graphs["data-invalid.ttl"], shacl_graph=graphs["shapes.ttl"])
n = len(list(rg.subjects(rdflib.RDF.type, rdflib.URIRef("http://www.w3.org/ns/shacl#ValidationResult"))))
report("shapes.ttl", c1 and not c2 and n == 2, f"正しいデータ=適合 {c1}、誤ったデータ=適合 {c2}（違反 {n} 件）")
# JSON Schema
s = json.load(open("part.schema.json")); jsonschema.Draft202012Validator.check_schema(s)
jsonschema.validate(json.load(open("part.json")), s)
try: jsonschema.validate({"part_id": "100", "name": "x"}, s); bad = False
except jsonschema.ValidationError: bad = True
report("part.schema.json", bad, "正しい例は適合、誤った例は不適合")
# Ossie
doc = yaml.safe_load(open("ossie.yaml"))
if a.ossie_schema:
    jsonschema.validate(doc, json.load(open(a.ossie_schema))); report("ossie.yaml", True, "ossie-schema.json に適合")
else:
    print("SKIP ossie.yaml（--ossie-schema 未指定。YAML の構文のみ確認）")
print("注: property-graph.gql は処理系がなく未検証")
sys.exit(0 if ok else 1)
