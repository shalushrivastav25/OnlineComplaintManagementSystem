import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Online Complaint Management System",
    page_icon="📋",
    layout="wide"
)

DB = "complaints.db"

def connect():
    return sqlite3.connect(DB)

def initialize():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                created_at TEXT NOT NULL
            )
        """)

initialize()

# Demo credentials
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = "user"

st.title("📋 Online Complaint Management System")
st.caption("Submit, track, and manage complaints online.")

with st.sidebar:
    st.header("Navigation")

    if st.session_state.logged_in:
        st.success(f"Signed in as {st.session_state.role.title()}")

        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.role = "user"
            st.rerun()

    else:
        page = st.radio(
            "Choose a page",
            ["Submit Complaint", "Track Complaint", "Admin Login"]
        )

    st.divider()
    st.caption("Educational project prototype")

if not st.session_state.logged_in:
    if page == "Submit Complaint":
        st.header("📝 Submit a Complaint")
        st.write("Please provide the details of your complaint.")

        with st.form("complaint_form"):
            name = st.text_input("Full name")
            email = st.text_input("Email address")
            category = st.selectbox(
                "Complaint category",
                ["Education", "Healthcare", "Public Services",
                 "Technology", "Transport", "Other"]
            )
            title = st.text_input("Complaint title")
            description = st.text_area("Describe your complaint")
            submitted = st.form_submit_button(
                "Submit Complaint",
                use_container_width=True
            )

        if submitted:
            if not all([name.strip(), email.strip(),
                        title.strip(), description.strip()]):
                st.error("Please fill in every field.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.error("Please enter a valid email address.")
            else:
                with connect() as conn:
                    cursor = conn.execute("""
                        INSERT INTO complaints
                        (name, email, category, title, description,
                         status, created_at)
                        VALUES (?, ?, ?, ?, ?, 'Pending', ?)
                    """, (
                        name.strip(), email.strip(), category,
                        title.strip(), description.strip(),
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))
                    complaint_id = cursor.lastrowid

                st.success(
                    f"Complaint submitted successfully! "
                    f"Your complaint ID is: {complaint_id}"
                )
                st.info("Save this ID to track your complaint.")

    elif page == "Track Complaint":
        st.header("🔎 Track Your Complaint")
        complaint_id = st.number_input(
            "Enter complaint ID",
            min_value=1,
            step=1
        )

        if st.button("Track Complaint"):
            with connect() as conn:
                result = conn.execute("""
                    SELECT id, category, title, description,
                           status, created_at
                    FROM complaints WHERE id = ?
                """, (complaint_id,)).fetchone()

            if result:
                st.subheader(f"Complaint #{result[0]}")
                st.write(f"**Category:** {result[1]}")
                st.write(f"**Title:** {result[2]}")
                st.write(f"**Description:** {result[3]}")
                st.write(f"**Submitted:** {result[5]}")
                st.metric("Current Status", result[4])
            else:
                st.warning("Complaint not found. Please check the ID.")

    elif page == "Admin Login":
        st.header("🔐 Administrator Login")

        with st.form("admin_login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login = st.form_submit_button("Sign In")

        if login:
            if username == ADMIN_USER and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()
            else:
                st.error("Incorrect username or password.")

else:
    st.header("🛠️ Admin Dashboard")

    with connect() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM complaints ORDER BY id DESC", conn
        )

    total = len(df)
    pending = int((df["status"] == "Pending").sum()) if total else 0
    progress = int((df["status"] == "In Progress").sum()) if total else 0
    resolved = int((df["status"] == "Resolved").sum()) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Complaints", total)
    c2.metric("Pending", pending)
    c3.metric("In Progress", progress)
    c4.metric("Resolved", resolved)

    st.divider()
    st.subheader("All Complaints")

    if total:
        search = st.text_input("Search by title, name, or email")
        status_filter = st.selectbox(
            "Filter by status",
            ["All", "Pending", "In Progress", "Resolved"]
        )

        filtered = df.copy()

        if search:
            mask = (
                filtered["title"].str.contains(search, case=False, na=False)
                | filtered["name"].str.contains(search, case=False, na=False)
                | filtered["email"].str.contains(search, case=False, na=False)
            )
            filtered = filtered[mask]

        if status_filter != "All":
            filtered = filtered[filtered["status"] == status_filter]

        st.dataframe(
            filtered[["id", "name", "category", "title",
                      "status", "created_at"]],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Update Complaint Status")

        selected_id = st.selectbox(
            "Select complaint ID",
            df["id"].tolist()
        )

        current_status = df.loc[
            df["id"] == selected_id, "status"
        ].iloc[0]

        new_status = st.selectbox(
            "New status",
            ["Pending", "In Progress", "Resolved"],
            index=["Pending", "In Progress", "Resolved"].index(current_status)
        )

        if st.button("Update Status"):
            with connect() as conn:
                conn.execute(
                    "UPDATE complaints SET status = ? WHERE id = ?",
                    (new_status, selected_id)
                )
            st.success(f"Complaint #{selected_id} updated to {new_status}.")
            st.rerun()

        st.download_button(
            "Download Complaint Report (CSV)",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="complaint_report.csv",
            mime="text/csv"
        )

    else:
        st.info("No complaints have been submitted yet.")

st.divider()
st.caption("Online Complaint Management System | Student Project")
