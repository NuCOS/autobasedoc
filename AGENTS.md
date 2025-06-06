# Repo Guidelines

This repository requires a basic workflow for setting up the environment and running tests.

1. Use **Python ≥3.7**.
2. Install dependencies with `pip install -r requirements.txt`.
3. Install the project in editable mode using `pip install -e .`.
4. Install the additional test dependencies with `pip install pytest faker numpy`.
5. Set the environment variable `MPLBACKEND=Agg` before running tests.
6. Execute tests using `pytest -q`.
