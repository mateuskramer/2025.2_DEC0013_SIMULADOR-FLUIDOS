import streamlit as st
from config.settings import TUBE_MATERIALS

def render_pipe_configuration(pipe, idx):
    """
    Renderiza a configuração de um trecho de tubulação
    
    Parâmetros:
    - pipe: Dicionário com dados do tubo
    - idx: Índice do tubo na lista
    """
    with st.expander(f"🔧 Trecho {pipe['id']}", expanded=(idx == 0)):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parâmetros do Tubo")
            pipe['material'] = st.selectbox(
                f"Material", 
                list(TUBE_MATERIALS.keys()), 
                index=list(TUBE_MATERIALS.keys()).index(pipe['material']),
                key=f"mat_{pipe['id']}"
            )
            
            if pipe['material'] == "Personalizado":
                pipe['roughness'] = st.number_input(
                    f"Rugosidade (m)", 
                    value=0.000045, 
                    min_value=0.0, 
                    max_value=0.01, 
                    step=0.000001, 
                    format="%.6f",
                    key=f"rough_{pipe['id']}"
                )
            else:
                pipe['roughness'] = TUBE_MATERIALS[pipe['material']]
                st.info(f"Rugosidade: {pipe['roughness']:.8f} m")
            
            pipe['diameter'] = st.number_input(
                f"Diâmetro (m)", 
                value=pipe['diameter'], 
                min_value=0.001, 
                max_value=2.0, 
                step=0.01,
                key=f"diam_{pipe['id']}"
            )
            
            pipe['length'] = st.number_input(
                f"Comprimento (m)", 
                value=pipe['length'], 
                min_value=0.1, 
                max_value=10000.0, 
                step=10.0,
                key=f"len_{pipe['id']}"
            )
            
            pipe['elevation_change'] = st.number_input(
                f"Desnível (m) - positivo se sobe", 
                value=pipe['elevation_change'], 
                min_value=-1000.0, 
                max_value=1000.0, 
                step=1.0,
                key=f"elev_{pipe['id']}"
            )
        
        with col2:
            st.subheader("Acessórios e Singularidades")
            
            col2a, col2b = st.columns(2)
            
            with col2a:
                st.write("**Geometria:**")
                pipe['has_contraction'] = st.checkbox("Contração", key=f"contr_{pipe['id']}")
                if pipe['has_contraction']:
                    pipe['contraction_ratio'] = st.number_input(
                        "Razão D₁/D₂", 
                        value=2.0, 
                        min_value=1.01, 
                        max_value=10.0,
                        key=f"contr_r_{pipe['id']}"
                    )
                
                pipe['has_expansion'] = st.checkbox("Expansão", key=f"exp_{pipe['id']}")
                if pipe['has_expansion']:
                    pipe['expansion_ratio'] = st.number_input(
                        "Razão D₂/D₁", 
                        value=2.0, 
                        min_value=1.01, 
                        max_value=10.0,
                        key=f"exp_r_{pipe['id']}"
                    )
                
                pipe['has_curves'] = st.checkbox("Curvas 90°", key=f"curv_{pipe['id']}")
                if pipe['has_curves']:
                    pipe['n_curves'] = st.number_input(
                        "Número", 
                        value=1, 
                        min_value=1, 
                        max_value=20,
                        key=f"n_curv_{pipe['id']}"
                    )
            
            with col2b:
                st.write("**Válvulas:**")
                pipe['has_valve_gate'] = st.checkbox("Gaveta", key=f"vg_{pipe['id']}")
                pipe['has_valve_globe'] = st.checkbox("Globo", key=f"vgl_{pipe['id']}")
                pipe['has_valve_ball'] = st.checkbox("Esfera", key=f"vb_{pipe['id']}")
                pipe['has_valve_check'] = st.checkbox("Retenção", key=f"vc_{pipe['id']}")
                
                st.write("**Tês:**")
                pipe['has_tee_through'] = st.checkbox("Passagem direta", key=f"tt_{pipe['id']}")
                if pipe['has_tee_through']:
                    pipe['n_tee_through'] = st.number_input(
                        "Qtd", 
                        value=1, 
                        min_value=1, 
                        max_value=10,
                        key=f"n_tt_{pipe['id']}"
                    )
                
                pipe['has_tee_branch'] = st.checkbox("Lateral", key=f"tb_{pipe['id']}")
                if pipe['has_tee_branch']:
                    pipe['n_tee_branch'] = st.number_input(
                        "Qtd", 
                        value=1, 
                        min_value=1, 
                        max_value=10,
                        key=f"n_tb_{pipe['id']}"
                    )
