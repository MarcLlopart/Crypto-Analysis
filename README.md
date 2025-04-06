# Crypto Transaction Analysis

## 🧹 Data Cleaning & Preparation

The initial dataset consisted of **10,000 non-null transaction entries** across various blockchains, platforms, and transaction types. However, despite the lack of null values, there were notable inconsistencies in the `price_per_unit` field. The average value hovered around **$30,000**, which is unrealistic when considering less expensive cryptocurrencies like Dogecoin or XRP.

To address this, we recomputed the `price_per_unit` by pulling historical closing prices from [CoinGecko](https://www.coingecko.com/) using a utility function (`coin_gecko_scrapper.py`). Each transaction’s date and corresponding cryptocurrency were used to retrieve the correct closing price. This approach ensures a more **accurate and context-aware valuation**, though it does come with limitations such as not accounting for intraday volatility.

## 📊 Dataset Overview

- **Entries:** 10,000
- **Blockchains:** Bitcoin, Solana, Cardano, XRP, Dogecoin, BNB, Polkadot, Litecoin, Avalanche, Ethereum
- **Platforms:** KuCoin, Binance, OKX, FTX, Kraken, Coinbase, Huobi
- **Transaction Types:** Withdraw, Stake, Buy, Sell, Transfer
- **Transaction Status:** Completed, Failed, Pending

## 📈 Key Insights (Based on Completed Transactions Only)

- **Average Transaction Value:** `$307,664`
- **Fee to Transaction Value Ratio:** `2.46%`
- **Average Transactions per User:** `1.02`
- **Platform Distribution:**  
  - 🥇 *Coinbase* holds the largest share with `16.55%`
- **Crypto Distribution:**  
  - 🥇 *Polkadot* leads with `10.86%` of all transactions
- **Transaction Success Rate:** `33.2%`
- **Wallet Type Distribution:**  
  - 🔥 *Hot Wallets* are the most common at `20.77%`
- **Average Daily Active Users:** `4.61`
- **Growth Trends:**  
  - Minimal transaction growth across most of 2024  
  - The only positive quarter was **Q4 2024**, with a **1.75% increase**
- **Average Fee per Transaction:** `$7,582`

## 📉 Recommendations

1. **Improve Success Rate:** With only 33.2% of transactions marked as completed, there is a significant opportunity to improve reliability across platforms and wallet types.
2. **Fee Optimization:** At an average of $7.5k per transaction, platforms should assess whether high transaction fees are justifiable or impacting user retention.
3. **User Engagement:** With an average of just over 1 transaction per user, consider loyalty or incentive programs to increase engagement.
4. **Platform Expansion:** Coinbase dominates, but there’s room for platforms with lower fees or higher speed to compete for market share.

## 📍 Dashboard Interaction

To explore the data visually, an interactive dashboard is available.

To run the dashboard locally, use the following command in your terminal:

```bash
pip install -r requirements.txt
streamlit run src/dashboard.py
