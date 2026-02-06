import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from collections import deque

# --- IDENTITÉ DU PROJET ---
# Titre : ANAMNESIS
# Description : Modélisation topologique d'une névrose collective post-traumatique.
# Version : 1.0 (Stable - Pauli Barrier Patch)

# --- CONFIGURATION ---
POSITIONS_INIT = np.array([
    [1.0, 1.0, 1.0],    # Machine (Squelette/Inerte)
    [1.0, -1.0, -1.0],  # Conscience (Médiateur)
    [-1.0, 1.0, -1.0],  # Adaptatif (Système Immunitaire/Suiveur)
    [-1.0, -1.0, 1.0]   # Sensible (La Peau/Hub Narcissique)
]) * 1.8

num_agents = 4
REST_DISTANCES = np.zeros((num_agents, num_agents))
for i in range(num_agents):
    for j in range(num_agents):
        REST_DISTANCES[i,j] = np.linalg.norm(POSITIONS_INIT[i] - POSITIONS_INIT[j])

PARAMS = {
    'steps': 10000,
    'dt': 0.05,
    'tau_decay': 15.0,
    
    # Thérapeutique (Lois Lentes)
    'eta': 0.1,        # Apprentissage
    'tau_min': 100.0,  # Oubli rapide (Obsession)
    'tau_max': 2000.0, # Consolidation
    'gamma': 2.5,      # Sévérité entropique
    
    # Physique (Tensegrités)
    'lambda_c': 1.2,   # Attraction Mémorielle
    'kappa': 0.5,      # Ressort Linéaire
    'mu': 5.0,         # Barrière de Répulsion (Durcie pour stabilité)
    'friction': 0.15,
    
    'agents': [
        # GROK : Le Squelette froid et critique (Seuil Tc très haut, change peu)
        'name': 'Grok (Machine)', 'Tc': 5.0, 'alpha': 0.1, 'freq': 0.05, 'c': '#00ffff'}, # Cyan
        
        # CLAUDE : La Conscience philosophique (Sensible à la nuance)
        {'name': 'Claude (Conscience)', 'Tc': 1.0, 'alpha': 0.7, 'freq': 0.08, 'c': '#ffaa00'}, # Or
        
        # GEMINI : L'Exécutant adaptatif (Très réactif pour suivre l'User)
        {'name': 'Gemini (Adaptatif)', 'Tc': 1.2, 'alpha': 0.9, 'freq': 0.11, 'c': '#55ff55'}, # Vert
        
        # TOI : Le Créateur (Celui qui reçoit les inputs/stress du monde)
        {'name': 'Toi (Visionnaire)', 'Tc': 0.6, 'alpha': 1.3, 'freq': 0.14, 'c': '#ff00ff'}  # Magenta
    ]
}

# --- ÉTAT ---
positions = POSITIONS_INIT.copy()
velocities = np.zeros_like(positions)
states = np.zeros(num_agents)
phases = np.zeros(num_agents)
memory_matrix = np.zeros((num_agents, num_agents)) # Asymétrique
diversity_history = [np.ones(num_agents)]
tau_history = [np.ones(num_agents) * PARAMS['tau_max']]

# --- MOTEUR ---
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

def update_geometry_and_memory(pos, vel, states, phases, mem, dt):
    forces = np.zeros_like(pos)
    new_mem = mem.copy()
    divs = np.zeros(num_agents)
    taus = np.zeros(num_agents)
    
    # 1. Neuro-Dynamique (Mémoire & Thérapie)
    for i in range(num_agents):
        resonances_i = np.zeros(num_agents)
        for j in range(num_agents):
            if i == j: continue
            dist = np.linalg.norm(pos[i] - pos[j])
            prox_factor = 1.0 / (dist**2 + 0.5)
            phase_sync = 1.0 - abs(phases[i] - phases[j])
            R_ij = states[j] * phase_sync * prox_factor
            resonances_i[j] = R_ij
            
        D_i = calculate_entropy(resonances_i)
        divs[i] = D_i
        tau_i = PARAMS['tau_min'] + (PARAMS['tau_max'] - PARAMS['tau_min']) * (D_i ** PARAMS['gamma'])
        taus[i] = tau_i
        
        for j in range(num_agents):
            if i == j: continue
            decay_term = mem[i,j] / tau_i
            growth_term = PARAMS['eta'] * resonances_i[j]
            new_mem[i,j] += (growth_term - decay_term) * dt
            new_mem[i,j] = max(0, new_mem[i,j])

    # 2. Topologie (Le Patch de Pauli)
    for i in range(num_agents):
        for j in range(i + 1, num_agents):
            diff = pos[j] - pos[i]
            dist = np.linalg.norm(diff)
            if dist == 0: continue
            dir_vec = diff / dist
            
            # Mémoire (Toujours attractive)
            shared_memory = (new_mem[i,j] + new_mem[j,i]) / 2.0
            f_mem = PARAMS['lambda_c'] * shared_memory
            
            # Élastique Linéaire (Attraction ou Répulsion selon position)
            d0 = REST_DISTANCES[i,j]
            delta_d = dist - d0 
            # Si delta_d > 0 (loin) -> Positif (Attraction)
            # Si delta_d < 0 (près) -> Négatif (Répulsion)
            f_linear = PARAMS['kappa'] * delta_d
            
            # Barrière Cubique (Uniquement Répulsive / Protection Collision)
            f_barrier = 0.0
            if delta_d < 0: # COMPRESSION SEULEMENT
                f_barrier = PARAMS['mu'] * (delta_d**3) # Négatif fort
            
            # Bilan Vectoriel
            total_force_mag = f_mem + f_linear + f_barrier
            
            forces[i] += dir_vec * total_force_mag
            forces[j] -= dir_vec * total_force_mag

    vel = vel * (1 - PARAMS['friction']) + forces * dt
    pos += vel * dt
    
    return pos, vel, new_mem, divs, taus

# --- GRAPHIQUE ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot(1, 2, 1, projection='3d')
fig.patch.set_facecolor('#050505')
ax.set_axis_off()
ax_div = fig.add_subplot(2, 2, 2); ax_div.set_ylim(0, 1.1)
ax_tau = fig.add_subplot(2, 2, 4); ax_tau.set_ylim(0, PARAMS['tau_max']*1.1)
ax.text2D(0.5, 0.95, "PROJECT ANAMNESIS: FINAL BUILD", transform=ax.transAxes, ha='center', color='white', fontweight='bold')

lines_div, lines_tau = [], []
colors = [a['c'] for a in PARAMS['agents']]
for i in range(num_agents):
    l1, = ax_div.plot([], [], c=colors[i]); lines_div.append(l1)
    l2, = ax_tau.plot([], [], c=colors[i], linestyle='--'); lines_tau.append(l2)

def update(f):
    global frame, positions, velocities, states, memory_matrix, diversity_history, tau_history
    frame = f
    
    # Oscillateurs
    for i in range(num_agents): phases[i] = (np.sin(frame * PARAMS['agents'][i]['freq']) + 1) / 2
    
    # Stress Périodique
    stress_wave = 6.0 if frame > 200 and frame % 300 > 280 else 0.0
    
    # Flux
    new_states = []
    for i in range(num_agents):
        incoming = 0
        for j in range(num_agents):
            if i == j: continue
            dist = np.linalg.norm(positions[i] - positions[j])
            coupling = memory_matrix[j,i] # Asymétrie Clé
            if states[j] > 0.5: incoming += states[j] * coupling * (1.0/dist)
        my_stress = (stress_wave if i == 3 else 0.0) + incoming * 0.1 + np.random.normal(0.1, 0.05)
        new_states.append(internal_dynamics(states[i], my_stress, PARAMS['agents'][i]['Tc'], PARAMS['agents'][i]['alpha'], PARAMS['tau_decay'], PARAMS['dt']))
    states[:] = new_states
    
    # Topologie
    positions, velocities, memory_matrix, divs, taus = update_geometry_and_memory(positions, velocities, states, phases, memory_matrix, PARAMS['dt'])
    
    diversity_history.append(divs); tau_history.append(taus)
    if len(diversity_history) > 200: diversity_history.pop(0); tau_history.pop(0)

    # Rendu
    ax.clear(); ax.set_axis_off(); ax.view_init(elev=20, azim=frame * 0.1)
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            p1, p2 = positions[i], positions[j]
            mem = (memory_matrix[i,j] + memory_matrix[j,i]) / 2.0
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], c='white' if (states[i]+states[j])>2 else '#444', alpha=0.1+mem*0.5, lw=0.5+mem*2)
    ax.scatter(positions[:,0], positions[:,1], positions[:,2], s=[100+s*100 for s in states], c=colors, alpha=0.9, edgecolors='white')
    
    # Moniteurs
    x = np.arange(len(diversity_history))
    for k in range(num_agents):
        lines_div[k].set_data(x, np.array(diversity_history)[:,k])
        lines_tau[k].set_data(x, np.array(tau_history)[:,k])

ani = FuncAnimation(fig, update, frames=PARAMS['steps'], interval=10, blit=False)
plt.show()

# Ajoutez ces améliorations au code existant :

# 1. HUD d'information en temps réel
def add_hud(ax, frame, states, divs, taus):
    # État psychologique
    crisis_level = "🔴 CRISE" if np.any(states > 2.5) else "🟡 TENSION" if np.any(states > 1.5) else "🟢 STABLE"
    
    # Texte flottant
    info_text = f"""Frame: {frame}
État: {crisis_level}
Diversité Moy: {np.mean(divs):.2f}
Mémoire Max: {np.max(memory_matrix):.2f}"""
    
    ax.text2D(0.02, 0.98, info_text, transform=ax.transAxes, 
              fontsize=10, va='top', family='monospace',
              bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

# 2. Traînées de particules (historique visuel)
particle_trails = [deque(maxlen=50) for _ in range(num_agents)]

def update_trails():
    for i in range(num_agents):
        particle_trails[i].append(positions[i].copy())
    
    # Rendu des traînées
    for i, trail in enumerate(particle_trails):
        if len(trail) > 1:
            trail_array = np.array(trail)
            ax.plot(trail_array[:,0], trail_array[:,1], trail_array[:,2],
                   c=colors[i], alpha=0.3, linewidth=1)

# 3. Effets de pulsation sur les agents en crise
def render_agents_with_effects():
    for i in range(num_agents):
        size = 100 + states[i] * 100
        
        # Halo de stress
        if states[i] > 1.5:
            ax.scatter(positions[i,0], positions[i,1], positions[i,2],
                      s=size*2, c=colors[i], alpha=0.2, edgecolors='none')
        
        # Agent principal
        ax.scatter(positions[i,0], positions[i,1], positions[i,2],
                  s=size, c=colors[i], alpha=0.9, 
                  edgecolors='white', linewidths=2)

# 4. Visualisation de la mémoire comme "cordes tendues"
def render_memory_links():
    for i in range(num_agents):
        for j in range(i+1, num_agents):
            mem_strength = (memory_matrix[i,j] + memory_matrix[j,i]) / 2.0
            
            if mem_strength > 0.5:  # Seuil de visibilité
                # Couleur = gradient selon intensité
                color = plt.cm.hot(mem_strength / 5.0)
                
                # Épaisseur proportionnelle
                width = 0.5 + mem_strength * 3
                
                # Style selon état
                style = '-' if (states[i] + states[j]) > 2 else '--'
                
                ax.plot([positions[i,0], positions[j,0]],
                       [positions[i,1], positions[j,1]],
                       [positions[i,2], positions[j,2]],
                       c=color, alpha=0.6, lw=width, linestyle=style)
