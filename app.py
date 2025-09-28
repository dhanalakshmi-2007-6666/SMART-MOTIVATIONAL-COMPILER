from flask import Flask, render_template, request, jsonify
import requests
import random
app = Flask(__name__)
ERROR_MESSAGES = [
    "💡 Errors are proof you’re trying 🚀 Keep going!",
    "✨ Mistakes are portals to discovery 🌈 Don’t stop!",
    "🔥 Every bug you fix makes you stronger 💪",
    "🌟 Great coders are built on countless errors — you’re on the right path!",
    "🚀 Fail, learn, improve, repeat. That’s coding magic!",
    "💻 Debugging is where real programmers are born 🔥",
    "🌱 Small errors grow into big learnings 🌟",
    "🎯 You only fail when you stop trying — keep pushing!",
    "🔧 Every error is a teacher in disguise 📖",
    "🏆 Behind every successful coder is a mountain of error logs 😅",
    "⚡ The more bugs you face, the better you get 💪",
    "📚 Errors are not roadblocks — they’re stepping stones 🚀",
    "🎉 Don’t be afraid of red text, it’s guiding you!",
    "🔎 An error today is wisdom tomorrow 🌟",
    "🌈 Debugging is a journey, enjoy the process 💻",
]

SUCCESS_MESSAGES = [
    "🎉 Awesome! Try more programs and keep building 🚀",
    "💡 Success! Now challenge yourself with harder problems 🌟",
    "🔥 Great work! Keep sharpening your coding skills 💪",
    "🌈 You nailed it! Now push your limits even more ✨",
    "🌟 Bravo! Each program takes you one step closer to mastery 🚀",
    "🏆 Amazing! Keep writing code every day and you’ll shine 🌟",
    "🎯 Fantastic! The best way to learn is to practice more 💡",
    "📚 Great job! Try a new concept next 🌈",
    "💻 Super! Each success boosts your confidence 🔥",
    "🚀 You’re coding like a pro — keep experimenting!",
    "🌱 Learning never stops — keep growing your skills 🌟",
    "🎉 Wonderful! Your consistency will make you unstoppable 💪",
    "⚡ Excellent! Try solving a bigger challenge next time 💡",
    "✨ Superb work! You’re on the right track 🚀",
    "🌈 Keep coding, keep shining, keep moving forward 🌟",
]

@app.route("/")
def home():
    return render_template("frontpage.html")

@app.route("/fix-run", methods=["POST"])
def fix_run():
    data = request.get_json()
    code = data.get("code", "")
    user_input = data.get("input", "")

    url = "https://emkc.org/api/v2/piston/execute"
    payload = {
        "language": "java",
        "version": "*",
        "files": [{"name": "Main.java", "content": code}],
        "stdin": user_input
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        run_output = result.get("run", {}).get("stdout", "") + result.get("run", {}).get("stderr", "")
        if not run_output.strip():
            run_output = "⚠️ No output received from compiler."
    except Exception as e:
        run_output = f"❌ Error: {str(e)}"

    if "error" in run_output.lower() or "exception" in run_output.lower():
        motivation = random.choice(ERROR_MESSAGES)
    else:
        motivation = random.choice(SUCCESS_MESSAGES)

    return jsonify({
        "output": run_output,
        "motivation": motivation
    })

if __name__ == "__main__":
    app.run(debug=True)
