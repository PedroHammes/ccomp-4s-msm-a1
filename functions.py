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

    # vetor de tempo: PA com primeiro termo 0 e razao dt (Unidade 4, p. 11)
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

    # energia mecanica = cinetica + potencial (altura 0 no ponto mais baixo)
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