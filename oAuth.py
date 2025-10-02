from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates  # Optional for simple UI
from starlette.exceptions import HTTPException
import httpx
import os
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

app = FastAPI(title="eShopCo OAuth")

# Session middleware (stores id_token securely)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY"))

templates = Jinja2Templates(directory="templates")  # Create if needed

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# REDIRECT_URI = "https://your-codespace-8000.app.github.dev/auth/callback"  # Update with actual
REDIRECT_URI = "http://127.0.0.1:8000/auth/callback"  # Update with actual
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

# Root: Redirect unauth to Google login
@app.get("/")
async def root(request: Request):
    if "id_token" not in request.session:
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
        }
        auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
        return RedirectResponse(url=auth_url)
        return RedirectResponse(url=auth_url)
    return {"message": "Authenticated! Check /id_token."}

# Callback: Exchange code for tokens, store id_token
@app.get("/auth/callback")
async def callback(request: Request, code: str):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")
    
    # Exchange code for tokens
    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_URL, data=token_data)
        tokens = response.json()
    
    if "id_token" not in tokens:
        raise HTTPException(status_code=400, detail="Failed to get id_token")
    
    # Store in session
    request.session["id_token"] = tokens["id_token"]
    # Redirect to root or success
    return RedirectResponse(url="/")

# Expose raw id_token
@app.get("/id_token")
async def get_id_token(request: Request):
    id_token = request.session.get("id_token")
    if not id_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return JSONResponse(content={"id_token": id_token})