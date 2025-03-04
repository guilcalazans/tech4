import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np

def mostrar():
    st.title("Dashboard Brent")

    # CSS para estilização
    st.markdown("""
    <style>
        .main-header {
            font-size: 24px;
            font-weight: bold;
            color: #1E3D59;
            margin-bottom: 20px;
        }
        .metric-card {
            background-color: #f7f7f7;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .sub-header {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin: 20px 0 10px 0;
        }
        .explanation {
            font-size: 14px;
            color: #555;
            background-color: #f5f5f5;
            padding: 10px;
            border-left: 3px solid #1E3D59;
            margin: 5px 0 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Function to download Brent Oil data (reusing your approach)
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def baixar_dados(start_date='2007-08-01', end_date=None):
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        df = yf.download('BZ=F', start=start_date, end=end_date, progress=False)
        
        # Get the actual number of columns from the downloaded data
        num_columns = len(df.columns)
        
        # Correctly rename columns based on what Yahoo Finance returns
        if num_columns == 6:  # Standard Yahoo Finance format
            df.columns = ['abertura', 'max', 'min', 'fechamento', 'adj_close', 'volume']
        elif num_columns == 5:  # The format from the original code
            df.columns = ['fechamento', 'max', 'min', 'abertura', 'volume']
        
        # Round numeric columns
        df = df.round(2)
        
        # Process dates as in original code
        df.index = pd.to_datetime(df.index)
        df['ano'] = df.index.year
        df['mês'] = df.index.month
        df['dia'] = df.index.day
        
        # Add day of week
        dias_semana = {0: 'segunda', 1: 'terça', 2: 'quarta', 3: 'quinta', 4: 'sexta', 5: 'sábado', 6: 'domingo'}
        df['dia_semana'] = df.index.dayofweek.map(dias_semana)
        
        # Add additional useful features
        df['variacao_diaria'] = df['fechamento'].pct_change() * 100
        df['variacao_diaria_abs'] = df['variacao_diaria'].abs()
        df['amplitude'] = (df['max'] - df['min']).round(2)
        df['amplitude_percentual'] = ((df['max'] - df['min']) / df['abertura'] * 100).round(2)
        
        return df

    # Calculate trend signals
    def add_trend_signals(df, window_short=80, window_long=200):
        # Add moving averages
        df['ma_curta'] = df['fechamento'].rolling(window=window_short).mean()
        df['ma_longa'] = df['fechamento'].rolling(window=window_long).mean()
        
        # Golden Cross / Death Cross signals
        df['sinal'] = 0
        df.loc[df['ma_curta'] > df['ma_longa'], 'sinal'] = 1  # Golden Cross (bullish)
        df.loc[df['ma_curta'] < df['ma_longa'], 'sinal'] = -1  # Death Cross (bearish)
        
        # Detect signal changes
        df['mudanca_sinal'] = df['sinal'].diff().fillna(0)
        
        return df

    # Function to get price statistics by year/month/day
    def get_price_stats(df, groupby_col):
        stats = df.groupby(groupby_col).agg(
            abertura_media=('abertura', 'mean'),
            fechamento_medio=('fechamento', 'mean'),
            max_periodo=('max', 'max'),
            min_periodo=('min', 'min'),
            amplitude_media=('amplitude', 'mean'),
            volatilidade=('variacao_diaria', 'std'),
            variacao_media=('variacao_diaria', 'mean'),
            dias_positivos=('variacao_diaria', lambda x: (x > 0).sum()),
            dias_negativos=('variacao_diaria', lambda x: (x < 0).sum()),
            total_dias=('variacao_diaria', 'count')
        ).round(2)
        
        stats['win_rate'] = (stats['dias_positivos'] / stats['total_dias'] * 100).round(2)
        
        return stats

    # Definir eventos importantes que afetaram o preço do petróleo
    def get_external_events():
        return {
            "Crises e Recessões": {
                "Crise Financeira Global (2008-2009)": {
                    "start_date": "2008-09-01",
                    "end_date": "2009-06-30",
                    "description": "Queda acentuada dos preços devido à crise financeira global e recessão econômica."
                },
                "Pandemia de COVID-19 (2020-2021)": {
                    "start_date": "2020-02-15",
                    "end_date": "2021-03-31",
                    "description": "Colapso na demanda global por petróleo devido a lockdowns e restrições de viagem."
                }
            },
            "Conflitos Geopolíticos": {
                "Primavera Árabe (2010-2012)": {
                    "start_date": "2010-12-18",
                    "end_date": "2012-12-31",
                    "description": "Instabilidade política em países produtores de petróleo do Oriente Médio e Norte da África."
                },
                "Sanções ao Irã (2011-2012)": {
                    "start_date": "2011-12-01",
                    "end_date": "2012-12-31",
                    "description": "Sanções ocidentais contra o setor petroleiro iraniano elevaram preços devido a preocupações com oferta."
                },
                "Sanções ao Irã (2018)": {
                    "start_date": "2018-05-08",
                    "end_date": "2018-11-05",
                    "description": "Reimposição de sanções ao Irã após os EUA saírem do acordo nuclear."
                },
                "Invasão da Ucrânia pela Rússia (2022-2025)": {
                    "start_date": "2022-02-24",
                    "end_date": "2025-01-01",
                    "description": "Sanções contra a Rússia, um dos maiores produtores de petróleo, causaram turbulência no mercado global."
                }
            },
            "Decisões da OPEP+": {
                "Acordos da OPEP para corte na produção (2016-2018)": {
                    "start_date": "2016-11-30",
                    "end_date": "2018-12-31",
                    "description": "OPEP e não-OPEP (incluindo Rússia) acordaram em reduzir produção para estabilizar preços."
                },
                "OPEP e OPEP+ reduzem produção (2023-2024)": {
                    "start_date": "2023-04-02",
                    "end_date": "2024-12-31",
                    "description": "Cortes voluntários na produção anunciados por Arábia Saudita e outros membros da OPEP+ para sustentar preços."
                }
            }
        }

    # Analisar impacto do evento nos preços do petróleo
    def analyze_event_impact(df, event_start, event_end, window_before=30):
        # Verificar se a data de início está no índice
        if event_start not in df.index:
            # Encontrar a data mais próxima usando a diferença absoluta
            closest_date = min(df.index, key=lambda x: abs(x - pd.Timestamp(event_start)))
            print(f"Usando data mais próxima para o início do evento: {closest_date}")
            event_start = closest_date
        
        # Verificar se o intervalo antes do evento está no índice
        pre_event_start = pd.Timestamp(event_start) - pd.Timedelta(days=window_before)
        if pre_event_start not in df.index:
            # Encontrar a data mais próxima para o intervalo antes do evento
            pre_event_start = min(df.index, key=lambda x: abs(x - pre_event_start))
            print(f"Usando data mais próxima para o início do período antes do evento: {pre_event_start}")
        
        # Definir períodos para análise
        pre_event_data = df.loc[(df.index >= pre_event_start) & (df.index < event_start)]
        during_event_data = df.loc[(df.index >= event_start) & (df.index <= event_end)]
        
        # Verificar se há dados disponíveis para os períodos
        if pre_event_data.empty or during_event_data.empty:
            return None, None
        
        # Calcular estatísticas
        pre_avg_price = pre_event_data['fechamento'].mean()
        event_avg_price = during_event_data['fechamento'].mean()
        price_change_pct = ((event_avg_price / pre_avg_price) - 1) * 100
        
        pre_volatility = pre_event_data['variacao_diaria'].std()
        event_volatility = during_event_data['variacao_diaria'].std()
        volatility_change_pct = ((event_volatility / pre_volatility) - 1) * 100
        
        # Resultados
        price_impact = {
            "pre_avg_price": pre_avg_price,
            "event_avg_price": event_avg_price,
            "price_change_pct": price_change_pct,
            "price_change_direction": "aumentou" if price_change_pct > 0 else "diminuiu"
        }
        
        volatility_impact = {
            "pre_volatility": pre_volatility,
            "event_volatility": event_volatility,
            "volatility_change_pct": volatility_change_pct,
            "volatility_change_direction": "aumentou" if volatility_change_pct > 0 else "diminuiu"
        }
        
        return price_impact, volatility_impact

    # Dashboard header
    # st.markdown('<div class="main-header">Brent Oil Analysis Dashboard</div>', unsafe_allow_html=True)

    # Help and About section
    with st.expander("Sobre este Dashboard"):
        st.markdown("""
        Este dashboard fornece análise detalhada dos preços do Brent Oil, um dos principais benchmark para petróleo bruto negociado globalmente.
        
        **Principais recursos:**
        - Análise de preços e tendências de mercado
        - Estatísticas de desempenho por períodos
        - Análise sazonal de comportamento de preços
        - Métricas de volatilidade e distribuição de retornos
        - Indicadores técnicos baseados em médias móveis
        
        **Dados:** Todos os dados são obtidos em tempo real através da API Yahoo Finance (ticker: BZ=F).
        """)

    # Date range selection
    col1, col2 = st.columns(2)
    with col1:
        default_start = datetime(2007, 8, 1)
        start_date = st.date_input("Data inicial", value=default_start)
    with col2:
        end_date = st.date_input("Data final", value=datetime.now())

    # Load data
    try:
        df = baixar_dados(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        df = add_trend_signals(df)

        # Show data loading status
        if df.empty:
            st.error("Não foi possível carregar os dados. Verifique sua conexão com a internet.")
        else:
            st.success(f"Dados carregados com sucesso! Período: {df.index.min().strftime('%d/%m/%Y')} até {df.index.max().strftime('%d/%m/%Y')}")

        # Key metrics with explanations
        st.markdown('<div class="sub-header">Métricas Chave</div>', unsafe_allow_html=True)
        
        with st.expander("O que significam estas métricas?"):
            st.markdown("""
            **Preço Atual:** O último preço de fechamento disponível no período selecionado, com a variação em relação ao dia anterior.
            
            **Máxima do Período:** O preço mais alto atingido durante o período selecionado, com a data em que ocorreu.
            
            **Mínima do Período:** O preço mais baixo atingido durante o período selecionado, com a data em que ocorreu.
            
            **Variação Diária Média:** A média das variações percentuais diárias absolutas, indicando a volatilidade típica do preço.
            """)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            current_price = df['fechamento'].iloc[-1]
            previous_price = df['fechamento'].iloc[-2]
            price_change = current_price - previous_price
            price_change_pct = (price_change / previous_price) * 100
            
            st.metric("Preço Atual", f"${current_price:.2f}", 
                    f"{price_change_pct:.2f}% ({'↑' if price_change_pct >= 0 else '↓'})")

        with col2:
            period_high = df['max'].max()
            period_date_high = df.loc[df['max'] == period_high].index[0].strftime('%d/%m/%Y')
            st.metric("Máxima do Período", f"${period_high:.2f}", f"em {period_date_high}")

        with col3:
            period_low = df['min'].min()
            period_date_low = df.loc[df['min'] == period_low].index[0].strftime('%d/%m/%Y')
            st.metric("Mínima do Período", f"${period_low:.2f}", f"em {period_date_low}")

        with col4:
            avg_daily_change = df['variacao_diaria_abs'].mean()
            st.metric("Variação Diária Média", f"{avg_daily_change:.2f}%")

        # Main price chart
        st.markdown('<div class="sub-header">Gráfico de Preços</div>', unsafe_allow_html=True)
        
        with st.expander("Entenda o gráfico e sinais de tendência"):
            st.markdown("""
            **Gráfico de Linha:** Mostra a evolução do preço de fechamento ao longo do tempo.
            
            **Gráfico Candlestick:** Cada "vela" representa um dia de negociação:
            - Corpo verde/branco: preço fechou acima da abertura (dia de alta)
            - Corpo vermelho/preto: preço fechou abaixo da abertura (dia de baixa)
            - Linhas finas (sombras): mostram os preços máximo e mínimo do dia
            
            **Médias Móveis:** 
            - Linha laranja: média móvel de 20 dias (curto prazo)
            - Linha azul: média móvel de 50 dias (médio prazo)
            
            **Sinais de Tendência:**
            - Triângulo verde (Sinal de Compra): quando a média móvel curta cruza acima da média móvel longa (Golden Cross)
            - Triângulo vermelho (Sinal de Venda): quando a média móvel curta cruza abaixo da média móvel longa (Death Cross)
            """)

        chart_type = st.radio("Tipo de Gráfico", ["Linha", "Candlestick"], horizontal=True)
        show_signals = st.checkbox("Mostrar Sinais de Tendência", value=True)

        if chart_type == "Linha":
            fig = px.line(df, x=df.index, y="fechamento", title="Preço de Fechamento do Brent")
            
            if show_signals:
                # Add moving averages
                fig.add_trace(go.Scatter(
                    x=df.index, y=df['ma_curta'], name='Média Móvel (80)', line=dict(color='orange', width=1)))
                # fig.add_trace(go.Scatter(
                #     x=df.index, y=df['ma_longa'], name='Média Móvel (200)', line=dict(color='blue', width=1)))
                
                # Add signal markers
                golden_cross = df[df['mudanca_sinal'] == 2]
                death_cross = df[df['mudanca_sinal'] == -2]
                
                if not golden_cross.empty:
                    fig.add_trace(go.Scatter(
                        x=golden_cross.index, y=golden_cross['fechamento'],
                        mode='markers', marker=dict(symbol='triangle-up', size=10, color='green'),
                        name='Sinal de Compra'))
                    
                if not death_cross.empty:
                    fig.add_trace(go.Scatter(
                        x=death_cross.index, y=death_cross['fechamento'],
                        mode='markers', marker=dict(symbol='triangle-down', size=10, color='red'),
                        name='Sinal de Venda'))
        else:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index,
                open=df['abertura'],
                high=df['max'],
                low=df['min'],
                close=df['fechamento'],
                name="Preço"
            )])
            
            if show_signals:
                # Add moving averages
                fig.add_trace(go.Scatter(
                    x=df.index, y=df['ma_curta'], name='Média Móvel (20)', line=dict(color='orange', width=1)))
                # fig.add_trace(go.Scatter(
                #     x=df.index, y=df['ma_longa'], name='Média Móvel (50)', line=dict(color='blue', width=1)))

        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Preço (USD)",
            height=500,
            xaxis_rangeslider_visible=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Analysis tabs
        tab1, tab2, tab3,tab4 = st.tabs(["Análise Estatística", "Análise Sazonal", "Análise de Volatilidade","Análise Fatores Externos"])

        with tab1:
            st.markdown('<div class="sub-header">Estatísticas por Período</div>', unsafe_allow_html=True)
            
            with st.expander("Entenda as métricas estatísticas"):
                st.markdown("""
                **Abertura Média:** Média dos preços de abertura no período.
                
                **Fechamento Médio:** Média dos preços de fechamento no período.
                
                **Máxima do Período:** Preço mais alto registrado no período.
                
                **Mínima do Período:** Preço mais baixo registrado no período.
                
                **Amplitude Média:** Média da diferença entre preço máximo e mínimo diários.
                
                **Volatilidade:** Desvio padrão das variações diárias, medida de dispersão dos retornos.
                
                **Variação Média:** Média das variações percentuais diárias.
                
                **Dias Positivos:** Número de dias com variação positiva no período.
                
                **Dias Negativos:** Número de dias com variação negativa no período.
                
                **Total de Dias:** Número total de dias de negociação no período.
                
                **Win Rate:** Percentual de dias positivos em relação ao total de dias no período.
                """)
            
            stats_period = st.radio("Agrupar por:", ["Ano", "Mês", "Dia da Semana"], horizontal=True)
            
            if stats_period == "Ano":
                stats_df = get_price_stats(df, 'ano')
            elif stats_period == "Mês":
                stats_df = get_price_stats(df, 'mês')
                # Map month numbers to names
                month_names = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
                stats_df.index = [month_names[m] for m in stats_df.index]
            else:  # Day of week
                stats_df = get_price_stats(df, 'dia_semana')
                # Ensure correct order of days
                day_order = ['segunda', 'terça', 'quarta', 'quinta', 'sexta', 'sábado', 'domingo']
                stats_df = stats_df.reindex(day_order)
            
            st.dataframe(stats_df, use_container_width=True)
            
            # Win rate chart
            st.markdown('<div class="sub-header">Taxa de Dias Positivos (%)</div>', unsafe_allow_html=True)
            
            with st.expander("O que significa o Win Rate?"):
                st.markdown("""
                **Win Rate** é a porcentagem de dias em que o preço fechou em alta (variação positiva) em relação ao total de dias analisados.
                
                **Interpretação:**
                - Win Rate > 50%: Indica tendência de alta no período analisado
                - Win Rate < 50%: Indica tendência de baixa no período analisado
                
                Esta métrica é útil para identificar períodos (anos, meses ou dias da semana) que historicamente apresentam maior probabilidade de altas.
                """)
            
            fig = px.bar(
                stats_df, 
                y='win_rate',
                color='win_rate',
                color_continuous_scale=[(0, "red"), (0.5, "yellow"), (1, "green")],
                text='win_rate'
            )
            
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(height=400, yaxis_range=[0, 100])
            
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown('<div class="sub-header">Análise de Sazonalidade</div>', unsafe_allow_html=True)
            
            with st.expander("O que é análise de sazonalidade?"):
                st.markdown("""
                **Análise de Sazonalidade** busca identificar padrões cíclicos nos preços que tendem a se repetir em determinados períodos do ano.
                
                **Tabela de Preço Médio Mensal:**
                - Mostra a média de preços para cada mês em diferentes anos
                - Permite identificar meses que tendem a ter preços mais altos ou mais baixos
                
                **Heatmap de Variação Média Mensal:**
                - As cores indicam a variação média percentual para cada mês em diferentes anos
                - Verde: variação média positiva (alta)
                - Vermelho: variação média negativa (baixa)
                - A intensidade da cor representa a magnitude da variação
                
                Estas visualizações ajudam a identificar padrões sazonais que podem se repetir anualmente.
                """)
            
            # Monthly average price heatmap
            monthly_data = df.pivot_table(
                index=df.index.year, 
                columns=df.index.month,
                values='fechamento',
                aggfunc='mean'
            ).round(2)
            
            # Rename columns to month names
            month_names = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
            monthly_data.columns = [month_names.get(col, col) for col in monthly_data.columns]
            
            st.markdown("**Preço Médio Mensal por Ano (USD)**")
            st.dataframe(monthly_data, use_container_width=True)
            
            # Monthly percentage change heatmap
            st.markdown('<div class="sub-header">Heatmap de Variação Média Mensal (%)</div>', unsafe_allow_html=True)
            
            # Compute monthly percentage changes
            monthly_pct = df.groupby([df.index.year, df.index.month])['variacao_diaria'].mean().unstack().round(2)
            monthly_pct.columns = [month_names.get(col, col) for col in monthly_pct.columns]
            
            # Create heatmap
            fig = px.imshow(
                monthly_pct,
                labels=dict(x="Mês", y="Ano", color="Variação (%)"),
                x=monthly_pct.columns,
                y=monthly_pct.index,
                color_continuous_scale="RdYlGn"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.markdown('<div class="sub-header">Análise de Volatilidade</div>', unsafe_allow_html=True)
            
            with st.expander("O que significa volatilidade?"):
                st.markdown("""
                **Volatilidade** mede a intensidade e frequência das oscilações de preço em um determinado período.
                
                **Gráfico de Volatilidade:**
                - Mostra o desvio padrão das variações diárias em uma janela móvel
                - Valores mais altos indicam períodos de maior incerteza e risco
                - Valores mais baixos indicam períodos de estabilidade
                
                **Distribuição das Variações Diárias:**
                - Histograma que mostra a frequência das variações percentuais diárias
                - A linha vermelha tracejada indica a média das variações
                - A linha verde tracejada indica a mediana das variações
                - O boxplot superior mostra: quartis, mediana, e outliers
                
                Alta volatilidade geralmente está associada a momentos de crise ou grandes mudanças no mercado. Baixa volatilidade costuma refletir períodos de estabilidade e confiança.
                """)
            
            # Calculate rolling volatility
            volatility_window = st.slider("Janela para Cálculo de Volatilidade (dias)", 5, 90, 20)
            
            # Calculate rolling volatility (standard deviation of returns)
            df['volatilidade'] = df['variacao_diaria'].rolling(window=volatility_window).std().round(2)
            
            # Plot volatility over time
            fig = px.line(
                df, 
                x=df.index, 
                y='volatilidade',
                title=f"Volatilidade do Brent (Desvio Padrão das Variações - Janela de {volatility_window} dias)"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Daily price change distribution
            st.markdown('<div class="sub-header">Distribuição das Variações Diárias</div>', unsafe_allow_html=True)
            
            fig = px.histogram(
                df, 
                x='variacao_diaria',
                nbins=50,
                color_discrete_sequence=['steelblue'],
                marginal='box'
            )
            
            fig.update_layout(
                title="Distribuição das Variações Diárias (%)",
                xaxis_title="Variação Diária (%)",
                yaxis_title="Frequência",
                height=400
            )
            
            # Add mean and median lines
            mean_val = df['variacao_diaria'].mean()
            median_val = df['variacao_diaria'].median()
            
            fig.add_vline(x=mean_val, line_dash="dash", line_color="red", annotation_text=f"Média: {mean_val:.2f}%")
            fig.add_vline(x=median_val, line_dash="dash", line_color="green", annotation_text=f"Mediana: {median_val:.2f}%")
            
            st.plotly_chart(fig, use_container_width=True)

        with tab4:
            st.markdown('<div class="sub-header">Análise Fatores Externos</div>', unsafe_allow_html=True)
            
            with st.expander("Como interpretar esta análise?"):
                st.markdown("""
                Esta seção permite analisar como eventos externos significativos afetaram os preços do petróleo Brent.
                
                **Como usar:**
                1. Selecione uma categoria de evento (Crises, Conflitos Geopolíticos, Decisões da OPEP+)
                2. Escolha um evento específico dentro dessa categoria
                3. O gráfico destacará o período do evento selecionado e mostrará as tendências de preço
                4. A análise de impacto quantifica as alterações nos preços e na volatilidade comparando o período do evento com o período anterior
                
                **Métricas de impacto:**
                - **Impacto no Preço:** Compara o preço médio durante o evento com o preço médio nos 30 dias anteriores
                - **Impacto na Volatilidade:** Compara a volatilidade (desvio padrão das variações diárias) durante o evento com a volatilidade nos 30 dias anteriores
                
                **Interpretação das cores no gráfico:**
                - A área sombreada em laranja indica a duração do evento selecionado
                - As linhas verticais indicam o início e o fim do evento
                """)
            # Obter lista de eventos
            external_events = get_external_events()
            
            # Seletores de evento
            event_category = st.selectbox("Selecione a categoria de evento:", list(external_events.keys()))
            
            if event_category:
                event_name = st.selectbox("Selecione o evento específico:", list(external_events[event_category].keys()))
                
                if event_name:
                    event_details = external_events[event_category][event_name]
                    
                    # Exibir informações do evento
                    st.markdown(f"**{event_name}**")
                    st.markdown(f"*Período: {pd.to_datetime(event_details['start_date']).strftime('%d/%m/%Y')} até {pd.to_datetime(event_details['end_date']).strftime('%d/%m/%Y')}*")
                    st.markdown(f"**Descrição:** {event_details['description']}")
                    
                    # Definir intervalo para exibição no gráfico (30 dias antes e depois do evento)
                    chart_start = pd.to_datetime(event_details['start_date']) - timedelta(days=30)
                    chart_end = pd.to_datetime(event_details['end_date']) + timedelta(days=30)
                    
                    # Filtrar dados para esse intervalo
                    chart_data = df[(df.index >= chart_start) & (df.index <= chart_end)]
                    
                    if not chart_data.empty:
                        # Criar gráfico com destaque para o período do evento
                        fig = go.Figure()
                        
                        # Adicionar preço de fechamento
                        fig.add_trace(go.Scatter(
                            x=chart_data.index,
                            y=chart_data['fechamento'],
                            mode='lines',
                            name='Preço de Fechamento',
                            line=dict(color='royalblue', width=2)
                        ))
                        
                        # Adicionar área sombreada para o período do evento
                        fig.add_vrect(
                            x0=event_details['start_date'],
                            x1=event_details['end_date'],
                            fillcolor="orange",
                            opacity=0.15,
                            layer="below",
                            line_width=0,
                            annotation_text=event_name,
                            annotation_position="top left"
                        )
                        
                        # Adicionar linhas verticais para início e fim do evento
                        fig.add_vline(x=event_details['start_date'], line_dash="dash", line_color="red")
                        fig.add_vline(x=event_details['end_date'], line_dash="dash", line_color="red")
                        
                        fig.update_layout(
                            title=f"Impacto do evento: {event_name}",
                            xaxis_title="Data",
                            yaxis_title="Preço (USD)",
                            height=500
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Analisar impacto do evento
                        price_impact, volatility_impact = analyze_event_impact(
                            df, 
                            event_details['start_date'], 
                            event_details['end_date']
                        )
                        
                        if price_impact and volatility_impact:
                            # Exibir resultados da análise
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("### Impacto no Preço")
                                impact_color = "green" if price_impact["price_change_pct"] > 0 else "red"
                                
                                st.markdown(f"""
                                - Preço médio antes do evento: **${price_impact['pre_avg_price']:.2f}**
                                - Preço médio durante o evento: **${price_impact['event_avg_price']:.2f}**
                                - Variação percentual: <span style='color:{impact_color};'>**{price_impact['price_change_pct']:.2f}%**</span>
                                
                                Durante este evento, o preço do petróleo Brent **{price_impact['price_change_direction']}** em média {abs(price_impact['price_change_pct']):.2f}% em comparação com os 30 dias anteriores.
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("### Impacto na Volatilidade")
                                vol_impact_color = "red" if volatility_impact["volatility_change_pct"] > 0 else "green"
                                
                                st.markdown(f"""
                                - Volatilidade antes do evento: **{volatility_impact['pre_volatility']:.2f}%**
                                - Volatilidade durante o evento: **{volatility_impact['event_volatility']:.2f}%**
                                - Variação percentual: <span style='color:{vol_impact_color};'>**{volatility_impact['volatility_change_pct']:.2f}%**</span>
                                
                                Durante este evento, a volatilidade do mercado **{volatility_impact['volatility_change_direction']}** em média {abs(volatility_impact['volatility_change_pct']):.2f}% em comparação com os 30 dias anteriores.
                                """, unsafe_allow_html=True)
                        else:
                            st.warning("Dados insuficientes para analisar o impacto deste evento. Verifique se o intervalo de datas selecionado cobre o período do evento e pelo menos 30 dias antes.")
                    else:
                        st.warning("Não há dados disponíveis para o período deste evento. Ajuste o intervalo de datas selecionado.")

        st.markdown('<div class="sub-header">Extra</div>', unsafe_allow_html=True)
        # Additional data view with explanations
        with st.expander("Ver Dados Brutos e Explicações das Colunas"):
            st.markdown("""
            **Explicação das colunas:**
            
            **Colunas de preço:**
            - **abertura**: Preço de abertura diário
            - **max**: Preço máximo atingido durante o dia
            - **min**: Preço mínimo atingido durante o dia
            - **fechamento**: Preço de fechamento do dia
            - **adj_close**: Preço de fechamento ajustado (considera dividendos, splits, etc.)
            - **volume**: Volume de negociação
            
            **Colunas calculadas:**
            - **variacao_diaria**: Variação percentual em relação ao dia anterior
            - **variacao_diaria_abs**: Valor absoluto da variação diária
            - **amplitude**: Diferença entre preço máximo e mínimo do dia
            - **amplitude_percentual**: Amplitude em relação ao preço de abertura (%)
            - **ma_curta**: Média móvel de 80 dias
            - **ma_longa**: Média móvel de 200 dias
            - **sinal**: Indicador de tendência (1: alta, -1: baixa)
            - **mudanca_sinal**: Mudança no indicador de tendência
            - **volatilidade**: Desvio padrão das variações na janela selecionada
            """)
            
            st.dataframe(df, use_container_width=True)

        # Add download capability
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download dados como CSV",
            data=csv,
            file_name=f'brent_oil_data_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Erro ao processar os dados: {e}")
        st.info("Detalhes técnicos: O Yahoo Finance às vezes muda o formato dos dados retornados. Este erro pode ocorrer se a estrutura dos dados mudou.")

    # Additional explanation section
    with st.expander("Interpretando Sinais Técnicos"):
        st.markdown("""
        ### Médias Móveis e Sinais de Tendência
        
        **O que são médias móveis?**
        - Média móvel é um indicador técnico que suaviza as flutuações de preço, calculando a média dos preços em um determinado período.
        - **Média Móvel de 80 dias (curta)**: Reflete tendências de curto prazo
        - **Média Móvel de 200 dias (longa)**: Reflete tendências de médio prazo
        
        **Sinais de compra e venda:**
        - **Golden Cross (Sinal de Compra)**: Ocorre quando a média móvel curta cruza acima da média móvel longa, indicando potencial início de tendência de alta.
        - **Death Cross (Sinal de Venda)**: Ocorre quando a média móvel curta cruza abaixo da média móvel longa, indicando potencial início de tendência de baixa.
        
        **Limitações:**
        - Estes sinais funcionam melhor em mercados com tendência definida
        - Podem gerar falsos sinais em mercados laterais (sem tendência clara)
        - Devem ser usados em conjunto com outras análises, não isoladamente
        
        **Observação importante:** Estas análises são informativas e não constituem recomendação de investimento.
        """)

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: grey; font-size: 12px;">
        Dados obtidos via Yahoo Finance (Ticker: BZ=F). Dashboard criado com Streamlit e Plotly.
    </div>
    """, unsafe_allow_html=True)
