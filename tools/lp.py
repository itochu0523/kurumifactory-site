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


# 各ページ: パス, タイトル, 説明, バッジ, 見出し, リード, こんな悩み, 本文（例題・まとめ）
LPS = [
    ("/hunting/wana/", "わな猟免許の試験対策", f"わな猟免許の知識試験に出る問題を、無料の例題つきで。わな猟の受験者向けに{C['trap']}問を収録した問題集アプリ。",
     "わな猟免許", "わな猟免許の試験対策",
     "くくりわな・はこわなの違い、標識のルール、使えないわな。<br>わな猟の受験で問われるところを、問題を解きながら覚えます。",
     ["どの範囲を勉強すればいいかわからない", "使えるわな・使えないわなが覚えられない", "法令の数字がまぎらわしい"],
     lambda: f"<p>わな猟免許の受験者に出る問題は、アプリに <b>{C['trap']}問</b>（共通の法令・鳥獣・安全を含む）。受ける免許を選ぶと、わな猟に関係する問題だけが出ます。</p>" + quiz(DATA["samples"]["trap"])),
    ("/hunting/ami/", "網猟免許の試験対策", f"網猟免許の知識試験に出る問題を、無料の例題つきで。網猟の受験者向けに{C['net']}問を収録した問題集アプリ。",
     "網猟免許", "網猟免許の試験対策",
     "むそう網・はり網・つき網・なげ網。<br>使える網と、網ならではのルールを問題で覚えます。",
     ["使える網の種類がまぎらわしい", "カモの捕獲数など、網猟だけのルールが覚えられない", "参考書が少ない"],
     lambda: f"<p>網猟免許の受験者に出る問題は、アプリに <b>{C['net']}問</b>（共通の法令・鳥獣・安全を含む）。</p>" + quiz(DATA["samples"]["net"])),
    ("/hunting/jyu/", "第一種銃猟免許（猟銃）の試験対策", f"第一種銃猟免許の知識試験に出る問題を、無料の例題つきで。銃猟の受験者向けに{C['gun1']}問を収録。猟銃等講習会の考査対策も。",
     "第一種銃猟免許", "第一種銃猟免許（猟銃）の試験対策",
     "散弾の号数、番径、弾の届く距離、安全な取扱い。<br>銃の知識と法令を、問題を解きながら覚えます。",
     ["銃や実包の用語がむずかしい", "安全の問題で数字を問われる", "狩猟免許と猟銃の講習、両方の勉強が必要"],
     lambda: f"<p>第一種銃猟免許の受験者に出る問題は、アプリに <b>{C['gun1']}問</b>。猟銃等講習会の考査対策（{C['gun']}問）も同じアプリで勉強できます。</p>" + quiz(DATA["samples"]["gun1"])),
    ("/hunting/koushu/", "猟銃等講習会（初心者講習）の考査対策", f"猟銃等講習会の考査に向けた○×問題{C['gun']}問。本番と同じ50問・60分の模擬考査つき。無料の例題あり。",
     "猟銃等講習会", "猟銃等講習会（初心者講習）の考査対策",
     "所持許可の手続き、保管・運搬、火薬類、安全な取扱い。<br>考査と同じ○×形式で、何度でも練習できます。",
     ["講習のテキストを読んでも、どこが問われるかわからない", "14日・3月など、手続きの期限が覚えられない", "本番の形で練習したい"],
     lambda: f"<p>アプリには考査対策の○×問題が <b>{C['gun']}問</b>。本番と同じ <b>50問・60分</b> の模擬考査もできます。</p>" + quiz(DATA["samples"]["koushu"])),
    ("/hunting/suji/", "狩猟免許試験のまぎらわしい数字まとめ", "狩猟免許試験のひっかけで狙われる数字（30日・14日・1か月、3年・10年・20年、1日の捕獲数）を並べて比較。例題つき。",
     "数字まとめ", "狩猟免許試験の「まぎらわしい数字」まとめ",
     "「30日だっけ？14日だっけ？」<br>ひっかけで狙われる数字を、並べて比べて覚えます。",
     ["似た数字が混ざって選べない", "ひっかけ問題で落とす", "暗記カードを作る時間がない"],
     lambda: table(DATA["summary"]["numbers_days"]) + table(DATA["summary"]["numbers_years"]) + table(DATA["summary"]["numbers_bag"])
     + "<h2>例題</h2>" + quiz(DATA["samples"]["numbers"])),
    ("/hunting/chojyu/", "狩猟鳥獣の見分け方・覚え方", "狩猟鳥獣46種（鳥26・獣20）と、間違えやすい狩猟鳥獣ではない鳥獣。似た種を比べる例題つき。",
     "狩猟鳥獣", "狩猟鳥獣の見分け方・覚え方",
     "マガモとトモエガモ、ヒドリガモとアメリカヒドリ。<br>似ているのに「捕っていい」「いけない」が分かれる鳥獣を、比べて覚えます。",
     ["46種が覚えられない", "似た鳥の区別がつかない", "狩猟鳥獣から外れた種を知らない"],
     lambda: table(DATA["summary"]["species_ng"]) + "<h2>例題</h2>" + quiz(DATA["samples"]["species"])),
]


def pages(app):
    out = {}
    links = "".join(f'<a class="chip" href="{p}">{escape(b)}</a>' for p, _, _, b, *_ in LPS)
    for path, title, desc, badge, h1, lead, pains, body in LPS:
        pain = "".join(f"<li>{escape(x)}</li>" for x in pains)
        out[path] = (title, desc, f"""
<span class="badge">{escape(badge)}</span>
<h1>{escape(h1)}</h1>
<p class="lead">{lead}</p>
<h2>こんな悩みに</h2>
<ul class="checks">{pain}</ul>
<h2>まずは解いてみよう</h2>
{body()}
{cta(app)}
<h2>ほかの対策ページ</h2>
<div class="chips">{links}</div>
<p class="muted small">本ページとアプリの問題は、法令・公的資料をもとに独自に作成したもので、公式の試験問題ではありません。法令は改正されることがあるため、受験・申請の前に都道府県・警察署の最新情報をご確認ください。</p>
""")
    return out
