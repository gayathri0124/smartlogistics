
import os
import streamlit as st

def main():
    st.title("Environment Variable Checker")
    
    email_vars = [
        "EMAIL_SENDER",
        "EMAIL_PASSWORD",
        "EMAIL_SMTP_SERVER",
        "EMAIL_SMTP_PORT"
    ]
    
    st.write("Checking environment variables for email configuration:")
    
    all_present = True
    for var in email_vars:
        value = os.environ.get(var)
        if value:
            masked_value = value if var != "EMAIL_PASSWORD" else "******" 
            st.success(f"✅ {var} is set to: {masked_value}")
        else:
            st.error(f"❌ {var} is not set")
            all_present = False
    
    if all_present:
        st.success("All required environment variables are set!")
    else:
        st.error("Some required environment variables are missing.")
        st.info("Please set these in the Replit Secrets tool.")

if __name__ == "__main__":
    main()
