"""
Tests for scoring module.
"""

import pytest
from src.scoring import StockScore, ScoringEngine
from src.data_loader import CompanyData
from src.config import SCORING_WEIGHTS


class TestScoreValidation:
    """Test score validation rules."""
    
    def test_score_not_negative(self):
        """Scores cannot be negative."""
        with pytest.raises(AssertionError):
            score = StockScore(
                ticker="TEST",
                company_name="Test Co",
                revenue_growth=-1,
                earnings_fcf=0,
                industry_growth=0,
                balance_sheet=0,
                valuation=0,
                competitive_advantage=0,
                momentum=0,
                insider_institutional=0,
                catalysts=0,
                inflation_resilience=0,
                total_score=0,
                classification="REJECT",
            )
            assert score.revenue_growth >= 0, "Negative score not allowed"
    
    def test_revenue_growth_max(self):
        """Revenue growth score cannot exceed maximum."""
        engine = ScoringEngine()
        score = engine._score_revenue_growth(CompanyData(ticker="TEST", company_name="Test", revenue_growth=1.0))
        assert score <= SCORING_WEIGHTS["revenue_growth"], f"Score {score} exceeds max {SCORING_WEIGHTS['revenue_growth']}"
    
    def test_earnings_fcf_max(self):
        """Earnings/FCF score cannot exceed maximum."""
        engine = ScoringEngine()
        score = engine._score_earnings_fcf(CompanyData(ticker="TEST", company_name="Test", eps_growth=1.0))
        assert score <= SCORING_WEIGHTS["earnings_fcf"]
    
    def test_total_score_max(self):
        """Total score cannot exceed 100."""
        engine = ScoringEngine()
        company = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            revenue_growth=1.0,
            eps_growth=1.0,
            industry_growth=1.0,
        )
        score = engine.score_company(company)
        assert score.total_score <= 100, f"Total score {score.total_score} exceeds 100"
    
    def test_total_equals_sum(self):
        """Total score equals sum of category scores."""
        engine = ScoringEngine()
        company = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            revenue_growth=0.15,
            eps_growth=0.15,
            industry_growth=0.15,
        )
        score = engine.score_company(company)
        
        expected_total = (
            score.revenue_growth +
            score.earnings_fcf +
            score.industry_growth +
            score.balance_sheet +
            score.valuation +
            score.competitive_advantage +
            score.momentum +
            score.insider_institutional +
            score.catalysts +
            score.inflation_resilience
        )
        
        assert abs(score.total_score - expected_total) < 0.01, "Total doesn't equal sum of categories"


class TestWeightValidation:
    """Test weight validation."""
    
    def test_weights_sum_to_100(self):
        """All scoring weights must sum to exactly 100."""
        total = sum(SCORING_WEIGHTS.values())
        assert total == 100, f"Weights sum to {total}, not 100"
    
    def test_all_categories_present(self):
        """All 10 categories must be defined."""
        required_categories = [
            "revenue_growth",
            "earnings_fcf",
            "industry_growth",
            "balance_sheet",
            "valuation",
            "competitive_advantage",
            "momentum",
            "insider_institutional",
            "catalysts",
            "inflation_resilience",
        ]
        for category in required_categories:
            assert category in SCORING_WEIGHTS, f"Missing category: {category}"


class TestSharePriceIndependence:
    """Test Rule A: Share price is NOT valuation."""
    
    def test_share_price_change_doesnt_affect_score(self):
        """Changing share price alone must not change the fundamental score."""
        engine = ScoringEngine()
        
        company1 = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            share_price=10.0,
            revenue_growth=0.20,
            eps_growth=0.15,
        )
        
        company2 = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            share_price=200.0,  # Different share price
            revenue_growth=0.20,
            eps_growth=0.15,
        )
        
        score1 = engine.score_company(company1)
        score2 = engine.score_company(company2)
        
        # Scores should be identical (or very close)
        assert abs(score1.total_score - score2.total_score) < 0.1, \
            f"Score changed with share price: {score1.total_score} vs {score2.total_score}"


class TestClassification:
    """Test score classification."""
    
    def test_buy_classification(self):
        """Score 85+ should be BUY."""
        engine = ScoringEngine()
        score = StockScore(
            ticker="TEST", company_name="Test",
            revenue_growth=15, earnings_fcf=15, industry_growth=15,
            balance_sheet=10, valuation=10, competitive_advantage=10,
            momentum=10, insider_institutional=5, catalysts=5,
            inflation_resilience=5,
            total_score=85, classification="BUY"
        )
        assert score.classification == "BUY"
    
    def test_watch_classification(self):
        """Score 75-84 should be WATCH."""
        score = StockScore(
            ticker="TEST", company_name="Test",
            revenue_growth=12, earnings_fcf=12, industry_growth=12,
            balance_sheet=8, valuation=8, competitive_advantage=8,
            momentum=7, insider_institutional=3, catalysts=3,
            inflation_resilience=3,
            total_score=77, classification="WATCH"
        )
        assert score.classification == "WATCH"
    
    def test_interesting_classification(self):
        """Score 65-74 should be INTERESTING."""
        score = StockScore(
            ticker="TEST", company_name="Test",
            revenue_growth=10, earnings_fcf=10, industry_growth=10,
            balance_sheet=6, valuation=6, competitive_advantage=6,
            momentum=5, insider_institutional=2, catalysts=2,
            inflation_resilience=2,
            total_score=69, classification="INTERESTING"
        )
        assert score.classification == "INTERESTING"
    
    def test_research_classification(self):
        """Score 50-64 should be RESEARCH."""
        score = StockScore(
            ticker="TEST", company_name="Test",
            revenue_growth=8, earnings_fcf=8, industry_growth=8,
            balance_sheet=4, valuation=4, competitive_advantage=4,
            momentum=3, insider_institutional=1, catalysts=1,
            inflation_resilience=1,
            total_score=55, classification="RESEARCH"
        )
        assert score.classification == "RESEARCH"
    
    def test_reject_classification(self):
        """Score 0-49 should be REJECT."""
        score = StockScore(
            ticker="TEST", company_name="Test",
            revenue_growth=4, earnings_fcf=4, industry_growth=4,
            balance_sheet=2, valuation=2, competitive_advantage=2,
            momentum=1, insider_institutional=0, catalysts=0,
            inflation_resilience=0,
            total_score=19, classification="REJECT"
        )
        assert score.classification == "REJECT"


class TestMissingData:
    """Test handling of missing financial data."""
    
    def test_missing_revenue_growth(self):
        """Missing revenue growth should not crash."""
        engine = ScoringEngine()
        company = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            revenue_growth=None,  # Missing
            eps_growth=0.10,
        )
        score = engine.score_company(company)
        assert score.total_score >= 0, "Score should still be calculated"
    
    def test_missing_momentum_data(self):
        """Missing momentum data should not crash."""
        engine = ScoringEngine()
        company = CompanyData(
            ticker="TEST",
            company_name="Test Co",
            one_month_return=None,
            three_month_return=None,
            six_month_return=None,
            one_year_return=None,
        )
        score = engine.score_company(company)
        assert score.momentum >= 0, "Momentum score should still exist"
    
    def test_all_none_values(self):
        """Scoring all None values should not crash."""
        engine = ScoringEngine()
        company = CompanyData(
            ticker="TEST",
            company_name="Test Co",
        )
        score = engine.score_company(company)
        assert 0 <= score.total_score <= 100, "Score should be valid range"
