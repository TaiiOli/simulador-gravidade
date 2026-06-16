# 🌌 AI-Powered Trajectory Prediction & Simulation

## Sobre o projeto
Este projeto é um simulador interativo de sistemas gravitacionais combinado com um modelo de Machine Learning para previsão de trajetórias.

A aplicação integra:
- Simulação física baseada em gravidade
- Pipeline de dados (geração, tratamento e modelagem)
- Modelo preditivo com XGBoost
- Visualização interativa em 3D

## Objetivo
Demonstrar como dados históricos podem ser usados para prever comportamentos futuros em sistemas dinâmicos complexos.

Esse tipo de abordagem pode ser aplicado em cenários reais como:
- Detecção de anomalias
- Previsão de padrões comportamentais
- Monitoramento de eventos em séries temporais (ex: transações financeiras)

## Como funciona

### 1. Simulação física
- Cálculo de forças gravitacionais entre corpos
- Atualização de posição e velocidade ao longo do tempo

### 2. Engenharia de features
- Criação de variáveis como:
  - posição atual (x, y)
  - lag de posição
  - velocidade (vx, vy)

### 3. Modelagem
- Treinamento com XGBoost para prever a próxima posição
- Divisão treino/teste
- Avaliação com MSE

### 4. Visualização
- Gráfico 3D com Plotly
- Comparação entre:
  - trajetória real
  - previsão da IA

## Tecnologias utilizadas
- Python
- Pandas / NumPy
- XGBoost
- Plotly
- Streamlit
- Scikit-learn

## Resultados
- Modelo capaz de prever trajetórias com baixo erro (MSE)
- Demonstração visual clara do poder preditivo da IA

## Possíveis aplicações
- Detecção de fraudes (identificação de padrões anômalos)
- Previsão de comportamento do usuário
- Sistemas de recomendação
- Monitoramento em tempo real

## Como executar
```bash

git clone https://github.com/TaiiOli/simulador-gravidade.git

pip install -r requirements.txt

streamlit run main.py
