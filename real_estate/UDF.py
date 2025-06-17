import pandas as pd
import plotly.express as px
import streamlit as st

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

import numpy_financial as npf



def generate_principal_vs_interest_plot(amortization_schedule):
    """
    Generates a DataFrame for the loan period showing how much principal is returned 
    and how much interests on the mortage
    
    Parameters:
    - amortization_schedule: The dataframe with the mortage info.
    """
    fig = px.bar(
        amortization_schedule,
        x='Month',
        y=['Interest', 'Principal'],
        barmode='group',
        labels={'value': 'Amount', 'variable': 'Component'},
        title='Principal vs. Interest Payment Over Time'
    )
    # Show the figure
    #fig.show()
    #st.plotly_chart(fig)

    # Create the ratio column
    amortization_schedule['I2P'] = 100*amortization_schedule['Interest'] / (amortization_schedule['Interest'] + amortization_schedule['Principal'])

    # Add the ratio line with a secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=amortization_schedule['Month'],
            y=amortization_schedule['I2P'],
            mode='lines',
            name='Interest to Principal Ratio (%)',
            line=dict(color='red', width=2),
            yaxis='y2'  # Secondary y-axis
        )
    )

    # Update layout to add secondary y-axis
    fig.update_layout(
        yaxis2=dict(
            title='Interest Ratio (%)',
            overlaying='y',
            side='right',
            range=[0, 100]  # The ratio will always be between 0 and 1
        )
    )

    # Show the plot
    st.plotly_chart(fig)
    #return(fig)


# Function to calculate French amortization schedule
def french_amortization(principal, years, annual_interest_rate):
    # Convert annual interest rate to monthly
    monthly_interest_rate = annual_interest_rate / 12
    # Total number of payments (months)
    total_payments = years * 12
    
    # Calculate fixed monthly payment using the French amortization formula
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    
    # Prepare the amortization schedule
    amortization_schedule = []
    balance = principal
    
    for month in range(1, total_payments + 1):
        # Calculate the interest for this month
        interest_payment = balance * monthly_interest_rate
        # Calculate the principal for this month
        principal_payment = monthly_payment - interest_payment
        # Update the remaining balance
        balance -= principal_payment
        # Calculate the total payment (interest + principal)
        total_payment = interest_payment + principal_payment
        
        # Store the month, interest payment, principal payment, total payment, and remaining balance
        amortization_schedule.append({
            'Month': month,
            'Interest': round(interest_payment, 2),
            'Principal': round(principal_payment, 2),
            'Total Payment': round(total_payment, 2),  # Added the total payment column
            'Remaining Balance': round(balance, 2)
        })
    
    # Convert to a pandas DataFrame
    return pd.DataFrame(amortization_schedule)


import pandas as pd

def enhance_amortization_schedule_df(amortization_schedule, initial_contribution, 
                                        property_growth_rate, rental_income_value, rental_growth_rate, principal):
    """
    Enhances the amortization schedule with property value, rental income, 
    net assets, pocket cash flow, and interest/principal ratio.

    Parameters:
        amortization_schedule (pd.DataFrame): The amortization schedule DataFrame.
        initial_contribution (float): Initial contribution amount.
        property_growth_rate (float): Annual property growth rate.
        rental_income_value (float): Initial rental income.
        rental_growth_rate (float): Annual rental income growth rate.
        principal (float): Initial mortgage principal.

    Returns:
        pd.DataFrame: The enhanced amortization schedule.
    """

    amortization_schedule['Property Value'] = 0.0
    amortization_schedule['Rental Income'] = 0.0
    amortization_schedule['Net Assets'] = 0.0
    amortization_schedule['Pocket CF'] = 0.0
    #amortization_schedule['Interest/Principal Ratio'] = 0.0  # New column

    current_property_value = principal
    accumulated_rent = 0

    for index, row in amortization_schedule.iterrows():
        # Property Value
        current_property_value *= (1 + property_growth_rate / 12)
        amortization_schedule.loc[index, 'Property Value'] = current_property_value

        # Rental Income
        rental_income_value *= (1 + rental_growth_rate / 12)
        amortization_schedule.loc[index, 'Rental Income'] = rental_income_value

        # Net Assets
        remaining_mortgage = principal - row['Principal']
        accumulated_rent += rental_income_value
        net_asset = current_property_value - remaining_mortgage + accumulated_rent
        amortization_schedule.loc[index, 'Net Assets'] = net_asset

        # Pocket CF
        pocket_cf_value = rental_income_value - row['Total Payment']
        if index == 0:  # Add initial contribution only in the first month
            pocket_cf_value += -initial_contribution
        amortization_schedule.loc[index, 'Pocket CF'] = pocket_cf_value

        # # Interest/Principal Ratio (New Calculation)
        # if row['Principal'] != 0:  # Avoid division by zero
        #     interest_principal_ratio = 100* row['Interest'] / row['Principal']
        # else:
        #     interest_principal_ratio = 0  # Or some other appropriate value like NaN
        # amortization_schedule.loc[index, 'Interest/Principal Ratio'] = interest_principal_ratio

    return amortization_schedule

# def enhance_amortization_schedule_df(amortization_schedule, initial_contribution, property_growth_rate, rental_growth_rate):

# def enhance_amortization_schedule_df(amortization_schedule, initial_contribution, 
#                                         property_growth_rate, rental_income_value, rental_growth_rate, principal):
#     """
#     This function calculates the net assets and pocket cash flow based on the given amortization schedule.

#     Parameters:
#     amortization_schedule (pd.DataFrame): The amortization schedule DataFrame.
#     initial_contribution (float): The initial contribution amount in the first month.
#     property_growth_rate (float): The annual property growth rate.
#     rental_growth_rate (float): The annual rental income growth rate.
#     principal (float): The initial mortgage principal.

#     Returns:
#     pd.DataFrame: The amortization schedule with new columns 'Net Assets', 'Pocket CF', 
#                   'Rental Income', and 'Moni' added.
#     """
#     # Initialize required lists to store results
#     net_assets = []
#     pocket_cf = []
#     rental_income_history = []
    
#     current_property_value = principal  # Assuming property value starts at principal
#     #rental_income_value = initial_rent #principal * 0.01  # Assuming initial rental income is 1% of the property value
#     accumulated_rent = 0

#     # Loop over the amortization schedule to calculate the net assets and pocket cash flow
#     for index, row in amortization_schedule.iterrows():
#         # Calculate property value growth
#         current_property_value *= (1 + property_growth_rate / 12)  # Monthly growth rate
        
#         # Update rental income with growth
#         rental_income_value *= (1 + rental_growth_rate / 12)  # Monthly rental income growth
        
#         print(rental_income_value)
#         # Store the rental income value for this month
#         rental_income_history.append(rental_income_value)
        
#         # Calculate outstanding mortgage balance after this payment
#         remaining_mortgage = principal - row['Principal']
        
#         # Calculate accumulated rental income (cumulative)
#         accumulated_rent += rental_income_value
        
#         # Net assets is property value minus remaining mortgage + accumulated rental income
#         net_asset = current_property_value - remaining_mortgage + accumulated_rent
#         net_assets.append(net_asset)
        
#         # Pocket CF is the difference between rental income and total payment
#         pocket_cf_value = rental_income_value - row['Total Payment']
        
#         # Add initial contribution in the first month
#         if index == 0:
#             pocket_cf_value += initial_contribution
            
#         pocket_cf.append(pocket_cf_value)

#     # Add the new columns to the amortization schedule
#     #amortization_schedule['Net Assets'] = net_assets
#     amortization_schedule['Pocket CF'] = pocket_cf
#     amortization_schedule['Rental Income'] = rental_income_history

#     # Calculate 'Moni' as the difference between Pocket CF and Rental Income
#     amortization_schedule['Moni'] = amortization_schedule['Pocket CF'] - amortization_schedule['Rental Income']
    
#     return amortization_schedule