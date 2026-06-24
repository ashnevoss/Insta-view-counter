import streamlit as st
import instaloader
import re

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="Instagram Reel View Counter", page_icon="📊", layout="centered")

st.title("📊 Public Instagram Reel View Counter")
st.write("To get exact, real-time Reel play counts, Instagram requires a valid login session. Please provide a temporary or burner Instagram account below to run the scan.")

# --- STEP 1: USER LOGIN INTERFACE ---
st.subheader("🔑 Step 1: Submitter Authentication")

col1, col2 = st.columns(2)
with col1:
    username = st.text_input("Your IG Username", placeholder="e.g., burner_acc_123")
with col2:
    password = st.text_input("Your IG Password", type="password", placeholder="••••••••")

# Initialize and Cache the Login Session per user session
@st.cache_resource(show_spinner=False)
def login_user(user, pwd):
    if not user or not pwd:
        return False, "Please enter both username and password."
    try:
        instance = instaloader.Instaloader()
        instance.login(user, pwd)
        return True, instance
    except Exception as e:
        return False, str(e)

# Trigger authentication check
L = None
is_authenticated = False

if username and password:
    with st.spinner("Authenticating with Instagram safely..."):
        success, result = login_user(username, password)
        if success:
            L = result
            is_authenticated = True
            st.success(f"✅ Authenticated successfully as @{username}!")
        else:
            st.error(f"❌ Login Failed: {result}")
            is_authenticated = False
else:
    st.info("💡 Enter an Instagram username and password above to unlock the URL scanner.")

st.markdown("---")

# --- STEP 2: REEL SCANNER INTERFACE ---
st.subheader("🔗 Step 2: Paste Reel Link")
reel_url = st.text_input("Instagram Reel Link:", placeholder="https://www.instagram.com/reel/...", disabled=not is_authenticated)

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
            "title": post.title or post.caption[:50] + "..." if post.caption else "No Caption",
            "owner": post.owner_username
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# Action Button
if st.button("Get Play Count", type="primary", disabled=not is_authenticated):
    if not reel_url.strip():
        st.warning("Please paste a link first.")
    else:
        with st.spinner("Scraping metrics via your session..."):
            shortcode = extract_shortcode(reel_url)
            if not shortcode:
                st.error("Invalid Instagram URL structure.")
            else:
                data = get_reel_views(L, shortcode)
                if data["success"]:
                    st.balloons()
                    st.markdown("---")
                    res_col1, res_col2 = st.columns(2)
                    res_col1.metric(label="Actual Plays / Views", value=f"{data['views']:,}")
                    res_col2.metric(label="Creator Account", value=f"@{data['owner']}")
                    st.info(f"**Caption:** {data['title']}")
                else:
                    st.error("Failed to fetch data.")
                    st.exception(data["error"])
