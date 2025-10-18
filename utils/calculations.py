import math
from fluids import friction_factor, Reynolds
from config.settings import GRAVITY
from utils.loss_coefficients import *

def Froude(V, L, g=GRAVITY):
    """
    Calcula o número de Froude
    V: Velocidade (m/s)
    L: Comprimento característico (m)
    g: Aceleração da gravidade (m/s²)
    """
    return V / (g * L)**0.5

def calculate_pipe_losses(pipe, flow_rate, rho, mu, g=GRAVITY):
    """
    Calcula todas as perdas de carga para um trecho de tubulação
    
    Retorna: dicionário com resultados detalhados
    """
    # Área e velocidade no trecho
    A = math.pi * (pipe['diameter']/2)**2
    V = flow_rate / A
    
    # Reynolds e fator de atrito
    Re = Reynolds(V=V, D=pipe['diameter'], rho=rho, mu=mu)
    try:
        f = friction_factor(Re=Re, eD=pipe['roughness']/pipe['diameter'])
    except:
        f = 0.02
    
    # Perda distribuída
    h_distributed = f * (pipe['length'] / pipe['diameter']) * (V**2 / (2 * g))
    
    # Perdas localizadas
    h_local = 0
    K_total = 0
    
    if pipe.get('has_contraction', False):
        K = K_contraction_round(D1=pipe['diameter']*pipe.get('contraction_ratio', 2.0), D2=pipe['diameter'])
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_expansion', False):
        K = K_expansion_round(D1=pipe['diameter'], D2=pipe['diameter']*pipe.get('expansion_ratio', 2.0))
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_curves', False):
        K = K_90_rounded(D=pipe['diameter']) * pipe.get('n_curves', 1)
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_valve_gate', False):
        K = K_valve_gate_open()
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_valve_globe', False):
        K = K_valve_globe_open()
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_valve_ball', False):
        K = K_valve_ball_open()
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_valve_check', False):
        K = K_valve_check()
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_tee_through', False):
        K = K_tee_through() * pipe.get('n_tee_through', 1)
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    if pipe.get('has_tee_branch', False):
        K = K_tee_branch() * pipe.get('n_tee_branch', 1)
        h_local += K * (V**2 / (2 * g))
        K_total += K
    
    # Perda total no trecho
    h_total_pipe = h_distributed + h_local + pipe.get('elevation_change', 0)
    
    # Regime
    if Re < 2300:
        regime = "Laminar"
    elif Re < 4000:
        regime = "Transição"
    else:
        regime = "Turbulento"
    
    return {
        'V': V,
        'Re': Re,
        'regime': regime,
        'f': f,
        'h_distributed': h_distributed,
        'h_local': h_local,
        'h_elevation': pipe.get('elevation_change', 0),
        'h_total': h_total_pipe,
        'K_total': K_total
    }

def normal_depth(Q, b, S, n):
    """
    Calcula a profundidade normal em um canal aberto usando iteração
    Q: Vazão (m³/s)
    b: Largura do canal (m)
    S: Inclinação do canal
    n: Coeficiente de Manning
    """
    y_guess = 1.0
    tolerance = 1e-6
    max_iter = 100
    
    for i in range(max_iter):
        A = b * y_guess
        P = b + 2 * y_guess
        R = A / P
        Q_calc = (1/n) * A * (R**(2/3)) * (S**0.5)
        
        if abs(Q_calc - Q) < tolerance:
            return y_guess
        
        if Q_calc < Q:
            y_guess *= 1.1
        else:
            y_guess *= 0.9
    
    return y_guess

def critical_depth(Q, b, g=GRAVITY):
    """
    Calcula a profundidade crítica em um canal aberto retangular
    Q: Vazão (m³/s)
    b: Largura do canal (m)
    g: Aceleração da gravidade (m/s²)
    """
    return (Q**2 / (g * b**2)) ** (1/3)
