import streamlit as st
import time
import datetime
import random

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="MindMinute", page_icon="🧘", layout="centered")


# =========================================================
# CSS: Pastel Theme + Clean Dropdown + Button Styling
# =========================================================
st.markdown("""
<style>

.main {
    background: linear-gradient(to bottom right, #faf8ff, #f3efff);
}

/* ---------- CLEAN LONG RECTANGULAR DROPDOWN ---------- */

/* Wipe wrapper spacing */
div[data-testid="stSelectbox"] > div:nth-child(2) {
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
}

/* Remove container borders */
div[data-baseweb="select"] {
    border: none !important;
}

/* The actual clean rectangle */
div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 2px solid #d9d2ff !important;
    border-radius: 14px !important;
    min-height: 56px !important;
    font-size: 18px !important;
    padding: 10px 12px !important;
    box-shadow: none !important;
}

/* Dropdown options styles */
ul[role="listbox"] li {
    font-size: 18px !important;
    padding: 12px !important;
    color: #4b3fa3 !important;
}

/* ---------- Inputs & buttons ---------- */
.stTextInput input {
    border-radius: 12px !important;
    border: 1.6px solid #d4ccff !important;
    padding: 8px !important;
}

.stButton button {
    background-color: #cfc9ff !important;
    color: #2d2566 !important;
    padding: 0.6em 1.3em !important;
    font-size: 1rem !important;
    border-radius: 14px !important;
    border: none !important;
    font-weight: 600 !important;
    white-space: nowrap !important; /* keep text on one line */
}
.stButton>button:hover {
    background-color: #bfb6ff !important;
}

/* SOS button color override */
.sos-btn button {
    background-color: #ffb3c1 !important;
    color: #5b1020 !important;
}
.sos-btn button:hover {
    background-color: #ff9aa9 !important;
}

/* Headers */
h1, h2, h3 {
    color: #4b3fa3 !important;
    font-family: 'Segoe UI', sans-serif;
}

hr {
    border: 1px solid #e0d8ff;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# PASTEL BOX
# =========================================================
def pastel_box(text):
    st.markdown(
        f"""
        <div style="
            background-color: #ffffff;
            border: 2px solid #e6e0ff;
            padding: 15px;
            border-radius: 14px;
            margin-top: 10px;
            margin-bottom: 18px;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "mood_log" not in st.session_state:
    # each entry: (date_str, time_str, mood, score)
    st.session_state.mood_log = []

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "requested_page" not in st.session_state:
    st.session_state.requested_page = None

if "page_selector" not in st.session_state:
    st.session_state.page_selector = "Home"


# =========================================================
# NAVIGATION HELPERS
# =========================================================
def go_to(page_name: str):
    """Request navigation to another page, then rerun."""
    st.session_state.requested_page = page_name
    st.rerun()

def back_to_home():
    """Back button shown on tool pages."""
    if st.button("← Back", key=f"back_{st.session_state.page_selector}"):
        go_to("Home")


# process pending navigation BEFORE sidebar
if st.session_state.requested_page:
    st.session_state.page_selector = st.session_state.requested_page
    st.session_state.requested_page = None


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
page = st.sidebar.radio(
    "Choose a tool:",
    ["Home", "Breathing", "Brain Dump", "Body Reset", "Grounding", "SOS"],
    key="page_selector",
)


# =========================================================
# MOOD SCORES + QUOTES
# =========================================================
MOOD_SCORES = {
    "😊 Good": 4,
    "😐 Okay": 3,
    "😫 Stressed": 2,
    "😞 Overwhelmed": 1,
    "😴 Tired": 2,
}

MOOD_QUOTES = {
    "😊 Good": [
        "Keep that glow going ✨",
        "You’re building a version of you that you’ll be proud of.",
        "Take a second to notice how good this feels."
    ],
    "😐 Okay": [
        "You don’t have to be amazing today. Showing up is enough.",
        "‘Okay’ is a perfectly valid place to be.",
        "Tiny steps still count as progress."
    ],
    "😫 Stressed": [
        "You’re allowed to pause. The world can wait a minute.",
        "Your best today might look different than yesterday, and that’s okay.",
        "You’ve survived 100% of your hard days so far."
    ],
    "😞 Overwhelmed": [
        "You don’t have to handle everything at once.",
        "You are not your to-do list.",
        "Even on the days you feel like you’re failing, you’re still learning."
    ],
    "😴 Tired": [
        "Rest is productive too.",
        "You deserve gentleness, especially from yourself.",
        "Slow is still a speed."
    ],
}


# =========================================================
# STREAK HELPER
# =========================================================
def compute_streak_days():
    """Return how many consecutive days (including today) the user has checked in."""
    if not st.session_state.mood_log:
        return 0

    # collect all dates as datetime.date
    dates = []
    for entry in st.session_state.mood_log:
        if len(entry) >= 1:
            try:
                dates.append(datetime.date.fromisoformat(entry[0]))
            except Exception:
                continue
    if not dates:
        return 0

    uniq = set(dates)
    today = datetime.date.today()
    streak = 0
    current = today
    while current in uniq:
        streak += 1
        current -= datetime.timedelta(days=1)
    return streak


# =========================================================
# HOME PAGE
# =========================================================
if page == "Home":

    # --- Name input ---
    st.session_state.user_name = st.text_input(
        "What’s your name?",
        value=st.session_state.user_name,
        placeholder="Enter your name"
    )

    # --- Greeting ---
    if st.session_state.user_name.strip():
        day = datetime.datetime.now().strftime("%A")
        hour = datetime.datetime.now().hour
        part = "morning" if hour < 12 else "afternoon" if hour < 18 else "evening"

        st.markdown(
            f"""
            <h2 style='font-size: 30px; color:#4b3fa3;'>
                ✨ Hey {st.session_state.user_name}, happy {day}!<br>
                <span style='font-size:22px; color:#7b6df1;'>Hope you're having a gentle {part} 🌿</span>
            </h2>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("### 👋 Hi! Enter your name to begin 🌿")

    # --- Streak display (if any history) ---
    streak = compute_streak_days()
    if streak > 0:
        st.markdown(f"**🔥 Check-in streak:** {streak} day{'s' if streak != 1 else ''}")

    # --- Mood selection ---
    st.header("How are you feeling right now?")

    mood = st.radio(
        "Pick the option that best fits you:",
        ["😊 Good", "😐 Okay", "😫 Stressed", "😞 Overwhelmed", "😴 Tired"]
    )

    if st.button("Log how I feel"):
        date_str = datetime.date.today().isoformat()
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        score = MOOD_SCORES[mood]
        st.session_state.mood_log.append((date_str, time_now, mood, score))
        st.success(f"Logged your mood: **{mood}** at {time_now} 💜")

        # recompute streak
        streak = compute_streak_days()
        st.info(f"🔥 You’ve checked in {streak} day{'s' if streak != 1 else ''} in a row.")

        # motivational quote
        quote_choices = MOOD_QUOTES.get(mood, [])
        if quote_choices:
            quote = random.choice(quote_choices)
            pastel_box(f"**Note to you:** {quote}")

    st.markdown("---")

    # =====================================================
    # MindMinute Plan
    # =====================================================
    st.subheader("Your MindMinute Plan")
    st.write("Let’s make a quick plan to help you feel better 💜")

    need = st.selectbox(
        "What do you feel you need most right now?",
        [
            "I want to calm down",
            "My thoughts are racing",
            "My body feels tense",
            "I feel kind of low / overwhelmed",
            "I just want a quick reset"
        ]
    )

    if "show_plan" not in st.session_state:
        st.session_state.show_plan = False

    if st.button("Get my 1-minute plan 💫"):
        st.session_state.show_plan = True

    def plan_step(text, btn, key, target):
        pastel_box(text)
        if st.button(btn, key=key):
            go_to(target)

    if st.session_state.show_plan:
        pastel_box("### 🌈 Your personalized MindMinute Plan is ready! 💗")

        if mood in ["😫 Stressed", "😞 Overwhelmed"]:
            if "calm" in need.lower():
                plan_step("🫁 **60 sec Breathing**", "Go to Breathing", "plan1", "Breathing")
                plan_step("🧠 **60 sec Brain Dump**", "Go to Brain Dump", "plan2", "Brain Dump")
                plan_step("💪 **30 sec Body Reset**", "Go to Body Reset", "plan3", "Body Reset")

            elif "thoughts" in need.lower():
                plan_step("🧠 Brain Dump – 60–90 sec", "Go to Brain Dump", "plan4", "Brain Dump")
                plan_step("🫁 Breathing – 30 sec", "Go to Breathing", "plan5", "Breathing")

            elif "body" in need.lower():
                plan_step("💪 Body Reset – 60 sec", "Go to Body Reset", "plan6", "Body Reset")
                plan_step("🫁 Breathing – 30 sec", "Go to Breathing", "plan7", "Breathing")

        elif mood == "😴 Tired":
            plan_step("💪 Body Reset – 60 sec", "Go to Body Reset", "plan8", "Body Reset")
            plan_step("🫁 Breathing – 30 sec", "Go to Breathing", "plan9", "Breathing")

        elif mood == "😊 Good":
            plan_step("🧠 Brain Dump", "Go to Brain Dump", "plan10", "Brain Dump")
            plan_step("🫁 Short Breathing", "Go to Breathing", "plan11", "Breathing")

        else:  # 😐 Okay
            plan_step("🫁 Breathing – 30–60 sec", "Go to Breathing", "plan12", "Breathing")
            plan_step("🧠 Optional Brain Dump", "Go to Brain Dump", "plan13", "Brain Dump")

    # --- SOS button on Home ---
    st.markdown("---")
    st.markdown("### Need urgent support?")
    sos_col = st.container()
    with sos_col:
        if st.button("I'm panicking — help me now ⚠️", key="sos_home"):
            go_to("SOS")

    # --- Mood history chart ---
    if st.session_state.mood_log:
        st.markdown("---")
        st.subheader("Mood History (this session)")
        scores = [entry[-1] for entry in st.session_state.mood_log]
        st.line_chart({"Mood Score": scores})


# =========================================================
# BREATHING PAGE
# =========================================================
elif page == "Breathing":
    back_to_home()
    st.header("🫁 Guided Breathing")

    length = st.selectbox(
        "Choose session length:",
        ["30 seconds", "60 seconds", "90 seconds"], index=1
    )
    total = int(length.split()[0])

    pastel_box("""
    ### 🌬 Breathing Cycle  
    - **Inhale** — 4 seconds  
    - **Hold** — 4 seconds  
    - **Exhale** — 6 seconds  
    """)

    phrases = [
        "You're doing amazing 💛",
        "Inhale calm, exhale tension…",
        "Let your shoulders soften 🌿",
        "You’re safe right now",
        "This moment is for you ✨"
    ]

    if st.button(f"Start {length}"):
        st.markdown("---")
        phase = st.empty()
        sub = st.empty()
        prog = st.progress(0)
        aff = st.empty()

        cycle = [("Inhale…", 4), ("Hold…", 4), ("Exhale…", 6)]
        cycle_len = sum(d for _, d in cycle)

        for sec in range(total):
            pos = sec % cycle_len
            elapsed = 0
            for name, dur in cycle:
                if pos < elapsed + dur:
                    phase.write(f"## {name}")
                    sub.write(f"{(elapsed + dur) - pos} sec left")
                    break
                elapsed += dur

            aff.caption(phrases[sec % len(phrases)])
            prog.progress((sec + 1) / total)
            time.sleep(1)

        st.success("Session complete 💜")


# =========================================================
# BRAIN DUMP PAGE
# =========================================================
elif page == "Brain Dump":
    back_to_home()
    st.header("🧠 Brain Dump")

    length = st.selectbox(
        "How long do you want to write?",
        ["30 seconds", "60 seconds", "90 seconds"], index=1
    )
    total = int(length.split()[0])

    txt = st.text_area("Write whatever is on your mind…")

    if st.button(f"Start {length} Timer"):
        timer = st.empty()
        for sec in range(total, 0, -1):
            timer.write(f"⏳ {sec} seconds remaining")
            time.sleep(1)
        timer.empty()
        st.success("Nice job letting it out 💜")

        if txt.strip():
            pastel_box(f"### You wrote:<br>{txt}")


# =========================================================
# BODY RESET PAGE
# =========================================================
elif page == "Body Reset":
    back_to_home()
    st.header("💪 Body Reset")

    length = st.selectbox(
        "Choose routine length:",
        ["30 seconds", "60 seconds", "90 seconds"], index=1
    )
    total = int(length.split()[0])

    pastel_box("""
    ### Recommended Routine  
    - 0–10 sec: Shoulder rolls  
    - 10–20 sec: Head tilts  
    - 20–30 sec: Arm stretch overhead  
    - 30–45 sec: Open chest stretch  
    - 45–60 sec: Neck circles  
    """)

    if st.button(f"Start {length} Routine"):
        prog = st.progress(0)
        txt = st.empty()

        for sec in range(total):
            txt.write(f"⏳ {sec+1}/{total} seconds")
            prog.progress((sec+1)/total)
            time.sleep(1)

        st.success("Body reset complete 🌸")


# =========================================================
# GROUNDING PAGE (5-4-3-2-1)
# =========================================================
elif page == "Grounding":
    back_to_home()
    st.header("🌍 Grounding Exercise (5-4-3-2-1)")

    pastel_box("""
    This quick exercise helps pull you out of spiraling thoughts and back into the present moment.
    """)

    steps = [
        ("5 things you can see", "Look around and notice five things you can see in your environment."),
        ("4 things you can feel", "Notice four things you can physically feel (your chair, your clothes, the floor, etc.)."),
        ("3 things you can hear", "Listen for three different sounds, near or far."),
        ("2 things you can smell", "Notice two scents around you. If you can't smell anything, think of two smells you enjoy."),
        ("1 thing you can taste", "Focus on one thing you can taste right now, or recall a taste you love."),
    ]

    for title, desc in steps:
        with st.expander(title):
            st.write(desc)

    st.info("You can come back to this tool anytime your thoughts feel chaotic or disconnected.")


# =========================================================
# SOS MODE PAGE
# =========================================================
elif page == "SOS":
    back_to_home()
    st.header("🚨 SOS Mode: Panic Support")

    pastel_box("""
    If your heart is racing or your thoughts feel out of control, you're not alone.  
    Let's take this one tiny step at a time.
    """)

    # Quick emergency breathing
    st.subheader("1. 30-second Breathing Reset")
    if st.button("Start 30-second calm breathing"):
        prog = st.progress(0)
        msg = st.empty()

        for sec in range(30):
            if sec % 6 < 3:
                msg.write("**Inhale slowly…**")
            else:
                msg.write("**Exhale gently…**")
            prog.progress((sec + 1) / 30)
            time.sleep(1)

        st.success("Nice job. Your body got a tiny reset. 💜")

    # 5-4-3-2-1 right here
    st.subheader("2. Ground yourself (5-4-3-2-1)")
    pastel_box("""
    - **5** things you can see  
    - **4** things you can feel  
    - **3** things you can hear  
    - **2** things you can smell  
    - **1** thing you can taste  
    """)

    st.write("You can also use the full **Grounding** tool from the sidebar whenever you need it.")

    st.subheader("3. Next gentle step")
    st.write("Text a friend, drink some water, or take a short walk. You do **not** have to solve everything right now.")


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div style='text-align:center; color:#9a8cff; margin-top:40px;'>
        made with 💜 for your wellbeing • MindMinute
    </div>
    """,
    unsafe_allow_html=True
)
