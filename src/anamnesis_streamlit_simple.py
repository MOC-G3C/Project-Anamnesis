import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

st.set_page_config(page_title="ANAMNESIS Demo", layout="wide")

# === TITRE ===
st.title("🧠 ANAMNESIS - Topological Trauma Memory")
st.markdown("*NPCs that remember psychological scars forever*")

# === SIDEBAR ===
st.sidebar.header("Simulation Settings")

trauma_event = st.sidebar.selectbox(
    "Trauma Type",
    ["Player Betrayal", "Ally Killed", "Territory Lost", "Promise Broken"]
)

intensity = st.sidebar.slider("Trauma Intensity", 1, 10, 5)

# === SIMULATION (Version TRES Simplifiée) ===
if st.sidebar.button("🔥 Simulate Trauma", type="primary"):
    
    # Simulation simplifiée
    agents = ["Warrior", "Diplomat", "Scout", "Leader"]
    
    # États AVANT
    relationships_before = np.array([
        [0, 0.5, 0.3, 0.7],  # Warrior relationships
        [0.5, 0, 0.6, 0.4],  # Diplomat
        [0.3, 0.6, 0, 0.2],  # Scout
        [0.7, 0.4, 0.2, 0]   # Leader
    ])
    
    # États APRÈS (Leader traumatisé)
    trauma_impact = intensity / 10.0
    relationships_after = relationships_before.copy()
    
    # Le trauma crée une cicatrice entre Leader et les autres
    relationships_after[3, :] *= (1 - trauma_impact * 0.5)  # Leader distance everyone
    relationships_after[:, 3] *= (1 - trauma_impact * 0.3)  # Others fear Leader
    relationships_after[3, 0] += trauma_impact * 0.8  # Scar with Warrior (dependency)
    
    # Calcul de la cicatrice
    scar_strength = np.abs(relationships_after[3, 0] - relationships_before[3, 0])
    
    st.success(f"✅ Trauma simulated: **{trauma_event}**")
    
    # === VISUALISATION ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Before Trauma")
        fig1, ax1 = plt.subplots(figsize=(6, 6), facecolor='black')
        ax1.set_facecolor('black')
        
        # Heatmap simplifiée
        im = ax1.imshow(relationships_before, cmap='Blues', vmin=0, vmax=1)
        ax1.set_xticks(range(4))
        ax1.set_yticks(range(4))
        ax1.set_xticklabels(agents, color='white')
        ax1.set_yticklabels(agents, color='white')
        plt.colorbar(im, ax=ax1)
        
        st.pyplot(fig1)
    
    with col2:
        st.subheader("After Trauma")
        fig2, ax2 = plt.subplots(figsize=(6, 6), facecolor='black')
        ax2.set_facecolor('black')
        
        im = ax2.imshow(relationships_after, cmap='hot', vmin=0, vmax=1)
        ax2.set_xticks(range(4))
        ax2.set_yticks(range(4))
        ax2.set_xticklabels(agents, color='white')
        ax2.set_yticklabels(agents, color='white')
        plt.colorbar(im, ax=ax2)
        
        # Highlight scar
        ax2.add_patch(plt.Rectangle((0-0.5, 3-0.5), 1, 1, 
                                    fill=False, edgecolor='red', lw=3))
        
        st.pyplot(fig2)
    
    # === METRICS ===
    st.subheader("📊 Psychological Impact")
    
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Topological Scar", f"{scar_strength:.2f}", 
                 delta=f"+{scar_strength:.2f}", delta_color="inverse")
    
    with m2:
        recovery = "∞ (Permanent)" if scar_strength > 0.5 else f"{int(scar_strength*200)} interactions"
        st.metric("Recovery Time", recovery)
    
    with m3:
        trust_loss = int(scar_strength * 100)
        st.metric("Trust Loss", f"{trust_loss}%", delta=f"-{trust_loss}%", delta_color="inverse")
    
    # === EXPLANATION ===
    with st.expander("🧬 What happened?"):
        st.markdown(f"""
        **Event:** {trauma_event} (Intensity {intensity}/10)
        
        **Topological Changes:**
        - Leader's trust in all agents decreased by {int(trauma_impact*50)}%
        - A **permanent scar** formed between Leader and Warrior (dependency bond)
        - This scar is **irreversible** - no amount of positive interactions can fully erase it
        
        **Physical Analogy:**
        Think of relationships as elastic bands. The trauma stretched the Leader-Warrior 
        band so hard it left a permanent deformation. The band still works, but it's 
        never the same shape again.
        
        **Game Design Implication:**
        If this were an RPG, the Leader NPC would now:
        - Refuse certain quests from the player
        - Demand higher payment for cooperation
        - Occasionally have trust breakdowns (random negative events)
        """)
    
    # === EXPORT ===
    export_data = {
        "trauma_type": trauma_event,
        "intensity": intensity,
        "scar_strength": float(scar_strength),
        "relationships_before": relationships_before.tolist(),
        "relationships_after": relationships_after.tolist()
    }
    
    st.download_button(
        "📥 Download Simulation Data",
        data=json.dumps(export_data, indent=2),
        file_name=f"anamnesis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

# === FOOTER ===
st.markdown("---")

col_a, col_b = st.columns([2, 1])

with col_a:
    st.markdown("""
    ### 🎮 Gaming Applications
    
    **Traditional Reputation Systems:**
    - Kill NPC's friend → Reputation -50
    - Give 10 gifts → Reputation +50
    - Result: Relationship restored
    
    **ANAMNESIS Approach:**
    - Kill NPC's friend → **Permanent topological scar**
    - Give 1000 gifts → Relationship improves BUT scar remains
    - Result: NPC trusts you for trade, but **never** for life-or-death decisions
    
    This creates **emergent psychology** - NPCs feel real because they have **irreversible histories**.
    """)

with col_b:
    st.markdown("""
    ### 📚 Citation
```
    @software{anamnesis2026,
      author = {Corbin, Marc-Olivier},
      title = {ANAMNESIS Engine},
      year = {2026},
      url = {github.com/MOC-G3C/
             Project-Anamnesis}
    }
```
    
    **License:** MIT  
    **Author:** MOC-G3C  
    **Location:** Montréal, QC
    """)

st.markdown("*Built with Streamlit, NumPy, Matplotlib | Based on Landau phase transition theory*")
