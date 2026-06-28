"""
Custom reusable Streamlit components and style injections for premium enterprise branding.
Dashboard Workspace Edition.
"""
import streamlit as st
import os
import base64
import urllib.parse

def get_base64_image(image_path: str) -> str:
    """Helper to load local image as base64 for HTML embedding."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception:
        return ""

def apply_bayer_theme():
    """
    Injects custom CSS to style the Streamlit app into an Enterprise Dashboard.
    """
    st.markdown(
        """
        <style>
        /* Hide Streamlit default header and footer */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Global Background and Font */
        .stApp {
            background-color: #F8F9FB;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        /* Primary accent colors */
        :root {
            --bayer-blue: #003E96;
            --bayer-light-blue: #00A9E0;
            --bayer-green: #5CB531;
            --border-color: #E2E8F0;
            --text-main: #1E293B;
            --text-muted: #64748B;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5 {
            color: var(--text-main) !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem;
        }
        
        /* Enterprise Panel styling */
        .enterprise-panel {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            margin-bottom: 16px;
        }
        
        .panel-header {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-main);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* KPI Metric Styling */
        .kpi-container {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
        }
        .kpi-box {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 12px 16px;
            flex: 1;
            display: flex;
            align-items: center;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }
        .kpi-icon {
            font-size: 24px;
            margin-right: 12px;
            background: #F1F5F9;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
        }
        .kpi-val {
            font-size: 18px;
            font-weight: 700;
            color: var(--bayer-blue);
            line-height: 1.2;
        }
        .kpi-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            font-weight: 600;
        }

        /* Streamlit Element Overrides */
        .stButton>button {
            background-color: var(--bayer-blue) !important;
            color: white !important;
            border-radius: 4px;
            border: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: var(--bayer-light-blue) !important;
        }
        
        /* Reduce padding in columns */
        [data-testid="column"] {
            padding: 0 8px;
        }
        
        /* Asset Card Styling */
        .asset-card {
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }
        .asset-header {
            background: #F8FAFC;
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .asset-platform {
            font-weight: 600;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .asset-badge {
            background: var(--bayer-blue);
            color: white;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
        }
        .asset-body {
            padding: 16px;
            flex-grow: 1;
            font-size: 14px;
            color: #334155;
            white-space: pre-wrap;
            line-height: 1.5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_compact_header():
    """Renders the top navigation bar with large centered logos."""
    bayer_logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "logos", "bayer logo.jpeg")
    sangam_logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "logos", "sangam 2.0.jpeg")
    seminis_logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "logos", "Seminis logo 2.png")
    
    b64_bayer = get_base64_image(bayer_logo_path)
    b64_sangam = get_base64_image(sangam_logo_path)
    b64_seminis = get_base64_image(seminis_logo_path)
    
    img_bayer = f'<img src="data:image/jpeg;base64,{b64_bayer}" class="nav-logo-bayer">' if b64_bayer else ''
    img_sangam = f'<img src="data:image/jpeg;base64,{b64_sangam}" class="nav-logo-sangam">' if b64_sangam else ''
    img_seminis = f'<img src="data:image/png;base64,{b64_seminis}" class="nav-logo-seminis">' if b64_seminis else ''

    st.markdown(f"""
    <style>
        .custom-nav-bar {{
            background-color: white; padding: 0 30px; display: flex; align-items: center; justify-content: space-between; 
            border-bottom: 2px solid #003E96; position: fixed; top: 0; left: 0; width: 100%; z-index: 999999; box-shadow: 0 2px 5px rgba(0,0,0,0.05); height: 190px;
        }}
        .nav-logo-bayer {{ height: 110px; margin-right: 20px; }}
        .nav-logo-sangam {{ height: 165px; border-radius: 8px; }}
        .nav-logo-seminis {{ height: 110px; border-radius: 4px; }}
        .nav-left, .nav-center, .nav-right {{ display: flex; align-items: center; flex: 1; }}
        .nav-center {{ justify-content: center; }}
        .nav-right {{ justify-content: flex-end; }}
        .nav-spacer {{ height: 210px; }}
        
        @media (max-width: 768px) {{
            .custom-nav-bar {{ flex-direction: column; height: auto; padding: 10px; gap: 10px; position: static; }}
            .nav-left, .nav-center, .nav-right {{ flex: auto; justify-content: center; width: 100%; }}
            .nav-logo-bayer, .nav-logo-sangam, .nav-logo-seminis {{ height: 60px; margin: 0; margin-bottom: 5px; }}
            .nav-left {{ flex-direction: column; text-align: center; }}
            .nav-title-text {{ font-size: 16px !important; margin-bottom: 5px; }}
            .nav-spacer {{ display: none; }}
            .nav-divider {{ display: none; }}
        }}
    </style>
    
    <div class="custom-nav-bar">
        <!-- Left Section -->
        <div class="nav-left">
            {img_bayer}
            <div class="nav-divider" style="width: 1px; height: 80px; background: #E2E8F0; margin-right: 20px;"></div>
            <div>
                <div class="nav-title-text" style="color: #003E96; font-size: 22px; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 5px;">Sangam 2.0 Campaign Workspace</div>
                <span style="background-color: #5CB531; color: white; padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: bold; text-transform: uppercase;">Production</span>
            </div>
        </div>
        <!-- Center Section (Sangam Logo) -->
        <div class="nav-center">
            {img_sangam}
        </div>
        <!-- Right Section (Seminis Logo) -->
        <div class="nav-right">
            {img_seminis}
        </div>
    </div>
    <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

def render_dashboard_kpis(event, num_channels, num_langs):
    """Renders a high-density metric bar at the top of the workspace."""
    if not event:
        return
        
    farmers = event.get('estimated_farmers', 0)
    territory = event.get('territory', 'Unknown')
    product = event.get('product_focus', 'None')
    
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-box">
            <div class="kpi-icon">👥</div>
            <div>
                <div class="kpi-label">Target Reach</div>
                <div class="kpi-val">{farmers} Farmers</div>
            </div>
        </div>
        <div class="kpi-box">
            <div class="kpi-icon">📍</div>
            <div>
                <div class="kpi-label">Territory Focus</div>
                <div class="kpi-val">{territory}</div>
            </div>
        </div>
        <div class="kpi-box">
            <div class="kpi-icon">🌾</div>
            <div>
                <div class="kpi-label">Product Focus</div>
                <div class="kpi-val" style="font-size: 14px;">{product}</div>
            </div>
        </div>
        <div class="kpi-box">
            <div class="kpi-icon">📢</div>
            <div>
                <div class="kpi-label">Delivery Scope</div>
                <div class="kpi-val">{num_channels} Channels</div>
            </div>
        </div>
        <div class="kpi-box">
            <div class="kpi-icon">🌐</div>
            <div>
                <div class="kpi-label">Localization</div>
                <div class="kpi-val">{num_langs} Languages</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_campaign_summary(event):
    """Renders a sleek campaign summary panel."""
    st.markdown(f"""
    <div class="enterprise-panel">
        <div class="panel-header">Campaign Source Data</div>
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 8px 0; color: #64748b; width: 120px;">Event Name</td>
                <td style="padding: 8px 0; font-weight: 500; color: #0f172a;">{event.get('event_name')}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 8px 0; color: #64748b;">Date & Location</td>
                <td style="padding: 8px 0; font-weight: 500; color: #0f172a;">{event.get('date')} | {event.get('location')}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 8px 0; color: #64748b;">Objective</td>
                <td style="padding: 8px 0; font-weight: 500; color: #0f172a;">{event.get('objective')}</td>
            </tr>
            <tr>
                <td style="padding: 8px 0; color: #64748b;">Group / LOB</td>
                <td style="padding: 8px 0; font-weight: 500; color: #0f172a;">{event.get('group_lob')}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

def render_poster_panel(image_bytes):
    """Renders the AI context panel for the uploaded poster."""
    b64_img = base64.b64encode(image_bytes).decode('utf-8')
    st.markdown(f"""
    <div class="enterprise-panel" style="border-left: 3px solid #00A9E0;">
        <div class="panel-header">AI Visual Context Active</div>
        <div style="display: flex; gap: 12px;">
            <img src="data:image/jpeg;base64,{b64_img}" style="width: 80px; height: 100%; object-fit: contain; border-radius: 4px; border: 1px solid #e2e8f0;">
            <div style="font-size: 12px; color: #475569;">
                <div style="margin-bottom: 6px;"><strong>Status:</strong> Poster Indexed</div>
                <div style="margin-bottom: 6px;"><strong>Capabilities:</strong> Multilingual OCR & Object Detection</div>
                <div><strong>Action:</strong> Gemini will synchronize generated copy with extracted visual themes and text.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_platform_url(platform: str, content: str) -> str:
    """Mock URL builder."""
    plat_lower = platform.lower()
    if "whatsapp" in plat_lower:
        encoded_msg = urllib.parse.quote(content)
        return f"https://web.whatsapp.com/send?text={encoded_msg}"
    elif "linkedin" in plat_lower:
        return "https://www.linkedin.com"
    elif "facebook" in plat_lower:
        return "https://www.facebook.com"
    elif "instagram" in plat_lower:
        return "https://www.instagram.com"
    return "#"

def render_asset_card(platform: str, post_content: str, lang: str):
    """
    Renders an Enterprise Asset Card with Header, Body, and Footer layout.
    """
    icon_map = {
        "facebook": "📘",
        "instagram": "📸",
        "linkedin": "💼",
        "farmer whatsapp": "💬",
        "internal whatsapp": "📱"
    }
    icon = icon_map.get(platform.lower(), "📄")
    
    st.markdown(f"""
    <div class="asset-card">
        <div class="asset-header">
            <div class="asset-platform">{icon} {platform.title()}</div>
            <div class="asset-badge">{lang}</div>
        </div>
        <div class="asset-body">{post_content}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Footer using Streamlit columns to align buttons tightly
    col1, col2 = st.columns(2)
    with col1:
        with st.popover("📄 Copy", use_container_width=True):
            st.code(post_content, language="markdown")
    with col2:
        url = generate_platform_url(platform, post_content)
        st.link_button(f"{icon} Open {platform.title()}", url, use_container_width=True)
