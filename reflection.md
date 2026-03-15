# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

Answer: 
- I cannot start a new game by clicking the new game button because I cannot submit the newly entered number.
  - Expected: I should be able to restart the game guessing circle.

- When I try to change the difficulty level on the website, nothing changes on the Developer Debug Info panel.
  - Expected: The panel should reflect the changes with fewer allowed guesses and a harder secret number (like using binary guesses to determine the optimal number of guesses for the secret number).

- Even when I enter a numbers outside the range of 1 to 100, it still gives me the same higher or lower hint.
  - Expected: It should show a warning of unexpected guess: Out of range!

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). 
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Answer: 
- Claude Sonnet 4.5-4.6

- One correct example by AI: When I reported that out-of-range numbers were still getting "go higher/lower" hints instead of an error, AI suggested adding range validation inside `parse_guess()` — specifically, checking whether the parsed integer falls within `[low, high]` and returning `ok=False` with an error message if not. This suggestion was correct. I verified it by asking AI to generate tests for valid, out-of-range, and non-numeric inputs, running them through the TDD cycle until all passed, and then manually testing the live app with edge cases like `0`, `150`, and `abc` to confirm the correct error messages appeared.

- One misleading suggestion by AI: When I asked AI to fix the broken scoring system, it repeatedly proposed different formulas — first an odd/even penalty system, then a pure countdown, then a difficulty-scaled version — each time missing one of my requirements: scores must stay in 0–100, wrong guesses should be visible during the game, winning must always reward more than losing, and faster wins should score higher. This was misleading because each proposal looked reasonable in isolation but broke another constraint I had stated earlier, costing nearly half an hour of back-and-forth. I verified each version by writing TDD tests that checked the score after wrong guesses, wins at different attempt counts, and the 0/100 floor/ceiling, then manually playing the game to feel whether the score feedback made intuitive sense as a player.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

Answer: I first took the TDD cycle to test and refractor my code and manually checked the results and played the game myself to see if the result is what I want.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

Answer: `test_decimal_input_is_accepted()` is used to test if the decimal number can be trimmed to the integer number. And it goes well with the current code design. 

- Did AI help you design or understand any tests? How?

Answer: I will first try to explain to AI what I want from the functions in the code. Then, I will ask AI to give me tests for wrong, right, and edge cases on the specific functions. After that, I will check if the testing achieved what I expected from the code. Finally, I used TDD to ensure all tests pass.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.

Answer: In the original app, the secret number was generated with random.randint() directly in the script, outside of session state. Streamlit reruns the script on every interaction—like clicking a button or changing options—causing random.randint() to generate a new number each time, so the secret changed with every interaction.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Answer: Imagine Streamlit as a whiteboard erased and redrawn every time you interact — a full 'rerun.' Variables reset, like a fresh app. However, st.session_state acts like a sticky note that survives erasures, storing values like scores or attempts. Instead of resetting variables each rerun, you store them in st.session_state to retain their values.

- What change did you make that finally gave the game a stable secret number?

Answer: The fix was moving random.randint() inside a session state guard, making the number generate only on the first run. Subsequent reruns skip it since “secret” exists in st.session_state. 

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Answer: I think understanding what I want from the app with concrete protocols of MVC and UML is important(like the job of a project manager). It makes AI understand what I want to achieve in the product app, instead of constantly checking if AI understand my ideas in each short prompt. 

- What is one thing you would do differently next time you work with AI on a coding task?

Answer: I would use the current app and list all the malfunctions I believe need fixing. Then, I would check with AI why it doesn't work the way I want. Next, I would ask AI to generate all the wrong, right, and edge cases for each function, and go through the TDD cycle to build, test, and refactor them. If the project is really complicated, I will ask AI to generate a walkthrough of the current project design and draw me a flowchart before initiating my work.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

Answer: Well, I used to think AI was so clever that it could generate the best solutions for a simple project like this. But when I actually deal with messy code, it takes way more hours and tweaks to get the app I want. I can't believe how forgettable and narrow-minded AI has been until now! I definitely need to be more careful and strategic in learning to collaborate with AI in the future.

