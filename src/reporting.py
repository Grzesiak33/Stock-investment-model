"""
Reporting module for generating human-readable investment reports.
"""

import logging
from typing import List, Optional
from datetime import datetime
from src.scoring import StockScore
from src.data_loader import CompanyData
from src.ranking import RankedStock

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate human-readable investment reports."""
    
    def __init__(self):
        """Initialize report generator."""
        pass
    
    def generate_stock_report(self, ranked_stock: RankedStock) -> str:
        """
        Generate a detailed report for a single stock.
        
        Args:
            ranked_stock: RankedStock object with score and company data
            
        Returns:
            Formatted report string
        """
        s = ranked_stock.score
        c = ranked_stock.company
        
        lines = []
        lines.append("=" * 100)
        lines.append(f"STOCK ANALYSIS REPORT - {s.ticker}")
        lines.append("=" * 100)
        lines.append(f"Company: {s.company_name}")
        lines.append(f"Sector: {c.sector or 'N/A'}")
        lines.append(f"Industry: {c.industry or 'N/A'}")
        lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Overall Score
        lines.append(f"OVERALL SCORE: {s.total_score:.1f}/100")
        lines.append(f"CLASSIFICATION: {s.classification}")
        lines.append("")
        
        # Score Breakdown
        lines.append("CATEGORY SCORES:")
        lines.append("-" * 60)
        lines.append(f"  Revenue Growth:           {s.revenue_growth:>5.1f}/15")
        lines.append(f"  Earnings / FCF:           {s.earnings_fcf:>5.1f}/15")
        lines.append(f"  Industry Growth:          {s.industry_growth:>5.1f}/15")
        lines.append(f"  Balance Sheet:            {s.balance_sheet:>5.1f}/10")
        lines.append(f"  Valuation:                {s.valuation:>5.1f}/10")
        lines.append(f"  Competitive Advantage:    {s.competitive_advantage:>5.1f}/10")
        lines.append(f"  Momentum:                 {s.momentum:>5.1f}/10")
        lines.append(f"  Insider/Institutional:    {s.insider_institutional:>5.1f}/5")
        lines.append(f"  Catalysts:                {s.catalysts:>5.1f}/5")
        lines.append(f"  Inflation Resilience:     {s.inflation_resilience:>5.1f}/5")
        lines.append("-" * 60)
        lines.append(f"  TOTAL:                    {s.total_score:>5.1f}/100")
        lines.append("")
        
        # Key Metrics
        lines.append("KEY METRICS:")
        lines.append("-" * 60)
        if c.share_price:
            lines.append(f"  Share Price:              ${c.share_price:,.2f}")
        if c.market_cap:
            lines.append(f"  Market Cap:               ${c.market_cap/1e9:,.2f}B")
        if c.pe_ratio:
            lines.append(f"  P/E Ratio:                {c.pe_ratio:.1f}x")
        if c.price_to_sales:
            lines.append(f"  Price/Sales:              {c.price_to_sales:.1f}x")
        if c.revenue_growth is not None:
            lines.append(f"  Revenue Growth:           {c.revenue_growth:.1%}")
        if c.eps_growth is not None:
            lines.append(f"  EPS Growth:               {c.eps_growth:.1%}")
        if c.gross_margin is not None:
            lines.append(f"  Gross Margin:             {c.gross_margin:.1%}")
        if c.operating_margin is not None:
            lines.append(f"  Operating Margin:         {c.operating_margin:.1%}")
        lines.append("")
        
        # Momentum
        if c.one_year_return is not None:
            lines.append("PRICE MOMENTUM:")
            lines.append("-" * 60)
            if c.one_month_return is not None:
                lines.append(f"  1-Month Return:           {c.one_month_return:>6.1%}")
            if c.three_month_return is not None:
                lines.append(f"  3-Month Return:           {c.three_month_return:>6.1%}")
            if c.six_month_return is not None:
                lines.append(f"  6-Month Return:           {c.six_month_return:>6.1%}")
            if c.one_year_return is not None:
                lines.append(f"  1-Year Return:            {c.one_year_return:>6.1%}")
            lines.append("")
        
        # Strengths
        if s.revenue_growth > 10 or s.earnings_fcf > 10 or s.competitive_advantage > 7:
            lines.append("MAJOR STRENGTHS:")
            lines.append("-" * 60)
            if s.revenue_growth > 10:
                lines.append(f"  • Strong revenue growth ({c.revenue_growth:.1%})")
            if s.earnings_fcf > 10:
                lines.append(f"  • Solid earnings and cash flow growth")
            if s.industry_growth > 12:
                lines.append(f"  • Operating in high-growth industry ({c.industry_growth:.1%})")
            if s.competitive_advantage > 7:
                moats = ", ".join(c.competitive_advantage) if c.competitive_advantage else "competitive advantages"
                lines.append(f"  • Clear competitive moat: {moats}")
            if s.balance_sheet > 7:
                lines.append(f"  • Strong balance sheet")
            lines.append("")
        
        # Risks
        if s.valuation < 5 or s.earnings_fcf < 5 or c.risk_factors:
            lines.append("MAJOR RISKS:")
            lines.append("-" * 60)
            if s.valuation < 5:
                if c.pe_ratio:
                    lines.append(f"  • High valuation (P/E: {c.pe_ratio:.1f}x)")
                else:
                    lines.append(f"  • Valuation concerns")
            if s.earnings_fcf < 5:
                lines.append(f"  • Weak earnings or cash flow")
            if c.risk_factors:
                for risk in c.risk_factors[:3]:  # Top 3 risks
                    lines.append(f"  • {risk}")
            lines.append("")
        
        # Catalysts
        if c.catalysts:
            lines.append("KEY CATALYSTS:")
            lines.append("-" * 60)
            for catalyst in c.catalysts:
                lines.append(f"  • {catalyst}")
            lines.append("")
        
        # Classification rationale
        lines.append("INVESTMENT CLASSIFICATION:")
        lines.append("-" * 60)
        if s.classification == "BUY":
            lines.append("  Strong buy opportunity. Company demonstrates strong fundamentals,")
            lines.append("  attractive valuation, competitive advantages, and positive catalysts.")
        elif s.classification == "WATCH":
            lines.append("  Good company to monitor. Strong fundamentals but either higher")
            lines.append("  valuation or slightly weaker catalysts than BUY candidates.")
        elif s.classification == "INTERESTING":
            lines.append("  Interesting opportunity that warrants deeper research. Mix of")
            lines.append("  positive and concerning factors.")
        elif s.classification == "RESEARCH":
            lines.append("  Requires additional research before investment consideration.")
            lines.append("  Significant concerns offset some positive attributes.")
        else:  # REJECT
            lines.append("  Does not meet investment criteria. Multiple concerns outweigh")
            lines.append("  any positive factors.")
        lines.append("")
        
        lines.append("=" * 100)
        return "\n".join(lines)
    
    def generate_ranking_report(self, ranked_stocks: List[RankedStock], top_n: int = 10) -> str:
        """
        Generate a ranking report for multiple stocks.
        
        Args:
            ranked_stocks: List of RankedStock objects
            top_n: Number of top stocks to display
            
        Returns:
            Formatted ranking report
        """
        lines = []
        lines.append("=" * 130)
        lines.append(f"INVESTMENT RANKING REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 130)
        lines.append(f"Total Stocks Analyzed: {len(ranked_stocks)}")
        lines.append("")
        
        # Classification summary
        buy_count = len([r for r in ranked_stocks if r.score.classification == "BUY"])
        watch_count = len([r for r in ranked_stocks if r.score.classification == "WATCH"])
        interesting_count = len([r for r in ranked_stocks if r.score.classification == "INTERESTING"])
        research_count = len([r for r in ranked_stocks if r.score.classification == "RESEARCH"])
        reject_count = len([r for r in ranked_stocks if r.score.classification == "REJECT"])
        
        lines.append("CLASSIFICATION SUMMARY:")
        lines.append(f"  BUY:         {buy_count} ({buy_count/len(ranked_stocks)*100:.1f}%)")
        lines.append(f"  WATCH:       {watch_count} ({watch_count/len(ranked_stocks)*100:.1f}%)")
        lines.append(f"  INTERESTING: {interesting_count} ({interesting_count/len(ranked_stocks)*100:.1f}%)")
        lines.append(f"  RESEARCH:    {research_count} ({research_count/len(ranked_stocks)*100:.1f}%)")
        lines.append(f"  REJECT:      {reject_count} ({reject_count/len(ranked_stocks)*100:.1f}%)")
        lines.append("")
        
        # Top stocks
        lines.append("TOP STOCKS BY SCORE:")
        lines.append("-" * 130)
        lines.append(f"{'Rank':<5} {'Ticker':<8} {'Company':<30} {'Score':<8} {'Class':<12} "
                     f"{'Revenue':<8} {'Earnings':<8} {'Industry':<8} {'Valuation':<10} {'Moat':<6} {'Momentum':<9}")
        lines.append("-" * 130)
        
        for ranked_stock in ranked_stocks[:top_n]:
            s = ranked_stock.score
            lines.append(
                f"{ranked_stock.rank:<5} {s.ticker:<8} {s.company_name[:28]:<30} "
                f"{s.total_score:<8.1f} {s.classification:<12} "
                f"{s.revenue_growth:<8.1f} {s.earnings_fcf:<8.1f} {s.industry_growth:<8.1f} "
                f"{s.valuation:<10.1f} {s.competitive_advantage:<6.1f} {s.momentum:<9.1f}"
            )
        
        lines.append("-" * 130)
        lines.append("")
        lines.append("=" * 130)
        
        return "\n".join(lines)


def generate_stock_report(ranked_stock: RankedStock) -> str:
    """Generate report for a single stock."""
    generator = ReportGenerator()
    return generator.generate_stock_report(ranked_stock)


def generate_ranking_report(ranked_stocks: List[RankedStock], top_n: int = 10) -> str:
    """Generate ranking report for multiple stocks."""
    generator = ReportGenerator()
    return generator.generate_ranking_report(ranked_stocks, top_n)
