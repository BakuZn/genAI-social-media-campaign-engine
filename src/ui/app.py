"""
Bayer Campaign Amplification Engine - Streamlit Dashboard.
"""
import sys
import os
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import time
from ui.components import apply_bayer_theme, render_post_preview_card
from core.orchestrator import CampaignOrchestrator

def mock_parse_csv(df):
    """
    Temporary mock parser until colleague's data_parser.py is ready.
    """
    events = []
    for _, row in df.iterrows():
        # Fallbacks for missing columns
        event_name = row.get("Title", "Unknown Event")
        date = row.get("Event Date", "Unknown Date")
        territory = row.get("Territory", "Unknown Territory")
        location_raw = row.get("Event Location", "Unknown Location")
        
        # Super simple mock extraction: just grab the first 30 chars or so to avoid huge JSON
        if pd.isna(location_raw):
            location = "Unknown Location"
        elif "DisplayName" in str(location_raw):
            try:
                import json
                loc_dict = json.loads(location_raw)
                location = loc_dict.get("DisplayName", "Unknown Location")
            except:
                location = str(location_raw)[:30]
        else:
            location = str(location_raw)

        events.append({
            "event_name": event_name,
            "date": date,
            "territory": territory,
            "location": location,
            "objective": row.get("Objective / Purpose", ""),
            "estimated_farmers": row.get("Estimated Farmers", 0),
            "product_focus": row.get("Product /Combo Focus", ""),
            "participants": row.get("Participants from Commercial(CP + Seminis)", ""),
            "group_lob": row.get("Group / LOB", "")
        })
    return events

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
            
    st.title("Bayer Sangam 2.0 Campaign Engine")
    st.markdown("Upload Sangam events and automatically generate platform-specific marketing campaigns.")
    
    # 1. Upload CSV
    st.header("1. Upload Event Data")
    uploaded_file = st.file_uploader("Upload Sangam_Events.csv exported from SharePoint", type=["csv"])
    
    if not uploaded_file:
        st.info("Please upload a CSV file to proceed.")
        return
        
    try:
        df = pd.read_csv(uploaded_file)
        events = mock_parse_csv(df)
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return

    if not events:
        st.warning("No events found in the uploaded file.")
        return

    st.markdown("---")
    
    # 2. Event Selection
    st.header("2. Select Event")
    event_names = [f"{e['event_name']} - {e['territory']} ({e['date']})" for e in events]
    selected_event_idx = st.selectbox("Choose an event to amplify", range(len(event_names)), format_func=lambda x: event_names[x])
    selected_event = events[selected_event_idx]
    
    # Event Preview
    st.subheader("Event Preview")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Name:** {selected_event.get('event_name')}")
            st.markdown(f"**Date:** {selected_event.get('date')}")
            st.markdown(f"**Location:** {selected_event.get('location')}")
        with col2:
            st.markdown(f"**Territory:** {selected_event.get('territory')}")
            st.markdown(f"**Group/LOB:** {selected_event.get('group_lob')}")
            st.markdown(f"**Est. Farmers:** {selected_event.get('estimated_farmers')}")
        with col3:
            st.markdown(f"**Objective:** {selected_event.get('objective')}")
            st.markdown(f"**Product Focus:** {selected_event.get('product_focus')}")
            st.markdown(f"**Participants:** {selected_event.get('participants')}")

    st.markdown("---")
    
    # 3. Select Language & 4. Select Platforms
    col3, col4 = st.columns(2)
    with col3:
        st.header("3. Target Languages")
        st.markdown("Select the languages to generate content for.")
        lang_en = st.checkbox("English", value=True)
        lang_hi = st.checkbox("Hindi")
        lang_mr = st.checkbox("Marathi")
        lang_kn = st.checkbox("Kannada")
        lang_te = st.checkbox("Telugu")
        lang_pa = st.checkbox("Punjabi")
        
    with col4:
        st.header("4. Communication Platforms")
        st.markdown("Select outputs for the campaign.")
        plat_int_wa = st.checkbox("Internal WhatsApp (Team Coordination)", value=True)
        plat_ext_wa = st.checkbox("Farmer WhatsApp", value=True)
        plat_fb = st.checkbox("Facebook", value=True)
        plat_ig = st.checkbox("Instagram", value=True)
        plat_li = st.checkbox("LinkedIn", value=True)

    # Compile selections
    languages = []
    if lang_en: languages.append("English")
    if lang_hi: languages.append("Hindi")
    if lang_mr: languages.append("Marathi")
    if lang_kn: languages.append("Kannada")
    if lang_te: languages.append("Telugu")
    if lang_pa: languages.append("Punjabi")
    
    platforms = []
    if plat_int_wa: platforms.append("Internal WhatsApp")
    if plat_ext_wa: platforms.append("Farmer WhatsApp")
    if plat_fb: platforms.append("Facebook")
    if plat_ig: platforms.append("Instagram")
    if plat_li: platforms.append("LinkedIn")

    # 5. Optional Image Upload for Context
    st.header("5. Campaign Poster (Optional)")
    st.markdown("Upload a poster so Gemini can read the visual context, and preview it in the output.")
    poster_file = st.file_uploader("Upload Poster", type=["jpg", "jpeg", "png"])
    image_bytes = None
    if poster_file:
        image_bytes = poster_file.getvalue()
        st.image(poster_file, width=300, caption="Uploaded Poster")

    st.markdown("---")
    
    # Generate Button
    if st.button("Generate Campaign Content", use_container_width=True):
        if not languages or not platforms:
            st.error("Please select at least one language and one platform.")
            return

        with st.spinner("Processing campaign request via Gemini (This may take longer if reading an image)..."):
            try:
                orchestrator = CampaignOrchestrator()
                # Pass the selected event dict directly and image bytes
                campaign_results = orchestrator.generate_campaign(selected_event, platforms, languages, image_bytes=image_bytes)
                
                st.success("Campaign Generated Successfully.")
                
                st.header("Campaign Output")
                
                # Display generated content iteratively by language, then platform
                for lang in languages:
                    st.subheader(f"{lang} Content")
                    
                    # Create a visual grid for platforms
                    cols = st.columns(len(platforms))
                    
                    for idx, plat in enumerate(platforms):
                        with cols[idx]:
                            content = campaign_results[lang].get(plat, "Generation failed for this platform.")
                            render_post_preview_card(plat, content, lang, image_bytes)
                    
                    st.markdown("---")
            
            except Exception as e:
                st.error(f"Error generating campaign: {str(e)}")

if __name__ == "__main__":
    main()
