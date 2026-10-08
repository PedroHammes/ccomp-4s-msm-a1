import numpy as np

def read_param(message, default):
    """Recebe um valor do usuário, se apertar Enter devolve o valor defauilt"""
    text = input(f"{message} [{default}]: ")
    if text == "":
        return default
    return float(text)

def pendulo():
    """Simulação do pêndulo"""
    print("\nParâmetros do pêndulo (Enter = deafault)")

    # Constantes da fórmila
    L = read_param("Comprimento do fio L (m)", 1.0)
    g = read_param("Gravidade g (m/s^2)", 9.8)
    m = read_param("Massa m (kg)", 1.0)

    # Atrito (sem atrito = 0)
    b = read_param("Coeficiente de amortecimento b (kg/s)", 0.0)

    # Estado inicial (equ. de seg. ordem)
    theta0_graus = read_param("Ângulo incial 0 (graud)", 30.0)
    omega = read_param("Velocidade angular inicial w0 (rad/s)", 0.0)

    # Discretização: constantes da simulação
    t_total = 20.0  # tmepo total (s)
    dt = 0.001      # passo de tempo(s)

    # Radianos informados em graus
    theta0 = np.radians(theta0_graus)
