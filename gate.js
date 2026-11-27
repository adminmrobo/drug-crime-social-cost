/* 페이지 진입 비밀번호 확인. 비밀번호 원문은 저장하지 않고 SHA-256 값만 비교한다.
   주의: 화면 진입만 막는 장치이며, 저장소 파일 자체를 암호화하지는 않는다. */
(function () {
  var HASH = 'c9431c3aff907d2acfec27deaa8807e239b7c30d2cd6c4bdb789bcc7d6271a44', KEY = 'dcsc-gate';
  var de = document.documentElement;
  function ok() { try { return localStorage.getItem(KEY) === HASH || sessionStorage.getItem(KEY) === HASH; } catch (e) { return false; } }
  function save() { try { localStorage.setItem(KEY, HASH); } catch (e) { try { sessionStorage.setItem(KEY, HASH); } catch (e2) {} } }
  if (ok()) return;
  var st = document.createElement('style');
  st.id = 'gate-hide';
  st.textContent = 'body>*:not(#gate){display:none!important}body{margin:0}';
  de.appendChild(st);
  function hex(buf) { return Array.prototype.map.call(new Uint8Array(buf), function (b) { return ('0' + b.toString(16)).slice(-2); }).join(''); }
  function show() {
    var w = document.createElement('div');
    w.id = 'gate';
    w.setAttribute('style', 'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#f7f8fa;font:15px/1.6 "Apple SD Gothic Neo","Malgun Gothic",sans-serif;color:#18212f;z-index:2147483647');
    w.innerHTML = '<form style="background:#fff;border:1px solid #d5dbe3;border-radius:6px;padding:28px 30px;width:min(360px,90vw);box-sizing:border-box">' +
      '<div style="font-weight:700;font-size:17px;margin-bottom:4px">\ub9c8\uc57d\ub958 \uc0ac\ud68c\uc801 \ube44\uc6a9 \uc5f0\uad6c</div>' +
      '<div style="font-size:13px;color:#4a5566;margin-bottom:16px">\ube44\ubc00\ubc88\ud638\ub97c \uc785\ub825\ud558\uba74 \uc5f4\ub9bd\ub2c8\ub2e4.</div>' +
      '<input type="password" autocomplete="current-password" aria-label="\ube44\ubc00\ubc88\ud638" style="width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #b9c2cf;border-radius:4px;font-size:15px">' +
      '<button type="submit" style="margin-top:12px;width:100%;padding:10px;border:0;border-radius:4px;background:#1f3352;color:#fff;font-size:15px;cursor:pointer">\ub4e4\uc5b4\uac00\uae30</button>' +
      '<div role="alert" style="min-height:20px;margin-top:8px;font-size:13px;color:#b3261e"></div></form>';
    document.body.appendChild(w);
    var f = w.querySelector('form'), inp = w.querySelector('input'), msg = w.querySelector('[role=alert]');
    inp.focus();
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (!(window.crypto && crypto.subtle)) { msg.textContent = '\uc774 \ube0c\ub77c\uc6b0\uc800\uc5d0\uc11c\ub294 \ud655\uc778\ud560 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.'; return; }
      crypto.subtle.digest('SHA-256', new TextEncoder().encode(inp.value)).then(function (b) {
        if (hex(b) === HASH) { save(); w.remove(); var s = document.getElementById('gate-hide'); if (s) s.remove(); window.dispatchEvent(new Event('resize')); }
        else { msg.textContent = '\ube44\ubc00\ubc88\ud638\uac00 \ub9de\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.'; inp.select(); }
      });
    });
  }
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
