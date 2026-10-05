# ComfortSense Analytics

ComfortSense Analytics is a machine-learning project for estimating occupant comfort from sensor and study data.

## Project Structure

- `data/raw/`: Original local CSV files.
- `data/processed/`: Locally processed datasets.
- `notebooks/`: Machine-learning experiments and preprocessing work.
- `backend/`: FastAPI service and comfort-scoring algorithms.
- `frontend/`: Reserved for a future Flutter or React Native client.

## Local Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install backend dependencies:

   ```powershell
   pip install -r backend/requirements.txt
   ```

3. Start the API from the project root:

   ```powershell
   uvicorn backend.main:app --reload
   ```

The API is then available at `http://127.0.0.1:8000`, with interactive documentation at `/docs`.

## Data Handling

Raw and processed CSV files are intentionally excluded from Git. Keep local study data under `data/raw/` and `data/processed/`.
