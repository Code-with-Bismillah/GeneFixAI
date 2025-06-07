# GeneFix AI Architecture

GeneFix AI is a modular platform for genome mutation detection and correction, combining deep learning and CRISPR simulation. Below is an overview of the system architecture and its main components.

## 1. Application Structure

- **app/**: Core logic, including models, CRISPR, data pipeline, and utilities.
- **api/**: FastAPI REST API for serving model predictions and CRISPR tools.
- **scripts/**: Training, inference, and simulation scripts.
- **notebooks/**: Jupyter notebooks for research and analysis.
- **configs/**: Configuration files for models, CRISPR, and logging.
- **data/**: Raw, processed, and mock datasets.
- **tests/**: Unit and integration tests.
- **docs/**: Documentation.

## 2. Core Components

### Models
- **MutationDetectionModel**: CNN+LSTM for mutation detection in DNA sequences.
- **CorrectionTransformer**: Transformer-based model for mutation correction.

### Data Pipeline
- **SequenceCleaner**: Preprocesses and one-hot encodes DNA sequences.
- **GenomeParser**: Placeholder for genome file parsing logic.

### CRISPR
- **GuideRNA**: Designs guide RNAs for CRISPR editing.
- **Cas9Interface**: Simulates Cas9 cutting (placeholder).

### Utilities
- **ConfigLoader**: Loads YAML/JSON config files.
- **Logger**: Standardized logging utility.

## 3. API Endpoints

- `/mutation_detection/detect`: Detect mutations in a DNA sequence.
- `/mutation_correction/correct`: Suggest corrections for detected mutations.
- `/design_guides`: Design CRISPR guide RNAs for a target sequence.

## 4. Data Flow

1. **Input**: User provides a DNA sequence (via API, script, or notebook).
2. **Preprocessing**: SequenceCleaner cleans and encodes the sequence.
3. **Detection**: MutationDetectionModel predicts mutation locations.
4. **Correction**: CorrectionTransformer suggests corrections (optional).
5. **CRISPR**: GuideRNA designs guides for genome editing.
6. **Output**: Results returned via API or script.

## 5. Extensibility
- Add new models in `app/models/`.
- Extend data pipeline in `app/data_pipeline/`.
- Add new API endpoints in `api/routes/`.
- Add new scripts or notebooks for research.

## 6. Deployment
- Run locally with Uvicorn or deploy in Docker.
- All dependencies are listed in `requirements.txt`.

---

For more details, see the README or individual module docstrings.
