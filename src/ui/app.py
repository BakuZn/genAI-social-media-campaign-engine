"""
Bayer Campaign Amplification Engine - Streamlit Dashboard.
Enterprise Workspace Edition.
"""
import sys
import os
import pandas as pd
import time
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import streamlit.components.v1 as components
from ui.components import (
    apply_bayer_theme, 
    render_compact_header, 
    render_dashboard_kpis,
    render_campaign_summary,
    render_poster_panel,
    render_asset_card
)
from core.orchestrator import CampaignOrchestrator
from data.parser import parse_csv_events


# Removed cache decorator to prevent stale responses during testing
def generate_campaign_cached(selected_event, platforms, languages, image_bytes):
    """Wrapper for the campaign generation orchestration."""
    orchestrator = CampaignOrchestrator()
    return orchestrator.generate_campaign(selected_event, platforms, languages, image_bytes=image_bytes)

def main():
    st.set_page_config(
        page_title="Sangam 2.0 Campaign Workspace",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 1. Apply Corporate Theme & Fixed Header
    apply_bayer_theme()
    render_compact_header()

    # Workspace Grid Layout
    left_col, right_col = st.columns([1, 2.5], gap="large")
    
    selected_event = None
    languages = []
    platforms = []
    image_bytes = None
    
    if "generate_clicked" not in st.session_state:
        st.session_state.generate_clicked = False
    
    # ================= LEFT COLUMN: OPERATIONS PANEL =================
    with left_col:
        st.markdown("<h3 style='font-size:16px; margin-bottom: 20px; border-bottom: 2px solid #003E96; padding-bottom: 5px; display:inline-block;'>OPERATIONS PANEL</h3>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div style='font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 8px;'>1. Upload Campaign Source</div>", unsafe_allow_html=True)
            
            # Distinct File Uploaders
            uploaded_file = st.file_uploader("SharePoint Export (.csv)", type=["csv"])
            poster_file = st.file_uploader("Campaign Poster Image", type=["jpg", "jpeg", "png"])
            
            events = []
            if uploaded_file:
                try:
                    df = pd.read_csv(uploaded_file)
                    events = parse_csv_events(df)
                except Exception as e:
                    st.error(f"Data error: {e}")

            if poster_file:
                image_bytes = poster_file.getvalue()

            # Unlock workspace if at least one source is uploaded
            if events or image_bytes:
                
                if events:
                    st.markdown("<br><div style='font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 8px;'>2. Select Event</div>", unsafe_allow_html=True)
                    event_names = [f"{e['event_name']} ({e['date']})" for e in events]
                    selected_event_idx = st.selectbox("Select Event", range(len(event_names)), format_func=lambda x: event_names[x], label_visibility="collapsed")
                    selected_event = events[selected_event_idx]
                else:
                    # Provide an empty/mock event dictionary so the orchestrator and UI don't crash
                    selected_event = {
                        "event_name": "Custom Image Campaign",
                        "date": "TBD",
                        "territory": "TBD",
                        "location": "TBD",
                        "objective": "Derived strictly from uploaded poster.",
                        "estimated_farmers": 0,
                        "product_focus": "Derived from poster",
                        "group_lob": "Unknown"
                    }

                custom_product = st.text_input("Additional Product Focus (Optional)", help="If you uploaded an image without a CSV, or want to force the AI to lookup a specific product, type it here (e.g. 'Camalus').")
                if custom_product:
                    selected_event["product_focus"] = custom_product

                st.markdown("<br><div style='font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 8px;'>3. Target Languages</div>", unsafe_allow_html=True)
                languages = st.multiselect(
                    "Target Languages",
                    ["English", "Hindi", "Marathi", "Kannada", "Telugu", "Punjabi"],
                    default=[],
                    label_visibility="collapsed"
                )
                
                st.markdown("<br><div style='font-size: 13px; font-weight: 600; color: #64748B; margin-bottom: 8px;'>4. Communication Channels</div>", unsafe_allow_html=True)
                platforms = st.multiselect(
                    "Delivery Channels",
                    ["Internal WhatsApp", "Farmer WhatsApp", "Facebook", "Instagram", "LinkedIn"],
                    default=[],
                    label_visibility="collapsed"
                )

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Validation Logic for Generate Button
                is_disabled = (len(languages) == 0) or (len(platforms) == 0)
                
                # Dynamic Button State
                btn_col1, btn_col2 = st.columns([2.5, 1])
                with btn_col1:
                    if st.button("▶ Execute Campaign Generation", use_container_width=True, disabled=is_disabled):
                        st.session_state.generate_clicked = True
                with btn_col2:
                    if st.button("🔄 Force Regenerate", help="Clears memory to generate fresh variations.", use_container_width=True, disabled=is_disabled):
                        generate_campaign_cached.clear()
                        st.session_state.generate_clicked = True

    # ================= RIGHT COLUMN: CONTEXT & INSIGHTS =================
    with right_col:
        st.markdown("<h3 style='font-size:16px; margin-bottom: 20px; border-bottom: 2px solid #5CB531; padding-bottom: 5px; display:inline-block;'>WORKSPACE & ASSETS</h3>", unsafe_allow_html=True)
        
        if not (events or image_bytes):
            st.info("Upload a CSV export or a Campaign Poster to populate the workspace.")
        else:
            # Render Top Metrics Bar
            render_dashboard_kpis(selected_event, len(platforms), len(languages))
            
            # Empty States for missing selections
            if len(languages) == 0:
                st.info("Select one or more target languages in the Operations Panel.")
            if len(platforms) == 0:
                st.info("Choose communication channels for content generation in the Operations Panel.")
                
            # Context Summary Row
            ctx_col1, ctx_col2 = st.columns([1.5, 1])
            with ctx_col1:
                render_campaign_summary(selected_event)
            with ctx_col2:
                if image_bytes:
                    render_poster_panel(image_bytes)
                else:
                    st.markdown("""
                    <div class="enterprise-panel" style="border: 1px dashed #cbd5e1; background: #f8fafc; text-align: center; color: #64748b;">
                        <div style="font-size: 24px; margin-bottom: 8px;">🖼️</div>
                        <div style="font-size: 13px; font-weight: 500;">No Visual Context Uploaded</div>
                        <div style="font-size: 11px;">Upload a campaign poster (optional) to provide visual context.</div>
                    </div>
                    """, unsafe_allow_html=True)

            if not st.session_state.generate_clicked and not is_disabled:
                st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;'>", unsafe_allow_html=True)
                st.info("No campaign assets generated yet. Execute campaign generation to begin.")

            # Generate Action execution
            if st.session_state.generate_clicked:
                st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #0f172a; margin-bottom: 20px;'>Generated Marketing Assets</h4>", unsafe_allow_html=True)
                
                with st.status("Executing Campaign Generation...", expanded=True) as status:
                    try:
                        status.update(label="✓ Reading Event Data...", state="running")
                        time.sleep(1) # Small pause for UX
                        
                        if image_bytes:
                            status.update(label="✓ Analyzing Campaign Poster...", state="running")
                            time.sleep(1)
                            
                        status.update(label="✓ Extracting Campaign Context...", state="running")
                        time.sleep(0.5)
                        
                        status.update(label="⟳ Generating Multilingual Content via Gemini...", state="running")
                        
                        # Call the cached function instead of orchestrator directly
                        campaign_results = generate_campaign_cached(selected_event, platforms, languages, image_bytes)
                        
                        status.update(label="Campaign Assets Generated Successfully", state="complete", expanded=False)
                        
                        st.markdown("<div id='campaign-results-start'></div>", unsafe_allow_html=True)
                        components.html(
                            "<script>window.parent.document.getElementById('campaign-results-start').scrollIntoView({behavior: 'smooth'});</script>",
                            height=0
                        )
                        
                        # Render output grids
                        for lang in languages:
                            st.markdown(f"<div style='margin-bottom: 15px; margin-top: 15px; font-weight: 600; color: #64748B; text-transform: uppercase;'>{lang} Pack</div>", unsafe_allow_html=True)
                            
                            # Auto-wrap columns based on number of platforms
                            cols = st.columns(min(len(platforms), 3))
                            for idx, plat in enumerate(platforms):
                                col_idx = idx % 3
                                with cols[col_idx]:
                                    content = campaign_results[lang].get(plat, "Generation failed.")
                                    render_asset_card(plat, content, lang)
                                    # Add some spacing between rows
                                    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
                    
                    except Exception as e:
                        error_str = str(e).lower()
                        if "503" in error_str or "429" in error_str or "unavailable" in error_str or "quota" in error_str:
                            status.update(label="AI Service Experiencing High Demand", state="error")
                            st.error("Google Gemini servers are currently overloaded. Background retries failed. Please wait a minute and try again.")
                        else:
                            status.update(label="Error Generating Campaign", state="error")
                            st.error(f"Error during API execution: {str(e)}")

if __name__ == "__main__":
    main()
