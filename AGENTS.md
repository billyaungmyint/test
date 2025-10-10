# Repository Guidelines

## Project Structure & Module Organization
Core scripts sit at the repository root for now. `main.py` is the lightweight entry point used in quick smoke checks. `linear_regression.py` handles model training, plotting, and returns metrics; `clustering_comparison.py` benchmarks K-Means versus DBSCAN and saves comparison visuals. Tests mirror those modules: `test_linear_regression.py` and `test_clustering_comparison.py` validate outputs and clean up plots. Generated artifacts such as `regression_plot.png` and `clustering_comparison_plot.png` are created in the root; keep them out of version control.

## Build, Test, and Development Commands
Use Python 3.13+, preferably via the committed `.venv`. Install dependencies with `uv sync` (locks to `uv.lock`) or `python -m pip install -r requirements.txt` when uv is unavailable. Run the full test suite with `python -m unittest discover -s . -p "test_*.py"`; add `-v` while debugging. Module entry points can be exercised with `python linear_regression.py` and `python clustering_comparison.py` to regenerate plots and inspect console metrics.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indentation, `snake_case` for functions/modules, and CapWords for classes. Favor explicit imports and keep plotting side effects wrapped in functions that return computed values, as in the current modules. Include docstrings on new public functions and prefer f-strings for formatted output. Keep generated files confined to predictable names so tests can delete them cleanly.

## Testing Guidelines
Unit tests rely on the standard library `unittest`. Mirror new production modules with `test_<module>.py` files at the repository root until a `tests/` package is introduced. Assert both numerical tolerances and file system side effects (e.g., plot creation) and ensure tests clean up any generated artifacts in `tearDown` or `tearDownClass`. When adding randomized behavior, seed generators inside tests to keep runs deterministic.

## Commit & Pull Request Guidelines
Recent history shows concise, lower-case subject lines (e.g., `after uv init`). Keep commit messages imperative and under 60 characters when possible. Each PR should summarize the change set, list verification steps (tests run, plots inspected), and link any related issues. Attach fresh plot snippets when graphics change so reviewers can compare outputs.
