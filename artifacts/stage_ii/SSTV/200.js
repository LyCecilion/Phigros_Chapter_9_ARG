const c = window.AudioContext || window.webkitAudioContext;
let d = null;
let e = null;
let f = null;
let g = false;
function h() {
    if (!e || !c) {
        return;
    }
    if (!d) {
        d = new c();
        d.addEventListener("statechange", h);
    }
    if (d.state !== "running") {
        try {
            const a = d.resume();
            if (a && a.catch) {
                a.catch(function () {});
            }
        } catch (a) {}
        return;
    }
    if (g) {
        return;
    }
    try {
        f = d.createBufferSource();
        f.buffer = e;
        f.loop = true;
        f.connect(d.destination);
        f.start(0);
        g = true;
    } catch (a) {
        g = false;
    }
}
(window.__sv.aud || Promise.resolve(null))
    .then(function (a) {
        if (!a || !c) {
            return;
        }
        const b = a.buffer.slice(a.byteOffset, a.byteOffset + a.byteLength);
        if (!d) {
            d = new c();
        }
        d.decodeAudioData(b)
            .then(function (a) {
                e = a;
                h();
            })
            .catch(function () {});
    })
    .catch(function () {});
["pointerdown", "touchstart", "click", "keydown"].forEach(function (a) {
    window.addEventListener(a, h, {
        passive: true,
    });
});
document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
        h();
    }
});
window.addEventListener("pageshow", h);
window.addEventListener("load", h);
