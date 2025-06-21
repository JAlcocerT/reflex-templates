# Stock Graph App

Tested:

```sh
#pip install reflex-ag-grid
#uv pip install reflex-ag-grid
```

* https://reflex.dev/docs/library/tables-and-data-grids/ag-grid/ Which is deprecated and **not working**
* https://reflex.dev/docs/library/tables-and-data-grids/table/ **Working**
* https://reflex.dev/docs/library/tables-and-data-grids/data-table/ **Working**

## Running with `uv` (uvicorn + pip replacement)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and runner. If you don't have it installed, get it with:

```bash
pip install uv
#uv pip install python-dotenv
```

Then, to install dependencies and run the app:

```bash
cd ./stock_graph_app
uv venv
uv pip install -r requirements.txt
uv run reflex run
#uv run reflex run --backend-port 8001 --frontend-port 3000
```

---

## Running with Python venv

1. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the app:**

    ```bash
    python -m reflex run
    ```

---
