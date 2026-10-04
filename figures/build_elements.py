#!/usr/bin/env python3
"""技術要素の解説章の図を生成する。配色は lineage.svg と共通（系統ごとに 1 色）。"""
import os
OUT=os.path.dirname(os.path.abspath(__file__))
INK,MUTED,LINE="#1f2933","#52606d","#9aa5b1"
DB,KR,WEB,BI="#0072B2","#D55E00","#009E73","#7B4EA3"
TINT={DB:"#e8f2f9",KR:"#fcefe6",WEB:"#e6f5f0",BI:"#f1ebf7","n":"#f6f8fa"}
FONT="'Noto Sans CJK JP','Hiragino Sans','Yu Gothic',sans-serif"
MONO="'Noto Sans Mono CJK JP','DejaVu Sans Mono',monospace"
class Fig:
    def __init__(s,w,h,label): s.w,s.h,s.o=w,h,[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}" font-family="{FONT}">','<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#52606d"/></marker></defs>',f'<rect width="{w}" height="{h}" fill="#ffffff"/>']
    def text(s,x,y,t,size=14,fill=INK,anchor="start",bold=False,mono=False):
        s.o.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{" font-weight=\"700\"" if bold else ""}{f" font-family=\"{MONO}\"" if mono else ""}>{t}</text>')
    def box(s,x,y,w,h,title=None,lines=(),col=None,dashed=False,mono=False,tsize=15):
        c=col or LINE; f=TINT.get(col,TINT["n"])
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f}" stroke="{c}" stroke-width="1.5"{" stroke-dasharray=\"6 4\"" if dashed else ""}/>')
        yy=y+24
        if title: s.text(x+w/2,yy,title,tsize,INK,"middle",True); yy+=22
        for l in lines: s.text(x+14 if mono else x+w/2,yy,l,13,MUTED if not mono else INK,"start" if mono else "middle",False,mono); yy+=19
    def ell(s,cx,cy,rx,ry,t,col): 
        s.o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{TINT[col]}" stroke="{col}" stroke-width="1.5"/>'); s.text(cx,cy+5,t,14,INK,"middle",False,True)
    def arrow(s,x1,y1,x2,y2,label=None,dashed=False,both=False,lx=None,ly=None,lanchor="middle"):
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#52606d" stroke-width="1.5" marker-end="url(#a)"{" marker-start=\"url(#a)\"" if both else ""}{" stroke-dasharray=\"5 4\"" if dashed else ""}/>')
        if label: s.text(lx if lx is not None else (x1+x2)/2, ly if ly is not None else (y1+y2)/2-8,label,13,INK,lanchor)
    def save(s,name): open(os.path.join(OUT,name),"w").write("\n".join(s.o+["</svg>"]))

def table(f,x,y,title,cols,row,widths,col):
    f.text(x,y-10,title,15,INK,"start",True); cx=x
    for c,v,w in zip(cols,row,widths):
        f.o.append(f'<rect x="{cx}" y="{y}" width="{w}" height="30" fill="{TINT[col]}" stroke="{col}" stroke-width="1.2"/>')
        f.o.append(f'<rect x="{cx}" y="{y+30}" width="{w}" height="30" fill="#ffffff" stroke="{col}" stroke-width="1.2"/>')
        f.text(cx+w/2,y+20,c,13,INK,"middle",True,True); f.text(cx+w/2,y+50,v,13,INK,"middle"); cx+=w

# 1 関係モデル
f=Fig(760,250,"関係モデルの例")
table(f,30,50,"部品（part）",["part_id","name","weight_g","supplier_id"],["P-100","六角ボルト M8","12","S-01"],[90,150,90,110],DB)
table(f,480,160,"供給者（supplier）",["supplier_id","name"],["S-01","東和精工"],[110,130],DB)
f.o.append('<path d="M415,110 L415,205 L478,205" fill="none" stroke="#52606d" stroke-width="1.5" marker-end="url(#a)"/>')
f.text(405,150,"外部キーで参照",13,INK,"end")
f.text(30,235,"データは表で持ち、表どうしは値の一致（キー）で結びつける。",13,MUTED)
f.save("el-relational.svg")
# 2 実体関連モデル
f=Fig(760,220,"実体関連モデルの例")
f.box(40,50,200,110,"部品",["部品番号（識別子）","名称","重量"],DB)
f.box(520,50,200,110,"供給者",["供給者番号（識別子）","名称"],DB)
f.o.append(f'<polygon points="380,60 450,105 380,150 310,105" fill="#ffffff" stroke="{DB}" stroke-width="1.5"/>'); f.text(380,110,"供給する",14,INK,"middle",True)
f.o.append('<line x1="240" y1="105" x2="310" y2="105" stroke="#52606d" stroke-width="1.5"/><line x1="450" y1="105" x2="520" y2="105" stroke="#52606d" stroke-width="1.5"/>')
f.text(275,95,"多",13,INK,"middle"); f.text(485,95,"1",13,INK,"middle")
f.text(40,200,"設計の段階で、実体（四角）と関連（ひし形）、数の対応を図に描く。",13,MUTED)
f.save("el-er.svg")
# 3 プロパティグラフ
f=Fig(760,230,"プロパティグラフの例")
f.box(40,50,220,110,":Part",["id: 'P-100'","name: '六角ボルト M8'","weight_g: 12"],DB,mono=True)
f.box(500,50,220,110,":Supplier",["id: 'S-01'","name: '東和精工'"],DB,mono=True)
f.arrow(260,105,500,105,":SUPPLIED_BY",ly=92); f.text(380,128,"{since: 2021}",13,MUTED,"middle",False,True)
f.text(40,205,"ノードにも辺にも、ラベルとプロパティを直接持たせる。",13,MUTED)
f.save("el-property-graph.svg")
# 4 RDF
f=Fig(760,270,"RDF のトリプルの例")
f.ell(140,130,100,28,"ex:P-100",WEB); f.ell(600,60,100,28,"ex:Part",WEB); f.ell(600,130,100,28,"ex:S-01",WEB)
f.o.append(f'<rect x="490" y="180" width="220" height="40" fill="#ffffff" stroke="{WEB}" stroke-width="1.5"/>'); f.text(600,205,'"六角ボルト M8"',14,INK,"middle")
f.arrow(232,115,502,68,"rdf:type",lx=360,ly=78); f.arrow(240,130,500,130,"ex:suppliedBy",ly=122); f.arrow(232,145,488,196,"ex:name",lx=350,ly=190)
f.text(140,180,"主語",13,MUTED,"middle"); f.text(370,150,"述語",13,MUTED,"middle"); f.text(600,22,"目的語",13,MUTED,"middle")
f.text(40,255,"すべての情報を「主語、述語、目的語」の 3 つ組で表す。楕円は識別子、四角は値。",13,MUTED)
f.save("el-rdf.svg")
# 5 RDFS / OWL
f=Fig(760,300,"RDF Schema と OWL の例")
f.box(60,30,180,44,"ex:Product",(),WEB); f.box(520,30,180,44,"ex:Organization",(),WEB)
f.box(60,130,180,44,"ex:Part",(),WEB); f.box(520,130,180,44,"ex:Supplier",(),WEB)
f.arrow(150,130,150,76,"rdfs:subClassOf",lx=160,ly=108,lanchor="start"); f.arrow(610,130,610,76,"rdfs:subClassOf",lx=600,ly=108,lanchor="end")
f.arrow(240,152,520,152,"ex:suppliedBy",ly=144); f.text(380,172,"domain: Part / range: Supplier",12.5,MUTED,"middle")
f.box(60,215,640,44,None,(),KR,dashed=True); f.text(380,243,"ex:ProcuredItem ＝ ex:suppliedBy の値に Supplier を 1 つ以上持つもの（OWL）",14,INK,"middle")
f.text(60,285,"実線は RDF Schema で書ける範囲。破線は OWL で加える論理的な定義。",13,MUTED)
f.save("el-rdfs-owl.svg")
# 6 SKOS
f=Fig(760,230,"SKOS の例")
f.box(250,30,260,62,"締結部品",["prefLabel: 締結部品 / fastener"],WEB)
f.box(250,140,260,82,"ボルト",["prefLabel: ボルト / bolt","altLabel: ボルト類"],WEB)
f.arrow(380,140,380,94,"skos:broader（上位）",lx=392,ly=122,lanchor="start")
f.text(30,60,"用語の階層と",13,MUTED); f.text(30,80,"言語ごとの表記を管理する。",13,MUTED)
f.text(30,180,"論理的な定義までは",13,MUTED); f.text(30,200,"書かない。",13,MUTED)
f.save("el-skos.svg")
# 7 SHACL
f=Fig(760,240,"SHACL による検証の流れ")
f.box(30,30,220,70,"データ（RDF）",["検査される側"],WEB); f.box(30,130,220,90,"シェイプ（条件）",["名称は 1 つ以上","供給者は 1 つ以上","重量は 0 より大きい"],WEB)
f.box(330,85,130,70,"検証",(),None)
f.box(540,30,190,70,"適合",["条件をすべて満たす"],WEB); f.box(540,130,190,90,"違反の報告",["どのデータが","どの条件に反したか"],KR)
f.arrow(250,65,330,105); f.arrow(250,175,330,135); f.arrow(460,105,540,65); f.arrow(460,135,540,175)
f.save("el-shacl.svg")
# 8 SPARQL
f=Fig(760,230,"SPARQL の問い合わせの流れ")
f.box(30,40,210,150,"RDF グラフ",["ex:P-100","  suppliedBy ex:S-01","  name 六角ボルト M8","ex:S-01","  name 東和精工"],WEB)
f.box(290,40,210,150,"パターン",["?part suppliedBy ?supplier","?part name ?partName","?supplier name ?supplierName"],WEB)
f.box(550,40,190,150,"結果の表",["partName: 六角ボルト M8","supplierName: 東和精工"],WEB)
f.arrow(240,115,290,115); f.arrow(500,115,550,115)
f.text(30,215,"「?」で始まる変数を含むパターンを書き、グラフの中で当てはまる部分を取り出す。",13,MUTED)
f.save("el-sparql.svg")
# 9 JSON-LD
f=Fig(760,230,"JSON-LD の仕組み")
f.box(30,30,220,80,"ふつうの JSON",['"name": "六角ボルト M8"','"suppliedBy": "ex:S-01"'],WEB,mono=True)
f.box(30,130,220,80,"@context",['"name": "ex:name"','"suppliedBy": "ex:suppliedBy"'],WEB,mono=True)
f.box(330,85,110,70,"読み替え",(),None)
f.box(510,60,230,120,"RDF のトリプル",["ex:P-100 ex:name ...","ex:P-100 ex:suppliedBy ex:S-01"],WEB,mono=True)
f.arrow(250,70,330,105); f.arrow(250,170,330,135); f.arrow(440,120,510,120)
f.save("el-jsonld.svg")
# 10 DCAT
f=Fig(760,250,"DCAT の主なクラス")
f.box(30,40,170,90,"dcat:Catalog",["データの目録","例: データカタログ"],WEB,tsize=14)
f.box(295,40,170,90,"dcat:Dataset",["データのまとまり","例: 部品マスタ"],WEB,tsize=14)
f.box(560,40,180,90,"dcat:Distribution",["入手できる形と場所","例: CSV、URL"],WEB,tsize=14)
f.arrow(200,85,295,85); f.arrow(465,85,560,85)
f.text(247,74,"dataset",12,MUTED,"middle"); f.text(512,74,"distribution",12,MUTED,"middle")
f.box(285,180,190,50,"データモデル",(),None,dashed=True,tsize=14); f.arrow(380,130,380,180,"dcterms:conformsTo",lx=392,ly=160,lanchor="start")
f.save("el-dcat.svg")
# 11 セマンティックレイヤ
f=Fig(760,300,"セマンティックレイヤの位置")
for i,t in enumerate(["BI ダッシュボード","SQL、ノートブック","AI エージェント"]): f.box(60+i*220,20,200,46,t,(),None,tsize=14)
f.box(60,110,640,80,"セマンティックレイヤ",["指標（例: 部品点数）、ディメンション、表どうしの結合を一度だけ定義する"],BI)
for i,t in enumerate(["part 表","supplier 表","発注明細 表"]): f.box(60+i*220,235,200,46,t,(),DB,tsize=14)
for i in range(3): f.arrow(160+i*220,110,160+i*220,68); f.arrow(160+i*220,235,160+i*220,192)
f.save("el-semantic-layer.svg")
# 12 Ossie
f=Fig(760,295,"Apache Ossie による定義の交換")
f.box(270,90,220,90,"Ossie の文書",["YAML または JSON","データセット、関係、指標"],BI)
for (x,y,t) in [(30,30,"BI ツール A"),(30,190,"BI ツール B"),(550,30,"データ基盤"),(550,190,"AI エージェント")]: f.box(x,y,180,50,t,(),None,tsize=14)
f.arrow(210,62,270,105,both=True); f.arrow(210,210,270,165,both=True); f.arrow(550,62,490,105,both=True); f.arrow(550,210,490,165,both=True)
f.text(380,278,"各ツールが独自形式で持つ定義を、共通の形式に書き出して受け渡す。",13,MUTED,"middle")
f.save("el-ossie.svg")
# 13 上位オントロジー
f=Fig(760,270,"上位、中位、領域オントロジーの重なり")
f.box(230,20,300,56,"上位オントロジー",["例: BFO"],KR)
f.box(150,100,460,56,"中位オントロジー",["例: Common Core Ontologies"],KR)
f.box(40,180,680,56,"領域オントロジー",["例: 金融、生命科学、製造などの分野ごとのオントロジー"],KR)
f.arrow(380,100,380,78); f.arrow(380,180,380,158)
f.text(40,258,"上位ほど一般的で、領域に依存しない。下の層は上の層の用語を特殊化して使う。",13,MUTED)
f.save("el-upper-ontology.svg")
# 14 知識グラフと GraphRAG
f=Fig(760,210,"知識グラフと GraphRAG の流れ")
f.box(20,50,150,80,"文書",["報告書、記録など"],None)
f.box(215,50,150,80,"抽出",["言語モデルが","事物と関係を取り出す"],None)
f.box(410,50,150,80,"知識グラフ",["事物と関係の網"],KR)
f.box(605,50,140,80,"回答",["グラフを手がかりに","言語モデルが答える"],None)
f.arrow(170,90,215,90); f.arrow(365,90,410,90); f.arrow(560,90,605,90)
f.text(20,180,"知識グラフは、事物を点、関係を線として持つデータの網である。",13,MUTED)
f.save("el-knowledge-graph.svg")
# 0 導入: 同じものを別の名前で呼ぶ問題
f=Fig(760,312,"同じものを別の名前で呼ぶ問題と、共通の語彙による対応づけ")
for i,(co,col) in enumerate([("A 社の表","supplier_id"),("B 社の表","仕入先コード"),("C 社の表","vendor")]):
    f.box(30,20+i*92,210,70,co,[col],None)
f.box(300,92,160,70,"対応づけ",(),None)
f.box(520,72,210,110,"共通の語彙",["ex:suppliedBy","「部品の供給者」","という意味を一度だけ定義"],WEB)
for i in range(3): f.arrow(240,55+i*92,300,127)
f.arrow(460,127,520,127)
f.text(30,302,"列の名前は会社ごとに違っても、指しているものが同じだと機械に分かるようにする。",13,MUTED)
f.save("el-intro.svg")
# 15 Cyc: 常識の知識から推論する（例示）
f=Fig(760,250,"常識の知識を書き下して推論する考え方")
f.box(30,30,250,62,"知識 1",["ボルトは物体である"],KR); f.box(30,120,250,62,"知識 2",["物体には重さがある"],KR)
f.box(340,75,120,62,"推論",(),None); f.box(520,75,210,62,"導かれる知識",["ボルトには重さがある"],KR)
f.arrow(280,61,340,96); f.arrow(280,151,340,116); f.arrow(460,106,520,106)
f.text(30,230,"筆者が作成した例であり、Cyc の実際の記述ではない。人には当然の知識を明示的に書いておく。",13,MUTED)
f.save("el-cyc.svg")
# 16 記述論理: 定義から自動で分類する
f=Fig(760,260,"記述論理による自動分類")
f.box(30,30,330,80,"定義",["調達品 ＝","供給者を 1 つ以上持つもの"],KR)
f.box(30,140,330,80,"データ",["P-100 の供給者は S-01 である","S-01 は供給者である"],None)
f.box(420,85,120,62,"分類",(),None); f.box(590,85,150,62,"結果",["P-100 は調達品"],KR)
f.arrow(360,70,420,106); f.arrow(360,180,420,126); f.arrow(540,116,590,116)
f.text(30,248,"「調達品である」とはどこにも書いていないが、定義から計算で導ける。",13,MUTED)
f.save("el-dl.svg")
# 17 RDF Schema: 宣言から型を推論する
f=Fig(760,260,"RDF Schema による推論")
f.box(30,30,330,80,"宣言（RDF Schema）",["ex:suppliedBy の主語は ex:Part","ex:suppliedBy の目的語は ex:Supplier"],WEB,mono=False)
f.box(30,140,330,80,"データ（RDF）",["ex:P-100 ex:suppliedBy ex:S-01"],WEB)
f.box(420,85,120,62,"推論",(),None); f.box(590,70,150,92,"導かれる文",["P-100 は Part","S-01 は Supplier"],WEB)
f.arrow(360,70,420,106); f.arrow(360,180,420,126); f.arrow(540,116,590,116)
f.text(30,248,"宣言はデータを拒否するためではなく、書かれていない事実を補うために使われる。",13,MUTED)
f.save("el-rdfs.svg")
# 18 XML Schema / JSON Schema: 文書の形を検査する
f=Fig(760,270,"スキーマによる文書の検査")
f.box(30,30,300,80,"文書 1",['part_id: "P-100"、name、supplier_id'],None)
f.box(30,150,300,80,"文書 2",['part_id: "100"、name のみ'],None)
f.box(390,90,140,80,"スキーマ",["必須の項目","値の型と形式"],WEB)
f.box(590,30,150,80,"適合",["条件をすべて満たす"],WEB); f.box(590,150,150,80,"不適合",["番号の形式が違う","供給者がない"],KR)
f.arrow(330,70,390,115); f.arrow(330,190,390,145); f.arrow(530,115,590,70); f.arrow(530,145,590,190)
f.text(30,258,"項目と型がそろっているかは検査できるが、項目の意味は扱わない。",13,MUTED)
f.save("el-schema.svg")
# 19 schema.org: Web ページに意味を添える
f=Fig(760,250,"schema.org による構造化データの読み取り")
f.box(30,30,300,170,"Web ページ",["人が読む本文","「六角ボルト M8 を販売…」","","機械向けの注記","種類: Product","名前: 六角ボルト M8"],None)
f.box(400,85,140,62,"検索エンジン",(),None)
f.box(600,60,140,112,"理解した内容",["製品のページ","名前が分かる"],WEB)
f.arrow(330,116,400,116); f.arrow(540,116,600,116)
f.text(30,236,"ページに共通の語彙で注記を添えると、検索エンジンが内容の種類と属性を読み取れる。",13,MUTED)
f.save("el-schemaorg.svg")
# 意味の 4 段階: 2 段目から 4 段目は積み上がる。1 段目の検査は独立している
f=Fig(760,350,"意味の 4 段階。機械が意味についてできることが、段を上がるごとに増える")
STEPS=[("1","形を検査できる","JSON Schema など","#dcefe8"),
       ("2","同じものだと分かる","RDF と共有語彙","#b9e0d1"),
       ("3","用語の関係をたどれる","SKOS","#8fcfb7"),
       ("4","定義から導ける","RDF Schema、OWL","#5fbc9a")]
BASE=290
for i,(n,title,tech,fill) in enumerate(STEPS):
    x=30+i*178; top=BASE-80-i*62
    f.o.append(f'<rect x="{x}" y="{top}" width="170" height="{BASE-top}" fill="{fill}" stroke="{WEB}" stroke-width="1.5"/>')
    f.text(x+12,top+24,f"{n} 段目",12.5,INK)
    f.text(x+12,top+46,title,14.5,INK,"start",True)
    f.text(x+12,top+68,tech,12.5,INK)
f.o.append(f'<line x1="20" y1="{BASE}" x2="750" y2="{BASE}" stroke="#52606d" stroke-width="1.5"/>')
f.arrow(30,BASE+28,730,BASE+28)
f.text(380,BASE+50,"機械に渡す意味が増える",13,MUTED,"middle")
f.save("el-ladder.svg")
# 一つの段に収まらない技術と、段との関係
f=Fig(760,504,"一つの段に収まらない技術と、各段との関係")
BASE=335
S2=[("1","形を検査","できる","#dcefe8"),("2","同じものだと","分かる","#b9e0d1"),("3","用語の関係を","たどれる","#8fcfb7"),("4","定義から","導ける","#5fbc9a")]
cx=[]
for i,(n,l1,l2,fill) in enumerate(S2):
    x=150+i*118; top=BASE-64-i*44
    f.o.append(f'<rect x="{x}" y="{top}" width="112" height="{BASE-top}" fill="{fill}" stroke="{WEB}" stroke-width="1.5"/>')
    f.text(x+56,top+20,f"{n} 段目",12,INK,"middle"); f.text(x+56,top+39,l1,13,INK,"middle",True); f.text(x+56,top+56,l2,13,INK,"middle",True)
    cx.append((x+56,top))
f.o.append(f'<line x1="140" y1="{BASE}" x2="632" y2="{BASE}" stroke="#52606d" stroke-width="1.5"/>')
# 外にある技術（破線の箱）と、関係する段への線
f.box(20,20,250,74,"DCAT、ダブリンコア",["データそのものではなく、","データについての情報を書く"],DB,dashed=True,tsize=14)
f.arrow(200,94,cx[1][0]-20,cx[1][1]-2,dashed=True); f.text(150,150,"2 段目の仕組みを使う",12.5,INK,"middle")
f.box(290,14,290,96,"Palantir の Ontology",["独自の形式で 1、2 段目に相当。3 段目は一部","4 段目にあたる推論は見当たらない","業務上の操作と結びつける"],KR,dashed=True,tsize=14)
f.arrow(340,110,cx[1][0]+14,cx[1][1]-2,dashed=True); f.text(332,172,"相当",12.5,INK,"end")
f.arrow(452,110,cx[2][0]+6,cx[2][1]-2,dashed=True); f.text(460,150,"一部",12.5,INK,"start")
# 下の列: SHACL（1 段目の横）、セマンティックレイヤ（1 段目の下）、OKF（1 から 3 段目の下）
f.box(10,392,200,74,"SHACL",["グラフの形のデータを検査","役割は 1 段目と同じ"],WEB,dashed=True,tsize=14)
f.arrow(110,392,cx[0][0]-58,BASE-30,dashed=True)
f.box(222,392,266,74,"セマンティックレイヤ、Apache Ossie",["集計の計算方法をそろえる","1 段目の表の上に定義する"],BI,dashed=True,tsize=14)
f.arrow(300,392,cx[0][0]+14,BASE+2,dashed=True)
f.box(500,392,250,74,"OKF",["1 段目は最小限、2 段目は一部","3 段目はごく一部。残りは文章で渡す"],KR,dashed=True,tsize=14)
f.arrow(520,392,cx[0][0]+44,BASE+2,dashed=True)
f.arrow(560,392,cx[1][0]+16,BASE+2,dashed=True)
f.arrow(600,392,cx[2][0]+18,BASE+2,dashed=True)
f.text(20,490,"またがる: Palantir、OKF　　同じ役割を担う: SHACL　　別の軸にある: DCAT、セマンティックレイヤ",12.5,MUTED)
f.save("el-off-ladder.svg")
# 意味の 4 段階と、四本の流れの対応。段の色は、その段を担う流れを表す
f=Fig(760,480,"意味の 4 段階と四本の流れの対応")
BASE=340
ST=[("1","形を検査できる",DB),("2","同じものだと分かる",WEB),("3","用語の関係をたどれる",WEB),("4","定義から導ける",WEB)]
for i,(n,title,col) in enumerate(ST):
    x=150+i*150; top=BASE-70-i*52
    f.o.append(f'<rect x="{x}" y="{top}" width="143" height="{BASE-top}" fill="{TINT[col]}" stroke="{col}" stroke-width="2"/>')
    f.text(x+72,top+22,f"{n} 段目",12.5,MUTED,"middle"); f.text(x+72,top+43,title,13,INK,"middle",True)
f.o.append(f'<line x1="140" y1="{BASE}" x2="752" y2="{BASE}" stroke="#52606d" stroke-width="1.5"/>')
# 流れの名前を段の下に置く
f.text(222,BASE+24,"データベース系",13.5,DB,"middle",True)
f.o.append(f'<line x1="304" y1="{BASE+14}" x2="742" y2="{BASE+14}" stroke="{WEB}" stroke-width="2"/>')
f.text(523,BASE+34,"Web 標準系",13.5,WEB,"middle",True)
# 知識表現系: 4 段目の理論を支える
f.box(560,16,190,62,"知識表現系",["4 段目の理論を支える"],KR,tsize=14)
f.arrow(655,78,672,BASE-70-3*52-3)
# 分析系: 別の軸にある
f.box(20,402,300,62,"分析系",["別の軸。1 段目の表の上に指標を定義する"],BI,dashed=True,tsize=14)
f.arrow(170,402,205,BASE+30,dashed=True)
f.text(350,452,"色は流れを表す。破線は別の軸にあることを表す。",12.5,MUTED)
f.save("el-ladder-streams.svg")
# データスペースプロトコルと ODS が、意味の 4 段階のどこを規範に置くか
f=Fig(760,470,"データスペースプロトコルと ODS が規範に置く段")
BASE=250; X0=170; SW=140
ST=[("1","形を検査できる","#dcefe8"),("2","同じものだと分かる","#b9e0d1"),("3","用語の関係をたどれる","#8fcfb7"),("4","定義から導ける","#5fbc9a")]
for i,(n,title,fill) in enumerate(ST):
    x=X0+i*SW; top=BASE-66-i*44
    f.o.append(f'<rect x="{x}" y="{top}" width="{SW-8}" height="{BASE-top}" fill="{fill}" stroke="{WEB}" stroke-width="1.5"/>')
    f.text(x+(SW-8)/2,top+22,f"{n} 段目",12.5,INK,"middle"); f.text(x+(SW-8)/2,top+43,title,12,INK,"middle",True)
f.o.append(f'<line x1="{X0-10}" y1="{BASE}" x2="{X0+4*SW}" y2="{BASE}" stroke="#52606d" stroke-width="1.5"/>')
def cell(i,y,kind,l1,l2=""):
    x=X0+i*SW; w=SW-8
    if kind=="norm":   style=f'fill="{INK}" stroke="{INK}" stroke-width="1.5"'; col="#ffffff"
    elif kind=="ref":  style=f'fill="#ffffff" stroke="{INK}" stroke-width="1.5"'; col=INK
    elif kind=="opt":  style=f'fill="#ffffff" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 4"'; col=INK
    elif kind=="des":  style=f'fill="#cbd2d9" stroke="{INK}" stroke-width="1.5"'; col=INK
    else:              style=f'fill="#f6f8fa" stroke="{LINE}" stroke-width="1"'; col=MUTED
    f.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="6" {style}/>')
    f.o.append(f'<text x="{x+w/2}" y="{y+(25 if l2 else 34)}" font-size="13" fill="{col}" text-anchor="middle" font-weight="700">{l1}</text>')
    if l2: f.o.append(f'<text x="{x+w/2}" y="{y+44}" font-size="11.5" fill="{col}" text-anchor="middle">{l2}</text>')
Y1,Y2=278,348
f.text(X0-18,Y1+26,"データスペース",13,INK,"end",True); f.text(X0-18,Y1+44,"プロトコル 2025-1",12.5,INK,"end")
f.text(X0-18,Y2+26,"ODS",13,INK,"end",True); f.text(X0-18,Y2+44,"（日本）",12.5,INK,"end")
cell(0,Y1,"norm","規範","JSON Schema"); cell(1,Y1,"ref","語彙を再利用","DCAT、ODRL"); cell(2,Y1,"none","規定なし"); cell(3,Y1,"none","規定なし")
cell(0,Y2,"opt","選択的に導入","閉世界的な検証"); cell(1,Y2,"norm","規範","RDF"); cell(2,Y2,"none","確認できず"); cell(3,Y2,"des","設計思想で採用","OWL")
# 凡例
lx=X0; ly=432
for k,(kind,lab) in enumerate([("norm","規範に置く"),("ref","語彙を再利用"),("des","設計思想で採用"),("opt","選択的に導入")]):
    x=lx+k*150
    if kind=="norm": st=f'fill="{INK}" stroke="{INK}"'
    elif kind=="des": st=f'fill="#cbd2d9" stroke="{INK}"'
    elif kind=="ref": st=f'fill="#ffffff" stroke="{INK}"'
    else: st=f'fill="#ffffff" stroke="{INK}" stroke-dasharray="5 3"'
    f.o.append(f'<rect x="{x}" y="{ly}" width="26" height="16" rx="3" {st} stroke-width="1.5"/>'); f.text(x+34,ly+13,lab,12.5,MUTED)
f.save("el-dsp-ods.svg")
# 意味の三角形（Ogden と Richards 1923 をもとに作成）に、四つの言葉を重ねる
f=Fig(760,470,"意味の三角形と四つの言葉")
TOP=(380,70); L=(150,330); R=(610,330)
f.o.append(f'<line x1="{L[0]+60}" y1="{L[1]-34}" x2="{TOP[0]-50}" y2="{TOP[1]+44}" stroke="#52606d" stroke-width="1.8"/>')
f.o.append(f'<line x1="{TOP[0]+50}" y1="{TOP[1]+44}" x2="{R[0]-60}" y2="{R[1]-34}" stroke="#52606d" stroke-width="1.8"/>')
f.o.append(f'<line x1="{L[0]+112}" y1="{L[1]}" x2="{R[0]-112}" y2="{R[1]}" stroke="#52606d" stroke-width="1.8" stroke-dasharray="6 5"/>')
f.box(TOP[0]-110,TOP[1]-44,220,88,"概念",["「部品を供給する会社」","という考え"],KR)
f.text(TOP[0]-120,TOP[1]-26,"原典:",11,MUTED,"end"); f.text(TOP[0]-120,TOP[1]-11,"Thought or Reference",11,MUTED,"end")
f.box(L[0]-110,L[1]-44,220,88,"記号",["列の名前 supplier_id","値 S-01"],DB)
f.text(L[0],L[1]-52,"原典: Symbol",11,MUTED,"middle")
f.box(R[0]-110,R[1]-44,220,88,"対象",["実在する会社","東和精工"],None)
f.text(R[0],R[1]-52,"原典: Referent",11,MUTED,"middle")
f.text(232,196,"表す",13,INK,"end"); f.text(528,196,"指す",13,INK,"start")
f.text(380,322,"直接にはつながらない",13,MUTED,"middle")
# 四つの言葉の位置づけ
f.text(L[0],L[1]+68,"データモデル",14,DB,"middle",True); f.text(L[0],L[1]+88,"記号の並べ方を決める",12.5,MUTED,"middle")
f.text(TOP[0]+130,TOP[1]-14,"オントロジー",14,KR,"start",True); f.text(TOP[0]+130,TOP[1]+6,"概念と、その関係を",12.5,MUTED,"start"); f.text(TOP[0]+130,TOP[1]+24,"明示的に書き表す",12.5,MUTED,"start")
f.text(92,170,"セマンティクス",14,WEB,"middle",True); f.text(92,190,"記号が何を表し、",12.5,MUTED,"middle"); f.text(92,208,"何を指すかの対応",12.5,MUTED,"middle")
f.o.append(f'<rect x="14" y="14" width="732" height="424" rx="10" fill="none" stroke="{BI}" stroke-width="1.5" stroke-dasharray="3 5"/>')
f.text(732,456,"標準化: この対応を、組織をまたいでそろえる",13,BI,"end",True)
f.save("el-triangle.svg")

# 意味の指定の強さによる連続体（Uschold と Gruninger 2004 の図をもとに作成）
# 意味の 4 段階（緑の階段）と見分けがつくよう、灰色の横一列の帯として描く
f=Fig(760,230,"意味の指定の強さによる連続体")
f.arrow(30,150,730,150)
f.text(30,178,"意味の指定が少ない",12.5,MUTED,"start"); f.text(730,178,"意味の指定が多く、形式的",12.5,MUTED,"end")
GX=[30,205,380,555]; GW=168
GR=[("用語集、データ辞書",["用語の一覧","自然言語による説明"]),("シソーラス、分類",["広い語と狭い語","言い換え"]),("スキーマ、データモデル",["DB や XML のスキーマ","UML などのデータモデル"]),("形式的なオントロジー",["記述論理（OWL）","一般の論理"])]
for (t,ls),x in zip(GR,GX):
    f.o.append(f'<rect x="{x}" y="30" width="{GW}" height="92" rx="4" fill="#f6f8fa" stroke="{LINE}" stroke-width="1.2"/>')
    f.text(x+GW/2,56,t,13.5,INK,"middle",True)
    for k,l in enumerate(ls): f.text(x+GW/2,80+k*19,l,12.5,MUTED,"middle")
    f.o.append(f'<line x1="{x+GW/2}" y1="122" x2="{x+GW/2}" y2="150" stroke="{LINE}" stroke-width="1.2"/>')
f.text(30,212,"成果物の種類を、意味をどれだけ形式的に指定するかの順に並べたもの。",12.5,MUTED)
f.save("el-spectrum.svg")

# Palantir の公式文書の図（航空業界の例）をもとに作成
f=Fig(760,470,"Palantir の Ontology の例。航空業界のオブジェクト型とリンク型")
def ot(x,y,name,obj,props): f.box(x,y,200,84,name,[obj,props],KR,tsize=14)
ot(280,16,"空港（Airport）","例: JFK","開港日、発着能力、緯度経度")
ot(280,178,"フライト（Flight）","例: JFK 発 SFO 行","出発、到着、乗客数")
ot(20,178,"遅延（Delay）","例: 38 分の遅延","時間、発着の別、原因")
ot(540,178,"航空会社（Airline）","例: Skybourne Airlines","本社、設立日、航空連合")
ot(280,340,"機材（Aircraft）","例: Boeing 747","就航日、座席数、航続距離")
f.arrow(360,178,360,102); f.text(352,146,"出発地",12.5,INK,"end")
f.arrow(400,178,400,102); f.text(408,146,"到着地",12.5,INK,"start")
f.arrow(280,220,222,220); f.text(251,210,"遅延",12.5,INK,"middle")
f.arrow(480,220,538,220); f.text(509,210,"運航会社",12.5,INK,"middle")
f.arrow(380,262,380,338); f.text(388,304,"使用機材",12.5,INK,"start")
f.arrow(482,74,600,176); f.text(556,116,"ハブ空港",12.5,INK,"start")
f.arrow(482,374,600,264); f.text(556,332,"所有会社",12.5,INK,"start")
f.text(20,454,"箱がオブジェクト型、矢印がリンク型である。各箱の 3 行目はプロパティの例。",12.5,MUTED)
f.save("el-palantir.svg")
# 意味の三角形の上に、意味の 4 段階を重ねる
f=Fig(760,450,"意味の三角形と意味の 4 段階の対応")
TOP=(380,96); L=(170,340); R=(590,340)
f.o.append(f'<line x1="{L[0]+50}" y1="{L[1]-40}" x2="{TOP[0]-60}" y2="{TOP[1]+44}" stroke="{WEB}" stroke-width="4"/>')
f.o.append(f'<line x1="{TOP[0]+60}" y1="{TOP[1]+44}" x2="{R[0]-50}" y2="{R[1]-40}" stroke="#9aa5b1" stroke-width="1.8" stroke-dasharray="6 5"/>')
f.o.append(f'<line x1="{L[0]+104}" y1="{L[1]}" x2="{R[0]-104}" y2="{R[1]}" stroke="#9aa5b1" stroke-width="1.8" stroke-dasharray="6 5"/>')
f.box(TOP[0]-120,TOP[1]-44,240,88,"概念",["「部品を供給する会社」","という考え"],KR)
f.box(L[0]-100,L[1]-40,200,80,"記号",["supplier_id、S-01"],DB)
f.box(R[0]-100,R[1]-40,200,80,"対象",["実在する会社"],None)
def badge(cx,cy,n):
    f.o.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{INK}"/>'); f.text(cx,cy+5,str(n),14,"#ffffff","middle",True)
badge(L[0]-100,L[1]-40,1); f.text(L[0]-100,L[1]+64,"1 段目: 形を検査できる",13,INK,"start",True); f.text(L[0]-100,L[1]+83,"記号の形だけを決める",12.5,MUTED,"start")
badge(250,214,2); f.text(232,200,"2 段目: 同じものだと分かる",13,INK,"end",True); f.text(232,219,"記号がどの概念を表すかを",12.5,MUTED,"end"); f.text(232,237,"共通の識別子で固定する",12.5,MUTED,"end")
badge(TOP[0]-120,TOP[1]-44,3); badge(TOP[0]+120,TOP[1]-44,4)
f.text(TOP[0]-134,TOP[1]-64,"3 段目: 用語の関係をたどれる",13,INK,"end",True); f.text(TOP[0]-134,TOP[1]-45,"概念どうしの広い狭いを書く",12.5,MUTED,"end")
f.text(TOP[0]+142,TOP[1]-64,"4 段目: 定義から導ける",13,INK,"start",True); f.text(TOP[0]+142,TOP[1]-45,"概念の定義を書き、推論する",12.5,MUTED,"start")
f.text(532,214,"どの段でも、機械には渡らない",12.5,MUTED,"start"); f.text(532,232,"（記録が現実と合っているか）",12.5,MUTED,"start")
f.save("el-triangle-steps.svg")
# 11 章: 意味の 4 段階 × 共有の範囲 の見取り図
f=Fig(760,520,"意味の 4 段階と共有の範囲による見取り図")
NX=16; CX=[188,328,468,608]; CW=136
HD=["1 形を検査できる","2 同じものだと分かる","3 用語の関係をたどれる","4 定義から導ける"]
f.text(NX,30,"意味の 4 段階",12.5,MUTED,"start")
for x,h in zip(CX,HD):
    f.o.append(f'<rect x="{x}" y="14" width="{CW}" height="28" rx="4" fill="#f6f8fa" stroke="{LINE}" stroke-width="1"/>'); f.text(x+CW/2,33,h,12,INK,"middle",True)
def strip(y,t):
    f.o.append(f'<rect x="{NX}" y="{y}" width="728" height="24" rx="4" fill="{INK}"/>'); f.text(NX+10,y+17,t,13,"#ffffff","start",True)
def row(y,name,sub,col,cells):
    f.text(NX,y+17,name,13,INK,"start",True); f.text(NX,y+34,sub,11.5,MUTED,"start")
    for i,(kind,t) in cells.items():
        x=CX[i-1]
        if kind=="s": f.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="40" rx="6" fill="{TINT.get(col,"#e4e7eb")}" stroke="{col}" stroke-width="2"/>')
        else: f.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="40" rx="6" fill="#ffffff" stroke="{col}" stroke-width="1.5" stroke-dasharray="5 4"/>')
        ls=t.split("|"); y0=y+25 if len(ls)==1 else y+17
        for k,l in enumerate(ls): f.text(x+CW/2,y0+k*16,l,12,INK,"middle")
G="#52606d"
strip(54,"組織をまたいで共有する")
row(88,"Web 標準","W3C の勧告",WEB,{1:("s","XML Schema、SHACL"),2:("s","RDF"),3:("s","SKOS"),4:("s","RDF Schema、OWL")})
row(138,"データスペースプロトコル","国際。Eclipse、2025-1",G,{1:("s","JSON Schema|規範"),2:("d","DCAT、ODRL|再利用")})
row(188,"ODS","日本",G,{1:("d","検証|選択的に導入"),2:("s","RDF|規範"),4:("d","OWL|設計思想で採用")})
row(238,"Open Knowledge Format","Google Cloud、0.2 版",BI,{1:("s","前書きの検査|最小限"),2:("d","資産の URI|一部"),3:("d","種類のないリンク|ごく一部")})
strip(296,"一つの組織、一つの基盤の中でそろえる")
row(330,"データベース","関係モデルなど",DB,{1:("s","表、列、キー")})
row(380,"セマンティックレイヤ","分析系。Apache Ossie",BI,{1:("d","別の軸。表の上に|指標の定義を置く")})
row(430,"Palantir の Ontology","製品独自の形式",KR,{1:("s","備える"),2:("s","備える|一つの基盤の中"),3:("d","一部|型の継承")})
f.o.append(f'<rect x="{NX}" y="488" width="26" height="16" rx="3" fill="#e4e7eb" stroke="{G}" stroke-width="2"/>'); f.text(NX+34,501,"規範に置く、または備える",12,MUTED)
f.o.append(f'<rect x="250" y="488" width="26" height="16" rx="3" fill="#ffffff" stroke="{G}" stroke-width="1.5" stroke-dasharray="5 4"/>'); f.text(284,501,"再利用、設計思想での採用、選択的な導入、一部、別の軸",12,MUTED)
f.save("el-map.svg")
# 分析系のコラム: 二本の流れの順序と接近
f=Fig(760,376,"分析系と Web 標準系の順序と接近")
SL=[1991,1999,2004,2009,2017,2021,2025,2026]; X0=150; DX=80
xs={y:X0+i*DX for i,y in enumerate(SL)}
YW,YB=110,250
# 2025 年以降の出来事の集中を示す帯
f.o.append(f'<rect x="{xs[2025]-34}" y="{YB-28}" width="{DX+72}" height="96" rx="8" fill="{TINT[BI]}" stroke="{BI}" stroke-width="1" stroke-dasharray="4 4"/>')
f.text(xs[2026]+38,YB+88,"約 10 か月に七つの出来事",12.5,BI,"end",True)
f.text(20,YW+5,"Web 標準系",14,WEB,"start",True); f.text(20,YB+5,"分析系",14,BI,"start",True)
f.o.append(f'<line x1="{xs[1999]}" y1="{YW}" x2="{xs[2026]+30}" y2="{YW}" stroke="{WEB}" stroke-width="3"/>')
f.o.append(f'<line x1="{xs[1991]}" y1="{YB}" x2="{xs[2026]+30}" y2="{YB}" stroke="{BI}" stroke-width="3"/>')
def ev(year,y,col,ls,up):
    x=xs[year]; f.o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#ffffff" stroke="{col}" stroke-width="2.5"/>')
    f.text(x,y-16 if up else y+26,f"{year} 年",12.5,INK,"middle",True)
    for k,l in enumerate(ls):
        f.text(x,(y-34-(len(ls)-1-k)*16) if up else (y+44+k*16),l,12,MUTED,"middle")
ev(1999,YW,WEB,["RDF"],True); ev(2004,YW,WEB,["OWL"],True); ev(2009,YW,WEB,["SKOS"],True); ev(2017,YW,WEB,["SHACL"],True)
ev(1991,YB,BI,["Business Objects","の特許"],False); ev(2021,YB,BI,["指標の層","の提唱"],False); ev(2025,YB,BI,["OSI の発表"],False); ev(2026,YB,BI,["Apache Ossie"],False)
f.o.append(f'<line x1="{xs[1991]}" y1="{YB-12}" x2="{xs[1991]}" y2="{YW}" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="4 4"/>')
f.o.append(f'<line x1="{xs[1991]}" y1="{YW}" x2="{xs[1999]-10}" y2="{YW}" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="4 4"/>')
f.text(xs[1991]+8,YW+24,"分析系の起点が先",12.5,INK,"start")
f.arrow(xs[2026],YB-10,xs[2026],YW+12)
f.text(xs[2026]-10,176,"オントロジー仕様が",12.5,INK,"end"); f.text(xs[2026]-10,193,"RDF、OWL の語彙に関連づく",12.5,INK,"end")
f.text(xs[2025],YB-12,"2021 年以降の課題: 指標の定義をそろえる",12.5,BI,"end")
f.text(xs[1991]+12,YB-12,"業務の言葉で問い合わせる",12.5,BI,"start")
f.text(20,362,"横軸は出来事の順序を示す。間隔は年数に比例しない。",12,MUTED)
f.save("el-two-streams.svg")

# データスペースプロトコルの成り立ち: 規範の置き方の移り変わり
f=Fig(760,330,"規範の置き方の移り変わり")
BX=[20,280,530]; BW=[210,210,210]
f.text(BX[0],26,"IDSA の先行する別の仕様",12.5,MUTED); f.text(BX[1],26,"データスペースプロトコル",12.5,MUTED)
f.o.append(f'<line x1="255" y1="14" x2="255" y2="232" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="5 4"/>')
f.box(BX[0],40,BW[0],96,"IDS-RAM 4.0",["規範: オントロジー","（IDS 語彙）"],WEB)
f.box(BX[1],40,BW[1],96,"2024-1 版",["必須: JSON-LD のコンパクト形式","スキーマは添付。規範ではない"],None)
f.box(BX[2],40,BW[2],96,"2025-1 版",["規範: JSON Schema","JSON-LD の処理は任意"],DB)
f.arrow(BX[1]+BW[1]+4,88,BX[2]-4,88)
f.text(BX[0],166,"意味の 4 段階でいうと",13,INK,"start",True)
def pill(x,w,t,col,fill): f.o.append(f'<rect x="{x}" y="180" width="{w}" height="40" rx="20" fill="{fill}" stroke="{col}" stroke-width="1.5"/>'); f.text(x+w/2,205,t,13,INK,"middle")
pill(BX[0],BW[0],"2 段目以上の仕組み",WEB,TINT[WEB]); pill(BX[1],BW[1],"2 段目の仕組みが必須",LINE,"#f6f8fa"); pill(BX[2],BW[2],"1 段目の検査",DB,TINT[DB])
f.text(20,262,"変わったのは、実装に何を求めるかである。",12.5,MUTED)
f.text(20,282,"語彙は名前空間として残っており、JSON-LD として処理すれば RDF として扱える。",12.5,MUTED)
f.text(20,312,"データスペースプロトコルが IDS のオントロジーを基にしたという記述は、見つかっていない。",12.5,MUTED)
f.save("el-dsp-norm.svg")

# 欧州相互運用性フレームワークの相互運用性モデル（同文書の図 3 をもとに作成）
f=Fig(760,330,"欧州相互運用性フレームワークの相互運用性モデル")
f.o.append(f'<rect x="20" y="16" width="470" height="264" rx="8" fill="#f6f8fa" stroke="{LINE}" stroke-width="1.5"/>')
f.text(34,40,"相互運用性のガバナンス",13.5,INK,"start",True); f.text(34,58,"Interoperability Governance",11.5,MUTED)
LY=[("法的な相互運用性","Legal"),("組織的な相互運用性","Organisational"),("意味的な相互運用性","Semantic"),("技術的な相互運用性","Technical")]
for i,(a,b2) in enumerate(LY):
    y=72+i*50; hot=(i==2)
    f.o.append(f'<rect x="40" y="{y}" width="290" height="40" rx="6" fill="{TINT[WEB] if hot else "#ffffff"}" stroke="{WEB if hot else LINE}" stroke-width="{2.5 if hot else 1.2}"/>')
    f.text(54,y+25,a,14,INK,"start",hot); f.text(318,y+25,b2,11.5,MUTED,"end")
f.o.append(f'<rect x="342" y="72" width="134" height="190" rx="6" fill="{TINT[DB]}" stroke="{DB}" stroke-width="1.5"/>')
for k,l in enumerate(["統合された","公共サービスの","ガバナンス"]): f.text(409,138+k*19,l,13,INK,"middle",True)
for k,l in enumerate(["Integrated Public","Service Governance"]): f.text(409,206+k*15,l,11,MUTED,"middle")
f.text(510,150,"意味的な相互運用性とは",13,WEB,"start",True)
for k,l in enumerate(["交換されるデータと情報の","正確な形式と意味が、","やり取りを通じて保たれ、","理解されること"]): f.text(510,174+k*18,l,12.5,INK,"start")
f.text(510,258,"この報告書が扱う層である",12.5,MUTED,"start")
f.text(20,308,"4 層と、4 層を横断する要素、背景となる層からなる。日本語の名称は筆者の訳である。",12,MUTED)
f.save("el-eif.svg")
# 1 章: なぜ今これが話題になるのか
f=Fig(760,330,"意味の定義が話題になる二つの理由")
f.text(20,28,"理由 1: 組織をまたいでデータを共有する",14,INK,"start",True)
f.box(20,44,120,70,"A 社",["supplier_id"],DB); f.box(230,44,120,70,"B 社",["仕入先コード"],DB)
f.box(110,150,150,62,"共通の意味の定義",["どちらも「供給者」"],WEB)
f.arrow(80,114,150,148); f.arrow(290,114,220,148)
f.text(20,246,"組織の間では、列の名前の意味を",12.5,MUTED); f.text(20,264,"その場ですり合わせられない。",12.5,MUTED)
f.o.append(f'<line x1="378" y1="14" x2="378" y2="290" stroke="{LINE}" stroke-width="1.2" stroke-dasharray="5 4"/>')
f.text(400,28,"理由 2: AI がデータを読む",14,INK,"start",True)
f.box(400,96,130,70,"一つの定義",["指標や規則"],WEB)
for i,t in enumerate(["ダッシュボード","SQL","AI エージェント"]):
    y=48+i*62; f.box(600,y,140,44,None,[],KR if i==2 else None); f.text(670,y+27,t,13.5,INK,"middle",i==2); f.arrow(532,131,598,y+22)
f.text(400,246,"定義がなければ、AI は意味を推測する。",12.5,MUTED); f.text(400,264,"推測は外れることがあり、毎回同じとも限らない。",12.5,MUTED)
f.text(20,314,"どちらも、意味をあらかじめ定義して機械に渡すことを求める。",12.5,INK)
f.save("el-why-now.svg")

# 8 章: ドメインオントロジーと業界標準の見取り図
f=Fig(760,400,"ドメインオントロジーと業界標準の見取り図")
FX=[150,272,394,516,638]; FW=114
for x,t in zip(FX,["金融","生命科学","医療","製造、プロセス産業","行政（米国）"]):
    f.o.append(f'<rect x="{x}" y="14" width="{FW}" height="28" rx="4" fill="#f6f8fa" stroke="{LINE}" stroke-width="1"/>'); f.text(x+FW/2,33,t,12,INK,"middle",True)
RW=[("オントロジー","概念と関係を定義",KR,{0:["FIBO"],1:["Gene Ontology","OBO Foundry"],3:["Industrial","Ontologies Foundry"]}),
    ("用語、製品データ","言葉や項目をそろえる",WEB,{2:["SNOMED CT"],3:["ECLASS"]}),
    ("交換の仕様","やり取りの形を決める",DB,{2:["HL7 FHIR"],3:["アセット管理シェル","CFIHOS"],4:["NIEM"]})]
for r,(a,b2,col,cells) in enumerate(RW):
    y=56+r*72; f.text(16,y+26,a,13,INK,"start",True); f.text(16,y+44,b2,11.5,MUTED,"start")
    for i,ls in cells.items():
        f.o.append(f'<rect x="{FX[i]}" y="{y}" width="{FW}" height="60" rx="6" fill="{TINT[col]}" stroke="{col}" stroke-width="1.5"/>')
        y0=y+35 if len(ls)==1 else y+26
        for k,l in enumerate(ls): f.text(FX[i]+FW/2,y0+k*18,l,11.5,INK,"middle")
f.text(16,296,"分野を問わない",13,INK,"start",True)
f.o.append(f'<rect x="150" y="278" width="602" height="34" rx="6" fill="{TINT[KR]}" stroke="{KR}" stroke-width="1.5"/>'); f.text(451,300,"中位: Common Core Ontologies",13,INK,"middle")
f.o.append(f'<rect x="150" y="320" width="602" height="34" rx="6" fill="{TINT[KR]}" stroke="{KR}" stroke-width="1.5"/>'); f.text(451,342,"上位: BFO（ISO/IEC 21838-2:2021）",13,INK,"middle")
f.text(16,376,"種類の分け方は、各団体の自己記述をもとにした筆者の整理である。",12,MUTED)
f.text(16,393,"SNOMED CT は概念と関係も持ち、オントロジーの行にもまたがる。",12,MUTED)
f.save("el-domain-map.svg")

# 10 章: ODS のオープンソース実装における意味の扱い
f=Fig(760,400,"ODS のオープンソース実装における意味の扱い")
f.text(20,28,"二層のオントロジー（OWL）",14,INK,"start",True)
f.box(20,42,350,66,"ODS オントロジー",["データ交換サービスと接続先を定義する"],WEB)
f.box(390,42,350,66,"領域のオントロジー",["分野の概念を定義する。例: ドローン航路"],WEB)
f.text(20,146,"分散カタログ",14,INK,"start",True)
f.box(20,160,200,62,"ドメインアプリケーション",["SPARQL エンドポイントを公開"],None)
f.box(290,160,170,62,"分散カタログ",["RDF データを収集"],None)
f.box(530,160,210,62,"キャッシュ",["収集したデータを格納し、問い合わせる"],DB)
f.arrow(222,191,288,191); f.arrow(462,191,528,191)
f.text(20,262,"AI との接続",14,INK,"start",True)
f.box(20,276,200,62,"意味定義と API 定義",["SAMM アスペクトモデル"],WEB)
f.box(290,276,170,62,"チャットサーバ",["MCP ツールを生成"],None)
f.box(530,276,210,62,"AI アプリケーション",["MCP ツールを道具として使う"],KR)
f.arrow(222,307,288,307); f.arrow(462,307,528,307)
f.text(20,366,"サンプルの RDF サーバーは、Apache Jena Fuseki に対して SPARQL クエリを実行する。",12.5,MUTED)
f.text(20,386,"各要素の出典は、本文の表に示した。",12.5,MUTED)
f.save("el-ods-oss.svg")
# 7 章: 何をそろえる標準か
f=Fig(760,380,"データモデルとメタデータの標準が、何をそろえるか")
f.o.append(f'<rect x="20" y="16" width="350" height="300" rx="8" fill="#ffffff" stroke="{DB}" stroke-width="1.5"/>')
f.o.append(f'<rect x="390" y="16" width="350" height="300" rx="8" fill="#ffffff" stroke="{WEB}" stroke-width="1.5"/>')
f.text(36,42,"形をそろえる",15,DB,"start",True); f.text(354,42,"1 段目に関係する",12,MUTED,"end")
f.text(406,42,"言葉をそろえる",15,WEB,"start",True); f.text(724,42,"2 段目に関係する",12,MUTED,"end")
def item(x,y,head,ls,col):
    f.o.append(f'<rect x="{x}" y="{y}" width="318" height="{28+len(ls)*19}" rx="6" fill="{TINT[col]}" stroke="{col}" stroke-width="1.2"/>')
    f.text(x+12,y+21,head,13,INK,"start",True)
    for k,l in enumerate(ls): f.text(x+12,y+42+k*19,l,12.5,MUTED,"start")
item(36,56,"データの形",["関係モデル（1970 年）","実体関連モデル（1976 年）"],DB)
item(36,138,"文書の形",["XML Schema（2001 年に W3C 勧告）","JSON Schema"],DB)
item(36,220,"モデルの定義のしかた",["OMG の MOF"],DB)
item(406,56,"データについての情報の語彙",["ダブリンコア（2003 年に ISO 15836）"],WEB)
item(406,138,"Web ページ向けの語彙",["schema.org（2011 年に発表）"],WEB)
item(406,220,"データに用いる用語",["共通語彙基盤（日本、IMI の一部）"],WEB)
f.text(20,344,"左は項目の並びや型を決める。右は項目の名前が何を指すかを決める。",12.5,INK)
f.text(20,364,"左右の分け方と、意味の 4 段階との対応は筆者の整理である。",12,MUTED)
f.save("el-datamodel-map.svg")

# 9 章: OSI から Apache Ossie への経過
f=Fig(760,330,"OSI から Apache Ossie への経過")
EV=[("2025-09-23",["Snowflake らが","OSI を発表"]),("2026-01-27",["仕様の最初の版","を公開"]),("2026-04-28",["コミュニティ更新","参加者を列挙"]),("2026-06-22",["Apache Incubator で","インキュベーション開始"]),("2026-07-10",["Apache Ossie への","改称を公表"])]
XS=[90,235,380,525,670]; Y=70
f.o.append(f'<line x1="{XS[0]}" y1="{Y}" x2="{XS[3]}" y2="{Y}" stroke="{BI}" stroke-width="3"/>')
f.o.append(f'<line x1="{XS[3]}" y1="{Y}" x2="{XS[4]+40}" y2="{Y}" stroke="{KR}" stroke-width="3"/>')
f.text(XS[0],32,"Open Semantic Interchange（OSI）",13,BI,"start",True); f.text(XS[4]+40,32,"Apache Ossie (Incubating)",13,KR,"end",True)
for (d,ls),x in zip(EV,XS):
    col=KR if x>=XS[3] else BI
    f.o.append(f'<circle cx="{x}" cy="{Y}" r="6" fill="#ffffff" stroke="{col}" stroke-width="2.5"/>')
    f.text(x,Y+28,d,12.5,INK,"middle",True)
    for k,l in enumerate(ls): f.text(x,Y+48+k*17,l,12,MUTED,"middle")
f.text(20,186,"仕様の説明は、出どころによって違う",13.5,INK,"start",True)
f.box(20,200,350,84,"Apache Incubator のステータスページ",["業務指標、ディメンション、それらの関係","オントロジーには触れていない"],BI,tsize=13)
f.box(390,200,350,84,"プロジェクトのブログ記事",["セマンティックレイヤとオントロジーの","両方のためのオープン仕様"],KR,tsize=13)
f.text(20,312,"横軸は出来事の順序を示す。間隔は日数に比例しない。",12,MUTED)
f.save("el-ossie-timeline.svg")
# ---------------------------------------------------------------- スライド専用の図（dk-*）
# 同じ名前で、違うものを指す
f=Fig(760,360,"同じ名前で違うものを指す例")
table(f,40,60,"A 社の部品表",["part_id","重量"],["P-100","12"],[130,130],DB)
table(f,460,60,"B 社の部品表",["part_id","重量"],["P-100","0.03"],[130,130],DB)
f.text(170,150,"グラム。部品そのものの重さ",13,MUTED,"middle"); f.text(590,150,"キログラム。梱包を含む重さ",13,MUTED,"middle")
f.box(250,210,260,70,"列の名前はどちらも「重量」",["単位も、何の重さかも書かれていない"],KR)
f.arrow(170,160,300,208); f.arrow(590,160,460,208)
f.text(40,320,"名前がそろっていても、意味がそろっているとは限らない。数値は説明用の例である。",13,MUTED)
f.save("dk-same-name.svg")

# 意味の定義の読み手に AI が加わった
f=Fig(760,360,"意味の定義の読み手")
f.box(40,130,220,90,"意味の定義",["指標、規則、語彙"],WEB)
for i,(t,sub,col) in enumerate([("人","定義書を読み、尋ねて確かめる",None),("分析ツール","定義どおりに計算する",None),("AI エージェント","定義がなければ推測する",KR)]):
    y=40+i*100; f.box(470,y,250,76,t,[sub],col); f.arrow(262,175,468,y+38)
f.text(365,36,"読み手",13,MUTED,"middle")
f.text(470,232,"近年、読み手に加わった",12.5,KR,"start")
f.text(40,340,"どこまでを推測に任せ、どこからを定義で渡すかを決める必要がある。",13,INK)
f.save("dk-readers.svg")

# OWL と SHACL: 同じデータを、別の見方で扱う
f=Fig(760,380,"OWL と SHACL の違い")
f.box(230,20,300,84,"データ",["部品 P-200","供給者が書かれていない"],None)
f.box(40,170,310,120,"OWL（推論）",["書かれていないことは「未知」","供給者はいるかもしれない","誤りとは判定しない"],KR)
f.box(410,170,310,120,"SHACL（検査）",["書かれていなければ「違反」","供給者は必須、という条件に","合わないと報告する"],WEB)
f.arrow(320,104,210,168); f.arrow(440,104,550,168)
f.text(195,318,"開世界の前提",13,KR,"middle",True); f.text(565,318,"閉じたデータとして検査",13,WEB,"middle",True)
f.text(40,360,"定義から導きたいときは OWL、条件を満たすか調べたいときは SHACL を使う。",13,MUTED)
f.save("dk-owl-shacl.svg")

# Ossie が近づく二つの相手
f=Fig(760,380,"Apache Ossie が近づく二つの相手")
f.box(270,140,220,96,"Apache Ossie",["出発点は、指標と","ディメンションの交換"],BI)
f.box(20,20,300,84,"製品のオントロジー",["Palantir、Goldman Sachs Legend"],KR)
f.box(440,20,300,84,"Web 標準系",["RDF、OWL の語彙"],WEB)
f.arrow(320,140,210,106); f.arrow(440,140,550,106)
f.text(150,128,"ロードマップが先例に挙げる",12.5,INK,"middle"); f.text(610,128,"オントロジー仕様が関連づける",12.5,INK,"middle")
f.box(150,280,460,60,None,[],None,dashed=True)
f.text(380,305,"Apache Incubator の公式な説明は、",13,INK,"middle"); f.text(380,325,"オントロジーに触れていない",13,INK,"middle")
f.text(20,368,"2026 年 4 月には、オントロジーの表現を扱うワーキンググループがあった。",13,MUTED)
f.save("dk-ossie-two.svg")
# 連続体と意味の 4 段階の対応。並べ直すと順が入れ替わる
f=Fig(760,410,"連続体と意味の 4 段階の対応")
GX=[30,205,380,555]; GW=168
f.text(30,30,"先行する整理: 成果物の種類を、形式的な順に並べる",13,MUTED)
for x,(t,s2) in zip(GX,[("用語集、データ辞書","人が読む説明"),("シソーラス、分類","広い語と狭い語"),("スキーマ、データモデル","項目と型"),("形式的なオントロジー","論理による定義")]):
    f.o.append(f'<rect x="{x}" y="44" width="{GW}" height="62" rx="4" fill="#f6f8fa" stroke="{LINE}" stroke-width="1.2"/>')
    f.text(x+GW/2,69,t,13,INK,"middle",True); f.text(x+GW/2,90,s2,12.5,MUTED,"middle")
f.text(723,352,"意味の 4 段階: 機械にできることの順に並べる",13,WEB,"end",True)
for i,(x,(t,s2)) in enumerate(zip(GX,[("1 形を検査できる","JSON Schema など"),("2 同じものだと分かる","RDF と共有の語彙"),("3 用語の関係をたどれる","SKOS"),("4 定義から導ける","RDF Schema、OWL")])):
    dash=' stroke-dasharray="6 4"' if i==1 else ''
    f.o.append(f'<rect x="{x}" y="270" width="{GW}" height="62" rx="4" fill="{TINT[WEB]}" stroke="{WEB}" stroke-width="1.5"{dash}/>')
    f.text(x+GW/2,295,t,13,INK,"middle",True); f.text(x+GW/2,316,s2,12.5,MUTED,"middle")
def link(a,b): f.o.append(f'<line x1="{GX[a]+GW/2}" y1="108" x2="{GX[b]+GW/2}" y2="268" stroke="#52606d" stroke-width="1.6" marker-end="url(#a)"/>')
link(1,2); link(2,0); link(3,3)
f.text(GX[0]+GW/2,128,"段の手前",12.5,MUTED,"middle"); f.text(GX[0]+GW/2,145,"機械は中身を扱えない",12.5,MUTED,"middle")
f.text(GX[1]+GW/2,352,"連続体には、",12.5,MUTED,"middle"); f.text(GX[1]+GW/2,369,"対応するものがない",12.5,MUTED,"middle")
f.text(30,398,"スキーマとシソーラスの順が入れ替わる。対応は筆者の整理である。",12.5,MUTED)
f.save("dk-spectrum-ladder.svg")
# AI に意味を渡す二つの方法: Ossie と OKF
f=Fig(760,390,"AI に意味を渡す二つの方法")
f.box(30,30,320,150,"構造化した定義で渡す",["Apache Ossie","指標や概念の定義そのものを","決まった形で書く","機械が項目を解釈する"],BI)
f.box(410,30,320,150,"文章のまま渡す",["Open Knowledge Format","1 概念を 1 つの Markdown で書く","型、URI、リンクは機械が読める","意味の多くは文章で、言語モデルが解釈する"],KR)
f.box(270,250,220,70,"AI エージェント",["同じ定義、同じ文脈で答える"],None)
f.arrow(190,182,330,248); f.arrow(570,182,430,248)
f.text(380,208,"どちらも分析系から出た",13,BI,"middle",True)
f.text(380,228,"違いは、どこまでを構造にするか",12.5,MUTED,"middle")
f.text(30,360,"Ossie は 2025 年 9 月に OSI として発表、OKF は 2026 年 6 月に発表。",13,MUTED)
f.text(30,380,"二つに分けて見るのは筆者の整理である。",12.5,MUTED)
f.save("dk-okf.svg")
# 一つの段に収まらない技術の三つの種類
f=Fig(760,318,"一つの段に収まらない技術の三つの種類")
SH=["#dcefe8","#b9e0d1","#8fcfb7","#5cb894"]; BASE=178; SWD=46
def mini(x0):
    xs=[]
    for i in range(4):
        x=x0+i*SWD; h=34+i*26
        f.o.append(f'<rect x="{x}" y="{BASE-h}" width="{SWD-4}" height="{h}" fill="{SH[i]}" stroke="{WEB}" stroke-width="1.2"/>')
        f.text(x+(SWD-4)/2,BASE-h+16,str(i+1),12,INK,"middle",True); xs.append(x)
    f.o.append(f'<line x1="{x0-8}" y1="{BASE}" x2="{x0+4*SWD+4}" y2="{BASE}" stroke="#52606d" stroke-width="1.5"/>')
    return xs
def panel(x0,title,l1,l2,ex):
    f.text(x0+110,28,title,16,INK,"middle",True)
    f.text(x0+110,250,l1,14,INK,"middle"); f.text(x0+110,270,l2,14,INK,"middle")
    f.text(x0+110,298,ex,13,MUTED,"middle")
    return mini(x0+20)
# またがる: 1 から 3 段目の下の部分を、一つの枠が覆う
xs=panel(20,"またがる","複数の段を","一部ずつ備える","Palantir の Ontology、OKF")
f.o.append(f'<rect x="{xs[0]-5}" y="{BASE-30}" width="{3*SWD+6}" height="36" rx="6" fill="{KR}" fill-opacity="0.22" stroke="{KR}" stroke-width="2" stroke-dasharray="6 4"/>')
# 同じ役割を担う: 1 段目の隣に、同じ高さの箱
xs=panel(270,"同じ役割を担う","ある段の役割を","別の対象で果たす","SHACL")
f.o.append(f'<rect x="{xs[0]}" y="{BASE+12}" width="{SWD-4}" height="34" rx="4" fill="{TINT[WEB]}" stroke="{WEB}" stroke-width="2" stroke-dasharray="6 4"/>')
f.text(xs[0]+(SWD-4)/2,BASE+33,"1",12,INK,"middle",True)
f.text(xs[0]+SWD+6,BASE+34,"グラフを検査",12,MUTED,"start")
# 別の軸にある: 段の上に載る箱と、横から使う箱
xs=panel(520,"別の軸にある","段の仕組みを使うが、","目的は意味の深さと別","DCAT、セマンティックレイヤ")
f.o.append(f'<rect x="{xs[0]-4}" y="{BASE-34-30}" width="{SWD+4}" height="26" rx="4" fill="{TINT[BI]}" stroke="{BI}" stroke-width="2" stroke-dasharray="6 4"/>')
f.text(xs[0]+SWD/2-2,BASE-34-12,"指標",12,INK,"middle")
f.o.append(f'<rect x="{xs[1]-2}" y="{BASE-60-30}" width="{SWD}" height="26" rx="4" fill="{TINT[DB]}" stroke="{DB}" stroke-width="2" stroke-dasharray="6 4"/>')
f.text(xs[1]+SWD/2-2,BASE-60-12,"目録",12,INK,"middle")
f.o.append(f'<line x1="255" y1="14" x2="255" y2="304" stroke="{LINE}" stroke-width="1" stroke-dasharray="4 4"/>')
f.o.append(f'<line x1="505" y1="14" x2="505" y2="304" stroke="{LINE}" stroke-width="1" stroke-dasharray="4 4"/>')
f.save("dk-not-fit.svg")
# 課題から選ぶ木
f=Fig(760,470,"課題から候補を選ぶ木")
PX,PW=14,206; CXL=236; LX,LW=494,252; RH=40; Y0=42
f.text(PX,26,"何をしたいか",13,MUTED,"start",True); f.text(CXL+14,26,"条件",13,MUTED,"start",True); f.text(LX,26,"候補",13,MUTED,"start",True)
TREE=[("数字をそろえたい","同じ指標が違う値になる",[("一つの組織の中で","セマンティックレイヤ",BI),("ツールやベンダをまたいで","Apache Ossie",BI)]),
      ("データを突き合わせたい","どこまで機械に任せるか",[("形が合えばよい（1 段目）","JSON Schema、SHACL",DB),("同じものだと分かればよい（2 段目）","RDF と共有の語彙",WEB),("用語の関係もたどる（3 段目）","SKOS",WEB),("定義から導く（4 段目）","RDF Schema、OWL",WEB)]),
      ("業務の操作につなげたい","データと操作を結ぶ",[("一つの基盤の中で","製品のオントロジー（Palantir）",KR)]),
      ("AI に文脈を渡したい","どこまでを構造にするか",[("定義を構造で渡す","セマンティックレイヤ、Ossie",BI),("文章のまま渡す","Open Knowledge Format",BI)]),
      ("データを見つけたい","データについての情報を書く",[("カタログを公開する","DCAT、ダブリンコア",WEB)])]
r=0
for name,sub,leaves in TREE:
    y0=Y0+r*RH; n=len(leaves); h=n*RH-8
    f.o.append(f'<rect x="{PX}" y="{y0}" width="{PW}" height="{h}" rx="6" fill="#f6f8fa" stroke="{LINE}" stroke-width="1.5"/>')
    cy=y0+h/2
    two=bool(sub) and n>1
    f.text(PX+12,cy-2 if two else cy+5,name,13.5,INK,"start",True)
    if two: f.text(PX+12,cy+16,sub,11.5,MUTED,"start")
    ys=[Y0+(r+k)*RH+(RH-8)/2 for k in range(n)]
    f.o.append(f'<line x1="{PX+PW}" y1="{cy}" x2="{CXL}" y2="{cy}" stroke="#52606d" stroke-width="1.4"/>')
    if n>1: f.o.append(f'<line x1="{CXL}" y1="{ys[0]}" x2="{CXL}" y2="{ys[-1]}" stroke="#52606d" stroke-width="1.4"/>')
    for (cond,leaf,col),yy in zip(leaves,ys):
        f.o.append(f'<line x1="{CXL}" y1="{yy}" x2="{LX-2}" y2="{yy}" stroke="#52606d" stroke-width="1.4" marker-end="url(#a)"/>')
        f.o.append(f'<rect x="{CXL+10}" y="{yy-11}" width="{len(cond)*12.4+10:.0f}" height="20" fill="#ffffff"/>')
        f.text(CXL+14,yy+4,cond,12,INK,"start")
        f.o.append(f'<rect x="{LX}" y="{yy-15}" width="{LW}" height="30" rx="6" fill="{TINT[col]}" stroke="{col}" stroke-width="1.5"/>')
        f.text(LX+LW/2,yy+5,leaf,13,INK,"middle",True)
    r+=n
f.text(PX,452,"複数に当てはまるのが普通である。候補は組み合わせて使う。筆者の整理である。",12.5,MUTED)
f.save("el-choose.svg")
print("done")
