# Cakebaba Crypto Trading Skill

A comprehensive cryptocurrency trading analysis skill based on **Dow Theory 123 Rule**, **Engulfing Pattern**, and **2B Rule** from [CAKEBABA 頻道](https://www.youtube.com/c/cakebaba). Provides detailed technical analysis, risk assessment, and leveraged trading recommendations (10x/50x/100x).

> **CAKEBABA (蛋糕爸爸)** - 專業加密貨幣交易教育頻道，分享技術分析、趨勢交易和風險管理策略。

## Features

- 🎯 **123 Rule Detection**: Identifies trend reversals using Dow Theory
- 📊 **Technical Analysis**: RSI, MACD, Moving Averages, Support/Resistance, ATR
- 🕯️ **Engulfing Pattern (吞沒型態)**: High-probability reversal signals at key S/R zones
- 🔄 **2B Rule (假突破/假跌破)**: False breakout/breakdown detection for precision entries
- 📈 **Trend Identification**: HH/HL (uptrend), LL/LH (downtrend), consolidation patterns
- ⚖️ **Leverage-Specific Recommendations**: Tailored advice for 10x, 50x, and 100x leverage
- 🛡️ **Risk Management**: Position sizing, stop-loss calculations, risk/reward ratios
- 🖼️ **Chart Analysis**: Supports image-based K-line chart analysis
- 🔄 **Flexible Data Input**: Manual input, API auto-fetch, or chart screenshots

## About CAKEBABA

This skill is based on trading strategies and educational content from **CAKEBABA (蛋糕爸爸)** - a professional cryptocurrency trading education channel.

**🎓 Learn More:**
- **Website**: [https://www.cakebaba.com](https://www.cakebaba.com)
- **YouTube Channel**: [https://www.youtube.com/c/cakebaba](https://www.youtube.com/c/cakebaba)

**Key Patterns Taught by CAKEBABA:**
| Pattern | Win Rate | Description |
|---------|----------|-------------|
| Engulfing (吞沒型態) | 50-55% (alone), 60-75% (combined) | Large candle covering previous candle(s) at key S/R |
| 2B Rule (假突破) | 50-55% (alone), 60-70% (combined) | False breakout/breakdown with quick reversal |
| 2B + Engulfing | **60-65%** | False move + engulfing confirmation |
| 2B + 123 Rule | **65-70%** | False breakout confirming trend reversal |
| All Combined | **70-75%** | Highest probability setup |

> 💡 **Promo Code**: Use code **"CAKEBABA"** for a 1-month TradingView trial

## Installation

### Prerequisites

```bash
# Optional: Install numpy for technical indicator calculations
pip install numpy
```

**No API keys required!** The data fetcher uses Binance's public API with Python's standard library.

## Usage

### Basic Usage

Simply ask Claude about cryptocurrency trading:

```
"Should I buy BTC?"
"Analyze ETH, I'm thinking 50x long"
"Is this a good time to sell?"
[Upload chart image] "What do you think about this setup?"
```

### Triggering the Skill

The skill activates when you mention:
- Coin symbols: BTC, ETH, SOL, etc.
- Trading actions: buy, sell, long, short
- Leverage: 10x, 50x, 100x
- Technical terms: chart, trend, analysis, 123 rule

### Input Options

1. **Coin Symbol Only**:
   ```
   "Analyze BTC"
   ```
   → Skill auto-fetches real-time data (if API configured)

2. **Manual Data**:
   ```
   "BTC is at $50,000, up 3% today, RSI is 68, should I enter?"
   ```
   → Skill analyzes provided data

3. **Chart Screenshot**:
   ```
   [Upload K-line chart] "Analyze this chart"
   ```
   → Skill performs visual pattern analysis

4. **Mixed Input**:
   ```
   [Upload chart] "ETH, thinking 50x long, is this safe?"
   ```
   → Combines visual + context analysis

## Output Format

The skill provides structured analysis reports:

```
📊 BTC Professional Trading Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【Market Overview】
• Current Price, 24h Change, Trend, Sentiment

【Dow Theory 123 Rule Analysis】
• Trend Structure (HH/HL or LL/LH)
• 123 Signal Status (Points 1, 2, 3)
• Trendline levels
• 2B False Breakout Risk

【Technical Indicators】
• RSI, MACD, Moving Averages
• Key Support/Resistance Levels

【Trading Recommendations】
💼 CONSERVATIVE (10x) - Detailed entry/exit/risk
⚡ AGGRESSIVE (50x) - Detailed entry/exit/risk
🔥 EXTREME (100x) - Detailed entry/exit/risk

【Risk Warnings】
• Specific risks and invalidation levels
```

## File Structure

```
cakebaba-crypto-skill/
├── SKILL.md                          # Core skill instructions
├── README.md                          # This file
├── references/                        # Knowledge base (CAKEBABA content)
│   ├── dow-theory-123-rule.md        # Comprehensive 123 Rule guide
│   ├── engulfing-pattern.md          # 吞沒型態 trading strategy
│   ├── 2b-rule.md                    # 假突破/假跌破 detection
│   ├── technical-indicators.md       # Indicator calculations & interpretations
│   ├── trend-patterns.md             # HH/HL, LL/LH patterns
│   └── risk-management.md            # Position sizing & leverage guidelines
└── scripts/                           # Automation tools
    ├── fetch_crypto_data.py          # Real-time data fetcher (no dependencies!)
    └── calculate_indicators.py       # Technical indicator calculator
```

## Scripts Usage

### Fetch Real-Time Data

```bash
# Basic usage (no API key needed!)
python scripts/fetch_crypto_data.py --symbol BTC

# Get ticker only
python scripts/fetch_crypto_data.py --symbol ETH --mode ticker

# Get OHLCV data
python scripts/fetch_crypto_data.py --symbol SOL --mode ohlcv --timeframe 1h

# Full market summary
python scripts/fetch_crypto_data.py --symbol BTC --mode summary --output btc_data.json
```

### Calculate Technical Indicators

```bash
# Calculate all indicators
python scripts/calculate_indicators.py --file btc_data.json

# Specific indicators only
python scripts/calculate_indicators.py --file btc_data.json --indicators rsi macd ma

# Save to file
python scripts/calculate_indicators.py --file btc_data.json --output indicators.json
```

## Key Concepts

### Dow Theory 123 Rule

**Point 1**: Break of trendline
**Point 2**: Failure to create new high/low
**Point 3**: New low/high opposite to trend

**Signal**: All 3 points complete = 60-70% probability of trend reversal

### Engulfing Pattern (吞沒型態) - CAKEBABA Core Strategy

**Bullish Engulfing** (at support):
- Large green candle fully covers previous red candle(s)
- Small lower shadow (<20% of candle) = stronger signal
- Must occur at key support zone
- Wait for candle close before entry
- **Stop Loss**: Below engulfing candle low

**Bearish Engulfing** (at resistance):
- Large red candle fully covers previous green candle(s)
- Small upper shadow (<20% of candle) = stronger signal
- Must occur at key resistance zone
- Wait for candle close before entry
- **Stop Loss**: Above engulfing candle high

**Win Rate**: 50-55% alone, 60-75% with confirmations

### 2B Rule (假突破/假跌破) - CAKEBABA Precision Entry

**Bullish 2B** (false breakdown):
- Price briefly breaks support, reverses within 1-2 candles (5M timeframe)
- Closes back above support zone
- **Stop Loss**: Below false breakdown low (tight)

**Bearish 2B** (false breakout):
- Price briefly breaks resistance, reverses within 1-2 candles
- Closes back below resistance zone
- **Stop Loss**: Above false breakout high (tight)

**Win Rate**: 50-55% alone, 60-70% with confirmations

### High-Probability Combinations

| Combination | Win Rate | Best For |
|-------------|----------|----------|
| 2B + Engulfing | 60-65% | Precision entries at S/R |
| 2B + 123 Rule | 65-70% | Trend reversal confirmation |
| All Three | 70-75% | Highest probability setups |

### Trend Types

- **Uptrend**: Higher Highs (HH) + Higher Lows (HL)
- **Downtrend**: Lower Lows (LL) + Lower Highs (LH)
- **Consolidation**: Sideways movement between support/resistance

### Risk Management by Leverage

| Leverage | Risk/Trade | Stop-Loss | Min R:R | Skill Level |
|----------|------------|-----------|---------|-------------|
| 10x      | 2-3%       | 2-3%      | 1:3     | Intermediate |
| 50x      | 1-1.5%     | 1-1.5%    | 1:6     | Advanced |
| 100x     | 0.5-1%     | 0.5-1%    | 1:10    | Expert |

## Important Warnings

⚠️ **High Leverage = High Risk**:
- 100x leverage: 1% adverse move = total liquidation
- Only use leverage you understand and can afford to lose

⚠️ **Not Financial Advice**:
- This skill provides educational analysis only
- 123 Rule is 60-70% reliable, not guaranteed
- Always do your own research (DYOR)
- Never trade with money you can't afford to lose

⚠️ **Crypto Volatility**:
- False breakouts (2B patterns) are very common
- Always wait for candle close confirmation
- Use stop-losses without exception

## Best Practices

1. ✅ Always use stop-loss orders
2. ✅ Wait for candle close confirmation (15min minimum)
3. ✅ Confirm signals with multiple indicators
4. ✅ Start with lower leverage (10x) until experienced
5. ✅ Risk only 1-3% of capital per trade
6. ✅ Scale out of positions at profit targets
7. ✅ Review losing trades to learn
8. ✅ Focus on left-side trading (at S/R zones) for better R:R
9. ✅ Faster reversal = Stronger 2B signal

## Recommended Timeframes (CAKEBABA Guidelines)

| Market | Primary Timeframe | Acceptable Range | Notes |
|--------|------------------|------------------|-------|
| **Crypto (BTC/ETH)** | 5-minute | 5M - 15M | 1M too noisy; 5M recommended |
| **Altcoins** | 5-minute | 5M - 15M | Lower liquidity requires caution |
| **Stocks** | 1-hour | 1H - 4H | Lower liquidity = higher timeframe needed |
| **Forex** | 1-hour | 1H - 4H | 24H for trend following |

**Reversal Speed Requirements:**
- 5-minute: Reversal within 1-3 candles (~15 min max)
- 15-minute: Reversal within 1-2 candles (~30 min max)
- 1-hour: Reversal within 1 candle (~1 hour max)

**Key Point**: Faster reversal = Stronger 2B signal. Slow reversals (>5 candles on 5M) are weak or invalid.

## Support

For issues or questions:
- Check the reference documents in `references/`
- Review the SKILL.md for detailed instructions
- Verify API configuration if auto-fetch isn't working

## License & Attribution

This skill is for educational purposes. Use at your own risk.

**Trading strategies and educational content are based on [CAKEBABA 頻道](https://www.youtube.com/c/cakebaba)** - 專業加密貨幣交易教育頻道.

- **Website**: [https://www.cakebaba.com](https://www.cakebaba.com)
- **YouTube**: [https://www.youtube.com/c/cakebaba](https://www.youtube.com/c/cakebaba)

> **特別感謝 CAKEBABA 蛋糕爸爸頻道** - 本技能的交易策略和教育內容源自 CAKEBABA 頻道的專業分享，包括道氏理論 123 法則、吞沒型態、假突破假跌破等核心交易方法。

---

**Remember**: Protecting capital is more important than making profits. The market will always be there—make sure you are too.

**學習建議**: 觀看 [CAKEBABA 頻道](https://www.youtube.com/c/cakebaba) 的影片以深入理解這些交易策略。使用代碼 **"CAKEBABA"** 獲得 TradingView 1 個月免費試用。
