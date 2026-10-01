(function () {
    const slogan = document.getElementById("slogan");
    const toast = document.getElementById("toast");
    let curIndex = 12;
    let hideTimer;

    function flash(ms) {
        toast.classList.add("show");
        clearTimeout(hideTimer);
        hideTimer = setTimeout(
            () => toast.classList.remove("show"),
            ms || 1200,
        );
    }

    async function copyText(text) {
        try {
            if (navigator.clipboard && window.isSecureContext) {
                await navigator.clipboard.writeText(text);
                return true;
            }
        } catch (e) {}

        const ta = document.createElement("textarea");
        ta.value = text;
        ta.setAttribute("readonly", "");
        ta.style.position = "fixed";
        ta.style.top = "-1000px";
        ta.style.opacity = "0";
        document.body.appendChild(ta);
        ta.select();
        ta.setSelectionRange(0, ta.value.length);
        let ok = false;
        try {
            ok = document.execCommand("copy");
        } catch (e) {
            ok = false;
        }
        ta.remove();
        return ok;
    }

    async function handleCopy() {
        const ok = await copyText(slogan.textContent);
        toast.textContent = ok ? "Copied" : "Copy failed";
        flash(ok ? 1200 : 2200);
    }

    slogan.addEventListener("click", handleCopy);

    slogan.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " " || e.key === "Spacebar") {
            e.preventDefault();
            handleCopy();
        }
    });

    function fnv(str, seed) {
        let h = seed >>> 0;
        for (let i = 0; i < str.length; i++) {
            h ^= str.charCodeAt(i);
            h = Math.imul(h, 16777619) >>> 0;
        }
        return h >>> 0;
    }

    function hex8(n) {
        return ("0000000" + n.toString(16)).slice(-8);
    }

    function fingerprint() {
        const p = [];
        p.push(navigator.userAgent || "");
        p.push(navigator.language || "");
        p.push((navigator.languages || []).join(","));
        p.push(navigator.platform || "");
        p.push("hc" + (navigator.hardwareConcurrency || 0));
        p.push("dm" + (navigator.deviceMemory || 0));
        p.push("mt" + (navigator.maxTouchPoints || 0));
        p.push(
            "sc" +
                screen.width +
                "x" +
                screen.height +
                "x" +
                screen.colorDepth +
                "x" +
                (window.devicePixelRatio || 1),
        );
        p.push("tz" + new Date().getTimezoneOffset());

        try {
            p.push("zone" + Intl.DateTimeFormat().resolvedOptions().timeZone);
        } catch (e) {
            p.push("zone?");
        }

        try {
            const c = document.createElement("canvas");
            c.width = 200;
            c.height = 40;
            const ctx = c.getContext("2d");
            ctx.textBaseline = "top";
            ctx.font = "16px 'Arial'";
            ctx.fillStyle = "#f60";
            ctx.fillRect(0, 0, 100, 20);
            ctx.fillStyle = "#069";
            ctx.fillText("ARG-fp-1234", 2, 4);
            ctx.fillStyle = "rgba(102,204,0,0.7)";
            ctx.fillText("ARG-fp-1234", 4, 6);
            p.push("cv" + c.toDataURL().slice(-80));
        } catch (e) {
            p.push("cv?");
        }

        try {
            const gl = document.createElement("canvas").getContext("webgl");
            const dbg = gl.getExtension("WEBGL_debug_renderer_info");
            p.push(
                "gv" +
                    gl.getParameter(
                        dbg ? dbg.UNMASKED_VENDOR_WEBGL : gl.VENDOR,
                    ),
            );
            p.push(
                "gr" +
                    gl.getParameter(
                        dbg ? dbg.UNMASKED_RENDERER_WEBGL : gl.RENDERER,
                    ),
            );
        } catch (e) {
            p.push("gl?");
        }

        const s = p.join("|");
        return (
            hex8(fnv(s, 2166136261)) +
            hex8(fnv(s, 1099511628)) +
            hex8(fnv(s + "#2", 2166136261)) +
            hex8(fnv(s + "#3", 1099511628))
        );
    }

    function syncFromServer() {
        if (!window.fetch) {
            return;
        }

        let fp;
        try {
            fp = fingerprint();
        } catch (e) {
            return;
        }

        fetch("api.php?fp=" + encodeURIComponent(fp), {
            cache: "no-store",
            credentials: "same-origin",
        })
            .then(function (r) {
                return r.json();
            })
            .then(function (d) {
                if (!d || d.ok !== true) {
                    return;
                }
                if (
                    typeof d.index === "number" &&
                    typeof d.text === "string" &&
                    d.index !== curIndex
                ) {
                    curIndex = d.index;
                    slogan.textContent = d.text;
                }
            })
            .catch(function () {});
    }

    const triCanvas = document.getElementById("tri");
    const tctx = triCanvas.getContext("2d");
    let triW = 0,
        triH = 0;
    let isPortrait = false;
    const TRI_SPEED = 63;
    const TRI_SPEED_LANDSCAPE = 72;
    const TRI_SCALE_PORTRAIT = 0.75;
    const TRI_SCALE_LANDSCAPE = 0.8;

    function resizeTri() {
        isPortrait = window.innerHeight > window.innerWidth;
        triW = triCanvas.width = isPortrait
            ? window.innerHeight
            : window.innerWidth;
        triH = triCanvas.height = isPortrait
            ? window.innerWidth
            : window.innerHeight;
    }
    resizeTri();
    window.addEventListener("resize", resizeTri);

    const tris = [];

    function spawnTri() {
        const h0 = 15 + Math.random() * 15;
        const scale = isPortrait ? TRI_SCALE_PORTRAIT : TRI_SCALE_LANDSCAPE;
        const h = h0 * scale;
        const side = (h * 2) / Math.sqrt(3);
        const dir = Math.random() < 0.5 ? 1 : -1;
        tris.push({
            x: dir > 0 ? -side : triW + side,
            y: (triH * (Math.random() + Math.random())) / 2,
            h0: h0,
            side: side,
            h: h,
            up: true,
            dir: dir,
            speed: isPortrait ? TRI_SPEED : TRI_SPEED_LANDSCAPE,
            alpha: 0.18 + Math.random() * 0.2,
        });
    }

    let triLast = performance.now();
    let triNextSpawn = triLast + 150;

    function triFrame(now) {
        const dt = Math.min((now - triLast) / 1000, 0.1);
        triLast = now;

        const curSpeed = isPortrait ? TRI_SPEED : TRI_SPEED_LANDSCAPE;
        const curScale = isPortrait ? TRI_SCALE_PORTRAIT : TRI_SCALE_LANDSCAPE;
        const spawnGap = (((triW + 80) / curSpeed) * 1000) / 30;
        if (now >= triNextSpawn) {
            if (tris.length < 30) {
                spawnTri();
            }
            triNextSpawn = now + spawnGap * (0.8 + Math.random() * 0.4);
        }

        tctx.clearRect(0, 0, triW, triH);
        for (let i = tris.length - 1; i >= 0; i--) {
            const t = tris[i];
            t.speed = curSpeed;
            t.h = t.h0 * curScale;
            t.side = (t.h * 2) / Math.sqrt(3);
            t.x += t.speed * t.dir * dt;
            if (t.x > triW + t.side || t.x < -t.side) {
                tris.splice(i, 1);
                continue;
            }
            const half = t.side / 2;
            tctx.beginPath();
            if (t.up) {
                tctx.moveTo(t.x, t.y - t.h / 2);
                tctx.lineTo(t.x + half, t.y + t.h / 2);
                tctx.lineTo(t.x - half, t.y + t.h / 2);
            } else {
                tctx.moveTo(t.x, t.y + t.h / 2);
                tctx.lineTo(t.x + half, t.y - t.h / 2);
                tctx.lineTo(t.x - half, t.y - t.h / 2);
            }
            tctx.closePath();
            tctx.fillStyle = "rgba(255, 255, 255, " + t.alpha + ")";
            tctx.fill();
        }

        requestAnimationFrame(triFrame);
    }
    requestAnimationFrame(triFrame);

    syncFromServer();
})();
console.log(
    "To our non-Chinese players: during our review, we found an information gap between mainland China and overseas that may leave you stuck on the puzzles. If you've made it this far but have no idea how to proceed, visit Bilibili and browse the Phigros official account's past posts. Earlier puzzles may give you the inspiration you need.",
);
