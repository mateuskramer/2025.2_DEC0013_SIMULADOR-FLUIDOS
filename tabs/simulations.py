import streamlit as st
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fluids import friction_factor, Reynolds
from config.settings import GRAVITY, TUBE_MATERIALS

def render_simulations_tab(sidebar_data):
    """Renderiza a aba de Simulações"""
    st.header("Simulações e Comparações")
    
    # Extrair dados da sidebar
    rho = sidebar_data['rho']
    mu = sidebar_data['mu']
    pressure_inlet = sidebar_data['pressure_inlet']
    input_type = sidebar_data['input_type']
    flow_rate = sidebar_data['flow_rate']
    velocity = sidebar_data['velocity']
    
    # Calcular flow_rate se necessário
    if input_type == "Velocidade (V)":
        first_pipe = st.session_state.pipes[0]
        A_first = math.pi * (first_pipe['diameter']/2)**2
        flow_rate = velocity * A_first
    
    # Simulação de variação de vazão
    _render_flow_rate_simulation(rho, mu)
    
    # Simulação de variação de pressão
    _render_pressure_simulation(rho, mu, flow_rate)
    
    # Comparação de materiais
    _render_material_comparison(rho, mu, flow_rate)


def _render_flow_rate_simulation(rho, mu):
    """Renderiza simulação de variação de vazão"""
    st.subheader("Variação de Vazão no Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        Q_min = st.number_input("Vazão mínima (m³/s)", value=0.001, step=0.001, format="%.4f")
        Q_max = st.number_input("Vazão máxima (m³/s)", value=0.05, step=0.005, format="%.4f")
        n_points = st.slider("Número de pontos", 10, 100, 50)
    
    flow_rates_sim = np.linspace(Q_min, Q_max, n_points)
    head_losses_sim = []
    pressure_drops_sim = []
    velocities_sim = []
    
    for Q_sim in flow_rates_sim:
        total_h = 0
        first_pipe = st.session_state.pipes[0]
        A = math.pi * (first_pipe['diameter']/2)**2
        V_sim = Q_sim / A
        velocities_sim.append(V_sim)
        
        for pipe in st.session_state.pipes:
            A = math.pi * (pipe['diameter']/2)**2
            V = Q_sim / A
            
            Re_sim = Reynolds(V=V, D=pipe['diameter'], rho=rho, mu=mu)
            try:
                f_sim = friction_factor(Re=Re_sim, eD=pipe['roughness']/pipe['diameter'])
            except:
                f_sim = 0.02
            
            h_dist = f_sim * (pipe['length'] / pipe['diameter']) * (V**2 / (2 * GRAVITY))
            total_h += h_dist + pipe.get('elevation_change', 0)
        
        head_losses_sim.append(total_h)
        pressure_drops_sim.append(total_h * rho * GRAVITY / 1000)
    
    fig_sim1 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_sim1.add_trace(
        go.Scatter(x=flow_rates_sim*3600, y=head_losses_sim, name="Perda de Carga (m)", 
                  line=dict(color='#00d4ff', width=3)),
        secondary_y=False,
    )
    
    fig_sim1.add_trace(
        go.Scatter(x=flow_rates_sim*3600, y=velocities_sim, name="Velocidade (m/s)", 
                  line=dict(color='#ff6b6b', width=3)),
        secondary_y=True,
    )
    
    fig_sim1.update_xaxes(title_text="Vazão (m³/h)", color='#e0fbfc')
    fig_sim1.update_yaxes(title_text="Perda de Carga (m)", secondary_y=False, color='#e0fbfc')
    fig_sim1.update_yaxes(title_text="Velocidade (m/s)", secondary_y=True, color='#e0fbfc')
    fig_sim1.update_layout(
        title="Perda de Carga e Velocidade vs Vazão",
        paper_bgcolor='#1f3044',
        plot_bgcolor='#2d4059',
        font=dict(color='#e0fbfc'),
        legend=dict(bgcolor='#2d4059', bordercolor='#3d5a73', borderwidth=1)
    )
    
    st.plotly_chart(fig_sim1, use_container_width=True)


def _render_pressure_simulation(rho, mu, flow_rate):
    """Renderiza simulação de variação de pressão de entrada"""
    st.subheader("Variação de Pressão de Entrada")
    
    col3, col4 = st.columns(2)
    
    with col3:
        P_min = st.number_input("Pressão mínima (kPa)", value=100.0, step=10.0)
        P_max = st.number_input("Pressão máxima (kPa)", value=500.0, step=10.0)
    
    n_points = 50
    pressures_inlet_sim = np.linspace(P_min*1000, P_max*1000, n_points)
    pressures_outlet_sim = []
    
    for P_in in pressures_inlet_sim:
        P_current = P_in
        for pipe in st.session_state.pipes:
            A = math.pi * (pipe['diameter']/2)**2
            V = flow_rate / A
            
            Re_sim = Reynolds(V=V, D=pipe['diameter'], rho=rho, mu=mu)
            try:
                f_sim = friction_factor(Re=Re_sim, eD=pipe['roughness']/pipe['diameter'])
            except:
                f_sim = 0.02
            
            h_dist = f_sim * (pipe['length'] / pipe['diameter']) * (V**2 / (2 * GRAVITY))
            h_total = h_dist + pipe.get('elevation_change', 0)
            
            P_loss = h_total * rho * GRAVITY
            P_current -= P_loss
        
        pressures_outlet_sim.append(P_current/1000)
    
    fig_sim2 = go.Figure()
    
    fig_sim2.add_trace(go.Scatter(
        x=pressures_inlet_sim/1000, 
        y=pressures_outlet_sim,
        mode='lines',
        name='Pressão de Saída',
        line=dict(color='#4ecdc4', width=3)
    ))
    
    fig_sim2.update_xaxes(title_text="Pressão de Entrada (kPa)", color='#e0fbfc')
    fig_sim2.update_yaxes(title_text="Pressão de Saída (kPa)", color='#e0fbfc')
    fig_sim2.update_layout(
        title="Pressão de Saída vs Pressão de Entrada",
        paper_bgcolor='#1f3044',
        plot_bgcolor='#2d4059',
        font=dict(color='#e0fbfc')
    )
    
    st.plotly_chart(fig_sim2, use_container_width=True)


def _render_material_comparison(rho, mu, flow_rate):
    """Renderiza comparação entre materiais"""
    st.subheader("Comparação de Materiais (Primeiro Trecho)")
    
    materials_comp = {
        "PVC": 0.0000015,
        "Cobre": 0.0000015,
        "Aço comercial": 0.000045,
        "Aço galvanizado": 0.00015,
        "Concreto": 0.0003,
        "Ferro fundido": 0.00026
    }
    
    material_head_loss = []
    material_names = list(materials_comp.keys())
    
    first_pipe = st.session_state.pipes[0]
    A = math.pi * (first_pipe['diameter']/2)**2
    V = flow_rate / A
    
    for material, rough in materials_comp.items():
        Re_temp = Reynolds(V=V, D=first_pipe['diameter'], rho=rho, mu=mu)
        try:
            f_temp = friction_factor(Re=Re_temp, eD=rough/first_pipe['diameter'])
        except:
            f_temp = 0.02
        
        hl_temp = f_temp * (first_pipe['length'] / first_pipe['diameter']) * (V**2 / (2 * GRAVITY))
        material_head_loss.append(hl_temp)
    
    fig_mat = go.Figure(data=[
        go.Bar(name='Perda de Carga', x=material_names, y=material_head_loss, marker_color='#00d4ff')
    ])
    fig_mat.update_layout(
        title="Comparação de Perda de Carga por Material",
        xaxis_title="Material",
        yaxis_title="Perda de Carga (m)",
        paper_bgcolor='#1f3044',
        plot_bgcolor='#2d4059',
        font=dict(color='#e0fbfc'),
        xaxis=dict(color='#e0fbfc'),
        yaxis=dict(color='#e0fbfc')
    )
    
    st.plotly_chart(fig_mat, use_container_width=True)