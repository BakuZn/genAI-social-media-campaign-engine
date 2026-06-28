"""
Custom reusable Streamlit components and style injections for premium enterprise branding.
Dashboard Workspace Edition.
"""
import streamlit as st
import os
import base64
import urllib.parse
import json

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

def render_smart_share_button(platform: str, content: str):
    """
    Renders a branded smart button that copies text and opens the native platform in one click.
    """
    plat_lower = platform.lower()
    encoded_msg = urllib.parse.quote(content)
    
    # Defaults
    bg_color = "#333333"
    svg_icon = ""
    url = "#"
    
    if "whatsapp" in plat_lower:
        bg_color = "#25D366"
        url = f"https://api.whatsapp.com/send?text={encoded_msg}"
        svg_icon = '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M17.47 16.53c-.32.9-1.8 1.62-2.52 1.76-.6.12-1.39.22-4.14-1-3.23-1.44-5.26-4.9-5.42-5.14-.15-.24-1.29-1.81-1.29-3.46s.85-2.48 1.15-2.82c.26-.29.69-.37.99-.37.1 0 .19 0 .28.01.27.02.63-.09.91.64.3.75 1.01 2.61 1.1 2.82.09.21.16.47.03.74-.12.28-.19.45-.39.69-.21.24-.45.54-.62.72-.18.19-.39.4-.17.78.22.38 1.01 1.75 2.15 2.8 1.48 1.36 2.8 1.83 3.19 2.01.38.18.6.15.82-.1.22-.25.96-1.16 1.22-1.55.26-.39.52-.33.88-.2.37.13 2.3 1.13 2.7 1.33.39.2.66.3.75.46.09.16.09.93-.23 1.83M12.02 2C6.49 2 2 6.49 2 12.02c0 1.77.46 3.5 1.34 5.03L2 22l5.1-1.33c1.47.8 3.14 1.22 4.9 1.22 5.53 0 10.02-4.49 10.02-10.02C22 6.49 17.55 2 12.02 2z" fill="#FFFFFF"/></svg>'
    elif "facebook" in plat_lower:
        bg_color = "#1877F2"
        url = f"https://www.facebook.com/sharer/sharer.php?u=https://bayer.com&quote={encoded_msg}"
        svg_icon = '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 2.04C6.5 2.04 2 6.53 2 12.06C2 17.06 5.66 21.21 10.44 21.96V14.96H7.9V12.06H10.44V9.85C10.44 7.34 11.93 5.96 14.22 5.96C15.31 5.96 16.45 6.15 16.45 6.15V8.62H15.19C13.95 8.62 13.56 9.39 13.56 10.18V12.06H16.35L15.9 14.96H13.56V21.96A10 10 0 0 0 22 12.06C22 6.53 17.5 2.04 12 2.04Z" fill="#FFFFFF"/></svg>'
    elif "instagram" in plat_lower:
        bg_color = "#E1306C"
        url = "https://www.instagram.com"
        svg_icon = '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.22.41.56.22.95.48 1.38.91.43.43.69.82.91 1.38.16.42.36 1.05.41 2.22.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.22-.22.56-.48.95-.91 1.38-.43.43-.82.69-1.38.91-.42.16-1.05.36-2.22.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.22-.41-.56-.22-.95-.48-1.38-.91-.43-.43-.69-.82-.91-1.38-.16-.42-.36-1.05-.41-2.22C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.22.22-.56.48-.95.91-1.38.43-.43.82-.69 1.38-.91.42-.16 1.05-.36 2.22-.41 1.27-.06 1.65-.07 4.85-.07M12 0C8.74 0 8.33.01 7.05.07 5.77.13 4.9.33 4.14.63c-.8.3-1.47.7-2.14 1.37-.67.67-1.07 1.34-1.37 2.14-.3.76-.5 1.63-.56 2.91C.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.28.26 2.15.56 2.91.3.8.7 1.47 1.37 2.14.67.67 1.34 1.07 2.14 1.37.76.3 1.63.5 2.91.56 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c1.28-.06 2.15-.26 2.91-.56.8-.3 1.47-.7 2.14-1.37.67-.67 1.07-1.34 1.37-2.14.3-.76.5-1.63.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.28-.26-2.15-.56-2.91-.3-.8-.7-1.47-1.37-2.14-.67-.67-1.34-1.07-2.14-1.37-.76-.3-1.63-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1018.16 12 6.16 6.16 0 0012 5.84zm0 10.16A4 4 0 1116 12a4 4 0 01-4 4zm6.4-9.67a1.44 1.44 0 11-2.88 0 1.44 1.44 0 012.88 0z" fill="#FFFFFF"/></svg>'
    elif "linkedin" in plat_lower:
        bg_color = "#0A66C2"
        url = f"https://www.linkedin.com/shareArticle?mini=true&url=https://bayer.com&title=Bayer%20Campaign&summary={encoded_msg}"
        svg_icon = '<svg viewBox="0 0 24 24" width="20" height="20"><path d="M19 0h-14c-2.76 0-5 2.24-5 5v14c0 2.76 2.24 5 5 5h14c2.76 0 5-2.24 5-5v-14c0-2.76-2.24-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.27c-.97 0-1.75-.79-1.75-1.76s.78-1.76 1.75-1.76 1.75.79 1.75 1.76-.78 1.76-1.75 1.76zm13.5 12.27h-3v-5.6c0-1.34-.03-3.05-1.86-3.05-1.86 0-2.15 1.45-2.15 2.95v5.7h-3v-11h2.88v1.5h.04c.4-.76 1.38-1.56 2.84-1.56 3.04 0 3.6 2 3.6 4.6v6.46z" fill="#FFFFFF"/></svg>'
    
    # Safe JSON string for the JS payload
    safe_content = json.dumps(content)
    
    html_code = f"""
    <div id="btn-container" style="
        display: flex; 
        align-items: center; 
        justify-content: center; 
        background-color: {bg_color}; 
        color: white; 
        padding: 10px 15px; 
        border-radius: 6px; 
        cursor: pointer; 
        font-family: 'Inter', sans-serif; 
        font-weight: 600; 
        font-size: 14px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        transition: transform 0.1s ease, box-shadow 0.1s ease;
        user-select: none;
        margin-top: 10px;
    " 
    onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.15)';" 
    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';"
    onclick="handleSmartClick()">
        <div style="display: flex; align-items: center; gap: 8px;">
            {svg_icon}
            <span>Open {platform.title()}</span>
        </div>
    </div>
    
    <div id="toast" style="
        visibility: hidden;
        min-width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 4px;
        padding: 8px;
        position: fixed;
        z-index: 1;
        left: 50%;
        bottom: 10px;
        transform: translateX(-50%);
        font-family: sans-serif;
        font-size: 12px;
        opacity: 0;
        transition: opacity 0.3s, visibility 0.3s;
    ">Caption copied! Opening...</div>

    <script>
        function handleSmartClick() {{
            const content = {safe_content};
            const url = "{url}";
            
            // Try clipboard
            navigator.clipboard.writeText(content).then(() => {{
                showToast();
                setTimeout(() => {{
                    window.open(url, '_blank');
                }}, 800);
            }}).catch(err => {{
                console.error("Clipboard failed", err);
                // Still open URL if clipboard fails
                window.open(url, '_blank');
            }});
        }}
        
        function showToast() {{
            const toast = document.getElementById("toast");
            toast.style.visibility = "visible";
            toast.style.opacity = "1";
            setTimeout(() => {{
                toast.style.visibility = "hidden";
                toast.style.opacity = "0";
            }}, 2000);
        }}
    </script>
    """
    import streamlit.components.v1 as components
    components.html(html_code, height=60)

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
    
    # Action Footer using Smart Button
    render_smart_share_button(platform, post_content)
