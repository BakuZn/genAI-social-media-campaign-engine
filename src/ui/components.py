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

def render_post_preview_card(platform: str, post_content: str, lang: str):
    """
    Renders an interactive, styled card matching the platform.
    """
    # Create the visually styled card
    st.markdown(f"""
    <div class="platform-box">
        <div class="platform-header">{platform.capitalize()} · {lang}</div>
        <div style="white-space: pre-wrap; margin-top: 15px; color: #2C3E50; line-height: 1.6;">{post_content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Provide a raw code block for easy copy-pasting
    with st.expander(f"Copy Raw Text for {platform}"):
        st.code(post_content, language="markdown")
