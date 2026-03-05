def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 1000
    return 1, 100 # Default to normal range if unknown difficulty


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Unexpected guess: Out of range! Please enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"
    except TypeError:
        g = str(guess)
        s = str(secret) 
        if g == s:
            return "Win", "🎉 Correct!"
        if g > s:
            return "Too High", "📈 Go LOWER!"
        return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int, attempt_limit: int = 8):
    """
    Scoring system (0-100), scaled per difficulty:
    - Win on attempt 1: always 100 points
    - Win on last attempt: always ~10 points
    - Step size = 90 // (attempt_limit - 1)
    - During game: shows potential score if you win next attempt
    """
    step = 90 // (attempt_limit - 1)

    if outcome == "Win":
        return max(10, 100 - (attempt_number - 1) * step)

    if outcome in ["Too High", "Too Low"]:
        # Show potential score for next attempt (countdown feedback)
        return max(0, 100 - attempt_number * step)

    return current_score
