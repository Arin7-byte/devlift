import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="DevLift AI", page_icon="⚡", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.6rem; max-width: 1200px}
.hero {padding: 1.5rem 1.7rem; border-radius: 18px; background: linear-gradient(120deg,#101b35,#243d68); color:white; margin-bottom:1.2rem}
.hero h1 {font-size:2.4rem; margin:0}
.hero p {font-size:1.05rem; color:#d6e4ff; margin:.5rem 0 0}
div[data-testid="stMetric"] {border:1px solid rgba(128,128,128,.25); padding:12px; border-radius:12px}
.small {color:#7d8ba5; font-size:.9rem}
</style>
<div class="hero">
<h1>⚡ DevLift AI</h1>
<p>Your pocket tutor for understanding code, fixing bugs, and learning technology faster.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Your workspace")
    mode = st.radio("Choose a tool", ["Explain code", "Debug a problem", "Learn a concept", "Improve my code"])
    level = st.selectbox("Explanation level", ["Beginner", "Intermediate", "Advanced"])
    language = st.selectbox("Preferred language / stack", ["Python", "JavaScript", "Java", "C++", "SQL", "General"])
    st.divider()
    st.caption("AI provider")
    provider = st.selectbox("Mode", ["Auto (API if configured)", "Demo mode (no API key)"])
    st.caption("Add OPENAI_API_KEY to .env to enable live AI responses.")

def demo_answer(mode, prompt, code, level, language):
    p = (prompt or "").strip()
    c = (code or "").strip()
    if mode == "Explain code":
        if not c:
            return "## Add some code first\nPaste a snippet in the input area and I’ll walk through its purpose, important lines, and concepts."
        lines = [x for x in c.splitlines() if x.strip()]
        return f"""## Plain-English overview
This {language} snippet contains **{len(lines)} non-empty line(s)**. Read it from top to bottom and identify the inputs, transformations, and final output.

## How to understand it
1. **Find the entry point:** look for the first statement that runs, such as a function call or `main`.
2. **Track the data:** note each variable and how its value changes.
3. **Follow control flow:** inspect conditions, loops, and function calls.
4. **Check the result:** identify what is printed, returned, or modified.

## Concepts to look for
{', '.join(sorted(set(['variables'] + (['functions'] if '(' in c else []) + (['conditions'] if 'if ' in c or 'if(' in c else []) + (['loops'] if 'for ' in c or 'while ' in c else []) + (['collections'] if '[' in c or '{' in c else []))))}.

## Next step
Run the snippet with a tiny input, then change one value and predict what will happen before running it.
"""
    if mode == "Debug a problem":
        return f"""## Debugging plan
**Problem:** {p or 'No error description provided yet.'}

1. **Read the first error line carefully.** The last line often names the exception; the stack trace points to where it surfaced.
2. **Reproduce it minimally.** Keep only the code and input needed to trigger the issue.
3. **Inspect assumptions.** Check types, `None`/null values, array boundaries, imports, and file paths.
4. **Add targeted logging.** Print or inspect the values immediately before the failing line.
5. **Test the fix and a nearby edge case.**

{"### Code to inspect\\n```" + language.lower() + "\\n" + c + "\\n```" if c else "Paste the failing code to get a more specific diagnosis."}

*Demo mode gives a debugging checklist rather than claiming to have executed your code. Configure an API key for contextual AI analysis.*
"""
    if mode == "Learn a concept":
        topic = p or "the selected technology"
        return f"""## Learn: {topic}
**Simple idea:** Think of {topic} as a tool or pattern that helps a program accomplish one specific job.

### Build understanding in 3 passes
1. **Intuition:** explain the idea in one sentence without jargon.
2. **Example:** write the smallest working example you can.
3. **Transfer:** change one part of the example and predict the result.

### Quick self-check
- What problem does {topic} solve?
- When would you choose it over an alternative?
- What is one common mistake beginners make?

### 10-minute practice
Spend 3 minutes reading a minimal example, 4 minutes modifying it, and 3 minutes explaining it aloud in your own words.
"""
    return f"""## Code improvement checklist
Review your snippet for:
- **Clarity:** descriptive names and small functions.
- **Correctness:** clear handling of empty inputs and edge cases.
- **Maintainability:** avoid repeated logic; separate responsibilities.
- **Performance:** optimize only after identifying a likely bottleneck.
- **Testing:** include a normal case, a boundary case, and an invalid-input case.

{"### Your snippet\\n```" + language.lower() + "\\n" + c + "\\n```" if c else "Paste code to get a focused review."}
"""

def ask_ai(mode, prompt, code, level, language):
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if provider.startswith("Demo") or not key:
        return demo_answer(mode, prompt, code, level, language), False
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key, base_url=os.getenv("OPENAI_BASE_URL") or None)
        instructions = f"""You are DevLift AI, a careful developer tutor. Tool: {mode}. Learner level: {level}. Preferred stack: {language}.
Be practical, structured, and accurate. Explain jargon. For debugging, distinguish likely causes from certainty and propose verification steps. Never claim you executed code unless a tool actually did. Use Markdown. End with one useful next step."""
        user_content = f"Request / error / topic:\n{prompt or '(not provided)'}\n\nCode:\n{code or '(not provided)'}"
        result = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role":"system","content":instructions},{"role":"user","content":user_content}],
            temperature=0.3
        )
        return result.choices[0].message.content, True
    except Exception as e:
        return demo_answer(mode, prompt, code, level, language) + f"\n\n---\n**AI connection issue:** {e}\nShowing the offline guidance instead.", False

col1, col2 = st.columns([1.15, .85], gap="large")
with col1:
    st.subheader("What are you working on?")
    if mode == "Explain code":
        prompt = st.text_input("Optional context", placeholder="e.g. This is for my college assignment")
        code = st.text_area("Paste code", height=260, placeholder="def greet(name):\n    return f'Hello, {name}!'")
    elif mode == "Debug a problem":
        prompt = st.text_area("Describe the error and what you expected", height=110, placeholder="What happened? Include the exact error message.")
        code = st.text_area("Failing code (if available)", height=210, placeholder="Paste the smallest code snippet that reproduces it.")
    elif mode == "Learn a concept":
        prompt = st.text_input("Concept to learn", placeholder="e.g. recursion, APIs, SQL joins, neural networks")
        code = ""
    else:
        prompt = st.text_input("Goal or concern (optional)", placeholder="e.g. make this easier to maintain")
        code = st.text_area("Code to review", height=260, placeholder="Paste your code here...")
    run = st.button("✨ Help me with this", type="primary", use_container_width=True)

with col2:
    st.subheader("Your learning workspace")
    st.markdown("**Designed for understanding, not just copying answers.**")
    st.markdown("- 🧠 Plain-language explanations matched to your level")
    st.markdown("- 🐞 A repeatable debugging workflow")
    st.markdown("- 🧩 Small practice steps that reinforce learning")
    st.markdown("- 🛠️ Practical code-quality feedback")
    st.info("Tip: Include the exact error message and a minimal code sample for more useful debugging.")
    st.caption("Privacy: snippets are sent to your configured AI provider only when you request live AI mode.")

if run:
    with st.spinner("Preparing your guidance..."):
        answer, live = ask_ai(mode, prompt, code, level, language)
    st.divider()
    st.subheader("Your DevLift result")
    st.caption("Live AI response" if live else "Offline demo guidance")
    st.markdown(answer)
    st.download_button("Download this answer (.md)", answer, file_name="devlift-answer.md", mime="text/markdown")

st.divider()
a,b,c = st.columns(3)
a.metric("4", "Developer tools")
b.metric("3", "Learning levels")
c.metric("10 min", "Practice loop")
st.caption("DevLift AI • Built for the challenge: learn faster, work smarter, understand technology.")
