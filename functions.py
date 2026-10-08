import numpy as np
import matplotlib.pyplot as plt


def read_param(message, default):
    # le um valor digitado; se apertar Enter, usa o valor padrao
    text = input(f"{message} [{default}]: ")
    if text == "":
        return default
    return float(text)


def pendulo():
    print("\nParametros do pendulo (Enter mantem o padrao)")

    # constantes do sistema
    L = read_param("Comprimento do fio L (m)", 1.0)
    g = read_param("Gravidade g (m/s^2)", 9.8)
    m = read_param("Massa m (kg)", 1.0)

    # atrito, 0 = sem atrito
    b = read_param("Coeficiente de amortecimento b (kg/s)", 0.0)

    # estado inicial (eq. de 2a ordem precisa de angulo e velocidade)
    theta0_graus = read_param("Angulo inicial theta0 (graus)", 30.0)
    omega0 = read_param("Velocidade angular inicial w0 (rad/s)", 0.0)

    # parametros da simulacao
    t_total = 20.0  # tempo total (s)
    dt = 0.001      # passo de tempo (s)

    theta0 = np.radians(theta0_graus)  # a formula usa radianos

    # vetor de tempo: PA com primeiro termo 0 e razao dt
    t = np.arange(0.0, t_total, dt)
    n = len(t)

    # vetores de estado, ja com o tamanho final
    theta = np.zeros(n)
    omega = np.zeros(n)

    # condicoes iniciais
    theta[0] = theta0
    omega[0] = omega0

    # Euler-Cromer: calcula a velocidade nova e usa ela pra atualizar o angulo
    for i in range(n - 1):
        alfa = -(g / L) * np.sin(theta[i]) - (b / m) * omega[i]
        omega[i + 1] = omega[i] + alfa * dt
        theta[i + 1] = theta[i] + omega[i + 1] * dt

    # periodo teorico, so vale pra angulos pequenos
    T_teorico = 2 * np.pi * np.sqrt(L / g)

    # periodo simulado: tempo entre as passagens de theta por zero subindo
    cruzamentos = np.where((theta[:-1] < 0) & (theta[1:] >= 0))[0]
    if len(cruzamentos) >= 2:
        T_simulado = np.mean(np.diff(t[cruzamentos]))
    else:
        T_simulado = None  # nao deu uma oscilacao completa

    # energia mecanica = cinetica + potencial
    energia = 0.5 * m * (L * omega) ** 2 + m * g * L * (1 - np.cos(theta))

    print("\n--- Resultados: pendulo ---")
    print(f"Periodo teorico (angulos pequenos): {T_teorico:.4f} s")
    if T_simulado is not None:
        diferenca = (T_simulado - T_teorico) / T_teorico * 100
        print(f"Periodo simulado: {T_simulado:.4f} s ({diferenca:+.2f}% em relacao ao teorico)")
    else:
        print("Periodo simulado: nao medido (menos de uma oscilacao)")
    print(f"Angulo maximo: {np.degrees(np.max(np.abs(theta))):.2f} graus")
    print(f"Angulo final: {np.degrees(theta[-1]):.2f} graus")
    print(f"Energia inicial: {energia[0]:.4f} J")
    print(f"Energia final: {energia[-1]:.4f} J\n")

    # graficos de angulo, velocidade e energia no mesmo eixo de tempo
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    fig.suptitle(f"Pendulo (L={L} m, m={m} kg, theta0={theta0_graus} graus, b={b} kg/s)")

    ax1.plot(t, np.degrees(theta))
    ax1.set_ylabel("theta (graus)")
    ax1.grid(True)

    ax2.plot(t, omega, color="tab:orange")
    ax2.set_ylabel("w (rad/s)")
    ax2.grid(True)

    ax3.plot(t, energia, color="tab:green")
    ax3.set_ylabel("Energia (J)")
    ax3.set_xlabel("Tempo (s)")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()


def mola_sem_atrito():
    print("\nParametros da mola sem atrito (Enter mantem o padrao)")

    # constantes do sistema
    m = read_param("Massa m (kg)", 1.0)
    k = read_param("Constante da mola k (N/m)", 4.0)
    b = 0.0  # sem atrito fixo em 0

    # estado inicial
    x0 = read_param("Posicao inicial x0 (m)", 1.0)
    v0 = read_param("Velocidade inicial v0 (m/s)", 0.0)

    # parametros da simulacao
    t_total = 20.0
    dt = 0.001

    t = np.arange(0.0, t_total, dt)
    n = len(t)

    x = np.zeros(n)
    v = np.zeros(n)

    x[0] = x0
    v[0] = v0

    # Euler-Cromer para o sistema massa-mola linear
    for i in range(n - 1):
        a = -(k / m) * x[i] - (b / m) * v[i]
        v[i + 1] = v[i] + a * dt
        x[i + 1] = x[i] + v[i + 1] * dt  # usa a velocidade nova

    # periodo teorico da mola
    T_teorico = 2 * np.pi * np.sqrt(m / k)

    # periodo simulado: passagens de x por zero subindo
    cruzamentos = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    if len(cruzamentos) >= 2:
        T_simulado = np.mean(np.diff(t[cruzamentos]))
    else:
        T_simulado = None

    # energia mecanica = cinetica (0.5*m*v^2) + elastica (0.5*k*x^2)
    energia = 0.5 * m * (v ** 2) + 0.5 * k * (x ** 2)

    print("\n--- Resultados: mola sem atrito ---")
    print(f"Periodo teorico: {T_teorico:.4f} s")
    if T_simulado is not None:
        diferenca = (T_simulado - T_teorico) / T_teorico * 100
        print(f"Periodo simulado: {T_simulado:.4f} s ({diferenca:+.2f}% em relacao ao teorico)")
    else:
        print("Periodo simulado: nao medido (menos de uma oscilacao)")
    print(f"Amplitude maxima: {np.max(np.abs(x)):.4f} m")
    print(f"Posicao final: {x[-1]:.4f} m")
    print(f"Energia inicial: {energia[0]:.4f} J")
    print(f"Energia final: {energia[-1]:.4f} J\n")

    # graficos de posicao, velocidade e energia
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    fig.suptitle(f"Massa-Mola Sem Atrito (m={m} kg, k={k} N/m, x0={x0} m, v0={v0} m/s)")

    ax1.plot(t, x)
    ax1.set_ylabel("Posicao x (m)")
    ax1.grid(True)

    ax2.plot(t, v, color="tab:orange")
    ax2.set_ylabel("Velocidade v (m/s)")
    ax2.grid(True)

    ax3.plot(t, energia, color="tab:green")
    ax3.set_ylabel("Energia (J)")
    ax3.set_xlabel("Tempo (s)")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()


def mola_com_atrito():
    print("\nParametros da mola com atrito (Enter mantem o padrao)")

    # constantes do sistema
    m = read_param("Massa m (kg)", 1.0)
    k = read_param("Constante da mola k (N/m)", 4.0)
    b = read_param("Coeficiente de amortecimento b (kg/s)", 0.5)

    # estado inicial
    x0 = read_param("Posicao inicial x0 (m)", 1.0)
    v0 = read_param("Velocidade inicial v0 (m/s)", 0.0)

    # parametros da simulacao
    t_total = 20.0
    dt = 0.001

    t = np.arange(0.0, t_total, dt)
    n = len(t)

    x = np.zeros(n)
    v = np.zeros(n)

    x[0] = x0
    v[0] = v0

    # Euler-Cromer com termo de amortecimento
    for i in range(n - 1):
        a = -(k / m) * x[i] - (b / m) * v[i]
        v[i + 1] = v[i] + a * dt
        x[i + 1] = x[i] + v[i + 1] * dt

    # periodo teorico de referencia (sem atrito)
    T_teorico = 2 * np.pi * np.sqrt(m / k)

    # periodo simulado
    cruzamentos = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    if len(cruzamentos) >= 2:
        T_simulado = np.mean(np.diff(t[cruzamentos]))
    else:
        T_simulado = None

    # classificacao do amortecimento
    b_critico = 2 * np.sqrt(m * k)
    if b < b_critico:
        tipo_amortecimento = "subamortecido (oscila, amplitude decai)"
    elif np.isclose(b, b_critico):
        tipo_amortecimento = "critico (retorna ao equilibrio sem oscilar)"
    else:
        tipo_amortecimento = "superamortecido (retorna devagar sem oscilar)"

    # energia mecanica
    energia = 0.5 * m * (v ** 2) + 0.5 * k * (x ** 2)

    print("\n--- Resultados: mola com atrito ---")
    print(f"Tipo de amortecimento: {tipo_amortecimento}")
    print(f"Periodo teorico de referencia: {T_teorico:.4f} s")
    if T_simulado is not None:
        print(f"Periodo simulado: {T_simulado:.4f} s")
    else:
        print("Periodo simulado: nao medido (sistema nao oscilatorio)")
    print(f"Amplitude maxima: {np.max(np.abs(x)):.4f} m")
    print(f"Posicao final: {x[-1]:.4f} m")
    print(f"Energia inicial: {energia[0]:.4f} J")
    print(f"Energia final: {energia[-1]:.4f} J\n")

    # graficos
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
    fig.suptitle(f"Massa-Mola Com Atrito (m={m}, k={k}, b={b}, x0={x0}, v0={v0})")

    ax1.plot(t, x)
    ax1.set_ylabel("Posicao x (m)")
    ax1.grid(True)

    ax2.plot(t, v, color="tab:orange")
    ax2.set_ylabel("Velocidade v (m/s)")
    ax2.grid(True)

    ax3.plot(t, energia, color="tab:green")
    ax3.set_ylabel("Energia (J)")
    ax3.set_xlabel("Tempo (s)")
    ax3.grid(True)

    plt.tight_layout()
    plt.show()