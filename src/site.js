(function () {
  var d = document;
  var root = d.documentElement;

  var burger = d.querySelector('.ppw-burger');
  var nav = d.getElementById('ppw-nav');
  var header = d.getElementById('ppw-header');

  function setMenu(open) {
    if (!burger) return;
    if (open && header) {
      root.style.setProperty('--ppw-nav-top', Math.max(header.getBoundingClientRect().bottom, 0) + 'px');
    }
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    root.classList.toggle('ppw-menu-open', open);
  }

  if (burger && nav) {
    burger.addEventListener('click', function () {
      setMenu(burger.getAttribute('aria-expanded') !== 'true');
    });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 1060) setMenu(false);
    });
    nav.querySelectorAll('.ppw-nav__toggle').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var li = btn.closest('li');
        var open = !li.classList.contains('is-open');
        li.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }

  var here = location.pathname.replace(/\/+$/, '') || '/';
  d.querySelectorAll('.ppw-nav a[href]').forEach(function (a) {
    var url;
    try { url = new URL(a.getAttribute('href'), location.href); } catch (e) { return; }
    if (url.host !== location.host) return;
    var path = url.pathname.replace(/\/+$/, '') || '/';
    if (path === here) {
      a.setAttribute('aria-current', 'page');
      var top = a.closest('.ppw-nav__list > li');
      if (top) top.classList.add('is-current');
    }
  });

  function copyText(text, done) {
    function fallback() {
      var ta = d.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.top = '0';
      ta.style.opacity = '0';
      d.body.appendChild(ta);
      ta.select();
      ta.setSelectionRange(0, text.length);
      try { d.execCommand('copy'); } catch (e) {}
      d.body.removeChild(ta);
      done();
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else {
      fallback();
    }
  }

  d.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-ppw-copy]');
    if (!btn) return;
    var label = btn.lastChild;
    var original = label.textContent;
    copyText(btn.getAttribute('data-ppw-copy'), function () {
      label.textContent = ' Skopiowano';
      btn.classList.add('is-done');
      setTimeout(function () {
        label.textContent = original;
        btn.classList.remove('is-done');
      }, 2000);
    });
  });

  d.querySelectorAll('[data-ppw-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
