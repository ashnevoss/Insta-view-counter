# Insta-view-counter

A public Instagram Reel View/Play Counter app built with Streamlit and Instaloader.

## Features
- **Public-ready interface**: Users can provide a temporary/burner Instagram account directly in the UI to log in safely.
- **Accurate Play Count**: Fetches the exact loop/play count metric from the Reels tab using internal structures (requires login).
- **Session Caching**: Caches authentication to avoid entering password on every search.

## How to Run Locally

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit application:
   ```bash
   python3 -m streamlit run app.py
   ```

## Deploying to Streamlit Community Cloud

If you deploy this app to Streamlit Community Cloud, you can avoid logging in through the UI by adding your burner credentials to **App settings ➡️ Secrets**:
```toml
IG_USERNAME = "your_burner_username"
IG_PASSWORD = "your_secure_password"
```
