// Recover the obfuscated string table of song.html's main <script> block.
//
// song.html's first script uses the usual javascript-obfuscator layout:
//   function _0x49b4(){ ...string array... }
//   function _0x129b(idx, key){ ...base64 + RC4 decoder over that array... }
//   (function(_0x5e021c, _0x5c774c){ /* rotation IIFE */ }(_0x49b4, 0x...));
//   (function(){ /* the actual page logic */ })();
//
// The string array is *rotated* by the IIFE, so the decoder is only correct
// after that IIFE has run. The trick is therefore not to rewrite `_0x129b()`
// calls by hand but to actually execute the prefix (array + decoder + rotation)
// and then call the recovered decoder once per (index, key) pair.
//
// Usage: node deobfuscate.js song.html > 9.deobf.js
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync(process.argv[2] || "song.html", "utf8");
const script = html.match(/<script[^>]*>([\s\S]*?)<\/script>/)[1];

const noop = () => {};
const anyFn = new Proxy(function () {}, { get: () => anyFn, apply: () => anyFn });
const stub = new Proxy({}, {
  get: (t, p) =>
    p === "getContext" ? () => anyFn
    : p === "style" || p === "classList" || p === "dataset"
      ? new Proxy({}, { get: () => anyFn })
      : anyFn,
});

const sandbox = {
  console, Date, Math, JSON, Promise, Object, Array, String, Number, Boolean, Error,
  Uint8Array, Uint32Array, Int32Array, Float32Array, Float64Array, ArrayBuffer,
  DataView, TextDecoder, TextEncoder,
  setTimeout: () => 0, clearTimeout: noop, setInterval: () => 0, clearInterval: noop,
  requestAnimationFrame: () => 0, cancelAnimationFrame: noop,
  fetch: () => Promise.reject(new Error("offline")),
  btoa: (s) => Buffer.from(s, "binary").toString("base64"),
  atob: (s) => Buffer.from(s, "base64").toString("binary"),
  performance: { now: () => 0 },
};
Object.assign(sandbox, { window: sandbox, self: sandbox, globalThis: sandbox });
sandbox.document = {
  getElementById: () => null, querySelector: () => null, querySelectorAll: () => [],
  createElement: () => stub, addEventListener: noop, removeEventListener: noop,
  body: stub, documentElement: stub, hidden: false, visibilityState: "visible",
  cookie: "", fullscreenElement: null,
};
sandbox.navigator = { language: "zh-CN", userAgent: "x", hardwareConcurrency: 4 };
sandbox.location = { search: "", hash: "", pathname: "/", href: "", replace: noop };

vm.createContext(sandbox);
try {
  vm.runInContext(script, sandbox, { filename: "song-main.js" });
} catch (e) {
  // The page logic itself needs a real DOM; the string decoder is already usable.
}
const decode = sandbox._0x129b;
if (typeof decode !== "function") throw new Error("decoder not found");

// Resolve every call site. `9.js` is the (partially) deobfuscated dump of the
// same block, so we harvest the (index, key) pairs straight from it.
const target = process.argv[3] || "9.js";
const body = fs.readFileSync(target, "utf8");
let unresolved = 0;
const out = body.replace(
  /_0x129b\(\s*(0x[0-9a-fA-F]+|\d+)\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)/g,
  (full, idx, key) => {
    try {
      return JSON.stringify(decode(Number(idx), key));
    } catch (e) {
      unresolved++;
      return full;
    }
  }
);
// The deobfuscator that produced `9.js` left `//decode_error: ...` markers where
// it could not resolve a lookup; drop them, then join literals that the
// obfuscator split as `"key.php?n=" + "1"`.
const stripped = out
  .replace(/[ \t]*\/\/decode_error:[^\n]*/g, "")
  .split("\n")
  .filter((l) => l.trim())
  .join("\n");
let collapsed = stripped, prev;
do {
  prev = collapsed;
  collapsed = collapsed.replace(
    /"((?:[^"\\]|\\.)*)"\s*\+\s*"((?:[^"\\]|\\.)*)"/g,
    (m, a, b) => JSON.stringify(JSON.parse('"' + a + '"') + JSON.parse('"' + b + '"'))
  );
} while (collapsed !== prev);

process.stdout.write(collapsed);
process.stderr.write(`resolved, unresolved=${unresolved}\n`);
