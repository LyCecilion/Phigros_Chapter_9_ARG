(function () {
    "use strict";

    if (!window.Starfield) {
        return;
    }
    var a = (function () {
        var a = location.pathname;
        if (a === "" || a === "/") {
            return "/index.php";
        }
        if (/\/$/.test(a)) {
            return a.replace(/\/+$/, "") + "/index.php";
        }
        if (/\.(html?|php)$/i.test(a)) {
            return a.replace(/\/[^/]*$/, "") + "/index.php";
        }
        return a.replace(/\/+$/, "") + "/index.php";
    })();
    var b = location.protocol === "file:";
    var c = 130;
    var d = "player_messages";
    var e = 20;
    var f = 86400000;
    var g = 3500;
    var h = 10;
    var i = 0.5;
    var j = "&%*…（）￥#@?!·-=+";
    function k(a) {
        var b = document.cookie ? document.cookie.split("; ") : [];
        for (var c = 0; c < b.length; c++) {
            var d = b[c].indexOf("=");
            if (d > 0 && b[c].slice(0, d) === a) {
                return b[c].slice(d + 1);
            }
        }
        return null;
    }
    function l(a, b, c) {
        var d =
            a +
            "=" +
            b +
            "; Path=/; Max-Age=" +
            Math.max(0, Math.floor(c)) +
            "; SameSite=Lax";
        if (location.protocol === "https:") {
            d += "; Secure";
        }
        document.cookie = d;
    }
    function m(a) {
        l(a, "", 0);
    }
    function n(a) {
        var b = new TextEncoder().encode(a);
        var c = "";
        for (var d = 0; d < b.length; d++) {
            c += String.fromCharCode(b[d]);
        }
        return btoa(c)
            .replace(/\+/g, "-")
            .replace(/\//g, "_")
            .replace(/=+$/, "");
    }
    function o(a) {
        a = a.replace(/-/g, "+").replace(/_/g, "/");
        while (a.length % 4) {
            a += "=";
        }
        var b = atob(a);
        var c = new Uint8Array(b.length);
        for (var d = 0; d < b.length; d++) {
            c[d] = b.charCodeAt(d);
        }
        return new TextDecoder().decode(c);
    }
    function p() {
        var a = k(d);
        if (!a) {
            return [];
        }
        var b = [];
        try {
            var c = JSON.parse(o(a));
            if (Array.isArray(c)) {
                b = c;
            }
        } catch (a) {
            b = [];
        }
        var f = Date.now();
        var g = [];
        for (var h = 0; h < b.length; h++) {
            var i = b[h];
            if (!i || typeof i.text !== "string" || !i.text) {
                continue;
            }
            if (!i.exp || i.exp <= f) {
                continue;
            }
            g.push(i);
        }
        g.sort(function (a, b) {
            return (a.ts || 0) - (b.ts || 0);
        });
        return g.slice(-e);
    }
    function q(a) {
        a = a.slice(-e);
        while (a.length) {
            var b = n(JSON.stringify(a));
            if (b.length <= g || a.length === 1) {
                l(d, b, f / 1000);
                return a;
            }
            a.shift();
        }
        m(d);
        return [];
    }
    function r(a) {
        var b = p();
        b.push(a);
        return q(b);
    }
    var s = Object.create(null);
    var t = Object.create(null);
    var u = Object.create(null);
    function v() {
        var a = [];
        var b = Starfield.stars || [];
        for (var c = 0; c < b.length; c++) {
            if (b[c].pickable) {
                a.push(b[c]);
            }
        }
        return a;
    }
    function w(a) {
        var b = 2166136261 >>> 0;
        for (var c = 0; c < a.length; c++) {
            b ^= a.charCodeAt(c);
            b = Math.imul(b, 16777619);
        }
        return b >>> 0;
    }
    function x() {
        var a = p();
        var b = v();
        if (!b.length) {
            return;
        }
        var c = Object.create(null);
        for (var d = 0; d < a.length; d++) {
            var e = a[d];
            var f = t[e.id];
            var g = f ? Starfield.find(f) : null;
            if (!g || !g.pickable) {
                var h = w(String(e.id || e.ts || d)) % b.length;
                var i = null;
                for (var j = 0; j < b.length; j++) {
                    var k = b[(h + j) % b.length];
                    if (!c[k.id] && !s[k.id] && !k.message) {
                        i = k;
                        break;
                    }
                }
                f = i ? i.id : b[h].id;
            }
            t[e.id] = f;
            s[f] = true;
            c[f] = true;
            Starfield.setMessage(f, e.text, e.sender || null);
        }
    }
    function y() {
        var a = 2 + Math.floor(Math.random() * 4);
        var b = "";
        for (var c = 0; c < a; c++) {
            b += j.charAt(Math.floor(Math.random() * j.length));
        }
        return "——" + b;
    }
    function z(a) {
        if (!a || !a.length) {
            return;
        }
        var b = [];
        for (var c = 0; c < a.length; c++) {
            var d = String(a[c].text || "");
            if (d) {
                b.push({
                    text: d,
                    sender: y(),
                });
            }
        }
        if (!b.length) {
            return;
        }
        var e = v();
        var f = [];
        for (var g = 0; g < e.length; g++) {
            if (!s[e[g].id] && !u[e[g].id] && !e[g].message) {
                f.push(e[g]);
            }
        }
        for (var h = f.length - 1; h > 0; h--) {
            var j = Math.floor(Math.random() * (h + 1));
            var k = f[h];
            f[h] = f[j];
            f[j] = k;
        }
        var l = Math.floor(f.length * i);
        for (var m = 0; m < l; m++) {
            var n = f[m];
            var o = b[m % b.length];
            Starfield.setMessage(n.id, o.text, o.sender);
            u[n.id] = true;
        }
    }
    var A = document.querySelector('meta[name="page-token"]');
    var B = A ? String(A.content || "").trim() : "";
    if (!B || B === "__PAGE_TOKEN__") {
        B = null;
    }
    var C = null;
    var D = null;
    function E(b, c) {
        c = c || {};
        c.credentials = "same-origin";
        c.headers = c.headers || {};
        c.headers.Accept = "application/json";
        if (B) {
            c.headers["X-Page-Token"] = B;
        }
        if (c.body && C) {
            c.headers["X-CSRF-Token"] = C;
        }
        return fetch(a + "?api=" + b, c).then(function (a) {
            return a
                .json()
                .catch(function () {
                    return {};
                })
                .then(function (b) {
                    return {
                        status: a.status,
                        ok: a.ok,
                        data: b || {},
                    };
                });
        });
    }
    function F(a) {
        if (D && !a) {
            return D;
        }
        D = E("bootstrap", {
            method: "GET",
        })
            .then(function (a) {
                C =
                    a.status === 200 && a.data && a.data.csrf
                        ? a.data.csrf
                        : null;
                return !!C;
            })
            .catch(function () {
                C = null;
                return false;
            });
        return D;
    }
    function G(a, b, c) {
        return F()
            .then(function () {
                return E(a, b);
            })
            .then(function (d) {
                if (
                    !c &&
                    (d.status === 401 || d.status === 403 || d.status === 773)
                ) {
                    D = null;
                    return F(true).then(function () {
                        return E(a, b);
                    });
                }
                return d;
            });
    }
    function H() {
        if (b) {
            return Promise.resolve();
        }
        var a =
            (window.Starfield && Starfield.i18n && Starfield.i18n.lang) || "zh";
        return G("highlights&count=" + h + "&lang=" + a, {
            method: "GET",
        })
            .then(function (a) {
                if (
                    a.ok &&
                    a.data &&
                    a.data.ok &&
                    a.data.items &&
                    a.data.items.length
                ) {
                    z(a.data.items);
                }
            })
            .catch(function () {});
    }
    function I() {
        var a = new Uint8Array(16);
        if (window.crypto && crypto.getRandomValues) {
            crypto.getRandomValues(a);
        } else {
            for (var b = 0; b < a.length; b++) {
                a[b] = Math.floor(Math.random() * 256);
            }
        }
        var c = "";
        for (var d = 0; d < a.length; d++) {
            c += ("0" + a[d].toString(16)).slice(-2);
        }
        return c;
    }
    document.addEventListener("say:send", function (a) {
        var d = a.detail || {};
        var e = String(d.text || "");
        if (!e) {
            return;
        }
        if (Array.from(e).length > c) {
            return;
        }
        if (d.star && d.star.id) {
            s[d.star.id] = true;
            u[d.star.id] = true;
        }
        var g = I();
        var h = String(d.sender || "");
        function i(a, b) {
            var c = {
                id: a,
                text: e,
                sender: h,
                ts: Number(b) || Date.now(),
                exp: Date.now() + f,
            };
            if (d.star && d.star.id) {
                t[a] = d.star.id;
            }
            r(c);
        }
        if (b) {
            i(g);
            return;
        }
        G("messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text: e,
                rid: g,
            }),
        })
            .then(function (a) {
                var b = (a && a.data) || {};
                var c = !!(a && a.ok && b.ok);
                i(c ? String(b.id || g) : g, c ? b.ts : 0);
            })
            .catch(function (a) {
                i(g);
            });
    });
    x();
    if (!b) {
        F().then(H);
    } else if (window.console && console.info) {
        console.info(
            "[message] 以 file:// 打开：离线预览模式，已跳过全部后端请求",
        );
    }
    window.PlayerBackend = {
        maxChars: c,
        refreshHighlights: H,
        restoreOwn: x,
        localMessages: p,
    };
})();
