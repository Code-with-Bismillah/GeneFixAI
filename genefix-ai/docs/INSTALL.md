# GeneFix AI Installation Guide

## 1. Clone the Repository
```bash
git clone <your-repo-url>
cd genefix-ai
```

## 2. Create and Activate a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## 4. (Optional) Install Jupyter for Notebooks
```bash
pip install notebook
```

## 5. (Optional) Install Additional System Packages
If you use Biopython or need to work with Excel files, you may need:
```bash
sudo apt-get update && sudo apt-get install -y libopenblas-dev liblapack-dev
```

## 6. Run the API Server
```bash
uvicorn api.main:app --reload
```

## 7. Run Tests
```bash
pytest tests
```

## 8. Open Notebooks
```bash
jupyter notebook notebooks/
```

---

- For Docker usage, see the Dockerfile and docker-compose.yml (if provided).
- For environment variables, see the .env file.
- For configuration, see the configs/ directory.
