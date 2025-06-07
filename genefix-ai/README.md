# Project: GeneFix AI

GeneFix AI is a research-level platform for genome mutation detection and correction using deep learning and CRISPR simulation.

## Features
- Modular deep learning models for mutation detection (CNN+LSTM) and correction (Transformer)
- CRISPR guide RNA design and Cas9 interface simulation
- Data pipeline for sequence cleaning and genome parsing
- REST API (FastAPI) for mutation detection, correction, and guide design
- Scripts for training, inference, and simulation
- Extensible utilities for logging and config loading
- Unit and integration tests

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn api.main:app --reload
   ```
3. Run tests:
   ```bash
   pytest tests
   ```

## Project Structure
- `app/` - Core logic (models, CRISPR, data pipeline, utils)
- `api/` - FastAPI REST API
- `scripts/` - Training, inference, and simulation scripts
- `tests/` - Unit and integration tests
- `configs/` - Config files (YAML/JSON)
- `data/` - Datasets (not tracked in Git)
- `docs/` - Documentation
- `notebooks/` - Jupyter notebooks for research

## License
See `LICENSE` file.
