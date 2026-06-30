import streamlit as st
import instaloader
import re
import os

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Instagram Reel View Counter", page_icon="📊", layout="centered")

# --- CUSTOM PREMIUM CSS & FONTS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Font Overrides */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Background Theme */
    .stApp {
        background: linear-gradient(135deg, #0f081d 0%, #150b28 50%, #08040f 100%);
        color: #f3effa;
    }
    
    /* Header Gradient Text */
    .header-container {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .header-title {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .header-subtitle {
        color: #bfaed6;
        font-weight: 300;
        font-size: 1.15rem;
        margin-bottom: 30px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 26px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-bottom: 25px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
        transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(220, 39, 67, 0.35);
    }
    
    /* Status Badge styling */
    .status-badge-container {
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .status-active {
        background: rgba(46, 213, 115, 0.12);
        color: #2ed573;
        border: 1px solid rgba(46, 213, 115, 0.25);
    }
    
    .status-inactive {
        background: rgba(255, 71, 87, 0.12);
        color: #ff4757;
        border: 1px solid rgba(255, 71, 87, 0.25);
    }
    
    .status-dot {
        height: 8px;
        width: 8px;
        border-radius: 50px;
        margin-right: 8px;
        display: inline-block;
    }
    
    .status-active .status-dot {
        background-color: #2ed573;
        box-shadow: 0 0 8px #2ed573;
    }
    
    .status-inactive .status-dot {
        background-color: #ff4757;
        box-shadow: 0 0 8px #ff4757;
    }
    
    /* Metrics Layout styling */
    .metrics-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 15px;
    }
    
    .metric-box {
        flex: 1;
        min-width: 200px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff8a00, #e52d27);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 5px;
        margin-bottom: 0px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #bfaed6;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Input Form aesthetics */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        padding: 4px 8px !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #dc2743 !important;
        box-shadow: 0 0 10px rgba(220, 39, 67, 0.25) !important;
        background-color: rgba(255, 255, 255, 0.07) !important;
    }
    
    /* Buttons Customization */
    button[kind="primary"] {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 12px 30px !important;
        border-radius: 12px !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 20px rgba(220, 39, 67, 0.35) !important;
        width: 100% !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(220, 39, 67, 0.55) !important;
    }
    
    /* Footer details */
    .footer-text {
        text-align: center;
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.25);
        margin-top: 60px;
        padding: 20px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER TITLE ---
st.markdown("""
<div class="header-container">
    <div class="header-title">Instagram Reel View Counter</div>
    <div class="header-subtitle">Instantly scrape precise, real-time Reel play counts bypassed securely.</div>
</div>
""", unsafe_allow_html=True)

# --- CONFIGURATION & SESSION LOADING ---
SESSION_USERNAME = "dino0112233"
SESSION_FILE = f"session-{SESSION_USERNAME}"

@st.cache_resource(show_spinner=False)
def load_global_session():
    instance = instaloader.Instaloader()
    if os.path.exists(SESSION_FILE):
        try:
            # Load the trusted session file directly from the repo root
            instance.load_session_from_file(SESSION_USERNAME, filename=SESSION_FILE)
            return True, instance, f"Background Scraping Active (@{SESSION_USERNAME})"
        except Exception as e:
            return False, instance, f"Session File Error: {str(e)}"
    else:
        return False, instance, "Running in Unauthenticated Guest Mode"

# Connect to the pre-authenticated session
with st.spinner("Initializing scraping session..."):
    success, L, message = load_global_session()

# --- DISPLAY AUTHENTICATION STATUS ---
if success:
    st.markdown(f"""
    <div class="status-badge-container">
        <div class="status-badge status-active">
            <span class="status-dot"></span>
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="status-badge-container">
        <div class="status-badge status-inactive">
            <span class="status-dot"></span>
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- STEP 2: REEL SCANNER INTERFACE ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔗 Paste Reel Link")
reel_url = st.text_input("Instagram Reel Link:", placeholder="https://www.instagram.com/reel/...", label_visibility="collapsed")

def extract_shortcode(url):
    pattern = r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel)/([^/?#&]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_reel_views(instance, shortcode):
    try:
        # Fetch post data
        try:
            post = instaloader.Post.from_shortcode(instance.context, shortcode)
        except Exception as fetch_err:
            post = None
            error_log = str(fetch_err)
        
        # CRITICAL FIX: Safe check to prevent the 'NoneType' crash completely
        if post is None:
            return {
                "success": False,
                "error": "Instagram returned an empty response or threw an exception during fetch.",
                "is_expired": True
            }
            
        # 1. Start with the default legacy view count fallback
        plays = post.video_view_count 
        
        # 2. Try the built-in property (Added in newer Instaloader updates)
        if hasattr(post, 'video_play_count') and post.video_play_count:
            plays = post.video_play_count
        
        # 3. Aggressively search the internal dictionary structure for 'play_count'
        try:
            if hasattr(post, '_iphone_struct') and post._iphone_struct:
                struct = post._iphone_struct
                if isinstance(struct, dict):
                    # Check directly in the root of the structure
                    if 'play_count' in struct and struct['play_count']:
                        plays = struct['play_count']
                    elif 'video_play_count' in struct and struct['video_play_count']:
                        plays = struct['video_play_count']
                    # Check inside the media/video node if nested
                    elif 'video_codec' in struct or 'image_versions2' in struct:
                        plays = struct.get('play_count', plays)
        except Exception:
            pass

        # 4. Final safety validation: If Instagram gives us a 0 or None, fallback safely
        if not plays or plays == 0:
            plays = post.video_view_count

        return {
            "success": True,
            "views": plays,
            "title": post.title or post.caption[:60].replace("\n", " ") + "..." if post.caption else "No Caption",
            "owner": post.owner_username
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Action Button
if st.button("Get Play Count", type="primary"):
    if not reel_url.strip():
        st.warning("Please paste a link first.")
    else:
        with st.spinner("Scraping metrics..."):
            shortcode = extract_shortcode(reel_url)
            if not shortcode:
                st.error("Invalid Instagram URL structure. Please make sure the URL contains '/reel/SHORTCODE' or '/p/SHORTCODE'.")
            else:
                data = get_reel_views(L, shortcode)
                if data["success"]:
                    st.balloons()
                    st.markdown("""
                    <div style="margin-top:20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top:20px;">
                        <div class="metrics-grid">
                            <div class="metric-box">
                                <div class="metric-label">Actual Plays / Views</div>
                                <div class="metric-value">{:,}</div>
                            </div>
                            <div class="metric-box">
                                <div class="metric-label">Creator Account</div>
                                <div class="metric-value" style="font-size: 1.8rem; padding-top:10px;">@{}</div>
                            </div>
                        </div>
                        <div style="margin-top: 20px; background: rgba(255,255,255,0.02); border-radius:10px; padding: 15px; border-left: 3px solid #dc2743;">
                            <strong style="color: #bfaed6;">Caption:</strong> <span style="color: #f3effa;">{}</span>
                        </div>
                    </div>
                    """.format(data['views'], data['owner'], data['title']), unsafe_allow_html=True)
                else:
                    st.error("❌ Failed to fetch data from Instagram.")
                    err_msg = data.get("error", "")
                    if data.get("is_expired") or "401" in err_msg or "login" in err_msg.lower():
                        st.info("💡 **Why this happens:** Instagram is temporarily throttling requests from this server IP, or your session file has been logged out by Meta. Give it a few minutes or refresh your login file inside Antigravity.")
                    else:
                        st.caption(f"Error breakdown: {err_msg}")
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-text">
    Instagram Reel View Counter • Secure Global Session Bypass Enabled
</div>
""", unsafe_allow_html=True)
