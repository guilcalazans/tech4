import streamlit as st
import pandas as pd
import streamlit as st
import re

def mostrar():
    st.title("Análise Exploratória de Dados (AED)")

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
    abas = st.tabs(["Cenário Geral", "Conjunto de Dados", "Série Temporal"])

    with abas[0]:
        st.subheader("1. Análise Geral do Cenário",divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        
        **Brent Crude**

        O Brent Crude é um dos principais benchmarks globais para a precificação do petróleo, sendo utilizado como referência nos mercados da Europa, Ásia e África. Seu nome vem do campo petrolífero Brent, descoberto em 1971 pela Shell no Mar do Norte. A partir da década de 1980, com o crescimento da produção na região, o Brent passou a ser amplamente utilizado como referência de preços no mercado internacional.

        Atualmente, seus contratos futuros são negociados na ICE Futures Europe, onde servem como base para a precificação de grande parte do petróleo comercializado mundialmente. Seu preço reflete a oferta e demanda global por energia e é fortemente influenciado por fatores como instabilidade geopolítica, decisões da OPEP e estoques de petróleo nos EUA. Assim, o Brent funciona como um indicador do equilíbrio entre produção e consumo de petróleo no cenário global.

        **Período Analisado**

        A partir dos dados diários de fechamento do Brent, extraídos do Yahoo Finance, foi construída uma série temporal abrangendo o período de agosto de 2007 (primeiro registro disponível) a fevereiro de 2025. Essa série reflete a intensa volatilidade do índice e sua sensibilidade a eventos internos e externos. A evolução do Brent nos últimos 18 anos está ilustrada no Gráfico 1, que servirá como ponto de partida para nossa análise.        </div>
        """, unsafe_allow_html=True)
        
        # Carregar o SVG
        with open("imagens/1.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Exibir o SVG de forma responsiva
        st.markdown(f"""
            <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                {svg_content}
        """, unsafe_allow_html=True)
        
        # Adicionar a legenda (caption) abaixo do gráfico
        st.markdown("**Gráfico 1:** Série temporal do Brent (2007-2025) com destaque para os principais eventos que influenciaram sua trajetória.", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("A análise da série temporal do Brent revela períodos de alta e baixa volatilidade, demonstrando a influência de eventos específicos nas oscilações do índice. Ademais, observa-se uma leve tendência de queda ao longo do tempo, com acentuadas retrações em 2009, 2015, 2016 e 2020. A análise bivariada indica que essa tendência poderia ter sido mais expressiva sem a intervenção da OPEP e OPEP+, cujo papel tem sido crucial para sustentar os preços e estabilizar o mercado.", unsafe_allow_html=True)
        
        st.subheader("1.1 Eventos que causaram grande impacto no Brent",divider="gray")
        with st.expander("Saiba mais"):
            st.markdown("""
            **Crises e Recessões:**

            *   **2008 - 2009** - **Crise financeira global**: A crise financeira de 2008, catalisada pela falência do Lehman Brothers em 15 de setembro de 2008 e uma série de colapsos no mercado imobiliário dos Estados Unidos, gerou uma crise de confiança nos mercados globais. Esse evento impactou significativamente o Brent que caiu de cerca de 145 dólares (julho de 2008) para 36 dólares (dezembro de 2008) devido à recessão global e queda na demanda.
            *   **2020 - 2021** - **Pandemia de COVID-19**: A pandemia, declarada oficialmente pela OMS em 11 de março de 2020, provocou uma das maiores crises globais recentes. O colapso da demanda levou o Brent 19 dólares (abril/2020), um dos níveis mais baixos da história.

            **Conflitos Geopolíticos:**

            *   **2010 - 2012** - **Primavera Árabe**: Foi uma onda de protestos, revoltas e revoluções que começou em dezembro de 2010 na Tunísia e se espalhou por vários países do Oriente Médio e Norte da África, impulsionada por demandas por democracia, direitos civis e melhores condições econômicas. Como resultado, os preços foram elevados acima de 120 dólares.
            *   **2011-2012 e 2018** - **Sanções ao Irã**: Ocorreram principalmente devido ao seu programa nuclear, que gerou preocupações internacionais sobre a possibilidade de desenvolvimento de armas atômicas. Os Estados Unidos, a União Europeia e a ONU impuseram restrições econômicas e comerciais para pressionar o país a limitar suas atividades nucleares. Além disso, o Irã enfrentou sanções por seu apoio a grupos considerados terroristas, violações de direitos humanos e instabilidade geopolítica no Oriente Médio. Algumas dessas sanções foram parcialmente suspensas após o Acordo Nuclear de 2015 (JCPOA), mas muitas foram restabelecidas em 2018, quando os EUA se retiraram do acordo. Estas restrições ao petróleo iraniano causaram oscilações acima de 100 dólares.
            *  **2022 - 2025** - **Invasão da Ucrânia pela Rússia**: Em 24 de fevereiro de 2022, após anos de tensões desde a anexação da Crimeia em 2014. A Rússia alegou motivos de segurança, mas a comunidade internacional condenou a ação como uma violação da soberania ucraniana, impondo sanções severas. O conflito resultou em milhares de mortes, crise energética global e contínuos embates militares. A guerra impulsionou o Brent acima de 130 dólares, devido ao temor de restrições ao petróleo russo.

            **Decisões da Organização dos Países Exportadores de Petróleo (OPEP+):**

            * **2016 - 2018** - **Acordos da OPEP para corte na produção**: Em setembro e novembro, a OPEP fechou dois acordos para reduzir a produção de petróleo, buscando conter o excesso de oferta e impulsionar os preços no mercado global. Como resultado, houve um aumento gradual nos preços do petróleo, que subiram de cerca de 30 dólares por barril em 2016 para mais de 70 dólares por barril em 2018. A redução na oferta ajudou a equilibrar o mercado, embora os preços não tenham se estabilizado totalmente, com flutuações ainda visíveis.
            * **2023 - 2024** - **OPEP e OPEP+ reduzem produção**: Em novembro, a OPEP e seus aliados anunciaram um corte de quase 2,2 milhões de barris por dia para aumentar os preços do petróleo, com início em janeiro de 2024. Após o anúncio, o preço do Brent subiu 1,5%, mas essa alta não se manteve devido à demanda mais fraca, especialmente na China e EUA. Em setembro de 2024, o preço caiu para menos de 70 dólares por barril, o que não ocorria desde novembro de 2021.
            """)

    with abas[1]:
        st.subheader("2. Análise do Conjunto de Dados",divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        
        A análise exploratória dos dados do Brent é uma etapa fundamental para a compreensão da natureza da série temporal e identificação de padrões relevantes para a modelagem. Por meio da análise univariada e bivariada, é possível observar a sensibilidade do índice a eventos e fatores temporais.

        * A **análise univariada** evidenciou que eventos excepcionais, como crises, elevam a média dos fechamentos, mesmo com a moda sendo mais baixa, indicando o impacto de outliers na alta dispersão dos dados.
        * A **análise bivariada** revelou uma correlação positiva (0.74) entre o volume e o ano, indicando que o volume de negociações vem aumentando de forma consistente ao longo do tempo. Por outro lado, a correlação negativa entre fechamento e ano (-0.27) evidencia uma leve tendência de queda nos preços de fechamento do Brent.

        Essa tendência de queda, embora sutil, poderia ter sido mais acentuada sem a intervenção da OPEP e OPEP+. O papel desses organismos tem sido fundamental para manter os preços elevados, estabilizando o mercado e evitando quedas significativas.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("2.1 Fechamentos Diários: Análise Univariada",divider="gray")
        st.write("""
        A análise dos preços de fechamento do petróleo Brent nos últimos 18 anos revela características importantes sobre seu comportamento. O histograma (Gráfico 2) mostra uma distribuição bimodal, com picos em torno de 80 e 110 dólares, sugerindo dois pontos de equilíbrio relacionados a diferentes ciclos econômicos ou regimes de oferta e demanda. A média de 78.61 dólares é superior à mediana de 76.67 dólares, confirmando a assimetria positiva e a influência de preços elevados que puxam a média para cima. A moda de 77.59 dólares, próxima ao primeiro pico do histograma, indica o nível de preço mais frequente, sugerindo que o mercado tende a operar em valores moderados, com picos ocasionais mais altos. O desvio padrão elevado de 24.23 dólares evidencia a alta volatilidade do Brent, com ampla dispersão entre 20 e 145 dólares.

        Desta forma, a análise mostra que o Brent oscila em torno de seus dois valores modais, apresentando maior propensão a picos de alta do que a quedas extremas, o que é típico em mercados de commodities estratégicas como o petróleo que são fortemente influenciados por eventos extremos, como crises econômicas e euforias do mercado.
        """)
        # Criar a tabela com pandas
        data = {
            'Média': [78.61],
            'Mediana': [76.67],
            'Moda': [77.59],
            'Desvio Padrão': [24.23]
        }
        df = pd.DataFrame(data)
        # Exibir a tabela abaixo do texto
        st.write(df)

        # Carregar o SVG
        with open("imagens/2.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Exibir o SVG de forma responsiva
        st.markdown(f"""
            <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                {svg_content}
        """, unsafe_allow_html=True)
        
        # Adicionar a legenda (caption) abaixo do gráfico
        st.markdown("**Gráfico 2:** Histograma da distribuição de frequência dos fechamentos diários do Brent (2007-2025)", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.subheader("2.2 Fechamentos Diários: Análise Bivariada",divider="gray")
        st.markdown("A matriz de correlação apresentada fornece um panorama geral das relações lineares entre as diferentes variáveis do Brent. Através dela, é possível observar três pontos importantes:", unsafe_allow_html=True)
        # Carregar o SVG
        with open("imagens/3.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()
        # Exibir o SVG de forma responsiva
        st.markdown(f"""
            <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                {svg_content}
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
       
       #2.2
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">2.2.1 Fechamento e Ano </p>', unsafe_allow_html=True)
        # Criar o expander com o texto
        with st.expander("Saiba mais."):
            st.write("""
            Há uma correlação negativa fraca (-0.27) entre o preço de fechamento e o ano, indicando que, ao longo do tempo, os preços tendem a cair ligeiramente, embora sem grande significância estatística. Isso é evidenciado pelo Gráfico 3, que mostra uma leve tendência de queda nos fechamentos anuais do Brent nos últimos 18 anos. Após o pico entre 2012 e 2013, houve uma forte queda entre 2014 e 2016, seguida por uma recuperação gradual a partir de 2017. Nos anos mais recentes (2022-2025), os preços parecem ter se estabilizado em um patamar médio, sugerindo que a OPEP tem atuado para controlar a volatilidade e evitar quedas mais acentuadas.
            
            Vale mencionar,também, que em anos de queda na média anual do Brent, o último fechamento tende a subir, sugerindo uma possível recuperação do mercado. Esse padrão pode refletir expectativas futuras mais otimistas, fatores sazonais ou correções após períodos de baixa.
            """)
            # Carregar o SVG
            with open("imagens/4.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 3:** Evolução do Brent ao longo dos anos – comparação entre a média anual de fechamento e o último valor de cada ano (2007-2025)", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        #2.3
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">2.2.2 Volume e Ano </p>', unsafe_allow_html=True)
        # Criar o expander com o texto
        with st.expander("Saiba mais."):
            st.write("""
            Há uma correlação positiva (0.74) entre volume e ano, indicando que o volume de negociações aumentou ao longo do tempo, conforme demonstrado no Gráfico 4.
            """)
            # Carregar o SVG
            with open("imagens/5.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 4:** Volume de ações negociadas anualmente no Brent (2007-2025)", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        #2.4
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">2.2.3 Mês com demais variáveis </p>', unsafe_allow_html=True)
        # Criar o expander com o texto
        with st.expander("Saiba mais."):
            st.write("""
            O mês do ano tem uma correlação muito fraca com todas as outras variáveis, indicando que a sazonalidade mensal não teve um impacto significativo no preço do Brent nos últimos 18 anos. Os gráficos 5 e 6 corroboram o fato.
            """)
            # Carregar o SVG
            with open("imagens/6.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 5:** Comparação da Performance Mensal do Brent em Diferentes Décadas", unsafe_allow_html=True)
            
            # Carregar o SVG
            with open("imagens/7.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 6:** Comparação da Performance Semanal do Brent em Diferentes Décadas", unsafe_allow_html=True)
    
    with abas[2]:
        st.subheader("3. Análise da Série Temporal",divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        
        Após a análise dos dados, foi realizada a decomposição da série temporal do Brent e aplicado o teste de raiz unitária de Dickey-Fuller para verificar a estacionariedade. Esta etapa é crucial, pois a maioria dos modelos de aprendizado de máquina assume que os dados são estacionários. A não estacionariedade pode levar a modelos imprecisos e previsões errôneas. 
            
        >Caso a série não seja estacionária, transformações como a diferenciação podem ser aplicadas para torná-la estacionária.

        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Carregar o SVG
        with open("imagens/8.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Exibir o SVG de forma responsiva
        st.markdown(f"""
            <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                {svg_content}
        """, unsafe_allow_html=True)
        
        # Adicionar a legenda (caption) abaixo do gráfico
        st.markdown("**Gráfico 7:** Série temporal dos fechamentos diários do Brent dos últimos 18 anos.", unsafe_allow_html=True)
        
        st.subheader("3.1 Decomposição da Série Temporal",divider="gray")
        st.markdown("Séries temporais apresentam características como tendência, sazonalidade, resíduo e autocorrelação. A decomposição da série do Brent permite isolar esses componentes, proporcionando uma análise mais precisa e detalhada desses componentes.", unsafe_allow_html=True)
        # Carregar o SVG
        with open("imagens/9.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()
        # Exibir o SVG de forma responsiva
        st.markdown(f"""
            <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                {svg_content}
        """, unsafe_allow_html=True)

        # Adicionar a legenda (caption) abaixo do gráfico
        st.markdown("**Gráfico 8:** Decomposição da série temporal do fechamento do Brent em seus 4 componentes principais.", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        #Tendencia
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.1.1 Tendência</p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** Refere-se ao movimento de longo prazo nos dados. É a parte da série que representa o crescimento ou declínio gradual ao longo do tempo.

            **Resultado:** A série temporal do Brent não exibe uma forte tendência linear consistente, indicando que os valores de fechamento não seguem um padrão claro de crescimento ou declínio ao longo do tempo, apesar das variações diárias típicas do mercado. Nesse contexto, a **análise por médias móveis se mostra mais eficaz para identificar padrões e tendências na série temporal do Brent**.
            """)
        with st.expander("Saiba mais"):
            st.write("""
            A análise de regressão linear (Gráfico 9) mostra uma tendência muito sutil nos preços de fechamento do Brent, com um coeficiente de determinação de apenas 0,0756. Isso significa que apenas 7,56% da variação dos preços pode ser explicada pelo tempo, evidenciando a forte influência de fatores externos e a alta volatilidade do mercado de petróleo. Esse resultado indica que um modelo linear simples não é suficiente para capturar suas oscilações de forma precisa.
            """)
            # Carregar o SVG
            with open("imagens/10.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 9:** Regressão linear do fechamento diário do Brent.", unsafe_allow_html=True)
            st.markdown("""
            Para capturar melhor essas dinâmicas, foi empregada a análise de média móvel de 80 dias. Ao considerar a média móvel, obteve-se um erro percentual absoluto médio (MAPE) de apenas 9,79%, indicando um ajuste mais preciso aos dados e uma melhor capacidade de acompanhar as flutuações de curto prazo do índice.

            Vale destacar que A média móvel de 80 dias foi definida após testes exploratórios, partindo de uma janela de 200 dias, um indicador técnico amplamente utilizado no mercado financeiro.

            > A média móvel é um indicador técnico amplamente utilizado na análise de mercado para suavizar os dados de preços de um ativo e identificar tendências. Ela é calculada tomando a média dos preços de um determinado período, como por exemplo, os últimos 80 dias.
            """)
            
            # Carregar o SVG
            with open("imagens/11.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Carregar o SVG
            with open("imagens/12.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()
            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)

            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 10:** Análise de tendência de longo prazo do Brent: Comparação entre Médias Móveis de 80 e 200 Dias.", unsafe_allow_html=True)
        
        #Sazonalidade
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.1.2 Sazonalidade</p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** O componente de sazonalidade mostra padrões repetitivos em intervalos regulares.

            **Resultado:** A complexidade da sazonalidade do Brent reside na variação de seus ciclos, tanto em duração quanto em intensidade. Essa oscilação reforça a influência de fatores macroeconômicos, geopolíticos e de oferta/demanda, o que dificulta a decomposição sazonal.
            """)
        with st.expander("Saiba mais"):
            st.write("""
            A função seasonal_decompose foi utilizada para entender a sazonalidade da série. Foram analisados 4 diferentes periodos na busca por uma sazonalidade:
            * **180 dias (6 meses):** Apresenta picos regulares seguidos de quedas, sugerindo ciclos curtos de alta demanda seguidos por correções. Possivelmente ligados a estoques e sazonalidade industrial.
            * **365 dias (1 ano)**: Começa subindo no início do ano e desacelera ao longo do período. Reflete padrões anuais de consumo, como maior demanda no inverno e ajustes da OPEP.
            * **540 dias (1,5 anos):** Mostra tendências menos simétricas, com oscilações mais suaves e ciclos de alta seguidos por quedas moderadas. Pode indicar realinhamentos de oferta e demanda globais.
            * **730 dias (2 anos):** Mostra ciclos de alta seguidos por períodos prolongados de estabilização ou queda. Indica movimentos estruturais do mercado, como choques de oferta, crises econômicas e mudanças na geopolítica do petróleo.""")
            # Carregar o SVG
            with open("imagens/13.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 11:** O gráfico mostra o Componente Sazonal (CS) de uma série temporal do fechamento do Brent, usando uma decomposição sazonal multiplicativa com um período de 180,365, 540 e 730 dias.", unsafe_allow_html=True)

        #Resíduo
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.1.3 Resíduo </p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** O resíduo representa as variações não explicadas pela tendência e pela sazonalidade, ou seja, os movimentos aleatórios e imprevisíveis do mercado.

            **Resultado:** A análise dos resíduos corrobora a observação inicial de que os movimentos aleatórios do Brent estão frequentemente relacionados a  fatores macroeconômicos, geopolíticos e oferta/demanda.
            """)
        with st.expander("Saiba mais"):
            st.write("""
            A análise dos resíduos do Brent revela picos e vales ligados a períodos de alta volatilidade, geralmente impulsionados por eventos que afetam abruptamente o mercado.
            A crise financeira de 2008, por exemplo, desencadeou quedas acentuadas nos preços. Já os cortes de produção acordados pela OPEP no final de 2016 impulsionaram os preços entre 2017 e 2018. A pandemia de COVID-19 em 2020 causou uma queda brusca, enquanto a guerra na Ucrânia em 2022 exerceu pressão de alta sobre os preços.
            """)
            
            # Carregar o SVG
            with open("imagens/14.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 12:** Resíduo da série temporal do Brent (2007 - 2025)", unsafe_allow_html=True)

        st.subheader("3.2 Decomposição Autoregressiva",divider="gray")
        st.markdown("""
        Após analisar a tendência, sazonalidade e resíduos da série temporal do Brent, realizou-se o estudo de autocorrelação para embasar a modelagem de machine learning.

        **Resultado:** Ao final do estudo foi observado que a série temporal do Brent revelou um ACF alto/persistente (227 lag) e PACF com corte rápido (2), o que é característico de séries com forte componente autorregressiva, possivelmente integradas. É comum em séries de preços financeiros e sugere que, embora a história distante importe para o comportamento geral da série, para fins de previsão imediata, é necessário considerar os dois dias anteriores.

        Essa combinação exige um modelo de previsão que capture tanto a dependência de longo prazo quanto os efeitos de curto prazo. Modelos ARIMA, por sua flexibilidade, são os mais adequados para ajustar essa série, permitindo capturar essas duas dinâmicas.
        """)

        #Autocorrelação
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.2.1 Autocorrelação </p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** A autocorrelação é um fenômeno estatístico que mede a dependência entre os valores passados e presentes de uma série temporal. Uma alta autocorrelação significa que os valores anteriores influenciam significativamente os valores futuros. No cenário do Brent indica que os valores de um dia podem influenciar os dias seguintes, criando padrões. No entanto, é importante lembrar que o ACF mostra apenas padrões passados e não garante o comportamento futuro do mercado.

            **Resultado:** A série do Brent apresenta uma autocorrelação que diminui à medida que os lags aumentam, sugerindo que a influência dos valores passados na previsão dos valores futuros diminui com o tempo. """)
        with st.expander("Saiba mais"):
            st.markdown("""
            O gráfico de autocorrelação do Brent (Gráfico 13) mostra uma forte correlação positiva nos primeiros 500 dias, indicando que os preços mantêm uma "memória" de cerca de dois anos de negociação. Após esse período, a correlação diminui gradualmente e oscila próximo de zero, sugerindo que o impacto dos eventos passados enfraquece com o tempo. Entre os lags 1000-2000 (cerca de 5-6 anos), observa-se uma autocorrelação negativa, o que pode refletir ciclos de longo prazo ou reversões de tendência no mercado de petróleo. Com o tempo, a autocorrelação tende a zero, indicando que eventos muito antigos deixam de influenciar os preços atuais.

            Esse padrão sugere que modelos preditivos podem se beneficiar de dados históricos de até 500 dias.
            """)
            # Carregar o SVG
            with open("imagens/15.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 13:** Autocorrelação da Série Temporal do Brent (2007 - 2025)", unsafe_allow_html=True)

        #ACF
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.2.2 ACF </p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** O ACF, ou Função de Autocorrelação (Autocorrelation Function), é uma ferramenta usada para medir quão forte é a autocorrelação nos dados ao longo de diferentes intervalos de tempo. Permitindo, assim, a identificação de padrões repetitivos nos dados, como tendências de alta ou baixa.

            **Resultado:** A série apresenta ACF alto e de decaimento lento, indicando uma forte persistência na série temporal, onde valores passados continuam influenciando os valores atuais por longos períodos (até 227 lags). Isso sugere memória longa e possível não-estacionariedade na série.
            Por fim, através desta análise fica claro que modelos de aprendizado de curto prazo podem não ser adequados. É preciso utilizar modelos que capturam a sazonalidade de longo prazo, como SARIMA. Assim como realizar a transformação da série (diferenciação) para obter um resultado melhor com o modelo de aprendizado.""")
        with st.expander("Saiba mais"): 
            st.code("""
                    #Código utilizado para plotar gráfico e obter o ACF
                    from statsmodels.graphics.tsaplots import plot_acf as _plot_acf

                    def plot_acf(df, lags=365, title="Autocorrelação da Série Temporal"):

                        fig, ax = plt.subplots(figsize=(18, 4))
                        # Get the ACF values and confidence intervals
                        _plot_acf(df, lags=lags, ax=ax, alpha=0.05)
                        ax.set_title(title)
                        ax.set_xlabel("Lags")
                        ax.set_ylabel("Autocorrelação")
                        fig.set_tight_layout(True)

                        acf_x = sm.tsa.acf(df, alpha=0.05, nlags=500)
                        acf, ci = acf_x[:2]
                        intercept_point = np.where(abs(acf) < (ci[:, 1] - acf))
                        if intercept_point[0].size > 0:
                            print(
                                f"Os coeficientes ACF interceptam o limiar no lag {intercept_point[0][0]}"
                            )
                        else:
                            print("Os coeficientes ACF não interceptam o limiar")

                    plot_acf(df['fechamento'])
                """, language="python")
                      
            # Carregar o SVG
            with open("imagens/16.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 14:** Autocorrelação da série temporal do Brent com lag 227 (2007 - 2025)", unsafe_allow_html=True)

            st.markdown("""
            Analisando o resultado do acf mais o gráfico de autocorrelação do Brent, nota-se que os coeficientes ACF interceptam o limiar apenas no lag 227, indicando uma memória longa na série temporal. O decaimento extremamente lento da autocorrelação sugere forte não-estacionariedade nos preços, provavelmente com presença de raiz unitária. Isso demonstra que o petróleo Brent mantém forte inércia e previsibilidade por quase um ano de negociação.
            Este comportamento exige modelos específicos como SARIMA para capturar adequadamente a dinâmica dos preços. Para o mercado, isso indica que tendências nos preços do Brent tendem a persistir por longos períodos antes de reverterem.
            """)

        #PACF
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; font-weight:bold; color:#1E3D59">3.2.3 PACF </p>', unsafe_allow_html=True)
        st.write("""
            **O que é:** O PACF, ou Função de Autocorrelação Parcial, mede a autocorrelação entre uma série temporal e suas defasagens, ignorando as influências das defasagens intermediárias. Isso ajuda a entender a relação direta entre os dados e a definir a ordem dos modelos autoregressivos (AR).

            **Resultado:** Os coeficientes PACF interceptam o limiar no lag 2, isto é, os últimos 2 dias são cruciais para prever o valor atual do Brent, e um modelo AR(2) é uma boa opção para capturar essa dinâmica.
            Mesmo que a autocorrelação (ACF) mostre uma influência duradoura, esta influência ocorre principalmente através dos dois últimos dias. Em outras palavras, o impacto dos dias mais antigos já está refletido nos dois dias mais recentes.""")
        with st.expander("Saiba mais"):
            st.code("""
                    #Código para plotar gráfico e obter o PACF
                    from statsmodels.graphics.tsaplots import plot_pacf as _plot_pacf
                    def plot_pacf(df, lags=30, title="Autocorrelação Parcial da Série Temporal"):

                        fig, ax = plt.subplots(figsize=(20, 4.5))
                        # Get the ACF values and confidence intervals
                        _plot_pacf(df, lags=lags, ax=ax, alpha=0.05)
                        ax.set_title(title)
                        ax.set_xlabel("Lags")
                        ax.set_ylabel("Autocorrelação Parcial")
                        fig.set_tight_layout(True)

                        acf_x = sm.tsa.pacf(df, alpha=0.05, nlags=30)
                        acf, ci = acf_x[:2]
                        intercept_point = np.where(abs(acf) < (ci[:, 1] - acf))
                        if intercept_point[0].size > 0:
                            print(
                                f"Os coeficientes PACF interceptam o limiar no lag {intercept_point[0][0]}"
                            )
                        else:
                            print("Os coeficientes PACF não interceptam o limiar")

                    plot_pacf(df["fechamento"])
                """, language="python")    
            # Carregar o SVG
            with open("imagens/17.svg", "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Exibir o SVG de forma responsiva
            st.markdown(f"""
                <div style="width: 100%; height: auto; min-width: 200px; min-height: 200px; display: flex; justify-content: left;">
                    {svg_content}
            """, unsafe_allow_html=True)
            # Adicionar a legenda (caption) abaixo do gráfico
            st.markdown("**Gráfico 15:** Autocorrelação Parcial da Série Temporal do Brent com lag 2 (2007 - 2025)", unsafe_allow_html=True)








