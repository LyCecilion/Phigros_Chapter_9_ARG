let a = 1920;
let b = 1080;
const c = 1920;
const d = 1080;
const e = {
    speed: 0.6,
    strength: 12,
    cellPx: 4.5,
};
const f = document.getElementById("displace-canvas");
const g = f.getContext("2d", {
    willReadFrequently: true,
});
const h = document.getElementById("fx-canvas");
const i = h.getContext("2d");
const j = {
    sparkCell: 8,
    sparkDensity: 0.4,
    sparkAlpha: 0.55,
    cell: 6,
    bigDensity: 0.06,
    moveSpeed: 1.4,
    flashRate: 2,
    onRatio: 0.7,
};
const k = /[?&]lite([&=]|$)/.test(location.search);
const l = /[?&](black|nobg)([&=]|$)/.test(location.search);
if (k) {
    e.cellPx = 8;
    e.speed = 0.22;
    j.sparkCell = 11;
    j.sparkDensity = 0.22;
    j.sparkAlpha = 0.5;
    j.cell = 9;
    j.bigDensity = 0.03;
    j.flashRate = 1.5;
}
function m(a, b, c) {
    return (ga(a + b * 7919 + c * 104729, 1) >>> 0) / 4294967296;
}
const n = document.createElement("canvas");
const o = n.getContext("2d");
let p = null;
let q = 0;
let r = 0;
let s = null;
const t = 64;
const u = new Float32Array(t * t);
const v = new Float32Array(t * t);
(function a() {
    const b = fa(20260909);
    for (let a = 0; a < u.length; a++) {
        u[a] = b();
        v[a] = b();
    }
})();
function w(a, b, c) {
    const d = Math.floor(b);
    const e = Math.floor(c);
    const f = b - d;
    const g = c - e;
    const h = f * f * (3 - f * 2);
    const i = g * g * (3 - g * 2);
    const j = ((d % t) + t) % t;
    const k = ((e % t) + t) % t;
    const l = (j + 1) % t;
    const m = (k + 1) % t;
    const n = a[k * t + j];
    const o = a[k * t + l];
    const p = a[m * t + j];
    const q = a[m * t + l];
    return (n + (o - n) * h) * (1 - i) + (p + (q - p) * h) * i;
}
const x = k ? 16 : 8;
const y = 1.56;
const z = 0.9;
const A = (3.8 / y) * z;
const B = 0.0127 / y;
const C = 0.017 / y;
const D = 0.35 / y;
const E = 132;
const F = 36;
const G = 40;
const H = 0.15;
const I = 0.3;
const J = -0.25;
const K = 0.45;
const L = 2.4;
const M = 0.55;
const N = 2.6;
const O = document.getElementById("fog-canvas");
const P = O
    ? O.getContext("2d", {
          willReadFrequently: true,
      })
    : null;
let Q = null;
let R = null;
let S = null;
let T = null;
let U = 0;
let V = 0;
const W = new Float32Array(t * t);
const X = new Float32Array(t * t);
const Y = new Float32Array(t * t);
(function a() {
    const b = fa(20260913);
    for (let a = 0; a < W.length; a++) {
        W[a] = b();
        X[a] = b();
    }
    const c = fa(20260914);
    for (let a = 0; a < Y.length; a++) {
        Y[a] = c();
    }
})();
function Z() {
    if (!P) {
        return;
    }
    U = Math.max(2, Math.ceil(a / x));
    V = Math.max(2, Math.ceil(b / x));
    O.width = U;
    O.height = V;
    Q = P.createImageData(U, V);
    R = new Float32Array(U * V);
    S = new Float32Array(U * V);
    T = new Float32Array(U * V);
}
function $(a) {
    const b = Math.floor(a);
    const c = a - b;
    const d = c * c * (3 - c * 2);
    const e = (m(b, 3, 7) * 2 - 1) * 0.3;
    const f = (m(b + 1, 3, 7) * 2 - 1) * 0.3;
    return e + (f - e) * d;
}
function _(a) {
    if (!P || !Q || !R || !T) {
        return;
    }
    const b = Q.data;
    const c = a * A;
    const d = c * I;
    const e = c * 1.4;
    const f = $(a * D);
    const g = B;
    const h = C;
    const i = L;
    const j = (d + f) * i;
    const k = V * 0.3;
    let l = 0;
    for (let b = 0; b < V; b++) {
        const a = b * x;
        const d = a * g - c;
        const f = a * h - e;
        const m = b < k ? 0.55 + (b / k) * 0.45 : 1;
        for (let a = 0; a < U; a++) {
            const b = a * x;
            const c = b * g * i;
            const e = b * h * i;
            const k = w(W, c + j, d) * 0.85 + w(X, e + j * 0.7, f) * 0.15;
            const n = w(X, c - j, d) * 0.85 + w(W, e - j * 0.7, f) * 0.15;
            const o = (Math.max(k, n) - 0.5) * 2;
            const p = w(Y, c * N + 9.4, d * N + 31.7);
            T[l] = M + (1 - M) * p;
            let q = 0;
            const r = (o - J) / K;
            if (r > 0) {
                const a = r < 1 ? r * r * (3 - r * 2) : 1;
                q = a * H;
            }
            R[l++] = q * m;
        }
    }
    for (let b = 0; b < V; b++) {
        const a = b * U;
        const c = a + U - 1;
        S[a] = (R[a] * 3 + R[a + 1]) * 0.25;
        for (let b = a + 1; b < c; b++) {
            S[b] = (R[b - 1] + R[b] * 2 + R[b + 1]) * 0.25;
        }
        S[c] = (R[c - 1] + R[c] * 3) * 0.25;
    }
    const m = (V - 1) * U;
    for (let b = 0; b < U; b++) {
        R[b] = (S[b] * 3 + S[U + b]) * 0.25;
        R[m + b] = (S[m - U + b] + S[m + b] * 3) * 0.25;
    }
    for (let b = 1; b < V - 1; b++) {
        const a = b * U;
        for (let b = 0; b < U; b++) {
            const c = a + b;
            R[c] = (S[c - U] + S[c] * 2 + S[c + U]) * 0.25;
        }
    }
    for (let c = 0, d = 0; c < R.length; c++, d += 4) {
        b[d] = E;
        b[d + 1] = F;
        b[d + 2] = G;
        b[d + 3] = (R[c] * T[c] * 255) | 0;
    }
    P.putImageData(Q, 0, 0);
    if (!la(O, P, ha)) {
        ja(O, P, ha);
    }
}
function aa() {
    if (!bgImg.complete || !bgImg.naturalWidth) {
        return;
    }
    n.width = a;
    n.height = b;
    const c = Math.max(a / bgImg.naturalWidth, b / bgImg.naturalHeight);
    const d = bgImg.naturalWidth * c;
    const e = bgImg.naturalHeight * c;
    o.clearRect(0, 0, a, b);
    o.drawImage(bgImg, (a - d) / 2, (b - e) / 2, d, e);
    q = n.width;
    r = n.height;
    try {
        p = o.getImageData(0, 0, q, r).data;
    } catch (a) {
        p = null;
    }
}
function ba() {
    f.width = Math.ceil(a / e.cellPx);
    f.height = Math.ceil(b / e.cellPx);
    s = null;
    h.width = Math.ceil(a / (k ? 4 : 3));
    h.height = Math.ceil(b / (k ? 4 : 3));
    Z();
    aa();
}
const ca = document.getElementById("scaler");
function da() {
    const a = window.innerWidth;
    const b = window.innerHeight;
    const e = Math.max(a / c, b / d);
    ca.style.transform =
        "translate(" +
        ((a - c * e) / 2).toFixed(3) +
        "px," +
        ((b - d * e) / 2).toFixed(3) +
        "px) scale(" +
        e.toFixed(6) +
        ")";
}
function ea() {
    da();
}
window.addEventListener("resize", ea);
if (bgImg) {
    const a = () => {
        aa();
    };
    bgImg.addEventListener("load", a, {
        once: true,
    });
    if (bgImg.complete && bgImg.naturalWidth) {
        a();
    }
}
ba();
da();
function fa(a) {
    let b = a | 0;
    return function () {
        b = (b + 1831565813) | 0;
        let a = Math.imul(b ^ (b >>> 15), b | 1);
        a = (a + Math.imul(a ^ (a >>> 7), a | 61)) ^ a;
        return ((a ^ (a >>> 14)) >>> 0) / 4294967296;
    };
}
function ga(a, b) {
    let c = (a | 0) + ((b * 2654435761) | 0);
    c = ((c ^ (c >>> 16)) * 2246822507) | 0;
    return (c ^ (c >>> 13)) >>> 0;
}
const ha = 0.25;
let ia = null;
function ja(a, b, c, d) {
    const e = a.width;
    const f = a.height;
    if (!e || !f) {
        return;
    }
    if (!ia || ia.width !== e || ia.height !== f) {
        ia = document.createElement("canvas");
        ia.width = e;
        ia.height = f;
    }
    const g = ia.getContext("2d");
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
            b.drawImage(ia, z, A, B - z, C - A, c, g, d, a);
        }
    }
}
const ka = new WeakMap();
function la(a, b, c) {
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
    let h = ka.get(a);
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
        ka.set(a, h);
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
        i[e + 1] = g[a + 1] * h + g[b + 1] * j + g[c + 1] * s + g[f + 1] * t;
        i[e + 2] = g[a + 2] * h + g[b + 2] * j + g[c + 2] * s + g[f + 2] * t;
        i[e + 3] = g[a + 3] * h + g[b + 3] * j + g[c + 3] * s + g[f + 3] * t;
    }
    b.putImageData(h.dst, 0, 0);
    return true;
}
function ma(a) {
    const b = f.width;
    const c = f.height;
    if (!b || !c) {
        return;
    }
    if (l) {
        g.fillStyle = "#000";
        g.fillRect(0, 0, b, c);
        return;
    }
    if (p) {
        na(a, b, c);
    } else {
        oa(a, b, c);
    }
    if (!la(f, g, ha)) {
        ja(f, g, ha, k ? 24 : 16);
    }
}
function na(a, b, c) {
    const d = e.cellPx;
    const f = e.strength;
    const h = e.speed;
    const i = 0.012;
    const j = a * h;
    if (!s || s.width !== b || s.height !== c) {
        s = g.createImageData(b, c);
    }
    const k = s.data;
    const l = 2;
    for (let e = 0; e < c; e += l) {
        const a = (e + l * 0.5) * d;
        const g = Math.min(l, c - e);
        for (let c = 0; c < b; c += l) {
            const h = (c + l * 0.5) * d;
            const m = (w(u, h * i + j * 0.8, a * i) - 0.5) * 2 * f;
            const n = (w(v, h * i, a * i + j * 0.8) - 0.5) * 2 * f;
            const o = Math.min(l, b - c);
            for (let a = 0; a < g; a++) {
                const f = (e + a + 0.5) * d;
                const g = (e + a) * b * 4;
                for (let a = 0; a < o; a++) {
                    const b = (c + a + 0.5) * d;
                    let e = b + m;
                    let h = f + n;
                    if (e < 0) {
                        e = 0;
                    } else if (e >= q) {
                        e = q - 1;
                    }
                    if (h < 0) {
                        h = 0;
                    } else if (h >= r) {
                        h = r - 1;
                    }
                    const i = ((h | 0) * q + (e | 0)) * 4;
                    const j = g + (c + a) * 4;
                    k[j] = p[i];
                    k[j + 1] = p[i + 1];
                    k[j + 2] = p[i + 2];
                    k[j + 3] = 255;
                }
            }
        }
    }
    g.putImageData(s, 0, 0);
}
function oa(a, b, c) {
    if (!n.width) {
        return;
    }
    g.clearRect(0, 0, b, c);
    const d = e.cellPx;
    const f = e.strength;
    const h = e.speed;
    const i = 0.012;
    const j = a * h;
    const l = k ? 6 : 3;
    const m = l * d;
    for (let e = 0; e < c; e += l) {
        for (let a = 0; a < b; a += l) {
            const b = (a + l * 0.5) * d;
            const c = (e + l * 0.5) * d;
            const h = (w(u, b * i + j * 0.8, c * i) - 0.5) * 2 * f;
            const k = (w(v, b * i, c * i + j * 0.8) - 0.5) * 2 * f;
            const o = m;
            let p = b - o / 2 + h;
            let s = c - o / 2 + k;
            if (p < 0) {
                p = 0;
            } else if (p + o > q) {
                p = q - o;
            }
            if (s < 0) {
                s = 0;
            } else if (s + o > r) {
                s = r - o;
            }
            g.drawImage(n, p, s, o, o, a, e, l, l);
        }
    }
}
function pa(a) {
    const b = h.width;
    const c = h.height;
    if (!b || !c) {
        return;
    }
    i.clearRect(0, 0, b, c);
    i.globalCompositeOperation = "lighter";
    const d = ["#ff4949", "#ff5454", "#ff2e2e"];
    const e = (a * 12) | 0;
    const f = j.sparkCell;
    const g = Math.ceil(b / f);
    const k = Math.ceil(c / f);
    for (let b = 0; b < k; b++) {
        for (let a = 0; a < g; a++) {
            const c = a + b * g;
            if (m(a, b, 3) >= j.sparkDensity) {
                continue;
            }
            const h = ga(c * 101 + 13, e);
            if (h % 10 > 6) {
                continue;
            }
            const k = 0.08 + (((h >>> 8) % 100) / 100) * j.sparkAlpha;
            const l = a * f + ((h >>> 0) % f);
            const n = b * f + ((h >>> 4) % f);
            const o = (h >>> 16) % 6;
            i.globalAlpha = k;
            i.fillStyle = d[o === 0 ? 0 : o < 4 ? 1 : 2];
            i.fillRect(l, n, 1, 1);
        }
    }
    const l = j.cell;
    const n = Math.ceil(b / l);
    const o = Math.ceil(c / l);
    const p = a * j.moveSpeed;
    const q = Math.floor(p);
    const r = p - q;
    const s = r * r * (3 - r * 2);
    for (let b = 0; b < o; b++) {
        for (let c = 0; c < n; c++) {
            const e = c + b * n;
            if (m(c, b, 5) >= j.bigDensity) {
                continue;
            }
            const f = Math.floor(a * j.flashRate + m(c, b, 7) * 40);
            const g = ga(e * 31 + 7, f);
            if (g % 10 >= j.onRatio * 10) {
                continue;
            }
            const h = m(c, b, 11 + (q % 97));
            const k = m(c, b, 31 + (q % 97));
            const o = m(c, b, 11 + ((q + 1) % 97));
            const p = m(c, b, 31 + ((q + 1) % 97));
            const r = (c + (h + (o - h) * s)) * l;
            const t = (b + (k + (p - k) * s)) * l;
            const u = ga(e, 12345);
            const v = 1 + ((u >>> 0) % 2);
            const w = 1 + ((u >>> 8) % 2);
            const x = 0.45 + ((u >>> 20) % 45) / 100;
            const y = (u >>> 16) % 6;
            i.globalAlpha = x;
            i.fillStyle = d[y === 0 ? 0 : y < 4 ? 1 : 2];
            i.fillRect(Math.floor(r), Math.floor(t), v, w);
        }
    }
    i.globalAlpha = 1;
    i.globalCompositeOperation = "source-over";
}
let qa = performance.now();
let ra = 0;
let sa = 0;
function ta(a) {
    requestAnimationFrame(ta);
    const b = Math.min((a - qa) / 1000, 0.1);
    qa = a;
    if (document.hidden) {
        return;
    }
    ra += b;
    sa++;
    if (k && sa & 1) {
        return;
    }
    if (!k && (sa & 1) === 0) {
        ma(ra);
    }
    if ((sa & 1) === 0) {
        _(ra);
    }
    pa(ra);
}
requestAnimationFrame(ta);
if (k) {
    // TOLOOK
    setInterval(() => {
        if (!document.hidden) {
            ma(ra);
        }
    }, 180);
}
