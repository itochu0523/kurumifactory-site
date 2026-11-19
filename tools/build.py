"""公式サイトの各ページを共通の枠（ヘッダー・フッター）で生成する。
使い方: python3 tools/build.py  （ページ本文は PAGES を編集）"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRAND = "Kurumi Factory"
MAIL = "support@kurumifactory.com"
UPDATED = "2026年11月19日"
APP = "狩猟免許・猟銃講習 学習アプリ"  # 正式名が決まったら置き換える


# 更新情報（新しいものを上に追加する）。tag: release / update / fix / info
NEWS = [
    ("2026-11-19", "info", "", "公式サイトを公開しました。狩猟アプリは iPhone・iPad・Android 向けに準備中です。"),
]
TAG_LABEL = {"release": "リリース", "update": "アップデート", "fix": "修正", "info": "お知らせ"}


def news_list(items):
    rows = []
    for date, tag, app, text in items:
        y, m, d = date.split("-")
        app_html = f'<span class="app">{app}</span>' if app else ""
        rows.append(f'<li><time datetime="{date}">{y}年{int(m)}月{int(d)}日</time>'
                    f'<div><span class="tag tag-{tag}">{TAG_LABEL[tag]}</span>{app_html}<div>{text}</div></div></li>')
    return '<ul class="news">' + "".join(rows) + "</ul>"


def layout(title, desc, body, path):
    t = f"{title}｜{BRAND}" if title != BRAND else BRAND
    return f"""<!doctype html>
<html lang="ja"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="https://kurumifactory.com{path}"><meta property="og:type" content="website">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/theme.js"></script>
</head><body>
<header><div class="wrap"><a class="brand" href="/"><img src="/assets/favicon.svg" alt="">{BRAND}</a>
<div class="head-right"><nav><a href="/hunting/">狩猟アプリ</a><a href="/news/">更新情報</a><a href="/support/">サポート</a></nav>
<button id="theme-btn" class="theme-btn" type="button"><span class="icon">🌓</span><span class="label">自動</span></button></div></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap"><a href="/news/">更新情報</a><a href="/support/">サポート</a><a href="/privacy/">プライバシーポリシー</a><a href="/terms/">利用規約</a>
<p>&copy; 2026 {BRAND}</p></div></footer>
</body></html>
"""


PAGES = {
"/": ("Kurumi Factory", "毎日の「やりたい」を支える、小さくて使いやすいアプリをつくっています。", f"""
<h1>小さくて、ちゃんと使えるアプリを。</h1>
<p class="lead">Kurumi Factory は、自分が毎日使いたいと思えるアプリだけをつくる個人の工房です。</p>
<h2>アプリ</h2>
<div class="grid">
<a class="card" href="/hunting/" style="text-decoration:none;color:inherit">
<span class="badge">準備中</span><h3>{APP}</h3>
<p class="muted">狩猟免許の試験対策から、猟銃の所持許可までの手続きを一つのアプリで。</p></a>
</div>
<h2>更新情報</h2>
{news_list(NEWS[:3])}
<p><a href="/news/">すべての更新情報 →</a></p>
<h2>お問い合わせ</h2>
<p>ご質問・不具合のご報告は <a href="/support/">サポート</a> からどうぞ。</p>
"""),
"/hunting/": (APP, "狩猟免許試験と猟銃等講習会の対策、取得までの手続きをまとめて管理できる iPhone・iPad・Android アプリ。", f"""
<span class="badge">iPhone・iPad・Android 準備中</span>
<h1>{APP}</h1>
<p class="lead">「何を覚えればいいか」から「いつまでに何をするか」まで。<br>狩猟免許と猟銃の取得を、このアプリひとつで。</p>
<div class="grid">
<div class="card"><h3>📘 体系まとめ</h3><p class="muted">数字・期限・回数など、覚えれば取れる要点を分野ごとに整理。</p></div>
<div class="card"><h3>✍️ 狩猟免許の問題</h3><p class="muted">法令・猟具・鳥獣・保護管理を分野別に。苦手だけを繰り返す演習も。</p></div>
<div class="card"><h3>🎯 猟銃講習の問題</h3><p class="muted">猟銃等講習会の考査に向けた ○× 演習と模擬テスト。</p></div>
<div class="card"><h3>🗓 取得までのタスク</h3><p class="muted">免許 → 所持許可 → 登録までの手順と期限を通知でお知らせ。</p></div>
<div class="card"><h3>📈 学習記録と分析</h3><p class="muted">正答率・苦手分野・模試の履歴をひと目で。</p></div>
<div class="card"><h3>📴 オフラインで動く</h3><p class="muted">山の中でも勉強できます。データは端末の中に保存します。</p></div>
</div>
<h2>ご注意</h2>
<p class="muted">本アプリは公式の試験問題ではありません。問題と解説は法令・公的資料をもとに独自に作成しています。法令は改正されることがあるため、受験・申請の前に必ず各都道府県・警察署の最新情報をご確認ください。</p>
<h2>このアプリの更新情報</h2>
{news_list([n for n in NEWS if n[2] in ("", APP)][:5])}
<p><a href="/news/">すべての更新情報 →</a></p>
"""),
"/news/": ("更新情報", f"{BRAND}のアプリのリリース・アップデート・修正のお知らせ。", f"""
<h1>更新情報</h1>
<p class="lead">アプリのリリース、新しい機能、不具合の修正をお知らせします。</p>
{news_list(NEWS)}
"""),
"/support/": ("サポート", f"{APP}のよくある質問とお問い合わせ先。", f"""
<h1>サポート</h1>
<p class="lead">お困りのことがあれば、まずはよくある質問をご覧ください。</p>
<h2>よくある質問</h2>
<details><summary>機種変更したとき、学習記録は引き継げますか？</summary><p>アプリの「設定 → データの書き出し」でファイルを保存し、新しい端末で「読み込み」すると引き継げます。</p></details>
<details><summary>購入した機能が使えなくなりました。</summary><p>「設定 → 購入の復元」を押してください。購入時と同じ Apple ID / Google アカウントでログインしている必要があります。</p></details>
<details><summary>問題の内容が間違っている気がします。</summary><p>お手数ですが、問題の画面の「報告」ボタン、または下記メールでお知らせください。確認のうえ修正します。</p></details>
<details><summary>この問題は本番の試験と同じですか？</summary><p>いいえ。公式の試験問題ではなく、法令・公的資料をもとに独自に作成した練習問題です。</p></details>
<details><summary>返金してほしい。</summary><p>購入はストア（Apple / Google）を通して行われるため、返金は各ストアの窓口からお申し込みください。</p></details>
<h2>お問い合わせ</h2>
<div class="card"><p>メール: <a href="mailto:{MAIL}">{MAIL}</a></p>
<p class="muted">お使いの端末（例: iPhone 16）、OS のバージョン、アプリのバージョン、起きたことをお書き添えください。通常 3 営業日以内にお返事します。</p></div>
"""),
"/privacy/": ("プライバシーポリシー", f"{BRAND}のアプリとサイトにおける個人情報の取り扱い。", f"""
<h1>プライバシーポリシー</h1>
<p class="muted">最終更新: {UPDATED}</p>
<p>{BRAND}（以下「当方」）は、当方が提供するアプリ（以下「本アプリ」）およびこのサイトにおける利用者の情報を、以下のとおり取り扱います。</p>
<h2>1. 集める情報</h2>
<p>本アプリは、アカウント登録を必要とせず、氏名・メールアドレス・位置情報などの個人情報を当方のサーバーに送信しません。学習記録・タスク・設定は、利用者の端末の中にのみ保存されます。</p>
<h2>2. 購入について</h2>
<p>アプリ内の購入は Apple（App Store）または Google（Google Play）が処理します。当方はクレジットカード等の支払い情報を受け取りません。購入の有無の確認のため、ストアから購入記録（取引 ID 等）を受け取ることがあります。</p>
<h2>3. 通知</h2>
<p>期限のお知らせは、端末内で予約する通知（ローカル通知）を使います。通知の内容が外部に送られることはありません。</p>
<h2>4. 広告・解析</h2>
<p>本アプリは広告を表示せず、利用状況の解析ツールも組み込んでいません。このサイトも Cookie を使用していません。</p>
<h2>5. お問い合わせで頂いた情報</h2>
<p>メールでお問い合わせいただいた場合、頂いたメールアドレスと内容は、返信と不具合の修正のためにのみ使い、第三者に提供しません（法令に基づく場合を除きます）。</p>
<h2>6. 変更</h2>
<p>内容を変更する場合は、このページでお知らせします。</p>
<h2>7. お問い合わせ先</h2>
<p>{BRAND}　<a href="mailto:{MAIL}">{MAIL}</a></p>
"""),
"/terms/": ("利用規約", f"{BRAND}のアプリの利用規約。", f"""
<h1>利用規約</h1>
<p class="muted">最終更新: {UPDATED}</p>
<p>この規約は、{BRAND}（以下「当方」）が提供するアプリ（以下「本アプリ」）の利用条件を定めるものです。本アプリを利用された時点で、この規約に同意したものとみなします。</p>
<h2>1. 本アプリの内容</h2>
<p>本アプリの問題・解説・まとめは、法令および公的資料をもとに当方が独自に作成した学習用の情報です。公式の試験問題ではなく、試験の合格や許可の取得を保証するものではありません。</p>
<h2>2. 法令の改正</h2>
<p>法令や手続きは改正されることがあります。受験・申請・狩猟の際は、必ず都道府県・警察署等の最新の情報をご確認ください。</p>
<h2>3. 禁止事項</h2>
<p>本アプリの問題・文章・画像の無断転載、再配布、本アプリの改変・解析、その他法令に反する行為を禁止します。</p>
<h2>4. 有料機能</h2>
<p>有料機能の購入・返金は、各ストア（Apple / Google）の規約に従います。</p>
<h2>5. 免責</h2>
<p>当方は、本アプリの内容の正確さに努めますが、その完全性を保証しません。本アプリの利用によって生じた損害について、当方の故意または重大な過失による場合を除き、責任を負いません。</p>
<h2>6. 変更・終了</h2>
<p>当方は、本アプリの内容やこの規約を変更し、または提供を終了することがあります。</p>
<h2>7. 準拠法</h2>
<p>この規約は日本法に従って解釈されます。</p>
"""),
}

for path, (title, desc, body) in PAGES.items():
    out = ROOT / "index.html" if path == "/" else ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(layout(title, desc, body.strip(), path), encoding="utf-8")
    print("生成", out.relative_to(ROOT))
