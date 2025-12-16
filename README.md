# Cyrus Chua - Portfolio Website Source

This repository contains the **source code** (Python/Flask) for [secrng.github.io](https://secrng.github.io/).

## 🚧 Project Structure

| Branch | Content | Purpose |
|box|box|box|
| **`main`** | Python, Flask, Jinja2 | **Source Code**. Edit files here. |
| **`gh-pages`** | HTML, CSS, JS | **Deployed Website**. Do not edit manually. |

## 🛠 How to Edit
1.  Modify `data.py` or `templates/`.
2.  Push to `main`.
3.  **GitHub Actions** will automatically build the site and push it to `gh-pages`.

## ⚠️ Troubleshooting "404 Not Found"
If your site is not loading, check your **GitHub Settings**:
1.  Go to **Settings > Pages**.
2.  Ensure **Source** is `Deploy from a branch`.
3.  Ensure **Branch** is **`gh-pages`** (NOT `main`).
