"""公式サイトの各ページを共通の枠（ヘッダー・フッター）で生成する。
使い方: python3 tools/build.py  （ページ本文は PAGES を編集）"""
from pathlib import Path

from lp import hub_panels, pager, rail, pages as lp_pages

ROOT = Path(__file__).resolve().parent.parent
BRAND = "Kurumi Factory"
MAIL = "support@kurumifactory.com"
UPDATED = "2026年11月19日"
APP = "かりべん"  # アプリ名（2026-11-23 決定）
APP_DESC = "狩猟免許・猟銃講習の問題集"


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
<script src="/assets/pager.js" defer></script>
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
<p><b>{APP_DESC}</b></p>
<p class="muted">狩猟免許600問・猟銃講習759問。ひっかけと数字のまとめ、合格予想の分析、取得までの手続きと期限の通知まで。</p></a>
</div>
<h2>更新情報</h2>
{news_list(NEWS[:3])}
<p><a href="/news/">すべての更新情報 →</a></p>
<h2>お問い合わせ</h2>
<p>ご質問・不具合のご報告は <a href="/support/">サポート</a> からどうぞ。</p>
"""),
"/hunting/": (APP, "狩猟免許試験と猟銃等講習会の考査対策アプリ。狩猟免許600問・猟銃講習759問、ひっかけと数字のまとめ、合格予想の分析、取得までの手続きと期限の通知まで。", f"""
{rail("/hunting/")}
<span class="badge">iPhone・iPad・Android 準備中</span>
<h1>{APP}</h1>
<p><b>{APP_DESC}</b></p>
<p class="lead">「何を覚えればいいか」から「いつまでに何をするか」まで。<br>狩猟免許と猟銃の取得を、このアプリひとつで。</p>
<div class="stores">
<span class="store" aria-disabled="true">App Store（近日公開）</span>
<span class="store" aria-disabled="true">Google Play（近日公開）</span>
</div>
<p class="muted">公開したら、このページと<a href="/news/">更新情報</a>でお知らせします。</p>

<div class="stats">
<div class="stat"><b>600問</b><span>狩猟免許（3択）</span></div>
<div class="stat"><b>759問</b><span>猟銃講習（○×）</span></div>
<div class="stat"><b>210項目</b><span>体系まとめ（7章）</span></div>
<div class="stat"><b>22手順</b><span>取得までのやること</span></div>
</div>

<h2>こんな方に</h2>
<ul class="checks">
<li>狩猟免許（わな猟・網猟・第一種／第二種銃猟）の試験を受ける方</li>
<li>猟銃等講習会（初心者講習）の考査を受ける方</li>
<li>免許の申請から猟銃の所持許可、狩猟者登録までの流れと期限を整理したい方</li>
</ul>

<h2>できること</h2>
<div class="grid">
<div class="card"><h3>✍️ 狩猟免許の問題 600問</h3><p class="muted">法令・猟具・鳥獣・保護管理・安全を分野別に。持っている免許の種類に合わせて出題します。</p></div>
<div class="card"><h3>🎯 猟銃講習の問題 759問</h3><p class="muted">猟銃等講習会の考査に向けた ○× 演習。本番と同じ50問・60分の模擬考査も。</p></div>
<div class="card"><h3>⚠️ ひっかけ・数字に強くなる</h3><p class="muted">「30日と14日」「3年・10年・20年」など、間違えやすい数字を並べて比べる章と、ひっかけ問題を多数収録。</p></div>
<div class="card"><h3>📘 体系まとめ</h3><p class="muted">覚えれば取れる要点を分野ごとに整理。「隠して覚える」で答えを伏せて暗記チェック。覚えた項目には印が付きます。</p></div>
<div class="card"><h3>📈 分析とグラフ</h3><p class="muted">合格予想・毎日の学習量・正答率の推移・分野ごとの正答率・苦手な論点ランキング。苦手だけをまとめて解き直せます。</p></div>
<div class="card"><h3>🗓 取得までのやること</h3><p class="muted">免許 → 所持許可 → 狩猟者登録までの22の手順。日付を入れると法令どおりに期限を計算し、30日前・7日前・当日に通知します。</p></div>
<div class="card"><h3>📜 すべての問題に根拠</h3><p class="muted">各問題に、もとにした条文（例: 鳥獣法 第40条）や公的資料を表示。条文と自動で照らし合わせて確認しています。</p></div>
<div class="card"><h3>📴 オフライン・アカウント不要</h3><p class="muted">山の中でも勉強できます。登録不要で、学習記録は端末の中だけに保存します。</p></div>
</div>

<h2>試験別の対策（例題つき）</h2>
{hub_panels()}

<h2>無料版と有料版</h2>
<p>まずは無料でお試しいただけます。気に入っていただけたら、買い切りですべての機能が使えます。<b>月額料金（サブスクリプション）や広告はありません。</b></p>
<table class="compare">
<thead><tr><th></th><th>無料</th><th>すべて使える（買い切り ¥800）</th></tr></thead>
<tbody>
<tr><th>問題</th><td>分野ごとに20問まで</td><td class="paid">全1,359問</td></tr>
<tr><th>模擬試験・模擬考査</th><td>それぞれ1回</td><td class="paid">何度でも</td></tr>
<tr><th>体系まとめ</th><td>各試験の最初の1章</td><td class="paid">全7章（まぎらわしい数字の章を含む）</td></tr>
<tr><th>分析とグラフ</th><td>使えます</td><td class="paid">使えます</td></tr>
<tr><th>取得までのやること・期限の通知</th><td>使えます</td><td class="paid">使えます</td></tr>
<tr><th>問題の追加・法令改正への対応</th><td>無料の範囲に反映</td><td class="paid">すべてに反映（追加料金なし）</td></tr>
</tbody>
</table>
<p class="muted">購入は App Store / Google Play を通して行います。機種変更や再インストールのあとは、アプリの「購入を復元する」で、もう一度お支払いせずに使えます。</p>

<h2>サポートについて</h2>
<p>個人で作っているアプリだからこそ、一人ひとりのお問い合わせにきちんとお返事します。</p>
<ul class="checks">
<li><b>メールでのお問い合わせ</b>に、通常3営業日以内にお返事します（<a href="mailto:{MAIL}">{MAIL}</a>）</li>
<li><b>問題の誤りのご指摘</b>は、根拠の条文と照らして確認し、アップデートで修正します</li>
<li><b>法令の改正</b>があったときは、問題・まとめ・手続きの内容を見直して更新します</li>
<li><b>購入のトラブル</b>は「購入を復元する」と、ストアの窓口のご案内でサポートします</li>
<li>よくある質問は<a href="/support/">サポートページ</a>にまとめています</li>
</ul>

<h2>もとにしている公的な情報</h2>
<p class="muted">問題と解説は、次のような法令・公的資料をもとに、独自の文章で作成しています。</p>
<ul class="links">
<li><a href="https://laws.e-gov.go.jp/" rel="noopener">e-Gov 法令検索</a>（鳥獣保護管理法・銃刀法・火薬類取締法など）</li>
<li><a href="https://www.env.go.jp/nature/choju/docs/docs5/docs5-hanbetu.pdf" rel="noopener">環境省「狩猟鳥獣の見分け方」</a></li>
<li><a href="https://www.env.go.jp/nature/choju/capture/pdf/pdf4-1.pdf" rel="noopener">環境省「捕獲従事者研修テキスト」</a></li>
<li><a href="https://www.npa.go.jp/laws/notification/seian/hoan/hoantsutatu2/20_ryojyukousa.pdf" rel="noopener">警察庁「猟銃等講習会における考査の運用要領」</a></li>
</ul>

<h2>ご注意</h2>
<p class="muted">本アプリは公式の試験問題ではありません。試験の合格や許可の取得を保証するものではありません。法令は改正されることがあるため、受験・申請の前に必ず各都道府県・警察署の最新情報をご確認ください。</p>
<p class="muted"><a href="/privacy/">プライバシーポリシー</a>　<a href="/terms/">利用規約</a></p>

<h2>このアプリの更新情報</h2>
{news_list([n for n in NEWS if n[2] in ("", APP)][:5])}
<p><a href="/news/">すべての更新情報 →</a></p>
{pager("/hunting/")}
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
<details><summary>無料版と有料版の違いは？</summary><p>無料版は、問題が分野ごとに20問まで、模擬試験が1回、体系まとめが各試験の最初の1章です。買い切り（¥800）で、全問題・模擬試験の何度でも・まとめの全章が使えます。分析とグラフ、取得までのやること・期限の通知は無料でも使えます。月額料金や広告はありません。</p></details>
<details><summary>購入した機能が使えなくなりました。</summary><p>アプリの「設定 → 購入を復元する」を押してください。購入時と同じ Apple ID / Google アカウントでサインインしている必要があります。</p></details>
<details><summary>機種変更したとき、学習記録は引き継げますか？</summary><p>学習記録は端末の中だけに保存しているため、今は新しい端末に引き継げません（引き継ぎの機能は準備中です）。購入は「購入を復元する」で引き継げます。</p></details>
<details><summary>問題の内容が間違っている気がします。</summary><p>お手数ですが、問題の文章（またはスクリーンショット）を添えて、下記メールでお知らせください。根拠の条文と照らして確認し、修正します。</p></details>
<details><summary>この問題は本番の試験と同じですか？</summary><p>いいえ。公式の試験問題ではなく、法令・公的資料をもとに独自に作成した練習問題です。</p></details>
<details><summary>期限の通知が来ません。</summary><p>端末の「設定 → 通知」で、{APP} の通知が許可されているかご確認ください。</p></details>
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

PAGES.update(lp_pages(APP))

for path, (title, desc, body) in PAGES.items():
    out = ROOT / "index.html" if path == "/" else ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(layout(title, desc, body.strip(), path), encoding="utf-8")
    print("生成", out.relative_to(ROOT))

# 検索エンジン向け（ページを足したら自動で載る）
urls = "".join(f"<url><loc>https://kurumifactory.com{p}</loc></url>" for p in PAGES)
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://kurumifactory.com/sitemap.xml\n", encoding="utf-8")
print("生成 sitemap.xml robots.txt")
