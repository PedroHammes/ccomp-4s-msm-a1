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

    # Vetor de tempo. Progressão Aritmetica partindo de termo 0 e razão dt (Unidade 4, página 11)
    t = np.arange(0.0, t_total, dt)
    n = len(t)

    # vetor para guardar as variaveis de estado (tamanho previsto)
    theta = np.zeros(n)     # cria array de tamanho n prenchido com zeros
    omega = np.zeros(n)

    theta[0] = theta0 # variavel em radianos: precisa estar assim para não quebrar a formula
    omega[0] = omega0

    for i in range(n-1):
        # 1) aceleração no instante i (equação do pêndulo)
        alfa = -(g / L) * np.sin(theta[i]) - (b / m) * omega[i]

        # 2) nova velocidade a partir da velocidade atual e da aceleração 
        omega[i + 1] = omega[i] + alfa * dt

        # 3) novo ângulo usando a velocidade NOVA (incrementação padrão)
        theta[i + 1] = theta[i] + omega[i + 1] * dt

