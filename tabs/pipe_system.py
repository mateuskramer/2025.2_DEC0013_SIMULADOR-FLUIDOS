import streamlit as st
import pandas as pd
import math
import plotly.graph_objects as go
from config.settings import GRAVITY, WATER_VELOCITY_MIN, WATER_VELOCITY_MAX, AIR_VELOCITY_MAX
from components.pipe_config import render_pipe_configuration
from utils.calculations import calculate_pipe_losses

def render_pipe_system_tab(sidebar_data):
    """Renderiza a aba de Sistema de Tubulações"""
    st.header("Sistema de Tubulações em Série")
    
    # Botões para adicionar/remover tubos
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("➕ Adicionar Trecho", use_container_width=True):
            new_id = max([p['id'] for p in st.session_state.pipes]) + 1
            st.session_state.pipes.append({
                'id': new_id,
                'material': 'Aço comercial',
                'diameter': 0.1,
                'length': 100.0,
                'elevation_change': 0.0,
                'has_contraction': False,
                'has_expansion': False,
                'has_curves': False,
                'n_curves': 0,
                'has_valve_gate': False,
                'has_valve_globe': False,
                'has_valve_ball': False,
                'has_valve_check': False,
                'has_tee_through': False,
                'has_tee_branch': False,
                'n_tee_through': 0,
                'n_tee_branch': 0
            })
            st.rerun()
    
    with col_btn2:
        if len(st.session_state.pipes) > 1:
            if st.button("➖ Remover Último", use_container_width=True):
                st.session_state.pipes.pop()
                st.rerun()
    
    st.markdown("---")
    
    # Configuração de cada trecho
    for idx, pipe in enumerate(st.session_state.pipes):
        render_pipe_configuration(pipe, idx)
    
    st.markdown("---")
    st.markdown('<div class="section-title">📊 Resultados do Sistema</div>', unsafe_allow_html=True)
    
    # Extrair dados da sidebar
    rho = sidebar_data['rho']
    mu = sidebar_data['mu']
    pressure_inlet = sidebar_data['pressure_inlet']
    input_type = sidebar_data['input_type']
    flow_rate = sidebar_data['flow_rate']
    velocity = sidebar_data['velocity']
    fluid_type = sidebar_data['fluid_type']
    
    # Cálculos do sistema
    current_pressure = pressure_inlet
    total_head_loss_system = 0
    total_length_system = 0
    pipe_results = []
    
    # Calcular velocidade se entrada for por vazão
    if input_type == "Vazão (Q)":
        first_pipe = st.session_state.pipes[0]
        A_first = math.pi * (first_pipe['diameter']/2)**2
        velocity = flow_rate / A_first
    else:
        first_pipe = st.session_state.pipes[0]
        A_first = math.pi * (first_pipe['diameter']/2)**2
        flow_rate = velocity * A_first
    
    # Processar cada trecho
    for pipe in st.session_state.pipes:
        result = calculate_pipe_losses(pipe, flow_rate, rho, mu, GRAVITY)
        
        # Pressão de saída do trecho
        pressure_loss = result['h_total'] * rho * GRAVITY
        pressure_out = current_pressure - pressure_loss
        
        pipe_results.append({
            'id': pipe['id'],
            'V': result['V'],
            'Re': result['Re'],
            'regime': result['regime'],
            'f': result['f'],
            'h_distributed': result['h_distributed'],
            'h_local': result['h_local'],
            'h_elevation': result['h_elevation'],
            'h_total': result['h_total'],
            'P_in': current_pressure,
            'P_out': pressure_out,
            'K_total': result['K_total']
        })
        
        total_head_loss_system += result['h_total']
        total_length_system += pipe['length']
        current_pressure = pressure_out
    
    # Exibir resultados do sistema
    _display_system_results(flow_rate, total_head_loss_system, total_length_system, 
                           pressure_inlet, pipe_results[-1]['P_out'])
    
    # Alertas de velocidade
    _display_velocity_warnings(pipe_results, fluid_type)
    
    # Tabela detalhada
    _display_detailed_table(pipe_results)
    
    # Gráficos
    _display_pressure_profile(pipe_results, st.session_state.pipes)
    _display_losses_by_section(pipe_results)


def _display_system_results(flow_rate, total_head_loss, total_length, pressure_in, pressure_out):
    """Exibe os resultados principais do sistema"""
    st.markdown('<div class="results-card">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <h3>Vazão do Sistema</h3>
            <h2>{flow_rate:.5f} m³/s</h2>
            <small>{flow_rate*3600:.2f} m³/h</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <h3>Perda de Carga Total</h3>
            <h2>{total_head_loss:.2f} m</h2>
            <small>Comprimento: {total_length:.1f} m</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="result-card">
            <h3>Pressão Inicial</h3>
            <h2>{pressure_in/1000:.1f} kPa</h2>
            <small>{pressure_in/100000:.2f} bar</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="result-card">
            <h3>Pressão Final</h3>
            <h2>{pressure_out/1000:.1f} kPa</h2>
            <small>{pressure_out/100000:.2f} bar</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def _display_velocity_warnings(pipe_results, fluid_type):
    """Exibe alertas sobre velocidades fora das faixas recomendadas"""
    st.markdown("### ⚠️ Verificações")
    
    warnings = []
    for result in pipe_results:
        V = result['V']
        
        if fluid_type == "Água":
            if V < WATER_VELOCITY_MIN:
                warnings.append(f"⚠️ Trecho {result['id']}: Velocidade muito baixa ({V:.2f} m/s < {WATER_VELOCITY_MIN} m/s) - risco de sedimentação")
            elif V > WATER_VELOCITY_MAX:
                warnings.append(f"⚠️ Trecho {result['id']}: Velocidade muito alta ({V:.2f} m/s > {WATER_VELOCITY_MAX} m/s) - risco de erosão e ruído")
        elif fluid_type == "Ar":
            if V > AIR_VELOCITY_MAX:
                warnings.append(f"⚠️ Trecho {result['id']}: Velocidade muito alta para ar ({V:.2f} m/s > {AIR_VELOCITY_MAX} m/s)")
    
    if warnings:
        for warning in warnings:
            st.markdown(f'<div class="alert-warning">{warning}</div>', unsafe_allow_html=True)
    else:
        st.success("✅ Todas as velocidades estão dentro das faixas recomendadas!")


def _display_detailed_table(pipe_results):
    """Exibe tabela detalhada com resultados por trecho"""
    st.markdown("### 📋 Detalhamento por Trecho")
    
    df_results = pd.DataFrame([{
        'Trecho': r['id'],
        'Velocidade (m/s)': f"{r['V']:.2f}",
        'Reynolds': f"{r['Re']:,.0f}",
        'Regime': r['regime'],
        'Fator f': f"{r['f']:.4f}",
        'K total': f"{r['K_total']:.2f}",
        'h distribuída (m)': f"{r['h_distributed']:.2f}",
        'h local (m)': f"{r['h_local']:.2f}",
        'h elevação (m)': f"{r['h_elevation']:.2f}",
        'h total (m)': f"{r['h_total']:.2f}",
        'P entrada (kPa)': f"{r['P_in']/1000:.1f}",
        'P saída (kPa)': f"{r['P_out']/1000:.1f}"
    } for r in pipe_results])
    
    st.dataframe(df_results, use_container_width=True)


def _display_pressure_profile(pipe_results, pipes):
    """Exibe gráfico de perfil de pressão ao longo do sistema"""
    st.markdown("### 📉 Perfil de Pressão ao Longo do Sistema")
    
    positions = [0]
    pressures = [pipe_results[0]['P_in']/1000]  # kPa
    
    cumulative_length = 0
    for i, (pipe, result) in enumerate(zip(pipes, pipe_results)):
        cumulative_length += pipe['length']
        positions.append(cumulative_length)
        pressures.append(result['P_out']/1000)
    
    fig_pressure = go.Figure()
    fig_pressure.add_trace(go.Scatter(
        x=positions, 
        y=pressures,
        mode='lines+markers',
        name='Pressão',
        line=dict(color='#00d4ff', width=3),
        marker=dict(size=8)
    ))
    
    # Adicionar marcadores de trechos
    for i, pipe in enumerate(pipes):
        if i == 0:
            x_start = 0
        else:
            x_start = sum([p['length'] for p in pipes[:i]])
        x_end = x_start + pipe['length']
        
        fig_pressure.add_annotation(
            x=(x_start + x_end)/2,
            y=max(pressures) * 1.05,
            text=f"Trecho {pipe['id']}",
            showarrow=False,
            font=dict(color='#a8dadc', size=10)
        )
    
    fig_pressure.update_layout(
        xaxis_title="Posição ao longo do sistema (m)",
        yaxis_title="Pressão (kPa)",
        paper_bgcolor='#1f3044',
        plot_bgcolor='#2d4059',
        font=dict(color='#e0fbfc'),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_pressure, use_container_width=True)


def _display_losses_by_section(pipe_results):
    """Exibe gráfico de perdas por trecho"""
    st.markdown("### 📊 Perdas por Trecho")
    
    fig_losses = go.Figure()
    
    trechos = [f"Trecho {r['id']}" for r in pipe_results]
    h_dist = [r['h_distributed'] for r in pipe_results]
    h_loc = [r['h_local'] for r in pipe_results]
    h_elev = [r['h_elevation'] for r in pipe_results]
    
    fig_losses.add_trace(go.Bar(name='Distribuída', x=trechos, y=h_dist, marker_color='#00d4ff'))
    fig_losses.add_trace(go.Bar(name='Localizada', x=trechos, y=h_loc, marker_color='#4ecdc4'))
    fig_losses.add_trace(go.Bar(name='Elevação', x=trechos, y=h_elev, marker_color='#ffd60a'))
    
    fig_losses.update_layout(
        barmode='stack',
        xaxis_title="Trechos",
        yaxis_title="Perda de Carga (m)",
        paper_bgcolor='#1f3044',
        plot_bgcolor='#2d4059',
        font=dict(color='#e0fbfc'),
        legend=dict(bgcolor='#2d4059', bordercolor='#3d5a73', borderwidth=1)
    )
    
    st.plotly_chart(fig_losses, use_container_width=True)
