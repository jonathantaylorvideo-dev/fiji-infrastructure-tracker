# fiji-infrastructure-tracker
-----

# 🇫🇯 Fiji Infrastructure Command Center

### **Voice-to-GIS Field Reporting System**

[](https://share.streamlit.io/)
[](https://ai.google.dev/)
[](https://supabase.com/)

## 📖 Overview

The **Fiji Infrastructure Command Center** is a multimodal AI agent designed to bridge the gap between remote field workers and central government planning. In many maritime environments like the Fiji Islands, manual data entry is slow and error-prone.

This system allows field engineers to record **voice updates**, which are then synthesized by **Gemini 2.5 Flash**, validated against an official project registry, and plotted instantly onto a **Satellite GIS Dashboard**.

## 🚀 Key Features

  * **Voice-First Interface:** Uses `st.audio_input` to capture field reports, reducing administrative overhead for engineers in the field.
  * **AI Synthesis:** Leverages Gemini 2.5 Flash to extract structured JSON data (Project Name, Completion %, Transcript) from raw audio.
  * **Geospatial Intelligence:** Interactive Folium-based map with **Satellite/Road view switching** and color-coded "Health Bubbles" (Red: At Risk, Orange: Active, Cyan: Complete).
  * **Real-time Persistence:** Powered by a Supabase backend for instant synchronization across all Ministry stakeholders.
  * **Vibe Coding Architecture:** Built using high-automation tools for rapid prototyping and deployment.

## 🛠️ Tech Stack

  * **Frontend:** [Streamlit](https://streamlit.io/)
  * **AI/LLM:** [Google Gemini 2.5 Flash](https://ai.google.dev/) (Multimodal Audio-to-JSON)
  * **Database:** [Supabase](https://supabase.com/) (PostgreSQL with Service Role security)
  * **Mapping:** [Folium](https://python-visualization.github.io/folium/) & [Esri World Imagery](https://www.esri.com/)
  * **Language:** Python 3.11+

## 📥 Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/fiji-infrastructure-tracker.git
    cd fiji-infrastructure-tracker
    ```

2.  **Install dependencies:**

    ```bash
    pip install streamlit pandas requests supabase streamlit-folium folium
    ```

3.  **Configure Environment:**
    Ensure your `SUPABASE_KEY` and `GEMINI_KEY` are correctly placed in the `app.py` or managed via Streamlit Secrets.

4.  **Run the App:**

    ```bash
    streamlit run app.py
    ```

## 📋 Data Schema (Supabase)

To replicate this project, create a table named `reports` with the following columns:

  * `id`: int8 (Primary Key)
  * `created_at`: timestamptz (Default: now())
  * `project_name`: text
  * `status_percent`: int4
  * `original_transcript`: text

-----
