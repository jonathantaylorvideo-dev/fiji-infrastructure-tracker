# 🇫🇯 Fiji Infrastructure Voice-to-GIS Tracker
### **Project Status: Version 1.2 (Active Field Pilot)**
**Target Agency:** Ministry of Rural and Maritime Development, Fiji  
**Live Demo:** [https://fiji-infrastructure-tracker-dsnaph6p98uzg7nteaapmp.streamlit.app/]

## 📋 Executive Summary
This application is a **Voice-First AI Pipeline** designed to solve data-entry bottlenecks in remote maritime regions. This solution allows agents to submit **natural language voice reports**. The system uses a multimodal AI engine to parse audio into structured geospatial data, providing national-level oversight via a real-time GIS dashboard.

## 🚀 Phase 1: Active Field Pilots (Current)
The following projects are currently live in the tracking database:
1.  **Lau Group Solar Array** (Eastern) — *Successfully handled 180° Longitude Logic*
2.  **Suva Port Expansion** (Central) — *Urban Infrastructure baseline*

## 🏗️ Phase 2: National Expansion (Planned)
The following projects are identified as the next priority for the voice-to-data rollout:
1.  **Koro Island Water Catchment** (Lomaiviti)
2.  **Taveuni Agricultural Hub** (Northern)
3.  **Vanua Levu Roadworks** (Northern)

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **Framework:** Streamlit
* **AI/LLM:** Google Gemini API (Multimodal Audio Parsing)
* **Database:** Supabase (PostgreSQL)
* **Mapping:** Folium & Esri Satellite Imagery

---

## 🛰️ Strategic Roadmap
For detailed technical specifications on the **Audit Queue**, **Automated Procurement**, and **Supply Chain Routing**, please refer to the **[PHASE_2.md](./PHASE_2.md)** file.

**Upcoming Technical Milestones:**
* **Automated Procurement:** Voice-triggered supply requests routed to logistics agents after audit.
* **Supervisor Audit Queue:** A "Human-in-the-Loop" verification gateway for all field data.
* **Role-Based Security:** Secure login for Ministry Officials and Field Agents via Supabase Auth.
* **Offline Mode:** Edge-caching of audio reports for "Zero-Signal" zones in the Outer Islands.
