import streamlit as st
from config.settings import configure_page
from components.styles import apply_custom_styles
from components.sidebar import create_sidebar
from tabs.pipe_system import render_pipe_system_tab
from tabs.simulations import render_simulations_tab
from tabs.about import render_about_tab

# Configuração da página
configure_page()

# Aplicar estilos personalizados
apply_custom_styles()

# Título principal
st.markdown('<div class="main-header">Simulação de Escoamento - Sistema de Tubulações</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análise completa de sistemas com múltiplos trechos, pressões variáveis e otimização</div>', unsafe_allow_html=True)

# Inicializar session state para tubos
if 'pipes' not in st.session_state:
    st.session_state.pipes = [{
        'id': 1,
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
    }]

# Criar sidebar e obter configurações
sidebar_data = create_sidebar()

# Layout principal com abas
tab1, tab2, tab3 = st.tabs(["📊 Sistema de Tubos",  "📈 Simulações", "ℹ️ Sobre"])

with tab1:
    render_pipe_system_tab(sidebar_data)

with tab2:
    render_simulations_tab(sidebar_data)

with tab3:
    render_about_tab()


# Rodapé
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #a8dadc;'>"
    "Desenvolvido com Streamlit • Simulações Avançadas de Engenharia de Escoamento"
    "</div>",
    unsafe_allow_html=True
)
