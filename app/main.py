import streamlit as st
from prediction_helper import predict

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Credit Risk Assessment",
    page_icon="📊",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("Credit Risk Assessment")
st.caption("AI-based Loan Risk Evaluation System")

st.divider()

# ---------------- SECTION 1 ----------------
st.subheader("Applicant Profile")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=28)

with col2:
    income = st.number_input("Annual Income (₹)", min_value=0, value=1200000)

with col3:
    residence_type = st.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

# ---------------- SECTION 2 ----------------
st.subheader("Loan Details")

col4, col5, col6, col7 = st.columns(4)

with col4:
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=2560000)

with col5:
    loan_tenure_months = st.number_input("Tenure (Months)", min_value=1, value=36)

with col6:
    loan_purpose = st.selectbox("Loan Purpose", ["Education", "Home", "Auto", "Personal"])

with col7:
    loan_type = st.selectbox("Loan Type", ["Unsecured", "Secured"])

# ---------------- LTI ----------------
if income > 0:
    lti = loan_amount / income
    st.info(f"Loan-to-Income Ratio: {lti:.2f}x")
else:
    lti = 0
    st.warning("Income must be greater than 0")

# ---------------- SECTION 3 ----------------
st.subheader("Risk Indicators")

col8, col9, col10, col11 = st.columns(4)

with col8:
    avg_dpd = st.number_input("Avg DPD", min_value=0, value=20)

with col9:
    delinquency_ratio = st.number_input("Delinquency (%)", min_value=0, max_value=100, value=30)

with col10:
    credit_utilization = st.number_input("Credit Utilization (%)", min_value=0, max_value=100, value=30)

with col11:
    open_accounts = st.number_input("Open Accounts", min_value=1, max_value=10, value=2)

st.divider()

# ---------------- BUTTONS ----------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    run = st.button("Calculate Risk")

with col_btn2:
    if st.button("Reset"):
        st.rerun()

# ---------------- RESULT ----------------
if run:
    if income <= 0 or loan_amount <= 0:
        st.error("Please enter valid Income and Loan Amount")
    else:
        with st.spinner("Analyzing risk..."):
            probability, credit_score, rating = predict(
                age, income, loan_amount, loan_tenure_months,
                avg_dpd, delinquency_ratio,
                credit_utilization, open_accounts,
                residence_type, loan_purpose, loan_type
            )

        st.subheader("Results")

        r1, r2, r3 = st.columns(3)

        r1.metric("Default Probability", f"{probability:.2%}")
        r2.metric("Credit Score", credit_score)
        r3.metric("Rating", rating)

        # Decision Insight
        if probability >= 0.6:
            st.error("High Risk Applicant")
        elif probability >= 0.3:
            st.warning("Moderate Risk Applicant")
        else:
            st.success("Low Risk Applicant")