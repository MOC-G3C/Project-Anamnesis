# anamnesis_demo.py
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="ANAMNESIS - Traumatic Memory Simulator", layout="wide")

# HEADER
st.title("🧠 ANAMNESIS Engine")
st.markdown("**Topological Memory for NPCs - Give Your Characters PTSD**")

# SIDEBAR CONTROLS
st.sidebar.header("Simulation Parameters")

num_agents = st.sidebar.slider("Number of NPCs", 2, 6, 4)
trauma_strength = st.sidebar.slider("Trauma Intensity", 0.1, 2.0, 1.0)
simulation_time = st.sidebar.slider("Simulation Duration", 10, 100, 50)

# TRAUMA EVENT SELECTOR
trauma_type = st.sidebar.selectbox(
    "Trauma Type",
    ["Betrayal", "Violence Witnessed", "Loss of Ally", "Territory Invasion"]
)

# RUN BUTTON
if st.sidebar.button("🔥 Simulate Trauma Event"):
    
    # PLACEHOLDER POUR TON CODE
    # Ici tu vas copier ton code anamnesis_core.py
    # et générer les résultats
    
    st.success(f"✅ Simulated {trauma_type} with intensity {trauma_strength}")
    
    # VISUALIZATION
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Agent Relationships (Before)")
        # Graphique réseau AVANT trauma
        
    with col2:
        st.subheader("Agent Relationships (After)")
        # Graphique réseau APRÈS trauma
        # Avec la cicatrice visible
    
    # METRICS
    st.subheader("📊 Impact Metrics")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("Topological Scar Strength", "0.85", "+0.45")
    
    with metric_col2:
        st.metric("System Resilience", "73%", "-12%")
    
    with metric_col3:
        st.metric("Recovery Time", "∞", "Irreversible")
    
    # EXPORT
    st.download_button(
        label="📥 Download Results (JSON)",
        data='{"scar": 0.85, "agents": 4}',  # Remplacer par vraies données
        file_name=f"anamnesis_sim_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    )

# FOOTER
st.markdown("---")
st.markdown("""
### Use Cases
- **RPGs:** NPCs who remember player betrayals
- **Strategy Games:** AI allies who form permanent grudges
- **Social Sims:** Characters with realistic trauma responses

### Cite This Work
```
@software{corbin2026anamnesis,
  author = {Corbin, Marc-Olivier},
  title = {ANAMNESIS: Topological Memory Engine},
  year = {2026},
  url = {github.com/MOC-G3C/anamnesis}
}
```
""")
