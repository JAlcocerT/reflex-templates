# EDA_Mortage_Reflex: Mortgage Analysis Web Application

## Overview
EDA_Mortage_Reflex is a web application built with the Reflex framework that provides tools for mortgage analysis and visualization. The application allows users to input mortgage parameters and visualize amortization schedules, cash flows, and property investment metrics.

## Key Features
- **French Amortization Schedule Calculation**: Calculate detailed monthly payment breakdowns using the French amortization method
- **Interactive Data Visualization**: View mortgage data through interactive charts and graphs
- **Investment Analysis**: Analyze property investments with metrics like net asset value and cash flow
- **Customizable Parameters**: Adjust mortgage terms, interest rates, property values, and rental income

## Project Structure

### Main Components
- **EDA_Mortage_Reflex.py**: The main application file containing the web interface and form handling
- **UDF.py**: Utility functions for calculations and data processing
- **mortage_plots.py**: Functions for generating visualizations and plots
- **mortage_v6a_ref.py**: Reference implementation file
- **rxconfig.py**: Reflex configuration file

### Core Functionality

#### Mortgage Calculation
The application implements the French amortization method to calculate monthly payments, interest, principal, and remaining balance over the loan term. The core calculation is handled by the `french_amortization()` function, which:
- Converts annual interest rates to monthly rates
- Calculates fixed monthly payments
- Generates a complete amortization schedule showing:
  - Monthly interest payments
  - Principal payments
  - Total payments
  - Remaining balance

#### Investment Analysis
The application enhances mortgage analysis with investment metrics through the `enhance_amortization_schedule_df()` function, which adds:
- Property value projections based on growth rates
- Rental income calculations with growth projections
- Net asset value calculations
- Pocket cash flow analysis

#### Data Visualization
The application provides several visualization tools:
- **Principal vs Interest Plot**: Shows the breakdown between principal and interest payments over time
- **Cash Flow Plot**: Visualizes monthly and cumulative cash flows
- **Loan Data Plot**: Displays asset values, net asset values, and remaining principal/interest

## User Interface
The web interface features:
- Input form for mortgage and property parameters
- Results section displaying calculation outputs
- Interactive data table showing the amortization schedule
- Visual charts and graphs for data analysis

## Technologies Used
- **Reflex**: Web framework for building reactive applications
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy Financial**: Financial calculations

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `reflex run`
3. Access the web interface in your browser

## Use Cases
- Mortgage planning and comparison
- Real estate investment analysis
- Cash flow projections for rental properties
- Long-term financial planning for property ownership
