import streamlit as st
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
import webbrowser
import base64
import random
import os
import json

# Page config
st.set_page_config(
    page_title="📱 ScrollPoints - Time Waster Certificate Generator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling with animations
st.markdown("""
    <style>
    :root {
        --primary: #405DE6;
        --secondary: #5851DB;
        --accent: #833AB4;
        --light: #F5F5F5;
        --dark: #121212;
        --instagram: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        --facebook: #1877F2;
        --twitter: #1DA1F2;
        --tiktok: #000000;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main {
        background-color: var(--light);
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-out;
    }
    
    .header {
        text-align: center;
        margin-bottom: 2.5rem;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        position: relative;
    }
    
    .header::after {
        content: "";
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(to right, var(--primary), var(--accent));
        border-radius: 2px;
    }
    
    .button {
        background: linear-gradient(135deg, var(--primary), var(--accent));
        color: white;
        border: none;
        padding: 14px 28px;
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        margin: 12px 0;
        cursor: pointer;
        border-radius: 50px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(64, 93, 230, 0.3);
        animation: pulse 2s infinite;
    }
    
    .button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(64, 93, 230, 0.4);
        animation: none;
    }
    
    .social-button {
        display: inline-block;
        padding: 12px 24px;
        margin: 8px;
        border-radius: 50px;
        font-weight: 600;
        transition: all 0.3s ease;
        color: white !important;
        text-align: center;
        min-width: 120px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .social-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .instagram { background: var(--instagram); }
    .facebook { background: var(--facebook); }
    .twitter { background: var(--twitter); }
    .tiktok { 
        background: var(--tiktok); 
        position: relative;
        overflow: hidden;
    }
    
    .tiktok::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 2s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 150%; }
    }
    
    .points-display {
        font-size: 28px;
        text-align: center;
        margin: 30px 0;
        padding: 25px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        animation: fadeIn 0.6s ease-out;
        border-left: 5px solid var(--accent);
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .certificate-preview {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        margin: 25px 0;
        animation: fadeIn 0.8s ease-out;
    }
    
    .customization-option {
        padding: 15px;
        background: rgba(255,255,255,0.7);
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        animation: gradient 3s ease infinite;
        background-size: 200% 200% !important;
    }
    
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ffd700, #ff9800);
        color: #000;
        padding: 5px 10px;
        border-radius: 20px;
        font-weight: bold;
        margin: 0 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .download-btn {
        background: linear-gradient(135deg, #4CAF50, #2E7D32) !important;
        animation: pulse 1.5s infinite !important;
    }
    
    .download-btn:hover {
        background: linear-gradient(135deg, #388E3C, #1B5E20) !important;
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #f00;
        border-radius: 50%;
        animation: confetti-fall 5s linear infinite;
    }
    
    @keyframes confetti-fall {
        0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_active' not in st.session_state:
    st.session_state.session_active = False
    st.session_state.start_time = None
    st.session_state.points = 0
    st.session_state.total_time = 0
    st.session_state.platform = None
    st.session_state.sessions = []
    st.session_state.achievements = []
    st.session_state.certificate_customized = False
    st.session_state.certificate_generated = False
    st.session_state.certificate_data = {
        "name": "Anonymous Scroller",
        "title": "Certified Time Waster",
        "theme": "modern",
        "badge": "scroll"
    }

# Certificate templates
TEMPLATES = {
    "modern": {
        "bg_color": (255, 253, 245),
        "border_color": (64, 93, 230),
        "title_color": (64, 93, 230),
        "name_color": (131, 58, 180),
        "stats_color": (225, 48, 108),
        "footer_color": (100, 100, 100),
        "accent_color": (200, 200, 200)
    },
    "vintage": {
        "bg_color": (248, 240, 227),
        "border_color": (139, 69, 19),
        "title_color": (139, 69, 19),
        "name_color": (101, 67, 33),
        "stats_color": (188, 143, 143),
        "footer_color": (120, 90, 60),
        "accent_color": (169, 169, 169)
    },
    "dark": {
        "bg_color": (30, 30, 40),
        "border_color": (128, 0, 128),
        "title_color": (64, 224, 208),
        "name_color": (255, 215, 0),
        "stats_color": (50, 205, 50),
        "footer_color": (180, 180, 180),
        "accent_color": (100, 100, 150)
    }
}

TITLES = [
    "Certified Time Waster",
    "Master Procrastinator",
    "Doomscroll Expert",
    "Professional Scroller",
    "Chief Meme Officer",
    "Infinite Scroll Champion",
    "Digital Time Bandit",
    "Notification Ninja",
    "Social Media Sensei",
    "Scroll Sultan"
]

BADGES = {
    "scroll": "📜",
    "clock": "⏰",
    "phone": "📱",
    "trophy": "🏆",
    "crown": "👑",
    "zap": "⚡",
    "fire": "🔥",
    "star": "⭐",
    "medal": "🎖️",
    "ghost": "👻"
}

ACHIEVEMENTS = [
    {"name": "First Scroll", "points": 50, "emoji": "🥉", "desc": "First time wasting session"},
    {"name": "Hour Waster", "points": 300, "emoji": "⏳", "desc": "Wasted 1 hour total"},
    {"name": "Social Butterfly", "points": 500, "emoji": "🦋", "desc": "Used 3+ platforms"},
    {"name": "Night Owl", "points": 200, "emoji": "🦉", "desc": "Scrolled after midnight"},
    {"name": "Weekend Warrior", "points": 400, "emoji": "🏆", "desc": "5+ sessions on weekend"}
]

# Certificate generator function
def generate_certificate(name, points, time_wasted, platform, title, theme, badge):
    template = TEMPLATES.get(theme, TEMPLATES["modern"])
    img = Image.new('RGB', (1000, 700), color=template["bg_color"])
    d = ImageDraw.Draw(img)
    
    # Add decorative border
    d.rectangle([(50, 50), (950, 650)], outline=template["border_color"], width=8)
    
    # Title with gradient effect
    title_font = ImageFont.truetype("arial.ttf", 48)
    d.text((500, 120), title.upper(), 
           fill=template["title_color"], font=title_font, anchor="mm")
    
    # Main text
    main_font = ImageFont.truetype("arial.ttf", 32)
    d.text((500, 220), f"This certifies that", 
           fill=template["name_color"], font=main_font, anchor="mm")
    
    d.text((500, 280), f"{name.upper()}", 
           fill=template["name_color"], font=main_font, anchor="mm")
    
    d.text((500, 360), f"has successfully wasted {time_wasted} minutes", 
           fill=template["name_color"], font=main_font, anchor="mm")
    
    d.text((500, 420), f"scrolling on {platform}", 
           fill=template["stats_color"], font=main_font, anchor="mm")
    
    d.text((500, 480), f"and earned {points} ScrollPoints", 
           fill=template["stats_color"], font=main_font, anchor="mm")
    
    # Badge
    badge_font = ImageFont.truetype("arial.ttf", 80)
    d.text((500, 560), BADGES[badge], 
           fill=template["title_color"], font=badge_font, anchor="mm")
    
    # Footer
    footer_font = ImageFont.truetype("arial.ttf", 24)
    d.text((500, 620), "Presented by ScrollPoints Academy", 
           fill=template["footer_color"], font=footer_font, anchor="mm")
    
    d.text((800, 650), datetime.now().strftime("%Y-%m-%d"), 
           fill=template["footer_color"], font=footer_font)
    
    # Add decorative elements
    for i in range(20):
        x = random.randint(60, 940)
        y = random.randint(60, 640)
        r = random.randint(2, 8)
        d.ellipse([(x, y), (x+r, y+r)], fill=template["accent_color"])
    
    img_path = f"certificate_{name}_{int(time.time())}.png"
    img.save(img_path)
    return img_path

def create_confetti_effect():
    confetti_html = ""
    for i in range(50):
        color = random.choice(["#FF5252", "#FFD740", "#64FFDA", "#448AFF", "#E040FB"])
        size = random.randint(5, 10)
        left = random.randint(0, 100)
        delay = random.uniform(0, 5)
        duration = random.uniform(3, 8)
        
        confetti_html += f"""
        <div class="confetti" style="
            width: {size}px;
            height: {size}px;
            background: {color};
            left: {left}%;
            top: -20px;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
        "></div>
        """
    return confetti_html

def check_achievements(points, time_wasted, sessions):
    new_achievements = []
    for achievement in ACHIEVEMENTS:
        if achievement not in st.session_state.achievements:
            if achievement["name"] == "First Scroll" and len(sessions) > 0:
                new_achievements.append(achievement)
            elif achievement["name"] == "Hour Waster" and time_wasted >= 60:
                new_achievements.append(achievement)
            elif achievement["name"] == "Social Butterfly" and len(set(session["platform"] for session in sessions)) >= 3:
                new_achievements.append(achievement)
            elif achievement["name"] == "Night Owl" and any(session["start_hour"] >= 0 for session in sessions):
                new_achievements.append(achievement)
            elif achievement["name"] == "Weekend Warrior" and len([s for s in sessions if s["is_weekend"]]) >= 5:
                new_achievements.append(achievement)
    
    return new_achievements

# Main app interface
st.markdown("""
    <div class="header">
        <h1 class="floating">📱 ScrollPoints</h1>
        <p>Turn your social media scrolling into academic credit!</p>
    </div>
""", unsafe_allow_html=True)

# Social media selection
st.markdown("### 🚀 Start Your Scrolling Journey")
st.markdown("Select your preferred time-wasting platform:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.markdown(f"""
        <div class="social-button instagram" onclick="window.open('https://www.instagram.com/')">
            <div style="display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 24px; margin-right: 8px;">📸</span>
                Instagram
            </div>
        </div>
    """, unsafe_allow_html=True):
        st.session_state.platform = "Instagram"

with col2:
    if st.markdown(f"""
        <div class="social-button facebook" onclick="window.open('https://www.facebook.com/')">
            <div style="display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 24px; margin-right: 8px;">👍</span>
                Facebook
            </div>
        </div>
    """, unsafe_allow_html=True):
        st.session_state.platform = "Facebook"

with col3:
    if st.markdown(f"""
        <div class="social-button twitter" onclick="window.open('https://twitter.com/')">
            <div style="display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 24px; margin-right: 8px;">🐦</span>
                Twitter
            </div>
        </div>
    """, unsafe_allow_html=True):
        st.session_state.platform = "Twitter"

with col4:
    if st.markdown(f"""
        <div class="social-button tiktok" onclick="window.open('https://www.tiktok.com/')">
            <div style="display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 24px; margin-right: 8px;">🎵</span>
                TikTok
            </div>
        </div>
    """, unsafe_allow_html=True):
        st.session_state.platform = "TikTok"

# Session control
if st.session_state.platform and not st.session_state.session_active:
    if st.button(f"🚀 Start {st.session_state.platform} Session", key="start", use_container_width=True):
        st.session_state.session_active = True
        st.session_state.start_time = time.time()
        st.rerun()

if st.session_state.session_active:
    elapsed = time.time() - st.session_state.start_time
    points = int(elapsed // 60) * 10  # 10 points per minute
    
    st.markdown(f"""
        <div class="points-display">
            ⏱️ <strong>Time wasted:</strong> {int(elapsed//60)}m {int(elapsed%60)}s<br>
            🏆 <strong>Points earned:</strong> {points}<br>
            📱 <strong>Platform:</strong> {st.session_state.platform}
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("⏹️ End Session & Collect Points", key="end", use_container_width=True):
        st.session_state.session_active = False
        st.session_state.points += points
        
        session_data = {
            "platform": st.session_state.platform,
            "duration": elapsed,
            "points": points,
            "start_time": st.session_state.start_time,
            "end_time": time.time(),
            "start_hour": datetime.now().hour,
            "is_weekend": datetime.now().weekday() >= 5
        }
        st.session_state.sessions.append(session_data)
        st.session_state.total_time += elapsed
        
        # Check for achievements
        new_achievements = check_achievements(
            st.session_state.points,
            st.session_state.total_time // 60,
            st.session_state.sessions
        )
        
        for achievement in new_achievements:
            st.session_state.achievements.append(achievement)
            st.toast(f"🎉 Achievement Unlocked: {achievement['emoji']} {achievement['name']}!")
        
        st.rerun()

# Stats display
st.markdown("### 📊 Your Wasting Stats")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total ScrollPoints</h3>
            <p style="font-size: 32px; color: var(--accent);">{st.session_state.points}</p>
            <p>Earned through {len(st.session_state.sessions)} sessions</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <h3>Total Time Wasted</h3>
            <p style="font-size: 32px; color: var(--accent);">{int(st.session_state.total_time//60)} minutes</p>
            <p>{int(st.session_state.total_time//3600)} hours of quality procrastination</p>
        </div>
    """, unsafe_allow_html=True)

# Achievements display
if st.session_state.achievements:
    st.markdown("### 🏆 Your Achievements")
    cols = st.columns(3)
    for i, achievement in enumerate(st.session_state.achievements):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 32px; text-align: center;">{achievement['emoji']}</div>
                    <h3 style="text-align: center;">{achievement['name']}</h3>
                    <p style="text-align: center;">{achievement['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

# Certificate generation
st.divider()
st.markdown("## 🎨 Customize Your Certificate")

with st.expander("Certificate Customization", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", st.session_state.certificate_data["name"])
        title = st.selectbox("Certificate Title", TITLES, index=TITLES.index(st.session_state.certificate_data["title"]))
        
    with col2:
        theme = st.selectbox("Design Theme", list(TEMPLATES.keys()), index=list(TEMPLATES.keys()).index(st.session_state.certificate_data["theme"]))
        badge = st.selectbox("Achievement Badge", list(BADGES.keys()), format_func=lambda x: f"{BADGES[x]} {x.capitalize()}", 
                            index=list(BADGES.keys()).index(st.session_state.certificate_data["badge"]))
    
    st.session_state.certificate_data = {
        "name": name,
        "title": title,
        "theme": theme,
        "badge": badge
    }
    st.session_state.certificate_customized = True

if st.button("✨ Generate Certificate", key="generate", use_container_width=True, 
            disabled=st.session_state.total_time == 0):
    if st.session_state.total_time > 0 and st.session_state.platform:
        time_wasted = int(st.session_state.total_time // 60)
        cert_path = generate_certificate(
            st.session_state.certificate_data["name"],
            st.session_state.points,
            time_wasted,
            st.session_state.platform,
            st.session_state.certificate_data["title"],
            st.session_state.certificate_data["theme"],
            st.session_state.certificate_data["badge"]
        )
        
        st.session_state.certificate_path = cert_path
        st.session_state.certificate_generated = True
        st.toast("🎉 Your certificate is ready! Scroll down to download")
        st.rerun()
    else:
        st.warning("You need to complete at least one scrolling session first!")

if st.session_state.get('certificate_generated', False):
    st.divider()
    st.markdown("## 📜 Your ScrollPoints Certificate")
    
    st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <h3>{st.session_state.certificate_data['title']}</h3>
            <p>Customized for {st.session_state.certificate_data['name']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.image(st.session_state.certificate_path, use_container_width=True, caption="Your Official Time Waster Certificate")
    
    with col2:
        st.markdown("### Certificate Details")
        st.markdown(f"""
            - **Recipient:** {st.session_state.certificate_data['name']}
            - **Title:** {st.session_state.certificate_data['title']}
            - **Design:** {st.session_state.certificate_data['theme'].capitalize()} Theme
            - **Achievement Badge:** {BADGES[st.session_state.certificate_data['badge']]}
            - **Total Points:** {st.session_state.points}
            - **Time Wasted:** {int(st.session_state.total_time//60)} minutes
            - **Favorite Platform:** {st.session_state.platform}
        """)
        
        st.download_button(
            label="⬇️ Download Certificate",
            data=open(st.session_state.certificate_path, "rb").read(),
            file_name=f"ScrollPoints_Certificate_{st.session_state.certificate_data['name']}.png",
            mime="image/png",
            use_container_width=True,
            key="download_cert",
            type="primary",
            help="Download your certificate as a PNG file"
        )
        
        st.markdown("### Share Your Achievement")
        st.markdown("""
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
                <button style="background: #1877F2; color: white; border: none; border-radius: 50px; padding: 10px 20px;">
                    Share on Facebook
                </button>
                <button style="background: #1DA1F2; color: white; border: none; border-radius: 50px; padding: 10px 20px;">
                    Share on Twitter
                </button>
            </div>
        """, unsafe_allow_html=True)
    
    # Confetti effect
    st.markdown(create_confetti_effect(), unsafe_allow_html=True)

# Progress to next achievement
if st.session_state.achievements and len(st.session_state.achievements) < len(ACHIEVEMENTS):
    st.divider()
    st.markdown("### 🚀 Your Progress to Next Achievement")
    
    next_achievement = next(
        (a for a in ACHIEVEMENTS if a not in st.session_state.achievements), 
        None
    )
    
    if next_achievement:
        if next_achievement["name"] == "First Scroll":
            progress = 1 if st.session_state.sessions else 0
        elif next_achievement["name"] == "Hour Waster":
            progress = min(st.session_state.total_time / 3600, 1)
        elif next_achievement["name"] == "Social Butterfly":
            unique_platforms = len(set(session["platform"] for session in st.session_state.sessions))
            progress = min(unique_platforms / 3, 1)
        elif next_achievement["name"] == "Night Owl":
            progress = 1 if any(session["start_hour"] >= 0 for session in st.session_state.sessions) else 0
        elif next_achievement["name"] == "Weekend Warrior":
            weekend_sessions = len([s for s in st.session_state.sessions if s["is_weekend"]])
            progress = min(weekend_sessions / 5, 1)
        
        st.progress(progress)
        st.markdown(f"""
            <div style="text-align: center; margin-top: 10px;">
                <span class="achievement-badge">Next: {next_achievement['emoji']} {next_achievement['name']}</span>
                <p>{next_achievement['desc']}</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #777; margin-top: 30px;">
        <p>📱 ScrollPoints - Celebrating Your Procrastination Since 2023</p>
        <p>Disclaimer: This is a satirical project. Actual time wasting not encouraged.</p>
    </div>
""", unsafe_allow_html=True)