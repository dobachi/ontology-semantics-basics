#!/usr/bin/env python3
"""四本の系譜の年表図 figures/lineage.svg を生成する。年は調査報告の年表の出典による。"""
import os
W,LEFT,RIGHT=1040,170,30
LANE_H,TOP=128,54
INK,MUTED,GRID="#1f2933","#52606d","#d9dee4"
# 系統ごとに 1 色。色覚多様性に配慮した配色（Okabe-Ito）。色は系統の区別だけに使う。
# 出来事: (年, ラベル, 上下(-1 上/+1 下), 段(0 近い/1 遠い), 文字揃え)
LANES=[
 ("データベース系","データの構造を決める","#0072B2",[(1970,"関係モデル",-1,0,"middle"),(1976,"実体関連モデル",1,0,"middle"),(2024,"GQL（グラフ問い合わせ）",-1,0,"end")]),
 ("知識表現系","概念と論理を記述する","#D55E00",[(1984,"Cyc 着手",-1,0,"end"),(1985,"KL-ONE の概説論文",1,0,"middle"),(1993,"オントロジーの定義",-1,0,"middle"),(1998,"定義の改訂と分類",1,0,"middle"),(2021,"BFO が ISO/IEC 規格に",-1,0,"middle")]),
 ("Web 標準系","意味を Web で共有する","#009E73",[(1999,"RDF",-1,0,"middle"),(2004,"OWL",1,0,"middle"),(2008,"SPARQL",-1,0,"end"),(2009,"SKOS",1,0,"start"),(2014,"DCAT、JSON-LD",-1,0,"middle"),(2017,"SHACL",1,0,"middle"),(2024,"DCAT 第 3 版",-1,0,"middle")]),
 ("分析系","指標の定義を一元化する","#7B4EA3",[(1991,"Business Objects の特許",-1,0,"middle"),(2023,"Power BI が「セマンティックモデル」に改称",-1,0,"end"),(2025,"OSI 発表",1,0,"end"),(2026,"Apache Ossie、OKF",1,1,"end")]),
]
# 1995 年以前は出来事が少ないので横幅を圧縮する
X0,X1,XB=LEFT+20,W-RIGHT-20,LEFT+20+300
def x(y):
    return X0+(y-1968)/(1995-1968)*(XB-X0) if y<=1995 else XB+(y-1995)/(2027-1995)*(X1-XB)
H=TOP+LANE_H*len(LANES)+46
o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="四本の系譜の年表" font-family="\'Noto Sans CJK JP\',\'Hiragino Sans\',\'Yu Gothic\',sans-serif">',
   f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
# 年の目盛り
for y in [1970,1980,1990,2000,2005,2010,2015,2020,2025]:
    o.append(f'<line x1="{x(y):.1f}" y1="{TOP-8}" x2="{x(y):.1f}" y2="{TOP+LANE_H*len(LANES)}" stroke="{GRID}" stroke-width="1"/>')
    o.append(f'<text x="{x(y):.1f}" y="{TOP-16}" font-size="13" fill="{MUTED}" text-anchor="middle">{y}</text>')
for i,(name,sub,col,evs) in enumerate(LANES):
    y0=TOP+i*LANE_H; yc=y0+LANE_H/2
    if i%2==0: o.append(f'<rect x="0" y="{y0}" width="{W}" height="{LANE_H}" fill="#f6f8fa"/>')
    o.append(f'<rect x="0" y="{y0+14}" width="6" height="{LANE_H-28}" fill="{col}"/>')
    o.append(f'<text x="20" y="{yc-4:.0f}" font-size="17" font-weight="700" fill="{INK}">{name}</text>')
    o.append(f'<text x="20" y="{yc+16:.0f}" font-size="12.5" fill="{MUTED}">{sub}</text>')
    xs=[x(e[0]) for e in evs]
    o.append(f'<line x1="{min(xs):.1f}" y1="{yc}" x2="{X1+14:.1f}" y2="{yc}" stroke="{col}" stroke-width="3" stroke-linecap="round" opacity="0.45"/>')
    for (yr,label,side,tier,anchor) in evs:
        cx=x(yr); ty=(yc-16-22*tier) if side<0 else (yc+30+22*tier)
        tx=cx+9 if anchor=="end" else (cx-9 if anchor=="start" else cx)
        if tier: o.append(f'<line x1="{cx:.1f}" y1="{yc}" x2="{cx:.1f}" y2="{ty-14 if side>0 else ty+5:.0f}" stroke="{col}" stroke-width="1" opacity="0.6"/>')
        o.append(f'<circle cx="{cx:.1f}" cy="{yc}" r="7" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
        o.append(f'<text x="{tx:.1f}" y="{ty:.0f}" font-size="14" fill="{INK}" text-anchor="{anchor}">{label} <tspan fill="{MUTED}" font-size="12.5">{yr}</tspan></text>')
yb=TOP+LANE_H*len(LANES)+28
o.append(f'<text x="20" y="{yb}" font-size="12.5" fill="{MUTED}">横軸は年。1995 年以前は間隔を詰めて描いている。色は系統の区別だけを表す。</text>')
o.append('</svg>')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'lineage.svg'),'w').write("\n".join(o))
