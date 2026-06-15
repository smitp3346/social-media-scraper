import streamlit as st
import yt_dlp
import requests
from bs4 import BeautifulSoup
import re

# --- Page Setup & Professional UI ---
st.set_page_config(page_title="ScrapeX | Universal Analyzer", page_icon="🚀", layout="centered")

# Custom CSS for Premium Look (Hiding Streamlit branding & styling button)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Button Hover Effect */
            div.stButton > button:first-child {
                border-radius: 8px;
                font-weight: bold;
                transition: all 0.3s ease-in-out;
            }
            div.stButton > button:first-child:hover {
                transform: scale(1.02);
                box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🚀 ScrapeX: Universal Link Analyzer")
st.markdown("**Supports:** YouTube Videos, Instagram Reels, Facebook Videos & Insta Photos")
st.markdown("---")

# --- URL Cleaner Function ---
def extract_clean_url(text):
    match = re.search(r'(https?://[^\s]+)', text)
    if match:
        return match.group(1)
    return text

# --- ENGINE 2: PHOTO POSTS ---
def scrape_photo_post(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        meta_desc = soup.find('meta', property='og:description')
        meta_title = soup.find('meta', property='og:title')
        
        if meta_desc and meta_desc.get('content'):
            content = meta_desc['content']
            stats = content.split('-')[0].strip() if '-' in content else "Stats found in description"
            account = meta_title['content'] if meta_title else 'Unknown Account'
            return {"Type": "Photo/Post", "Account": account, "Stats": stats, "Raw Description": content[:150] + "..."}
        return None
    except Exception:
        return None

# --- ENGINE 1: REELS/VIDEOS (With FB & Comments Fix) ---
def scrape_video_link(url):
    ydl_opts = {'quiet': True, 'extract_flat': False, 'skip_download': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            platform = info.get('extractor_key', 'Unknown')
            raw_title = info.get('title', 'No Title')
            views = info.get('view_count', 'Hidden')
            likes = info.get('like_count', 'Hidden')
            comments = info.get('comment_count', 'Hidden')

            # --- SMART FACEBOOK FIX ---
            if platform == 'Facebook' and '|' in raw_title and 'views' in raw_title.lower():
                parts = raw_title.split('|', 1) 
                stats_part = parts[0].strip()   
                real_title = parts[1].strip()   
                
                raw_title = real_title 
                
                if '·' in stats_part:
                    stat_split = stats_part.split('·')
                    views = stat_split[0].strip()
                    likes = stat_split[1].strip()
                else:
                    views = stats_part

            return {
                "Type": "Video/Reel",
                "Platform": platform,
                "Uploader": info.get('uploader', 'N/A'),
                "Title": raw_title[:80],
                "Views": views,
                "Likes": likes,
                "Comments": comments
            }
    except Exception as e:
        error_msg = str(e)
        if "There is no video" in error_msg or "Unsupported URL" in error_msg:
            return "TRY_PHOTO"
        return f"Error: {error_msg}"

# --- UI Layout & Logic ---
raw_input = st.text_input("👉 Paste any Reel, Video, or Photo link here:")
analyze_btn = st.button("🔍 Analyze Link", type="primary", use_container_width=True)

if analyze_btn:
    if not raw_input:
        st.warning("⚠️ Please paste a link first!")
    else:
        url_input = extract_clean_url(raw_input)
        
        if url_input != raw_input:
            st.info(f"💡 Smart Extract: Pura text detect hua. Sirf link use kar rahe hain: {url_input[:50]}...")

        with st.spinner("Bypassing security and extracting data... Please wait."):
            result = scrape_video_link(url_input)
            
            if result == "TRY_PHOTO":
                st.info("No video detected. Switching to Photo Engine... 📸")
                photo_result = scrape_photo_post(url_input)
                
                if photo_result:
                    st.success("✅ Photo Data Successfully Extracted!")
                    st.divider() # Sleek visual line
                    # Professional Dropdown Expander for JSON
                    with st.expander("📂 View Raw Extracted Data"):
                        st.json(photo_result)
                else:
                    st.error("❌ Could not extract data. Post might be completely private.")
            
            elif isinstance(result, dict):
                st.success("✅ Video/Reel Data Successfully Extracted!")
                st.divider() # Sleek visual line
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Platform", result["Platform"])
                col2.metric("Views", result["Views"])
                col3.metric("Likes", result["Likes"])
                col4.metric("Comments", result["Comments"])
                
                st.text_input("Uploader", result["Uploader"], disabled=True)
                st.text_area("Title", result["Title"], disabled=True)
                
            else:
                st.error("❌ " + result)