import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# -------------------------------
# Google Sheets Setup with Caching
# -------------------------------

@st.cache_resource
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_file(
        'C:/Users/janar226/Desktop/StreamlitApp/credentials.json', scopes=scope
    )
    client = gspread.authorize(credentials)
    return client

client = get_gspread_client()
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1TFB6s4MLhImsrDzWjWaSLQFBSp_waOvy6i2yiWZGhCQ/edit?gid=0')
worksheet = spreadsheet.worksheet("Sheet1")

# -------------------------------
# Function to save participant feedback to Google Sheets
# -------------------------------

def save_feedback_to_google_sheets(feedback):
    try:
        worksheet.append_row([feedback])
        st.session_state.feedback_submitted = True
    except gspread.exceptions.APIError as e:
        st.error(f"Failed to save feedback to Google Sheet: {e}")
    except Exception as e:
        st.error("An unexpected error occurred.")
        print(e)  # Consider using logging instead

# -------------------------------
# Main Function
# -------------------------------

def main():
    st.title("Military Decision-Making Feedback Test")

    # Initialize the session state if it's not already set
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False

    # If feedback is submitted, only show the thank you message
    if st.session_state.feedback_submitted:
        st.markdown("<h3 style='text-align: center; color: green;'>Thank you for sharing your thoughts</h3>", unsafe_allow_html=True)
    else:
        # Show the feedback form if feedback hasn't been submitted
        with st.form(key="feedback_form"):
            feedback = st.text_area("Please provide any feedback about your decision-making experience (optional):", key="feedback")
            submit_button = st.form_submit_button(label="Submit Feedback")
            
            if submit_button:
                if feedback.strip():  # Ensure feedback is not empty
                    save_feedback_to_google_sheets(feedback)
                else:
                    st.warning("Please enter some feedback before submitting.")

# Run the main function
if __name__ == "__main__":
    main()
