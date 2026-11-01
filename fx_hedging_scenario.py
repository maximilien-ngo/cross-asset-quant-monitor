"""Illustrative corporate treasury FX hedging scenario.

Run: python3 fx_hedging_scenario.py
Produces: fx_hedging_scenario.png
All cash flows and forward rates are hypothetical; this is NOT LVMH internal data.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

USD_RECEIVABLE = 10_000_000
FORWARD_RATE = 1.10  # USD per EUR
rates = np.linspace(0.95, 1.25, 121)
unhedged_eur_m = USD_RECEIVABLE / rates / 1e6
hedged_eur_m = np.full_like(rates, USD_RECEIVABLE / FORWARD_RATE / 1e6)
difference_eur_m = hedged_eur_m - unhedged_eur_m

fig, axes = plt.subplots(2, 1, figsize=(11, 9), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
axes[0].plot(rates, unhedged_eur_m, label="Unhedged USD receipts", linewidth=2.3)
axes[0].plot(rates, hedged_eur_m, label="FX forward hedge (1.10 USD/EUR)", linewidth=2.3)
axes[0].axvline(FORWARD_RATE, linestyle="--", linewidth=1, alpha=0.6)
axes[0].set_ylabel("Value of USD 10m receipts (EUR millions)")
axes[0].set_title("Illustrative FX Risk Management | Locked-in EUR Cash Flow")
axes[0].legend()
axes[0].grid(alpha=0.25)

axes[1].plot(rates, difference_eur_m, linewidth=2, color="darkgreen")
axes[1].axhline(0, color="gray", linewidth=1)
axes[1].set_ylabel("Hedge minus unhedged (EUR m)")
axes[1].set_xlabel("EUR/USD at settlement (USD per EUR)")
axes[1].set_title("Hedge payoff relative to remaining unhedged")
axes[1].grid(alpha=0.25)

fig.text(0.5, 0.01,
         "Hypothetical example only: USD 10m receivable; forward rate 1.10; full hedge; no discounting or fees.\n"
         "Not LVMH proprietary treasury positions or evidence of realized hedging benefits.",
         ha="center", va="bottom", fontsize=9)
fig.tight_layout(rect=[0, 0.07, 1, 1])
fig.savefig("fx_hedging_scenario.png", dpi=160, bbox_inches="tight")
plt.close(fig)
print("Saved fx_hedging_scenario.png")
print("At EUR/USD 1.20: unhedged EUR %.2fm, hedged EUR %.2fm" % (USD_RECEIVABLE / 1.20 / 1e6, USD_RECEIVABLE / FORWARD_RATE / 1e6))
