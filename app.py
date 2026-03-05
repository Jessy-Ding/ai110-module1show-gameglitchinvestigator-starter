import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. All bugs fixed! ✅")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 11,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Initialize session state variables if they don't exist
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 50  # Start at 50
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []
if "current_hint" not in st.session_state:
    st.session_state.current_hint = ""

# Regenerate secret if difficulty changes
if st.session_state.current_difficulty != difficulty:
    st.session_state.current_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 50  # Reset to 50
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.current_hint = ""

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

# Display current hint after debug panel
if st.session_state.current_hint:
    st.warning(st.session_state.current_hint)

with st.form(key="guess_form", clear_on_submit=True):
    raw_guess = st.text_input(
        "Enter your guess:",
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 50  # Reset to 50
    st.session_state.current_hint = ""
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        st.error(
            f"Game over! Out of attempts! "
            f"The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    st.stop()


if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
        # Don't rerun immediately so error message is visible
    else:
        # Increment attempts immediately for valid guesses
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # Store hint for display after rerun
        if show_hint:
            st.session_state.current_hint = message
        else:
            st.session_state.current_hint = ""

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.current_hint = ""  # Clear hint on win
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.current_hint = ""  # Clear hint on loss
        
        # Rerun only for valid guesses to update counters
        st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
