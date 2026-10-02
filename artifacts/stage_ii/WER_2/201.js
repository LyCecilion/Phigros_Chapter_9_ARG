(function () {
    const b = "https://c9.gaoice.run/start.png";
    const c = new Image();
    c.fetchPriority = "high";
    c.decoding = "async";
    function d(a) {
        if (
            a.length < 8 ||
            a[0] !== 137 ||
            a[1] !== 80 ||
            a[2] !== 78 ||
            a[3] !== 71
        ) {
            return 0;
        }
        let b = 8;
        while (b + 8 <= a.length) {
            const c =
                ((a[b] << 24) |
                    (a[b + 1] << 16) |
                    (a[b + 2] << 8) |
                    a[b + 3]) >>>
                0;
            const d = String.fromCharCode(
                a[b + 4],
                a[b + 5],
                a[b + 6],
                a[b + 7],
            );
            b += 12 + c;
            if (b > a.length) {
                return 0;
            }
            if (d === "IEND") {
                return b;
            }
        }
        return 0;
    }
    (async function e() {
        try {
            const a = await (
                await fetch(b, {
                    credentials: "omit",
                })
            ).arrayBuffer();
            const e = new Uint8Array(a);
            const f = URL.createObjectURL(
                new Blob([e.subarray(d(e))], {
                    type: "image/png",
                }),
            );
            c.addEventListener(
                "load",
                function () {
                    // TOLOOK
                    setTimeout(function () {
                        URL.revokeObjectURL(f);
                    }, 2000);
                },
                {
                    once: true,
                },
            );
            c.src = f;
        } catch (a) {
            c.src = b;
        }
    })();
    document.addEventListener("contextmenu", function (a) {
        a.preventDefault();
    });
    let e = 1920;
    let f = 1080;
    const g = 1920;
    const h = 1080;
    const i = {
        speed: 0.6,
        strength: 12,
        cellPx: 4.5,
    };
    const j = document.getElementById("displace-canvas");
    const k = j.getContext("2d", {
        willReadFrequently: true,
    });
    const l = document.getElementById("fx-canvas");
    const m = l.getContext("2d");
    const n = {
        sparkCell: 8,
        sparkDensity: 0.4,
        sparkAlpha: 0.55,
        cell: 6,
        bigDensity: 0.06,
        moveSpeed: 1.4,
        flashRate: 2,
        onRatio: 0.7,
    };
    const o = /[?&]lite([&=]|$)/.test(location.search);
    const p = /[?&](black|nobg)([&=]|$)/.test(location.search);
    if (o) {
        i.cellPx = 8;
        i.speed = 0.22;
        n.sparkCell = 11;
        n.sparkDensity = 0.22;
        n.sparkAlpha = 0.5;
        n.cell = 9;
        n.bigDensity = 0.03;
        n.flashRate = 1.5;
    }
    function q(a, b, c) {
        return (ka(a + b * 7919 + c * 104729, 1) >>> 0) / 4294967296;
    }
    const r = document.createElement("canvas");
    const s = r.getContext("2d");
    let t = null;
    let u = 0;
    let v = 0;
    let w = null;
    const x = 64;
    const y = new Float32Array(x * x);
    const z = new Float32Array(x * x);
    (function a() {
        const b = ja(20260909);
        for (let a = 0; a < y.length; a++) {
            y[a] = b();
            z[a] = b();
        }
    })();
    function A(a, b, c) {
        const d = Math.floor(b);
        const e = Math.floor(c);
        const f = b - d;
        const g = c - e;
        const h = f * f * (3 - f * 2);
        const i = g * g * (3 - g * 2);
        const j = ((d % x) + x) % x;
        const k = ((e % x) + x) % x;
        const l = (j + 1) % x;
        const m = (k + 1) % x;
        const n = a[k * x + j];
        const o = a[k * x + l];
        const p = a[m * x + j];
        const q = a[m * x + l];
        return (n + (o - n) * h) * (1 - i) + (p + (q - p) * h) * i;
    }
    const B = o ? 16 : 8;
    const C = 1.56;
    const D = 0.9;
    const E = (3.8 / C) * D;
    const F = 0.0127 / C;
    const G = 0.017 / C;
    const H = 0.35 / C;
    const I = 132;
    const J = 36;
    const K = 40;
    const L = 0.15;
    const M = 0.3;
    const N = -0.25;
    const O = 0.45;
    const P = 2.4;
    const Q = 0.55;
    const R = 2.6;
    const S = document.getElementById("fog-canvas");
    const T = S
        ? S.getContext("2d", {
              willReadFrequently: true,
          })
        : null;
    let U = null;
    let V = null;
    let W = null;
    let X = null;
    let Y = 0;
    let Z = 0;
    const $ = new Float32Array(x * x);
    const _ = new Float32Array(x * x);
    const aa = new Float32Array(x * x);
    (function a() {
        const b = ja(20260913);
        for (let a = 0; a < $.length; a++) {
            $[a] = b();
            _[a] = b();
        }
        const c = ja(20260914);
        for (let a = 0; a < aa.length; a++) {
            aa[a] = c();
        }
    })();
    function ba() {
        if (!T) {
            return;
        }
        Y = Math.max(2, Math.ceil(e / B));
        Z = Math.max(2, Math.ceil(f / B));
        S.width = Y;
        S.height = Z;
        U = T.createImageData(Y, Z);
        V = new Float32Array(Y * Z);
        W = new Float32Array(Y * Z);
        X = new Float32Array(Y * Z);
    }
    function ca(a) {
        const b = Math.floor(a);
        const c = a - b;
        const d = c * c * (3 - c * 2);
        const e = (q(b, 3, 7) * 2 - 1) * 0.3;
        const f = (q(b + 1, 3, 7) * 2 - 1) * 0.3;
        return e + (f - e) * d;
    }
    function da(a) {
        if (!T || !U || !V || !X) {
            return;
        }
        const b = U.data;
        const c = a * E;
        const d = c * M;
        const e = c * 1.4;
        const f = ca(a * H);
        const g = F;
        const h = G;
        const i = P;
        const j = (d + f) * i;
        const k = Z * 0.3;
        let l = 0;
        for (let b = 0; b < Z; b++) {
            const a = b * B;
            const d = a * g - c;
            const f = a * h - e;
            const m = b < k ? 0.55 + (b / k) * 0.45 : 1;
            for (let a = 0; a < Y; a++) {
                const b = a * B;
                const c = b * g * i;
                const e = b * h * i;
                const k = A($, c + j, d) * 0.85 + A(_, e + j * 0.7, f) * 0.15;
                const n = A(_, c - j, d) * 0.85 + A($, e - j * 0.7, f) * 0.15;
                const o = (Math.max(k, n) - 0.5) * 2;
                const p = A(aa, c * R + 9.4, d * R + 31.7);
                X[l] = Q + (1 - Q) * p;
                let q = 0;
                const r = (o - N) / O;
                if (r > 0) {
                    const a = r < 1 ? r * r * (3 - r * 2) : 1;
                    q = a * L;
                }
                V[l++] = q * m;
            }
        }
        for (let b = 0; b < Z; b++) {
            const a = b * Y;
            const c = a + Y - 1;
            W[a] = (V[a] * 3 + V[a + 1]) * 0.25;
            for (let b = a + 1; b < c; b++) {
                W[b] = (V[b - 1] + V[b] * 2 + V[b + 1]) * 0.25;
            }
            W[c] = (V[c - 1] + V[c] * 3) * 0.25;
        }
        const m = (Z - 1) * Y;
        for (let b = 0; b < Y; b++) {
            V[b] = (W[b] * 3 + W[Y + b]) * 0.25;
            V[m + b] = (W[m - Y + b] + W[m + b] * 3) * 0.25;
        }
        for (let b = 1; b < Z - 1; b++) {
            const a = b * Y;
            for (let b = 0; b < Y; b++) {
                const c = a + b;
                V[c] = (W[c - Y] + W[c] * 2 + W[c + Y]) * 0.25;
            }
        }
        for (let c = 0, d = 0; c < V.length; c++, d += 4) {
            b[d] = I;
            b[d + 1] = J;
            b[d + 2] = K;
            b[d + 3] = (V[c] * X[c] * 255) | 0;
        }
        T.putImageData(U, 0, 0);
        if (!pa(S, T, la)) {
            na(S, T, la);
        }
    }
    function ea() {
        if (!c.complete || !c.naturalWidth) {
            return;
        }
        r.width = e;
        r.height = f;
        const a = Math.max(e / c.naturalWidth, f / c.naturalHeight);
        const b = c.naturalWidth * a;
        const d = c.naturalHeight * a;
        s.clearRect(0, 0, e, f);
        s.drawImage(c, (e - b) / 2, (f - d) / 2, b, d);
        u = r.width;
        v = r.height;
        try {
            t = s.getImageData(0, 0, u, v).data;
        } catch (a) {
            t = null;
        }
    }
    function fa() {
        j.width = Math.ceil(e / i.cellPx);
        j.height = Math.ceil(f / i.cellPx);
        w = null;
        l.width = Math.ceil(e / (o ? 4 : 3));
        l.height = Math.ceil(f / (o ? 4 : 3));
        ba();
        ea();
    }
    const ga = document.getElementById("scaler");
    function ha() {
        const a = window.innerWidth;
        const b = window.innerHeight;
        const c = Math.max(a / g, b / h);
        ga.style.transform =
            "translate(" +
            ((a - g * c) / 2).toFixed(3) +
            "px," +
            ((b - h * c) / 2).toFixed(3) +
            "px) scale(" +
            c.toFixed(6) +
            ")";
    }
    function ia() {
        ha();
    }
    window.addEventListener("resize", ia);
    if (c) {
        const a = () => {
            ea();
        };
        c.addEventListener("load", a, {
            once: true,
        });
        if (c.complete && c.naturalWidth) {
            a();
        }
    }
    fa();
    ha();
    function ja(a) {
        let b = a | 0;
        return function () {
            b = (b + 1831565813) | 0;
            let a = Math.imul(b ^ (b >>> 15), b | 1);
            a = (a + Math.imul(a ^ (a >>> 7), a | 61)) ^ a;
            return ((a ^ (a >>> 14)) >>> 0) / 4294967296;
        };
    }
    function ka(a, b) {
        let c = (a | 0) + ((b * 2654435761) | 0);
        c = ((c ^ (c >>> 16)) * 2246822507) | 0;
        return (c ^ (c >>> 13)) >>> 0;
    }
    const la = 0.25;
    let ma = null;
    function na(a, b, c, d) {
        const e = a.width;
        const f = a.height;
        if (!e || !f) {
            return;
        }
        if (!ma || ma.width !== e || ma.height !== f) {
            ma = document.createElement("canvas");
            ma.width = e;
            ma.height = f;
        }
        const g = ma.getContext("2d");
        g.clearRect(0, 0, e, f);
        g.drawImage(a, 0, 0);
        const h = (e - 1) * 0.5;
        const i = (f - 1) * 0.5;
        const j = 1 / Math.max(h, 1);
        const k = 1 / Math.max(i, 1);
        const l = 1 + c;
        const m = d || 16;
        b.clearRect(0, 0, e, f);
        function n(a, b) {
            const d = (a - h) * j;
            const e = (b - i) * k;
            return (1 + c * (d * d + e * e)) / l;
        }
        for (let g = 0; g < f; g += m) {
            const a = Math.min(m, f - g);
            for (let c = 0; c < e; c += m) {
                const d = Math.min(m, e - c);
                const j = c + d;
                const k = g + a;
                const l = n(c, g);
                const o = h + (c - h) * l;
                const p = i + (g - i) * l;
                const q = n(j, g);
                const r = h + (j - h) * q;
                const s = i + (g - i) * q;
                const t = n(c, k);
                const u = h + (c - h) * t;
                const v = i + (k - i) * t;
                const w = n(j, k);
                const x = h + (j - h) * w;
                const y = i + (k - i) * w;
                let z = Math.min(o, r, u, x) - 0.5;
                let A = Math.min(p, s, v, y) - 0.5;
                let B = Math.max(o, r, u, x) + 0.5;
                let C = Math.max(p, s, v, y) + 0.5;
                if (z < 0) {
                    z = 0;
                }
                if (A < 0) {
                    A = 0;
                }
                if (B > e) {
                    B = e;
                }
                if (C > f) {
                    C = f;
                }
                b.drawImage(ma, z, A, B - z, C - A, c, g, d, a);
            }
        }
    }
    const oa = new WeakMap();
    function pa(a, b, c) {
        const d = a.width;
        const e = a.height;
        if (!d || !e) {
            return false;
        }
        let f;
        try {
            f = b.getImageData(0, 0, d, e);
        } catch (a) {
            return false;
        }
        const g = f.data;
        let h = oa.get(a);
        if (h === undefined || h.w !== d || h.h !== e || h.k !== c) {
            const b = d * e;
            const f = new Int32Array(b);
            const g = new Int32Array(b);
            const i = new Int32Array(b);
            const j = new Int32Array(b);
            const k = new Float32Array(b);
            const l = new Float32Array(b);
            const m = new Float32Array(b);
            const n = new Float32Array(b);
            const o = (d - 1) * 0.5;
            const p = (e - 1) * 0.5;
            const q = 1 / Math.max(o, 1);
            const r = 1 / Math.max(p, 1);
            const s = 1 + c;
            const t = d - 1;
            const u = e - 1;
            let v = 0;
            for (let a = 0; a < e; a++) {
                const b = a - p;
                const e = b * r;
                const h = e * e;
                for (let a = 0; a < d; a++, v++) {
                    const e = a - o;
                    const r = e * q;
                    const w = (1 + c * (r * r + h)) / s;
                    let x = o + e * w;
                    let y = p + b * w;
                    if (x < 0) {
                        x = 0;
                    } else if (x > t) {
                        x = t;
                    }
                    if (y < 0) {
                        y = 0;
                    } else if (y > u) {
                        y = u;
                    }
                    const z = x | 0;
                    const A = y | 0;
                    const B = z < t ? z + 1 : z;
                    const C = A < u ? A + 1 : A;
                    const D = x - z;
                    const E = y - A;
                    const F = 1 - D;
                    const G = 1 - E;
                    const H = A * d;
                    const I = C * d;
                    f[v] = (H + z) << 2;
                    g[v] = (H + B) << 2;
                    i[v] = (I + z) << 2;
                    j[v] = (I + B) << 2;
                    k[v] = F * G;
                    l[v] = D * G;
                    m[v] = F * E;
                    n[v] = D * E;
                }
            }
            h = {
                w: d,
                h: e,
                k: c,
                n: b,
                o0: f,
                o1: g,
                o2: i,
                o3: j,
                e0: k,
                e1: l,
                e2: m,
                e3: n,
                dst: null,
            };
            oa.set(a, h);
        }
        if (h.dst === null || h.dst.width !== d || h.dst.height !== e) {
            h.dst = b.createImageData(d, e);
        }
        const i = h.dst.data;
        const j = h.n;
        const k = h.o0;
        const l = h.o1;
        const m = h.o2;
        const n = h.o3;
        const o = h.e0;
        const p = h.e1;
        const q = h.e2;
        const r = h.e3;
        for (let d = 0, e = 0; d < j; d++, e += 4) {
            const a = k[d];
            const b = l[d];
            const c = m[d];
            const f = n[d];
            const h = o[d];
            const j = p[d];
            const s = q[d];
            const t = r[d];
            i[e] = g[a] * h + g[b] * j + g[c] * s + g[f] * t;
            i[e + 1] =
                g[a + 1] * h + g[b + 1] * j + g[c + 1] * s + g[f + 1] * t;
            i[e + 2] =
                g[a + 2] * h + g[b + 2] * j + g[c + 2] * s + g[f + 2] * t;
            i[e + 3] =
                g[a + 3] * h + g[b + 3] * j + g[c + 3] * s + g[f + 3] * t;
        }
        b.putImageData(h.dst, 0, 0);
        return true;
    }
    function qa(a) {
        const b = j.width;
        const c = j.height;
        if (!b || !c) {
            return;
        }
        if (p) {
            k.fillStyle = "#000";
            k.fillRect(0, 0, b, c);
            return;
        }
        if (t) {
            ra(a, b, c);
        } else {
            sa(a, b, c);
        }
        if (!pa(j, k, la)) {
            na(j, k, la, o ? 24 : 16);
        }
    }
    function ra(a, b, c) {
        const d = i.cellPx;
        const e = i.strength;
        const f = i.speed;
        const g = 0.012;
        const h = a * f;
        if (!w || w.width !== b || w.height !== c) {
            w = k.createImageData(b, c);
        }
        const j = w.data;
        const l = 2;
        for (let f = 0; f < c; f += l) {
            const a = (f + l * 0.5) * d;
            const i = Math.min(l, c - f);
            for (let c = 0; c < b; c += l) {
                const k = (c + l * 0.5) * d;
                const m = (A(y, k * g + h * 0.8, a * g) - 0.5) * 2 * e;
                const n = (A(z, k * g, a * g + h * 0.8) - 0.5) * 2 * e;
                const o = Math.min(l, b - c);
                for (let a = 0; a < i; a++) {
                    const e = (f + a + 0.5) * d;
                    const g = (f + a) * b * 4;
                    for (let a = 0; a < o; a++) {
                        const b = (c + a + 0.5) * d;
                        let f = b + m;
                        let h = e + n;
                        if (f < 0) {
                            f = 0;
                        } else if (f >= u) {
                            f = u - 1;
                        }
                        if (h < 0) {
                            h = 0;
                        } else if (h >= v) {
                            h = v - 1;
                        }
                        const i = ((h | 0) * u + (f | 0)) * 4;
                        const k = g + (c + a) * 4;
                        j[k] = t[i];
                        j[k + 1] = t[i + 1];
                        j[k + 2] = t[i + 2];
                        j[k + 3] = 255;
                    }
                }
            }
        }
        k.putImageData(w, 0, 0);
    }
    function sa(a, b, c) {
        if (!r.width) {
            return;
        }
        k.clearRect(0, 0, b, c);
        const d = i.cellPx;
        const e = i.strength;
        const f = i.speed;
        const g = 0.012;
        const h = a * f;
        const j = o ? 6 : 3;
        const l = j * d;
        for (let f = 0; f < c; f += j) {
            for (let a = 0; a < b; a += j) {
                const b = (a + j * 0.5) * d;
                const c = (f + j * 0.5) * d;
                const i = (A(y, b * g + h * 0.8, c * g) - 0.5) * 2 * e;
                const m = (A(z, b * g, c * g + h * 0.8) - 0.5) * 2 * e;
                const n = l;
                let o = b - n / 2 + i;
                let p = c - n / 2 + m;
                if (o < 0) {
                    o = 0;
                } else if (o + n > u) {
                    o = u - n;
                }
                if (p < 0) {
                    p = 0;
                } else if (p + n > v) {
                    p = v - n;
                }
                k.drawImage(r, o, p, n, n, a, f, j, j);
            }
        }
    }
    function ta(a) {
        const b = l.width;
        const c = l.height;
        if (!b || !c) {
            return;
        }
        m.clearRect(0, 0, b, c);
        m.globalCompositeOperation = "lighter";
        const d = ["#ff4949", "#ff5454", "#ff2e2e"];
        const e = (a * 12) | 0;
        const f = n.sparkCell;
        const g = Math.ceil(b / f);
        const h = Math.ceil(c / f);
        for (let b = 0; b < h; b++) {
            for (let a = 0; a < g; a++) {
                const c = a + b * g;
                if (q(a, b, 3) >= n.sparkDensity) {
                    continue;
                }
                const h = ka(c * 101 + 13, e);
                if (h % 10 > 6) {
                    continue;
                }
                const i = 0.08 + (((h >>> 8) % 100) / 100) * n.sparkAlpha;
                const j = a * f + ((h >>> 0) % f);
                const k = b * f + ((h >>> 4) % f);
                const l = (h >>> 16) % 6;
                m.globalAlpha = i;
                m.fillStyle = d[l === 0 ? 0 : l < 4 ? 1 : 2];
                m.fillRect(j, k, 1, 1);
            }
        }
        const i = n.cell;
        const j = Math.ceil(b / i);
        const k = Math.ceil(c / i);
        const o = a * n.moveSpeed;
        const p = Math.floor(o);
        const r = o - p;
        const s = r * r * (3 - r * 2);
        for (let b = 0; b < k; b++) {
            for (let c = 0; c < j; c++) {
                const e = c + b * j;
                if (q(c, b, 5) >= n.bigDensity) {
                    continue;
                }
                const f = Math.floor(a * n.flashRate + q(c, b, 7) * 40);
                const g = ka(e * 31 + 7, f);
                if (g % 10 >= n.onRatio * 10) {
                    continue;
                }
                const h = q(c, b, 11 + (p % 97));
                const k = q(c, b, 31 + (p % 97));
                const l = q(c, b, 11 + ((p + 1) % 97));
                const o = q(c, b, 31 + ((p + 1) % 97));
                const r = (c + (h + (l - h) * s)) * i;
                const t = (b + (k + (o - k) * s)) * i;
                const u = ka(e, 12345);
                const v = 1 + ((u >>> 0) % 2);
                const w = 1 + ((u >>> 8) % 2);
                const x = 0.45 + ((u >>> 20) % 45) / 100;
                const y = (u >>> 16) % 6;
                m.globalAlpha = x;
                m.fillStyle = d[y === 0 ? 0 : y < 4 ? 1 : 2];
                m.fillRect(Math.floor(r), Math.floor(t), v, w);
            }
        }
        m.globalAlpha = 1;
        m.globalCompositeOperation = "source-over";
    }
    let ua = performance.now();
    let va = 0;
    let wa = 0;
    function xa(a) {
        requestAnimationFrame(xa);
        const b = Math.min((a - ua) / 1000, 0.1);
        ua = a;
        if (document.hidden) {
            return;
        }
        va += b;
        wa++;
        if (o && wa & 1) {
            return;
        }
        if (!o && (wa & 1) === 0) {
            qa(va);
        }
        if ((wa & 1) === 0) {
            da(va);
        }
        ta(va);
    }
    requestAnimationFrame(xa);
    if (o) {
        // TOLOOK
        setInterval(() => {
            if (!document.hidden) {
                qa(va);
            }
        }, 180);
    }
    const ya = document.getElementById("garble-canvas");
    const za = ya.getContext("2d");
    function Aa(a) {
        const b =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}<>?/\\|~";
        let c = "";
        for (let d = 0; d < a; d++) {
            c += b[Math.floor(Math.random() * b.length)];
        }
        return c;
    }
    const Ba = 0.7;
    let Ca = "";
    let Da = 1;
    function Ea() {
        return [Aa(2), Aa(2), Aa(2), Aa(2)].join(":");
    }
    function Fa() {
        Da += Ba;
        if (Da >= 1) {
            Da -= 1;
            Ca = Ea();
        }
        return Ca;
    }
    let Ga = null;
    let Ha = 0;
    function Ia(a, b) {
        const c = b * 0.0417;
        if (!Ga || Ha !== c) {
            const b = document.createElement("canvas");
            b.width = 1;
            b.height = Math.max(2, Math.round(c * 4));
            const d = b.getContext("2d");
            d.fillStyle = "rgba(255,255,255,0.95)";
            d.fillRect(0, 0, 1, b.height);
            d.fillStyle = "rgba(0,0,0,0.55)";
            for (let a = 0; a < b.height; a += c) {
                d.fillRect(0, a, 1, c * 0.5);
            }
            Ga = a.createPattern(b, "repeat");
            Ha = c;
        }
        return Ga;
    }
    function Ja() {
        const a = window.innerWidth;
        const b = window.innerHeight;
        if (ya.width !== a) {
            ya.width = a;
        }
        if (ya.height !== b) {
            ya.height = b;
        }
        const c = za;
        c.setTransform(1, 0, 0, 1, 0, 0);
        c.clearRect(0, 0, a, b);
        const d = a < 800;
        const e = d ? Math.max(40, Math.min(96, a * 0.12)) : a * 0.05;
        c.font = e + "px 'Saira Condensed', 'Microsoft YaHei', sans-serif";
        c.textAlign = "center";
        c.textBaseline = "middle";
        const f = Fa();
        const g = a / 2;
        const h = b / 2;
        const i = [];
        if (d) {
            const a = f.split(":");
            const b = e * 1.2;
            const c = h - ((a.length - 1) * b) / 2;
            a.forEach((a, d) =>
                i.push({
                    ch: a,
                    x: g,
                    y: c + d * b,
                }),
            );
        } else {
            const b = a * 0.8;
            const c = f.length;
            const d = e;
            const j = (b - c * d) / (c - 1);
            let k = g - b / 2 + d / 2;
            for (const a of f) {
                i.push({
                    ch: a,
                    x: k,
                    y: h,
                });
                k += d + j;
            }
        }
        c.save();
        c.shadowColor = "rgba(0,0,0,1)";
        c.shadowBlur = 48;
        c.shadowOffsetX = 0;
        c.shadowOffsetY = 0;
        c.fillStyle = "#000";
        for (let a = 0; a < 4; a++) {
            for (const a of i) {
                c.fillText(a.ch, a.x, a.y);
            }
        }
        c.restore();
        c.fillStyle = "rgba(255,45,45,0.5)";
        for (const a of i) {
            c.fillText(a.ch, a.x + 2, a.y);
        }
        c.fillStyle = "rgba(60,200,255,0.5)";
        for (const a of i) {
            c.fillText(a.ch, a.x - 2, a.y);
        }
        c.save();
        c.shadowColor = "rgba(255,255,255,0.35)";
        c.shadowBlur = 8;
        c.shadowOffsetX = 0;
        c.shadowOffsetY = 0;
        c.fillStyle = Ia(c, e);
        for (const a of i) {
            c.fillText(a.ch, a.x, a.y);
        }
        c.restore();
        na(ya, c, la, 8);
    }
    window.addEventListener("resize", Ja);
    // TOLOOK
    setInterval(Ja, 33);
    Ja();
    if (document.fonts && document.fonts.ready) {
        document.fonts.ready.then(Ja);
    }
    const Ka = document.getElementById("scanline-canvas");
    const La = Ka.getContext("2d");
    const Ma = 3;
    const Na = 0.16;
    function Oa() {
        const a = window.innerWidth;
        const b = window.innerHeight;
        if (Ka.width !== a) {
            Ka.width = a;
        }
        if (Ka.height !== b) {
            Ka.height = b;
        }
        const c = La;
        c.setTransform(1, 0, 0, 1, 0, 0);
        c.clearRect(0, 0, a, b);
        const d = document.createElement("canvas");
        d.width = 1;
        d.height = Ma;
        const e = d.getContext("2d");
        e.fillStyle = "rgba(0,0,0," + Na + ")";
        e.fillRect(0, 0, 1, 1);
        c.fillStyle = c.createPattern(d, "repeat");
        c.fillRect(0, 0, a, b);
        na(Ka, c, la, 8);
    }
    window.addEventListener("resize", Oa);
    Oa();
})();
