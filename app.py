import streamlit as st
import instaloader
import re
import os
import base64
import pickle

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
        transform: translateY(-3px);
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
    
    /* Expanders styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
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
    
    button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f3effa !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 8px 20px !important;
        transition: all 0.25s ease !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px) !important;
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
DEFAULT_USERNAME = st.secrets.get("IG_USERNAME", "avcreators.co")
SESSION_FILE = f"session-{DEFAULT_USERNAME}"

@st.cache_resource(show_spinner=False)
def load_global_session():
    # Priority 1: Streamlit Cloud Secrets
    if "instagram" in st.secrets:
        try:
            username = st.secrets["instagram"].get("username")
            session_str = st.secrets["instagram"].get("session_data")
            if username and session_str:
                instance = instaloader.Instaloader(max_connection_attempts=1)
                session_dict = pickle.loads(base64.b64decode(session_str.strip().encode()))
                instance.context.load_session(username, session_dict)
                
                # Verify session
                logged_in_user = instance.test_login()
                if logged_in_user:
                    return True, instance, f"Connected via Cloud Secrets (@{username})"
                else:
                    return False, None, "Session in Cloud Secrets is expired or invalid."
        except Exception as e:
            return False, None, f"Failed to load from Cloud Secrets: {str(e)}"

    # Priority 2: Local Session File
    if os.path.exists(SESSION_FILE):
        try:
            instance = instaloader.Instaloader(max_connection_attempts=1)
            instance.load_session_from_file(DEFAULT_USERNAME, filename=SESSION_FILE)
            logged_in_user = instance.test_login()
            if logged_in_user:
                return True, instance, f"Connected via Session File (@{DEFAULT_USERNAME})"
            else:
                return False, None, f"Session file '{SESSION_FILE}' is expired or invalid."
        except Exception as e:
            return False, None, f"Failed to load session file: {str(e)}"
            
    return False, None, "No active background session found."

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "loader" not in st.session_state:
    st.session_state.loader = None
if "checkpoint_username" not in st.session_state:
    st.session_state.checkpoint_username = None
if "auth_method" not in st.session_state:
    st.session_state.auth_method = None
if "explicit_logout" not in st.session_state:
    st.session_state.explicit_logout = False

# Auto-load background session if applicable
bg_msg = ""
if not st.session_state.authenticated and not st.session_state.explicit_logout and st.session_state.checkpoint_username is None:
    with st.spinner("Checking background session..."):
        bg_success, bg_result, bg_msg = load_global_session()
    if bg_success:
        st.session_state.loader = bg_result
        st.session_state.authenticated = True
        st.session_state.auth_method = "secrets" if "Secrets" in bg_msg else "file"

# --- DISPLAY AUTHENTICATION STATUS ---
if st.session_state.authenticated:
    current_user = st.session_state.loader.context.username
    st.markdown(f"""
    <div class="status-badge-container">
        <div class="status-badge status-active">
            <span class="status-dot"></span>
            Connected as @{current_user} ({st.session_state.auth_method.upper()})
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-badge-container">
        <div class="status-badge status-inactive">
            <span class="status-dot"></span>
            Background Session Offline
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- LOGIN & 2FA CONTROLS (IF NOT AUTHENTICATED) ---
if not st.session_state.authenticated:
    st.markdown("""
    <div class="glass-card">
        <h4 style="margin-top:0px; color:#ff4757; font-weight:700;">⚠️ Scraping Session Offline</h4>
        <p style="color:#bfaed6; font-size:0.95rem; margin-bottom: 0px;">
            To unlock the Reel URL scanner, log into a temporary burner Instagram account below. 
            If Instagram challenges the login, the app will request your 6-digit security code.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if a 2FA checkpoint challenge is currently pending
    if st.session_state.checkpoint_username:
        st.markdown(f"""
        <div class="glass-card" style="border-color: rgba(240, 148, 51, 0.4);">
            <h4 style="margin-top:0px; color:#f09433; font-weight:700;">📩 Verification Required</h4>
            <p style="color:#bfaed6; font-size:0.95rem;">
                Instagram sent a security code to your account (<strong>@{st.session_state.checkpoint_username}</strong>). Please check your SMS, Email, or Authenticator App.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        verification_code = st.text_input("Enter 6-Digit Verification Code", placeholder="e.g. 123456")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Verification Code", type="primary"):
                if verification_code:
                    with st.spinner("Submitting security code..."):
                        try:
                            # Send code to the waiting instaloader instance
                            st.session_state.loader.two_factor_login(verification_code.strip())
                            st.session_state.authenticated = True
                            st.session_state.auth_method = "dynamic"
                            st.session_state.checkpoint_username = None
                            st.success("🎉 Account connected successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Verification Failed: {str(e)}")
                else:
                    st.warning("Please enter the code first.")
        with col2:
            if st.button("Cancel & Reset"):
                st.session_state.checkpoint_username = None
                st.session_state.loader = None
                st.rerun()
    else:
        # Show standard username/password login fields
        with st.expander("🔑 Log In with Instagram Burner Account", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("IG Username", placeholder="e.g. my_burner_123")
            with col2:
                password = st.text_input("IG Password", type="password", placeholder="••••••••")
                
            if st.button("Connect Account", type="primary"):
                if username and password:
                    with st.spinner("Attempting secure authentication..."):
                        try:
                            loader_temp = instaloader.Instaloader()
                            loader_temp.login(username.strip(), password)
                            
                            # Success path
                            st.session_state.loader = loader_temp
                            st.session_state.authenticated = True
                            st.session_state.auth_method = "dynamic"
                            st.session_state.explicit_logout = False
                            st.success(f"✅ Temporary access unlocked as @{username}!")
                            st.rerun()
                            
                        except instaloader.exceptions.TwoFactorAuthRequiredException:
                            # 2FA triggered
                            st.session_state.loader = loader_temp
                            st.session_state.checkpoint_username = username.strip()
                            st.rerun()
                            
                        except Exception as e:
                            error_msg = str(e)
                            if "Checkpoint" in error_msg or "challenge" in error_msg:
                                # Treat checkpoint URL challenges like 2FA code challenges
                                st.session_state.loader = loader_temp
                                st.session_state.checkpoint_username = username.strip()
                                st.rerun()
                            else:
                                st.error(f"❌ Login Failed: {error_msg}")
                else:
                    st.warning("Please enter both username and password.")

# --- DISCONNECT / ADMIN EXPORT CONTROLS (IF AUTHENTICATED) ---
if st.session_state.authenticated:
    # 1. User Disconnect
    col_out1, col_out2 = st.columns([3, 1])
    with col_out2:
        if st.button("Disconnect Session", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.loader = None
            st.session_state.auth_method = None
            st.session_state.explicit_logout = True
            st.rerun()
            
    # 2. Administrator Export Tool (Only if dynamically logged in)
    if st.session_state.auth_method == "dynamic":
        with st.expander("🛠️ Administrator: Export Current Session to Secrets Vault", expanded=False):
            st.markdown(f"""
            ### 📋 Streamlit Secrets Configuration
            You are successfully authenticated as `@{current_user}`. Since you bypassed Instagram's checkpoints via this UI, you can export this verified session to your **Streamlit Secrets vault** so the app stays logged in permanently in the cloud.
            """)
            if st.button("Generate Secrets TOML Config", type="secondary"):
                try:
                    # Save the active session to a temp file
                    temp_filename = f"session-temp-{current_user}"
                    st.session_state.loader.save_session_to_file(temp_filename)
                    
                    # Read the binary data
                    with open(temp_filename, 'rb') as f:
                        session_bytes = f.read()
                    
                    # Clean up temp file
                    if os.path.exists(temp_filename):
                        os.remove(temp_filename)
                    
                    # Convert to base64
                    base64_session = base64.b64encode(session_bytes).decode('utf-8')
                    
                    secrets_toml = f"""[instagram]
username = "{current_user}"
session_data = \"\"\"
{base64_session}
\"\"\""""
                    st.success("🎉 Session exported successfully!")
                    st.code(secrets_toml, language="toml")
                except Exception as e:
                    st.error(f"Failed to export session: {e}")

# --- STEP 2: REEL SCANNER INTERFACE ---
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("🔗 Paste Reel Link")
reel_url = st.text_input("Instagram Reel Link:", placeholder="https://www.instagram.com/reel/...", disabled=not st.session_state.authenticated, label_visibility="collapsed")

def extract_shortcode(url):
    pattern = r'(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel)/([^/?#&]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_reel_views(instance, shortcode):
    try:
        post = instaloader.Post.from_shortcode(instance.context, shortcode)
        
        # 1. Start with the default legacy view count fallback
        plays = post.video_view_count 
        
        # 2. Try the built-in property (Added in newer Instaloader updates)
        if hasattr(post, 'video_play_count') and post.video_play_count:
            plays = post.video_play_count
        
        # 3. Aggressively search the internal dictionary structure for 'play_count'
        try:
            if hasattr(post, '_iphone_struct') and post._iphone_struct:
                struct = post._iphone_struct
                
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
if st.button("Get Play Count", type="primary", disabled=not st.session_state.authenticated):
    if not reel_url.strip():
        st.warning("Please paste a link first.")
    else:
        with st.spinner("Scraping metrics via active session..."):
            shortcode = extract_shortcode(reel_url)
            if not shortcode:
                st.error("Invalid Instagram URL structure. Please make sure the URL contains '/reel/SHORTCODE' or '/p/SHORTCODE'.")
            else:
                data = get_reel_views(st.session_state.loader, shortcode)
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
                    st.error("Failed to fetch data from Instagram.")
                    st.exception(data["error"])
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-text">
    Instagram Reel View Counter • Secure Cloud Session Bypass Enabled
</div>
""", unsafe_allow_html=True)
