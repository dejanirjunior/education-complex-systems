# 🎓 Education Complex Systems Simulator
### Virtuous Triangle: Education, Technology, and Economy

This project implements a **complex systems simulation** to study the interaction between:

- Education systems  
- Technological capability  
- Economic productivity  

It is part of a **Master’s research project (PPGET / IFTM)** focused on evaluating the impact of **computing education** on national development.

---

## 🌐 Live Access (On-Demand)

The simulator is available online when the research environment is active.

👉 Access link is generated dynamically using a secure tunnel (ngrok).  
👉 Contact the author to obtain the current active link.

---

## 🧠 Conceptual Model

The simulation is based on the hypothesis of a **Virtuous Triangle**:

Education → Technology → Economy → (reinforces Education)


Key mechanisms:

- Skill formation (knowledge + computational thinking)
- Conversion into productivity and innovation
- Institutional modulation (efficiency, corruption, policy stability)
- Capital attraction and reinvestment

---

## 🔬 What the Simulator Provides

### Standard Analysis
- Predefined scenarios
- Comparative outputs

### Experimental Lab
- Full parameter control
- Scenario customization

### Outputs
- PISA-like educational indicator
- Computational thinking level
- Economic productivity
- Innovation capacity
- Capital attraction
- Inequality dynamics

---

## ⚙️ Running Locally (Development Mode)

### 1. Clone repository

```bash
git clone https://github.com/dejanirjunior/education-complex-systems.git
cd education-complex-systems

2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Run application
python app.py
5. Access locally
http://localhost:5000
🌍 Running as Public Server (Recommended)

This project is designed to be served from a local Linux machine using ngrok.

Start the simulator:
./start_simulator.sh
Get public link:
curl -s http://127.0.0.1:4040/api/tunnels | python3 -m json.tool

Look for:

"public_url": "https://xxxxx.ngrok-free.dev"
Stop the simulator:
./stop_simulator.sh
🔐 Access Control

The simulation interface requires a password:

simulador2026

This prevents uncontrolled usage in a public environment.

⚠️ Important Notes
The model is exploratory, not predictive
The “PISA-like” indicator is synthetic
Results should be interpreted comparatively
Performance depends on the host machine
🧩 System Characteristics
Agent-based simulation
Stochastic dynamics (seed-controlled)
Emergent macro indicators
Multi-variable institutional influence
🧪 Example Use Cases
Academic research
Policy scenario testing
Education system modeling
Complex systems teaching
🚀 Deployment Strategy

Current architecture:

Linux Host → Flask App → ngrok → Public URL

Advantages:

Full control over performance
No cloud cost
Real-time experimentation
🔮 Future Improvements
Persistent public endpoint
Cloud deployment (controlled)
Sensitivity analysis tools
Integration with real-world datasets
AI-assisted interpretation
👨‍🎓 Author

Dejanir de Almeida Junior
Master’s Research Project – PPGET / IFTM

📧 junekko@msn.com

📄 License

Academic and research use only.
Attribution required.


---

# 🚀 Próximo passo

Agora execute:

```bash
git add README.md
git commit -m "Add operational README"
git push


