import streamlit as st
import pandas as pd
import streamlit as st

def mostrar():
    st.title("Tech Challenge: Fase 4")

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
    abas = st.tabs(["Introdução", "Metodologia"])

    with abas[0]:
        st.subheader("Introdução", divider="gray")
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
        O projeto <b>Tech Challenge 4</b> teve como objetivo desenvolver um modelo de machine learning para prever o preço do petróleo Brent, transformando dados históricos em insights acionáveis e previsões precisas para apoiar a tomada de decisões estratégicas. O processo envolveu desde a coleta, limpeza e preparação dos dados até a construção, teste e validação do modelo preditivo. Após sua implementação, o modelo foi disponibilizado por meio de um deploy em um ambiente web (Streamlit), garantindo acessibilidade e usabilidade. Além disso, foi desenvolvido um dashboard interativo para a visualização das da série temporal do Brent e um vídeo explicativo para facilitar a compreensão dos resultados. Esse trabalho demonstrou a aplicação prática de análise de dados, visualização e machine learning na solução de problemas reais.
        
        <br> O que você encontrará neste projeto:
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Cards para os componentes do projeto
        components = [
            {"title": "Análise e Insights", "desc": "Insights sobre o mercado do petróleo Brent, demonstrando a capacidade de extrair informações relevantes dos dados."},
            {"title": "Modelo de Machine Learning", "desc": "Para previsão do preço do petróleo, com detalhamento do desenvolvimento, avaliação de desempenho e código utilizado."},
            {"title": "Dashboard Interativo", "desc": "Explora as variações do preço do petróleo Brent, contextualizando-as com eventos globais relevantes."},
            {"title": "Deploy", "desc": "Plano de implementação em produção com MVP no Streamlit, permitindo a aplicação prática das previsões geradas."},
            {"title": "Vídeo Explicativo", "desc": "Apresentação de todo o processo de desenvolvimento do projeto."}
        ]

        # CSS personalizado no estilo Apple com tamanho reduzido
        st.markdown("""
        <style>
            .apple-card {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 16px;
                margin-bottom: 15px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                transition: transform 0.2s, box-shadow 0.2s;
                height: 120px;
                display: flex;
                flex-direction: column;
            }
            
            .apple-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.12);
            }
                       
            .card-title {
                font-weight: 600;
                font-size: 16px;
                color: #1d1d1f;
                margin-bottom: 8px;
            }
            
            .card-desc {
                font-size: 13px;
                line-height: 1.4;
                color: #6e6e73;
                flex-grow: 1;
            }
        </style>
        """, unsafe_allow_html=True)

        # Exibindo os cards em duas colunas
        col_a, col_b = st.columns(2)

        for i, comp in enumerate(components):
            with col_a if i % 2 == 0 else col_b:
                st.markdown(f"""
                <div class="apple-card">
                    <div class="card-title">{comp['title']}</div>
                    <div class="card-desc">{comp['desc']}</div>
                </div>
                """, unsafe_allow_html=True)
     

    with abas[1]:
        st.subheader("Ferramentas e Metodologia", divider="gray")
        
        st.markdown("""
        <div style="background-color:#f5f5f5; padding:20px; border-radius:10px; border-left:5px solid #1E88E5;">
            <p>Para a realização deste trabalho, foram utilizadas as seguintes ferramentas:</p>
            <ul>
                 <li><b>Google Colab</b>: para análise e modelagem do modelo de Machine Learning.</li>
                 <li><b>VSCode e Streamlit</b>: para a criação de dashboard dinâmico e informativo, e deploy do modelo em produção, e desenvolvimento do MVP. </li>
                 <br>
                O processo foi estruturado em cinco etapas principais:
                    <br>
                    <li><b>Etapa 1 - Análise e Modelagem</b>: Inicialmente, foi realizada a coleta e análise exploratória dos dados, utilizando o Google Colab para preparar os dados, treinar e avaliar modelos de machine learning, culminando na seleção e salvamento do modelo mais adequado.</li>
                    <li><b>Etapa 2 - Desenvolvimento e Deploy</b>: A segunda etapa focou no desenvolvimento do modelo em um ambiente de produção, utilizando o VSCode para organizar o código, criar um ambiente virtual, carregar o modelo treinado e preparar a infraestrutura para o deploy. O projeto incluiu ainda a criação de um dashboard para a visualização das previsões e a realização de testes para garantir a qualidade e a precisão do modelo.</li>
                    <li><b>Etapa 3 - Versionamento</b>: Para garantir o controle de versão e a colaboração, o código do projeto foi versionado no GitHub, permitindo o acompanhamento das alterações e a gestão do código-fonte.</li>
                    <li><b>Etapa 4 - Publicação e Visualização</b>: O modelo foi disponibilizado em um ambiente web através do Streamlit, permitindo a visualização das previsões em um dashboard interativo.</li>
                    <li><b>Etapa 5 - Comunicação e Explicação</b>: Para disseminar o conhecimento e explicar o projeto, foi criado um vídeo explicativo detalhando o processo de desenvolvimento e os resultados obtidos.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        import re
        # Carregar o SVG
        with open("imagens/fluxo2.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()
        # Remover a frase ".com" do SVG
        svg_content_cleaned = svg_content.replace("Powered by textografo.com", "")
        # Modificar o viewBox para cortar a esquerda (aumente X para cortar mais)
        svg_cleaned = re.sub(r'viewBox="([^"]+)"', lambda m: f'viewBox="{int(m.group(1).split()[0]) + 30} {m.group(1).split()[1]} {m.group(1).split()[2]} {m.group(1).split()[3]}"', svg_content_cleaned)
        # Exibir no Streamlit
        st.markdown(f'<div style="text-align: left;">{svg_cleaned}</div>', unsafe_allow_html=True)
        # Adicionar a legenda (caption) abaixo do gráfico
        st.markdown("**Imagem 1:** Fluxograma do Projeto.", unsafe_allow_html=True)









 