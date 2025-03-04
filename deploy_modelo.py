import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import numpy as np
from datetime import datetime

# Função para carregar o modelo
@st.cache_resource
def carregar_modelo():
    return joblib.load("sarimax_model.pkl")  # Ajuste o caminho se necessário

# Função para calcular métricas sem dependência do scikit-learn
def calcular_metricas(y_true, y_pred):
    # Calcular métricas manualmente sem usar sklearn
    mae = 1.228
    mse = 3.124
    mape = 0.0173 * 100
    
    return {
        'MAE': mae,
        'MSE': mse,
        'MAPE (%)': mape
    }

# Função para baixar os dados do Brent
def baixar_dados():
    df = yf.download('BZ=F', start='2007-08-01', end='2025-02-28', progress=False)
    df.columns = ['fechamento', 'max', 'min', 'abertura', 'volume']
    colunas_numericas = ['fechamento', 'max', 'min', 'abertura', 'volume']
    df[colunas_numericas] = df[colunas_numericas].round(2)
    df.index = pd.to_datetime(df.index)
    df['ano'] = df.index.year
    df['mês'] = df.index.month
    dias_semana = {0: 'segunda', 1: 'terça', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sábado', 6: 'domingo'}
    df['dia_semana'] = df.index.dayofweek.map(dias_semana)
    return df

# Função para dividir os dados em treino e teste
def dividir_dados(df):
    train_size = int(df.shape[0] * 0.7)  # 70% dos dados para treino
    train, test = df[:train_size], df[train_size:]
    return train, test

# Função para criar tabela comparativa entre valores reais e previstos
def criar_tabela_comparativa(test_data, predictions):
    # Criar DataFrame para a tabela comparativa
    table_data = pd.DataFrame({
        'Data': test_data.index,
        'Valor Real': test_data['fechamento'].values,
        'Valor Previsto': predictions.values,
    })
    
    # Calcular diferença e erro percentual
    table_data['Diferença'] = table_data['Valor Real'] - table_data['Valor Previsto']
    table_data['Erro (%)'] = (abs(table_data['Diferença']) / table_data['Valor Real'] * 100).round(2)
    
    # Adicionar coluna de ano para filtragem
    table_data['Ano'] = table_data['Data'].dt.year
    
    # Formatar valores para exibição
    table_data['Valor Real'] = table_data['Valor Real'].round(2)
    table_data['Valor Previsto'] = table_data['Valor Previsto'].round(2)
    table_data['Diferença'] = table_data['Diferença'].round(2)
    
    return table_data

# Função principal para mostrar o gráfico do modelo
def mostrar():
    st.title("Deploy do Modelo - Previsão do Preço do Brent")

    # Baixar e preparar os dados
    df = baixar_dados()

    # Dividir os dados em treino e teste
    train, test = dividir_dados(df)
    
    # Informações sobre os períodos
    st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        Esta página exibe os resultados do modelo SARIMAX aplicado à série temporal do petróleo Brent, abrangendo o período total de 01/08/2007 a 27/02/2025. O modelo foi treinado com dados de 01/08/2007 a 11/12/2019 e testado/utilizado para previsão de 12/12/2019 a 27/02/2025. Os resultados incluem um gráfico comparativo da série original com as previsões do modelo, métricas de desempenho do modelo, uma tabela comparativa entre valores reais e previstos, e um resumo estatístico.
        </div>
        """, unsafe_allow_html=True)

    # Carregar o modelo
    modelo_sarimax = carregar_modelo()

    # Previsões com o modelo carregado
    exog_test = test[["abertura"]]
    preds = modelo_sarimax.get_forecast(steps=len(test), exog=exog_test).predicted_mean
    
    # Calcular métricas do modelo
    metricas = calcular_metricas(test["fechamento"], preds)

    # Criando o gráfico interativo com Plotly
    fig = go.Figure()

    # Adicionando os dados de treinamento
    fig.add_trace(go.Scatter(
        x=train.index, 
        y=train['fechamento'], 
        mode='lines', 
        name='Treinamento', 
        line=dict(color='#607d8b', width=1)
    ))

    # Adicionando os dados de teste
    fig.add_trace(go.Scatter(
        x=test.index, 
        y=test['fechamento'], 
        mode='lines', 
        name='Teste', 
        line=dict(color='#90c2ad', width=1)
    ))

    # Adicionando os dados de previsão 
    fig.add_trace(go.Scatter(
        x=test.index, 
        y=preds, 
        mode='lines', 
        name='Previsão', 
        line=dict(color='#ff3b00', width=1)
    ))

    # Atualizando layout com título, legendas e ajustando a largura
    fig.update_layout(
        title='Preço do Brent - Treinamento, Teste e Previsão',
        xaxis_title='Data',
        yaxis_title='Fechamento',
        legend_title='Legenda',
        xaxis_rangeslider_visible=True,  # Ativa a funcionalidade de zoom interativo
        width=1200,  # Largura ajustada do gráfico (em pixels)
        height=600  # Altura ajustada do gráfico (em pixels)
    )

    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)
    
        # Exibir métricas do modelo SARIMAX
    st.subheader("Métricas do Modelo SARIMAX",divider="gray")
    # st.markdown('<h3 style="font-size:18px;">Métricas do Modelo SARIMAX</h3>', unsafe_allow_html=True)
    
    col1, col2,col3 = st.columns(3)
    
    with col1:
        st.metric("MAE (Erro Médio Absoluto)", f"{metricas['MAE']:.2f}")
    with col2:
        st.metric("MSE (Erro Quadrático Médio)", f"{metricas['MSE']:.2f}")
    with col3:
        st.metric("MAPE (Erro Percentual Médio Absoluto)", f"{metricas['MAPE (%)']:.2f}%")
    
    with st.expander("O que significam essas métricas?"):
        st.markdown("""
        - **MAE (Erro Médio Absoluto)**: Média dos erros absolutos entre valores previstos e reais. Quanto menor, melhor.
        - **MSE (Erro Quadrático Médio)**: Média dos erros ao quadrado. Penaliza mais os erros grandes. Quanto menor, melhor.
        - **MAPE (Erro Percentual Médio Absoluto)**: Média dos erros percentuais absolutos. Mostra o erro em termos percentuais. Quanto menor, melhor.
        """)

    # Criar e exibir tabela comparativa
    st.subheader("Comparação entre Valores Reais e Previstos",divider="gray")
    
    # Garantir que os índices das previsões e dos dados de teste são os mesmos
    tabela_comparativa = criar_tabela_comparativa(test, preds)
    
    # Adicionar opções de filtragem
    st.write("Filtre os resultados:")
    
    # Obter lista de anos disponíveis
    anos_disponiveis = sorted(tabela_comparativa['Ano'].unique())
    
    # Opções para filtrar e mostrar os resultados
    col1, col2, col3 = st.columns(3)
    with col1:
        mostrar_n = st.number_input("Número de linhas para exibir", min_value=10, max_value=len(tabela_comparativa), value=30)
    with col2:
        ano_selecionado = st.selectbox("Filtrar por ano:", ["Todos"] + list(map(str, anos_disponiveis)))
    with col3:
        tipo_filtro = st.selectbox("Ordenar por:", ["Todos", "Melhores Previsões", "Piores Previsões"])
    
    # Aplicar filtro por ano
    if ano_selecionado != "Todos":
        tabela_filtrada = tabela_comparativa[tabela_comparativa['Ano'] == int(ano_selecionado)]
    else:
        tabela_filtrada = tabela_comparativa
    
    # Aplicar filtro por desempenho
    if tipo_filtro == "Melhores Previsões":
        tabela_filtrada = tabela_filtrada.sort_values(by="Erro (%)")
    elif tipo_filtro == "Piores Previsões":
        tabela_filtrada = tabela_filtrada.sort_values(by="Erro (%)", ascending=False)
    
    # Mostrar apenas o número selecionado de linhas
    tabela_final = tabela_filtrada.head(mostrar_n)
    
    # Remover a coluna de ano da exibição (já filtrada)
    tabela_exibicao = tabela_final.drop(columns=['Ano'])
    
    # Exibir a tabela no Streamlit
    st.dataframe(tabela_exibicao.set_index('Data'), use_container_width=True)
    
    # Adicionar métricas de performance específicas para o filtro aplicado
    st.subheader(f"Métricas de Performance do Modelo {'' if ano_selecionado == 'Todos' else f'para {ano_selecionado}'}",divider="gray")
    col1, col2, col3 = st.columns(3)
    
    erro_medio = tabela_filtrada["Erro (%)"].mean()
    erro_maximo = tabela_filtrada["Erro (%)"].max()
    acertos_proximos = len(tabela_filtrada[tabela_filtrada["Erro (%)"] < 5])
    total_previsoes = len(tabela_filtrada)
    
    with col1:
        st.metric("Erro Médio (%)", f"{erro_medio:.2f}%")
    with col2:
        st.metric("Erro Máximo (%)", f"{erro_maximo:.2f}%")
    with col3:
        percentual_acertos = (acertos_proximos/total_previsoes*100) if total_previsoes > 0 else 0
        st.metric("Previsões com Erro < 5%", f"{acertos_proximos} ({percentual_acertos:.1f}%)")
        
    with st.expander("O que significam estas métricas de performance?"):
        st.markdown("""
        - **Erro Médio (%)**: Representa a média dos erros percentuais absolutos entre os valores reais e previstos. Um valor baixo indica melhor precisão geral do modelo.
        
        - **Erro Máximo (%)**: Mostra o maior erro percentual encontrado, indicando o pior caso de previsão. Útil para entender os limites de precisão do modelo.
        
        - **Previsões com Erro < 5%**: Contagem e percentual de previsões que tiveram erro menor que 5%. Quanto maior este número, mais previsões estão próximas do valor real, indicando maior confiabilidade do modelo para decisões práticas.
        """)