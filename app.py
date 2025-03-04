import streamlit as st

st.set_page_config(page_title="Projeto Pós-Graduação", layout="wide")

# Configuração do menu lateral
st.sidebar.title("Menu")

pagina = st.sidebar.radio("Navegação", [
    "Tech Challenge: Fase 4",
    "Análise Exploratória de Dados (AED)",
    "Modelagem",
    "Deploy do Modelo",
    "Dashboard"
])

st.sidebar.markdown(""" 
    <div style='margin-top: 50px; padding: 15px; background-color: #F8F9FB; border-radius: 10px; '>
        <div style='font-size: 18px'>
            Autora: Glynda Calazans
        </div>
        <div style='font-size: 16px;'>
            RM: 357444<br>
            Grupo: 40<br>
            Turma: 6DTAT
        </div>
    </div>
""", unsafe_allow_html=True)

# Navegação entre as páginas
if pagina == "Tech Challenge: Fase 4":
    import tech
    tech.mostrar()
elif pagina == "Análise Exploratória de Dados (AED)":
    import analise
    analise.mostrar()
elif pagina == "Modelagem":
    import modelagem
    modelagem.mostrar()
elif pagina == "Deploy do Modelo":
    import deploy_modelo  # Só importa aqui quando a página é escolhida
    deploy_modelo.mostrar()
elif pagina == "Dashboard":
    import dashboard_oficial
    dashboard_oficial.mostrar()
