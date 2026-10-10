import streamlit as st
import datetime
import json
import os

# Set the browser tab title, favicon, and a centered layout for readability
st.set_page_config(
    page_title="Holiday Planner",
    page_icon="✈️",
    layout="centered"
)

# Application header
st.title("✈️ Holiday & Travel Planner")

# Filepath used for storing trip data locally in JSON format
DATA_FILE = "trips.json"


def load_trips():
    """Reads existing trip data from the local JSON file.
    
    Returns an empty list if the file has not been created yet.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_trips(trips):
    """Writes the current list of trips back to the JSON file with clean indentation."""
    with open(DATA_FILE, "w") as f:
        json.dump(trips, f, indent=2)


# Load trips from storage on each run
trips = load_trips()

# Use an expandable accordion to keep the interface neat
with st.expander("➕ Add New Trip", expanded=True):
    # Form batches input updates so the page only reruns when submitted
    with st.form("new_trip"):
        destination = st.text_input("Destination")

        # Place date selectors side-by-side in two columns
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", min_value=datetime.date.today())
        end_date = col2.date_input("End Date", min_value=datetime.date.today())

        budget = st.number_input("Estimated Budget (£)", min_value=0, step=50)

        # Form submission trigger button
        submitted = st.form_submit_button("Save Trip")

        if submitted:
            # 1. Ensure the holiday doesn't end before it starts
            if end_date < start_date:
                st.error("End date cannot be before start date.")
            # 2. Prevent empty destination submissions
            elif not destination.strip():
                st.error("Destination cannot be empty.")
            else:
                # Append new record (convert date objects to strings for JSON compatibility)
                trips.append({
                    "destination": destination.strip(),
                    "start": str(start_date),
                    "end": str(end_date),
                    "budget": budget
                })
                # Persist changes to disk
                save_trips(trips)
                st.success(f"Trip to {destination} added!")
                # Rerun the app to immediately refresh the displayed trips list
                st.rerun()

st.subheader("Your Upcoming Trips")

# Display a notice if no records exist yet, otherwise iterate and print details
if not trips:
    st.info("No trips planned yet.")
else:
    for t in trips:
        st.write(
            f"**{t['destination']}** | "
            f"{t['start']} to {t['end']} | "
            f"Budget: £{t['budget']}"
        )
