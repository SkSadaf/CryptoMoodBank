# 

from flask import Flask, request, jsonify , render_template
import random

app = Flask(__name__)

@app.route('/mood')
def mood():
   return render_template("mood.html", data = "")

# Data storage (in memory for simplicity)
moods = []
rewards = []
days_in_month = 30

# Function to generate random coin rewards
def generate_random_rewards():
    return random.randint(5, 20)

# API to submit mood
@app.route('/submit_mood', methods=['POST'])
def submit_mood():
    global moods
    mood = request.json.get('mood')
    if mood not in ["happy", "sad", "neutral"]:
        return jsonify({"error": "Invalid mood"}), 400

    if len(moods) < days_in_month:
        moods.append(mood)
        if len(moods) % 7 == 0 or len(moods) == days_in_month:
            return jsonify({"message": "Mood added, stats updated!", "updateStats": True}), 200
        return jsonify({"message": "Mood added!"}), 200
    return jsonify({"error": "Mood tracking complete for the month"}), 400

# API to get stats
@app.route('/get_stats', methods=['GET'])
def get_stats():
    global moods, rewards
    weekly_rewards = []
    mood_counts = {"happy": 0, "sad": 0, "neutral": 0}
    stats = {"weekly": [], "monthly": {}, "total_rewards": 0}

    for i, mood in enumerate(moods):
        mood_counts[mood] += 1

        if (i + 1) % 7 == 0 or i + 1 == len(moods):
            week_number = len(stats["weekly"]) + 1
            reward = generate_random_rewards()
            weekly_rewards.append(reward)

            stats["weekly"].append({
                "week": week_number,
                "happy": mood_counts["happy"],
                "sad": mood_counts["sad"],
                "neutral": mood_counts["neutral"],
                "reward": reward
            })
            mood_counts = {"happy": 0, "sad": 0, "neutral": 0}

    # Monthly stats
    for mood in moods:
        stats["monthly"][mood] = stats["monthly"].get(mood, 0) + 1

    stats["total_rewards"] = sum(weekly_rewards)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
