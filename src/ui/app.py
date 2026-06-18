"""
Bayer Campaign Amplification Engine - Streamlit Dashboard.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import time
from ui.components import apply_bayer_theme, render_post_preview_card
from core.orchestrator import CampaignOrchestrator

def main():
    st.set_page_config(
        page_title="Bayer Campaign Engine",
        layout="wide"
    )
    apply_bayer_theme()
    
    # Sidebar for API Configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Gemini API Key", type="password", placeholder="Enter your API key...")
        st.markdown("[Get a Gemini API Key](https://aistudio.google.com/app/apikey)")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key.strip()
            st.success("API Key loaded into memory!")
            
    st.title("Bayer Pre-Event Campaign Engine")
    st.markdown("Configure and generate platform-specific marketing campaigns.")
    
    # 1. Fill event details
    st.header("1. Event Details")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event Name")
            location = st.text_input("Location")
            event_date = st.text_input("Date")
            target_audience = st.text_input("Target Audience")
            campaign_objective = st.text_input("Campaign Objective")
        with col2:
            state = st.text_input("State/Region")
            crop = st.text_input("Primary Crop(s)")
            seed_product = st.text_input("Seed Products")
            crop_protection = st.text_input("Crop Protection Products")
            key_messages = st.text_area("Key Messages")

    st.markdown("---")
    
    # 2. Select Language & 3. Select Platforms
    col3, col4 = st.columns(2)
    with col3:
        st.header("2. Target Languages")
        st.markdown("Select the languages to generate content for.")
        lang_en = st.checkbox("English", value=True)
        lang_hi = st.checkbox("Hindi")
        lang_mr = st.checkbox("Marathi")
        lang_kn = st.checkbox("Kannada")
        lang_te = st.checkbox("Telugu")
        
    with col4:
        st.header("3. Social Platforms")
        st.markdown("Select platforms for the campaign.")
        plat_li = st.checkbox("LinkedIn", value=True)
        plat_ig = st.checkbox("Instagram", value=True)
        plat_fb = st.checkbox("Facebook", value=True)
        plat_wa = st.checkbox("WhatsApp", value=True)

    # Compile selections
    languages = []
    if lang_en: languages.append("English")
    if lang_hi: languages.append("Hindi")
    if lang_mr: languages.append("Marathi")
    if lang_kn: languages.append("Kannada")
    if lang_te: languages.append("Telugu")
    
    platforms = []
    if plat_li: platforms.append("LinkedIn")
    if plat_ig: platforms.append("Instagram")
    if plat_fb: platforms.append("Facebook")
    if plat_wa: platforms.append("WhatsApp")

    st.markdown("---")
    
    # 4. Click Generate
    if st.button("Generate Campaign", use_container_width=True):
        if not event_name or not campaign_objective:
            st.error("Please fill in at least the Event Name and Campaign Objective.")
            return
            
        if not languages or not platforms:
            st.error("Please select at least one language and one platform.")
            return

        with st.spinner("Processing campaign request..."):
            
            try:
                # Build the dictionary to pass to the orchestrator
                event_data = {
                    "event_name": event_name,
                    "location": location,
                    "state": state,
                    "date": event_date,
                    "target_audience": [target_audience] if target_audience else [],
                    "campaign_objective": campaign_objective,
                    "crop": [crop] if crop else [],
                    "seed_product": [seed_product] if seed_product else [],
                    "crop_protection_product": [crop_protection] if crop_protection else [],
                    "key_messages": [key_messages] if key_messages else []
                }
                
                orchestrator = CampaignOrchestrator()
                campaign_results = orchestrator.generate_campaign(event_data, platforms, languages)
                
                st.success("Campaign Generated Successfully.")
                
                st.header("Campaign Output")
                
                # Display generated content iteratively by language, then platform
                for lang in languages:
                    st.subheader(f"{lang} Campaign")
                    
                    # Create a visual grid for platforms
                    cols = st.columns(len(platforms))
                    
                    for idx, plat in enumerate(platforms):
                        with cols[idx]:
                            content = campaign_results[lang][plat]
                            render_post_preview_card(plat, content, lang)
                    
                    st.markdown("---")
            
            except Exception as e:
                st.error(f"Error connecting to Gemini API: {str(e)}")

if __name__ == "__main__":
    main()
