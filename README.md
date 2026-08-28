# 🌿 green-squares-bot

> **A GitHub Actions bot that automatically commits every day to keep a contribution graph active.**

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Daily%20Activity%20Bot-brightgreen?logo=github)
![Volume](https://img.shields.io/badge/commits-20--40%20per%20day-1f883d)
![License](https://img.shields.io/badge/license-MIT-blue)

**📊 Live dashboard:** https://green-squares-bot-niranjan266s-projects.vercel.app

---

## 💡 What is this?

`green-squares-bot` is an automation demo by **Niranjan** ([@Niranjan266](https://github.com/Niranjan266)) that
generates a steady stream of commits on a schedule using **GitHub Actions**.

It's a hands-on way to explore scheduled workflows (CRON), Git automation inside CI, persisted
state between runs, and a static dashboard deployed on Vercel.

---

## ✨ Features

- 📅 **Commits every single day** — no skipped days.
- 🔢 **20–40 commits per day**, with the exact target randomized once per day.
- 🕒 **Three runs daily**, each doing its share of that day's target.
- 🧠 **Randomized messages and quotes** drawn from a 30-entry pool each.
- 🗂️ **Persistent state** in `.commit_tracker.json` so the three runs cooperate.
- 📜 **Full audit trail** in `commit_log.txt`.
- 📊 **Live Vercel dashboard** with a contribution heatmap, streak, and daily stats.

---

## ⚙️ How it works

A scheduled workflow (`.github/workflows/activity.yml`) runs `commit.py` three times a day:

| Slot | UTC | IST | Share of daily target |
|------|-----|-----|----------------------|
| 🌅 Morning | `06:00` | 11:30 AM | first 35% |
| 🌞 Afternoon | `12:00` | 5:30 PM | up to 70% |
| 🌙 Evening | `15:45` | 9:15 PM | remaining 100% |

On the first run of each day the script picks a target of **20–40** commits and stores it in
`.commit_tracker.json`. Each later run reads that same target and commits only the difference
between what's already done and what the current slot should have reached — so the day always
lands **exactly** on its target, and a missed run is automatically caught up by the next one.

Every commit appends a timestamped quote to one of three rotating files, then commits it with a
randomly chosen message.

### Example

For a daily target of `33`, the three runs commit `12`, `11`, and `10` times respectively.

---

## 🔧 File structure

```
green-squares-bot/
├── commit.py                    # Commit generator (stdlib only)
├── .commit_tracker.json         # Per-day counts + per-day targets
├── daily_log.txt                # Rotating target file
├── progress.md                  # Rotating target file
├── inspiration.txt              # Rotating target file
├── commit_log.txt               # Audit trail of every run
├── web/
│   └── index.html               # Vercel dashboard (live stats)
└── .github/
    └── workflows/
        └── activity.yml         # Scheduled workflow
```

---

## 🚀 Running it yourself

```bash
git clone https://github.com/Niranjan266/green-squares-bot.git
cd green-squares-bot
python3 commit.py     # requires Python 3.9+ — no external dependencies
```

To run it on your own account, change the Git identity in `.github/workflows/activity.yml`
to your own name and GitHub noreply email, and make sure the repository is **public** so
commits appear on your profile graph.

> **Note:** the workflow needs `permissions: contents: write` to push — this is already set.
> Without it, `GITHUB_TOKEN` is read-only on new repositories and the push step fails with a 403.

---

## 📊 The dashboard

The Vercel page reads `.commit_tracker.json` **directly from the `main` branch** at runtime, so
it always shows current data without needing a rebuild. This is deliberate: the deployment is
intentionally *not* linked to the Git repository, because 20–40 commits a day would otherwise
trigger 20–40 Vercel builds a day.

To redeploy after changing the page:

```bash
npx vercel deploy web --prod
```

---

## ⚠️ Disclaimer

> **This project is for educational and demonstration purposes only.**

It exists to demonstrate GitHub Actions, CRON scheduling, and CI-driven Git automation.

Be aware of what this actually does: it produces commits that contain no real work. A
contribution graph filled this way does not represent engineering activity, and anyone who
clicks into the commits sees quote-appending diffs immediately. Treat it as a visible automation
demo — not as a portfolio signal.

---

## 📄 License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Niranjan.
