"""
Data loader module for fetching company financial data.
Supports both real market data and mock/demo data.
"""

import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class CompanyData:
    """Normalized company financial data structure."""
    
    ticker: str
    company_name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    share_price: Optional[float] = None
    revenue: Optional[float] = None
    revenue_growth: Optional[float] = None
    eps: Optional[float] = None
    eps_growth: Optional[float] = None
    free_cash_flow: Optional[float] = None
    free_cash_flow_growth: Optional[float] = None
    cash: Optional[float] = None
    debt: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    pe_ratio: Optional[float] = None
    price_to_sales: Optional[float] = None
    price_to_fcf: Optional[float] = None
    one_month_return: Optional[float] = None
    three_month_return: Optional[float] = None
    six_month_return: Optional[float] = None
    one_year_return: Optional[float] = None
    insider_activity: Optional[str] = None  # "buying", "selling", "neutral", "unknown"
    institutional_activity: Optional[str] = None  # "accumulating", "reducing", "neutral", "unknown"
    industry_growth: Optional[float] = None
    competitive_advantage: Optional[List[str]] = field(default_factory=list)
    catalysts: Optional[List[str]] = field(default_factory=list)
    inflation_resilience: Optional[str] = None  # "high", "medium", "low", "unknown"
    risk_factors: Optional[List[str]] = field(default_factory=list)
    data_timestamp: datetime = field(default_factory=datetime.now)
    data_sources: Dict[str, str] = field(default_factory=dict)


class DataLoader:
    """Load and manage company financial data."""
    
    def __init__(self, use_mock_data: bool = True):
        """
        Initialize data loader.
        
        Args:
            use_mock_data: If True, use mock data. If False, fetch real data.
        """
        self.use_mock_data = use_mock_data
        self.data_cache: Dict[str, CompanyData] = {}
        logger.info(f"DataLoader initialized (mock_data={use_mock_data})")
    
    def load_company(self, ticker: str) -> Optional[CompanyData]:
        """
        Load data for a single company.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            CompanyData object or None if data unavailable
        """
        if ticker in self.data_cache:
            return self.data_cache[ticker]
        
        if self.use_mock_data:
            return self._load_mock_data(ticker)
        else:
            return self._load_real_data(ticker)
    
    def load_multiple(self, tickers: List[str]) -> List[CompanyData]:
        """
        Load data for multiple companies.
        
        Args:
            tickers: List of stock ticker symbols
            
        Returns:
            List of CompanyData objects
        """
        results = []
        for ticker in tickers:
            data = self.load_company(ticker)
            if data:
                results.append(data)
                self.data_cache[ticker] = data
            else:
                logger.warning(f"Failed to load data for {ticker}")
        
        return results
    
    def _load_mock_data(self, ticker: str) -> CompanyData:
        """Load mock/demo data for testing without API credentials."""
        mock_data = {
            "NVDA": {
                "company_name": "NVIDIA Corporation",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 1.2e12,
                "share_price": 875.00,
                "revenue": 60.9e9,
                "revenue_growth": 0.126,  # 12.6%
                "eps": 3.85,
                "eps_growth": 0.189,  # 18.9%
                "free_cash_flow": 28.0e9,
                "free_cash_flow_growth": 0.156,
                "cash": 22.0e9,
                "debt": 8.0e9,
                "gross_margin": 0.65,
                "operating_margin": 0.38,
                "pe_ratio": 65.2,
                "price_to_sales": 19.7,
                "price_to_fcf": 37.6,
                "one_month_return": 0.082,  # 8.2%
                "three_month_return": 0.156,  # 15.6%
                "six_month_return": 0.312,  # 31.2%
                "one_year_return": 0.89,  # 89%
                "insider_activity": "neutral",
                "institutional_activity": "accumulating",
                "industry_growth": 0.15,
                "competitive_advantage": ["Moat (GPU technology)", "Scale", "Patent IP"],
                "catalysts": ["AI adoption acceleration", "Data center growth"],
                "inflation_resilience": "medium",
                "risk_factors": ["High valuation", "Concentration in AI", "Geopolitical risk"],
            },
            "PLTR": {
                "company_name": "Palantir Technologies Inc.",
                "sector": "Information Technology",
                "industry": "Software",
                "market_cap": 62.5e9,
                "share_price": 29.50,
                "revenue": 2.23e9,
                "revenue_growth": 0.27,  # 27%
                "eps": 0.06,
                "eps_growth": 0.50,  # 50%
                "free_cash_flow": 0.5e9,
                "free_cash_flow_growth": 0.40,
                "cash": 2.8e9,
                "debt": 0.5e9,
                "gross_margin": 0.78,
                "operating_margin": 0.08,
                "pe_ratio": 491.7,
                "price_to_sales": 28.0,
                "price_to_fcf": 59.0,
                "one_month_return": 0.065,  # 6.5%
                "three_month_return": 0.125,  # 12.5%
                "six_month_return": 0.245,  # 24.5%
                "one_year_return": 0.48,  # 48%
                "insider_activity": "buying",
                "institutional_activity": "accumulating",
                "industry_growth": 0.12,
                "competitive_advantage": ["Government relationships", "Data analytics", "Switching costs"],
                "catalysts": ["Commercial revenue growth", "Profitability milestone"],
                "inflation_resilience": "high",
                "risk_factors": ["High valuation", "Limited profitability", "Customer concentration"],
            },
            "AMD": {
                "company_name": "Advanced Micro Devices Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 220.0e9,
                "share_price": 165.30,
                "revenue": 22.7e9,
                "revenue_growth": 0.04,  # 4%
                "eps": 3.42,
                "eps_growth": -0.15,  # -15%
                "free_cash_flow": 2.5e9,
                "free_cash_flow_growth": -0.45,
                "cash": 3.2e9,
                "debt": 1.0e9,
                "gross_margin": 0.48,
                "operating_margin": 0.18,
                "pe_ratio": 48.3,
                "price_to_sales": 9.7,
                "price_to_fcf": 66.1,
                "one_month_return": 0.021,  # 2.1%
                "three_month_return": -0.045,  # -4.5%
                "six_month_return": 0.08,  # 8%
                "one_year_return": 0.15,  # 15%
                "insider_activity": "neutral",
                "institutional_activity": "reducing",
                "industry_growth": 0.15,
                "competitive_advantage": ["GPU design", "EPYC servers", "Manufacturing partnerships"],
                "catalysts": ["New GPU architecture launch", "Data center recovery"],
                "inflation_resilience": "medium",
                "risk_factors": ["EPS decline", "Margin compression", "NVIDIA competition"],
            },
            "AVGO": {
                "company_name": "Broadcom Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 315.0e9,
                "share_price": 189.20,
                "revenue": 36.8e9,
                "revenue_growth": 0.11,  # 11%
                "eps": 8.62,
                "eps_growth": 0.22,  # 22%
                "free_cash_flow": 10.5e9,
                "free_cash_flow_growth": 0.18,
                "cash": 5.5e9,
                "debt": 18.0e9,
                "gross_margin": 0.68,
                "operating_margin": 0.35,
                "pe_ratio": 21.9,
                "price_to_sales": 8.6,
                "price_to_fcf": 18.0,
                "one_month_return": 0.055,  # 5.5%
                "three_month_return": 0.095,  # 9.5%
                "six_month_return": 0.185,  # 18.5%
                "one_year_return": 0.38,  # 38%
                "insider_activity": "neutral",
                "institutional_activity": "accumulating",
                "industry_growth": 0.15,
                "competitive_advantage": ["Connectivity solutions", "Diversified customer base", "Scale"],
                "catalysts": ["AI infrastructure demand", "5G buildout continuation"],
                "inflation_resilience": "high",
                "risk_factors": ["High debt", "Cyclical business", "Competition"],
            },
            "AMAT": {
                "company_name": "Applied Materials Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 195.0e9,
                "share_price": 198.50,
                "revenue": 26.5e9,
                "revenue_growth": 0.08,  # 8%
                "eps": 6.18,
                "eps_growth": 0.12,  # 12%
                "free_cash_flow": 5.2e9,
                "free_cash_flow_growth": 0.08,
                "cash": 4.8e9,
                "debt": 6.5e9,
                "gross_margin": 0.45,
                "operating_margin": 0.25,
                "pe_ratio": 32.1,
                "price_to_sales": 7.4,
                "price_to_fcf": 38.2,
                "one_month_return": 0.032,  # 3.2%
                "three_month_return": 0.068,  # 6.8%
                "six_month_return": 0.125,  # 12.5%
                "one_year_return": 0.28,  # 28%
                "insider_activity": "neutral",
                "institutional_activity": "neutral",
                "industry_growth": 0.15,
                "competitive_advantage": ["Equipment innovation", "Customer relationships", "Technology"],
                "catalysts": ["Semiconductor equipment demand", "Advanced node ramp"],
                "inflation_resilience": "medium",
                "risk_factors": ["Cyclical", "Capital intensity", "Concentration risk"],
            },
            "MU": {
                "company_name": "Micron Technology Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 85.0e9,
                "share_price": 108.75,
                "revenue": 30.0e9,
                "revenue_growth": -0.02,  # -2%
                "eps": 4.38,
                "eps_growth": -0.25,  # -25%
                "free_cash_flow": 2.8e9,
                "free_cash_flow_growth": -0.55,
                "cash": 2.5e9,
                "debt": 8.0e9,
                "gross_margin": 0.35,
                "operating_margin": 0.10,
                "pe_ratio": 24.8,
                "price_to_sales": 2.8,
                "price_to_fcf": 38.8,
                "one_month_return": 0.045,  # 4.5%
                "three_month_return": 0.085,  # 8.5%
                "six_month_return": 0.12,  # 12%
                "one_year_return": 0.32,  # 32%
                "insider_activity": "buying",
                "institutional_activity": "neutral",
                "industry_growth": 0.15,
                "competitive_advantage": ["DRAM/NAND manufacturing", "Cost structure", "Patents"],
                "catalysts": ["Memory market recovery", "AI demand surge"],
                "inflation_resilience": "low",
                "risk_factors": ["Cyclical downturn", "Oversupply", "Margin pressure"],
            },
            "CRWD": {
                "company_name": "CrowdStrike Holdings Inc.",
                "sector": "Information Technology",
                "industry": "Cybersecurity",
                "market_cap": 38.5e9,
                "share_price": 125.00,
                "revenue": 2.24e9,
                "revenue_growth": 0.35,  # 35%
                "eps": 0.82,
                "eps_growth": 0.48,  # 48%
                "free_cash_flow": 0.65e9,
                "free_cash_flow_growth": 0.42,
                "cash": 1.2e9,
                "debt": 0.1e9,
                "gross_margin": 0.76,
                "operating_margin": 0.18,
                "pe_ratio": 152.4,
                "price_to_sales": 17.2,
                "price_to_fcf": 192.3,
                "one_month_return": 0.025,  # 2.5%
                "three_month_return": 0.045,  # 4.5%
                "six_month_return": 0.085,  # 8.5%
                "one_year_return": 0.42,  # 42%
                "insider_activity": "neutral",
                "institutional_activity": "accumulating",
                "industry_growth": 0.18,
                "competitive_advantage": ["AI-driven security", "Cloud platform", "Customer switching costs"],
                "catalysts": ["Emerging threat response", "International expansion"],
                "inflation_resilience": "high",
                "risk_factors": ["High valuation", "Rapid growth sustainability", "Market saturation risk"],
            },
            "PANW": {
                "company_name": "Palo Alto Networks Inc.",
                "sector": "Information Technology",
                "industry": "Cybersecurity",
                "market_cap": 68.5e9,
                "share_price": 275.50,
                "revenue": 7.48e9,
                "revenue_growth": 0.26,  # 26%
                "eps": 3.45,
                "eps_growth": 0.35,  # 35%
                "free_cash_flow": 1.8e9,
                "free_cash_flow_growth": 0.28,
                "cash": 2.1e9,
                "debt": 3.5e9,
                "gross_margin": 0.76,
                "operating_margin": 0.15,
                "pe_ratio": 79.9,
                "price_to_sales": 9.2,
                "price_to_fcf": 152.5,
                "one_month_return": 0.038,  # 3.8%
                "three_month_return": 0.068,  # 6.8%
                "six_month_return": 0.125,  # 12.5%
                "one_year_return": 0.35,  # 35%
                "insider_activity": "neutral",
                "institutional_activity": "accumulating",
                "industry_growth": 0.18,
                "competitive_advantage": ["Consolidated security platform", "Customer relationships", "Brand"],
                "catalysts": ["AI security features", "Cloud adoption acceleration"],
                "inflation_resilience": "high",
                "risk_factors": ["High valuation", "Competition", "Integration risks"],
            },
            "TER": {
                "company_name": "Teradyne Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 28.0e9,
                "share_price": 142.00,
                "revenue": 3.36e9,
                "revenue_growth": -0.05,  # -5%
                "eps": 3.28,
                "eps_growth": -0.18,  # -18%
                "free_cash_flow": 0.58e9,
                "free_cash_flow_growth": -0.35,
                "cash": 0.95e9,
                "debt": 2.1e9,
                "gross_margin": 0.58,
                "operating_margin": 0.22,
                "pe_ratio": 43.3,
                "price_to_sales": 8.3,
                "price_to_fcf": 245.0,
                "one_month_return": 0.028,  # 2.8%
                "three_month_return": -0.032,  # -3.2%
                "six_month_return": 0.065,  # 6.5%
                "one_year_return": 0.18,  # 18%
                "insider_activity": "neutral",
                "institutional_activity": "reducing",
                "industry_growth": 0.12,
                "competitive_advantage": ["Test equipment technology", "Industry relationships"],
                "catalysts": ["Semiconductor cycle recovery", "AI chip testing demand"],
                "inflation_resilience": "medium",
                "risk_factors": ["Declining revenue", "EPS contraction", "Cyclical downturn"],
            },
            "ACMR": {
                "company_name": "ACM Research Inc.",
                "sector": "Information Technology",
                "industry": "Semiconductors",
                "market_cap": 5.2e9,
                "share_price": 82.50,
                "revenue": 0.285e9,
                "revenue_growth": 0.48,  # 48%
                "eps": 0.45,
                "eps_growth": 0.85,  # 85%
                "free_cash_flow": 0.04e9,
                "free_cash_flow_growth": 0.25,
                "cash": 0.38e9,
                "debt": 0.05e9,
                "gross_margin": 0.45,
                "operating_margin": 0.08,
                "pe_ratio": 183.3,
                "price_to_sales": 18.2,
                "price_to_fcf": 2062.5,
                "one_month_return": 0.062,  # 6.2%
                "three_month_return": 0.145,  # 14.5%
                "six_month_return": 0.32,  # 32%
                "one_year_return": 1.25,  # 125%
                "insider_activity": "buying",
                "institutional_activity": "accumulating",
                "industry_growth": 0.15,
                "competitive_advantage": ["Innovative cleaning tech", "Growth trajectory", "Customer traction"],
                "catalysts": ["Advanced node adoption", "Market share gains"],
                "inflation_resilience": "low",
                "risk_factors": ["Very high valuation", "Small-cap", "Limited profitability", "Liquidity"],
            },
            "CRDO": {
                "company_name": "Corrado Inc.",
                "sector": "Information Technology",
                "industry": "Software",
                "market_cap": 12.5e9,
                "share_price": 45.25,
                "revenue": 0.52e9,
                "revenue_growth": 0.42,  # 42%
                "eps": 0.08,
                "eps_growth": 1.50,  # 150%
                "free_cash_flow": 0.06e9,
                "free_cash_flow_growth": 0.55,
                "cash": 0.42e9,
                "debt": 0.1e9,
                "gross_margin": 0.68,
                "operating_margin": 0.05,
                "pe_ratio": 565.6,
                "price_to_sales": 24.0,
                "price_to_fcf": 754.2,
                "one_month_return": 0.085,  # 8.5%
                "three_month_return": 0.185,  # 18.5%
                "six_month_return": 0.425,  # 42.5%
                "one_year_return": 1.68,  # 168%
                "insider_activity": "buying",
                "institutional_activity": "accumulating",
                "industry_growth": 0.14,
                "competitive_advantage": ["Emerging tech", "High growth", "Market position"],
                "catalysts": ["Product launches", "Market expansion"],
                "inflation_resilience": "low",
                "risk_factors": ["Extremely high valuation", "Not profitable", "Small-cap", "High risk"],
            },
        }
        
        if ticker in mock_data:
            data_dict = mock_data[ticker]
            return CompanyData(
                ticker=ticker,
                data_timestamp=datetime.now(),
                data_sources={"mock": "demo_data_v1.0"},
                **data_dict
            )
        else:
            logger.warning(f"Mock data not available for {ticker}")
            return None
    
    def _load_real_data(self, ticker: str) -> Optional[CompanyData]:
        """
        Load real data from market data providers.
        This would integrate with yfinance, Alpha Vantage, etc.
        For now, returns None - to be implemented.
        """
        logger.warning(f"Real data loading not yet implemented for {ticker}")
        return None
