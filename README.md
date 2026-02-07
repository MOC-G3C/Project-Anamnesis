# 🧠 ANAMNESIS - Topological Memory Engine for NPCs

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Status](https://img.shields.io/badge/status-alpha-orange)

**Give your NPCs psychological scars that never heal.**

---

## What is ANAMNESIS?

ANAMNESIS is a physics-based memory system for game NPCs. Unlike traditional reputation systems (simple numbers going up and down), ANAMNESIS models relationships as **topological structures** that can form **permanent scars**.

### Key Concept: Topological Scars

When a traumatic event occurs (betrayal, violence, loss), the system doesn't just decrease a number - it creates a **permanent structural change** in the relationship network.

**Example:**
- Player kills an NPC's friend
- Traditional system: Reputation -50 (can be recovered with gifts)
- ANAMNESIS: **Irreversible scar** forms (relationship never fully recovers)

---

## Features

- ✅ **Trauma-Based Memory**: Events leave permanent marks
- ✅ **Asymmetric Relationships**: NPCs remember differently
- ✅ **Physics-Grounded**: Based on Landau phase transitions
- ✅ **Emergent Psychology**: Complex behaviors from simple rules
- ✅ **Game-Ready**: Designed for RPGs, strategy games, social sims

---

## Quick Start

### Installation
```bash
git clone https://github.com/MOC-G3C/Project-Anamnesis
cd Project-Anamnesis
pip install -r requirements.txt
```

### Run Interactive Demo
```bash
streamlit run src/anamnesis_streamlit_simple.py
```

### Run Core Simulation
```bash
python src/anamnesis_core.py
```

---

## How It Works

ANAMNESIS models 4 agents in a 3D elastic space:

1. **Memory as Gravity**: Shared experiences pull agents together
2. **Trauma as Deformation**: Extreme stress permanently warps the space
3. **Entropy as Therapy**: Diverse connections prevent obsessive patterns

**Mathematical Foundation:**
- Landau phase transitions (critical stress thresholds)
- Topological memory (hysteresis loops)
- Kuramoto oscillators (synchronization dynamics)

---

## Use Cases

### 🎮 **RPG Games**
Create NPCs who remember betrayals permanently. A king whose advisor you once exposed will **never** trust you with state secrets, even if you save his life later.

### ⚔️ **Strategy Games**
Allied AI that forms grudges. Betray an ally in turn 50? They'll remember and refuse critical trades in turn 500.

### 🏘️ **Social Simulations**
Characters with realistic trauma responses. An NPC who witnessed violence develops lasting anxiety around the player.

---

## Documentation

- **[Whitepaper](docs/WHITEPAPER.md)** - Theory & methodology
- **[API Reference](docs/API.md)** - Integration guide (coming soon)
- **[Examples](examples/)** - Sample implementations

---

## Roadmap

- [x] Core physics simulation
- [x] Interactive web demo
- [ ] Unity plugin (Q2 2026)
- [ ] Unreal Engine integration (Q3 2026)
- [ ] Commercial licensing (Q4 2026)

---

## Citation

If you use ANAMNESIS in research or production:
```bibtex
@software{corbin2026anamnesis,
  author = {Corbin, Marc-Olivier},
  title = {ANAMNESIS: Topological Memory Engine for NPCs},
  year = {2026},
  url = {https://github.com/MOC-G3C/Project-Anamnesis}
}
```

---

## License

MIT License - see [LICENSE](LICENSE) for details

**TL;DR:** Free for any use (including commercial), just credit the source.

---

## Author

**Marc-Olivier Corbin (MOC-G3C)**  
Independent AI researcher | Montréal, Quebec  

**Contact:** [Your email or Twitter]

---

## Acknowledgments

Built on principles from:
- Lev Landau (phase transition theory)
- Yoshiki Kuramoto (synchronization)
- Modern neuroscience (memory consolidation)

---

*"The scar is not a bug - it's the feature."*
## 🚀 Try It Online

**[Live Demo →](https://anamnesisappsimplepy-p2enl7ufhacnncopz8xpxm.streamlit.app/)**

No installation needed - simulate trauma events in your browser.

---
```

---

### **4. Créer un Fichier `LICENSE`**

GitHub détecte automatiquement les licences et affiche un badge.

**Action :**
1. Va sur ton repo GitHub
2. Clique "Add file" → "Create new file"
3. Nomme-le `LICENSE`
4. Choisis "MIT License" dans le dropdown
5. Remplace `[year]` par `2026` et `[fullname]` par `Marc-Olivier Corbin`
6. Commit

**Résultat :** Badge "License: MIT" apparaît automatiquement.

---

## 📅 PLAN POUR LES 2 PROCHAINES SEMAINES

### **Semaine 2 (17-23 Février) : Feedback Privé**

**Objectif :** Tester avec 5 personnes AVANT de poster sur Reddit

**Qui contacter :**
1. **Discord "Game Dev League"** - Partage en DM à 2-3 membres actifs
2. **LinkedIn** - Si t'as des contacts en jeu vidéo
3. **Amis qui jouent aux RPGs** - Montre-leur la démo, demande "est-ce que ça te parlerait dans un jeu ?"

**Template de message :**
```
Hey [nom],

Je bosse sur un système de mémoire pour NPCs de jeux vidéo.
L'idée : les personnages se souviennent des traumas de façon permanente 
(pas juste un score de réputation qui monte/descend).

J'ai une démo interactive de 2 minutes :
https://anamnesisappsimplepy-p2enl7ufhacnncopz8xpxm.streamlit.app/

Ça te prendrait 5 min de tester et me dire :
1. Est-ce que le concept est clair ?
2. Est-ce que tu verrais ça dans un jeu ?
3. Qu'est-ce qui est confus ?

Merci ! 🙏
```

**Collecte le feedback dans un Google Doc.**

---

### **Semaine 3 (24 Février - 2 Mars) : Première Publication Reddit**

**Subreddit cible :** **r/proceduralgeneration** (100k membres, moins intimidant que r/gamedev)

**Pourquoi ce sub ?**
- Communauté technique mais accessible
- Apprécient les approches basées sur la physique
- Moins de noise que r/gamedev
- Historique de posts similaires qui ont bien marché

**Template de post Reddit** (je te le donne quand tu seras prêt) :
```
Title: I built a trauma memory system for NPCs using phase transition physics [Open Source]

Body:
Hey r/proceduralgeneration,

I've been working on ANAMNESIS, a system that gives NPCs "topological scars" 
- permanent memories that can't be fully healed.

Unlike reputation systems (numbers that go up/down), this uses physics-based 
memory formation. When a traumatic event occurs, it creates an irreversible 
structural change in the relationship network.

**Live demo:** [ton-lien-streamlit]
**Code:** https://github.com/MOC-G3C/Project-Anamnesis

Built with Python/NumPy, based on Landau phase transition theory.

[Screenshot de la heatmap]

Feedback welcome!
