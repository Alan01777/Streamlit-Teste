import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def set_page_configuration():
    # Configuração inicial da página
    st.set_page_config(
        page_title="Dashboard Personalizado",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def load_data(file_path):
    # Carrega os dados do arquivo CSV
    return pd.read_csv(file_path)

def render_sidebar(df):
    # Renderiza a barra lateral com opções do dashboard
    st.header("Dashboard de Teste")
    st.sidebar.title("Opções do Dashboard")
    lista_turmas = list(df.Turma.unique())[::-1]
    return st.sidebar.multiselect("Selecione a turma:", lista_turmas)

def render_average_score(df, lista_turmas):
    # Renderiza a média de notas de cada turma, exibindo os dados de todas as turmas se nenhuma for selecionada
    if lista_turmas:  # Verifica se alguma turma foi selecionada
        st.header("Média de Notas de Cada Turma")
        row = st.columns(4)
        ano = 6
        for turma, column in zip(lista_turmas, row):
            df_select_turma = df[df.Turma == turma]
            media_turma = df_select_turma["Nota"].median()
            with column:
                st.write(f"<strong>{turma}:</strong> {media_turma} pts ✨", unsafe_allow_html=True)
            ano += 1
    else:  # Se nenhuma turma foi selecionada, exibe os dados de todas as turmas
        st.subheader("Média de Notas de Cada Turma")
        row = st.columns(4)
        for turma, column in zip(df['Turma'].unique(), row):
            df_select_turma = df[df.Turma == turma]
            media_turma = df_select_turma["Nota"].median()
            with column:
                tile = st.container(height=120)
                tile.caption(f"{turma}")
                tile.subheader(f"{media_turma} pts")
                #st.write(f"<strong>{turma}:</strong> {media_turma} pts", unsafe_allow_html=True)

        fig = px.bar(df, x="Nome", y="Nota", title="Nota dos alunos", color="Turma")
        st.plotly_chart(fig)


def render_student_data(df_select_turma_sorted):
    # Renderiza o gráfico e os dados sobre os alunos (aprovados, recuperação, reprovados)
    num_aprovados = df_aprovados(df_select_turma_sorted)
    num_recuperacao = df_recuperacao(df_select_turma_sorted)
    num_reprovados = df_reprovados(df_select_turma_sorted)

    labels = ["Aprovados", "Recuperação", "Reprovados"]
    values = [num_aprovados[1], num_recuperacao[1], num_reprovados[1]]
    layout = go.Layout(
        autosize=False,
        width=400,
        height=400,
        title="Porcentagem de alunos aprovados")
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6)], layout=layout)
    st.plotly_chart(fig)

def render_student_table(df_select_turma_sorted):
    # Renderiza a tabela com dados detalhados dos alunos
    df_display = df_select_turma_sorted.iloc[:, 0:]  # Seleciona todas as linhas e todas as colunas a partir da primeira coluna
    
    df_alunos_aprovados = df_aprovados(df_display)
    st.write("Aprovados: ", df_alunos_aprovados[1])
    st.dataframe(df_alunos_aprovados[0].set_index(df_alunos_aprovados[0].columns[0]))  # Oculta o índice
    
    df_alunos_recuperacao = df_recuperacao(df_display)
    st.write("Recuperação: ", df_alunos_recuperacao[1])
    st.dataframe(df_alunos_recuperacao[0].set_index(df_alunos_recuperacao[0].columns[0]))  # Oculta o índice
    
    df_alunos_reprovados = df_reprovados(df_display)
    st.write("Reprovados: ", df_alunos_reprovados[1])
    st.dataframe(df_alunos_reprovados[0].set_index(df_alunos_reprovados[0].columns[0]))  # Oculta o índice




def main():
    # Função principal que orquestra o fluxo do dashboard
    set_page_configuration()
    df = load_data("data.csv")
    lista_turmas = render_sidebar(df)

    if not lista_turmas:
        render_average_score(df, lista_turmas)
    else:
        df_select_turma = df[df.Turma.isin(lista_turmas)]
        df_select_turma_sorted = df_select_turma.sort_values(by="Nota", ascending=False)

        col1, col2 = st.columns([6, 2])

        with col1:
            fig = px.bar(
                df_select_turma_sorted,
                x="Nome",
                y="Nota",
                width=800,
                height=400,
                title="Nota dos alunos",
                color="Turma"
            )
            st.plotly_chart(fig)

            render_student_data(df_select_turma_sorted)

        with col2:
            render_student_table(df_select_turma_sorted)

def df_aprovados(input):
    # Retorna os alunos aprovados e a quantidade de alunos aprovados
    df_aprovados = input[input["Nota"] >= 6]
    num_aprovados = df_aprovados.shape[0]
    return df_aprovados, num_aprovados

def df_recuperacao(input):
    # Retorna os alunos em recuperação e a quantidade de alunos em recuperação
    df_recuperacao = input[(input["Nota"] >= 4) & (input["Nota"] < 6)]
    num_recuperacao = df_recuperacao.shape[0]
    return df_recuperacao, num_recuperacao

def df_reprovados(input):
    # Retorna os alunos reprovados e a quantidade de alunos reprovados
    df_reprovados = input[input["Nota"] < 4]
    num_reprovados = df_reprovados.shape[0]
    return df_reprovados, num_reprovados

if __name__ == "__main__":
    main()
