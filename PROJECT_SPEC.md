# Investment Model Project Specification

## Overview

This is an AI-assisted investment research and stock-scoring system designed to identify publicly traded companies with the strongest combination of growth, financial quality, valuation, competitive advantage, catalysts, momentum, inflation resilience, and acceptable risk.

**Purpose:** Research and decision-support system. NOT a guarantee of investment returns.

---

## 1. TECHNOLOGY REQUIREMENTS

- Python 3.11+
- pandas
- numpy
- pytest
- Additional open-source packages as needed

Architecture: Modular and maintainable

---

## 2. CORE SCORING MODEL

Every stock receives a score from 0–100.

### Scoring Weights

| Category | Points |
|----------|--------|
| Revenue Growth | 15 |
| Earnings / Free Cash Flow | 15 |
| Industry Growth | 15 |
| Balance Sheet / Financial Strength | 10 |
| Valuation | 10 |
| Competitive Advantage / Moat | 10 |
| Price Trend / Momentum | 10 |
| Insider / Institutional Activity | 5 |
| Catalysts | 5 |
| Inflation Resilience / Pricing Power | 5 |
| **TOTAL** | **100** |

The scoring engine retains every individual category score.

---

## 3. ABSOLUTE MODEL RULES

### Rule A — Share Price is NOT Valuation

- A $2 stock is not automatically cheaper than a $200 stock
- Absolute share price must NEVER directly increase investment score
- Changing only share price must not improve fundamental investment score

### Rule B — Do Not Chase Hype

- Recently exploding stocks don't automatically get high scores
- Momentum is only one component (10/100 points)

### Rule C — Growth Alone is Insufficient

High revenue growth cannot compensate for:
- Terrible valuation
- Unsustainable cash burn
- Excessive debt
- Severe dilution
- Weak competitive position
- Collapsing margins

### Rule D — Small-Cap Stocks Allowed

- Model discovers small-cap/high-growth opportunities
- Market capitalization receives zero bonus points
- Company must earn score through fundamentals, growth, valuation, moat, catalysts

### Rule E — Never Fabricate Data

- Mark unavailable data clearly
- Identify missing fields
- Do not invent numbers
- Do not silently substitute estimates
- Record data source and timestamp

---

## 4. FUNDAMENTAL ANALYSIS

### Revenue Growth (15 points max)
- Historical growth rate
- Recent growth
- Forward growth projections
- Acceleration/deceleration trends
- Consistency
- Organic vs acquisition-driven

### Earnings / Free Cash Flow (15 points max)
- EPS growth
- Profitability
- Operating margins
- Margin expansion
- Free cash flow
- FCF growth
- Operating leverage

### Industry Growth (15 points max)
- Total addressable market (TAM)
- Industry growth rate
- Secular trends
- Technological disruption
- Competitive intensity
- Long-term demand outlook

### Balance Sheet (10 points max)
- Cash position
- Debt levels
- Net debt
- Liquidity
- Debt/equity ratio
- Interest coverage
- Dilution
- Ability to finance growth

### Valuation (10 points max)
Evaluate relative to:
- Revenue multiples
- Earnings multiples
- Free cash flow multiples
- Growth rate (PEG)
- Industry peers
- Historical valuation
- Expected future growth

**Must NOT use absolute share price**

### Competitive Advantage (10 points max)
- Network effects
- Switching costs
- Brand strength
- Proprietary technology
- Patents/IP
- Cost advantage
- Distribution
- Scale
- Data advantage
- Customer lock-in

### Momentum (10 points max)
- 1-month return
- 3-month return
- 6-month return
- 1-year return
- Relative strength
- Trend consistency
- Volume analysis
- Breakouts/breakdowns

**Must NOT dominate the model**

### Insider / Institutional Activity (5 points max)
- Insider buying activity
- Insider selling activity
- Institutional ownership levels
- Institutional accumulation
- Changes in positioning

### Catalysts (5 points max)
Genuine, identifiable catalysts:
- Earnings releases
- Product launches
- New contracts
- Regulatory approvals
- Partnerships
- AI adoption
- Capacity expansion
- New markets
- M&A activity
- Industry changes

**Distinguish actual catalysts from speculation**

### Inflation Resilience (5 points max)
- Pricing power
- Recurring revenue
- Essential products/services
- Ability to pass costs to customers
- Gross margin stability
- Input-cost sensitivity

---

## 5. RISK ENGINE

Identify and clearly display:
- Excessive valuation
- High debt levels
- Dilution
- Customer concentration
- Regulatory risk
- Competitive threats
- Commodity exposure
- Single-product dependence
- Unprofitable growth
- Management concerns
- Concentration risk
- Macroeconomic sensitivity

Risk must be clearly visible, not hidden.

---

## 6. CLASSIFICATION

| Score Range | Classification |
|-------------|-----------------|
| 85–100 | BUY |
| 75–84 | WATCH |
| 65–74 | INTERESTING |
| 50–64 | RESEARCH |
| 0–49 | REJECT |

Classification generated programmatically.

---

## 7. INITIAL STOCK UNIVERSE

Starting stocks:
```
TICKERS = [
    "NVDA",
    "PLTR",
    "AMD",
    "AVGO",
    "AMAT",
    "MU",
    "ACMR",
    "CRDO",
    "TER",
    "CRWD",
    "PANW",
]
```

Easy to add additional stocks.

---

## 8. DATA ARCHITECTURE

- Modular data layer
- Data providers replaceable
- No hard-coded API dependencies
- Normalized company data structures
- Support for mock/demo data
- Clear separation of real vs test data

### Required Fields

```
ticker, company_name, sector, industry, market_cap,
share_price, revenue, revenue_growth, eps, eps_growth,
free_cash_flow, free_cash_flow_growth, cash, debt,
gross_margin, operating_margin, pe_ratio, price_to_sales,
price_to_fcf, one_month_return, three_month_return,
six_month_return, one_year_return, insider_activity,
institutional_activity, industry_growth, competitive_advantage,
catalysts, inflation_resilience, risk_factors,
data_timestamp, data_sources
```

Use `None`/`NaN` for unavailable information.

---

## 9. SCORING ENGINE

Clean, validated scoring interface:

```python
class StockScore:
    revenue_growth: float
    earnings_fcf: float
    industry_growth: float
    balance_sheet: float
    valuation: float
    competitive_advantage: float
    momentum: float
    insider_institutional: float
    catalysts: float
    inflation_resilience: float
    
    total_score: float
    classification: str
```

Validation:
- 0 ≤ category score ≤ category maximum
- 0 ≤ total_score ≤ 100
- total = sum of categories

---

## 10. RANKING

Given multiple companies, return ranked list:
1. Highest score
2. Second highest
3. Third highest
4. etc.

Include:
- Ticker, company name
- Total score, classification
- Category scores
- Major strengths
- Major weaknesses
- Risks
- Catalysts

Tie handling: Deterministic

---

## 11. REPORTING

Generate human-readable report with:
- Ticker, score, classification
- Individual category scores
- Major strengths (3+)
- Major risks
- Key catalysts
- Investment thesis
- What would invalidate thesis

Example structure included in system.

---

## 12. HISTORICAL PREDICTION TRACKING

Save every research cycle:
- Date
- Ticker
- Score
- Ranking
- Classification
- Price at prediction
- Investment thesis
- Catalysts
- Risks

Later record:
- Actual price
- Percentage return
- Benchmark return
- Prediction accuracy
- Thesis accuracy
- Catalyst outcome

**Never overwrite historical predictions.**

---

## 13. 14-DAY EXPERIMENT

Experiment period: August 14 - August 28, 2026

Decision point: August 28, 2026

System identifies strongest candidate for $10 investment based on evidence.

Does not automatically select highest-scoring company if major risk or data-quality issue exists.

Final report explains selection rationale.

---

## 14. BENCHMARKING

Track performance against:
- S&P 500
- Equal-weight candidate portfolio
- Simple momentum strategy
- Simple growth strategy

Calculate:
- Return, percentage return
- Relative performance
- Drawdown
- Win rate
- Ranking effectiveness

Objective: Determine if scoring system adds value.

---

## 15. MACHINE LEARNING

**Phase 1:** Transparent, deterministic scoring

**Phase 2 (when data accumulates):** Prepare architecture for:
- Regression models
- Classification models
- Ranking models
- NLP
- Sentiment analysis
- Hugging Face models

Only introduce ML with sufficient historical data and proper training/evaluation.

---

## 16. TEST-DRIVEN DEVELOPMENT

pytest tests include:

### Score Validation
- Scores cannot be negative
- Scores cannot exceed maximum
- Total cannot exceed 100
- Total equals category sum

### Weight Validation
- All category maximums sum to exactly 100

### Share-Price Independence
- Changing only share price does NOT increase fundamental score

### Classification
- 85 → BUY
- 84 → WATCH
- 75 → WATCH
- 74 → INTERESTING
- 65 → INTERESTING
- 64 → RESEARCH
- 50 → RESEARCH
- 49 → REJECT

### Missing Data
- Missing financial info does not crash system

### Ranking
- Identical input produces deterministic rankings

### Historical Tracking
- Historical predictions unchanged after model updates

---

## 17. DATA VALIDATION

Validation layer detects:
- Impossible values
- Missing required fields
- Stale data
- Conflicting data
- Malformed ticker symbols
- Invalid percentages
- Invalid financial ratios

Generate warnings for questionable data.

---

## 18. MODEL VERSIONING

Every scoring methodology has version:
```
MODEL_VERSION = "1.0.0"
```

When weights/methodology change:
- Increment version
- Document change
- Preserve old results
- Never rewrite historical scores

Maintain CHANGELOG.md

---

## 19. README

Complete README includes:
- Project description
- Installation instructions
- Environment setup
- Running the model
- Adding stocks
- How scoring works
- Report generation
- Running tests
- Historical tracking
- Limitations
- Responsible-use disclaimer
- Examples

---

## 20. COMMAND-LINE INTERFACE

Support commands:
```bash
python -m src.main                    # Current rankings, scores, recommended candidate
python -m src.main --ticker PLTR      # Analyze specific company
```

Output:
- Current rankings
- Individual scores
- Recommended candidate
- Risks
- Catalysts
- Report location

---

## 21. CODE QUALITY

**Use:**
- Type hints
- Docstrings
- Clear variable names
- Small functions
- Modular design
- Error handling
- Logging

**Avoid:**
- Giant monolithic files
- Duplicated logic
- Hard-coded magic numbers
- Silent failures
- Fake data presented as real

---

## 22. DEVELOPMENT INSTRUCTION

Do not stop after skeleton.

Actually implement working code:
1. Install dependencies
2. Run pytest
3. Fix failures
4. Run application
5. Fix runtime errors
6. Verify scoring engine
7. Verify ranking
8. Verify missing-data handling
9. Verify historical tracking
10. Update README

External APIs: Support demo/mock dataset for testing without credentials.

---

## 23. FIRST IMPLEMENTATION GOAL

Version 1.0: Fully functioning research and scoring engine.

Pipeline:
```
Input company data
    ↓
Validate data
    ↓
Analyze fundamentals
    ↓
Analyze valuation
    ↓
Analyze momentum
    ↓
Analyze risk
    ↓
Calculate 0–100 score
    ↓
Assign classification
    ↓
Rank candidates
    ↓
Generate explanation/report
    ↓
Save historical prediction
```

---

## 24. FINAL PRINCIPLE

**NOT:** Lowest share price, current hype, highest growth, guaranteed profit

**GOAL:** Identify companies where combination of:
- Future growth potential
- Business quality
- Financial strength
- Valuation
- Competitive advantage
- Catalysts
- Risk profile

creates attractive risk-adjusted investment opportunity.

Favor evidence over hype. Maintain historical record to validate methodology.
