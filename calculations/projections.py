from calculations.savings import project_savings
from calculations.loans import amortisation_schedule
from calculations.goals import will_reach_goal, required_monthly_contribution


def run_full_simulation(user_data, months=60):
    """
    Takes the dictionary of user inputs (from session_state) and
    returns a full results package: savings projection, loan schedule
    (if applicable), and goal progress (if applicable).
    """
    results = {}

    # Always run savings projection
    results["savings_projection"] = project_savings(
        starting_balance=user_data["current_savings"],
        monthly_contribution=user_data["monthly_savings"],
        annual_rate=user_data["savings_rate"],
        months=months
    )

    # Only run loan calculations if the user has a loan
    if user_data.get("has_loan"):
        results["loan_schedule"] = amortisation_schedule(
            principal=user_data["loan_amount"],
            annual_rate=user_data["loan_rate"],
            term_years=user_data["loan_term_years"]
        )
        total_paid = sum(m["payment"] for m in results["loan_schedule"])
        total_interest = sum(m["interest_portion"] for m in results["loan_schedule"])
        results["loan_summary"] = {
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2)
        }

    # Only run goal calculations if the user has a goal
    if user_data.get("has_goal"):
        goal_months = user_data["goal_years"] * 12
        results["goal_status"] = will_reach_goal(
            goal_amount=user_data["goal_amount"],
            current_savings=user_data["current_savings"],
            monthly_contribution=user_data["monthly_savings"],
            annual_rate=user_data["savings_rate"],
            months=goal_months
        )
        results["required_monthly_for_goal"] = required_monthly_contribution(
            goal_amount=user_data["goal_amount"],
            current_savings=user_data["current_savings"],
            annual_rate=user_data["savings_rate"],
            months=goal_months
        )

    return results