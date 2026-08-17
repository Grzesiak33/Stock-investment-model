"""
Main entry point for the investment model.
Provides CLI interface and orchestrates the scoring pipeline.
"""

import logging
import argparse
import sys
from datetime import datetime
from typing import List, Optional

from src.config import TICKERS, MODEL_VERSION
from src.data_loader import DataLoader, CompanyData
from src.data_validation import validate_multiple
from src.scoring import score_multiple, ScoringEngine
from src.ranking import rank_stocks
from src.reporting import generate_stock_report, generate_ranking_report
from src.tracking import save_prediction, get_tracker
from src.benchmarking import benchmark_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_analysis(tickers: Optional[List[str]] = None, verbose: bool = False) -> None:
    """
    Run the complete investment analysis pipeline.
    
    Args:
        tickers: List of tickers to analyze. If None, use default universe.
        verbose: If True, print detailed information.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Starting Investment Model Analysis v{MODEL_VERSION}")
    logger.info("=" * 100)
    
    # Use provided tickers or defaults
    if tickers is None:
        tickers = TICKERS
    
    logger.info(f"Analyzing {len(tickers)} stocks: {', '.join(tickers)}")
    
    # Step 1: Load data
    logger.info("Step 1: Loading company data...")
    loader = DataLoader(use_mock_data=True)
    companies = loader.load_multiple(tickers)
    logger.info(f"  Loaded data for {len(companies)} companies")
    
    # Step 2: Validate data
    logger.info("Step 2: Validating data quality...")
    valid_companies, warnings = validate_multiple(companies)
    logger.info(f"  {len(valid_companies)} companies passed validation")
    if warnings:
        logger.warning(f"  {len(warnings)} validation warnings found")
        for w in warnings[:5]:  # Show first 5
            logger.warning(f"    {w}")
    
    # Step 3: Score companies
    logger.info("Step 3: Calculating investment scores...")
    scores = score_multiple(valid_companies)
    logger.info(f"  Scored {len(scores)} companies")
    
    # Step 4: Rank companies
    logger.info("Step 4: Ranking stocks...")
    ranked = rank_stocks(scores, valid_companies)
    logger.info(f"  Ranked {len(ranked)} companies")
    
    # Step 5: Generate reports
    logger.info("Step 5: Generating reports...")
    ranking_report = generate_ranking_report(ranked, top_n=len(ranked))
    print("\n" + ranking_report)
    
    # Step 6: Save predictions for top candidates
    logger.info("Step 6: Saving predictions for tracking...")
    for ranked_stock in ranked[:3]:  # Save top 3
        thesis = f"Score: {ranked_stock.score.total_score:.1f}/100. {ranked_stock.score.classification} recommendation."
        save_prediction(
            ticker=ranked_stock.score.ticker,
            company_name=ranked_stock.score.company_name,
            score=ranked_stock.score,
            ranking=ranked_stock.rank,
            price_at_prediction=ranked_stock.company.share_price or 0,
            thesis=thesis,
            catalysts=ranked_stock.company.catalysts or [],
            risks=ranked_stock.company.risk_factors or [],
        )
    
    # Step 7: Benchmark performance
    logger.info("Step 7: Benchmarking model performance...")
    benchmarks = benchmark_model(ranked, datetime(2026, 8, 14), datetime.now())
    
    logger.info("=" * 100)
    logger.info("Analysis Complete!")
    logger.info(f"  Top candidate: {ranked[0].score.ticker} ({ranked[0].score.total_score:.1f}/100)")


def analyze_ticker(ticker: str, verbose: bool = False) -> None:
    """
    Analyze a specific stock ticker.
    
    Args:
        ticker: Stock ticker to analyze
        verbose: If True, print detailed information
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info(f"Analyzing {ticker}...")
    logger.info("=" * 100)
    
    # Load data for single ticker
    loader = DataLoader(use_mock_data=True)
    company = loader.load_company(ticker)
    
    if not company:
        logger.error(f"Could not load data for {ticker}")
        return
    
    # Validate
    valid_companies, warnings = validate_multiple([company])
    if not valid_companies:
        logger.error(f"Data validation failed for {ticker}")
        for w in warnings:
            logger.error(f"  {w}")
        return
    
    # Score
    engine = ScoringEngine()
    score = engine.score_company(company)
    
    # Create ranked stock for reporting
    from src.ranking import RankedStock
    ranked_stock = RankedStock(rank=1, score=score, company=company)
    
    # Generate detailed report
    report = generate_stock_report(ranked_stock)
    print(report)
    
    logger.info("=" * 100)


def show_top_picks(n: int = 5, classification: Optional[str] = None) -> None:
    """
    Show top N stock picks.
    
    Args:
        n: Number of top picks to show
        classification: Filter by classification (BUY, WATCH, etc.)
    """
    logger.info(f"Getting top {n} picks...")
    
    loader = DataLoader(use_mock_data=True)
    companies = loader.load_multiple(TICKERS)
    
    valid_companies, _ = validate_multiple(companies)
    scores = score_multiple(valid_companies)
    ranked = rank_stocks(scores, valid_companies)
    
    # Filter by classification if specified
    if classification:
        ranked = [r for r in ranked if r.score.classification == classification]
    
    # Show top N
    print("\n" + generate_ranking_report(ranked, top_n=min(n, len(ranked))))


def show_accuracy() -> None:
    """Show historical prediction accuracy."""
    logger.info("Loading historical predictions...")
    
    tracker = get_tracker()
    metrics = tracker.get_accuracy_metrics()
    
    print("\n" + "=" * 80)
    print("HISTORICAL PREDICTION ACCURACY")
    print("=" * 80)
    print(f"Total predictions: {metrics['total_predictions']}")
    print(f"Completed predictions: {metrics['completed_predictions']}")
    
    if metrics['completed_predictions'] > 0:
        print(f"Correct thesis: {metrics['correct_thesis_count']} ({metrics['correct_thesis_count']/metrics['completed_predictions']:.1%})")
        print(f"Realized catalysts: {metrics['realized_catalysts_count']} ({metrics['realized_catalysts_count']/metrics['completed_predictions']:.1%})")
        print(f"Average return: {metrics['average_return']:.1%}")
        print(f"Average benchmark return: {metrics['average_benchmark_return']:.1%}")
        print(f"Win rate: {metrics['win_rate']:.1%}")
        print(f"Outperformance: {metrics['outperformance']:.1%}")
    
    print("=" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Investment Model - AI-Assisted Stock Scoring System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                    # Run full analysis
  python -m src.main --ticker NVDA      # Analyze specific stock
  python -m src.main --top 5 --buy      # Show top 5 BUY recommendations
  python -m src.main --accuracy         # Show prediction accuracy
        """
    )
    
    parser.add_argument(
        "--ticker",
        type=str,
        help="Analyze a specific stock ticker"
    )
    
    parser.add_argument(
        "--tickers",
        type=str,
        help="Comma-separated list of tickers to analyze"
    )
    
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Show top N picks (default: 5)"
    )
    
    parser.add_argument(
        "--buy",
        action="store_true",
        help="Filter for BUY classifications"
    )
    
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Filter for WATCH classifications"
    )
    
    parser.add_argument(
        "--accuracy",
        action="store_true",
        help="Show historical prediction accuracy"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose logging output"
    )
    
    args = parser.parse_args()
    
    try:
        if args.accuracy:
            show_accuracy()
        elif args.ticker:
            analyze_ticker(args.ticker, verbose=args.verbose)
        elif args.tickers:
            tickers = [t.strip().upper() for t in args.tickers.split(",")]
            run_analysis(tickers=tickers, verbose=args.verbose)
        elif args.buy or args.watch:
            classification = "BUY" if args.buy else "WATCH"
            show_top_picks(n=args.top, classification=classification)
        else:
            run_analysis(verbose=args.verbose)
    
    except KeyboardInterrupt:
        logger.info("\nAnalysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
