import streamlit as st
import pandas as pd
import joblib
from datetime import date, timedelta
from pathlib import Path

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="StudySmart AI | Student Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- DESIGN ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #F5F7FC; }
    .block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1450px; }
    [data-testid="stSidebar"] { background: #101B36; }
    [data-testid="stSidebar"] * { color: #F3F6FF; }
    .hero { background: linear-gradient(120deg, #142448 0%, #244C91 65%, #477DE0 100%); padding: 30px 34px; border-radius: 22px; color: white; margin-bottom: 22px; }
    .hero h1 { color: white; font-family: 'Manrope', sans-serif; font-size: 35px; margin: 4px 0 8px 0; }
    .hero p { color: #E0E9FF; font-size: 15px; margin-bottom: 0; }
    .eyebrow { color: #BBD0FF; font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; }
    .section-title { font-family: 'Manrope', sans-serif; color: #172443; font-size: 22px; font-weight: 800; margin: 18px 0 12px 0; }
    .info-card { background: white; border: 1px solid #E6EAF3; border-radius: 17px; padding: 20px; min-height: 122px; box-shadow: 0 3px 14px rgba(31, 48, 84, 0.035); }
    .card-label { color: #71809B; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px; }
    .card-value { color: #182747; font-family: 'Manrope', sans-serif; font-size: 29px; font-weight: 800; margin: 8px 0 3px 0; }
    .card-note { color: #8490A7; font-size: 12px; }
    .tip-card { background: #EEF4FF; border-left: 4px solid #4D7FE5; padding: 14px 17px; border-radius: 9px; margin: 8px 0; color: #263B65; }
    div.stButton > button[kind="primary"] { background: #315FD0; border: none; border-radius: 10px; min-height: 46px; font-weight: 700; }
    div.stButton > button[kind="primary"]:hover { background: #2449A7; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- MODEL ----------
MODEL_PATH = Path(__file__).resolve().parent / "study_model.joblib"

@st.cache_resource
def load_model(model_path: str):
    return joblib.load(model_path)

model = None
model_ready = False
if MODEL_PATH.exists():
    try:
        model = load_model(str(MODEL_PATH))
        model_ready = True
    except Exception as exc:
        st.sidebar.error(f"Could not load model: {exc}")
else:
    st.sidebar.warning("Model file not found. Run train_model.py to create study_model.joblib.")

# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.markdown("## 📚 StudySmart AI")
    st.caption("YOUR PERSONAL LEARNING COMPANION")
    st.divider()
    page = st.radio(
        "NAVIGATION",
        ["🏠 Dashboard", "📝 My Subjects", "🗓️ Study Planner", "💡 Study Tips"],
        label_visibility="visible",
    )
    st.divider()
    st.markdown("### ⚙️ Your preferences")
    st.caption("Your entries are kept in this app session.")
    st.caption("This app does not save a student profile to a database.")

# ---------- HEADER ----------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">LEARN SMARTER · EVERY DAY</div>
      <h1>Your goals. Your plan. Your progress.</h1>
      <p>A personalized academic workspace to plan study time, review subjects, and understand how your habits relate to your estimated CGPA.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- DEFAULT PROFILE ----------
if "student_data" not in st.session_state:
    st.session_state.student_data = {
        "name": "", "college": "", "course": "", "semester": "Semester 1",
        "study_hours": 5.0, "extra_hours": 2.0, "sleep_hours": 8.0,
        "social_hours": 2.0, "activity_hours": 1.0, "stress": "Moderate",
        "available_hours": 3.0, "exam_date": date.today() + timedelta(days=14),
    }
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "Subject 1", "current": 55.0, "target": 80.0},
        {"name": "Subject 2", "current": 65.0, "target": 85.0},
        {"name": "Subject 3", "current": 70.0, "target": 85.0},
        {"name": "Subject 4", "current": 60.0, "target": 80.0},
        {"name": "Subject 5", "current": 75.0, "target": 90.0},
    ]

# ---------- PROFILE FORM ----------
st.markdown('<div class="section-title">👤 Student profile & daily routine</div>', unsafe_allow_html=True)
with st.expander("Enter or update your personal details and habits", expanded=True):
    with st.form("profile_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("Student name", value=st.session_state.student_data["name"])
            college = st.text_input("College name", value=st.session_state.student_data["college"])
        with c2:
            course = st.text_input("Course / branch", value=st.session_state.student_data["course"])
            semester_options = [f"Semester {i}" for i in range(1, 13)]
            current_semester = st.session_state.student_data["semester"]
            semester_index = semester_options.index(current_semester) if current_semester in semester_options else 0
            semester = st.selectbox("Semester", semester_options, index=semester_index)
        with c3:
            study_hours = st.number_input("Study hours per day", 0.0, 16.0, float(st.session_state.student_data["study_hours"]), 0.5)
            available_hours = st.number_input("Hours available for planned study", 0.5, 16.0, float(st.session_state.student_data["available_hours"]), 0.5)
        st.markdown("##### Your lifestyle")
        h1, h2, h3 = st.columns(3)
        with h1:
            extra_hours = st.number_input("Extracurricular hours/day", 0.0, 12.0, float(st.session_state.student_data["extra_hours"]), 0.5)
            sleep_hours = st.number_input("Sleep hours/day", 0.0, 16.0, float(st.session_state.student_data["sleep_hours"]), 0.5)
        with h2:
            social_hours = st.number_input("Social hours/day", 0.0, 16.0, float(st.session_state.student_data["social_hours"]), 0.5)
            activity_hours = st.number_input("Physical activity hours/day", 0.0, 12.0, float(st.session_state.student_data["activity_hours"]), 0.5)
        with h3:
            stress_options = ["Low", "Moderate", "High"]
            saved_stress = st.session_state.student_data["stress"]
            stress = st.selectbox("Current stress level", stress_options, index=stress_options.index(saved_stress) if saved_stress in stress_options else 1)
            exam_date = st.date_input("Next exam date", value=max(date.today(), st.session_state.student_data["exam_date"]), min_value=date.today())
        submitted = st.form_submit_button("Save profile & update dashboard", type="primary", use_container_width=True)
        if submitted:
            st.session_state.student_data = {
                "name": name, "college": college, "course": course, "semester": semester,
                "study_hours": study_hours, "extra_hours": extra_hours, "sleep_hours": sleep_hours,
                "social_hours": social_hours, "activity_hours": activity_hours, "stress": stress,
                "available_hours": available_hours, "exam_date": exam_date,
            }
            st.success("Profile updated successfully!")

p = st.session_state.student_data
subjects = st.session_state.subjects
days_left = max(0, (p["exam_date"] - date.today()).days)

# ---------- SUBJECTS PAGE ----------
if page == "📝 My Subjects":
    st.markdown('<div class="section-title">📘 Manage your subjects</div>', unsafe_allow_html=True)
    st.write("Enter your current marks and your target marks out of 100.")
    with st.form("subjects_form"):
        updated_subjects = []
        for i, subject in enumerate(subjects):
            st.markdown(f"**Subject {i + 1}**")
            a, b, c = st.columns([2, 1, 1])
            with a:
                sub_name = st.text_input("Subject name", value=subject["name"], key=f"sub_name_{i}")
            with b:
                current = st.number_input("Current marks (%)", 0.0, 100.0, float(subject["current"]), 1.0, key=f"current_{i}")
            with c:
                target = st.number_input("Target marks (%)", 0.0, 100.0, float(subject["target"]), 1.0, key=f"target_{i}")
            updated_subjects.append({"name": sub_name.strip() or f"Subject {i + 1}", "current": current, "target": target})
        save_subjects = st.form_submit_button("Save all subjects", type="primary", use_container_width=True)
        if save_subjects:
            st.session_state.subjects = updated_subjects
            st.success("Subjects saved!")
    subjects = st.session_state.subjects
    st.markdown("### Current vs target marks")
    subject_chart = pd.DataFrame(subjects).rename(columns={"name": "Subject", "current": "Current marks", "target": "Target marks"}).set_index("Subject")
    st.bar_chart(subject_chart)

# ---------- PREDICTION (independent of page navigation) ----------
predicted_gpa = None
estimated_cgpa = None
if model_ready:
    model_input = pd.DataFrame([{
        "Study_Hours_Per_Day": p["study_hours"],
        "Extracurricular_Hours_Per_Day": p["extra_hours"],
        "Sleep_Hours_Per_Day": p["sleep_hours"],
        "Social_Hours_Per_Day": p["social_hours"],
        "Physical_Activity_Hours_Per_Day": p["activity_hours"],
        "Stress_Level": p["stress"],
    }])
    try:
        predicted_gpa = float(model.predict(model_input)[0])
        # Assumes the trained model target is on a 4-point GPA scale.
        # This is an approximate display conversion, not an official university formula.
        estimated_cgpa = max(0.0, min(10.0, (predicted_gpa / 4.0) * 10.0))
    except Exception as exc:
        st.error(f"Could not generate CGPA prediction: {exc}")

# ---------- DASHBOARD PAGE ----------
if page == "🏠 Dashboard":
    greeting = f"Welcome back, {p['name']} 👋" if p["name"].strip() else "Welcome to your dashboard 👋"
    st.subheader(greeting)
    detail = " · ".join(x for x in [p["college"], p["course"], p["semester"]] if x)
    if detail:
        st.caption(detail)
    subjects = st.session_state.subjects
    avg_mark = sum(s["current"] for s in subjects) / len(subjects) if subjects else 0
    target_avg = sum(s["target"] for s in subjects) / len(subjects) if subjects else 0
    st.markdown('<div class="section-title">📊 Your academic snapshot</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        value = f"{estimated_cgpa:.2f} / 10" if estimated_cgpa is not None else "N/A"
        st.markdown(f'''<div class="info-card"><div class="card-label">AI-estimated CGPA</div><div class="card-value">{value}</div><div class="card-note">Approximate lifestyle-based estimate</div></div>''', unsafe_allow_html=True)
    with k2:
        st.markdown(f'''<div class="info-card"><div class="card-label">Average subject marks</div><div class="card-value">{avg_mark:.1f}%</div><div class="card-note">Based on your manual entries</div></div>''', unsafe_allow_html=True)
    with k3:
        st.markdown(f'''<div class="info-card"><div class="card-label">Target average</div><div class="card-value">{target_avg:.1f}%</div><div class="card-note">Your entered academic goal</div></div>''', unsafe_allow_html=True)
    with k4:
        st.markdown(f'''<div class="info-card"><div class="card-label">Days until exam</div><div class="card-value">{days_left}</div><div class="card-note">{p['exam_date'].strftime('%d %b %Y')}</div></div>''', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Subject performance</div>', unsafe_allow_html=True)
    chart_df = pd.DataFrame(subjects).rename(columns={"name": "Subject", "current": "Current marks", "target": "Target marks"}).set_index("Subject")
    st.bar_chart(chart_df[["Current marks", "Target marks"]], height=300)
    st.markdown('<div class="section-title">🎯 Focus areas</div>', unsafe_allow_html=True)
    priorities = sorted(subjects, key=lambda s: (s["target"] - s["current"]), reverse=True)
    for subject in priorities[:3]:
        gap = max(0, subject["target"] - subject["current"])
        st.markdown(f'<div class="tip-card"><b>{subject["name"]}</b> — Current: {subject["current"]:.0f}% · Target: {subject["target"]:.0f}% · Target gap: {gap:.0f} percentage points</div>', unsafe_allow_html=True)
    st.caption("CGPA is a model estimate, not an official academic result. Subject marks and target gaps come from your own entries.")
    if predicted_gpa is not None:
        st.info("The CGPA display assumes the model's original GPA target is on a 4-point scale. Confirm the dataset's scale before relying on this conversion.")

# ---------- STUDY PLANNER PAGE ----------
elif page == "🗓️ Study Planner":
    st.markdown('<div class="section-title">🗓️ Your daily study timetable</div>', unsafe_allow_html=True)
    st.write(f"You have entered **{p['available_hours']:.1f} hours** for planned study each day. Your next exam is in **{days_left} days**.")
    priorities = sorted(st.session_state.subjects, key=lambda s: (s["target"] - s["current"]), reverse=True)
    total_gap = sum(max(0, s["target"] - s["current"]) for s in priorities)
    if not priorities:
        st.info("Add subjects on the My Subjects page to create a timetable.")
    else:
        weights = ([1 / len(priorities)] * len(priorities)) if total_gap == 0 else [max(0, s["target"] - s["current"]) / total_gap for s in priorities]
        total_minutes = int(p["available_hours"] * 60)
        allocated = []
        remaining = total_minutes
        for i, (subject, weight) in enumerate(zip(priorities, weights)):
            minutes = remaining if i == len(priorities) - 1 else int(total_minutes * weight)
            if i != len(priorities) - 1:
                remaining -= minutes
            allocated.append((subject, max(0, minutes)))
        timetable = [{"Study block": s["name"], "Duration": f"{m // 60}h {m % 60}m", "Task": "Practice questions, revise notes, and review mistakes"} for s, m in allocated if m > 0]
        timetable += [
            {"Study block": "Breaks", "Duration": "10–15 min", "Task": "Take a screen-free break between longer sessions"},
            {"Study block": "Daily review", "Duration": "10 min", "Task": "Recall key ideas without looking at notes"},
        ]
        st.dataframe(pd.DataFrame(timetable), use_container_width=True, hide_index=True)
        st.markdown("### ✅ Today's checklist")
        for i, subject in enumerate(priorities):
            st.checkbox(f"Revise {subject['name']}", key=f"planner_check_{i}")
        st.checkbox("Review mistakes and difficult questions", key="review_check")
        st.checkbox("Prepare tomorrow's top three tasks", key="tomorrow_check")
        st.info("The schedule allocates more time to subjects with larger gaps between your current and target marks. Adjust it to match your syllabus and exam dates.")

# ---------- STUDY TIPS PAGE ----------
elif page == "💡 Study Tips":
    st.markdown('<div class="section-title">💡 Habits for effective studying</div>', unsafe_allow_html=True)
    tips = [
        ("🎯 Active recall", "Close your notes and try to explain a concept from memory."),
        ("⏱️ Focus sessions", "Try 25–50 minutes of focused work followed by a short break."),
        ("🔁 Spaced revision", "Review difficult material after one day, several days, and one week."),
        ("📝 Practice questions", "Use previous questions or self-tests to identify weak topics."),
        ("😴 Sleep routine", "Keep a consistent sleep schedule to support attention and learning."),
        ("🌿 Manage stress", "Break big tasks into smaller actions and make time for recovery."),
    ]
    for title, description in tips:
        st.markdown(f'<div class="tip-card"><b>{title}</b><br>{description}</div>', unsafe_allow_html=True)
    st.markdown("### Your current routine")
    a, b, c = st.columns(3)
    a.metric("Study hours/day", f"{p['study_hours']:.1f}")
    b.metric("Sleep hours/day", f"{p['sleep_hours']:.1f}")
    c.metric("Stress level", p["stress"])
    if p["sleep_hours"] < 7:
        st.warning("You entered less than 7 hours of sleep. Consider whether you can make room for more rest.")
    if p["stress"] == "High":
        st.info("Try dividing your next task into a small 15-minute starting step.")
    if p["study_hours"] < 2:
        st.info("Start small: schedule one focused session, then build your routine gradually.")

# ---------- FOOTER ----------
st.divider()
st.caption("StudySmart AI · A student planning and learning support project. Predictions are estimates and should not replace official academic results.")
