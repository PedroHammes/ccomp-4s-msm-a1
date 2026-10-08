# Guia para os colaboradores: massa-mola com e sem atrito

Trabalho A1 de MSM. Prazo: **quinta, 08/10, 23:59**.
Meta interna: as duas funções no `main` até as **13h** de quinta, para dar tempo de tirar os prints e montar o relatório.

---

## 1. Onde o projeto está

- O **pêndulo está pronto**, em `functions.py`, na função `pendulo()`. Ele é o **modelo a seguir**: leiam essa função antes de começar.
- O `main.py` tem o menu. As opções 1 e 2 ainda não chamam nada.
- **Falta fazer:** `mola_sem_atrito()` e `mola_com_atrito()`, as duas também em `functions.py`.

## 2. Preparar o ambiente

```bash
git clone https://github.com/PedroHammes/ccomp-4s-msm-a1.git
cd ccomp-4s-msm-a1
pip install numpy matplotlib
python main.py        # testem a opção 3 (pêndulo) antes de mexer em qualquer coisa
```

## 3. O que cada função precisa fazer

Cada função **não recebe argumentos** e faz, nesta ordem, as mesmas 5 etapas do pêndulo:

1. Ler os parâmetros com `read_param(mensagem, padrao)`, que já existe em `functions.py`. Não criem outra.
2. Criar os vetores `t`, `x` e `v` com numpy.
3. Rodar o laço de **Euler-Cromer**.
4. Imprimir os resultados numéricos.
5. Plotar os gráficos e chamar `plt.show()`.

Depois, no `main.py`, troquem os `print("")` das opções 1 e 2 por `functions.mola_sem_atrito()` e `functions.mola_com_atrito()`.

## 4. A física

Pela 2ª Lei de Newton, com a força da mola (Lei de Hooke) e a força do amortecedor:

```
m·x'' = -k·x - b·x'      =>      x'' = -(k/m)·x - (b/m)·x'
```

- **x**: posição em relação ao equilíbrio (m). **x'** = **v**: velocidade (m/s).
- **Sem atrito:** b = 0, e a equação fica x'' = -(k/m)·x.
- É a mesma estrutura do pêndulo, com uma diferença: aqui é **x**, e não sen θ. Por isso a mola é um sistema **linear**, e o período teórico vale para **qualquer amplitude**.

### Parâmetros

| Parâmetro | Unidade | Padrão | Sem atrito | Com atrito |
|---|---|---|---|---|
| m (massa) | kg | 1.0 | lê | lê |
| k (constante da mola) | N/m | 4.0 | lê | lê |
| b (amortecimento) | kg/s | 0.5 | **não lê, b = 0** | lê |
| x0 (posição inicial) | m | 1.0 | lê | lê |
| v0 (velocidade inicial) | m/s | 0.0 | lê | lê |
| t_total | s | 20.0 | fixo no código | fixo no código |
| dt | s | 0.001 | fixo no código | fixo no código |

A equação é de 2ª ordem, então **precisa de duas condições iniciais**: x0 e v0.

### O laço (Euler-Cromer)

```python
for i in range(n - 1):
    a = -(k / m) * x[i] - (b / m) * v[i]
    v[i + 1] = v[i] + a * dt
    x[i + 1] = x[i] + v[i + 1] * dt    # usa a velocidade NOVA
```

Usem `v[i + 1]` na última linha. Com `v[i]` vira o Euler simples, e a energia cresce sozinha: a amplitude aumenta sem nenhuma fonte de energia.

## 5. Resultados que cada função deve imprimir

**As duas:**
- Período teórico: `T = 2π·√(m/k)`
- Período simulado: copiem a lógica dos `cruzamentos` do pêndulo, trocando `theta` por `x`.
- Amplitude máxima (`np.max(np.abs(x))`) e posição final (`x[-1]`).
- Energia inicial e final: `E = 0.5·m·v² + 0.5·k·x²`

**Só a com atrito:** o tipo de amortecimento, comparando b com `2·√(m·k)`:

| Condição | Tipo | Comportamento |
|---|---|---|
| b < 2√(mk) | subamortecido | oscila, e a amplitude vai caindo |
| b = 2√(mk) | crítico | volta ao equilíbrio o mais rápido possível, sem oscilar |
| b > 2√(mk) | superamortecido | volta devagar, sem oscilar |

Nos casos crítico e superamortecido não há oscilação, então o período simulado sai "não medido". O `if len(cruzamentos) >= 2` do pêndulo já trata isso.

Opcional: o período com atrito leve é `T = 2π / √(k/m - (b/2m)²)`, um pouco maior que o sem atrito.

## 6. Gráficos

Igual ao pêndulo: `plt.subplots(3, 1, sharex=True)` com:
1. x(t), posição (m)
2. v(t), velocidade (m/s)
3. energia(t) (J)

## 7. Valores para conferir

Rodem estes casos. Os números precisam bater:

| Caso | Período simulado | Energia inicial, final |
|---|---|---|
| m=1, k=4, sem atrito | 3.1416 s (teórico: π = 3.1416) | 2.0000, 2.0020 |
| m=4, k=4, sem atrito | 6.2835 s (teórico: 2π) | 2.0000, 1.9993 |
| m=1, k=4, b=0.5 | 3.166 s (subamortecido) | 2.0000, ~0.0001 |
| m=1, k=4, b=4 | não medido (crítico) | 2.0000, ~0 |
| m=1, k=4, b=10 | não medido (superamortecido) | 2.0000, ~0 |

Todos com x0 = 1, v0 = 0. Se a energia **sem atrito** crescer muito (mais que ~1%), provavelmente está sendo usado `v[i]` em vez de `v[i + 1]` no laço.

## 8. Padrão de código

- Comentários curtos, em português, explicando a física ou a decisão, e não repetindo o código.
- Mensagens sem acento e sem símbolos especiais (θ, ω, °), como no pêndulo. Isso evita problema no terminal do Windows.
- Nomes de variáveis: `x0` e `v0` para os valores iniciais, `x` e `v` para os vetores. **Não confundam** `v` com `v0`: foi exatamente esse tipo de erro (`omega` × `omega0`) que quebrou o pêndulo.
- `t_total` e `dt` fixos no código.

## 9. Git

```bash
git pull origin main                 # sempre antes de começar
git checkout -b mola-sem-atrito      # ou mola-com-atrito
# ... trabalhar ...
git add functions.py main.py
git commit -m "Mola sem atrito: simulacao, resultados e graficos"
git push -u origin mola-sem-atrito
```

Depois, abram um **Pull Request para a `main`** no GitHub. Como as duas duplas mexem no mesmo `functions.py`, **escrevam cada função no fim do arquivo** e não alterem `pendulo()` nem `read_param()`. Assim o merge sai sem conflito.

## 10. Para o relatório (anotem enquanto programam)

- Prints do terminal com os resultados e da janela de gráficos, para 2 ou 3 cenários.
- Um parágrafo explicando cada sistema: equação, parâmetros e o que os gráficos mostram.
- Comparações que valem uma linha nas conclusões:
  - Mola: o período **não depende da amplitude** (linear). Pêndulo: **depende** (não linear).
  - Sem atrito, a energia é constante. Com atrito, cai.
  - O efeito do valor de b: sub, crítico e superamortecido.

## Referências

- Bassanezi, Bertone e Jafelice, *Modelagem Matemática*, UFU, 2014: p. 46 (recorrência e validação), p. 99 (EDO de 2ª ordem a·y'' + b·y' + c·y = 0) e p. 107 (contínuo × discreto).
- Oséias Farias, *Modelagem Matemática e simulação do Sistema Massa Mola Amortecedor* (Medium, 2022): dedução pela 2ª Lei de Newton. Ele usa a biblioteca `control`; **nós não**, porque o enunciado pede numpy e matplotlib.
- Material do professor, Unidade 4: p. 8 (recorrência) e p. 11 (P.A.).
- OpenStax *University Physics* vol. 1: seção 15.1 (movimento harmônico simples), 15.2 (energia) e 15.5 (oscilações amortecidas).
- numpy: [`arange`](https://numpy.org/doc/stable/reference/generated/numpy.arange.html), [`zeros`](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html), [`where`](https://numpy.org/doc/stable/reference/generated/numpy.where.html), [`diff`](https://numpy.org/doc/stable/reference/generated/numpy.diff.html)
- matplotlib: [`pyplot.subplots`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)