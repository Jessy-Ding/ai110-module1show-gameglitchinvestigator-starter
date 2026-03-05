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


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Improved scoring system:
    - Start with 50 points
    - Wrong guesses deduct 5 points (minimum 0)
    - Win bonus based on remaining attempts
    """
    if outcome == "Win":
        # Win bonus: base 50 points + remaining attempts × 15 points
        # Assumes Normal difficulty for simplicity (8 attempts total)
        remaining = 8 - attempt_number
        win_bonus = 50 + remaining * 15
        return current_score + win_bonus

    # Wrong guesses uniformly deduct 5 points, no distinction between Too High/Too Low
    if outcome in ["Too High", "Too Low"]:
        new_score = current_score - 5
        return max(0, new_score)

    return current_score
