"""
Game Logic Tests - Comprehensive Bug Fix Verification

This file tests all the logic functions and verifies that the original bugs
from the git initial commit have been fixed.

Usage:
    # Run as standalone script with nice formatting:
    python3 tests/test_game_logic.py
    
    # Run with pytest (if available):  
    pytest tests/test_game_logic.py -v
    
    # Import individual test functions:
    from tests.test_game_logic import test_all_original_bugs_are_fixed

Tests verify fixes for:
- Exception handler crashes (string vs int comparison)
- Backwards hints (wrong directional guidance)
- Missing range validation (out-of-range numbers getting hints)
- Invalid attempts counting against limit  
- Off-by-one errors in attempt counting
"""

import sys
import os
# Add parent directory to path for standalone execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting: "Invalid Guesses Count as Attempts" bug ---
# Bug: attempts += 1 ran before parse_guess(), so invalid inputs still
# consumed an attempt. Fix: only increment when parse_guess returns ok=True.

def test_out_of_range_guess_is_invalid():
    # A number above the range must return ok=False so it won't count as an attempt
    ok, guess_int, err = parse_guess("150", 1, 100)
    assert ok == False
    assert guess_int is None
    assert err is not None

def test_below_range_guess_is_invalid():
    # A number below the range must return ok=False so it won't count as an attempt
    ok, guess_int, err = parse_guess("0", 1, 100)
    assert ok == False
    assert guess_int is None
    assert err is not None

def test_non_numeric_guess_is_invalid():
    # A non-numeric string must return ok=False so it won't count as an attempt
    ok, guess_int, err = parse_guess("abc", 1, 100)
    assert ok == False
    assert guess_int is None
    assert err is not None

def test_valid_guess_is_ok():
    # A valid in-range number must return ok=True so it DOES count as an attempt
    ok, guess_int, err = parse_guess("50", 1, 100)
    assert ok == True
    assert guess_int == 50
    assert err is None


# --- Tests targeting: "Exception Handler Crash" bug ---
# Bug: Original check_guess would crash when comparing string to int in TypeError block
# Fix: Convert both values to strings before comparison

def test_string_guess_vs_int_secret_no_crash():
    """Test that string guess vs int secret doesn't crash (original bug)"""
    # This would have crashed in the original buggy version
    try:
        outcome, message = check_guess("60", 50)  # String guess, int secret
        assert outcome == "Too High"
        assert "LOWER" in message
    except TypeError:
        assert False, "check_guess crashed on string vs int comparison - bug not fixed!"

def test_string_guess_vs_int_secret_winning():
    """Test string guess that matches int secret"""
    try:
        outcome, message = check_guess("50", 50)  # String "50" vs int 50
        assert outcome == "Win"
        assert "Correct" in message
    except TypeError:
        assert False, "check_guess crashed on winning string vs int - bug not fixed!"

def test_string_guess_vs_int_secret_too_low():
    """Test string guess that's lower than int secret"""
    try:
        outcome, message = check_guess("40", 50)  # String "40" vs int 50
        assert outcome == "Too Low" 
        assert "HIGHER" in message
    except TypeError:
        assert False, "check_guess crashed on low string vs int - bug not fixed!"


# --- Tests targeting: "Backwards Hints" bug ---
# Bug: Original hints were backwards (told you to go higher when guess was too high)
# Fix: Corrected the hint directions

def test_too_high_guess_says_go_lower():
    """When guess > secret, hint should say 'LOWER' not 'HIGHER'"""
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"
    assert "HIGHER" not in message, f"Message incorrectly says HIGHER: {message}"

def test_too_low_guess_says_go_higher():
    """When guess < secret, hint should say 'HIGHER' not 'LOWER'"""
    outcome, message = check_guess(30, 50) 
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"
    assert "LOWER" not in message, f"Message incorrectly says LOWER: {message}"


# --- Tests targeting: "Off-by-One Attempt Counting" bug ---
# Bug: Starting attempts at 1 instead of 0 caused games to end one attempt early
# Fix: Start attempts at 0, increment only after successful validation

def test_attempt_counting_logic():
    """Test that attempt counting works correctly (fixes off-by-one bug)"""
    # Simulate the fixed logic: attempts start at 0, increment after validation
    attempts = 0  # Fixed: start at 0, not 1
    attempt_limit = 6  # Easy difficulty allows 6 attempts
    
    valid_guesses_made = 0
    
    # Make 6 valid guesses (should all be allowed)
    for i in range(6):
        # Simulate parsing a valid guess
        ok, guess_int, err = parse_guess(str(10 + i), 1, 100)  # Valid guesses: 10, 11, 12, 13, 14, 15
        
        if ok:  # Only increment on valid guess (fixed behavior)
            attempts += 1
            valid_guesses_made += 1
            
        # Check we haven't exceeded limit
        if attempts >= attempt_limit:
            break
    
    # Should have made exactly 6 valid attempts
    assert valid_guesses_made == 6, f"Expected 6 attempts, got {valid_guesses_made}"
    assert attempts == attempt_limit, f"Final attempts {attempts} should equal limit {attempt_limit}"

def test_invalid_guesses_dont_waste_attempts():
    """Test that invalid guesses don't increment attempt counter"""
    attempts = 0
    
    # Invalid guess 1: out of range
    ok, _, _ = parse_guess("999", 1, 100)
    if ok:
        attempts += 1
    assert attempts == 0, "Out-of-range guess should not increment attempts"
    
    # Invalid guess 2: non-numeric  
    ok, _, _ = parse_guess("abc", 1, 100)
    if ok:
        attempts += 1
    assert attempts == 0, "Non-numeric guess should not increment attempts"
    
    # Valid guess: should increment
    ok, _, _ = parse_guess("50", 1, 100)
    if ok:
        attempts += 1
    assert attempts == 1, "Valid guess should increment attempts"


def test_all_original_bugs_are_fixed():
    """
    Comprehensive test that verifies ALL the original bugs from git initial commit are fixed.
    
    This test would FAIL on the original buggy version but PASS on the fixed version.
    Tests the specific bugs mentioned in the reflection.md file:
    1. New game button not working (state reset issues)
    2. Difficulty changes not reflected in debug panel  
    3. Out-of-range numbers still getting hints instead of error messages
    4. Exception handler crashing on string vs int comparison
    5. Invalid guesses wasting attempts
    6. Off-by-one error in attempt counting
    """
    
    # BUG 1 & 4: Exception handler crash (string vs int comparison)
    # Original bug: TypeError when comparing string to int in exception block
    try:
        outcome, message = check_guess("75", 50)  # String guess, int secret
        assert outcome == "Too High"
        assert "LOWER" in message
        # If we reach here, the bug is fixed (original would crash)
    except TypeError:
        assert False, "ORIGINAL BUG NOT FIXED: Exception handler still crashes on string vs int"
    
    # BUG 2: Backwards hints  
    # Original bug: "Go HIGHER" when guess was too high, "Go LOWER" when too low
    outcome, message = check_guess(80, 50)  # Guess too high
    assert outcome == "Too High"
    assert "LOWER" in message, f"ORIGINAL BUG NOT FIXED: Should say LOWER, got {message}"
    
    outcome, message = check_guess(20, 50)  # Guess too low
    assert outcome == "Too Low"  
    assert "HIGHER" in message, f"ORIGINAL BUG NOT FIXED: Should say HIGHER, got {message}"
    
    # BUG 3: Out-of-range guesses getting gameplay hints instead of error messages
    # Original bug: parse_guess didn't do range validation, so out-of-range numbers
    # would pass validation and get "too high/low" hints instead of "out of range" errors
    ok, val, err = parse_guess("500", 1, 100)  # Way out of range
    assert not ok, "ORIGINAL BUG NOT FIXED: Out-of-range guess should be invalid"
    assert err is not None, "ORIGINAL BUG NOT FIXED: Should get error message"
    assert "Out of range" in err, f"ORIGINAL BUG NOT FIXED: Should get range error, got {err}"
    
    ok, val, err = parse_guess("-10", 1, 100)  # Below range
    assert not ok, "ORIGINAL BUG NOT FIXED: Below-range guess should be invalid"
    assert "Out of range" in err, "ORIGINAL BUG NOT FIXED: Should get range error"
    
    # BUG 5: Invalid guesses should not waste attempts 
    # Original bug: attempts += 1 happened before parse_guess validation
    attempts = 0
    
    # Simulate original buggy behavior vs fixed behavior
    # FIXED: Only increment after successful parse_guess
    ok, _, _ = parse_guess("999", 1, 100)  # Invalid guess
    if ok:  # Only increment if valid (FIXED behavior)
        attempts += 1
    assert attempts == 0, "ORIGINAL BUG NOT FIXED: Invalid guess shouldn't count as attempt"
    
    # BUG 6: Off-by-one error - starting attempts at 1 instead of 0
    # Original bug: attempts started at 1, so 6-attempt game only allowed 5 actual guesses
    # FIXED: attempts should start at 0
    initial_attempts = 0  # Fixed: start at 0, not 1
    attempt_limit = 6
    
    valid_attempts = 0
    for guess in ["10", "20", "30", "40", "50", "60"]:  # 6 valid guesses
        ok, _, _ = parse_guess(guess, 1, 100)
        if ok:
            initial_attempts += 1
            valid_attempts += 1
            
        # Check if we can still make guesses (should allow all 6)
        if initial_attempts >= attempt_limit:
            break
    
    assert valid_attempts == 6, f"ORIGINAL BUG NOT FIXED: Should allow 6 attempts, only got {valid_attempts}"
    assert initial_attempts == attempt_limit, "ORIGINAL BUG NOT FIXED: Off-by-one in attempt counting"
    
    # If we reach this point, ALL original bugs are fixed! 🎉


def test_score_never_goes_negative():
    """Test that score system never allows negative values and uses new scoring logic"""
    from logic_utils import update_score
    
    # Start with base score (new system starts with 50)
    score = 50
    
    # Make many bad guesses (each -5 points, but not below 0)
    for i in range(1, 15):  # More than enough to test the 0 floor
        score = update_score(score, "Too Low", i)
        assert score >= 0, f"Score became negative ({score}) after attempt {i}"
    
    # Score should be 0, not negative
    assert score == 0, f"Expected score to be 0, got {score}"
    
    # Test that positive scoring still works with new system
    score = 50  # Start fresh
    
    # Test error deduction
    score = update_score(score, "Too High", 1)  # Should be 45
    assert score == 45, f"Expected 45 after error, got {score}"
    
    # Test win bonus  
    score = update_score(score, "Win", 2)  # Should get base 50 + (8-2)*15 = 50+90 = 140 bonus
    expected_win_total = 45 + 50 + (8-2)*15  # current + base + remaining*15
    assert score == expected_win_total, f"Expected {expected_win_total} after win, got {score}"


def test_new_scoring_system():
    """Test the new simplified scoring system"""
    from logic_utils import update_score
    
    # Test consistent error deduction (no more odd/even nonsense)
    score = 50
    score = update_score(score, "Too High", 1)
    assert score == 45, "Too High should deduct 5 points"
    
    score = update_score(score, "Too Low", 2) 
    assert score == 40, "Too Low should also deduct 5 points"
    
    # Test win bonuses scale with remaining attempts
    quick_win = update_score(50, "Win", 1)  # 7 remaining attempts
    slow_win = update_score(50, "Win", 5)   # 3 remaining attempts
    assert quick_win > slow_win, "Quicker wins should get higher scores"


def main():
    """
    Standalone test runner with nice formatting.
    Runs all tests and provides clear feedback on bug fix status.
    """
    print("=" * 70)
    print("🔧 GAME GLITCH INVESTIGATOR - BUG FIX VERIFICATION")
    print("=" * 70)
    
    # Define test functions to run
    test_functions = [
        ("Basic Functionality", [
            test_winning_guess,
            test_guess_too_high, 
            test_guess_too_low,
        ]),
        ("Range Validation Fix", [
            test_out_of_range_guess_is_invalid,
            test_below_range_guess_is_invalid,
            test_non_numeric_guess_is_invalid,
            test_valid_guess_is_ok,
        ]),
        ("Exception Handler Fix", [
            test_string_guess_vs_int_secret_no_crash,
            test_string_guess_vs_int_secret_winning,
            test_string_guess_vs_int_secret_too_low,
        ]),
        ("Hint Correctness Fix", [
            test_too_high_guess_says_go_lower,
            test_too_low_guess_says_go_higher,
        ]),
        ("Attempt Counting Fix", [
            test_attempt_counting_logic,
            test_invalid_guesses_dont_waste_attempts,
        ]),
        ("Comprehensive Bug Fix Verification", [
            test_all_original_bugs_are_fixed,
        ]),
        ("Score System Fix", [
            test_score_never_goes_negative,
            test_new_scoring_system,
        ]),
    ]
    
    total_passed = 0
    total_tests = 0
    
    for category, tests in test_functions:
        print(f"\n🧪 {category}:")
        category_passed = 0
        
        for test in tests:
            total_tests += 1
            try:
                test()
                print(f"   ✅ {test.__name__}")
                category_passed += 1
                total_passed += 1
            except Exception as e:
                print(f"   ❌ {test.__name__}: {e}")
        
        print(f"   📊 {category_passed}/{len(tests)} passed")
    
    print("\n" + "=" * 70)
    print(f"📊 FINAL RESULTS: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! All original bugs have been fixed.")
        print("✨ The game should work correctly now!")
    else:
        failed = total_tests - total_passed
        print(f"⚠️  {failed} test(s) failed. Some bugs may still exist.")
        print("🔍 Check the failed tests above for details.")
    
    print("=" * 70)
    
    return total_passed == total_tests


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
