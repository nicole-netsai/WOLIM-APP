import streamlit as st
from datetime import datetime, date
import pandas as pd
from PIL import Image

# Configure page
st.set_page_config(
    page_title="Birthday Tracker",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for pink floral theme
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# User database with allowed users
USER_DATABASE = {
    "Nicole Netsai Nharaunda": "team esther leads",
    "Dcnes Antonette Manzungu": "team esther leads",
    "Mrs Viginia Tapfuma": "team esther leads"
}

# Convert to DataFrame
df = pd.DataFrame(BIRTHDAY_DATA)

# Login function
def authenticate(username, password):
    return username in USER_DATABASE and USER_DATABASE[username] == password

# Process birthdays
def process_birthdays(df):
    today = datetime.now()
    current_month = today.month
    current_day = today.day
    
    upcoming = []
    
    for _, row in df.iterrows():
        try:
            if pd.isna(row['Date']) or "Not Known" in row['Date']:
                continue
                
            month, day, year = map(int, row['Date'].split('/'))
            if month == current_month and day >= current_day:
                upcoming.append({
                    "Name": row['Name'],
                    "Date": f"{month}/{day}",
                    "Days Away": day - current_day,
                    "Turning": today.year - year if year > 0 else "Unknown"
                })
            elif month > current_month:
                upcoming.append({
                    "Name": row['Name'],
                    "Date": f"{month}/{day}",
                    "Days Away": (date(today.year, month, day) - today.date()).days,
                    "Turning": today.year - year if year > 0 else "Unknown"
                })
        except:
            continue
    
    return pd.DataFrame(upcoming).sort_values("Days Away")

# Main app
def main():
    st.title("🌸 House of Esther Birthday Tracker")
    st.markdown("""
    <div style="background-color:#ffebee;padding:10px;border-radius:10px;margin-bottom:20px;">
    <p style="text-align:center;font-style:italic;color:#d81b60;">
    "and who knoweth whether thou art come to the kingdom for such a time as this?."<br>
    - Esther 4:14
    </p>
    </div>
    """, unsafe_allow_html=True)

    # Login section
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        with st.form("login_form"):
            st.subheader("Login")
            username = st.selectbox("Select your name", list(USER_DATABASE.keys()))
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.user = username
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        return

    # Main content after login
    st.success(f"Welcome, {st.session_state.user}! ❤️")
    
    # Display upcoming birthdays
    st.header("🎉 Upcoming Birthdays")
    upcoming_bdays = process_birthdays(df)
    
    if not upcoming_bdays.empty:
        for _, row in upcoming_bdays.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="background-color:#fce4ec;padding:15px;border-radius:10px;margin-bottom:10px;">
                    <h3 style="color:#c2185b;">{row['Name']}</h3>
                    <p><b>Date:</b> {row['Date']} • <b>Days Away:</b> {row['Days Away']} • <b>Turning:</b> {row['Turning']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No upcoming birthdays in the next month. Check back later!")
    
    # Full database view
    st.header("📅 Complete Birthday Database")
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Logout button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

if __name__ == "__main__":
    main()
