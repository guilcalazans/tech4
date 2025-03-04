import streamlit as st
import pandas as pd
import streamlit as st

def mostrar():
    st.title("Modelagem")

    # Injetando CSS para remover qualquer resquício de vermelho e ajustar animações
    st.markdown("""
        <style>
        /* Aba ativa */
        div[data-baseweb="tab-list"] button[aria-selected="true"] {
            color: #6d97b2 !important;  /* Cor do texto da aba ativa */
            border-bottom: 3px solid #6d97b2 !important;  /* Linha inferior da aba ativa */
            font-weight: bold !important;  /* Deixa o texto em negrito */
        }

        /* Quando o mouse passa por cima */
        div[data-baseweb="tab-list"] button:hover {
            color: #6d97b2 !important;  /* Muda a cor do texto no hover */
            border-bottom: 3px solid #6d97b2 !important;  /* Linha inferior no hover */
        }

        /* Corrige a animação vermelha ao selecionar uma aba */
        div[data-baseweb="tab-list"] button {
            transition: all 0.3s ease-in-out !important;  /* Suaviza a transição */
        }

        /* Removendo qualquer efeito vermelho padrão */
        div[data-baseweb="tab-highlight"] {
            background-color: #6d97b2 !important;  /* Substitui a cor da animação */
        }
        </style>
    """, unsafe_allow_html=True)

    # Criando abas para navegação interna
    abas = st.tabs(["Preparação dos Dados", "Modelagem","Conclusão"])

    with abas[0]:
        st.subheader("4. Preparação dos Dados",divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        Nesta etapa, a preparação dos dados é fundamental para garantir a eficácia dos modelos preditivos. Para isso, são realizadas três principais ações: transformação da série temporal em estacionária, definição dos parâmetros para modelagem e divisão dos dados em treino e teste.        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("4.1 Estacionariedade",divider="gray")
        st.markdown("""
        Uma série temporal é considerada estacionária quando possui   propriedade   estatísticas  razoavelmente estáveis ao longo do tempo (no que se diz sobre média e à variância).
        Ao longo da Análise Exploratória dos Dados a série temporal apresentou caracteristicas não estacionarárias. O teste ADF (valor-p = 0,15) confirmou essa característica, evidenciando a necessidade de transformação (diferenciação) da série para garantir a estacionariedade e permitir uma modelagem mais precisa.
        Uma vez que a estacionariedade reduz a influência de tendências e facilita a identificação de padrões relevantes.
        """, unsafe_allow_html=True)

        with st.expander("Teste ADF"): 
            st.code("""
                    # Executar o teste de Dickey-Fuller Aumentado (ADF)
                    adf_result = sm.tsa.adfuller(df["fechamento"])

                    # Organizar os resultados em um DataFrame
                    adf_table = pd.DataFrame({
                        "Métrica": ["Estatística ADF", "Valor-p", "Valor Crítico 1%", "Valor Crítico 5%", "Valor Crítico 10%"],
                        "Valor": [round(adf_result[0], 2), round(adf_result[1], 2),
                                round(adf_result[4]['1%'], 2), round(adf_result[4]['5%'], 2),
                                round(adf_result[4]['10%'], 2)]
                    })

                    # Exibir a tabela formatada
                    print(adf_table.to_string(index=False))

                    # Verificar se a série é estacionária
                    if adf_result[1] < 0.05:
                        print("A série temporal é estacionária")
                    else:
                        print("A série temporal não é estacionária")
                                    """, language="python")
            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "Estatística ADF", 
                    "Valor-p", 
                    "Valor Crítico 1%", 
                    "Valor Crítico 5%", 
                    "Valor Crítico 10%"
                ],
                "Valor": [
                    -2.36, 
                    0.15, 
                    -3.43, 
                    -2.86, 
                    -2.57
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela
            st.write(df)
            # Adicionando uma observação
            st.markdown("**A série temporal não é estacionária.**")

        #Diferenciação
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">4.1.1 Diferenciação para estacionariedade </p>', unsafe_allow_html=True)
        st.write("""
            A fim de garantir a qualidade das análises e previsões, a série temporal foi transformada em estacionária por meio da diferenciação. Essa etapa é fundamental para remover componentes não estacionários, como tendências e sazonalidades, que podem prejudicar a modelagem.
            """)
        with st.expander("Resultado"): 
            st.write("""
            A estacionariedade da série, confirmada pelo teste ADF e Gráfico 16, permite dar prosseguimento à próxima etapa que consiste em identificar os parâmetros mais adequados para os modelos, a fim de capturar a dinâmica da série e gerar previsões precisas.
            """)
            st.code("""
            # Diferenciar a série uma vez e remover valores NaN
            df_diff = df["fechamento"].diff().dropna()

                # Executar o teste de Dickey-Fuller Aumentado (ADF) na série diferenciada
                adf_result = sm.tsa.adfuller(df_diff)

                # Organizar os resultados em um DataFrame
                adf_table = pd.DataFrame({
                    "Métrica": ["Estatística ADF", "Valor-p", "Valor Crítico 1%", "Valor Crítico 5%", "Valor Crítico 10%"],
                    "Valor": [round(adf_result[0], 2), round(adf_result[1], 2),
                            round(adf_result[4]['1%'], 2), round(adf_result[4]['5%'], 2),
                            round(adf_result[4]['10%'], 2)]
                })

                # Exibir a tabela formatada
                print(adf_table.to_string(index=False))

                # Verificar se a série diferenciada é estacionária
                if adf_result[1] < 0.05:
                    print("A série temporal diferenciada é estacionária")
                else:
                    print("A série temporal diferenciada não é estacionária")
            """, language="python")

            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "Estatística ADF", 
                    "Valor-p", 
                    "Valor Crítico 1%", 
                    "Valor Crítico 5%", 
                    "Valor Crítico 10%"
                ],
                "Valor": [
                    -15.76, 
                    0.00, 
                    -3.43, 
                    -2.86, 
                    -2.57
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela
            st.write(df)
            # Adicionando uma observação
            st.markdown("**A série temporal diferenciada é estacionária.**")

            # Carregar o SVG
            with open("imagens/18.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
                """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 16:** Transformação para Estacionariedade: Comparação entre a série original não estacionária e a série diferenciada, estacionária, obtida por meio da primeira diferença.", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("4.2 Definição dos parâmetros para modelagem",divider="gray")
        st.markdown("""
        Determinar os coeficientes de autoregressão (ARIMA) e os parâmetros sazonais (SARIMA), é uma etapa essencial para capturar a estrutura temporal dos dados e melhorar a precisão das previsões.
        """, unsafe_allow_html=True)

        #Coeficientes de autoregressão (ARIMA)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">4.2.1 Coeficientes de autoregressão (ARIMA) </p>', unsafe_allow_html=True)
        st.write("""
            Uma vez que a série temporal é estacionaria é possível obter os coeficientes de regressão : p, d e q. Esses coeficientes são essenciais para construir um modelo ARIMA adequado, que consiga capturar as dinâmicas da série temporal de forma eficaz, permitindo previsões mais precisas.

            * ACF é usada para determinar o parâmetro 𝑞, identificando a ordem da parte de médias móveis do modelo.
            * PACF é usada para determinar o parâmetro 𝑝, identificando a ordem da parte autoregressiva do modelo.
            *𝑑 foi previamente identificado como o número de diferenciações necessárias para tornar a série estacionária.
        """)
        with st.expander("**Resultado obtido:** (2, 1, 227)"): 
            st.code("""
            #Código utilizado para obter o parâmetro
            acf_x = sm.tsa.acf(df["fechamento"], alpha=0.05, nlags=500) #consigo apartir de 227
            acf, ci = acf_x[:2]
            # identificação do q pelo ponto de interceptação ao 95% com o acf
            q = np.where(abs(acf) < (ci[:, 1] - acf))[0][0]

            pacf_x = sm.tsa.pacf(df["fechamento"], alpha=0.05, nlags=30) #apartir de 2 dias
            pacf, ci = pacf_x[:2]
            # identificação do p pelo ponto de interceptação ao 95% com o pacf
            p = np.where(abs(pacf) < (ci[:, 1] - pacf))[0][0]

            d = 1  # apenas 1 diferenciação foi necessária para tornar a série estacionária

            #parametros do modelo ARIMA (autorregressivel com a média móvel)

            print("Valor de p:", p)
            print("Valor de d:", d)
            print("Valor de q:", q)
            
            """, language="python")
            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "Valor de p", 
                    "Valor de d", 
                    "Valor de q"
                ],
                "Valor": [
                    2, 
                    1, 
                    227
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela no Streamlit
            st.write(df)

        #Parâmetros de sazonalidade (SARIMA)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">4.2.2 Parâmetros de sazonalidade (SARIMA) </p>', unsafe_allow_html=True)
        st.write("""
            Para determinar os parâmetros de sazonalidade, foi utilizada a função model = pm.auto_arima.
        """)
        with st.expander("**Resultado obtido:** ARIMA(3,1,2)(1,0,0)[12] - SARIMA(3,1,2)(1,0,0,12)[12]"): 
            st.write('Esse modelo (1, 0, 0, 12) indica um ciclo sazonal de 12 meses, mas não leva em conta a autocorrelação ou a média móvel sazonal. Essa configuração sugere que a série temporal apresenta um padrão sazonal regular, sem complexidades adicionais.')
            st.code("""
            #Código utilizado para obter o parâmetro
            model = pm.auto_arima(
                df["fechamento"],
                seasonal=True,
                m=12,
                stepwise=True,
                trace=True,
            )

            # Summary of the model's detected parameters
            print(model.summary())

            # Detected seasonal order
            seasonal_order = model.seasonal_order
            print(f"Detected Seasonal Order: {seasonal_order}")
            """, language="python")
            
            # Carregar o imagem
            st.image("imagens/sarimax.png", width=700)
    
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("4.3 Dividindo os Dados em Treino e Teste",divider="gray")
        st.markdown("""
            Para avaliar a performance do modelo, os dados foram divididos em conjuntos de treinamento (70%) e teste (30%). O modelo foi treinado com o conjunto de treino e, em seguida, avaliado com o conjunto de teste.""", unsafe_allow_html=True)
        
        with st.expander("**Resultado obtido:** "): 
            st.code("""
            #Código utilizado dividir dataset em treino e teste
            train_size = int(df.shape[0] * 0.7)  # 70% dos dados para treino
            train, test = df[:train_size], df[train_size:]

            # Preparação dos dados para XGBoost (usando a data do índice)
            def create_features(modelo_df):
                modelo_df = modelo_df.copy()  # Evitar alterações na versão original
                modelo_df["year"] = modelo_df.index.year
                modelo_df["month"] = modelo_df.index.month
                modelo_df["day"] = modelo_df.index.day
                modelo_df["dayofweek"] = modelo_df.index.dayofweek
                return modelo_df

            train = create_features(train)
            test = create_features(test)

            FEATURES = ["year", "month", "day", "dayofweek", "abertura"]
            TARGET = "fechamento"
                    
            # Configurações do gráfico
            plt.figure(figsize=(22, 4))
            plt.gca().set_facecolor('#fdfefe')
            plt.grid(color='lightgray', linestyle='--', linewidth=0.5)

            # Plotando os dados de treino e teste
            plt.plot(train.index, train['fechamento'], color='#607d8b', linewidth=1, label='Treinamento')
            plt.plot(test.index, test['fechamento'], color='#52be80', linewidth=1, label='Teste')

            # Configurações dos rótulos e título
            plt.xlabel('Data', fontsize=12)
            plt.ylabel('Fechamento', fontsize=12)
            plt.title('Dados de Treinamento e Teste do Brent', fontsize=14)
            plt.legend()

            # Exibindo o gráfico
            plt.show()
            
            """, language="python")
            # Carregar o SVG
            with open("imagens/19.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)

            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 17:** Divisão dos Dados do Brent: Treino e Teste.", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)     
       
    with abas[1]:
        st.subheader("5. Modelagem",divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        Após a preparação dos dados, será realizada a escolha do modelo de previsão, que é crucial para obter previsões precisas. Três modelos de aprendizado serão testados com dados de treinamento e teste, e o desempenho será avaliado pelo MAPE (Mean Absolute Percentage Error) para identificar o ajuste mais adequado aos dados do Brent.
        
        > O MAPE mostra o quanto, em média, as previsões de um modelo estão erradas em relação aos valores reais, expressando esse erro em porcentagem. Logo, **quanto menor o MAPE melhor**.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("5.1 Modelo XGBoost",divider="gray")
        st.write("""
        **O que é:** O XGBoost é um algoritmo de machine learning baseado em boosting de árvores de decisão, conhecido por seu alto desempenho, mas suscetível a overfitting e menos adequado para séries temporais que requerem médias móveis, como em séries temporais financeiras.
        
        **Resultado:** XGBoost teve um MAPE de 2.64%.
        
        **Observações:** Este modelo demonstra excelente precisão (97,36%) na previsão dos preços do Brent. Observa-se um ajuste muito próximo entre as linhas de previsão (laranja) e dados reais (azul) ao longo de todo o período 2020-2025. O modelo captura com eficiência tanto os picos quanto as quedas bruscas, incluindo a queda histórica durante a pandemia em 2020. É notável como as previsões acompanham precisamente até mesmo as pequenas flutuações diárias.
        """)
        with st.expander("**Resultado obtido:** "): 
            st.code("""
            # Modelo XGBoost
            X_train, y_train = train[FEATURES], train[TARGET]
            X_test, y_test = test[FEATURES], test[TARGET]

            reg = xgb.XGBRegressor(objective="reg:squarederror")
            reg.fit(X_train, y_train)

            # Avaliação XGBoost
            preds = reg.predict(X_test)
            metrics_xgb = calculate_metrics(y_test, preds)
            print("XGBoost Metrics:")
            print_metrics(metrics_xgb)
            """, language="python")

            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "MAE", 
                    "MSE", 
                    "MAPE"
                ],
                "Valor": [
                    round(1.5832083125812249, 2), 
                    round(5.4108420147725536, 2), 
                    "2.64 %"
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela no Streamlit
            st.write(df)
            
            st.code("""
                # Plotar resultados
                plt.figure(figsize=(22, 4))
                plt.plot(test.index, y_test, label='Dados Reais', color='blue', linewidth=1)  # Linha real
                plt.plot(test.index, preds, label='Previsões', color='orange', linewidth=1)  # Previsões
                plt.title('Previsão com Modelo XGBoost - 97.36%')
                plt.xlabel('Data')
                plt.ylabel('Fechamento')
                plt.legend()
                plt.grid()
                plt.show()
            """, language="python")

            # Carregar o SVG
            with open("imagens/20.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)

            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 18:** Desempenho do Modelo XGBoost. O gráfico mostra uma comparação entre os dados reais do Brent (em azul) e as previsões geradas por um modelo XGBoost (em laranja) ao longo do tempo.", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True) 

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("5.2 Modelo Prophet",divider="gray")
        st.write("""
        **O que é:** O Prophet é um modelo de previsão de séries temporais, desenvolvido pelo Facebook, que lida bem com tendências e sazonalidades. Ele utiliza médias móveis e suavização exponencial para ajustar tendências de longo prazo, capturando variações sazonais e eventos externos, sendo eficaz em dados financeiros complexos.
        
        **Resultado:** O Prophet teve um MAPE de 20.35 %.
        
        **Observações:** Este modelo apresenta a menor precisão (79,65%) entre os três. Diferentemente dos outros, o Prophet mostra um intervalo de confiança (área cinza) e cobre um período histórico mais longo (desde 2008). Observa-se que as previsões começam apenas em 2020, e há divergências significativas em alguns períodos, especialmente em 2023-2024, onde o modelo não captura adequadamente algumas oscilações de preço.
        """)
        with st.expander("**Resultado obtido:** "): 
            st.code("""
                # Ajustando os dados para Prophet
                train_prophet = train.rename(columns={"fechamento": "y"}).copy()
                train_prophet["ds"] = train_prophet.index

                test_prophet = test.rename(columns={"fechamento": "y"}).copy()
                test_prophet["ds"] = test_prophet.index

                # Criando o modelo Prophet
                model = Prophet(daily_seasonality=True)
                model.add_regressor("abertura")
                model.fit(train_prophet)

                # Criando datas futuras para a previsão
                future = model.make_future_dataframe(periods=len(test))
                future = future.set_index("ds").join(pd.concat([train, test])["abertura"]).reset_index()

                # Preenchendo valores ausentes de "abertura"
                future["abertura"] = future["abertura"].ffill()

                # Fazendo previsão
                forecast = model.predict(future)

                # Preparando os dados para avaliação
                preds = forecast[["ds", "yhat"]].set_index("ds").tail(len(test))
                y_test = test_prophet.set_index("ds")["y"]

                # Calculando métricas
                metrics_pr = calculate_metrics(y_test, preds["yhat"])
                print("Prophet Metrics:")
                print_metrics(metrics_pr)
            """, language="python")

            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "MAE", 
                    "MSE", 
                    "MAPE"
                ],
                "Valor": [
                    round(14.749836402334529, 2), 
                    round(358.9347409005401, 2), 
                    "20.35 %"
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela no Streamlit
            st.write(df)
            
            st.code("""
                # Plotar resultados do modelo prophet
                plt.figure(figsize=(20, 4))
                plt.plot(y_test.index, y_test, label='Dados Reais', color='blue', linewidth=0.5)  # Linha fina
                plt.plot(preds.index, preds['yhat'], label='Previsões', color='orange', linewidth=0.5)  # Linha fina
                plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2, label='Intervalo de Confiança', linewidth=0.5)
                plt.title('Previsão com Modelo Prophe - 79.65%')
                plt.xlabel('Data')
                plt.ylabel('Fechamento')
                plt.legend()
                plt.grid()
                plt.show()
            """, language="python")

            # Carregar o SVG
            with open("imagens/21.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)

            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 19:** Desempenho do Modelo Prophet. O gráfico apresenta a previsão do modelo Prophet aplicado à série temporal do Brent, comparando dados reais (linha azul) com as previsões do modelo (linha laranja) e o intervalo de confiança (área cinza).", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True) 


        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("5.3 Modelo SARIMAX",divider="gray")
        st.write("""
        **O que é:** O SARIMAX é um modelo de séries temporais que integra autoregressão, médias móveis, sazonalidade e variáveis exógenas, sendo especialmente útil para dados financeiros com padrões sazonais e influenciados por fatores externos, como taxas de juros e indicadores econômicos.
                 
        **Resultado:** O SARIMAX teve um MAPE de 1.73 %.
        
        **Observações:** Este modelo apresenta a maior precisão entre os três (98,27%). As linhas de previsão e valores reais praticamente se sobrepõem, tornando difícil distinguir uma da outra em vários trechos. O SARIMAX captura com excelência os movimentos de alta volatilidade (como o pico de 2022) e também os períodos de tendência. O ajuste é excepcionalmente bom em todo o intervalo temporal analisado.
        """)
        with st.expander("**Resultado obtido:** "): 
            st.code("""
            # Modelo SARIMAX
            # p, d, q = (2, 1, 227)
            exog_train = train[["abertura"]]
            exog_test = test[["abertura"]]

            model = sm.tsa.statespace.SARIMAX(
                train["abertura"],
                exog=exog_train,
                order=(
                    p,
                    d,
                    10,
                ),  # q muito grande faz com que o modelo fique muito complexo e lento
                seasonal_order=(1, 0, 0, 12),
            )
            results = model.fit()

            preds = results.get_forecast(steps=len(test), exog=exog_test).predicted_mean

            metrics_sarimax = calculate_metrics(test["fechamento"], preds)
            print("SARIMAX Metrics:")
            print_metrics(metrics_sarimax)
            """, language="python")

            # Criando o DataFrame com os dados
            dados = {
                "Métrica": [
                    "MAE", 
                    "MSE", 
                    "MAPE"
                ],
                "Valor": [
                    round(1.2281504296386694, 2), 
                    round(3.124917408120124, 2), 
                    "1.73 %"
                ]
            }
            df = pd.DataFrame(dados)
            # Exibindo a tabela no Streamlit
            st.write(df)
            
            st.code("""
                # Plotando os resultados
                plt.figure(figsize=(18, 4))
                plt.plot(test.index, test["fechamento"], label='Valor Esperado (Real)', color='blue', linestyle='--')
                plt.plot(test.index, preds, label='Valor Previsto SARIMAX', color='orange')
                plt.title('Comparação entre Valor Esperado e Valor Previsto com SARIMAX - 98.27%')
                plt.xlabel('Data')
                plt.ylabel('Fechamento')
                plt.legend()
                plt.xticks(rotation=45)  # Rotaciona as labels do eixo x para melhor legibilidade
                plt.grid()
                plt.tight_layout()
                plt.show()
            """, language="python")

            # Carregar o SVG
            with open("imagens/22.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)

            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 20:** Desempenho do Modelo SARIMAX. O gráfico apresenta a previsão do modelo SARIMAX aplicado à série temporal do Brent, comparando dados reais (linha azul) com as previsões do modelo (linha laranja).", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True) 

    with abas[2]:
            st.subheader("6. Conclusão",divider="gray")
            st.markdown("""
            <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
            Para avaliar a precisão das previsões, três modelos foram comparados: SARIMAX, Prophet e XGBoost. Utilizando o erro percentual médio absoluto (MAPE) como métrica, o <b>SARIMAX apresentou o melhor desempenho, com um MAPE de 1,74%</b>
            . O XGBoost, com um MAPE de 2,64%, também demonstrou bons resultados. Já o Prophet, com um MAPE significativamente maior (20,35%), mostrou dificuldades em capturar as nuances dos dados da série do Brent.
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("""
                Diante dos resultados, o modelo SARIMAX se mostrou o mais adequado para prever o comportamento complexo do Brent pelos seguintes motivos:

                1. Apresenta a maior precisão (98,27%) entre os três modelos analisados.
                2. Captura com excelência tanto tendências quanto flutuações de curto prazo
                3. Seu desempenho é consistente ao longo de todo o período analisado
                4. Alinha-se com a característica de autocorrelação do Brent identificada anteriormente, onde os coeficientes PACF indicavam a importância dos lags mais recentes, enquanto o ACF mostrava persistência - características que o SARIMAX é especialmente projetado para modelar através de seus componentes sazonal e autorregressivo
                5. É particularmente adequado para séries temporais com potenciais componentes sazonais, como o mercado de petróleo que pode sofrer influências cíclicas de fatores econômicos e geopolíticos.
                6. Apesar do XGBoost apresentar resultado muito próximo o SARIMAX demonstra ligeira superioridade na precisão e maior adequação conceitual à estrutura temporal identificada na série do Brent.
                
            """)

            st.warning('Para obter mais informações sobre as métricas e códigos utilizados na análise e plotagem, acesse o Jupyter desenvolvido no Google Colab.', icon="⚠️")
