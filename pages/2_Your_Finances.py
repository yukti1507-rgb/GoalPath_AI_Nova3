import streamlit as st


st.set_page_config(
    page_title = "Your Finances",
    page_icon = "💰",
    layout = "wide"
    )

st.title("Can I afford my financial goals?")

st.caption("Answer what applies to you — you can skip sections that don't.")

#input necessary for all users
st.subheader("💵 Income & Expenses")
income = st.number_input("What's your monthly income?", min_value=0.0, step=100.0)
expenses = st.number_input("Roughly how much do you spend per month on essentials (rent, food, transport, bills)?", min_value=0.0, step=100.0)

st.divider()

#how much the user is willing to save each month
st.subheader("🏦 Savings")
current_savings = st.number_input("How much do you currently have saved?", min_value=0.0, step=100.0)
monthly_savings = st.number_input("How much would you like to save each month?", min_value=0.0, step=100.0)
savings_rate = st.slider("Expected annual interest rate on your savings (%)", 0.0, 10.0, 3.0, step=0.1)

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