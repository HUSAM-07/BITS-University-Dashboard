import streamlit as st
import pandas as pd 
import json  # Added this line


def main():
    st.set_page_config(page_title="BITS Pilani, Dubai Clubs Dashboard", page_icon=":mortar_board:", layout="centered")
    st.title("University Dashboard")
    st.markdown("---")

    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.selectbox("Go to", ("Home","University Resources", "Clubs Resources", "Attendance Tracker"))

    if section == "Home":
        show_homepage()
    elif section == "University Resources":
        show_university_resources()
    elif section == "Clubs Resources":
        show_clubs_resources()
    elif section == "Attendance Tracker":
        show_attendance_tracker()

    st.divider()
    st.caption("Designed & Developed by HUSAM")
    st.write("This Web App Is Made to Help You Access All The Important BITS Pilani, Dubai Admin & Academic Websites at a Single Website")


def show_homepage():
    st.header("Welcome to the University Clubs Dashboard!")
    st.write("Use the sidebar to navigate to different sections.")

    # Initialize session state for subjects if not already present
    if 'subjects' not in st.session_state:
        st.session_state.subjects = {}

    # Load subjects from query parameters if available
    if 'subjects' in st.query_params:
        subjects_json = st.query_params['subjects']
        try:
            st.session_state.subjects = json.loads(subjects_json)
        except json.JSONDecodeError:
            st.error("Error decoding subjects from URL. Using empty subjects.")
            st.session_state.subjects = {}

    # Brief overview of features
    st.subheader("Features:")
    st.write("- Track attendance for your subjects")
    st.write("- Access university and club resources")
    st.write("- Stay updated with important information")

    st.info("Navigate to the Attendance Tracker to manage your subjects and attendance.")

    # Save subjects to query parameters whenever it changes
    st.query_params['subjects'] = json.dumps(st.session_state.subjects)


def show_clubs_resources():
    st.header("Clubs Resources")
    st.markdown("---")
    st.markdown("Feel free to contribute")

    resources = [
        ("GDSC Resources", "https://gdscbpdc.github.io/"),
        ("ACM Resources", "https://openlib-cs.acmbpdc.org/"),
        ("Ahmed Thahir's Notes", "https://uni-notes.netlify.app/")
    ]

    for title, url in resources:
        st.subheader(title)
        st.components.v1.iframe(url, width=1000, height=600, scrolling=True)
        st.markdown("---")


def show_university_resources():
    st.header("University Resources")
    st.markdown("---")

    resources = [
        ("Library Resources", "http://webopac.bits-dubai.ac.ae/AutoLib/index.jsp"),
        ("Courses & LMS", "https://lms.bitspilanidubai.ae/login/index.php"),
        ("BITS ERP", "https://erp.bits-pilani.ac.in/")
    ]

    for title, url in resources:
        st.subheader(title)
        st.components.v1.iframe(url, width=1000, height=600, scrolling=True)
        st.markdown("---")


def show_attendance_tracker():
    st.header("Attendance Tracker")

    # Add new subject (hidden in an expander)
    with st.expander("Add New Subject"):
        new_subject = st.text_input("Enter a new subject:")
        total_classes = st.number_input("Total number of classes for the semester:", min_value=1, value=30)
        st.caption("There are typically 30 classes in a semester for a 3 credit course")
        if st.button("Add Subject"):
            if new_subject and new_subject not in st.session_state.subjects:
                st.session_state.subjects[new_subject] = {"total": total_classes, "missed": 0}
                st.success(f"Added {new_subject} with {total_classes} total classes.")
            else:
                st.error("Subject already exists or invalid name.")

    # Display and update existing subjects
    if st.session_state.subjects:
        st.subheader("Your Subjects")
        
        # Create columns for a more compact layout
        cols = st.columns(4)
        cols[0].subheader("Subject")
        cols[1].subheader("Missed")
        cols[2].subheader("Total")
        cols[3].subheader("Attendance")

        for subject, data in st.session_state.subjects.items():
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(subject)
            with col2:
                missed = st.number_input(f"Missed classes for {subject}", 
                                         min_value=0, 
                                         max_value=data['total'], 
                                         value=data['missed'],
                                         key=f"{subject}_missed",
                                         label_visibility="collapsed")
                if missed != data['missed']:
                    st.session_state.subjects[subject]['missed'] = missed
            with col3:
                st.write(data['total'])
            with col4:
                attendance = ((data['total'] - missed) / data['total']) * 100
                st.write(f"{attendance:.2f}%")
            
            # Progress bar for visual representation
            st.progress(attendance / 100)

        # Clear all subjects button (at the bottom)
        if st.button("Clear All Subjects"):
            st.session_state.subjects = {}
            st.session_state.subjects_json = '{}'
            st.markdown(
                """
                <script>
                    localStorage.removeItem('subjects');
                </script>
                """,
                unsafe_allow_html=True
            )
            st.query_params.clear()
            st.experimental_rerun()
    else:
        st.info("No subjects added yet. Use the 'Add New Subject' section to start tracking attendance.")

    # Update query params
    st.query_params['subjects'] = json.dumps(st.session_state.subjects)


if __name__ == '__main__':
    # Initialize session state for attendance tracking
    if 'subjects' not in st.session_state:
        st.session_state.subjects = {}

    main()