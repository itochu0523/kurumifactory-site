// 対策ページのページ送り: 左右スワイプ・矢印キーで前後のページへ。上のパネル列は今のページを見える位置に
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var prev = document.querySelector('[data-prev]');
    var next = document.querySelector('[data-next]');
    if (!prev && !next) return;
    var on = document.querySelector('.rail-item.on');
    if (on) on.scrollIntoView({ block: 'nearest', inline: 'center' });

    function go(a) { if (a) location.href = a.href; }
    document.addEventListener('keydown', function (e) {
      var t = e.target.tagName;
      if (t === 'INPUT' || t === 'TEXTAREA' || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'ArrowLeft') go(prev);
      if (e.key === 'ArrowRight') go(next);
    });
    // 横に大きく動かしたときだけ送る（縦スクロールやパネル列の横スクロールは邪魔しない）
    var x0 = null, y0 = 0;
    document.addEventListener('touchstart', function (e) {
      if (e.target.closest('.rail, table, .compare')) { x0 = null; return; }
      x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
    }, { passive: true });
    document.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      x0 = null;
      if (Math.abs(dx) > 80 && Math.abs(dx) > Math.abs(dy) * 2) go(dx < 0 ? next : prev);
    }, { passive: true });
  });
})();
