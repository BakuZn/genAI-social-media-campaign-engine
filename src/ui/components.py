"""
Custom reusable Streamlit components and style injections for premium branding.
"""
import streamlit as st

def apply_bayer_theme():
    """
    Injects custom CSS to style the Streamlit app with Bayer's brand colors
    (Bayer Blue, Bayer Green).
    """
    st.markdown(
        """
        <style>
        /* Primary accent colors */
        :root {
            --bayer-blue: #001A72;
            --bayer-light-blue: #00A9E0;
            --bayer-green: #89D329;
            --bayer-dark-green: #00B140;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: var(--bayer-blue) !important;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: var(--bayer-dark-green) !important;
            color: white !important;
            border-radius: 6px;
            border: none;
            font-weight: bold;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: var(--bayer-green) !important;
            color: var(--bayer-blue) !important;
            border: none;
        }
        
        /* Generated content boxes */
        .platform-box {
            background-color: #F8F9FA;
            border-left: 5px solid var(--bayer-light-blue);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .platform-header {
            color: var(--bayer-blue);
            margin-top: 0;
            display: flex;
            align-items: center;
            font-weight: bold;
            font-size: 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

import urllib.parse

def generate_platform_url(platform: str, content: str) -> str:
    """Mock URL builder until url_utils.py is provided."""
    plat_lower = platform.lower()
    if "whatsapp" in plat_lower:
        encoded_msg = urllib.parse.quote(content)
        return f"https://wa.me/?text={encoded_msg}"
    elif "linkedin" in plat_lower:
        return "https://www.linkedin.com/feed/"
    elif "facebook" in plat_lower:
        return "https://www.facebook.com/"
    elif "instagram" in plat_lower:
        return "https://www.instagram.com/"
    return "#"

import base64

def render_post_preview_card(platform: str, post_content: str, lang: str, image_bytes: bytes = None):
    """
    Renders an interactive, styled card matching the platform.
    """
    # Create the visually styled card
    st.markdown(f"""
    <div class="platform-box">
        <div class="platform-header">{platform.title()} · {lang}</div>
        <div style="white-space: pre-wrap; margin-top: 15px; color: #2C3E50; line-height: 1.6;">{post_content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Row
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.popover("Copy Content"):
            st.code(post_content, language="markdown")
    with col2:
        url = generate_platform_url(platform, post_content)
        st.link_button(f"Open {platform.title()}", url, use_container_width=True)
