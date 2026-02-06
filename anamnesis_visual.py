import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

# [Gardez votre code existant jusqu'à la section GRAPHIQUE]

# --- GRAPHIQUE AMÉLIORÉ ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(20, 12))
gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

# Visualisation 3D principale (grande)
ax_3d = fig.add_subplot(gs[:, 0:2], projection='3d')

# Métriques
ax_states = fig.add_subplot(gs[0, 2])
ax_div = fig.add_subplot(gs[1, 2])
ax_memory = fig.add_subplot(gs[2, 2])

# Configuration
fig.patch.set_facecolor('#0a0a0a')
ax_3d.set_facecolor('#000000')

# Titres
ax_states.set_title("ACTIVATION NEURONALE", fontsize=10, color='cyan')
ax_div.set_title("DIVERSITÉ (Santé)", fontsize=10, color='lime')
ax_memory.set_title("MÉMOIRE TOTALE", fontsize=10, color='magenta')

# Styles
for ax in [ax_states, ax_div, ax_memory]:
    ax.set_facecolor('#0a0a0a')
    ax.grid(alpha=0.2)

# Historiques étendus
state_history = [np.zeros(num_agents)]
memory_total_history = [0]

def update(f):
    global positions, velocities, states, memory_matrix
    
    # [Votre logique existante...]
    
    # Métriques supplémentaires
    state_history.append(states.copy())
    memory_total_history.append(np.sum(memory_matrix))
    
    if len(state_history) > 300:
        state_history.pop(0)
        memory_total_history.pop(0)
    
    # === RENDU 3D AVANCÉ ===
    ax_3d.clear()
    ax_3d.set_facecolor('#000000')
    ax_3d.grid(False)
    ax_3d.set_axis_off()
    
    # Caméra dynamique
    ax_3d.view_init(elev=15 + 10*np.sin(f*0.01), azim=f*0.2)
    
    # Liens mémoriels avec gradient
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            mem = (memory_matrix[i,j] + memory_matrix[j,i]) / 2.0
            if mem > 0.3:
                color = plt.cm.plasma(min(mem/3.0, 1.0))
                ax_3d.plot([positions[i,0], positions[j,0]],
                          [positions[i,1], positions[j,1]],
                          [positions[i,2], positions[j,2]],
                          c=color, alpha=0.7, lw=1+mem*2)
    
    # Agents avec effets
    for i in range(num_agents):
        # Halo si activé
        if states[i] > 1.0:
            ax_3d.scatter(*positions[i], s=800, c=colors[i], 
                         alpha=0.1, edgecolors='none')
        
        # Corps
        ax_3d.scatter(*positions[i], s=200+states[i]*150, 
                     c=colors[i], alpha=0.9, 
                     edgecolors='white', linewidths=2)
        
        # Label
        ax_3d.text(*positions[i], PARAMS['agents'][i]['name'],
                  fontsize=8, color='white', ha='center')
    
    # === GRAPHIQUES TEMPORELS ===
    x = np.arange(len(state_history))
    
    # États
    ax_states.clear()
    ax_states.set_title("ACTIVATION NEURONALE", fontsize=10, color='cyan')
    for i in range(num_agents):
        data = np.array(state_history)[:,i]
        ax_states.plot(x, data, c=colors[i], lw=2, label=PARAMS['agents'][i]['name'])
    ax_states.axhline(1.0, color='red', linestyle=':', alpha=0.5)
    ax_states.set_ylim(-0.5, 4)
    ax_states.legend(loc='upper right', fontsize=6)
    
    # Diversité
    ax_div.clear()
    ax_div.set_title("DIVERSITÉ (Santé)", fontsize=10, color='lime')
    for i in range(num_agents):
        data = np.array(diversity_history)[:,i]
        ax_div.plot(np.arange(len(diversity_history)), data, c=colors[i], lw=2)
    ax_div.set_ylim(0, 1.1)
    
    # Mémoire globale
    ax_memory.clear()
    ax_memory.set_title("MÉMOIRE TOTALE", fontsize=10, color='magenta')
    ax_memory.plot(memory_total_history, c='magenta', lw=3)
    ax_memory.fill_between(range(len(memory_total_history)), 
                           memory_total_history, alpha=0.3, color='magenta')
    
    # HUD principal
    crisis = "🔴 CRISE" if np.any(states > 2.5) else "🟢 STABLE"
    ax_3d.text2D(0.5, 0.98, f"ANAMNESIS | Frame {f} | {crisis}",
                transform=ax_3d.transAxes, ha='center', 
                fontsize=14, color='white', weight='bold')

ani = FuncAnimation(fig, update, frames=PARAMS['steps'], 
                   interval=20, blit=False)
plt.show()
