import streamlit as st
import pandas as pd
import requests
import json
import base64
from supabase import create_client
from streamlit_folium import st_folium
import folium

# --- 1. CONFIGURATION (SECURE VERSION) ---
# We pull these from the "Advanced Settings > Secrets" menu in Streamlit Cloud
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
except Exception as e:
    st.error("Missing Secrets! Please add SUPABASE_URL, SUPABASE_KEY, and GEMINI_KEY to Streamlit Secrets.")
    st.stop()

# Initialize Supabase
db = create_client(SUPABASE_URL, SUPABASE_KEY)

OFFICIAL_PROJECT_REGISTRY = ["Koro Island Water Catchment", "Lau Group Solar Array", "Taveuni Agricultural Hub", "Vanua Levu Roadworks", "Suva Port Expansion"]

PROJECT_LOCATIONS = {
    "Koro Island Water Catchment": {"lat": -17.3106, "lon": 179.4067},
    "Lau Group Solar Array": {"lat": -18.2000, "lon": 181.2000}, # This 'unwraps' the map
    "Taveuni Agricultural Hub": {"lat": -16.8286, "lon": 179.9441},
    "Vanua Levu Roadworks": {"lat": -16.5917, "lon": 179.1833},
    "Suva Port Expansion": {"lat": -18.1416, "lon": 178.4419}
}

# --- 2. SIDEBAR CONTROLS ---
st.set_page_config(page_title="Ministry Project Tracker", layout="wide", page_icon="🇫🇯")
st.sidebar.title("🛠️ Command Controls")

map_choice = st.sidebar.radio(
    "Select Map View:",
    ("Standard Road", "Satellite Terrain")
)

# --- 3. THE DASHBOARD & FOLIUM MAP ---
st.title("🇫🇯 Fiji Infrastructure Command Center")
col_map, col_progress = st.columns([2, 1])

# A. Initialize the Map Variable FIRST so it always exists
tiles = 'OpenStreetMap' if map_choice == "Standard Road" else 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
attr = 'Esri' if map_choice == "Satellite Terrain" else 'OpenStreetMap'

# Center the map to catch the Lau Group (179.0 is the sweet spot)
m = folium.Map(location=[-18.0, 179.0], zoom_start=6, tiles=tiles, attr=attr)

# B. Try to get Data from Supabase
try:
    res = db.table("reports").select("*").order("created_at", desc=True).execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
except Exception as e:
    st.error(f"Database Connection Error: {e}")
    df = pd.DataFrame() # Fallback to empty so the map still draws

# C. Draw the Dots (The "5-Dot Guarantee")
with col_map:
    st.subheader(f"🌐 Geographic Status: {map_choice}")
    
    for proj, coords in PROJECT_LOCATIONS.items():
        # Look for the latest update for this specific project
        if not df.empty and proj in df['project_name'].values:
            proj_row = df[df['project_name'] == proj].iloc[0]
            pct = int(proj_row['status_percent'])
        else:
            pct = 0 # Default if no data exists yet
        
        # Color logic
        color = "gray" if pct == 0 else "red" if pct < 30 else "orange" if pct < 80 else "blue"
        
        folium.CircleMarker(
            location=[coords["lat"], coords["lon"]],
            radius=(pct / 5) + 10, # Minimum size 10 so it's clickable
            popup=f"{proj}: {pct}%",
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6
        ).add_to(m)

    # Render the map
    st_folium(m, width=700, height=500, key=f"fiji_map_{len(df)}")

with col_progress:
    st.subheader("📊 Completion Status")
    for project in OFFICIAL_PROJECT_REGISTRY:
        if not df.empty and project in df['project_name'].values:
            val = int(df[df['project_name'] == project].iloc[0]['status_percent'])
        else:
            val = 0
        st.write(f"**{project}**")
        st.progress(val / 100, text=f"{val}%")
    
# --- 4. VOICE UPLINK & AI PROCESSING ---
st.subheader("🎙️ Send Field Update")
audio_file = st.audio_input("Record Update")

if audio_file:
    with st.status("📡 Processing Satellite Uplink...", expanded=True) as status:
        try:
            audio_bytes = audio_file.read()
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
            prompt_text = f"Extract 'project_name' (from {OFFICIAL_PROJECT_REGISTRY}), 'status_percent', and 'original_transcript' as JSON."
            payload = {"contents": [{"parts": [{"text": prompt_text}, {"inline_data": {"mime_type": "audio/wav", "data": audio_b64}}]}]}
            response = requests.post(url, json=payload)
            res_json = response.json()
            if 'candidates' in res_json:
                raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
                clean_json = raw_text.replace("```json", "").replace("```", "").strip()
                
                # 1. Insert the data
                db.table("reports").insert(json.loads(clean_json)).execute()
                
                # 2. Update the UI status
                status.update(label="✅ Satellite Sync Complete!", state="complete")
                st.balloons()
                
                # 3. CRITICAL: Force the whole app to refresh so the Map reads the new DB row
                st.rerun()
                # This tells Streamlit: "If the number of rows in my data changes, redraw this map"
                st_folium(m, width=700, height=500, key=f"map_{len(df)}") 
                st.rerun()
        except Exception as e:
            st.error(f"Uplink Error: {e}")

# --- 5. DATA LOG ---
st.divider()
st.subheader("📋 Raw Transmission Log")
try:
    log_res = db.table("reports").select("*").order("created_at", desc=True).limit(5).execute()
    if log_res.data: st.table(log_res.data)
except: st.caption("Awaiting field data...")
