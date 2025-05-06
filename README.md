
# Problema das N-Rainhas com Obstáculos usando Algoritmo Genético

Este projeto implementa uma solução para o problema das N-Rainhas com obstáculos utilizando um Algoritmo Genético com elitismo e minireparos.

## 📌 Descrição

O problema consiste em posicionar N rainhas em um tabuleiro NxN de forma que nenhuma rainha ataque outra, levando em consideração bloqueios aleatórios no tabuleiro. A solução foi desenvolvida com um Algoritmo Genético, utilizando técnicas como:

- Seleção por torneio
- Crossover com probabilidade configurável
- Mutação adaptada aos bloqueios
- Elitismo
- Estratégia de minirepair para reduzir conflitos

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- Bibliotecas padrão (`random`, `time`)

## 🧪 Experimentos

Os testes foram realizados para diferentes tamanhos de tabuleiro (N = 1, 2, 5, 8, 9, 10, 12, 16, 20). Os bloqueios foram gerados automaticamente com 7% de casas bloqueadas e um limite máximo de 13%.

Resultados mostram que o algoritmo encontra soluções eficientes para a maioria dos tamanhos, exceto N=2, que não possui solução possível (mesmo sem bloqueios).

O algoritmo genético demonstrou ser mais eficaz que algoritmos como A*, especialmente devido à sua capacidade de lidar com o grande espaço de busca e presença de obstáculos.

## 💻 Especificações da Máquina

- Sistema Operacional: Windows 11
- Processador: AMD Ryzen 5 5600G
- Memória RAM: 16 GB
- IDE: Visual Studio Code

## ▶️ Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/djhonatah/NRainhas_IA.git
   ```

2. Entre na pasta do projeto:
   ```bash
   cd NRainhas_IA
   ```

3. Abra o projeto no VS Code (opcional):
   ```bash
   code .
   ```

4. Execute o arquivo principal diretamente pelo terminal ou pelo botão "Run":
   ```bash
   python algoritmo_genetico.py
   ```

## 📊 Resultados Obtidos

| n  | Solução Encontrada | Gerações Usadas | Tempo      |
|----|--------------------|------------------|------------|
| 1  | True               | 1                | ~3.06 ms   |
| 2  | False              | 2000             | ~56.59 ms  |
| 5  | True               | 14               | ~37.27 ms  |
| 8  | True               | 15               | ~53.65 ms  |
| 9  | True               | 2                | ~51.71 ms  |
| 10 | True               | 4                | ~64.13 ms  |
| 12 | True               | 1                | ~63.67 ms  |
| 16 | True               | 1                | ~104.79 ms |
| 20 | True               | 2                | ~138.58 ms |

## 📝 Licença

Este projeto está licenciado sob a Licença MIT.
