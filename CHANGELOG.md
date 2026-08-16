# Changelog

All notable changes to the Investment Model project will be documented in this file.

## [1.0.0] - 2026-08-16

### Added
- Initial project structure with modular architecture
- Core scoring engine with 10 category evaluation system
- Data loading and validation modules
- Fundamental analysis engine (revenue, earnings, industry)
- Valuation analysis module
- Momentum analysis module
- Catalyst identification system
- Risk analysis engine
- Ranking and reporting modules
- Historical prediction tracking
- Benchmarking framework
- Comprehensive test suite
- Command-line interface
- Configuration management
- Mock/demo data support
- Project documentation

### Features
- Scoring range: 0-100 with classifications (BUY, WATCH, INTERESTING, RESEARCH, REJECT)
- Stock universe: 11 initial technology stocks
- Category weights totaling 100 points
- Risk-adjusted evaluation system
- Historical prediction storage
- Data source tracking
- Missing data handling

### Tests
- Score validation tests
- Weight validation tests
- Share-price independence verification
- Classification accuracy tests
- Missing data handling tests
- Ranking determinism tests
- Historical tracking immutability tests

### Documentation
- README.md with installation and usage
- PROJECT_SPEC.md with complete specifications
- CHANGELOG.md (this file)
- Inline code documentation with docstrings
- Type hints throughout codebase

### Known Limitations
- Real market data requires yfinance API or manual data entry
- Historical tracking begins August 14, 2026
- ML models not yet implemented
- Limited to single user per repository

---

## Future Releases

### [1.1.0] - Planned
- Enhanced data provider integrations
- Additional stock universe expansion
- Advanced momentum indicators
- Machine learning model preparation

### [2.0.0] - Planned
- Machine learning-based scoring
- Sentiment analysis integration
- Advanced benchmarking
- Portfolio optimization

---

## Versioning Strategy

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for methodology changes
- MINOR version for new features
- PATCH version for bug fixes

Historical scores are preserved when version updates occur.
