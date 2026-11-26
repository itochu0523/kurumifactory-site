"""目的別のランディングページ（検索・SNS からの入り口）。
数字・例題・まとめは、アプリの問題データから書き出した lp_data.json を使う（手で数字を書かない）。
更新: hunting-app で python3 tools/export_lp_data.py → このサイトで python3 tools/build.py"""
import hashlib
import json
from html import escape
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent / "lp_data.json").read_text(encoding="utf-8"))
C = DATA["counts"]
OX = {True: "○（正しい）", False: "×（誤り）"}


def quiz(items):
    """例題。答えは押すと開く（JavaScript なし）。3択は選択肢の並びを問題ごとに固定でずらす"""
    out = []
    for n, q in enumerate(items, 1):
        if q["type"] == "ox":
            choices = '<ol class="choices ox"><li>○</li><li>×</li></ol>'
            answer = OX[q["answer"]]
        else:
            shift = int(hashlib.md5(q["q"].encode()).hexdigest(), 16) % 3
            order = [(i + shift) % 3 for i in range(3)]
            choices = '<ol class="choices">' + "".join(f"<li>{escape(q['choices'][i])}</li>" for i in order) + "</ol>"
            answer = f"{'ABC'[order.index(q['answer'])]}. {escape(q['choices'][q['answer']])}"
        out.append(f"""<div class="quiz"><p class="qno">例題 {n}<span>{escape(q['topic'])}</span></p>
<p class="qtext">{escape(q['q'])}</p>{choices}
<details><summary>答えを見る</summary><p class="ans">正解: {answer}</p><p>{escape(q['explain'])}</p>
<p class="muted small">根拠: {escape(' / '.join(q['refs']))}</p></details></div>""")
    return "\n".join(out)


def table(sec):
    rows = []
    for it in sec["items"]:
        extra = "".join(f'<div class="tip">⚠️ {escape(it[k])}</div>' for k in ("tip",) if it.get(k))
        extra += f'<div class="muted small">{escape(it["note"])}</div>' if it.get("note") else ""
        rows.append(f"<tr><th>{escape(it['k'])}</th><td><b>{escape(it['v'])}</b>{extra}</td></tr>")
    return f'<h3>{escape(sec["title"])}</h3><table class="compare sum">' + "".join(rows) + "</table>"


def cta(app):
    return f"""<div class="cta">
<p class="cta-title">続きは「{app}」で</p>
<p>狩猟免許 {C['hunter']}問・猟銃講習 {C['gun']}問・まとめ {C['summary_items']}項目。<br>まずは無料で。全部使うなら<b>買い切り ¥800</b>（月額・広告なし）。</p>
<div class="stores"><span class="store" aria-disabled="true">App Store（近日公開）</span><span class="store" aria-disabled="true">Google Play（近日公開）</span></div>
<p><a class="btn" href="/hunting/">アプリのくわしい紹介を見る</a></p>
</div>"""


# 各ページ（並び順＝ページ送りの順）
LPS = [
    dict(path="/hunting/wana/", icon="🪤", short="わな猟免許", count=C["trap"], unit="問", fmt="3択",
         title="わな猟免許の試験対策", h1="わな猟免許の試験対策",
         desc=f"わな猟免許の知識試験に出る問題を、無料の例題つきで。わな猟の受験者向けに{C['trap']}問を収録した問題集アプリ。",
         lead="くくりわな・はこわなの違い、標識のルール、使えないわな。<br>わな猟の受験で問われるところを、問題を解きながら覚えます。",
         pains=["どの範囲を勉強すればいいかわからない", "使えるわな・使えないわなが覚えられない", "法令の数字がまぎらわしい"],
         note=f"わな猟の受験者に出る問題は {C['trap']}問（共通の法令・鳥獣・安全を含む）。受ける免許を選ぶと、関係する問題だけが出ます。",
         sums=[], sample="trap"),
    dict(path="/hunting/ami/", icon="🕸️", short="網猟免許", count=C["net"], unit="問", fmt="3択",
         title="網猟免許の試験対策", h1="網猟免許の試験対策",
         desc=f"網猟免許の知識試験に出る問題を、無料の例題つきで。網猟の受験者向けに{C['net']}問を収録した問題集アプリ。",
         lead="むそう網・はり網・つき網・なげ網。<br>使える網と、網ならではのルールを問題で覚えます。",
         pains=["使える網の種類がまぎらわしい", "カモの捕獲数など、網猟だけのルールが覚えられない", "参考書が少ない"],
         note=f"網猟の受験者に出る問題は {C['net']}問（共通の法令・鳥獣・安全を含む）。",
         sums=[], sample="net"),
    dict(path="/hunting/jyu/", icon="🎯", short="第一種銃猟免許", count=C["gun1"], unit="問", fmt="3択",
         title="第一種銃猟免許（猟銃）の試験対策", h1="第一種銃猟免許（猟銃）の試験対策",
         desc=f"第一種銃猟免許の知識試験に出る問題を、無料の例題つきで。銃猟の受験者向けに{C['gun1']}問を収録。猟銃等講習会の考査対策も。",
         lead="散弾の号数、番径、弾の届く距離、安全な取扱い。<br>銃の知識と法令を、問題を解きながら覚えます。",
         pains=["銃や実包の用語がむずかしい", "安全の問題で数字を問われる", "狩猟免許と猟銃の講習、両方の勉強が必要"],
         note=f"第一種銃猟の受験者に出る問題は {C['gun1']}問。猟銃等講習会の考査対策（{C['gun']}問）も同じアプリで。",
         sums=[], sample="gun1"),
    dict(path="/hunting/koushu/", icon="📝", short="猟銃等講習会", count=C["gun"], unit="問", fmt="○×",
         title="猟銃等講習会（初心者講習）の考査対策", h1="猟銃等講習会（初心者講習）の考査対策",
         desc=f"猟銃等講習会の考査に向けた○×問題{C['gun']}問。本番と同じ50問・60分の模擬考査つき。無料の例題あり。",
         lead="所持許可の手続き、保管・運搬、火薬類、安全な取扱い。<br>考査と同じ○×形式で、何度でも練習できます。",
         pains=["講習のテキストを読んでも、どこが問われるかわからない", "14日・3月など、手続きの期限が覚えられない", "本番の形で練習したい"],
         note=f"考査対策の○×問題は {C['gun']}問。本番と同じ50問・60分の模擬考査もできます。",
         sums=[], sample="koushu"),
    dict(path="/hunting/suji/", icon="🔢", short="まぎらわしい数字", count=sum(len(DATA["summary"][k]["items"]) for k in ("numbers_days", "numbers_years", "numbers_bag")), unit="項目", fmt="比較表",
         title="狩猟免許試験のまぎらわしい数字まとめ", h1="狩猟免許試験の「まぎらわしい数字」まとめ",
         desc="狩猟免許試験のひっかけで狙われる数字（30日・14日・1か月、3年・10年・20年、1日の捕獲数）を並べて比較。例題つき。",
         lead="「30日だっけ？14日だっけ？」<br>ひっかけで狙われる数字を、並べて比べて覚えます。",
         pains=["似た数字が混ざって選べない", "ひっかけ問題で落とす", "暗記カードを作る時間がない"],
         note="アプリの「まぎらわしい数字」の章では、関連する問題も解けて、正解した項目に「覚えた」の印が付きます。",
         sums=["numbers_days", "numbers_years", "numbers_bag"], sample="numbers"),
    dict(path="/hunting/chojyu/", icon="🦆", short="狩猟鳥獣の見分け", count=46, unit="種", fmt="見分け",
         title="狩猟鳥獣の見分け方・覚え方", h1="狩猟鳥獣の見分け方・覚え方",
         desc="狩猟鳥獣46種（鳥26・獣20）と、間違えやすい狩猟鳥獣ではない鳥獣。似た種を比べる例題つき。",
         lead="マガモとトモエガモ、ヒドリガモとアメリカヒドリ。<br>似ているのに「捕っていい」「いけない」が分かれる鳥獣を、比べて覚えます。",
         pains=["46種が覚えられない", "似た鳥の区別がつかない", "狩猟鳥獣から外れた種を知らない"],
         note="アプリには、似た鳥獣を比べる「狩猟鳥獣かどうか」の問題を76問収録しています。",
         sums=["species_ng"], sample="species"),
]
HUB = dict(path="/hunting/", icon="📊", short="アプリの紹介")
ORDER = [HUB] + LPS


def rail(current):
    """上部のパネル列（横にスクロール）。今のページを強調"""
    items = "".join(
        f'<a class="rail-item{" on" if x["path"] == current else ""}" href="{x["path"]}"'
        f'{" aria-current=page" if x["path"] == current else ""}><span>{x["icon"]}</span>{escape(x["short"])}</a>'
        for x in ORDER)
    return f'<nav class="rail" aria-label="対策ページ">{items}</nav>'


def pager(current):
    """下部の前後ボタン。スワイプ・矢印キーでも送れる（assets/pager.js）"""
    i = [x["path"] for x in ORDER].index(current)
    prev, nxt = ORDER[i - 1] if i > 0 else None, ORDER[i + 1] if i + 1 < len(ORDER) else ORDER[0]
    def btn(x, cls, label):
        return (f'<a class="pg {cls}" href="{x["path"]}" data-{cls}><small>{label}</small>'
                f'<b>{x["icon"]} {escape(x["short"])}</b></a>') if x else '<span class="pg empty"></span>'
    dots = "".join(f'<a class="dot{" on" if x["path"] == current else ""}" href="{x["path"]}" aria-label="{escape(x["short"])}"></a>' for x in ORDER)
    return f'<div class="pager">{btn(prev, "prev", "← 前へ")}{btn(nxt, "next", "次へ →" if i + 1 < len(ORDER) else "最初へ →")}</div><div class="dots">{dots}</div>'


def hub_panels():
    """紹介ページに置く、各対策ページへのパネル"""
    cards = "".join(
        f'<a class="panel link" href="{x["path"]}"><span class="p-icon">{x["icon"]}</span>'
        f'<span class="p-num">{x["count"]}<small>{x["unit"]}</small></span>'
        f'<b>{escape(x["short"])}</b><span class="muted small">{x["fmt"]}・例題3問 →</span></a>' for x in LPS)
    return f'<div class="panels">{cards}</div>'


def pages(app):
    out = {}
    for x in LPS:
        pain = "".join(f"<li>{escape(p)}</li>" for p in x["pains"])
        sums = "".join(f'<div class="panel">{table(DATA["summary"][k])}</div>' for k in x["sums"])
        out[x["path"]] = (x["title"], x["desc"], f"""
{rail(x["path"])}
<section class="panel hero">
<span class="badge">{x["icon"]} {escape(x["short"])}</span>
<h1>{escape(x["h1"])}</h1>
<p class="lead">{x["lead"]}</p>
<div class="tiles">
<div class="tile"><b>{x["count"]}<small>{x["unit"]}</small></b><span>アプリに収録</span></div>
<div class="tile"><b>{x["fmt"]}</b><span>形式</span></div>
<div class="tile"><b>3<small>問</small></b><span>無料の例題</span></div>
<div class="tile"><b>¥800</b><span>買い切り・広告なし</span></div>
</div>
</section>
<div class="panels two">
<section class="panel"><h2>こんな悩みに</h2><ul class="checks">{pain}</ul></section>
<section class="panel"><h2>アプリでは</h2><p>{escape(x["note"])}</p></section>
</div>
{sums}
<h2 class="sec">まずは解いてみよう</h2>
<div class="quizzes">{quiz(DATA["samples"][x["sample"]])}</div>
{cta(app)}
{pager(x["path"])}
<p class="muted small">本ページとアプリの問題は、法令・公的資料をもとに独自に作成したもので、公式の試験問題ではありません。法令は改正されることがあるため、受験・申請の前に都道府県・警察署の最新情報をご確認ください。</p>
""")
    return out
