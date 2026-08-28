"""
green-squares-bot — daily activity generator
Author: Niranjan (github.com/Niranjan266)

Makes 20-40 commits every day, split across three scheduled runs.
The daily target is chosen once per day and stored in .commit_tracker.json,
so the three runs cooperate instead of each guessing independently.
"""

import os
import random
import datetime
import subprocess
import json
from zoneinfo import ZoneInfo  # stdlib timezone support (Python 3.9+)

AUTHOR = "Niranjan"

# 🌿 Inspirational quotes
quotes = [
    "Push yourself, because no one else is going to do it for you.",
    "Success is the sum of small efforts, repeated.",
    "Small steps every day.",
    "One more brick in the wall of progress.",
    "Consistency is more important than intensity.",
    "Another line, another win!",
    "Stay curious, keep learning.",
    "Another commit to greatness.",
    "Progress, not perfection.",
    "Just showing up matters.",
    "Every commit counts toward greatness.",
    "Build something you're proud of.",
    "Bit by bit, you create the masterpiece.",
    "The habit of showing up wins the game.",
    "Don't break the streak — commit today!",
    "From bugs to brilliance — keep coding!",
    "It's not about perfection. It's about progress.",
    "You're one step closer to your goal.",
    "Keep calm and commit on.",
    "Even a tiny push moves the needle.",
    "Discipline beats motivation on the hard days.",
    "Ship it, then make it better.",
    "The best time to start was yesterday. The second best is now.",
    "Compounding works on habits too.",
    "Done is better than perfect.",
    "Read the error message. Then read it again.",
    "Simplicity is the ultimate sophistication.",
    "Write code you'd be happy to debug at 3am.",
    "Momentum is built, not found.",
    "Today's effort is tomorrow's foundation.",
]

# 🌈 Commit messages
commit_messages = [
    "🚀 Boosting productivity with code magic!",
    "🌈 Painting the contribution graph today",
    "💡 A bright idea strikes again!",
    "🧠 Just thinking in Python",
    "🔥 Staying consistent is key",
    "🤖 One more commit for the bot!",
    "📚 Learning something new today",
    "📝 Daily dose of code",
    "📊 Keeping the graph alive",
    "✨ One step at a time",
    "🎯 Another mark on the roadmap",
    "✅ Small win for the day",
    "📦 Packaging progress, one file at a time",
    "🔧 Tweaked, tuned, and tightened",
    "🧪 Experimented with improvements",
    "🎉 Progress never looked better",
    "💭 Thoughts turned into code",
    "🛠️ Building habits, one commit at a time",
    "📈 Slow and steady climb",
    "🚧 Another brick in the dev wall",
    "🌱 Growing the streak",
    "⚡ Quick iteration, steady gains",
    "🧹 Housekeeping and small refinements",
    "🔍 Reviewed and refined",
    "📌 Noting today's progress",
    "🗂️ Organized a little more",
    "🎨 Polishing the details",
    "⏳ Time invested, not spent",
    "🏗️ Laying more groundwork",
    "🧭 Staying on course",
]

target_files = ["daily_log.txt", "progress.md", "inspiration.txt"]

# ── Daily volume ─────────────────────────────────────────────
MIN_DAILY = 20
MAX_DAILY = 40

# How much of the daily target should be done by the end of each slot.
# Three scheduled runs: morning, afternoon, evening.
SLOT_CUMULATIVE = [0.35, 0.70, 1.00]

# ── Time setup ───────────────────────────────────────────────
ist = ZoneInfo("Asia/Kolkata")
now = datetime.datetime.now(ist)
date_key = now.strftime("%Y-%m-%d")

counter_file = ".commit_tracker.json"

# Load or initialize tracking
if os.path.exists(counter_file):
    with open(counter_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
else:
    data = {}

# ── Pick today's target once, then reuse it for every run today ──
targets = data.get("daily_targets", {})
if date_key not in targets:
    targets[date_key] = random.randint(MIN_DAILY, MAX_DAILY)
    data["daily_targets"] = targets

daily_target = targets[date_key]

# ── Work out how many commits this run owes ──────────────────
hour = now.hour
if hour < 14:
    slot = 0
elif hour < 20:
    slot = 1
else:
    slot = 2

done = data.get(date_key, 0)
goal_by_now = round(daily_target * SLOT_CUMULATIVE[slot])
slot_commit = max(0, min(goal_by_now, daily_target) - done)

print(f"📅 {date_key} | slot {slot + 1}/3 | target {daily_target} | done {done} | this run {slot_commit}")

if slot_commit <= 0:
    print("✅ Already caught up for this slot. Nothing to do.")
    # Still persist the target so later runs agree on it.
    with open(counter_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    raise SystemExit(0)

log_entries = []

# ── Do the commits ───────────────────────────────────────────
for _ in range(slot_commit):
    quote = random.choice(quotes)
    message = random.choice(commit_messages)
    filename = random.choice(target_files)
    timestamp = datetime.datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {quote}\n")

    subprocess.run(["git", "add", filename])
    subprocess.run(["git", "commit", "-m", message])
    log_entries.append(f"[{timestamp}] - {message}")

# ── Update tracking ──────────────────────────────────────────
data[date_key] = done + slot_commit
data["daily_targets"] = targets
with open(counter_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=1)

# ── Log ──────────────────────────────────────────────────────
run_stamp = datetime.datetime.now(ist).strftime("%Y-%m-%d %I:%M:%S %p")
with open("commit_log.txt", "a", encoding="utf-8") as log:
    log.write(f"[{run_stamp}] +{slot_commit} commit(s)\n")
    log.write("\n".join(log_entries) + "\n\n")

print(f"✅ {slot_commit} commit(s) made at {run_stamp}. Total today: {data[date_key]}/{daily_target}")
