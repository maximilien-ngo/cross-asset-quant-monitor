"""LVMH-focused charts: equities, rolling volatility, and EUR/USD.

Run with: python3 lvmh_dashboard.py
Data: Yahoo Finance. Charts are exploratory, not investment advice.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf


def close_prices(ticker, period="2y"):
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError(f"No market data returned for {ticker}")
    series = data["Close"].squeeze().dropna()
    if series.empty:
        raise ValueError(f"No closing prices returned for {ticker}")
    return series.astype(float)


def make_lvmh_dashboard():
    """Save three charts to lvmh_dashboard.png in the current directory."""
    tickers = {"LVMH": "MC.PA", "Euro Stoxx 50": "^STOXX50E", "EUR/USD": "EURUSD=X"}
    series = {}
    for name, ticker in tickers.items():
        series[name] = close_prices(ticker)

    # Align trading dates for a fair normalized equity performance comparison.
    equity = pd.concat(
        [series["LVMH"].rename("LVMH"), series["Euro Stoxx 50"].rename("Euro Stoxx 50")],
        axis=1,
    ).dropna()
    if len(equity) < 30:
        raise ValueError("Insufficient aligned equity observations (need 30+).")
    normalized = equity.div(equity.iloc[0]).mul(100)

    # Annualized realized volatility from daily log returns, 20 sessions.
    lvmh_vol = np.log(series["LVMH"] / series["LVMH"].shift(1)).rolling(20).std() * np.sqrt(252) * 100

    fig, axes = plt.subplots(3, 1, figsize=(12, 11))
    normalized.plot(ax=axes[0], linewidth=1.8)
    axes[0].set_title("LVMH vs Euro Stoxx 50 | Indexed performance (start = 100)")
    axes[0].set_ylabel("Index (base 100)")
    axes[0].grid(alpha=0.3)

    lvmh_vol.plot(ax=axes[1], color="darkblue", linewidth=1.7)
    axes[1].set_title("LVMH | 20-day annualized realized volatility")
    axes[1].set_ylabel("Volatility (%)")
    axes[1].grid(alpha=0.3)

    series["EUR/USD"].plot(ax=axes[2], color="darkgreen", linewidth=1.7)
    axes[2].set_title("EUR/USD | FX exposure reference (USD per EUR)")
    axes[2].set_ylabel("USD per EUR")
    axes[2].set_xlabel("Date")
    axes[2].grid(alpha=0.3)

    fig.suptitle("LVMH Market & Treasury Monitor | Historical Market Data", fontsize=15)
    fig.tight_layout()
    fig.savefig("lvmh_dashboard.png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("LVMH charts saved to: lvmh_dashboard.png")
    print("Note: EUR/USD is a market indicator, not a representation of LVMH's actual hedges.")


if __name__ == "__main__":
    make_lvmh_dashboard()
