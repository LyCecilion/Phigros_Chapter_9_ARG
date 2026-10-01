sq = "PSZLMYQEBJARTFCHNUGVKDOXW"
pos = {c: (i // 5 + 1, i % 5 + 1) for i, c in enumerate(sq)}
rev = {v: k for k, v in pos.items()}
ct = [56, 75, 65, 76, 35, 56, 75, 63, 97, 66, 67, 47, 72]
ks = [10 * pos[c][0] + pos[c][1] for c in "AROUSL"]
print("".join(rev[divmod(n - ks[i % len(ks)], 10)] for i, n in enumerate(ct)))
