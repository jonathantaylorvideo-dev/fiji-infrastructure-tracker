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
    "Lau Group Solar Array": {"lat": -18.2000, "lon": -178.8000},
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

try:
    res = db.table("reports").select("*").order("created_at", desc=True).execute()
    if res.data:
        df = pd.DataFrame(res.data)
        df['status_percent'] = pd.to_numeric(df['status_percent'], errors='coerce').fillna(0)
        latest_updates = df.sort_values('created_at').groupby('project_name').tail(1)

        with col_map:
            st.subheader(f"🌐 Geographic Status: {map_choice}")
            
            tiles = 'OpenStreetMap' if map_choice == "Standard Road" else 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
            attr = 'Esri' if map_choice == "Satellite Terrain" else 'OpenStreetMap'
            
            m = folium.Map(location=[-17.7134, 178.0650], zoom_start=7, tiles=tiles, attr=attr)

            for proj, coords in PROJECT_LOCATIONS.items():
                row = latest_updates[latest_updates['project_name'] == proj]
                pct = int(row.iloc[0]['status_percent']) if not row.empty else 0
                color = "red" if pct < 30 else "orange" if pct < 80 else "blue"
                
                folium.CircleMarker(
                    location=[coords["lat"], coords["lon"]],
                    radius=(pct / 5) + 5,
                    popup=f"{proj}: {pct}%",
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.6
                ).add_to(m)

            st_folium(m, width=700, height=500)
            
        with col_progress:
            st.subheader("📊 Completion Status")
            for project in OFFICIAL_PROJECT_REGISTRY:
                row = latest_updates[latest_updates['project_name'] == project]
                pct = int(row.iloc[0]['status_percent']) if not row.empty else 0
                st.write(f"**{project}**")
                st.progress(pct / 100, text=f"{pct}%")
except Exception as e:
    st.error(f"Map Rendering Error: {e}")

st.divider()

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
                db.table("reports").insert(json.loads(clean_json)).execute()
                status.update(label="✅ Data Archived!", state="complete")
                st.balloons()
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