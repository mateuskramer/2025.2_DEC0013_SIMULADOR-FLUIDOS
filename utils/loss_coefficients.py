"""
Coeficientes de perda de carga localizada (K) para diversos acessórios
"""

def K_contraction_round(D1, D2):
    """
    Coeficiente K para contração arredondada
    D1: Diâmetro maior (upstream)
    D2: Diâmetro menor (downstream)
    """
    beta = D2 / D1
    if beta >= 1:
        return 0
    return 0.5 * (1 - beta**2)

def K_expansion_round(D1, D2):
    """
    Coeficiente K para expansão arredondada
    D1: Diâmetro menor (upstream)
    D2: Diâmetro maior (downstream)
    """
    beta = D1 / D2
    if beta >= 1:
        return 0
    return (1 - beta**2)**2

def K_90_rounded(D, angle=90, fd=None, rc_ratio=1.5):
    """
    Coeficiente K para curva de 90° arredondada
    D: Diâmetro do tubo
    angle: Ângulo da curva (graus)
    fd: Fator de atrito (não usado nesta simplificação)
    rc_ratio: Razão raio de curvatura / diâmetro
    """
    return 0.3

def K_valve_gate_open():
    """Coeficiente K para válvula gaveta totalmente aberta"""
    return 0.15

def K_valve_globe_open():
    """Coeficiente K para válvula globo totalmente aberta"""
    return 10.0

def K_valve_ball_open():
    """Coeficiente K para válvula esfera totalmente aberta"""
    return 0.05

def K_valve_check():
    """Coeficiente K para válvula de retenção"""
    return 2.5

def K_tee_through():
    """Coeficiente K para tê - passagem direta"""
    return 0.6

def K_tee_branch():
    """Coeficiente K para tê - passagem lateral"""
    return 1.8
