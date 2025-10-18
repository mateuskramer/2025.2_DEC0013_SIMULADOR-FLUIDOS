import streamlit as st
from utils.fluid_properties import get_fluid_properties
import math

def create_sidebar():
    """
    Cria a sidebar com todos os inputs e retorna os dados configurados
    Retorna: dicionário com todas as configurações
    """
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Seleção de fluido e temperatura
        st.subheader("Fluido e Propriedades")
        fluid_type = st.selectbox(
            "Tipo de Fluido",
            ["Água", "Ar", "Óleo", "Gás ideal", "Personalizado"]
        )
        
        temp = st.number_input("Temperatura (°C)", value=20.0, min_value=-50.0, max_value=500.0, step=1.0)
        
        if fluid_type == "Gás ideal":
            pressure_inlet = st.number_input("Pressão inicial (Pa)", value=300000.0, min_value=1000.0, max_value=1e7, step=1000.0)
            gas_molar_mass = st.number_input("Massa molar (kg/mol)", value=0.02896, min_value=0.001, max_value=0.2, step=0.001)
        else:
            pressure_inlet = st.number_input("Pressão inicial (Pa)", value=300000.0, min_value=1000.0, max_value=1e7, step=1000.0)
            gas_molar_mass = 0.02896
        
        # Obter propriedades do fluido
        custom_rho = None
        custom_mu = None
        
        if fluid_type == "Personalizado":
            col1, col2 = st.columns(2)
            with col1:
                custom_rho = st.number_input("Densidade (kg/m³)", value=1000.0, min_value=1.0, max_value=2000.0, step=10.0)
            with col2:
                custom_mu = st.number_input("Viscosidade (Pa.s)", value=0.001, min_value=1e-6, max_value=1.0, step=0.0001, format="%.6f")
        
        rho, mu, nu = get_fluid_properties(
            fluid_type, temp, pressure_inlet, 
            gas_molar_mass, custom_rho, custom_mu
        )
        
        st.info(f"**Propriedades do Fluido:**\n- Densidade: {rho:.2f} kg/m³\n- Viscosidade: {mu:.6f} Pa.s\n- Viscosidade cinemática: {nu:.8f} m²/s")
        
        # Vazão ou Velocidade
        st.subheader("Condições de Escoamento")
        input_type = st.radio("Entrada por:", ["Vazão (Q)", "Velocidade (V)"])
        
        if input_type == "Vazão (Q)":
            flow_rate = st.number_input("Vazão (m³/s)", value=0.01571, min_value=0.0001, max_value=10.0, step=0.001, format="%.5f")
            velocity = None
        else:
            velocity = st.number_input("Velocidade (m/s)", value=2.0, min_value=0.01, max_value=50.0, step=0.1)
            flow_rate = None
        
        return {
            'fluid_type': fluid_type,
            'temp': temp,
            'pressure_inlet': pressure_inlet,
            'gas_molar_mass': gas_molar_mass,
            'rho': rho,
            'mu': mu,
            'nu': nu,
            'input_type': input_type,
            'flow_rate': flow_rate,
            'velocity': velocity
        }