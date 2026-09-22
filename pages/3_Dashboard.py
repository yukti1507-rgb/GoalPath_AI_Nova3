import streamlit as st

from calculations.projections import run_full_simulation


st.set_page_config(
    page_title="Your Dashboard",
    page_icon="📊", 
    layout="wide"
    )

st.title("Your Financial Future")

if "income" not in st.session_state:
    st.warning("Please fill in your details first.")
    st.stop()

results = run_full_simulation(st.session_state, months=60)

st.line_chart([m["balance"] for m in results["savings_projection"]])

if "loan_summary" in results:
    st.metric("Total interest on loan", f"Rs {results['loan_summary']['total_interest']}")

if "goal_status" in results:
    if results["goal_status"]["reached"]:
        st.success(f"🎯 Goal reached in month {results['goal_status']['month_reached']}!")
    else:
        st.warning(f"⚠️ At this rate, you won't reach your goal. You'd need Rs {results['required_monthly_for_goal']}/month instead.")