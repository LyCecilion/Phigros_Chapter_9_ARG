(function () {
    "use strict";

    var a = {
        zh: {
            htmlLang: "zh-CN",
            title: "Sky of Your Vault",
            sayPlaceholder: "向无序的宇宙说点什么……",
            sayNamePlaceholder: "署名",
            saySend: "发送",
            dialogLabel: "提示",
            dialogBody: [
                "终于，你亦抵达了这里。",
                "带着你刚刚获得的答案回到该去的地方吧。",
                "还是说，你还在试图向着无序的宇宙呼唤，企图得到点什么回应？",
                "如果你想的话，说说便是，因为这已没有任何意义。",
            ],
            dialogClose: "关闭",
            sigPrefix: "——",
            anon: "无名",
        },
        en: {
            htmlLang: "en",
            title: "Sky of Your Vault",
            sayPlaceholder: "Send something to this universe...",
            sayNamePlaceholder: "Name",
            saySend: "Send",
            dialogLabel: "Notice",
            dialogBody: [
                "Finally, you too have arrived here.",
                "Take the answer you have just obtained, and go back to where you are meant to go.",
                "Or perhaps... you are still trying to call out toward the disordered universe, in hopes of some kind of response?",
                "...If you wish, just say it, for this no longer has any meaning.",
            ],
            dialogClose: "Close",
            sigPrefix: "—",
            anon: "anonymous",
        },
    };
    var b = (function () {
        var a = (
            navigator.language ||
            navigator.userLanguage ||
            "zh"
        ).toLowerCase();
        if (a.indexOf("zh") === 0) {
            return "zh";
        } else {
            return "en";
        }
    })();
    var c = a[b] || a.en;
    function d() {
        document.documentElement.lang = c.htmlLang;
        document.title = c.title;
        var a;
        if ((a = document.getElementById("say-text"))) {
            a.placeholder = c.sayPlaceholder;
        }
        if ((a = document.getElementById("say-name"))) {
            a.placeholder = c.sayNamePlaceholder;
        }
        if ((a = document.querySelector(".say__btn-label"))) {
            a.textContent = c.saySend;
        }
        var b = document.getElementById("end-dialog");
        if (!b) {
            return;
        }
        var d = b.querySelector(".phi-dialog__box");
        if (d) {
            d.setAttribute("aria-label", c.dialogLabel);
        }
        var e = b.querySelector(".phi-dialog__body");
        if (e) {
            e.textContent = "";
            for (var f = 0; f < c.dialogBody.length; f++) {
                var g = document.createElement("p");
                g.textContent = c.dialogBody[f];
                e.appendChild(g);
            }
        }
        var h = b.querySelector('[data-close="close"]');
        if (h) {
            h.textContent = c.dialogClose;
        }
    }
    d();
    var e = document.getElementById("sky");
    var f = e.getContext("2d", {
        alpha: false,
    });
    var g = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var h = 0;
    var i = 0;
    var j = Math.sqrt(3);
    var k = 1;
    var l = {
        x: -9999,
        y: -9999,
        inside: false,
    };
    var m = 12;
    var n = 10;
    var o = "rgba(49, 168, 202, 1)";
    var p = "rgba(189, 234, 247, 1)";
    var q = null;
    var r = null;
    var s = 1.8;
    var t = true;
    var u = 0;
    var v = 1;
    var w = [
        {
            key: "far",
            rate: 0.000175,
            rMin: 0.3,
            rMax: 0.72,
            aMin: 0.1,
            aMax: 0.34,
            pickable: false,
            wobMin: 3,
            wobMax: 5,
            spdMin: 0.1,
            spdMax: 0.28,
        },
        {
            key: "mid",
            rate: 0.000115,
            rMin: 0.65,
            rMax: 1.5,
            aMin: 0.28,
            aMax: 0.7,
            pickable: true,
            wobMin: 5,
            wobMax: 7,
            spdMin: 0.16,
            spdMax: 0.42,
        },
        {
            key: "near",
            rate: 0.000045,
            rMin: 1.3,
            rMax: 2.8,
            aMin: 0.62,
            aMax: 1,
            pickable: true,
            wobMin: 6.5,
            wobMax: 8.5,
            spdMin: 0.22,
            spdMax: 0.55,
        },
    ];
    var x = [
        [255, 255, 255],
        [255, 255, 255],
        [205, 224, 255],
        [255, 237, 214],
        [221, 207, 255],
    ];
    function y(a, b, c, d, e) {
        var f = "rgba(" + c + ",";
        var g = a.createLinearGradient(0, 0, b, 0);
        g.addColorStop(0, f + "0)");
        g.addColorStop(0.06, f + (e * 0.03).toFixed(3) + ")");
        g.addColorStop(0.18, f + (e * 0.12).toFixed(3) + ")");
        g.addColorStop(0.36, f + (e * 0.45).toFixed(3) + ")");
        g.addColorStop(0.5, f + e.toFixed(3) + ")");
        g.addColorStop(0.64, f + (e * 0.45).toFixed(3) + ")");
        g.addColorStop(0.82, f + (e * 0.12).toFixed(3) + ")");
        g.addColorStop(0.94, f + (e * 0.03).toFixed(3) + ")");
        g.addColorStop(1, f + "0)");
        a.fillStyle = g;
        a.fillRect(0, b / 2 - d / 2, b, d);
        a.save();
        a.translate(b / 2, b / 2);
        a.rotate(Math.PI / 2);
        a.translate(-b / 2, -b / 2);
        a.fillRect(0, b / 2 - d / 2, b, d);
        a.restore();
    }
    var z = x.map(function (a) {
        var b = 64;
        var c = document.createElement("canvas");
        c.width = c.height = b;
        var d = c.getContext("2d");
        var e = a[0] + "," + a[1] + "," + a[2];
        var f = "rgba(" + e + ",";
        var g = d.createRadialGradient(b / 2, b / 2, 0, b / 2, b / 2, b / 2);
        g.addColorStop(0, f + "1)");
        g.addColorStop(0.14, f + "0.85)");
        g.addColorStop(0.3, f + "0.22)");
        g.addColorStop(0.6, f + "0.045)");
        g.addColorStop(1, f + "0)");
        d.fillStyle = g;
        d.fillRect(0, 0, b, b);
        d.globalCompositeOperation = "lighter";
        y(d, b, e, 4.6, 0.1);
        y(d, b, e, 2.4, 0.22);
        y(d, b, e, 1.1, 0.55);
        return c;
    });
    var A = [];
    var B = [];
    var C = {};
    function D() {
        A = [];
        B = [];
        var a = h * i;
        var b = 0;
        var c = Math.min(1, a / 1296000);
        var d = h < 760 ? 0.75 : 1;
        for (var e = 0; e < w.length; e++) {
            var f = w[e];
            var g = Math.max(
                Math.round((f.key === "near" ? 190 : 500) * c),
                Math.round(a * f.rate * 7.5 * d),
            );
            for (var j = 0; j < g; j++) {
                var k = f.key === "near" && Math.random() < 0.22;
                var l = Math.min(
                    f.wobMin + Math.random() * (f.wobMax - f.wobMin),
                    n / 1.17,
                );
                var m = Math.random() * Math.PI * 2;
                var o = Math.asin(Math.random() * 2 - 1);
                var p = {
                    id: "S" + String(++b).padStart(4, "0"),
                    layer: f.key,
                    pickable: f.pickable,
                    nx: Math.cos(o) * Math.sin(m),
                    ny: -Math.sin(o),
                    nz: Math.cos(o) * Math.cos(m),
                    zv: 1,
                    hx: 0,
                    hy: 0,
                    wob: l,
                    wspd: f.spdMin + Math.random() * (f.spdMax - f.spdMin),
                    phase: Math.random() * Math.PI * 2,
                    phase2: Math.random() * Math.PI * 2,
                    r:
                        (f.rMin + Math.random() * (f.rMax - f.rMin)) *
                        (k ? 1.55 : 1),
                    alpha: f.aMin + Math.random() * (f.aMax - f.aMin),
                    tint: (Math.random() * x.length) | 0,
                    twinkle: 0.4 + Math.random() * 1.7,
                    data: {},
                    message: "",
                    sender: "",
                    hover: 0,
                    flash: 0,
                    sx: 0,
                    sy: 0,
                };
                if (C[p.id]) {
                    p.message = C[p.id].message;
                    p.sender = C[p.id].sender;
                }
                A.push(p);
                if (p.pickable) {
                    B.push(p);
                }
            }
        }
        var q = Object.keys(C);
        if (q.length && B.length) {
            var r = Object.create(null);
            for (var s = 0; s < A.length; s++) {
                if (A[s].pickable && C[A[s].id]) {
                    r[A[s].id] = 1;
                }
            }
            for (var t = 0; t < q.length; t++) {
                var u = q[t];
                var v = H(u);
                if (v && v.pickable) {
                    continue;
                }
                var y = C[u];
                delete C[u];
                if (v) {
                    v.message = "";
                    v.sender = "";
                }
                var z = 2166136261 >>> 0;
                for (var D = 0; D < u.length; D++) {
                    z ^= u.charCodeAt(D);
                    z = Math.imul(z, 16777619);
                }
                z = z >>> 0;
                var E = null;
                for (var F = 0; F < B.length; F++) {
                    var G = B[(z + F) % B.length];
                    if (!r[G.id]) {
                        E = G;
                        break;
                    }
                }
                if (!E) {
                    E = B[z % B.length];
                }
                C[E.id] = y;
                r[E.id] = 1;
                E.message = y.message;
                E.sender = y.sender;
            }
        }
        ra.stars = A;
    }
    var E = {
        left: 0,
        top: 0,
    };
    function F() {
        var a = Math.min(2, window.devicePixelRatio || 1);
        h = e.clientWidth || window.innerWidth;
        i = e.clientHeight || window.innerHeight;
        e.width = Math.round(h * a);
        e.height = Math.round(i * a);
        f.setTransform(a, 0, 0, a, 0, 0);
        var b = e.getBoundingClientRect();
        E.left = b.left;
        E.top = b.top;
        k = (Math.sqrt(h * h + i * i) * 0.5) / j;
        D();
        q = null;
    }
    function G(a, b) {
        var c = null;
        var d = Infinity;
        var e =
            ra.config.hitPad +
            (ca && (ca.pt === "touch" || ca.pt === "pen") ? 12 : 0);
        for (var f = 0; f < B.length; f++) {
            var g = B[f];
            if (g.zv <= 0.08) {
                continue;
            }
            var h = g.sx - a;
            var i = g.sy - b;
            var j = Math.sqrt(h * h + i * i);
            var k = g.r * 3.2 + e + g.hover * 10;
            if (j < k && j < d) {
                d = j;
                c = g;
            }
        }
        return c;
    }
    function H(a) {
        for (var b = 0; b < A.length; b++) {
            if (A[b].id === a) {
                return A[b];
            }
        }
        return null;
    }
    function I(a) {
        return {
            id: a.id,
            message: a.message,
            sender: a.sender,
            layer: a.layer,
            x: Math.round(a.sx),
            y: Math.round(a.sy),
            size: +a.r.toFixed(2),
            data: a.data,
            ref: a,
        };
    }
    function J(a, b) {
        var c;
        if (typeof window.CustomEvent === "function") {
            c = new CustomEvent(a, {
                detail: b,
            });
        } else {
            c = document.createEvent("CustomEvent");
            c.initCustomEvent(a, false, false, b);
        }
        document.dispatchEvent(c);
    }
    function K(a) {
        e.style.cursor = ca.on ? "grabbing" : a ? "pointer" : "grab";
        ra.hovered = a;
        var b = a ? I(a) : null;
        if (typeof ra.onStarHover === "function") {
            ra.onStarHover(b);
        }
        J("star:hover", b);
    }
    function L(a, b, c, d) {
        var e = Math.min(1, b);
        var h = z[a.tint];
        var i = d * (2 + e * 2);
        var j = 1.6 + e * 1.2;
        f.globalAlpha = e * 0.5;
        f.drawImage(h, a.sx - i / 2, a.sy - j / 2, i, j);
        f.drawImage(h, a.sx - j / 2, a.sy - i / 2, j, i);
        var k = 1 - Math.pow(1 - e, 3);
        var l = g ? 1 : 0.97 + Math.sin(c * 2.4) * 0.05;
        var m = (d * 0.62 + 7) * k * l;
        f.globalAlpha = e * (0.5 + e * 0.4);
        f.strokeStyle = o;
        f.lineWidth = 1.5;
        M(a.sx, a.sy, m, 0);
    }
    function M(a, b, c, d) {
        f.beginPath();
        for (var e = 0; e < 4; e++) {
            var g = d + (e * Math.PI) / 2;
            var h = a + Math.cos(g) * c;
            var i = b + Math.sin(g) * c;
            if (e === 0) {
                f.moveTo(h, i);
            } else {
                f.lineTo(h, i);
            }
        }
        f.closePath();
        f.stroke();
    }
    var N = performance.now();
    var O = [];
    var P = [];
    var Q = 5;
    function R(a) {
        var b = Math.min(0.05, (a - N) / 1000);
        N = a;
        var c = a / 1000;
        if (!ca.on && (ba.vyaw !== 0 || ba.vpitch !== 0)) {
            var d = Math.exp(-b * 4.2);
            ba.yaw += ba.vyaw * b;
            ba.pitch = ja(ba.pitch + ba.vpitch * b);
            ba.vyaw *= d;
            ba.vpitch *= d;
            if (Math.abs(ba.vyaw) < 0.01) {
                ba.vyaw = 0;
            }
            if (Math.abs(ba.vpitch) < 0.01) {
                ba.vpitch = 0;
            }
        }
        var e = Math.cos(ba.yaw);
        var j = Math.sin(ba.yaw);
        var m = Math.cos(ba.pitch);
        var n = Math.sin(ba.pitch);
        for (var o = 0; o < A.length; o++) {
            var p = A[o];
            var w = p.nx * e + p.nz * j;
            var x = p.nz * e - p.nx * j;
            var y = p.ny * m - x * n;
            var C = p.ny * n + x * m;
            p.zv = C;
            if (C > 0.06) {
                p.hx = h / 2 + (w / C) * k;
                p.hy = i / 2 + (y / C) * k;
            }
            if (g) {
                p.sx = p.hx;
                p.sy = p.hy;
                continue;
            }
            var D = c * p.wspd + p.phase;
            p.sx = p.hx + Math.cos(D) * p.wob;
            p.sy = p.hy + Math.sin(D * 0.63 + p.phase2) * p.wob * 0.6;
        }
        if (t) {
            u = 0;
        } else if (g) {
            u = 1;
        } else if (u < 1) {
            u = Math.min(1, u + b / s);
        }
        var E = q;
        q = l.inside && u >= 1 && !ca.on && !ka() ? G(l.x, l.y) : null;
        if (q !== E) {
            K(q);
        }
        var F = Math.min(1, b * 13);
        for (var H = 0; H < B.length; H++) {
            var I = B[H];
            var J = I === q || I === r ? 1 : 0;
            I.hover += (J - I.hover) * F;
            if (Math.abs(J - I.hover) < 0.003) {
                I.hover = J;
            }
            if (I.flash > 0) {
                I.flash -= b * 0.9;
                if (I.flash < 0) {
                    I.flash = 0;
                }
            }
        }
        f.globalCompositeOperation = "source-over";
        f.globalAlpha = 1;
        f.fillStyle = "#000000";
        f.fillRect(0, 0, h, i);
        var T = u;
        var U = Math.sqrt(h * h + i * i) * 0.5;
        v = T < 1 ? 0.45 + (1 - Math.pow(1 - T, 2.2)) * 0.55 : 1;
        f.save();
        if (v !== 1) {
            f.translate(h / 2, i / 2);
            f.scale(v, v);
            f.translate(-h / 2, -i / 2);
        }
        f.globalCompositeOperation = "lighter";
        for (var V = 0; V < A.length; V++) {
            var W = A[V];
            if (W.zv <= 0.06) {
                continue;
            }
            if (W.sx < -60 || W.sx > h + 60 || W.sy < -60 || W.sy > i + 60) {
                continue;
            }
            var X = 1;
            if (T < 1) {
                var Y = W.sx - h / 2;
                var Z = W.sy - i / 2;
                var $ = Math.sqrt(Y * Y + Z * Z) / U;
                X = (T - $ * 0.45) / 0.55;
                if (X <= 0) {
                    continue;
                }
                if (X > 1) {
                    X = 1;
                }
                X = X * X * (3 - X * 2);
            }
            var _ = W.message ? 1 : 0;
            var da = W.hover + W.flash * 0.9 + _ * 0.35;
            var ea = g ? 1 : 0.74 + Math.sin(c * W.twinkle + W.phase) * 0.26;
            var fa = Math.min(1, W.zv);
            var ga = 0.5 + fa * 0.5;
            var ha = (W.alpha * ea * (_ ? 1 : 0.55) + da * 0.7) * X * ga;
            if (ha > 1) {
                ha = 1;
            }
            if (ha <= 0.004) {
                continue;
            }
            var ia =
                (W.r * 7.5 * (1 + da * 1) + da * 9) *
                (0.35 + X * 0.65) *
                (0.78 + fa * 0.22);
            f.globalAlpha = ha;
            f.drawImage(z[W.tint], W.sx - ia / 2, W.sy - ia / 2, ia, ia);
            if (W.hover > 0.01 || _) {
                var la = ia * 0.7;
                f.globalAlpha = Math.min(1, W.hover * 0.95 + _ * 0.3);
                f.drawImage(z[0], W.sx - la / 2, W.sy - la / 2, la, la);
                if (W.hover > 0.01) {
                    L(W, W.hover, c, ia);
                }
            }
        }
        f.restore();
        f.globalAlpha = 1;
        for (var ma = O.length - 1; ma >= 0; ma--) {
            var na = O[ma];
            na.t += b;
            var oa = na.t / na.dur;
            if (oa >= 1) {
                O.splice(ma, 1);
                continue;
            }
            var pa = 1 - Math.pow(1 - oa, 2);
            f.globalAlpha = Math.pow(1 - oa, 2) * 0.75;
            f.strokeStyle = na.color;
            f.lineWidth = (1 - oa) * 2.4 + 0.4;
            M(na.x, na.y, 8 + pa * 118 * na.s, 0);
        }
        f.lineWidth = 1;
        if (!g && u >= 1) {
            Q -= b;
            if (Q <= 0) {
                Q = 7 + Math.random() * 12;
                if (P.length < 2) {
                    P.push(S());
                }
            }
            for (var qa = P.length - 1; qa >= 0; qa--) {
                var ra = P[qa];
                ra.x += ra.vx * b;
                ra.y += ra.vy * b;
                ra.life += b;
                if (ra.life > ra.dur) {
                    P.splice(qa, 1);
                    continue;
                }
                var sa =
                    Math.min(1, ra.life * 4) *
                    0.9 *
                    Math.pow(1 - ra.life / ra.dur, 2);
                var ta = ra.x - ra.vx * ra.tail;
                var ua = ra.y - ra.vy * ra.tail;
                var va = f.createLinearGradient(ra.x, ra.y, ta, ua);
                va.addColorStop(0, "rgba(255,255,255," + sa + ")");
                va.addColorStop(0.25, "rgba(198,224,255," + sa * 0.45 + ")");
                va.addColorStop(1, "rgba(140,180,255,0)");
                f.globalAlpha = 1;
                f.strokeStyle = va;
                f.lineWidth = ra.w;
                f.lineCap = "round";
                f.beginPath();
                f.moveTo(ra.x, ra.y);
                f.lineTo(ta, ua);
                f.stroke();
                f.lineCap = "butt";
                f.globalAlpha = sa * 0.9;
                f.drawImage(z[0], ra.x - 13, ra.y - 13, 26, 26);
            }
        }
        aa(b);
        f.globalAlpha = 1;
        f.globalCompositeOperation = "source-over";
        requestAnimationFrame(R);
    }
    function S() {
        var a = 0.22 + Math.random() * 0.72;
        var b = 380 + Math.random() * 340;
        return {
            x: -140 + Math.random() * (h + 280),
            y: -100 - Math.random() * 140,
            vx: Math.cos(a) * b,
            vy: Math.sin(a) * b,
            tail: 0.42,
            w: 1 + Math.random() * 1.2,
            life: 0,
            dur: 1.6 + Math.random() * 0.9,
        };
    }
    var T = document.getElementById("tip");
    var U = document.getElementById("tip-msg");
    var V = document.getElementById("tip-from");
    var W = null;
    var X = null;
    var Y = false;
    var Z = 0;
    var $ = 160;
    var _ = 60;
    function aa(a) {
        var b = q && (q.message || q.sender) ? q : null;
        if (!b && r && (r.message || r.sender)) {
            b = r;
        }
        if (b) {
            W = b;
        }
        Z += ((b ? 1 : 0) - Z) * Math.min(1, a * 15);
        if (!b && Z < 0.01) {
            Z = 0;
            W = null;
            if (Y) {
                Y = false;
                T.style.display = "none";
            }
            return;
        }
        var c = W;
        if (!c) {
            Z = 0;
            return;
        }
        var d = c.message;
        var e = c.sender;
        if (!Y) {
            Y = true;
            T.style.display = "block";
        }
        if (X !== c.id || U.textContent !== d || V.textContent !== e) {
            X = c.id;
            U.textContent = d;
            V.textContent = e;
            V.style.display = e ? "" : "none";
            $ = T.offsetWidth || $;
            _ = T.offsetHeight || _;
        }
        var f = Math.round(c.r * 9.3 + 22);
        var g = E.left + c.sx + f + $ > window.innerWidth - 8;
        var h = g ? E.left + c.sx - f - $ : E.left + c.sx + f;
        var i = ya && ya.classList.contains("show") ? 108 : 8;
        var j = Math.min(
            Math.max(8, E.top + c.sy - _ / 2),
            window.innerHeight - _ - i,
        );
        T.style.transformOrigin = g ? "right center" : "left center";
        T.style.opacity = Z.toFixed(3);
        T.style.transform =
            "translate(" +
            h.toFixed(1) +
            "px," +
            j.toFixed(1) +
            "px) scale(" +
            (0.9 + Z * 0.1).toFixed(3) +
            ")";
    }
    var ba = {
        yaw: 0,
        pitch: 0,
        vyaw: 0,
        vpitch: 0,
    };
    var ca = {
        on: false,
        x: 0,
        y: 0,
        moved: 0,
        t: 0,
        pt: "mouse",
    };
    var da = false;
    var ea = 1.6;
    var fa = 1.15;
    var ga = 6;
    var ha = 16;
    function ia() {
        if (ca.pt === "touch" || ca.pt === "pen") {
            return ha;
        } else {
            return ga;
        }
    }
    function ja(a) {
        if (a < -fa) {
            return -fa;
        } else if (a > fa) {
            return fa;
        } else {
            return a;
        }
    }
    function ka() {
        return Math.abs(ba.vyaw) * k > 45 || Math.abs(ba.vpitch) * k > 45;
    }
    function la(a) {
        l.x = a.clientX - E.left;
        l.y = a.clientY - E.top;
        l.inside = true;
        if (!ca.on) {
            return;
        }
        var b = a.clientX - ca.x;
        var c = a.clientY - ca.y;
        ca.x = a.clientX;
        ca.y = a.clientY;
        ca.moved += Math.abs(b) + Math.abs(c);
        if (r && ca.moved > ia()) {
            r = null;
        }
        var d = performance.now();
        var e = Math.max(0.008, (d - ca.t) / 1000);
        ca.t = d;
        var f = ea / Math.max(1, k);
        ba.yaw += b * f;
        ba.pitch = ja(ba.pitch - c * f);
        ba.vyaw = ba.vyaw * 0.65 + ((b * f) / e) * 0.35;
        ba.vpitch = ba.vpitch * 0.65 + ((-c * f) / e) * 0.35;
    }
    function ma(a) {
        if (a.pointerType === "mouse" && a.button !== 0) {
            return;
        }
        ca.pt = a.pointerType || "mouse";
        da = false;
        la(a);
        ca.on = true;
        ca.x = a.clientX;
        ca.y = a.clientY;
        ca.moved = 0;
        ca.t = performance.now();
        ba.vyaw = ba.vpitch = 0;
        e.style.cursor = "grabbing";
        if (e.setPointerCapture) {
            try {
                e.setPointerCapture(a.pointerId);
            } catch (a) {}
        }
    }
    function na(a) {
        if (!ca.on) {
            return;
        }
        ca.on = false;
        if (!a || g) {
            ba.vyaw = ba.vpitch = 0;
        } else {
            var b = 1400 / Math.max(1, k);
            ba.vyaw = Math.max(-b, Math.min(b, ba.vyaw));
            ba.vpitch = Math.max(-b, Math.min(b, ba.vpitch));
        }
        e.style.cursor = q ? "pointer" : "grab";
    }
    function oa() {
        l.inside = false;
        l.x = l.y = -9999;
    }
    function pa(a, b) {
        var c = a.clientX - E.left;
        var d = a.clientY - E.top;
        var e = u >= 1 ? G(c, d) : null;
        if (e) {
            if (b) {
                r = r === e ? null : e;
            } else {
                r = null;
            }
            O.push({
                x: e.sx,
                y: e.sy,
                t: 0,
                dur: 0.9,
                s: e.layer === "near" ? 1.2 : 0.85,
                color: p,
            });
            var f = I(e);
            if (typeof ra.onStarClick === "function") {
                ra.onStarClick(f, a);
            }
            J("star:click", {
                star: f,
                originalEvent: a,
            });
        } else {
            r = null;
            var g = {
                x: c,
                y: d,
            };
            if (typeof ra.onSkyClick === "function") {
                ra.onSkyClick(g, a);
            }
            J("sky:click", g);
        }
    }
    e.addEventListener("pointermove", la, {
        passive: true,
    });
    e.addEventListener("pointerdown", ma, {
        passive: true,
    });
    e.addEventListener(
        "pointerup",
        function (a) {
            var b = a.pointerType === "touch" || a.pointerType === "pen";
            if (b && ca.moved <= ia()) {
                na(false);
                da = true;
                pa(a, true);
                return;
            }
            na(true);
        },
        {
            passive: true,
        },
    );
    e.addEventListener(
        "pointercancel",
        function () {
            na(false);
        },
        {
            passive: true,
        },
    );
    e.addEventListener("pointerleave", oa);
    window.addEventListener("blur", function () {
        oa();
        na(false);
    });
    e.addEventListener("click", function (a) {
        if (da) {
            da = false;
            return;
        }
        if (ca.moved > ia()) {
            ca.moved = 0;
            r = null;
            return;
        }
        pa(a, ca.pt === "touch" || ca.pt === "pen");
    });
    var qa = null;
    window.addEventListener("resize", function () {
        clearTimeout(qa);
        qa = // TOLOOK
            setTimeout(F, 130);
    });
    var ra = {
        version: "2.2.0",
        stars: A,
        hovered: null,
        onStarHover: null,
        onStarClick: null,
        onSkyClick: null,
        config: {
            hitPad: m,
        },
        find: H,
        starAt: G,
        reveal: ua,
        rotation: ba,
        setRotation: function (a, b) {
            if (typeof a === "number") {
                ba.yaw = a;
            }
            if (typeof b === "number") {
                ba.pitch = ja(b);
            }
            ba.vyaw = ba.vpitch = 0;
        },
        i18n: {
            lang: b,
            texts: c,
        },
        setMessage: function (a, b, c) {
            var d = H(a);
            var e =
                C[a] ||
                (C[a] = {
                    message: "",
                    sender: "",
                });
            if (b != null) {
                e.message = String(b);
            }
            if (c != null) {
                e.sender = String(c);
            }
            if (d) {
                d.message = e.message;
                d.sender = e.sender;
            }
        },
    };
    window.Starfield = ra;
    var sa = document.getElementById("end-dialog");
    var ta = false;
    function ua() {
        if (!t) {
            return;
        }
        t = false;
        var a = 900;
        // TOLOOK
        setTimeout(function () {
            Ea();
        }, a);
    }
    function va() {
        if (ta || !sa) {
            return;
        }
        ta = true;
        sa.hidden = false;
        sa.classList.remove("phi-dialog--closing");
        J("dialog:open", {
            dialog: "end",
        });
    }
    function wa() {
        if (!sa) {
            return;
        }
        sa.hidden = true;
        sa.classList.remove("phi-dialog--closing");
    }
    function xa(a) {
        if (!ta || !sa) {
            return;
        }
        ta = false;
        J("dialog:close", {
            dialog: "end",
            action: a || "close",
        });
        ua();
        if (g) {
            wa();
            return;
        }
        sa.classList.add("phi-dialog--closing");
        var b = sa.querySelector(".phi-dialog__box");
        var c = false;
        function d() {
            if (c) {
                return;
            }
            c = true;
            b.removeEventListener("animationend", e);
            wa();
        }
        function e(a) {
            if (!a || a.target === b) {
                d();
            }
        }
        b.addEventListener("animationend", e);
        // TOLOOK
        setTimeout(d, 700);
    }
    if (sa) {
        sa.addEventListener("click", function (a) {
            var b = a.target.closest ? a.target.closest("[data-close]") : null;
            if (b) {
                xa(b.getAttribute("data-close"));
            }
        });
    }
    document.addEventListener("keydown", function (a) {
        if (a.key === "Escape" && ta) {
            xa("esc");
        }
    });
    window.EndDialog = {
        open: va,
        close: xa,
        isOpen: function () {
            return ta;
        },
    };
    if (sa) {
        // TOLOOK
        setTimeout(va, 500);
    } else {
        ua();
    }
    var ya = document.getElementById("say-wrap");
    var za = document.getElementById("say");
    var Aa = document.getElementById("say-text");
    var Ba = document.getElementById("say-name");
    var Ca = 520;
    var Da = 1180;
    function Ea() {
        if (!ya || ya.classList.contains("show")) {
            return;
        }
        ya.classList.add("show");
        if (g) {
            ya.classList.add("open", "label");
            return;
        }
        // TOLOOK
        setTimeout(function () {
            ya.classList.add("open");
        }, Ca);
        // TOLOOK
        setTimeout(function () {
            ya.classList.add("label");
        }, Da);
    }
    function Fa() {
        if (!ya) {
            return;
        }
        ya.classList.remove("show", "open", "label");
    }
    function Ga() {
        if (!B.length) {
            return null;
        }
        var a = h / 2;
        var b = i / 2;
        var c = Math.max(1, Math.min(h, i) * 0.5);
        var d = [0.85, 1.05, 1.25, 1.45];
        var e = [];
        for (var f = 0; f < d.length && e.length < 8; f++) {
            e = [];
            var g = d[f] * c;
            for (var j = 0; j < B.length; j++) {
                var k = B[j];
                if (k.zv <= 0.08) {
                    continue;
                }
                var l = k.hx - a;
                var m = k.hy - b;
                var n = Math.sqrt(l * l + m * m);
                if (n <= g) {
                    e.push({
                        star: k,
                        u: n / c,
                    });
                }
            }
        }
        if (!e.length) {
            return B[(Math.random() * B.length) | 0];
        }
        var o = [];
        var p = 0;
        for (var q = 0; q < e.length; q++) {
            var r = Math.exp((-e[q].u * e[q].u) / 0.2);
            o.push(r);
            p += r;
        }
        var s = Math.random() * p;
        for (var t = 0; t < e.length; t++) {
            s -= o[t];
            if (s <= 0) {
                return e[t].star;
            }
        }
        return e[e.length - 1].star;
    }
    function Ha(a, b) {
        a = (a || "").trim();
        if (!a) {
            return null;
        }
        var d = (b || "").trim();
        var e = d
            ? d.indexOf(c.sigPrefix) === 0
                ? d
                : c.sigPrefix + d
            : c.sigPrefix + c.anon;
        var f = Ga();
        if (f) {
            ra.setMessage(f.id, a, e);
            f.flash = 1;
            O.push({
                x: f.sx,
                y: f.sy,
                t: 0,
                dur: 1.1,
                s: f.layer === "near" ? 1.3 : 0.95,
                color: p,
            });
        }
        J("say:send", {
            text: a,
            sender: e,
            star: f ? I(f) : null,
        });
        if (f) {
            return I(f);
        } else {
            return null;
        }
    }
    if (za) {
        za.addEventListener("submit", function (a) {
            a.preventDefault();
            if (!Aa.value.trim()) {
                za.classList.remove("shake");
                za.offsetWidth;
                za.classList.add("shake");
                Aa.focus();
                J("say:empty", null);
                return;
            }
            Ha(Aa.value, Ba.value);
            Aa.value = "";
            Aa.focus();
        });
    }
    window.StarSay = {
        send: function (a, b) {
            return Ha(a, b);
        },
        focus: function () {
            if (Aa) {
                Aa.focus();
            }
        },
        show: Ea,
        hide: Fa,
    };
    F();
    requestAnimationFrame(function (a) {
        N = a;
        R(a);
    });
})();
