# Stock Graph App: Documentation

## Overview
The Stock Graph App is a Reflex-based web application that enables users to fetch, visualize, and interact with historical stock data for any ticker symbol (e.g., AAPL, MSFT). The app features a responsive UI, search functionality, selectable time ranges, and real-time market indicators.

---

## Python Modules Used
- **reflex**: The main web/UI framework for building the app.
- **yfinance**: For fetching real-time and historical stock market data from Yahoo Finance.
- **typing**: For type annotations (e.g., `List`, `TypedDict`).

### Standard Library
- **asyncio**: Used implicitly by Reflex for async event handling.

---

## App Structure & Key Files
- `stock_graph_app/stock_graph_app.py`: Main entry point, app and page registration.
- `stock_graph_app/components/stock_chart_display.py`: UI components for the stock chart, header, search bar, etc.
- `stock_graph_app/states/stock_state.py`: State management, data fetching, and business logic.

---

## How UDFs (User-Defined Functions) Are Used

### State & Events (`stock_state.py`)
- **UDFs as Reflex State Events**: Decorated with `@rx.event`, these async methods are triggered by UI events (form submissions, button clicks, etc.).
    - `fetch_stock_data`: Fetches company info and historical prices using yfinance, triggered by the search bar form.
    - `refresh_data`: Refreshes data for the current ticker.
    - `set_time_range`: Changes the time range and refetches historical data.
    - `on_load_fetch`: Fetches initial data when the page loads.
- **UDFs as Computed Properties**: Decorated with `@rx.var`, these are reactive properties used in the UI for display logic.
    - Examples: `logo_url`, `stock_ticker`, `company_name`, `exchange_info`, `current_price_display_val`, `market_cap_display_val`, `is_market_currently_active`.

### UI Components (`stock_chart_display.py`)
- Functions like `search_bar_component`, `stock_header_component`, `time_range_selector_component`, and `chart_component` define modular UI blocks.
- These components use state values and trigger state events (e.g., `on_submit=StockState.fetch_stock_data`).

---

## External Dependencies
- **reflex** (>=0.7.13a1): Main framework for UI and state management.
- **yfinance** (>=0.2.61): Fetches stock and company data from Yahoo Finance.
- **pandas**, **numpy**: Used by yfinance for data manipulation.
- **Other Reflex dependencies**: (see `requirements.txt`) such as FastAPI, websockets, etc.

---

## Data Flow Summary
1. **User enters a ticker symbol** in the search bar and submits.
2. **UI triggers** `StockState.fetch_stock_data`, which fetches data using yfinance.
3. **State updates** with company info and historical prices.
4. **UI components** (header, chart, etc.) reactively update to display the latest data.
5. **User can select time ranges**, triggering `set_time_range` and refetching data.

---

## Notable Features
- **Live Indicator**: Shows if the market is currently active.
- **Responsive Design**: Uses Tailwind-like classes for layout and style.
- **Error Handling**: User-friendly messages if data fetch fails or ticker is invalid.
- **Customizable Time Ranges**: 1D, 5D, 1M, 6M, 1Y, 5Y, MAX.

---

## Extending the App
- Add new UI components in `components/` and link them in the main page.
- Extend state logic in `states/stock_state.py` for more advanced analytics or data sources.

---

## Reference: requirements.txt
```
reflex>=0.7.13a1
yfinance>=0.2.61
```

Other dependencies are installed transitively by these packages.

---

For more details, see the source code in the respective modules.
