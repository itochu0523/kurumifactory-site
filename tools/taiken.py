"""体験記（/hunting/taiken/）。content/taiken/*.md を記事ページと一覧パネルにし、note 用の文章も書き出す。

記事ファイルの形（先頭に --- で囲んだ設定、そのあと本文）:
    ---
    title: 狩猟を始めたきっかけ
    date: 2026-12-01
    icon: 🌲
    desc: 一覧と検索結果に出る 1〜2 文
    ---
    本文（## 見出し、- 箇条書き、**太字**、[文字](URL)、空行で段落）

使い方:
    python3 tools/build.py             … サイトに反映（build.py から呼ばれる）
    python3 tools/taiken.py --note     … note 用の文章を ../hunting-app/docs/note/taiken/ に書き出す
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "content" / "taiken"
SITE = "https://kurumifactory.com"


def load():
    """記事を新しい順に読む。ファイル名（拡張子なし）が URL になる"""
    out = []
    for p in sorted(SRC.glob("*.md")) if SRC.exists() else []:
        text = p.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if not m:
            raise SystemExit(f"設定（--- で囲んだ部分）がありません: {p}")
        meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        for k in ("title", "date", "desc"):
            if not meta.get(k):
                raise SystemExit(f"{k} がありません: {p}")
        out.append({**meta, "slug": p.stem, "body": m.group(2).strip(), "icon": meta.get("icon", "🌲")})
    return sorted(out, key=lambda a: a["date"], reverse=True)


def inline(s):
    s = escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"\[(.+?)\]\((https?://[^)\s]+|/[^)\s]*)\)", r'<a href="\2">\1</a>', s)


def to_html(md):
    """必要なぶんだけの Markdown 変換（見出し・箇条書き・段落・引用）"""
    html, para, items = [], [], []

    def flush():
        if para:
            html.append("<p>" + "<br>".join(inline(x) for x in para) + "</p>")
            para.clear()
        if items:
            html.append('<ul class="checks">' + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            items.clear()

    for line in md.splitlines():
        t = line.strip()
        if not t:
            flush()
        elif t.startswith("## "):
            flush(); html.append(f"<h2>{inline(t[3:])}</h2>")
        elif t.startswith("### "):
            flush(); html.append(f"<h3>{inline(t[4:])}</h3>")
        elif t.startswith(("- ", "・")):
            if para:
                flush()
            items.append(t[2:] if t.startswith("- ") else t[1:])
        elif t.startswith("> "):
            flush(); html.append(f'<blockquote>{inline(t[2:])}</blockquote>')
        else:
            if items:
                flush()
            para.append(t)
    flush()
    return "\n".join(html)


def ymd(d):
    y, m, dd = d.split("-")
    return f"{y}年{int(m)}月{int(dd)}日"


def pages(cta):
    """記事がひとつも無いときは何も作らない（空の一覧を公開しない）"""
    arts = load()
    if not arts:
        return {}
    out = {}
    cards = "".join(
        f'<a class="panel link" href="/hunting/taiken/{a["slug"]}/"><span class="p-icon">{a["icon"]}</span>'
        f'<b>{escape(a["title"])}</b><span class="muted small">{ymd(a["date"])}</span>'
        f'<span class="small">{escape(a["desc"])}</span></a>' for a in arts)
    out["/hunting/taiken/"] = ("狩猟の体験記", "狩猟免許の取得から猟銃の所持許可、はじめての猟期まで。現場でしかわからないことを、体験から書いています。", f"""
<span class="badge">🌲 体験記</span>
<h1>狩猟の体験記</h1>
<p class="lead">狩猟免許の取得から、猟銃の所持許可、はじめての猟期まで。<br>困ったこと、助けてもらったこと、現場でしかわからないことを書いています。</p>
<div class="panels">{cards}</div>
{cta}
""")
    # 一覧は新しい順、記事どうしのページ送りは書いた順（古い→新しい）
    seq = list(reversed(arts))
    for i, a in enumerate(seq):
        prev, nxt = (seq[i - 1] if i > 0 else None), (seq[i + 1] if i + 1 < len(seq) else None)
        def btn(x, cls, label):
            return (f'<a class="pg {cls}" href="/hunting/taiken/{x["slug"]}/" data-{cls}><small>{label}</small>'
                    f'<b>{x["icon"]} {escape(x["title"])}</b></a>') if x else '<span class="pg empty"></span>'
        out[f"/hunting/taiken/{a['slug']}/"] = (a["title"], a["desc"], f"""
<p class="muted small"><a href="/hunting/taiken/">体験記</a> › {ymd(a["date"])}</p>
<article class="panel article">
<h1>{a["icon"]} {escape(a["title"])}</h1>
{to_html(a["body"])}
</article>
{cta}
<div class="pager">{btn(prev, "prev", "← 前の話")}{btn(nxt, "next", "次の話 →")}</div>
<p><a href="/hunting/taiken/">体験記の一覧へ</a></p>
""")
    return out


def note_drafts():
    """note に貼る文章。サイトの記事へ戻るリンクには、どの記事から来たかを付ける"""
    out_dir = ROOT.parent / "hunting-app" / "docs" / "note" / "taiken"
    out_dir.mkdir(parents=True, exist_ok=True)
    for a in load():
        u = lambda path: f"{SITE}{path}?utm_source=note&utm_medium=article&utm_campaign=taiken-{a['slug']}"
        body = re.sub(r"^- ", "・", a["body"], flags=re.M)
        text = "\n".join([
            f"# {a['title']}", "",
            "ハッシュタグ: #狩猟 #狩猟免許 #ハンター #ジビエ #わな猟 #猟銃", "", "---", "",
            body, "", "---", "",
            "この体験記は、サイトにもまとめています。",
            f"👉 体験記の一覧: {u('/hunting/taiken/')}", "",
            "狩猟免許と猟銃講習の勉強には、アプリ「かりべん」を作りました。",
            "狩猟免許 600問・猟銃講習 759問、まぎらわしい数字のまとめ、合格予想の分析、取得までの手続きと期限の通知まで。",
            "まずは無料で。全部使うなら買い切り ¥800（月額料金・広告なし）。",
            f"👉 アプリの紹介: {u('/hunting/')}",
            "App Store: 【公開後にリンク】", "Google Play: 【公開後にリンク】", ""])
        p = out_dir / f"{a['slug']}.md"
        p.write_text(text, encoding="utf-8")
        print("note 用", p)


if __name__ == "__main__" and "--note" in sys.argv:
    note_drafts()
