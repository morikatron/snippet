"""pi_bcd.bin（円周率100万桁の BCD 詰め）を自分で作り直すためのスクリプト。

使い方:
    pip install mpmath        # 高速化したければ gmpy2 も
    python3 generate_pi.py

出力:
    pi_bcd.bin  … 500,000 バイト。整数部の「3」を含む先頭100万桁を、
                  1バイトに2桁（上位4ビットが先の桁）で詰めたもの。
                  先頭バイトは 0x31（= 3, 1）になる。

2006年の試作も製品も、円周率をこの詰め方（BCD）で持っていた。
"""

from mpmath import mp

N = 1_000_000  # 整数部の3を含む総桁数

mp.dps = N + 40
s = mp.nstr(mp.pi, N + 30, strip_zeros=False)
assert s.startswith("3."), s[:10]
digits = ("3" + s[2:])[:N]
assert len(digits) == N and digits.isdigit()

# ---- 自己点検 ----
assert digits.startswith("31415926535897932384626433832795028841971693993751")
total = sum(int(c) for c in digits)
total998 = total - int(digits[-1]) - int(digits[-2])
print(f"先頭100万桁の合計   : {total:,}（10で割ると {total % 10} 余る）")
print(f"先頭999,998桁の合計 : {total998:,}（10で割ると {total998 % 10} 余る）")
assert total998 % 10 == 0, "999,998桁の合計が10の倍数になっていない"

# ---- BCD に詰める ----
vals = [int(c) for c in digits]
bcd = bytearray(N // 2)
for i in range(0, N, 2):
    bcd[i // 2] = (vals[i] << 4) | vals[i + 1]
with open("pi_bcd.bin", "wb") as f:
    f.write(bcd)
print(f"pi_bcd.bin を書き出しました（{len(bcd):,} バイト）")
