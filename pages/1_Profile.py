import streamlit as st
from app_model.db import get_connection
from app_model.users import update_avatar, update_email, is_username_available, update_user, get_user, reset_password, get_user_info, delete_one_user, is_email_available, get_user_theme, update_background, get_email, get_role
from app_model.display_avatar import display_avatar
from registration_and_login.hashing import is_valid_hash, generate_hash
from app_model.theme import apply_user_theme, THEME_OPTIONS
import os
import time
from registration_and_login.send_email_to_user import OTP_initialisation, OTP_verification

st.set_page_config(
    page_title="Profile",
    page_icon="👤", 
    layout="wide")


st.caption(
    "These are costs that stay roughly the same every month. "
    "Edit any field and hit Save — anything you leave untouched keeps its last saved value."
)

# default values: use whatever was saved before, or 0.0 if this is the first visit
defaults = {
    "fixed_rent": 0.0,
    "fixed_loan_repayment": 0.0,
    "fixed_insurance": 0.0,
    "fixed_utilities": 0.0,
    "fixed_subscriptions": 0.0,
    "fixed_school_childcare": 0.0,
    "fixed_transport": 0.0,
    "fixed_other": 0.0,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

st.subheader("🏠 Housing & Loans")
rent = st.number_input(
    "Rent / mortgage", min_value=0.0, step=50.0,
    value=st.session_state["fixed_rent"]
)
loan_repayment = st.number_input(
    "Loan repayments (car, student, personal)", min_value=0.0, step=50.0,
    value=st.session_state["fixed_loan_repayment"],
    help="If this overlaps with a loan you entered on the Finances page, only enter it once."
)

st.subheader("🛡️ Insurance & Utilities")
insurance = st.number_input(
    "Insurance (health, car, life)", min_value=0.0, step=25.0,
    value=st.session_state["fixed_insurance"]
)
utilities = st.number_input(
    "Utilities base plan (internet, phone, electricity standing charge)", min_value=0.0, step=25.0,
    value=st.session_state["fixed_utilities"]
)

st.subheader("📺 Recurring Commitments")
subscriptions = st.number_input(
    "Subscriptions (streaming, gym, software)", min_value=0.0, step=10.0,
    value=st.session_state["fixed_subscriptions"]
)
school_childcare = st.number_input(
    "School / childcare fees", min_value=0.0, step=50.0,
    value=st.session_state["fixed_school_childcare"]
)
transport = st.number_input(
    "Transport pass / lease (bus pass, car lease)", min_value=0.0, step=25.0,
    value=st.session_state["fixed_transport"]
)
other = st.number_input(
    "Other fixed costs", min_value=0.0, step=25.0,
    value=st.session_state["fixed_other"],
    help="Any other recurring cost that's the same amount every month."
)

submitted = st.button("Save changes", type="primary")

if submitted:
    st.session_state["fixed_rent"] = rent
    st.session_state["fixed_loan_repayment"] = loan_repayment
    st.session_state["fixed_insurance"] = insurance
    st.session_state["fixed_utilities"] = utilities
    st.session_state["fixed_subscriptions"] = subscriptions
    st.session_state["fixed_school_childcare"] = school_childcare
    st.session_state["fixed_transport"] = transport
    st.session_state["fixed_other"] = other
    st.success("Fixed expenses saved.")

# total always reflects the last saved values, not unsaved edits still in the form
total_fixed = sum(st.session_state[key] for key in defaults)
st.divider()
st.metric("Total fixed expenses (last saved)", f"{total_fixed:,.0f}")

if 'Logged_in' not in st.session_state:
    st.session_state['Logged_in'] = False

if not st.session_state['Logged_in']:
    st.warning("Please log in to access the dashboard.")

    if st.button("Go to Login Page"):
        st.session_state['Logged_in'] = False
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("You are Logged in!")

conn = get_connection()


st.title(f"𓆉°❀⋆.ೃ࿔*:･･ Welcome to your Profile, {st.session_state.get('username','User')}! 𓆉°❀⋆.ೃ࿔*:･ ")


st.divider()

Avatar_options =["🧑", "👩", "🐾", "🐼", "🐻", "🐺", "🐶", "🐸", "🐵", "🐴", "🐳", "🐲", "🐱", "🐰", "🐯", "🐯", "🐭", "🐬", "🐣", "🐧", "🐨", "☯", "🐪", "🐦", "🐢", "🐠", "🐞", "🐝", "🐜", "🐚", "🐒", "🐇", "🐆", "🐅", "🧜‍♀️", "🦄", "👸", "💫", "🌸", "❤️‍🔥", "❄️", "👑", "🦉", "🐕", "🐈‍⬛"]

username = st.session_state.get('username')
#theme
apply_user_theme(conn, username)

#displaying the avatar
chosen_avatar = display_avatar(conn, username)
st.subheader("Your avatar")

if chosen_avatar:
    st.markdown(f"# {chosen_avatar}")
else:
    st.markdown(f"# 👤")

#display the user's username and email before changing it
current_username, current_email = get_user_info(conn, username)

st.write(f"𓆉⋆｡˚⋆❀ 🐚🫧𓇼 ˖° **Username:** {current_username} 𓆉⋆｡˚⋆❀ 🐚🫧𓇼 ˖°")
st.write(f"𓆉⋆｡˚⋆❀ 🐚🫧𓇼 ˖° **Email:** {current_email} 𓆉⋆｡˚⋆❀ 🐚🫧𓇼 ˖°")

#choose your avatar
if chosen_avatar in Avatar_options:
    i = Avatar_options.index(chosen_avatar)
else:
    i = 0

selected_avatar = st.selectbox("Choose an avatar", Avatar_options, index = i)

if st.button("Save avatar"):
    update_avatar(conn, username, selected_avatar)
    st.success("°❀.ೃ࿔*°❀.ೃ࿔* Avatar successfully updated. °❀.ೃ࿔*°❀.ೃ࿔*")
    st.rerun()

#change username 
st.divider()
st.subheader("Change username")

with st.expander("Change Username"):
    with st.form("change_username_form"):
        new_username = st.text_input("Please enter your new username.")
        submit_username = st.form_submit_button("Update username")

        if submit_username:
            if not new_username:
                st.error("Please enter your new username.")
            elif new_username == username:
                st.error("This is already your username.")
                st.session_state["username_updated"] = False
            elif not is_username_available(conn, new_username):
                st.error("This username is taken. Please choose another username.")
                st.session_state["username_updated"] = False
            else:
                update_user(conn, new_username, username)
                st.session_state['username'] = new_username
                st.session_state["username_updated"] = True
                st.rerun()
    
    if st.session_state.get("username_updated"):
        st.success("𓂃🪶 Username updated! 𓂃🪶")
        st.session_state["username_updated"] = True
        time.sleep(2)
        st.rerun()

#change password using 2 step verification - asks for old password
st.divider()
st.subheader("Change password")

with st.expander("Change Password"):
    with st.form("change_password_form", clear_on_submit=False):
        current_password = st.text_input("Please enter your current password.", type = "password", help = "Should be at least 12 characters")
        new_password = st.text_input("Please enter your new password.", type = "password", help = 'Should be the same as the password entered above')
        confirm_new_password = st.text_input("Confirm new password.", type = "password")
        submit_password = st.form_submit_button("Update password")

        if submit_password:
            #used here and in delete account
            user_data = get_user(conn, username)
            id, user_name, user_hash, failed_attempts, locked = user_data
            if not new_password:
                st.error("Please enter your new password.")
            elif not is_valid_hash(current_password, user_hash):
                st.error("Current password is incorrect.")
            elif new_password == current_password:
                st.error("Your new password cannot be the same as your current password.")
            elif new_password != confirm_new_password:
                st.error("New passwords do not match.")
            elif len(new_password) < 12:
                st.error("Password is too short. A secure password should be longer than 12 characters.")
            else:
                email = get_email(conn, username)
                with st.spinner("Sending verification code to your email..."):
                    #sending the otp to the user
                    sending_OTP =  OTP_initialisation(email)
                if sending_OTP:
                    st.session_state['awaiting_otp'] = True
                    st.session_state['pending_new_hash'] = generate_hash(new_password)
                    st.rerun()
                else:
                        st.error("Could not send verification email. Please try again.")   
    if st.session_state.get('awaiting_otp'):
        st.info(f"A verification code has been sent to your email. Your code will expire in 5 minutes.")
        code_input = st.text_input("Enter the 6-digit code", key="otp_input", help = 'Check your email for a 6 digit code')

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("Verify"):
                with st.spinner("Verifying code..."):
                    #calls function which checks if it is the right otp
                    ok, msg = OTP_verification(code_input)
                if ok:
                    reset_password(conn, username, st.session_state['pending_new_hash'] )
                    st.session_state.pop('awaiting_otp', None)
                    st.session_state.pop("pending_new_hash", None)
                    time.sleep(1)
                    st.success("˖° ✧ Password updated! ✧ °˖")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(msg)
                st.stop()
        with col2:
            #cancel button if the user entered the wrong username - then the otp will be directed to someone else's email
            if st.button("Cancel"):
                st.session_state.pop('awaiting_otp', None)
                st.session_state.pop('pending_username', None)
                st.session_state.pop('otp_code', None)
                st.session_state.pop('otp_email', None)
                st.session_state.pop('otp_expires_at', None)
                st.session_state.pop('otp_attempts', None)
                st.rerun()
        st.stop()


#change email
st.divider()
st.subheader("Change email")

with st.expander("Change Email"):
    with st.form("change_email", clear_on_submit=True):
        new_email = st.text_input("Please enter your new email")
        submit_email = st.form_submit_button("Update email")

        if submit_email:
            if not new_email:
                st.error("Please enter your new email.")
            elif new_email == current_email:
                st.error("This is your current email.")
            elif "@" not in new_email or "." not in new_email:
                st.error("Please enter a valid email address.")
            elif not is_email_available(conn, new_email):
                st.error("This email is already registered to another account.")
            else:
                update_email(conn, username, new_email)
                st.success("𓆉⋆｡˚⋆❀ Email updated! ❀⋆｡˚⋆𓆉")


st.divider()
st.subheader("Delete account")

with st.expander("Delete account"):
    st.write("Deletion of account is permanent. Do you wish to proceed?")
    
    role = get_role(conn, username)
    if role == "Admin":
        st.error("Cannot delete an admin account.")
    else:
        if 'confirm_delete' not in st.session_state:
            st.session_state['confirm_delete'] = False

        if not st.session_state['confirm_delete']:
            if st.button("Delete"):
                st.session_state['confirm_delete'] = True
                st.rerun()
        else:
            st.warning("Are you sure you want to delete your account? Enter your password to delete your account.")
            with st.form("delete_account_form"):
                password = st.text_input("Password", type ="password")
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    confirm_delete = st.form_submit_button("Delete Account")
                with col2:
                    cancel_delete = st.form_submit_button("Cancel")
                
                if confirm_delete:
                    user_data = get_user(conn, username)
                    id, user_name, user_hash, failed_attempts, locked = user_data
                    if is_valid_hash(password, user_hash):
                        delete_one_user(conn, username)
                        st.session_state["Logged_in"] = False
                        st.session_state["username"] = None
                        st.session_state['confirm_delete'] = False
                        st.success("Your account has been deleted")
                        time.sleep(2)
                        st.switch_page("Home.py")
                    else:
                        st.error("Password is incorrect. Unable to delete account.")

                if cancel_delete:
                    st.session_state["confirm_delete"] = False
                    st.rerun()

#change username 
st.divider()
st.subheader("Background Theme")

with st.expander("Change Background Theme"):
    current_theme = get_user_theme(conn, username)
    theme_choice = st.selectbox(
    "Choose a theme",
    list(THEME_OPTIONS.keys()),
    index=list(THEME_OPTIONS.keys()).index(current_theme))

    if st.button("Save theme"):
        update_background(conn, username, theme_choice)
        st.success("°❀.ೃ࿔*°❀.ೃ࿔* Theme successfully changed. °❀.ೃ࿔*°❀.ೃ࿔*")
        st.rerun()

#sidebar logout and exit
with st.sidebar:
    st.header("Navigation")

with st.sidebar:
    if st.button("Log out"):
        st.session_state['confirm_logout'] = True
    if st.button("Exit"):
        st.session_state['confirm_exit'] = True

    if st.session_state.get('confirm_logout'):
        st.warning("Do you wish to log out ?")
        #allows user to logout
        if st.button("Yes, log out", key = "logout_yes"):
            st.session_state["Logged_in"] = False
            st.session_state["username"] = None
            st.session_state.pop('messages', None)
            st.session_state.pop('confirm_logout', None)
            st.switch_page("Home.py")

        #allows user to cancel choice
        if st.button("Cancel", key = "logout_no"):
            st.session_state['confirm_logout'] = False
            st.rerun()

    if st.session_state.get('confirm_exit'):
        st.warning("Do u wish to end the connection(close the app) ?")
        #allows user to exit
        if st.button("Yes, exit", key = "exit_yes"):
            st.info("Ending the connection. Please go back to VS Code.")
            #allwos the user to see the previous message to know what to do 
            time.sleep(2)
            os._exit(0)
        #allows user to cancel
        if st.button("Cancel", key = "exit_no"):
            st.info("Exit cancelled.")
            st.session_state['confirm_exit'] = False
            st.rerun()