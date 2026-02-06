import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import json

st.set_page_config(page_title="ANAMNESIS - NPC Trauma Simulator", layout="wide")

# === PARAMS (copiés de ton core) ===
POSITIONS_INIT = np.array([
    [1.0, 1.0, 1.0],
    [1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, 1.0]
]) * 1.8

num_agents = 4

PARAMS = {
    'steps': 300,  # Réduit pour Streamlit
    'dt': 0.05,
    'tau_decay': 15.0,
    'eta': 0.1,
    'tau_min': 100.0,
    'tau_max': 2000.0,
    'gamma': 2.5,
    'lambda_c': 1.2,
    'kappa': 0.5,
    'mu': 5.0,
    'friction': 0.15,
    'agents': [
        {'name': 'Warrior', 'Tc': 4.0, 'alpha': 0.0, 'freq': 0.05, 'color': '#00ffff'},
        {'name': 'Diplomat', 'Tc': 0.8, 'alpha': 0.6, 'freq': 0.08, 'color': '#ffaa00'},
        {'name': 'Scout', 'Tc': 1.5, 'alpha': 0.8, 'freq': 0.11, 'color': '#55ff55'},
        {'name': 'Leader', 'Tc': 0.5, 'alpha': 1.2, 'freq': 0.14, 'color': '#ff00ff'}
    ]
}

# === FONCTIONS (copiées de ton core) ===
def calculate_entropy(resonances):
    total_r = np.sum(resonances)
    if total_r < 1e-6: return 1.0
    probs = resonances / total_r
    probs = probs[probs > 0]
    if len(probs) <= 1: return 0.0
    entropy = -np.sum(probs * np.log(probs))
    max_entropy = np.log(len(resonances))
    return entropy / max_entropy

def internal_dynamics(theta, stress, Tc, alpha, tau, dt):
    decay = -theta / tau
    plasticity = alpha * (1.0 if stress > Tc else 0.0) * (stress - Tc)
    return theta + (decay + plasticity) * dt

def run_simulation(trauma_frame, trauma_intensity):
    """Simulation complète avec trauma"""
    positions = POSITIONS_INIT.copy()
    velocities = np.zeros_like(positions)
    states = np.zeros(num_agents)
    phases = np.zeros(num_agents)
    memory_matrix = np.zeros((num_agents, num_agents))
    
    # Snapshots
    snapshot_before = None
    snapshot_after = None
    
    for frame in range(PARAMS['steps']):
        # Oscillateurs
        for i in range(num_agents):
            phases[i] = (np.sin(frame * PARAMS['agents'][i]['freq']) + 1) / 2
        
        # Trauma Event
        stress_wave = 0.0
        if frame == trauma_frame:
            stress_wave = trauma_intensity
            snapshot_before = {
                'positions': positions.copy(),
                'memory': memory_matrix.copy(),
                'states': states.copy()
            }
        
        # Dynamique interne
        new_states = []
        for i in range(num_agents):
            incoming = 0
            for j in range(num_agents):
                if i == j: continue
                dist = np.linalg.norm(positions[i] - positions[j])
                coupling = memory_matrix[j,i]
                if states[j] > 0.5:
                    incoming += states[j] * coupling * (1.0/dist)
            
            my_stress = (stress_wave if i == 3 else 0.0) + incoming * 0.1 + np.random.normal(0.01, 0.005)
            new_states.append(internal_dynamics(
                states[i], my_stress, 
                PARAMS['agents'][i]['Tc'], 
                PARAMS['agents'][i]['alpha'], 
                PARAMS['tau_decay'], 
                PARAMS['dt']
            ))
        states[:] = new_states
        
        # Géométrie (version simplifiée)
        forces = np.zeros_like(positions)
        for i in range(num_agents):
            for j in range(i+1, num_agents):
                diff = positions[j] - positions[i]
                dist = np.linalg.norm(diff)
                if dist < 0.01: continue
                dir_vec = diff / dist
                
                shared_mem = (memory_matrix[i,j] + memory_matrix[j,i]) / 2.0
                f_total = PARAMS['lambda_c'] * shared_mem
                
                forces[i] += dir_vec * f_total
                forces[j] -= dir_vec * f_total
        
        velocities = velocities * (1 - PARAMS['friction']) + forces * PARAMS['dt']
        positions += velocities * PARAMS['dt']
        
        # Mémoire (simplifié)
        for i in range(num_agents):
            for j in range(num_agents):
                if i == j: continue
                dist = np.linalg.norm(positions[i] - positions[j])
                growth = PARAMS['eta'] * states[j] * (1.0 / (dist**2 + 0.5))
                decay = memory_matrix[i,j] / 500.0
                memory_matrix[i,j] += (growth - decay) * PARAMS['dt']
                memory_matrix[i,j] = max(0, memory_matrix[i,j])
        
        # Snapshot après trauma
        if frame == trauma_frame + 50:
            snapshot_after = {
                'positions': positions.copy(),
                'memory': memory_matrix.copy(),
                'states': states.copy()
            }
    
    return snapshot_before, snapshot_after, memory_matrix

# === UI STREAMLIT ===
st.title("🧠 ANAMNESIS - NPC Trauma Memory Engine")
st.markdown("*Topological scars that NPCs never forget*")

st.sidebar.header("⚙️ Simulation Parameters")

trauma_type = st.sidebar.selectbox(
    "Trauma Event",
    ["Player Betrayal", "Ally Death", "Territory Lost", "Trust Broken"]
)

trauma_intensity = st.sidebar.slider("Trauma Intensity", 1.0, 10.0, 5.0)
trauma_timing = st.sidebar.slider("Trauma Frame", 50, 200, 100)

if st.sidebar.button("🔥 RUN SIMULATION", type="primary"):
    with st.spinner("Simulating psychological damage..."):
        before, after, final_memory = run_simulation(trauma_timing, trauma_intensity)
    
    st.success(f"✅ Simulated: **{trauma_type}** (Intensity: {trauma_intensity})")
    
    # === VISUALIZATIONS ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Before Trauma")
        if before:
            fig = go.Figure()
            pos = before['positions']
            for i in range(num_agents):
                fig.add_trace(go.Scatter3d(
                    x=[pos[i,0]], y=[pos[i,1]], z=[pos[i,2]],
                    mode='markers+text',
                    marker=dict(size=15, color=PARAMS['agents'][i]['color']),
                    text=PARAMS['agents'][i]['name'],
                    name=PARAMS['agents'][i]['name']
                ))
            
            fig.update_layout(
                scene=dict(
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    zaxis=dict(visible=False),
                    bgcolor='black'
                ),
                paper_bgcolor='black',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("After Trauma")
        if after:
            fig = go.Figure()
            pos = after['positions']
            mem = after['memory']
            
            # Links
            for i in range(num_agents):
                for j in range(i+1, num_agents):
                    if mem[i,j] + mem[j,i] > 0.5:
                        fig.add_trace(go.Scatter3d(
                            x=[pos[i,0], pos[j,0]],
                            y=[pos[i,1], pos[j,1]],
                            z=[pos[i,2], pos[j,2]],
                            mode='lines',
                            line=dict(color='red', width=3),
                            showlegend=False
                        ))
            
            # Agents
            for i in range(num_agents):
                fig.add_trace(go.Scatter3d(
                    x=[pos[i,0]], y=[pos[i,1]], z=[pos[i,2]],
                    mode='markers+text',
                    marker=dict(size=15, color=PARAMS['agents'][i]['color']),
                    text=PARAMS['agents'][i]['name'],
                    name=PARAMS['agents'][i]['name']
                ))
            
            fig.update_layout(
                scene=dict(
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    zaxis=dict(visible=False),
                    bgcolor='black'
                ),
                paper_bgcolor='black',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # === METRICS ===
    st.subheader("📊 Trauma Impact")
    m1, m2, m3 = st.columns(3)
    
    scar_strength = np.max(final_memory)
    
    with m1:
        st.metric("Topological Scar", f"{scar_strength:.2f}", f"+{scar_strength*0.8:.2f}")
    
    with m2:
        recovery_time = "∞ (Irreversible)" if scar_strength > 2.0 else f"{int(scar_strength*100)} turns"
        st.metric("Recovery Time", recovery_time)
    
    with m3:
        resilience = max(0, 100 - scar_strength*20)
        st.metric("System Resilience", f"{resilience:.0f}%", f"-{100-resilience:.0f}%")
    
    # === EXPORT ===
    export_data = {
        "trauma_type": trauma_type,
        "intensity": trauma_intensity,
        "scar_strength": float(scar_strength),
        "memory_matrix": final_memory.tolist()
    }
    
    st.download_button(
        "📥 Download Results (JSON)",
        data=json.dumps(export_data, indent=2),
        file_name=f"anamnesis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

# === FOOTER ===
st.markdown("---")
st.markdown("""
### 🎮 Use Cases
- **RPGs**: NPCs who permanently remember player betrayals
- **Strategy Games**: AI allies who form irreversible grudges  
- **Social Sims**: Characters with realistic PTSD responses

### 📚 Cite This Work
