#!/usr/bin/env python3
"""説明ペーパー用の独自テンプレート（simple.pptx）を作る。

スライドは 1 枚も含まない。持つのは 1 つのスライドマスタと 8 つのレイアウトだけである。
見た目はすべてここで決める。書体と色はテーマに、文字の大きさと箇条書きの形はマスタと
レイアウトの書式に、出典・章の名前・章番号・図の枠はレイアウトのプレースホルダに持たせる。
スライド側は文字と図を流し込むだけで、書式を直接は持たない。

    python3 build_template.py            # -> simple.pptx

見た目を変えたいときは、下の「デザインの値」を直してこのスクリプトを実行し直す。
PowerPoint で simple.pptx のスライドマスタを直接編集してもよい。
"""
import os, re
from pptx import Presentation
from pptx.util import Inches
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "simple.pptx")

# ------------------------------------------------------------ デザインの値
INK, MUTED, SURFACE = "1A1A1A", "6B7280", "F1F5F3"
ACCENT, ACCENT_DARK, ACCENT_LIGHT = "0B7A5C", "0A3D30", "7FD1B5"
HAIR = "D5DBD8"                     # 表の罫線と、章番号の薄い色
FONT_HEAD, FONT_BODY = "Yu Gothic Medium", "Yu Gothic"
PAGE_W, PAGE_H = 13.333, 7.5
MX = 0.92                           # 左右の余白
CW = PAGE_W - 2 * MX                # 本文の幅
TITLE = (MX, 0.62, CW, 1.04)        # 題名の枠。下ぞろえなので、2 行になると上へ伸びる
BODY = (MX, 1.88, CW, 5.00)
FOOT_Y, NUM_W, FOOT_W = 7.04, 0.6, 3.2
EYEBROW = (MX, 0.28, CW, 0.26)
SOURCE = (MX, FOOT_Y - 0.02, CW - NUM_W - FOOT_W - 0.2, 0.3)
SPLIT_TEXT_W = 3.55                 # 図と説明: 左の説明の幅
GAP = 0.28
TABLE_STYLE_ID = "{6D0BA5C1-51A0-4E2B-9B7E-0B7A5C000001}"

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
EMU = lambda inch: int(round(inch * 914400))


def clr(c):
    """色の指定。'tx1' のような名前はテーマ色、6 桁は直接の色。"""
    return '<a:schemeClr val="%s"/>' % c if not re.fullmatch(r"[0-9A-Fa-f]{6}", c) else '<a:srgbClr val="%s"/>' % c


def lvl(n, sz, color="tx1", bold=False, bullet=None, indent=0.0, before=0, algn="l", font="+mn"):
    """段落レベル n の書式。bullet が None なら行頭記号なし。indent は記号の分の字下げ（インチ）。"""
    mar = EMU(indent * n) if bullet else 0
    ind = -EMU(indent) if bullet else 0
    bu = ('<a:buClr>%s</a:buClr><a:buFont typeface="Arial"/><a:buChar char="%s"/>' % (clr("tx2"), bullet)
          if bullet else "<a:buNone/>")
    return ('<a:lvl%dpPr marL="%d" indent="%d" algn="%s"><a:spcBef><a:spcPts val="%d"/></a:spcBef>%s'
            '<a:defRPr sz="%d" b="%d" kern="1200"><a:solidFill>%s</a:solidFill>'
            '<a:latin typeface="%s-lt"/><a:ea typeface="%s-ea"/><a:cs typeface="%s-cs"/></a:defRPr></a:lvl%dpPr>'
            % (n, mar, ind, algn, before * 100, bu, sz * 100, 1 if bold else 0, clr(color), font, font, font, n))


def place(sp, box):
    x, y, w, h = box
    sp.left, sp.top, sp.width, sp.height = EMU(x), EMU(y), EMU(w), EMU(h)


def style(ph, levels, anchor="t", prompt=None):
    """プレースホルダの書式を、レイアウト（またはマスタ）の側に書き込む。"""
    tx = ph._element.txBody
    body_pr = tx.find(qn("a:bodyPr"))
    for k in list(body_pr.attrib):
        del body_pr.attrib[k]
    for ch in list(body_pr):
        body_pr.remove(ch)
    body_pr.set("anchor", anchor); body_pr.set("lIns", "0"); body_pr.set("rIns", "0")
    body_pr.set("tIns", "0"); body_pr.set("bIns", "0"); body_pr.set("wrap", "square")
    body_pr.append(parse_xml("<a:noAutofit %s/>" % NS))
    old = tx.find(qn("a:lstStyle"))
    new = parse_xml("<a:lstStyle %s>%s</a:lstStyle>" % (NS, "".join(levels)))
    if old is not None:
        tx.replace(old, new)
    else:
        body_pr.addnext(new)
    if prompt is not None:
        for p in tx.findall(qn("a:p")):
            tx.remove(p)
        for i, line in enumerate(prompt):
            tx.append(parse_xml('<a:p %s><a:pPr lvl="%d"/><a:r><a:rPr lang="ja-JP"/><a:t>%s</a:t></a:r></a:p>' % (NS, i, line)))


def next_id(container):
    return max([int(e.get("id")) for e in container.shapes._spTree.iter(qn("p:cNvPr")) if e.get("id")] + [1]) + 1


def add_ph(layout, name, idx, box, levels, prompt, anchor="t", kind="body"):
    """レイアウトにプレースホルダを 1 つ足す。name が、生成ツールが役割を見分ける手がかりになる。"""
    x, y, w, h = box
    sp = parse_xml(
        '<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        '<p:nvPr><p:ph type="%s" sz="quarter" idx="%d"/></p:nvPr></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm></p:spPr>'
        '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="ja-JP"/></a:p></p:txBody></p:sp>'
        % (NS, next_id(layout), name, kind, idx, EMU(x), EMU(y), EMU(w), EMU(h)))
    layout.shapes._spTree.insert_element_before(sp, "p:extLst")
    ph = [p for p in layout.placeholders if p.placeholder_format.idx == idx][0]
    style(ph, levels, anchor, [prompt])
    return ph


def add_rule(layout, x, y, color="accent1", w=1.05, h=0.045):
    """短い線。転換のページ（表紙、中扉、メッセージ）だけが持つ、レイアウト上の固定の図形。"""
    sp = parse_xml(
        '<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Rule"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill>%s</a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>'
        '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="ja-JP"/></a:p></p:txBody></p:sp>'
        % (NS, next_id(layout), EMU(x), EMU(y), EMU(w), EMU(h), clr(color)))
    layout.shapes._spTree.insert_element_before(sp, "p:extLst")


def set_bg(layout, color):
    c_sld = layout._element.find(qn("p:cSld"))
    for old in c_sld.findall(qn("p:bg")):
        c_sld.remove(old)
    c_sld.insert(0, parse_xml('<p:bg %s><p:bgPr><a:solidFill>%s</a:solidFill><a:effectLst/></p:bgPr></p:bg>' % (NS, clr(color))))


def by_type(container, *names):
    out = []
    for ph in container.placeholders:
        t = str(ph.placeholder_format.type).split(".")[-1].split(" ")[0]
        if t in names:
            out.append(ph)
    return out


def drop(ph):
    ph._element.getparent().remove(ph._element)


def furniture(container, color="tx2"):
    """フッター（著作権表示）とページ番号。右下に並べる。日付の枠は使わないので外す。"""
    for ph in by_type(container, "DATE"):
        drop(ph)
    for ph in by_type(container, "FOOTER"):
        place(ph, (PAGE_W - MX - NUM_W - FOOT_W, FOOT_Y, FOOT_W, 0.3))
        style(ph, [lvl(1, 10, color, algn="r")], "ctr")
    for ph in by_type(container, "SLIDE_NUMBER"):
        place(ph, (PAGE_W - MX - NUM_W, FOOT_Y, NUM_W, 0.3))
        style(ph, [lvl(1, 10, color, algn="r")], "ctr")


BULLETS = [lvl(1, 18, bullet="–", indent=0.30, before=8), lvl(2, 16, bullet="–", indent=0.30, before=4),
           lvl(3, 14, "tx2", bullet="–", indent=0.30, before=3)]
# 見出しつきの欄（図と説明、2 つのコンテンツ）: 1 段目が見出し、2 段目からが箇条書き
HEADED = [lvl(1, 18, "accent1", bold=True, before=0, font="+mj"),
          lvl(2, 18, bullet="–", indent=0.28, before=9).replace('marL="%d"' % EMU(0.56), 'marL="%d"' % EMU(0.28)),
          lvl(3, 16, "tx2", bullet="–", indent=0.28, before=4).replace('marL="%d"' % EMU(0.84), 'marL="%d"' % EMU(0.56))]
HEADED_WIDE = [h.replace('sz="1800"', 'sz="1600"').replace('<a:spcPts val="900"/>', '<a:spcPts val="400"/>') for h in HEADED]
SMALL = lambda sz, color="tx2": [lvl(1, sz, color)]


def content_extras(layout):
    add_ph(layout, "Eyebrow (section label)", 20, EYEBROW, SMALL(12), "章の名前", "ctr")
    add_ph(layout, "Source", 21, SOURCE, SMALL(11), "出典", "ctr")


def main():
    prs = Presentation()
    prs.slide_width, prs.slide_height = EMU(PAGE_W), EMU(PAGE_H)
    master = prs.slide_masters[0]

    # ---- テーマ: 書体と色。スライドの文字はここを参照する
    theme = master.part.part_related_by("http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme")
    x = theme.blob.decode("utf-8")
    def font(block, face):
        def sub(m):
            b = m.group(0)
            b = re.sub(r'<a:latin typeface="[^"]*"', '<a:latin typeface="%s"' % face, b, count=1)
            b = re.sub(r'<a:ea typeface="[^"]*"', '<a:ea typeface="%s"' % face, b, count=1)
            b = re.sub(r'<a:font script="Jpan" typeface="[^"]*"', '<a:font script="Jpan" typeface="%s"' % face, b, count=1)
            return b
        return re.sub(r"<a:%s>.*?</a:%s>" % (block, block), sub, x, count=1, flags=re.S)
    x = font("majorFont", FONT_HEAD); x = font("minorFont", FONT_BODY)
    for tag, val in (("dk1", INK), ("lt1", "FFFFFF"), ("dk2", MUTED), ("lt2", SURFACE), ("accent1", ACCENT),
                     ("accent2", ACCENT_DARK), ("accent3", ACCENT_LIGHT), ("accent4", MUTED), ("accent5", HAIR),
                     ("accent6", INK), ("hlink", ACCENT), ("folHlink", MUTED)):
        x = re.sub(r"<a:%s>.*?</a:%s>" % (tag, tag), '<a:%s><a:srgbClr val="%s"/></a:%s>' % (tag, val, tag), x, count=1, flags=re.S)
    x = re.sub(r'(<a:theme [^>]*name=")[^"]*"', r'\1Dobashi Simple"', x, count=1)
    # 図形に影をつけない。既定のテーマは図形に影の効果を持たせている
    x = re.sub(r"<a:effectStyleLst>.*?</a:effectStyleLst>",
               "<a:effectStyleLst>" + "<a:effectStyle><a:effectLst/></a:effectStyle>" * 3 + "</a:effectStyleLst>",
               x, count=1, flags=re.S)
    theme._blob = x.encode("utf-8")

    # ---- 表の既定スタイル: 帯を塗らない。見出し行は太字で、下にアクセント色の線を引く
    ts = prs.part.part_related_by("http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles")
    def bdr(side, w, color): return '<a:%s><a:ln w="%d" cmpd="sng"><a:solidFill>%s</a:solidFill></a:ln></a:%s>' % (side, w, clr(color), side)
    none = lambda side: '<a:%s><a:ln><a:noFill/></a:ln></a:%s>' % (side, side)
    ts._blob = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="%s">'
        '<a:tblStyle styleId="%s" styleName="Dobashi Simple">'
        '<a:wholeTbl><a:tcTxStyle><a:fontRef idx="minor"/><a:schemeClr val="tx1"/></a:tcTxStyle>'
        '<a:tcStyle><a:tcBdr>%s%s%s%s%s%s</a:tcBdr><a:fill><a:noFill/></a:fill></a:tcStyle></a:wholeTbl>'
        '<a:firstRow><a:tcTxStyle b="on"><a:fontRef idx="major"/><a:schemeClr val="tx1"/></a:tcTxStyle>'
        '<a:tcStyle><a:tcBdr>%s</a:tcBdr><a:fill><a:noFill/></a:fill></a:tcStyle></a:firstRow>'
        '</a:tblStyle></a:tblStyleLst>'
        % (TABLE_STYLE_ID, TABLE_STYLE_ID, none("left"), none("right"), none("top"), bdr("bottom", 6350, HAIR),
           bdr("insideH", 6350, HAIR), none("insideV"), bdr("bottom", 15875, ACCENT))).encode("utf-8")
    # 表とテキストボックスの既定の文字の大きさ
    for d in prs.part._element.iter(qn("a:defRPr")):
        if d.get("sz"):
            d.set("sz", "1600")

    # ---- マスタ: 題名と本文の書式、フッターとページ番号
    tx = master._element.find(qn("p:txStyles"))
    tx.getparent().replace(tx, parse_xml(
        "<p:txStyles %s><p:titleStyle>%s</p:titleStyle><p:bodyStyle>%s</p:bodyStyle><p:otherStyle>%s</p:otherStyle></p:txStyles>"
        % (NS, lvl(1, 28, bold=True, font="+mj"), "".join(BULLETS), lvl(1, 16))))
    for ph in by_type(master, "TITLE"):
        place(ph, TITLE); style(ph, [], "b")
    for ph in by_type(master, "BODY"):
        place(ph, BODY); style(ph, [], "t")
    furniture(master)

    L = {l.name: l for l in prs.slide_layouts}
    for name in ("Title Only", "Vertical Title and Text"):
        prs.slide_layouts.remove(L[name])

    def reset(layout, new_name):
        """レイアウト固有の位置指定を外し、マスタの位置を継がせる。"""
        layout.name = new_name
        furniture(layout)
        return layout

    # 1 表紙
    lo = reset(L["Title Slide"], "タイトル スライド")
    add_rule(lo, MX, 2.62)
    t = by_type(lo, "CENTER_TITLE")[0]; place(t, (MX, 2.76, CW, 1.56)); style(t, [lvl(1, 40, bold=True, font="+mj")], "ctr")
    s = by_type(lo, "SUBTITLE")[0]; place(s, (MX, 4.56, CW, 0.80)); style(s, [lvl(1, 22, "tx2")], "t")
    add_ph(lo, "Presenter", 13, (MX, 5.50, CW, 1.20), [lvl(1, 18, before=2)], "作者、日付")

    # 2 タイトルとコンテンツ
    lo = reset(L["Title and Content"], "タイトルとコンテンツ")
    for ph in by_type(lo, "TITLE"): place(ph, TITLE); style(ph, [], "b")
    for ph in by_type(lo, "OBJECT", "BODY"): place(ph, BODY); style(ph, [], "t")
    content_extras(lo)

    # 3 中扉
    lo = reset(L["Section Header"], "セクション見出し")
    add_ph(lo, "Section number", 22, (MX, 1.30, CW, 1.60), [lvl(1, 80, "tx2", bold=True, font="+mj")], "00", "b")
    add_rule(lo, MX, 3.02)
    t = by_type(lo, "TITLE")[0]; place(t, (MX, 3.16, CW, 1.50)); style(t, [lvl(1, 36, bold=True, font="+mj")], "t")
    for ph in by_type(lo, "BODY"):
        if ph.placeholder_format.idx != 22: drop(ph)

    # 4 2 つのコンテンツ
    lo = reset(L["Two Content"], "2 つのコンテンツ")
    for ph in by_type(lo, "TITLE"): place(ph, TITLE); style(ph, [], "b")
    half = (CW - 0.5) / 2
    for i, ph in enumerate(sorted(by_type(lo, "OBJECT", "BODY"), key=lambda p: p.left)):
        place(ph, (MX + i * (half + 0.5), BODY[1], half, BODY[3])); style(ph, HEADED, "t")
    content_extras(lo)

    # 5 図と説明: 左に説明、右に図。図は枠の中に、切り取らずに収める
    lo = reset(L["Picture with Caption"], "図と説明")
    for ph in by_type(lo, "TITLE"): place(ph, TITLE); style(ph, [], "b")
    for ph in by_type(lo, "BODY"):
        place(ph, (MX, BODY[1], SPLIT_TEXT_W, BODY[3])); style(ph, HEADED, "t", ["見出し", "箇条書き"])
    for ph in by_type(lo, "PICTURE"):
        place(ph, (MX + SPLIT_TEXT_W + GAP, BODY[1], CW - SPLIT_TEXT_W - GAP, BODY[3]))
    content_extras(lo)

    # 5b 図と説明（横長）: 横に長い図を全幅に置き、説明をその下に置く
    lo = reset(L["Title and Vertical Text"], "図と説明（横長）")
    for ph in by_type(lo, "TITLE"): place(ph, TITLE); style(ph, [], "b")
    for ph in by_type(lo, "BODY", "OBJECT"):
        ph._element.txBody.find(qn("a:bodyPr")).attrib.pop("vert", None)
        place(ph, (MX, 5.70, CW, 1.25)); style(ph, HEADED_WIDE, "t", ["見出し", "箇条書き"])
    add_ph(lo, "Picture", 23, (MX, BODY[1], CW, 3.70), [], "図", kind="pic")
    content_extras(lo)

    # 6 メッセージ: 一文だけを置く
    def statement(lo, name, dark):
        reset(lo, name)
        if dark:
            set_bg(lo, ACCENT_DARK); furniture(lo, ACCENT_LIGHT)
        w = CW * 0.84
        t = by_type(lo, "TITLE")[0]; place(t, (MX, 1.95, w, 2.20))
        style(t, [lvl(1, 36, "FFFFFF" if dark else "tx1", bold=True, font="+mj")], "b")
        add_rule(lo, MX, 4.27, ACCENT_LIGHT if dark else "accent1")
        bodies = sorted(by_type(lo, "BODY", "OBJECT"), key=lambda p: (p.top, p.left))
        for ph in bodies[1:]:
            drop(ph)
        place(bodies[0], (MX, 4.42, w, 0.90)); style(bodies[0], [lvl(1, 18, ACCENT_LIGHT if dark else "tx2")], "t", ["補足"])
    statement(L["Content with Caption"], "メッセージ", False)
    statement(L["Comparison"], "メッセージ（濃色）", True)
    # 濃色を通常の後ろに置く。名前で探すとき、通常のほうが先に見つかるようにする
    lst = master._element.find(qn("p:sldLayoutIdLst"))
    ids = {prs.slide_layouts[i].name: el for i, el in enumerate(list(lst))}
    lst.remove(ids["メッセージ（濃色）"]); lst.append(ids["メッセージ（濃色）"])

    # 7 白紙
    reset(L["Blank"], "白紙")

    # ファイルの作成者情報。python-pptx の既定値を残さない
    cp = prs.core_properties
    cp.author = cp.last_modified_by = "Masaru Dobashi"
    cp.title = ""
    prs.save(OUT)
    print("wrote", OUT, "layouts:", [l.name for l in Presentation(OUT).slide_layouts])


if __name__ == "__main__":
    main()
