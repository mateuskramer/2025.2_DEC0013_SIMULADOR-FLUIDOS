import streamlit as st
from utils.calculations import normal_depth, critical_depth, Froude

def render_open_channels_tab():
    """Renderiza a aba de Canais Abertos"""
    st.header("Canais Abertos (Escoamento Livre)")
    
    with st.container():
        st.markdown('<div class="section-title">📋 Especificações do Canal</div>', unsafe_allow_html=True)
        st.markdown('<div class="specs-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parâmetros do Canal")
            Q_canal = st.number_input("Vazão (Q, m³/s)", value=1.0, min_value=0.01, max_value=100.0, step=0.1, key="flow_rate_canal")
            b = st.number_input("Largura do canal (b, m)", value=2.0, min_value=0.1, max_value=20.0, step=0.1, key="width")
        
        with col2:
            st.subheader("Propriedades do Canal")
            S = st.number_input("Inclinação (S)", value=0.001, min_value=0.0001, max_value=0.1, step=0.0001, format="%.4f", key="slope")
            n_manning = st.number_input("Coeficiente de Manning (n)", value=0.013, min_value=0.01, max_value=0.1, step=0.001, format="%.3f", key="manning")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="section-title">📊 Resultados do Canal</div>', unsafe_allow_html=True)
        st.markdown('<div class="results-card">', unsafe_allow_html=True)
        
        # Cálculos
        y_normal = normal_depth(Q_canal, b, S, n_manning)
        y_critical = critical_depth(Q_canal, b)
        
        A_normal = b * y_normal
        V_normal = Q_canal / A_normal
        Fr = Froude(V=V_normal, L=y_normal)
        
        regime_open = "Supercrítico" if Fr > 1 else "Subcrítico" if Fr < 1 else "Crítico"
        regime_color_open = "#ff6b6b" if Fr > 1 else "#00d4ff" if Fr < 1 else "#ffd60a"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
                <h3>Profundidade Normal</h3>
                <h2>{y_normal:.3f} m</h2>
                <small>Altura da lâmina d'água</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-card">
                <h3>Profundidade Crítica</h3>
                <h2>{y_critical:.3f} m</h2>
                <small>Transição de regime</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="result-card">
                <h3>Velocidade Média</h3>
                <h2>{V_normal:.2f} m/s</h2>
                <small>No escoamento normal</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="result-card">
                <h3>Número de Froude</h3>
                <h2 style="color: {regime_color_open}">{Fr:.2f}</h2>
                <p style="color: {regime_color_open}; font-weight: bold;">{regime_open}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.subheader("📏 Geometria do Canal")
            st.write(f"**Área molhada:** {A_normal:.3f} m²")
            st.write(f"**Perímetro molhado:** {b + 2*y_normal:.3f} m")
            st.write(f"**Raio hidráulico:** {A_normal/(b + 2*y_normal):.3f} m")
        
        with col_info2:
            st.subheader("🌊 Características do Escoamento")
            st.write(f"**Vazão:** {Q_canal:.3f} m³/s")
            st.write(f"**Inclinação:** {S:.4f}")
            st.write(f"**Coeficiente de Manning:** {n_manning:.3f}")
        
        st.markdown('</div>', unsafe_allow_html=True)
