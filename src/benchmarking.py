"""
Benchmarking module for tracking model performance.
Compares against S&P 500, equal-weight portfolio, and simple strategies.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from src.ranking import RankedStock

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkMetrics:
    """Metrics for a benchmark."""
    
    name: str
    total_return: float  # e.g., 0.25 for 25%
    win_rate: float  # percentage of winning predictions
    average_win: float
    average_loss: float
    max_drawdown: float
    sharpe_ratio: Optional[float] = None
    
    def summary(self) -> str:
        """Generate summary string."""
        return (f"{self.name}: Return={self.total_return:.1%}, Win Rate={self.win_rate:.1%}, "
                f"Max DD={self.max_drawdown:.1%}")


class Benchmarking:
    """Track model performance against benchmarks."""
    
    def __init__(self):
        """Initialize benchmarking."""
        self.benchmarks: Dict[str, BenchmarkMetrics] = {}
    
    def calculate_portfolio_performance(self,
                                       ranked_stocks: List[RankedStock],
                                       start_date: datetime,
                                       end_date: datetime,
                                       equal_weight: bool = True) -> BenchmarkMetrics:
        """
        Calculate performance of candidate portfolio.
        
        Args:
            ranked_stocks: List of RankedStock objects
            start_date: Portfolio start date
            end_date: Portfolio end date
            equal_weight: If True, use equal weights; else use score-based weights
            
        Returns:
            BenchmarkMetrics for the portfolio
        """
        # This is a placeholder - real implementation would need actual price data
        metrics = BenchmarkMetrics(
            name="Equal-Weight Candidate Portfolio",
            total_return=0.15,  # 15% for demo
            win_rate=0.65,
            average_win=0.08,
            average_loss=-0.03,
            max_drawdown=-0.12,
            sharpe_ratio=1.2,
        )
        return metrics
    
    def get_sp500_performance(self, start_date: datetime, end_date: datetime) -> BenchmarkMetrics:
        """Get S&P 500 performance for period."""
        # This would fetch real data from market data provider
        metrics = BenchmarkMetrics(
            name="S&P 500",
            total_return=0.12,  # 12% for demo
            win_rate=0.60,
            average_win=0.06,
            average_loss=-0.03,
            max_drawdown=-0.15,
            sharpe_ratio=0.9,
        )
        return metrics
    
    def get_momentum_strategy_performance(self, start_date: datetime, end_date: datetime) -> BenchmarkMetrics:
        """Get simple momentum strategy performance."""
        metrics = BenchmarkMetrics(
            name="Simple Momentum Strategy",
            total_return=0.18,  # 18% for demo
            win_rate=0.58,
            average_win=0.09,
            average_loss=-0.04,
            max_drawdown=-0.20,
            sharpe_ratio=0.8,
        )
        return metrics
    
    def get_growth_strategy_performance(self, start_date: datetime, end_date: datetime) -> BenchmarkMetrics:
        """Get simple growth strategy performance."""
        metrics = BenchmarkMetrics(
            name="Simple High-Growth Strategy",
            total_return=0.22,  # 22% for demo
            win_rate=0.55,
            average_win=0.12,
            average_loss=-0.05,
            max_drawdown=-0.25,
            sharpe_ratio=0.7,
        )
        return metrics
    
    def compare_performance(self, ranked_stocks: List[RankedStock],
                          start_date: datetime,
                          end_date: datetime) -> Dict[str, BenchmarkMetrics]:
        """
        Compare model performance against multiple benchmarks.
        
        Args:
            ranked_stocks: List of ranked stocks
            start_date: Analysis start date
            end_date: Analysis end date
            
        Returns:
            Dictionary of benchmark metrics
        """
        self.benchmarks = {
            "candidate_portfolio": self.calculate_portfolio_performance(ranked_stocks, start_date, end_date),
            "sp500": self.get_sp500_performance(start_date, end_date),
            "momentum": self.get_momentum_strategy_performance(start_date, end_date),
            "growth": self.get_growth_strategy_performance(start_date, end_date),
        }
        
        return self.benchmarks
    
    def generate_benchmark_report(self) -> str:
        """Generate benchmark comparison report."""
        if not self.benchmarks:
            return "No benchmark data available. Run compare_performance() first."
        
        lines = []
        lines.append("=" * 100)
        lines.append("BENCHMARK PERFORMANCE COMPARISON")
        lines.append("=" * 100)
        lines.append("")
        
        # Sort by return
        sorted_benchmarks = sorted(self.benchmarks.items(), 
                                  key=lambda x: x[1].total_return, 
                                  reverse=True)
        
        lines.append(f"{'Strategy':<35} {'Return':<12} {'Win Rate':<12} {'Avg Win':<12} {'Avg Loss':<12} {'Max DD':<12}")
        lines.append("-" * 100)
        
        for name, metrics in sorted_benchmarks:
            lines.append(
                f"{name:<35} {metrics.total_return:>10.1%}  {metrics.win_rate:>10.1%}  "
                f"{metrics.average_win:>10.1%}  {metrics.average_loss:>10.1%}  {metrics.max_drawdown:>10.1%}"
            )
        
        lines.append("-" * 100)
        
        # Identify best performer
        best = sorted_benchmarks[0]
        lines.append(f"\nBest Performer: {best[0]} with {best[1].total_return:.1%} return")
        
        lines.append("")
        lines.append("=" * 100)
        
        return "\n".join(lines)


def benchmark_model(ranked_stocks: List[RankedStock],
                   start_date: datetime,
                   end_date: datetime) -> Dict[str, BenchmarkMetrics]:
    """Convenience function to benchmark model performance."""
    benchmarker = Benchmarking()
    return benchmarker.compare_performance(ranked_stocks, start_date, end_date)
