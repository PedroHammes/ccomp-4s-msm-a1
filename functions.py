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

    # Período teórico (vamos usar em pequenos angulos)
    T_teorico = 2 * np.pi * np.sqrt(L / g)

    # Período simulado(instantes em que θ passa de negativo para positivo)
    # theta[:-1] é o valor antes de cada execução
    # theta[1:] é o valor depois de cada exeucção
    cruzamentos = np.where((theta[:-1] < 0) & (theta[1:] >= 0))[0] # onde o zero é cruzado na subida
    if len(cruzamentos) >= 2:
        # média dos intervalos entre cruzamentos consecutivos
        T_simulado = np.mean(np.diff(t[cruzamentos]))
    else:
        T_simulado = None   # menos de uma oscilação completa não medimos

    # Energia mecânica = cinética + potencial (altura zero no ponto mais baixo)
    energia = 0.5 * m * (L * omega) ** 2 + m * g * L * (1 - np.cos(theta))

    print("\n========== RESULTADOS — PÊNDULO ==========")
    print(f"Período teórico (pequenos ângulos): {T_teorico:.4f} s")
    if T_simulado is not None:
        diferenca = (T_simulado - T_teorico) / T_teorico * 100
        print(f"Período simulado:                   {T_simulado:.4f} s ({diferenca:+.2f}% vs teórico)")
    else:
        print("Período simulado:                   não medido (menos de uma oscilação)")
    print(f"Ângulo máximo:                      {np.degrees(np.max(np.abs(theta))):.2f}°")
    print(f"Ângulo final:                       {np.degrees(theta[-1]):.2f}°")
    print(f"Energia mecânica inicial:           {energia[0]:.4f} J")
    print(f"Energia mecânica final:             {energia[-1]:.4f} J")
    print("==========================================")

