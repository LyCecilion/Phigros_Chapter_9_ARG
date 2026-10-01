const a = "https://c9.gaoice.run/start.png";
const b = new Image();
b.fetchPriority = "high";
b.decoding = "async";
function c(a) {
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
            ((a[b] << 24) | (a[b + 1] << 16) | (a[b + 2] << 8) | a[b + 3]) >>>
            0;
        const d = String.fromCharCode(a[b + 4], a[b + 5], a[b + 6], a[b + 7]);
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
(async function d() {
    try {
        const d = await (
            await fetch(a, {
                credentials: "omit",
            })
        ).arrayBuffer();
        const e = new Uint8Array(d);
        const f = URL.createObjectURL(
            new Blob([e.subarray(c(e))], {
                type: "image/png",
            }),
        );
        b.addEventListener(
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
        b.src = f;
    } catch (c) {
        b.src = a;
    }
})();
document.addEventListener("contextmenu", function (a) {
    a.preventDefault();
});
