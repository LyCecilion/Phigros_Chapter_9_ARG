const a = document.getElementById("countdown-canvas");
const b = a.getContext("2d");
const c = new Date("2026/10/02 17:00:00").getTime();
function d(a) {
    return String(a).padStart(2, "0");
}
function e() {
    const a = c - Date.now();
    if (a <= 0) {
        return "0:00:00:00";
    }
    const b = Math.floor(a / 1000);
    return (
        Math.floor(b / 86400) +
        ":" +
        d(Math.floor((b % 86400) / 3600)) +
        ":" +
        d(Math.floor((b % 3600) / 60)) +
        ":" +
        d(b % 60)
    );
}
let f = null;
let g = 0;
function h(a, b) {
    const c = b * 0.0417;
    if (!f || g !== c) {
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
        f = a.createPattern(b, "repeat");
        g = c;
    }
    return f;
}
function i() {
    const c = window.innerWidth;
    const d = window.innerHeight;
    if (a.width !== c) {
        a.width = c;
    }
    if (a.height !== d) {
        a.height = d;
    }
    const f = b;
    f.setTransform(1, 0, 0, 1, 0, 0);
    f.clearRect(0, 0, c, d);
    const g = c < 800;
    const i = g ? Math.max(40, Math.min(96, c * 0.12)) : c * 0.05;
    f.font = i + "px 'Saira Condensed', 'Microsoft YaHei', sans-serif";
    f.textAlign = "center";
    f.textBaseline = "middle";
    const j = e();
    const k = c / 2;
    const l = d / 2;
    const m = [];
    if (g) {
        const a = j.split(":");
        const b = i * 1.2;
        const c = l - ((a.length - 1) * b) / 2;
        a.forEach((a, d) =>
            m.push({
                ch: a,
                x: k,
                y: c + d * b,
            }),
        );
    } else {
        const a = c * 0.8;
        const b = j.length;
        const d = i;
        const e = (a - b * d) / (b - 1);
        let f = k - a / 2 + d / 2;
        for (const a of j) {
            m.push({
                ch: a,
                x: f,
                y: l,
            });
            f += d + e;
        }
    }
    f.save();
    f.shadowColor = "rgba(0,0,0,1)";
    f.shadowBlur = 48;
    f.shadowOffsetX = 0;
    f.shadowOffsetY = 0;
    f.fillStyle = "#000";
    for (let a = 0; a < 4; a++) {
        for (const a of m) {
            f.fillText(a.ch, a.x, a.y);
        }
    }
    f.restore();
    f.fillStyle = "rgba(255,45,45,0.5)";
    for (const a of m) {
        f.fillText(a.ch, a.x + 2, a.y);
    }
    f.fillStyle = "rgba(60,200,255,0.5)";
    for (const a of m) {
        f.fillText(a.ch, a.x - 2, a.y);
    }
    f.save();
    f.shadowColor = "rgba(255,255,255,0.35)";
    f.shadowBlur = 8;
    f.shadowOffsetX = 0;
    f.shadowOffsetY = 0;
    f.fillStyle = h(f, i);
    for (const a of m) {
        f.fillText(a.ch, a.x, a.y);
    }
    f.restore();
    barrelWarpCanvas(a, f, BARREL_K, 8);
}
window.addEventListener("resize", i);
// TOLOOK
setInterval(i, 1000);
i();
if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(i);
}
const j = document.getElementById("scanline-canvas");
const k = j.getContext("2d");
const l = 3;
const m = 0.16;
function n() {
    const c = window.innerWidth;
    const d = window.innerHeight;
    if (j.width !== c) {
        j.width = c;
    }
    if (j.height !== d) {
        j.height = d;
    }
    const e = k;
    e.setTransform(1, 0, 0, 1, 0, 0);
    e.clearRect(0, 0, c, d);
    const f = document.createElement("canvas");
    f.width = 1;
    f.height = l;
    const g = f.getContext("2d");
    g.fillStyle = "rgba(0,0,0," + m + ")";
    g.fillRect(0, 0, 1, 1);
    e.fillStyle = e.createPattern(f, "repeat");
    e.fillRect(0, 0, c, d);
    barrelWarpCanvas(j, e, BARREL_K, 8);
}
window.addEventListener("resize", n);
n();
