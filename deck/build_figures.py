#!/usr/bin/env python3
"""説明ペーパー用の図を deck/figures/ に用意する。

- 調査報告の図（figures/*.svg）を PNG に変換する。
- 年表だけは、スライドで読める文字の大きさにした専用版を描く。出来事を絞り、文字を大きくしている。
"""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "..", "figures"); OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)
for name in ["el-intro", "el-why-now", "el-triangle", "el-ladder", "el-triangle-steps", "el-off-ladder", "el-ladder-streams", "el-rdf", "el-semantic-layer", "el-datamodel-map", "el-domain-map", "el-palantir", "el-two-streams", "el-eif", "el-dsp-norm", "el-dsp-ods", "el-ods-oss", "el-map", "el-spectrum", "dk-same-name", "dk-readers", "dk-owl-shacl", "dk-ossie-two", "dk-spectrum-ladder", "dk-okf", "dk-not-fit", "el-choose"]:
    subprocess.run(["rsvg-convert", "-w", "2000", os.path.join(SRC, name + ".svg"), "-o", os.path.join(OUT, name + ".png")], check=True)

# 外部の図（Wikimedia Commons、CC0）はそのまま写す
import shutil
shutil.copy(os.path.join(SRC, "ext-wikidata-datamodel.png"), os.path.join(OUT, "ext-wikidata-datamodel.png"))

# 年表（スライド専用版）
W, LEFT, RIGHT, LANE_H, TOP = 1040, 190, 30, 86, 50
INK, MUTED, GRID = "#1f2933", "#52606d", "#d9dee4"
LANES = [
 ("データベース系", "#0072B2", [(1970, "関係モデル", -1, "start"), (1976, "実体関連モデル", 1, "start"), (2024, "GQL", -1, "middle")]),
 ("知識表現系", "#D55E00", [(1984, "Cyc 着手", -1, "end"), (1993, "オントロジーの定義", 1, "middle"), (2021, "BFO が国際規格に", -1, "end")]),
 ("Web 標準系", "#009E73", [(1999, "RDF", -1, "middle"), (2004, "OWL", 1, "middle"), (2014, "DCAT", -1, "middle"), (2017, "SHACL", 1, "middle")]),
 ("分析系", "#7B4EA3", [(1991, "Business Objects の特許", -1, "middle"), (2025, "OSI 発表", -1, "end"), (2026, "Apache Ossie、OKF", 1, "end")]),
]
X0, X1, XB = LEFT + 20, W - RIGHT - 20, LEFT + 20 + 290
def x(y): return X0 + (y - 1968) / (1995 - 1968) * (XB - X0) if y <= 1995 else XB + (y - 1995) / (2027 - 1995) * (X1 - XB)
H = TOP + LANE_H * len(LANES) + 8
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="\'Noto Sans CJK JP\',\'Yu Gothic\',sans-serif">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
for y in [1970, 1980, 1990, 2000, 2010, 2020]:
    o.append(f'<line x1="{x(y):.1f}" y1="{TOP-6}" x2="{x(y):.1f}" y2="{H-8}" stroke="{GRID}" stroke-width="1"/>')
    o.append(f'<text x="{x(y):.1f}" y="{TOP-16}" font-size="17" fill="{MUTED}" text-anchor="middle">{y}</text>')
for i, (name, col, evs) in enumerate(LANES):
    y0 = TOP + i * LANE_H; yc = y0 + LANE_H / 2
    if i % 2 == 0: o.append(f'<rect x="0" y="{y0}" width="{W}" height="{LANE_H}" fill="#f6f8fa"/>')
    o.append(f'<rect x="0" y="{y0+12}" width="7" height="{LANE_H-24}" fill="{col}"/>')
    o.append(f'<text x="20" y="{yc+7:.0f}" font-size="21" font-weight="700" fill="{INK}">{name}</text>')
    xs = [x(e[0]) for e in evs]
    o.append(f'<line x1="{min(xs):.1f}" y1="{yc}" x2="{X1+14:.1f}" y2="{yc}" stroke="{col}" stroke-width="3" opacity="0.45"/>')
    for yr, label, side, anchor in evs:
        cx = x(yr); ty = yc - 15 if side < 0 else yc + 30
        tx = cx + 10 if anchor == "end" else (cx - 10 if anchor == "start" else cx)
        o.append(f'<circle cx="{cx:.1f}" cy="{yc}" r="8" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
        o.append(f'<text x="{tx:.1f}" y="{ty:.0f}" font-size="18" fill="{INK}" text-anchor="{anchor}">{label} <tspan fill="{MUTED}" font-size="16">{yr}</tspan></text>')
o.append("</svg>")
svg = os.path.join(OUT, "lineage-deck.svg"); open(svg, "w").write("\n".join(o))
subprocess.run(["rsvg-convert", "-w", "2400", svg, "-o", os.path.join(OUT, "lineage-deck.png")], check=True)
print("deck figures ready")
