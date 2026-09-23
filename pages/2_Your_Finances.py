import streamlit as st
from main import profile_icon

st.set_page_config(
    page_title = "Your Finances",
    page_icon = "💰",
    layout = "wide"
    )

col1, col2= st.columns([1,3])

with col1:
    st.title("Tell us about your finances")

with col2:
    profile_icon()

st.caption("Answer what applies to you — you can skip sections that don't.")

#input necessary for all users
# st.subheader("💵 Income")
# income = st.number_input("What's your monthly income?", min_value=0.0, step=100.0)

st.divider()

#expenses broken down by category so "what if" scenarios have something to adjust
st.subheader("🧾 Monthly Expenses")
st.caption("Enter what applies to you. Leave a category at 0 if it doesn't apply — every monthly expense should be captured here.")

st.markdown("**Food & groceries**")
food_type = st.selectbox(
    "Is this spending a need or a want?",
    ["Need (e.g. groceries, home cooking)", "Want (e.g. takeout, snacks, treats)"],
    key="food_type"
)
food = st.number_input("How much do you spend on this per month?", min_value=0.0, step=50.0, key="food_amount")
food_is_need = food_type.startswith("Need")

transport = st.number_input("Transport (fuel, bus, taxi, car payments)", min_value=0.0, step=50.0)
utilities = st.number_input("Utilities & bills (electricity, water, phone, internet)", min_value=0.0, step=50.0)
other = st.number_input(
    "Other expenses",
    min_value=0.0,
    step=50.0,
    help="Anything not covered above — e.g. insurance, clothing, gifts, medical, childcare, pet costs."
)

expenses = rent + food + transport + utilities + other

col_e1, col_e2 = st.columns(2)
with col_e1:
    st.metric("Total monthly expenses", f"{expenses:,.0f}")
with col_e2:
    available = income - expenses
    st.metric("Available after expenses", f"{available:,.0f}")

if income > 0 and expenses > income:
    st.warning("⚠️ Your expenses currently exceed your income — there's nothing left over to save.")

st.divider()

#how much the user is willing to save each month
st.subheader("🏦 Savings")
current_savings = st.number_input("How much do you currently have saved?", min_value=0.0, step=100.0)
monthly_savings = st.number_input("How much would you like to save each month?", min_value=0.0, step=100.0)
savings_rate = st.slider("Expected annual interest rate on your savings (%)", 0.0, 10.0, 3.0, step=0.1,
                          help="The average return your savings account or investment earns per year.")

if monthly_savings > available:
    st.warning(f"⚠️ You're planning to save {monthly_savings:,.0f} but only have {available:,.0f} available after expenses.")

st.divider()

#if the user has to repay a loan
st.subheader("💳 Loan")
has_loan = st.radio("Do you have a loan you're currently repaying?", ["No", "Yes"], horizontal=True)

loan_amount = 0.0
loan_rate = 0.0
loan_term_years = 0

if has_loan == "Yes":
    loan_amount = st.number_input("How much did you borrow?", min_value=0.0, step=500.0)
    loan_rate = st.slider("What's the interest rate (%)?", 0.0, 20.0, 9.0, step=0.1)
    loan_term_years = st.number_input("Over how many years are you repaying it?", min_value=1, max_value=30, step=1)

st.divider()

#goal to be achieved by user by a specific time
st.subheader("🎯 Savings Goal")
has_goal = st.radio("Are you saving toward a specific goal?", ["No", "Yes"], horizontal=True)

goal_name = ""
goal_amount = 0.0
goal_years = 0

if has_goal == "Yes":
    goal_name = st.text_input("What are you saving for? (e.g. Car, Emergency fund, Trip)")
    goal_amount = st.number_input("How much do you need?", min_value=0.0, step=500.0)
    goal_years = st.number_input("By when? (years from now)", min_value=1, max_value=30, step=1)

st.divider()

#saving session states
if st.button("Run my simulation", type="primary"):
    st.session_state["income"] = income

    st.session_state["rent"] = rent
    st.session_state["food"] = food
    st.session_state["transport"] = transport
    st.session_state["utilities"] = utilities
    st.session_state["discretionary"] = discretionary
    st.session_state["other"] = other
    st.session_state["expenses"] = expenses

    st.session_state["current_savings"] = current_savings
    st.session_state["monthly_savings"] = monthly_savings
    st.session_state["savings_rate"] = savings_rate

    st.session_state["has_loan"] = has_loan == "Yes"
    st.session_state["loan_amount"] = loan_amount
    st.session_state["loan_rate"] = loan_rate
    st.session_state["loan_term_years"] = loan_term_years

    st.session_state["has_goal"] = has_goal == "Yes"
    st.session_state["goal_name"] = goal_name
    st.session_state["goal_amount"] = goal_amount
    st.session_state["goal_years"] = goal_years

    st.success("Got it! Heading to Dashboard to see your projection.")
    st.switch_page("pages/3_Dashboard.py")
