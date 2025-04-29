# Personal News Feed Generator

Create your own customisable news feed website using simple RSS sources — automatically updated every day — hosted on GitHub Pages!

This tool is designed for **anyone with a GitHub account**, no programming required beyond basic GitHub skills.

Click here to see a sample feed: [My news feed](https://technoid99.github.io/my_news_feed/index.html)

---

# ✅ Quick Setup Summary:

| Step | Action |
|:-----|:-------|
| 1 | Click **"Use this template"** |
| 2 | Create your own repository |
| 3 | Enable **GitHub Pages** (main branch, root folder) |
| 4 | Customize your `feeds.json` |
| 5 | Enjoy your personal news feed! 🚀 |

---

## 📌 What This Project Does

- Displays the latest articles from RSS feeds you choose.
- Lets you filter by:
  - **News source**
  - **Publication time** (past 24h, 48h, 7 days, or all time)
  - **Keyword search** (supports AND, OR, and "quoted phrases")
- Automatically updates itself **every morning**.
- Hosted for free on **GitHub Pages** — no servers needed.
- You stay in control: choose your sources, update anytime.

---

## 🚀 How to Set Up Your Own News Feed

### 1. Make Your Own Copy

- Click the green **"Use this template"** button at the top of this page.
- Choose **"Create a new repository"**.
- Give your repository a name (e.g., `my_news_feed`).
- Click **Create repository**.

✅ You now have your own personal copy — no coding needed!

---

### 2. Enable GitHub Pages

- In your new repository, go to **Settings**.
- Scroll down to **Pages**.
- Under **"Source"**, select:
  - **Branch:** `main`
  - **Folder:** `/ (root)`
- Click **Save**.

✅ After a few seconds, GitHub will give you a live web link to your personal news feed!

---

### 3. Customize Your News Sources

- In your repository, open the `config.html` file.
- Click **"View raw"** (top right).
- Use the simple web form to edit, add, or remove RSS feeds.
- After making changes, **copy** the updated JSON text.
- Then:
  - Open `feeds.json`.
  - Click the ✏️ **edit button**.
  - Paste your updated feeds.json.
  - Save the changes.

✅ Now you control exactly what news you see!

---

### 4. How Updates Work

- Every morning at **6AM AEST (Australia Eastern Standard Time)**,
  GitHub Actions will automatically update your news feed.
- You don't need to do anything — it refreshes itself!

---

### 5. View Your Personal News Feed

- Visit your GitHub Pages link (found in **Settings → Pages**).
- Bookmark it for quick access!

✅ You can filter articles by:
- Source
- Time range (24h, 48h, 7d, or all time)
- Keyword search (supports **AND**, **OR**, and **"quoted phrases"**)

---

## 🛠 Requirements

- A GitHub account.

No servers.  
No coding beyond basic file editing.  
No installations.  
Just GitHub + RSS!

---

## ⚙️ How It Works (Under the Hood)

- `main.py` pulls articles from your selected RSS feeds using Python and `feedparser`.
- It generates an `index.html` page listing all articles.
- A GitHub Actions workflow (`update_feed.yml`) runs `main.py` automatically every day.
- Changes are committed back to your repository if anything new appears.
- GitHub Pages serves your latest news to the world.

---

## 💡 Tips

- Bookmark your feed and customise filters (source selection, keywords, time range) — they are saved in the URL!
- Add niche topics (e.g., science, regional news, personal interests).
- Remove or add feeds anytime by editing `feeds.json`.

---

## 📚 Need Help?

- Check the About page on your news feed site.
- Open an Issue in this repository if you get stuck.
- Explore GitHub documentation if you're completely new!

---

## 🤔 Why This Project?

Today’s news feeds are cluttered and controlled by algorithms.  
**This project lets you take back control.**  
Select only the topics and sources you trust.  
No ads. No tracking. Just the news you want, updated daily.

---

## 📝 License

Free to use, copy, modify, or redistribute.

---
