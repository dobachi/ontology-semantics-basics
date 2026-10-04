#!/usr/bin/env python3
"""生成物の元ファイルを監視し、変わったら生成物を作り直す。

quarto preview が監視するのは .qmd などの入力だけで、図や章を生成するスクリプトは監視しない。
このスクリプトはその隙間を埋める。標準ライブラリだけで動く（inotify 系の道具を前提にしない）。

  監視対象                         変わったときに実行する
  figures/build_*.py               そのスクリプト（SVG を作り直す）
  examples/ の例と build_chapter.py examples/build_chapter.py（_elements.qmd を作り直す）

_elements.qmd が書き換わると、quarto preview がそれを検知して再描画する。

もう一つの役目は、描画の取りこぼしの回復である。quarto preview は、描画の途中で届いた編集を
取りこぼすことがある。出力の時刻は新しくなるのに中身は古いままになり、以後は何も起きない。
このスクリプトは出力の中身がソースに追いついているかを定期的に調べ、遅れていたら
ソースの更新時刻だけを進めて、描画をやり直させる。それでも古いままなら、プレビューを起動し直す。

三つ目の役目は、描画エラーからの回復である。quarto の内部キャッシュ（Sass の KV）が壊れると、
全ページが「Bad resource ID」のエラーページになり、描画をやり直しても直らない。
配信がエラーページになったのを検知したら quarto preview を止める。scripts/preview.sh が
キャッシュを消して起動し直す。
"""
import os, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import freshness
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERVAL = float(os.environ.get("WATCH_INTERVAL", "1.0"))

def targets():
    t = {}
    fig = os.path.join(ROOT, "figures")
    for f in sorted(os.listdir(fig)):
        if f.startswith("build_") and f.endswith(".py"):
            t[os.path.join(fig, f)] = [sys.executable, os.path.join(fig, f)]
    ex = os.path.join(ROOT, "examples")
    chapter = [sys.executable, os.path.join(ex, "build_chapter.py")]
    for f in sorted(os.listdir(ex)):
        p = os.path.join(ex, f)
        if os.path.isfile(p) and not f.startswith(".") and f != "validate.py":
            t[p] = chapter
    return t

def mtimes(paths):
    out = {}
    for p in paths:
        try: out[p] = os.stat(p).st_mtime_ns
        except FileNotFoundError: pass
    return out

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    name = os.path.relpath(cmd[-1], ROOT)
    if r.returncode == 0:
        print(f"[watch] 再生成: {name}", flush=True)
    else:
        print(f"[watch] 失敗: {name}\n{r.stderr.strip()}", flush=True)

SETTLE = 20.0      # ソースの最後の編集からこの秒数たっても遅れていたら、取りこぼしとみなす
# 描画のやり直しを要求する間隔の下限。1 回の描画（30 秒前後）より十分長くする。
# 短いと、描画中に次の更新を入れてしまい、監視自身が取りこぼしを起こす
RETRY_GAP = 90.0
GIVE_UP = 3        # 同じ行がこの回数やり直しても足りなければ、照合に向かない行とみなす

def stale_pages(ignore):
    """出力が遅れているページを返す。{page: [足りない行]}"""
    out = {}
    for page, srcs in freshness.SOURCES.items():
        path = os.path.join(ROOT, "_output", page)
        if not os.path.exists(path): continue
        newest = max(os.stat(os.path.join(ROOT, s)).st_mtime for s in srcs)
        if time.time() - newest < SETTLE: continue
        with open(path, encoding="utf-8") as fh:
            miss, _ = freshness.missing_lines(fh.read(), page)
        miss = [l for l in miss if l not in ignore]
        if miss: out[page] = miss
    return out

ERROR_GAP = 60.0   # エラーページを検知して再起動を要求する間隔の下限

def render_error():
    """配信がエラーページになっていれば、その理由を返す。"""
    url = os.environ.get("PREVIEW_URL")
    if not url: return None
    try:
        h = urllib.request.urlopen(url + "/index.html", timeout=10).read(4000).decode("utf-8", "replace")
    except Exception:
        return None
    if "quarto-render-error" in h:
        i = h.find('type="text/plain">'); j = h.find("</script>", i)
        return h[i + 18:j].strip() if i >= 0 else "render error"
    return None

def main():
    t = targets(); seen = mtimes(t); last_kill = 0.0
    print(f"[watch] 監視を開始: {len(t)} ファイル（{INTERVAL} 秒ごと）", flush=True)
    last_retry, fails, ignore, tick = 0.0, {}, set(), 0
    while True:
        time.sleep(INTERVAL); tick += 1
        t = targets(); now = mtimes(t)
        changed = [p for p in now if now[p] != seen.get(p)]
        seen = now
        for cmd in {tuple(t[p]) for p in changed}:
            run(list(cmd))
        if tick % 5: continue
        # 配信がエラーページなら、描画のやり直しでは直らない。quarto preview を止めて起動し直させる
        err = render_error()
        if err and time.time() - last_kill > ERROR_GAP:
            pat = os.environ.get("PREVIEW_KILL_PATTERN")
            print(f"[watch] 描画エラーを検知: {err}。プレビューを起動し直す", flush=True)
            if pat: subprocess.run(["pkill", "-f", pat])
            last_kill = time.time()
            continue
        if err: continue
        if time.time() - last_retry < RETRY_GAP: continue
        try: stale = stale_pages(ignore)
        except OSError: continue
        if not stale: continue
        restart = False
        for page, miss in stale.items():
            # 何度やり直しても足りない行は、照合に向かない行なので以後は無視する（無限に再描画しないための歯止め）
            for l in miss: fails[l] = fails.get(l, 0) + 1
            dead = [l for l in miss if fails[l] > GIVE_UP]
            if dead:
                ignore.update(dead)
                print(f"[watch] 照合対象から外した: {page} の {len(dead)} 項目", flush=True)
            fresh = [l for l in miss if l not in ignore]
            if not fresh: continue
            if max(fails[l] for l in fresh) == 1:
                # 1 回目: ソースの更新時刻を進めて、描画をやり直させる
                os.utime(os.path.join(ROOT, freshness.SOURCES[page][0]), None)
                print(f"[watch] 描画の取りこぼしを検知: {page} に {len(fresh)} 項目が未反映。描画をやり直す", flush=True)
            else:
                # 2 回目以降: やり直しても古いままなら、プレビューごと起動し直す。
                # 描画し直しても古いソースの内容が出続けることがあり、更新時刻を進めるだけでは直らなかった
                restart = True
                print(f"[watch] やり直しても {page} に {len(fresh)} 項目が未反映。プレビューを起動し直す", flush=True)
        if restart:
            pat = os.environ.get("PREVIEW_KILL_PATTERN")
            if pat: subprocess.run(["pkill", "-f", pat])
        last_retry = time.time()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: pass
