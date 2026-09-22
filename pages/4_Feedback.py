import streamlit as st
from main import profile_icon]

profile_icon()

st.title("📬 Contact Us")
st.write("We would love to hear from you!") 
st.write("Reach out to us using the details below:")

# Company email (clickable)
company_email = "testingcw331@gmail.com"
st.markdown(f"**Email:** [{company_email}](mailto:{company_email})")

# Company phone (clickable)
company_phone = "+230 123 4567"
st.markdown(f"**Phone:** [{company_phone}](tel:{company_phone})")

# # Company address
# company_address = "123 Business Street, Vacoas-Phoenix, Mauritius"
# st.markdown(f"**Address:** {company_address}")

# # Optional: add a feedback form
# st.write("### Send us a message")
# with st.form("feedback_form", clear_on_submit=True):
#     name = st.text_input("Your Name")
#     email = st.text_input("Your Email")
#     message = st.text_area("Your Message")
#     submitted = st.form_submit_button("Submit")

#     if submitted:
#         if not name or not email or not message:
#             st.error("⚠ Please fill in all fields before submitting.")
#         else:
#             # Here you can save to DB or send via email
#             st.success("✅ Thank you for your feedback! We’ll get back to you soon.")
