// テーマ切替: 自動（端末の設定）→ ライト → ダーク の順に切り替え、選択は端末に保存する
(function () {
  var KEY = 'kf-theme';
  var ORDER = ['auto', 'light', 'dark'];
  var LABEL = { auto: '自動', light: 'ライト', dark: 'ダーク' };
  var ICON = { auto: '🌓', light: '☀️', dark: '🌙' };

  function current() {
    try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; }
  }
  function apply(mode) {
    var root = document.documentElement;
    if (mode === 'auto') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', mode);
    var btn = document.getElementById('theme-btn');
    if (btn) {
      btn.querySelector('.icon').textContent = ICON[mode];
      btn.querySelector('.label').textContent = LABEL[mode];
      btn.setAttribute('aria-label', '表示モード: ' + LABEL[mode] + '（押すと切り替え）');
    }
  }
  // 画面のちらつきを防ぐため、読み込み直後に一度適用する
  apply(current());
  document.addEventListener('DOMContentLoaded', function () {
    apply(current());
    var btn = document.getElementById('theme-btn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var next = ORDER[(ORDER.indexOf(current()) + 1) % ORDER.length];
      try { localStorage.setItem(KEY, next); } catch (e) {}
      apply(next);
    });
  });
})();
