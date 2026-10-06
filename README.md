# FastAPI Dev Container: Student Class API & Google OAuth

Assignment work for **Tools in Data Science (IIT Madras), Graded Assignment 2**. The repository has two small **FastAPI** services and a **VS Code Dev Container** / GitHub Codespaces setup, so the environment is reproducible with a single click.

---

## ✨ What's Inside

### 1. Student Class API (`main.py`)
A REST API that loads `q-fastapi.csv` into memory at startup and serves student records.

| Endpoint | Description |
|---|---|
| `GET /api` | All students: `{"students": [{"studentId": 1, "class": "1A"}, ...]}` |
| `GET /api?class=1A&class=1B` | Students filtered by one or more classes (repeatable query param), in original CSV order |

CORS is enabled for all origins, so the API can be called from any web page.

### 2. Google OAuth 2.0 Login, "eShopCo" (`oAuth.py`)
A minimal **OpenID Connect** login flow:

| Endpoint | Description |
|---|---|
| `GET /` | Redirects unauthenticated users to Google's consent screen |
| `GET /auth/callback` | Exchanges the authorization code for tokens (via `httpx`) and stores the `id_token` in a signed session cookie |
| `GET /id_token` | Returns the raw `id_token` for the logged-in user |

---

## 🏗️ Architecture & Concepts

```
Client ──► FastAPI (main.py) ──► in-memory list ◄── q-fastapi.csv (loaded once at startup)

Browser ──► FastAPI (oAuth.py) ──► Google OAuth 2.0 (authorize) ──► /auth/callback
                    │                                                 │
                    └──── SessionMiddleware (signed cookie) ◄── id_token (token exchange)
```

**Concepts:** RESTful API design · query-parameter filtering (multi-value params with `alias`) · CORS · OAuth 2.0 Authorization Code flow · OpenID Connect `id_token` · session middleware · async HTTP (`httpx`) · environment-based secrets (`python-dotenv`) · Dev Containers / Codespaces · `uv` package manager

---

## ⚙️ Getting Started

### Option A: Dev Container / Codespaces
Open the repo in **GitHub Codespaces** or VS Code with the *Dev Containers* extension. The container installs Python and runs `uv pip install fastapi` automatically.

### Option B: Local

```bash
git clone https://github.com/God-Gamer-Manyu/ga2-56fdab-devcontainer.git
cd ga2-56fdab-devcontainer
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install "fastapi[standard]" uvicorn httpx python-dotenv itsdangerous jinja2
```

**Run the Student API**
```bash
uvicorn main:app --reload
# → http://127.0.0.1:8000/api?class=1A
```

**Run the OAuth app**: first create a `.env` file:
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
SESSION_SECRET_KEY=any-long-random-string
```
Register `http://127.0.0.1:8000/auth/callback` as an authorised redirect URI in Google Cloud Console, then:
```bash
uvicorn oAuth:app --reload
# → http://127.0.0.1:8000
```

---

## 📁 Project Structure

```
├── .devcontainer/devcontainer.json   # Dev Container definition (Python + uv)
├── main.py                           # Student Class API
├── oAuth.py                          # Google OAuth / OIDC demo
├── q-fastapi.csv                     # Student dataset
└── template/index.html               # Simple landing template
```

## 🛠️ Tech Stack

`Python` · `FastAPI` · `Uvicorn` · `Starlette Sessions` · `httpx` · `Google OAuth 2.0 / OIDC` · `Dev Containers` · `uv`

## 👤 Author

**Rtamanyu N J**, [@God-Gamer-Manyu](https://github.com/God-Gamer-Manyu)
