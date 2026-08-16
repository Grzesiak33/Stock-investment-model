"""
Core scoring engine for evaluating stocks.
Produces 0-100 score across 10 categories.
"""

import logging
from typing import Optional, List, Dict
from dataclasses import dataclass
from src.data_loader import CompanyData
from src.config import SCORING_WEIGHTS, CLASSIFICATION_THRESHOLDS

logger = logging.getLogger(__name__)


@dataclass
class StockScore:
    """Complete stock score with all category breakdowns."""
    
    ticker: str
    company_name: str
    
    # Category scores
    revenue_growth: float  # 0-15
    earnings_fcf: float  # 0-15
    industry_growth: float  # 0-15
    balance_sheet: float  # 0-10
    valuation: float  # 0-10
    competitive_advantage: float  # 0-10
    momentum: float  # 0-10
    insider_institutional: float  # 0-5
    catalysts: float  # 0-5
    inflation_resilience: float  # 0-5
    
    # Total and classification
    total_score: float  # 0-100
    classification: str  # BUY, WATCH, INTERESTING, RESEARCH, REJECT
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "ticker": self.ticker,
            "company_name": self.company_name,
            "revenue_growth": self.revenue_growth,
            "earnings_fcf": self.earnings_fcf,
            "industry_growth": self.industry_growth,
            "balance_sheet": self.balance_sheet,
            "valuation": self.valuation,
            "competitive_advantage": self.competitive_advantage,
            "momentum": self.momentum,
            "insider_institutional": self.insider_institutional,
            "catalysts": self.catalysts,
            "inflation_resilience": self.inflation_resilience,
            "total_score": self.total_score,
            "classification": self.classification,
        }


class ScoringEngine:
    """Calculate investment scores for stocks."""
    
    def __init__(self):
        """Initialize scoring engine."""
        self._validate_weights()
    
    def _validate_weights(self) -> None:
        """Ensure scoring weights sum to exactly 100."""
        total = sum(SCORING_WEIGHTS.values())
        assert total == 100, f"Scoring weights must sum to 100, got {total}"
        logger.info(f"Scoring weights validated: {total} points total")
    
    def score_company(self, company: CompanyData) -> StockScore:
        """
        Calculate investment score for a company.
        
        Args:
            company: CompanyData object with financial metrics
            
        Returns:
            StockScore with all category scores and total
        """
        # Calculate individual category scores
        revenue_growth_score = self._score_revenue_growth(company)
        earnings_fcf_score = self._score_earnings_fcf(company)
        industry_growth_score = self._score_industry_growth(company)
        balance_sheet_score = self._score_balance_sheet(company)
        valuation_score = self._score_valuation(company)
        competitive_advantage_score = self._score_competitive_advantage(company)
        momentum_score = self._score_momentum(company)
        insider_institutional_score = self._score_insider_institutional(company)
        catalysts_score = self._score_catalysts(company)
        inflation_resilience_score = self._score_inflation_resilience(company)
        
        # Calculate total score
        total_score = (
            revenue_growth_score +
            earnings_fcf_score +
            industry_growth_score +
            balance_sheet_score +
            valuation_score +
            competitive_advantage_score +
            momentum_score +
            insider_institutional_score +
            catalysts_score +
            inflation_resilience_score
        )
        
        # Clamp to 0-100
        total_score = max(0, min(100, total_score))
        
        # Determine classification
        classification = self._classify_score(total_score)
        
        # Create score object
        score = StockScore(
            ticker=company.ticker,
            company_name=company.company_name,
            revenue_growth=revenue_growth_score,
            earnings_fcf=earnings_fcf_score,
            industry_growth=industry_growth_score,
            balance_sheet=balance_sheet_score,
            valuation=valuation_score,
            competitive_advantage=competitive_advantage_score,
            momentum=momentum_score,
            insider_institutional=insider_institutional_score,
            catalysts=catalysts_score,
            inflation_resilience=inflation_resilience_score,
            total_score=total_score,
            classification=classification,
        )
        
        logger.debug(f"{company.ticker}: Score={total_score:.1f} ({classification})")
        return score
    
    def _score_revenue_growth(self, company: CompanyData) -> float:
        """Score revenue growth (0-15 points)."""
        max_points = SCORING_WEIGHTS["revenue_growth"]
        
        if company.revenue_growth is None:
            return 0
        
        growth_rate = company.revenue_growth
        
        # Scoring logic:
        # < 0% growth: 0 points
        # 0-5%: 3 points
        # 5-10%: 6 points
        # 10-15%: 9 points
        # 15-25%: 12 points
        # 25%+: 15 points
        
        if growth_rate < 0:
            score = 0
        elif growth_rate < 0.05:
            score = 3
        elif growth_rate < 0.10:
            score = 6
        elif growth_rate < 0.15:
            score = 9
        elif growth_rate < 0.25:
            score = 12
        else:
            score = 15
        
        return min(score, max_points)
    
    def _score_earnings_fcf(self, company: CompanyData) -> float:
        """Score earnings and free cash flow (0-15 points)."""
        max_points = SCORING_WEIGHTS["earnings_fcf"]
        
        # Consider both EPS growth and FCF growth
        eps_growth = company.eps_growth or 0
        fcf_growth = company.free_cash_flow_growth or 0
        
        # Average the two if both available
        if company.eps_growth is not None and company.free_cash_flow_growth is not None:
            avg_growth = (eps_growth + fcf_growth) / 2
        elif company.eps_growth is not None:
            avg_growth = eps_growth
        elif company.free_cash_flow_growth is not None:
            avg_growth = fcf_growth
        else:
            return 0
        
        # Scoring:
        # < 0%: 0 points
        # 0-5%: 3 points
        # 5-10%: 6 points
        # 10-20%: 10 points
        # 20%+: 15 points
        
        if avg_growth < 0:
            score = 0
        elif avg_growth < 0.05:
            score = 3
        elif avg_growth < 0.10:
            score = 6
        elif avg_growth < 0.20:
            score = 10
        else:
            score = 15
        
        # Deduction for negative profitability
        if company.eps is not None and company.eps < 0:
            score = max(0, score - 5)
        
        return min(score, max_points)
    
    def _score_industry_growth(self, company: CompanyData) -> float:
        """Score industry growth potential (0-15 points)."""
        max_points = SCORING_WEIGHTS["industry_growth"]
        
        if company.industry_growth is None:
            return 7.5  # Neutral score if unknown
        
        growth = company.industry_growth
        
        # Scoring:
        # < 0%: 0 points
        # 0-3%: 3 points
        # 3-8%: 7.5 points
        # 8-15%: 12 points
        # 15%+: 15 points
        
        if growth < 0:
            score = 0
        elif growth < 0.03:
            score = 3
        elif growth < 0.08:
            score = 7.5
        elif growth < 0.15:
            score = 12
        else:
            score = 15
        
        return min(score, max_points)
    
    def _score_balance_sheet(self, company: CompanyData) -> float:
        """Score balance sheet strength (0-10 points)."""
        max_points = SCORING_WEIGHTS["balance_sheet"]
        
        score = 0
        
        # Debt-to-equity considerations
        if company.debt is not None and company.cash is not None:
            net_debt = company.debt - company.cash
            if net_debt < 0:  # More cash than debt
                score += 4
            elif company.debt < 5e9:  # Manageable debt
                score += 2
            else:
                score += 0  # High debt
        
        # Cash position
        if company.cash is not None:
            if company.cash > 10e9:
                score += 3
            elif company.cash > 1e9:
                score += 2
            elif company.cash > 0.1e9:
                score += 1
        
        # Profitability contribution
        if company.operating_margin is not None:
            if company.operating_margin > 0.20:
                score += 3
            elif company.operating_margin > 0.10:
                score += 2
            elif company.operating_margin > 0:
                score += 1
        
        return min(score, max_points)
    
    def _score_valuation(self, company: CompanyData) -> float:
        """Score valuation attractiveness (0-10 points)."""
        max_points = SCORING_WEIGHTS["valuation"]
        
        # NOTE: This uses RELATIVE metrics, not absolute share price
        # Rule A: Share price is NOT valuation
        
        score = 5  # Start with neutral
        
        # P/E ratio assessment
        if company.pe_ratio is not None and company.pe_ratio > 0:
            if company.pe_ratio < 15:
                score += 3
            elif company.pe_ratio < 25:
                score += 2
            elif company.pe_ratio < 40:
                score += 1
            else:
                score -= 2  # High P/E is concerning
        
        # P/S ratio assessment
        if company.price_to_sales is not None and company.price_to_sales > 0:
            if company.price_to_sales < 2:
                score += 2
            elif company.price_to_sales < 5:
                score += 1
            elif company.price_to_sales < 10:
                score += 0
            else:
                score -= 1
        
        # Growth adjusted valuation (PEG-like)
        if (company.pe_ratio is not None and company.revenue_growth is not None and
            company.pe_ratio > 0 and company.revenue_growth > 0):
            peg = company.pe_ratio / (company.revenue_growth * 100)
            if peg < 1.0:
                score += 1
            elif peg > 2.0:
                score -= 1
        
        return max(0, min(score, max_points))
    
    def _score_competitive_advantage(self, company: CompanyData) -> float:
        """Score competitive advantage / moat (0-10 points)."""
        max_points = SCORING_WEIGHTS["competitive_advantage"]
        
        if not company.competitive_advantage:
            return 3  # Some neutral score
        
        # Score based on number and quality of advantages
        moat_count = len(company.competitive_advantage)
        
        if moat_count >= 4:
            score = 10
        elif moat_count >= 3:
            score = 8
        elif moat_count >= 2:
            score = 6
        elif moat_count >= 1:
            score = 4
        else:
            score = 2
        
        return min(score, max_points)
    
    def _score_momentum(self, company: CompanyData) -> float:
        """Score price momentum (0-10 points)."""
        max_points = SCORING_WEIGHTS["momentum"]
        
        # NOTE: Momentum is only 10% of score - Rule B: Do not chase hype
        
        returns = []
        weights = []
        
        # Collect available returns with different weights (more recent = more weight)
        if company.one_month_return is not None:
            returns.append(company.one_month_return)
            weights.append(0.4)
        
        if company.three_month_return is not None:
            returns.append(company.three_month_return)
            weights.append(0.3)
        
        if company.six_month_return is not None:
            returns.append(company.six_month_return)
            weights.append(0.2)
        
        if company.one_year_return is not None:
            returns.append(company.one_year_return)
            weights.append(0.1)
        
        if not returns:
            return 5  # Neutral if no data
        
        # Calculate weighted average return
        weighted_return = sum(r * w for r, w in zip(returns, weights)) / sum(weights)
        
        # Scoring:
        # < -30%: 0 points
        # -30% to 0%: 2 points
        # 0% to 10%: 4 points
        # 10% to 30%: 7 points
        # 30%+: 10 points (but capped)
        
        if weighted_return < -0.30:
            score = 0
        elif weighted_return < 0:
            score = 2
        elif weighted_return < 0.10:
            score = 4
        elif weighted_return < 0.30:
            score = 7
        else:
            score = 10
        
        return min(score, max_points)
    
    def _score_insider_institutional(self, company: CompanyData) -> float:
        """Score insider/institutional activity (0-5 points)."""
        max_points = SCORING_WEIGHTS["insider_institutional"]
        
        score = 2.5  # Start neutral
        
        # Insider activity
        if company.insider_activity == "buying":
            score += 1.5
        elif company.insider_activity == "selling":
            score -= 1
        
        # Institutional activity
        if company.institutional_activity == "accumulating":
            score += 1.5
        elif company.institutional_activity == "reducing":
            score -= 1
        
        return max(0, min(score, max_points))
    
    def _score_catalysts(self, company: CompanyData) -> float:
        """Score identifiable catalysts (0-5 points)."""
        max_points = SCORING_WEIGHTS["catalysts"]
        
        if not company.catalysts:
            return 1  # Minimal score if no catalysts identified
        
        catalyst_count = len(company.catalysts)
        
        if catalyst_count >= 3:
            score = 5
        elif catalyst_count >= 2:
            score = 4
        elif catalyst_count >= 1:
            score = 2
        else:
            score = 1
        
        return min(score, max_points)
    
    def _score_inflation_resilience(self, company: CompanyData) -> float:
        """Score inflation resilience and pricing power (0-5 points)."""
        max_points = SCORING_WEIGHTS["inflation_resilience"]
        
        if company.inflation_resilience is None:
            return 2.5  # Neutral
        
        resilience = company.inflation_resilience.lower()
        
        if resilience == "high":
            score = 5
        elif resilience == "medium":
            score = 3
        elif resilience == "low":
            score = 1
        else:
            score = 2.5
        
        # Adjust based on gross margin if available
        if company.gross_margin is not None:
            if company.gross_margin > 0.60:
                score = min(score + 0.5, max_points)
            elif company.gross_margin < 0.30:
                score = max(score - 0.5, 0)
        
        return min(score, max_points)
    
    def _classify_score(self, total_score: float) -> str:
        """Determine classification based on score."""
        for classification, (min_score, max_score) in CLASSIFICATION_THRESHOLDS.items():
            if min_score <= total_score <= max_score:
                return classification
        
        # Fallback (shouldn't happen if thresholds are complete)
        if total_score >= 85:
            return "BUY"
        elif total_score >= 75:
            return "WATCH"
        elif total_score >= 65:
            return "INTERESTING"
        elif total_score >= 50:
            return "RESEARCH"
        else:
            return "REJECT"


def score_multiple(companies: List[CompanyData]) -> List[StockScore]:
    """
    Score multiple companies.
    
    Args:
        companies: List of CompanyData objects
        
    Returns:
        List of StockScore objects
    """
    engine = ScoringEngine()
    scores = []
    
    for company in companies:
        try:
            score = engine.score_company(company)
            scores.append(score)
        except Exception as e:
            logger.error(f"Error scoring {company.ticker}: {e}")
    
    return scores
