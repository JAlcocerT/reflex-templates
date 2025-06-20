



## Quickstart version


```sh
cd login_mailerlite

reflex init
#reflex run
reflex run --backend-port 8001 --frontend-port 3001
```

### 1. Using [uv](https://github.com/astral-sh/uv) (Recommended)

```bash
# Install uv if not already installed
pip install uv

# Install dependencies
uv venv
uv pip install -r requirements.txt

# Run the Streamlit app
streamlit run st_debt.py
```

### 2. Using Python venv

```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run st_debt.py
```

---
