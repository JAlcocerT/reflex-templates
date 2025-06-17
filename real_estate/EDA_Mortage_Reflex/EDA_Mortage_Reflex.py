import reflex as rx
import reflex as rx
import pandas as pd


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


def composed():
    return rx.recharts.composed_chart(
        rx.recharts.area(
            data_key="uv", stroke="#8884d8", fill="#8884d8"
        ),
        rx.recharts.bar(
            data_key="amt", bar_size=20, fill="#413ea0"
        ),
        rx.recharts.line(
            data_key="pv",
            type_="monotone",
            stroke="#ff7300",
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
        rx.recharts.graphing_tooltip(),
        data=data,
        height=250,
        width="100%",
    )


data = [
    {"name": "Page A", "uv": 4000, "pv": 2400, "amt": 2400},
    {"name": "Page B", "uv": 3000, "pv": 1398, "amt": 2210},
    {"name": "Page C", "uv": 2000, "pv": 9800, "amt": 2290},
    {"name": "Page D", "uv": 2780, "pv": 3908, "amt": 2000},
    {"name": "Page E", "uv": 1890, "pv": 4800, "amt": 2181},
    {"name": "Page F", "uv": 2390, "pv": 3800, "amt": 2500},
    {"name": "Page G", "uv": 3490, "pv": 4300, "amt": 2100},
]
# Function to create a pie chart for total interest vs principal paid
def payment_pie_chart(interest_total, principal_total):
    data = [
        {"name": "Total Interest", "value": interest_total},
        {"name": "Total Principal", "value": principal_total}
    ]
    
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=data,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            label=True,
            outer_radius="80%"
        ),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        height=300,
        width="100%",
    )

class FormState(rx.State):
    principal: str = "560000.00"
    years: str = "25"
    annual_interest_rate: str = "7.31"
    property_value: str = "700000.00"
    rental_gross_income: str = "3500.00"
    property_growth_rate: str = "5.0"
    rental_growth_rate: str = "8.0"
    expenses_rate: str = "10.00"

    form_data: dict = {}
    output_text: str = ""
    amortization_schedule: pd.DataFrame = pd.DataFrame() # Add this for the DataFrame
    interest_total: float = 0
    principal_total: float = 0
    
    def set_principal(self, principal: str):
        self.principal = principal
        
    def set_years(self, years: str):
        self.years = years
        
    def set_annual_interest_rate(self, rate: str):
        self.annual_interest_rate = rate
        
    def set_property_value(self, value: str):
        self.property_value = value
        
    def set_rental_gross_income(self, income: str):
        self.rental_gross_income = income
        
    def set_property_growth_rate(self, rate: str):
        self.property_growth_rate = rate
        
    def set_rental_growth_rate(self, rate: str):
        self.rental_growth_rate = rate
        
    def set_expenses_rate(self, rate: str):
        self.expenses_rate = rate

    @rx.event
    def handle_submit(self):
        try:
            self.form_data = {
                "principal": float(self.principal),
                "years": int(self.years),
                "annual_interest_rate": float(self.annual_interest_rate),
                "property_value": float(self.property_value),
                "rental_gross_income": float(self.rental_gross_income),
                "property_growth_rate": float(self.property_growth_rate),
                "rental_growth_rate": float(self.rental_growth_rate),
                "expenses_rate": float(self.expenses_rate),
            }
            self.output_text = (
                f"Principal: {self.form_data['principal']}\n"
                f"Years: {self.form_data['years']}\n"
                f"Annual Interest Rate: {self.form_data['annual_interest_rate']}%\n"
                f"Property Value: {self.form_data['property_value']}\n"
                f"Rental Gross Income: {self.form_data['rental_gross_income']}\n"
                f"Property Growth Rate: {self.form_data['property_growth_rate']}%\n"
                f"Rental Growth Rate: {self.form_data['rental_growth_rate']}%\n"
                f"Expenses Rate: {self.form_data['expenses_rate']}%\n"
            )

            # Calculate amortization schedule:
            self.amortization_schedule = french_amortization(
                self.form_data["principal"],
                self.form_data["years"],
                self.form_data["annual_interest_rate"] / 100,  # Convert percentage to decimal
            )
            
            # Calculate total interest and principal paid
            if not self.amortization_schedule.empty:
                self.interest_total = round(self.amortization_schedule['Interest'].sum(), 2)
                self.principal_total = round(self.form_data["principal"], 2)  # Original principal amount

        except ValueError:
            self.output_text = "Invalid input. Please enter numbers."

        except Exception as e: # Catch any other exceptions during calculation
            self.output_text = f"An error occurred during calculation: {e}"


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("Mortgage Calculator"),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("Principal"),
                        rx.input(
                            placeholder="Loan amount",
                            value=FormState.principal,
                            on_change=FormState.set_principal,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Years"),
                        rx.input(
                            placeholder="Loan term in years",
                            value=FormState.years,
                            on_change=FormState.set_years,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Annual Interest Rate (%)"),
                        rx.input(
                            placeholder="Annual interest rate",
                            value=FormState.annual_interest_rate,
                            on_change=FormState.set_annual_interest_rate,
                        ),
                    ),
                    spacing="4",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("Property Value"),
                        rx.input(
                            placeholder="Property value",
                            value=FormState.property_value,
                            on_change=FormState.set_property_value,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Rental Gross Income"),
                        rx.input(
                            placeholder="Monthly rental income",
                            value=FormState.rental_gross_income,
                            on_change=FormState.set_rental_gross_income,
                        ),
                    ),
                    spacing="4",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("Property Growth Rate (%)"),
                        rx.input(
                            placeholder="Annual property growth rate",
                            value=FormState.property_growth_rate,
                            on_change=FormState.set_property_growth_rate,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Rental Growth Rate (%)"),
                        rx.input(
                            placeholder="Annual rental growth rate",
                            value=FormState.rental_growth_rate,
                            on_change=FormState.set_rental_growth_rate,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Expenses Rate (%)"),
                        rx.input(
                            placeholder="Expenses as % of rental income",
                            value=FormState.expenses_rate,
                            on_change=FormState.set_expenses_rate,
                        ),
                    ),
                    spacing="4",
                ),
                rx.center(
                    rx.button("Calculate", on_click=FormState.handle_submit),
                ),
                width="100%",
                spacing="4",
            ),
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.output_text),

        # Display pie chart for total interest vs principal paid
        rx.cond(
            FormState.amortization_schedule.empty,
            rx.text("Interest vs Principal chart will appear here after calculation."),
            rx.center(
                rx.vstack(
                    rx.heading("Total Interest vs Principal Paid", size="3"),
                    payment_pie_chart(FormState.interest_total, FormState.principal_total),
                    width="80%",
                )
            ),
        ),
        
        # Display amortization schedule if available
        rx.cond(
            FormState.amortization_schedule.empty,  # The Var directly!
            rx.text("Amortization schedule will be shown here after calculation."),  # If true (empty)
            rx.data_table(  # If false (not empty)
                data=FormState.amortization_schedule,
                pagination=True,
                search=True,
                sort=True,
            ),
        ),
        # composed()
    )

app = rx.App()
app.add_page(index)