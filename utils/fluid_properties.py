import numpy as np
from config.settings import GAS_CONSTANT, AIR_GAS_CONSTANT

def rho_water(T):
    """
    Calcula a densidade da água em função da temperatura
    T: Temperatura em Kelvin
    Retorna: Densidade em kg/m³
    """
    if T < 273.15:
        return 1000
    elif T > 373.15:
        return 958
    else:
        return 1000 - 0.42 * (T - 273.15)

def mu_water(T):
    """
    Calcula a viscosidade dinâmica da água em função da temperatura
    T: Temperatura em Kelvin
    Retorna: Viscosidade em Pa.s
    """
    if T <= 273.15:
        return 0.00179
    elif T >= 373.15:
        return 0.00028
    else:
        temps = [273.15, 283.15, 293.15, 303.15, 313.15, 323.15, 333.15, 343.15, 353.15, 363.15, 373.15]
        viscosities = [0.00179, 0.00131, 0.00100, 0.00080, 0.00065, 0.00055, 0.00047, 0.00040, 0.00035, 0.00031, 0.00028]
        return np.interp(T, temps, viscosities)

def rho_air(T, P=101325):
    """
    Calcula a densidade do ar em função da temperatura e pressão
    T: Temperatura em Kelvin
    P: Pressão em Pa (padrão: 101325 Pa = 1 atm)
    Retorna: Densidade em kg/m³
    """
    return P / (AIR_GAS_CONSTANT * T)

def mu_air(T):
    """
    Calcula a viscosidade dinâmica do ar usando a equação de Sutherland
    T: Temperatura em Kelvin
    Retorna: Viscosidade em Pa.s
    """
    T0 = 273.15
    mu0 = 1.716e-5
    S = 110.4
    return mu0 * (T/T0)**1.5 * (T0 + S)/(T + S)

def rho_light_oil(T):
    """
    Densidade do óleo leve (simplificado)
    T: Temperatura em Kelvin
    Retorna: Densidade em kg/m³
    """
    return 850

def mu_light_oil(T):
    """
    Viscosidade dinâmica do óleo leve (simplificado)
    T: Temperatura em Kelvin
    Retorna: Viscosidade em Pa.s
    """
    return 0.01

def rho_ideal_gas(P, T, M):
    """
    Calcula a densidade de um gás ideal
    P: Pressão em Pa
    T: Temperatura em Kelvin
    M: Massa molar em kg/mol
    Retorna: Densidade em kg/m³
    """
    return (P * M) / (GAS_CONSTANT * T)

def get_fluid_properties(fluid_type, temp, pressure, gas_molar_mass=0.02896, custom_rho=None, custom_mu=None):
    """
    Retorna as propriedades do fluido (densidade, viscosidade dinâmica e cinemática)
    
    Parâmetros:
    - fluid_type: Tipo de fluido ("Água", "Ar", "Óleo", "Gás ideal", "Personalizado")
    - temp: Temperatura em °C
    - pressure: Pressão em Pa
    - gas_molar_mass: Massa molar para gás ideal (kg/mol)
    - custom_rho: Densidade personalizada (kg/m³)
    - custom_mu: Viscosidade personalizada (Pa.s)
    
    Retorna: (rho, mu, nu)
    """
    T_K = temp + 273.15
    
    if fluid_type == "Água":
        rho = rho_water(T_K)
        mu = mu_water(T_K)
    elif fluid_type == "Ar":
        rho = rho_air(T_K, pressure)
        mu = mu_air(T_K)
    elif fluid_type == "Óleo":
        rho = rho_light_oil(T_K)
        mu = mu_light_oil(T_K)
    elif fluid_type == "Gás ideal":
        rho = rho_ideal_gas(pressure, T_K, gas_molar_mass)
        mu = mu_air(T_K)
    else:  # Personalizado
        rho = custom_rho if custom_rho is not None else 1000.0
        mu = custom_mu if custom_mu is not None else 0.001
    
    nu = mu / rho
    return rho, mu, nu
