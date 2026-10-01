let a = null;
let b = 1920;
let c = 1080;
const d = 1920;
const e = 1080;
const f = {
    speed: 0.6,
    strength: 12,
    cellPx: 4.5,
};
const g = document.getElementById("displace-canvas");
const h = g.getContext("2d", {
    willReadFrequently: true,
});
const i = document.getElementById("fx-canvas");
const j = i.getContext("2d");
const k = {
    sparkCell: 8,
    sparkDensity: 0.4,
    sparkAlpha: 0.55,
    cell: 6,
    bigDensity: 0.06,
    moveSpeed: 1.4,
    flashRate: 2,
    onRatio: 0.7,
};
const l = /[?&]lite([&=]|$)/.test(location.search);
const m = /[?&](black|nobg)([&=]|$)/.test(location.search);
if (l) {
    f.cellPx = 8;
    f.speed = 0.22;
    k.sparkCell = 11;
    k.sparkDensity = 0.22;
    k.sparkAlpha = 0.5;
    k.cell = 9;
    k.bigDensity = 0.03;
    k.flashRate = 1.5;
}
function n(a, b, c) {
    return (ha(a + b * 7919 + c * 104729, 1) >>> 0) / 4294967296;
}
const o = document.createElement("canvas");
const p = o.getContext("2d");
let q = null;
let r = 0;
let s = 0;
let t = null;
const u = 64;
const v = new Float32Array(u * u);
const w = new Float32Array(u * u);
(function a() {
    const d = ga(20260909);
    for (let a = 0; a < v.length; a++) {
        v[a] = d();
        w[a] = d();
    }
})();
function x(a, b, c) {
    const d = Math.floor(b);
    const e = Math.floor(c);
    const f = b - d;
    const g = c - e;
    const h = f * f * (3 - f * 2);
    const i = g * g * (3 - g * 2);
    const j = ((d % u) + u) % u;
    const k = ((e % u) + u) % u;
    const l = (j + 1) % u;
    const m = (k + 1) % u;
    const n = a[k * u + j];
    const o = a[k * u + l];
    const p = a[m * u + j];
    const q = a[m * u + l];
    return (n + (o - n) * h) * (1 - i) + (p + (q - p) * h) * i;
}
const y = l ? 16 : 8;
const z = 1.56;
const A = 0.9;
const B = (3.8 / z) * A;
const C = 0.0127 / z;
const D = 0.017 / z;
const E = 0.35 / z;
const F = 132;
const G = 36;
const H = 40;
const I = 0.15;
const J = 0.3;
const K = -0.25;
const L = 0.45;
const M = 2.4;
const N = 0.55;
const O = 2.6;
const P = document.getElementById("fog-canvas");
const Q = P
    ? P.getContext("2d", {
          willReadFrequently: true,
      })
    : null;
let R = null;
let S = null;
let T = null;
let U = null;
let V = 0;
let W = 0;
const X = new Float32Array(u * u);
const Y = new Float32Array(u * u);
const Z = new Float32Array(u * u);
(function a() {
    const b = ga(20260913);
    for (let a = 0; a < X.length; a++) {
        X[a] = b();
        Y[a] = b();
    }
    const c = ga(20260914);
    for (let a = 0; a < Z.length; a++) {
        Z[a] = c();
    }
})();
function $() {
    if (!Q) {
        return;
    }
    V = Math.max(2, Math.ceil(b / y));
    W = Math.max(2, Math.ceil(c / y));
    P.width = V;
    P.height = W;
    R = Q.createImageData(V, W);
    S = new Float32Array(V * W);
    T = new Float32Array(V * W);
    U = new Float32Array(V * W);
}
function _(a) {
    const b = Math.floor(a);
    const c = a - b;
    const d = c * c * (3 - c * 2);
    const e = (n(b, 3, 7) * 2 - 1) * 0.3;
    const f = (n(b + 1, 3, 7) * 2 - 1) * 0.3;
    return e + (f - e) * d;
}
function aa(a) {
    if (!Q || !R || !S || !U) {
        return;
    }
    const b = R.data;
    const c = a * B;
    const d = c * J;
    const e = c * 1.4;
    const f = _(a * E);
    const g = C;
    const h = D;
    const i = M;
    const j = (d + f) * i;
    const k = W * 0.3;
    let l = 0;
    for (let b = 0; b < W; b++) {
        const a = b * y;
        const d = a * g - c;
        const f = a * h - e;
        const m = b < k ? 0.55 + (b / k) * 0.45 : 1;
        for (let a = 0; a < V; a++) {
            const b = a * y;
            const c = b * g * i;
            const e = b * h * i;
            const k = x(X, c + j, d) * 0.85 + x(Y, e + j * 0.7, f) * 0.15;
            const n = x(Y, c - j, d) * 0.85 + x(X, e - j * 0.7, f) * 0.15;
            const o = (Math.max(k, n) - 0.5) * 2;
            const p = x(Z, c * O + 9.4, d * O + 31.7);
            U[l] = N + (1 - N) * p;
            let q = 0;
            const r = (o - K) / L;
            if (r > 0) {
                const a = r < 1 ? r * r * (3 - r * 2) : 1;
                q = a * I;
            }
            S[l++] = q * m;
        }
    }
    for (let b = 0; b < W; b++) {
        const a = b * V;
        const c = a + V - 1;
        T[a] = (S[a] * 3 + S[a + 1]) * 0.25;
        for (let b = a + 1; b < c; b++) {
            T[b] = (S[b - 1] + S[b] * 2 + S[b + 1]) * 0.25;
        }
        T[c] = (S[c - 1] + S[c] * 3) * 0.25;
    }
    const m = (W - 1) * V;
    for (let b = 0; b < V; b++) {
        S[b] = (T[b] * 3 + T[V + b]) * 0.25;
        S[m + b] = (T[m - V + b] + T[m + b] * 3) * 0.25;
    }
    for (let b = 1; b < W - 1; b++) {
        const a = b * V;
        for (let b = 0; b < V; b++) {
            const c = a + b;
            S[c] = (T[c - V] + T[c] * 2 + T[c + V]) * 0.25;
        }
    }
    for (let c = 0, d = 0; c < S.length; c++, d += 4) {
        b[d] = F;
        b[d + 1] = G;
        b[d + 2] = H;
        b[d + 3] = (S[c] * U[c] * 255) | 0;
    }
    Q.putImageData(R, 0, 0);
    if (!la(P, Q, ia)) {
        ma(P, Q, ia);
    }
}
function ba() {
    if (!a) {
        return;
    }
    const d = a.naturalWidth || a.width;
    const e = a.naturalHeight || a.height;
    if (!d || !e) {
        return;
    }
    o.width = b;
    o.height = c;
    const f = Math.max(b / d, c / e);
    const g = d * f;
    const h = e * f;
    p.clearRect(0, 0, b, c);
    p.drawImage(a, (b - g) / 2, (c - h) / 2, g, h);
    r = o.width;
    s = o.height;
    try {
        q = p.getImageData(0, 0, r, s).data;
    } catch (a) {
        q = null;
    }
}
function ca() {
    g.width = Math.ceil(b / f.cellPx);
    g.height = Math.ceil(c / f.cellPx);
    t = null;
    i.width = Math.ceil(b / (l ? 4 : 3));
    i.height = Math.ceil(c / (l ? 4 : 3));
    $();
    ba();
}
const da = document.getElementById("scaler");
function ea() {
    const a = window.innerWidth;
    const b = window.innerHeight;
    const c = Math.max(a / d, b / e);
    da.style.transform =
        "translate(" +
        ((a - d * c) / 2).toFixed(3) +
        "px," +
        ((b - e * c) / 2).toFixed(3) +
        "px) scale(" +
        c.toFixed(6) +
        ")";
}
function fa() {
    ea();
}
window.addEventListener("resize", fa);
(window.__sv.img || Promise.resolve(null))
    .then(function (b) {
        if (!b) {
            return;
        }
        a = b;
        ba();
    })
    .catch(function () {});
ca();
ea();
function ga(a) {
    let b = a | 0;
    return function () {
        b = (b + 1831565813) | 0;
        let a = Math.imul(b ^ (b >>> 15), b | 1);
        a = (a + Math.imul(a ^ (a >>> 7), a | 61)) ^ a;
        return ((a ^ (a >>> 14)) >>> 0) / 4294967296;
    };
}
function ha(a, b) {
    let c = (a | 0) + ((b * 2654435761) | 0);
    c = ((c ^ (c >>> 16)) * 2246822507) | 0;
    return (c ^ (c >>> 13)) >>> 0;
}
const ia = 0.25;
let ja = null;
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
function ma(a, b, c, d) {
    const e = a.width;
    const f = a.height;
    if (!e || !f) {
        return;
    }
    if (!ja || ja.width !== e || ja.height !== f) {
        ja = document.createElement("canvas");
        ja.width = e;
        ja.height = f;
    }
    const g = ja.getContext("2d");
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
            b.drawImage(ja, z, A, B - z, C - A, c, g, d, a);
        }
    }
}
function na(a) {
    const b = g.width;
    const c = g.height;
    if (!b || !c) {
        return;
    }
    if (m) {
        h.fillStyle = "#000";
        h.fillRect(0, 0, b, c);
        return;
    }
    if (q) {
        oa(a, b, c);
    } else {
        pa(a, b, c);
    }
    if (!la(g, h, ia)) {
        ma(g, h, ia, l ? 24 : 16);
    }
}
function oa(a, b, c) {
    const d = f.cellPx;
    const e = f.strength;
    const g = f.speed;
    const i = 0.012;
    const j = a * g;
    if (!t || t.width !== b || t.height !== c) {
        t = h.createImageData(b, c);
    }
    const k = t.data;
    const l = 2;
    for (let f = 0; f < c; f += l) {
        const a = (f + l * 0.5) * d;
        const g = Math.min(l, c - f);
        for (let c = 0; c < b; c += l) {
            const h = (c + l * 0.5) * d;
            const m = (x(v, h * i + j * 0.8, a * i) - 0.5) * 2 * e;
            const n = (x(w, h * i, a * i + j * 0.8) - 0.5) * 2 * e;
            const o = Math.min(l, b - c);
            for (let a = 0; a < g; a++) {
                const e = (f + a + 0.5) * d;
                const g = (f + a) * b * 4;
                for (let a = 0; a < o; a++) {
                    const b = (c + a + 0.5) * d;
                    let f = b + m;
                    let h = e + n;
                    if (f < 0) {
                        f = 0;
                    } else if (f >= r) {
                        f = r - 1;
                    }
                    if (h < 0) {
                        h = 0;
                    } else if (h >= s) {
                        h = s - 1;
                    }
                    const i = ((h | 0) * r + (f | 0)) * 4;
                    const j = g + (c + a) * 4;
                    k[j] = q[i];
                    k[j + 1] = q[i + 1];
                    k[j + 2] = q[i + 2];
                    k[j + 3] = 255;
                }
            }
        }
    }
    h.putImageData(t, 0, 0);
}
function pa(a, b, c) {
    if (!o.width) {
        return;
    }
    h.clearRect(0, 0, b, c);
    const d = f.cellPx;
    const e = f.strength;
    const g = f.speed;
    const i = 0.012;
    const j = a * g;
    const k = l ? 6 : 3;
    const m = k * d;
    for (let f = 0; f < c; f += k) {
        for (let a = 0; a < b; a += k) {
            const b = (a + k * 0.5) * d;
            const c = (f + k * 0.5) * d;
            const g = (x(v, b * i + j * 0.8, c * i) - 0.5) * 2 * e;
            const l = (x(w, b * i, c * i + j * 0.8) - 0.5) * 2 * e;
            const n = m;
            let p = b - n / 2 + g;
            let q = c - n / 2 + l;
            if (p < 0) {
                p = 0;
            } else if (p + n > r) {
                p = r - n;
            }
            if (q < 0) {
                q = 0;
            } else if (q + n > s) {
                q = s - n;
            }
            h.drawImage(o, p, q, n, n, a, f, k, k);
        }
    }
}
function qa(a) {
    const b = i.width;
    const c = i.height;
    if (!b || !c) {
        return;
    }
    j.clearRect(0, 0, b, c);
    j.globalCompositeOperation = "lighter";
    const d = ["#ff4949", "#ff5454", "#ff2e2e"];
    const e = (a * 12) | 0;
    const f = k.sparkCell;
    const g = Math.ceil(b / f);
    const h = Math.ceil(c / f);
    for (let b = 0; b < h; b++) {
        for (let a = 0; a < g; a++) {
            const c = a + b * g;
            if (n(a, b, 3) >= k.sparkDensity) {
                continue;
            }
            const h = ha(c * 101 + 13, e);
            if (h % 10 > 6) {
                continue;
            }
            const i = 0.08 + (((h >>> 8) % 100) / 100) * k.sparkAlpha;
            const l = a * f + ((h >>> 0) % f);
            const m = b * f + ((h >>> 4) % f);
            const o = (h >>> 16) % 6;
            j.globalAlpha = i;
            j.fillStyle = d[o === 0 ? 0 : o < 4 ? 1 : 2];
            j.fillRect(l, m, 1, 1);
        }
    }
    const l = k.cell;
    const m = Math.ceil(b / l);
    const o = Math.ceil(c / l);
    const p = a * k.moveSpeed;
    const q = Math.floor(p);
    const r = p - q;
    const s = r * r * (3 - r * 2);
    for (let b = 0; b < o; b++) {
        for (let c = 0; c < m; c++) {
            const e = c + b * m;
            if (n(c, b, 5) >= k.bigDensity) {
                continue;
            }
            const f = Math.floor(a * k.flashRate + n(c, b, 7) * 40);
            const g = ha(e * 31 + 7, f);
            if (g % 10 >= k.onRatio * 10) {
                continue;
            }
            const h = n(c, b, 11 + (q % 97));
            const i = n(c, b, 31 + (q % 97));
            const o = n(c, b, 11 + ((q + 1) % 97));
            const p = n(c, b, 31 + ((q + 1) % 97));
            const r = (c + (h + (o - h) * s)) * l;
            const t = (b + (i + (p - i) * s)) * l;
            const u = ha(e, 12345);
            const v = 1 + ((u >>> 0) % 2);
            const w = 1 + ((u >>> 8) % 2);
            const x = 0.45 + ((u >>> 20) % 45) / 100;
            const y = (u >>> 16) % 6;
            j.globalAlpha = x;
            j.fillStyle = d[y === 0 ? 0 : y < 4 ? 1 : 2];
            j.fillRect(Math.floor(r), Math.floor(t), v, w);
        }
    }
    j.globalAlpha = 1;
    j.globalCompositeOperation = "source-over";
}
let ra = performance.now();
let sa = 0;
let ta = 0;
function ua(a) {
    requestAnimationFrame(ua);
    const b = Math.min((a - ra) / 1000, 0.1);
    ra = a;
    if (document.hidden) {
        return;
    }
    sa += b;
    ta++;
    if (l && ta & 1) {
        return;
    }
    if (!l && (ta & 1) === 0) {
        na(sa);
    }
    if ((ta & 1) === 0) {
        aa(sa);
    }
    qa(sa);
}
requestAnimationFrame(ua);
if (l) {
    // TOLOOK
    setInterval(() => {
        if (!document.hidden) {
            na(sa);
        }
    }, 180);
}
