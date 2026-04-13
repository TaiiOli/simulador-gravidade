import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# --- MOTOR DE FÍSICA ---
class GravitySim:
    def __init__(self, G=1.0, dt=0.05):
        self.G = G
        self.dt = dt

    def compute_acceleration(self, pos, masses, softening):
        n = len(masses)
        acc = np.zeros_like(pos)
        for i in range(n):
            for j in range(n):
                if i != j:
                    diff = pos[j] - pos[i]
                    # O softening varia conforme o cenário para permitir "funis" mais íngremes
                    dist = np.linalg.norm(diff) + softening 
                    acc[i] += self.G * masses[j] * diff / dist**3
        return acc

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="Gravidade 2.0: Do Planeta ao Buraco Negro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    stMarkdown { color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌌 Lab Virtual: Curvatura do Espaço-Tempo")
st.sidebar.header("Galeria de Gravidade")

# --- SELEÇÃO DE CENÁRIOS ---
cenario = st.sidebar.selectbox(
    "Escolha uma Massa Central",
    ["A Terra", "O Sol", "Estrela de Nêutrons", "Buraco Negro Estelar", "Sistema Binário"]
)

# Configurações de Física e Estética por Cenário
if cenario == "A Terra":
    m_central, c_central, softening, z_limit = 10.0, '#1E90FF', 1.0, -5
    pos_init = np.array([[0,0], [6,0]], dtype=float)
    vel_init = np.array([[0,0], [0,1.2]], dtype=float)
    masses = np.array([m_central, 0.1])
    desc = "A Terra cria uma curvatura suave, mantendo satélites em órbita sem distorcer drasticamente a luz."
elif cenario == "O Sol":
    m_central, c_central, softening, z_limit = 100.0, '#FFD700', 0.8, -20
    pos_init = np.array([[0,0], [5,0]], dtype=float)
    vel_init = np.array([[0,0], [0,4.5]], dtype=float)
    masses = np.array([m_central, 1.0])
    desc = "O Sol deforma o tecido significativamente. Note como a malha é mais profunda e as velocidades orbitais são maiores."
elif cenario == "Estrela de Nêutrons":
    m_central, c_central, softening, z_limit = 300.0, '#ADFF2F', 0.4, -60
    pos_init = np.array([[0,0], [4,0]], dtype=float)
    vel_init = np.array([[0,0], [0,8.0]], dtype=float)
    masses = np.array([m_central, 1.0])
    desc = "Massa solar comprimida em km. A curvatura é um funil estreito e extremamente íngreme."
elif cenario == "Buraco Negro Estelar":
    m_central, c_central, softening, z_limit = 600.0, '#000000', 0.1, -120
    pos_init = np.array([[0,0], [4,0]], dtype=float)
    vel_init = np.array([[0,0], [0,12.0]], dtype=float)
    masses = np.array([m_central, 1.0])
    desc = "Ruptura no espaço-tempo. O poço é tão profundo que nada escapa. Representado aqui com fundo infinito."
else: # Estrela Binária
    m_central, c_central, softening, z_limit = 50.0, '#FF4500', 0.6, -30
    pos_init = np.array([[-3,0], [3,0]], dtype=float)
    vel_init = np.array([[0,-2.5], [0,2.5]], dtype=float)
    masses = np.array([50.0, 50.0])
    desc = "Duas massas iguais orbitando um centro comum. A malha 'dança' conforme elas giram."

st.sidebar.info(desc)
num_steps = st.sidebar.slider("Duração da Animação", 100, 1000, 400)

# --- EXECUÇÃO DA SIMULAÇÃO ---
if st.button("🚀 Iniciar Simulação"):
    sim = GravitySim(G=1.0, dt=0.03)
    history = []
    
    curr_pos = pos_init.copy()
    curr_vel = vel_init.copy()
    
    # 1. Loop de Física
    for _ in range(num_steps):
        acc = sim.compute_acceleration(curr_pos, masses, softening)
        curr_vel += acc * sim.dt
        curr_pos += curr_vel * sim.dt
        history.append(curr_pos.copy())
    
    history = np.array(history)

    # 2. Malha de Espaço-Tempo (Geometria)
    grid_res = 30
    x_range = np.linspace(-12, 12, grid_res)
    y_range = np.linspace(-12, 12, grid_res)
    X, Y = np.meshgrid(x_range, y_range)

    def calcular_malha(p):
        z = np.zeros_like(X)
        for i in range(len(masses)):
            dist = np.sqrt((X - p[i,0])**2 + (Y - p[i,1])**2) + softening
            z -= masses[i] / dist
        return np.clip(z, z_limit, 2)

    # 3. Construção dos Frames
    frames = []
    for k in range(0, len(history), 6):
        z_frame = calcular_malha(history[k])
        frames.append(go.Frame(
            data=[
                go.Surface(z=z_frame, x=X, y=Y),
                go.Scatter3d(x=history[k,:,0], y=history[k,:,1], z=np.zeros(len(masses)), 
                             mode='markers', marker=dict(size=10, color=['white' if c == 'black' else c for c in [c_central, 'red']]))
            ],
            name=str(k)
        ))

    # 4. Figura Final e Layout Estético
    fig = go.Figure(
        data=[
            go.Surface(z=calcular_malha(history[0]), x=X, y=Y, colorscale='Viridis', showscale=False, opacity=0.8),
            go.Scatter3d(x=history[0,:,0], y=history[0,:,1], z=np.zeros(len(masses)), mode='markers')
        ],
        layout=go.Layout(
            title=dict(text=f"Simulando: {cenario}", font=dict(size=24, color='white')),
            template="plotly_dark",
            updatemenus=[{
                "type": "buttons",
                "buttons": [{"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 30, "redraw": True}}]}]
            }],
            scene=dict(
                xaxis=dict(visible=False), yaxis=dict(visible=False),
                zaxis=dict(range=[z_limit, 5], title="Deformação"),
                aspectmode='manual', aspectratio=dict(x=1, y=1, z=0.5),
                camera=dict(eye=dict(x=1.3, y=1.3, z=0.8))
            ),
            margin=dict(l=0, r=0, b=0, t=60)
        ),
        frames=frames
    )

    st.plotly_chart(fig, use_container_width=True)

    # Exportação de Dados para o Relatório (MLOps/CC)
    st.subheader("📊 Métricas da Simulação")
    col1, col2 = st.columns(2)
    col1.metric("Massa Total", f"{np.sum(masses)} u.m.")
    col2.metric("Passos Computados", f"{num_steps}")
    
    st.write("Dados Finais das Posições:")
    st.dataframe(pd.DataFrame(history[-1], columns=['X', 'Y']))