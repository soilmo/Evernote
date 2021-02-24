import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import altair as alt

# Importar dataset
url = 'https://github.com/soilmo/Evernote/blob/main/notas_historico_new.xlsx?raw=true'

@st.cache(persist=True, max_entries = 20, ttl = 1800)
def importar_base(url):
    df = pd.read_excel(url, usecols=['dt_creation', 'titulo', 'autor', 'tag_1', 'tag_2',
       'tag_3', 'tag_4', 'tag_5', 'tag_6', 'texto', 'conclusao', 'pager'])
    return df

# Qtd de Notas por autor
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def notas_por_autor(df_autor, dt_i, dt_f):

    # Tirar as news
    filtro_1 = df_autor['tag_1']!="News"
    filtro_2 = df_autor['tag_2']!="News"
    filtro_3 = df_autor['tag_3']!="News"
    filtro_4 = df_autor['tag_4']!="News"
    filtro_5 = df_autor['tag_5']!="News"
    filtro_6 = df_autor['tag_6']!="News"
    df_autor = df_autor[(filtro_1)&(filtro_2)&(filtro_3)&(filtro_4)&(filtro_5)&(filtro_6)]

    df_autor = df_autor.groupby(['autor'], as_index=False)['tag_1'].count()
    df_autor.columns = ["Autor","Quantidade"]
    
    return df_autor

# Notas por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def notas_por_tags(df_tags, dt_i, dt_f, tags_selecionadas):
    
    for tag in tags_selecionadas:
        filtro_1 = df_tags['tag_1']==tag
        filtro_2 = df_tags['tag_2']==tag
        filtro_3 = df_tags['tag_3']==tag
        filtro_4 = df_tags['tag_4']==tag
        filtro_5 = df_tags['tag_5']==tag
        filtro_6 = df_tags['tag_6']==tag

        # Tirar as News
        filtro_7 = df_tags['tag_1']!="News"
        filtro_8 = df_tags['tag_2']!="News"
        filtro_9 = df_tags['tag_3']!="News"
        filtro_10 = df_tags['tag_4']!="News"
        filtro_11 = df_tags['tag_5']!="News"
        filtro_12 = df_tags['tag_6']!="News"

        df_tags = df_tags[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)]
        
        df_tags = df_tags[(filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)]

    return df_tags
    
# Notas por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def notas_por_tags_autor(df_tags_autor, dt_i, dt_f, tags_selecionadas, autor):
    
    # Filtrar as tags
    for tag in tags_selecionadas:
        filtro_1 = df_tags_autor['tag_1']==tag
        filtro_2 = df_tags_autor['tag_2']==tag
        filtro_3 = df_tags_autor['tag_3']==tag
        filtro_4 = df_tags_autor['tag_4']==tag
        filtro_5 = df_tags_autor['tag_5']==tag
        filtro_6 = df_tags_autor['tag_6']==tag

        # Tirar as News
        filtro_7 = df_tags_autor['tag_1']!="News"
        filtro_8 = df_tags_autor['tag_2']!="News"
        filtro_9 = df_tags_autor['tag_3']!="News"
        filtro_10 = df_tags_autor['tag_4']!="News"
        filtro_11 = df_tags_autor['tag_5']!="News"
        filtro_12 = df_tags_autor['tag_6']!="News"

        df_tags_autor = df_tags_autor[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)]
        df_tags_autor = df_tags_autor[(filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)]

    # Filtrar pelo autor
    df_tags_autor = df_tags_autor[df_tags_autor['autor']==autor]

    return df_tags_autor

# Criar lista com tags
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def lista_tags_clean(df):

    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).unique())
    tags_clean = []
    for i in tags:
        try:
            if i[0]==".":
                tags_clean.append(i)
        except:
            pass
        
    for i in tags:
        try:
            if i[0]=="@":
                tags_clean.append(i)
        except:
            pass

    for i in tags:
        try:
            if i=="News" or i=="Participants" or i == "Management":
                tags_clean.append(i)
        except:
            pass
    return tags_clean

# Lista com tags setoriais
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def lista_tags_setoriais(df):
    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).unique())
    tags_setores = []
    for i in tags:
        try:
            if i[0]==".":
                tags_setores.append(i)
        except:
            pass
    return tags_setores

# Lista com tags empresas
@st.cache(persist=True, max_entries = 20, ttl = 1800)
def lista_tags_empresas(df):
    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).unique())
    tags_empresas = []
    for i in tags:
        try:
            if i[0]=="@":
                tags_empresas.append(i)
        except:
            pass
    return tags_empresas

# Title
st.title("Análises das notas do Evernote")
st.header("Digite a senha para ter acesso às análises")
senha = st.text_input("Senha","Digite aqui")
#if st.button("Ter acesso"):
if senha=="indie2021":
    senha = senha.title()
    st.success("Acesso autorizado.")
    # Funcionalidades ------------------------
    
    # Período de análise
    st.header("Período de análise")
    dt_i = st.date_input("Qual o dia inicial do período?", datetime.datetime.now())
    dt_i = dt_i.strftime('%Y-%m-%d')
    st.write("A data inicial é",dt_i)

    dt_f = st.date_input("Qual o dia final do período?", datetime.datetime.now())
    dt_f = dt_f.strftime('%Y-%m-%d')
    st.write("A data final é",dt_f)

    if st.checkbox("Disponibilizar análises para esse período"):
        # Importar base
        df = importar_base(url)
        
        filtro_1 = df['dt_creation']>=dt_i
        filtro_2 = df['dt_creation']<=dt_f
        df = df[(filtro_1) & (filtro_2)]

        # Criar lista com autores
        autores = list(df['autor'].unique())
        autores = [x for x in autores if str(x) != 'nan']

        tags_clean = lista_tags_clean(df)
        tags_setores = lista_tags_setoriais(df)
        tags_empresas = lista_tags_empresas(df)

        # Qtd de Notas por autor -------
        st.header("Notas por autor")

        if st.checkbox("Quero ver a quantidade de notas que cada analista fez em dado período"):
            
            df_autor = notas_por_autor(df,dt_i,dt_f)
            
            st.success("Temos " + str(df_autor['Quantidade'].sum())+ " notas")
            st.write(df_autor.sort_values(by='Quantidade',ascending = False))


        # Qtd de Notas por tag ----------
        st.header("Notas por Tag")

        if st.checkbox("Quero ver a quantidade de notas com tags específicas em dado período"):
            
            # Escolher tags
            tags_selecionadas = st.multiselect("Quais tags quer?", options=tags_clean)
            
            df_tags = notas_por_tags(df, dt_i, dt_f, tags_selecionadas)
            st.success("Temos " + str(df_tags.shape[0])+ " notas com essas tags simultaneamente.")
            st.write(df_tags[['titulo','dt_creation','autor']])

        # Qtd de Notas por autor e por tag ----------

        st.header("Notas por Tag e Autor")

        if st.checkbox("Quero ver a quantidade de notas com tags específicas em dado período e de um determinado autor"):
            
            # Escolher autor
            autor = st.selectbox("Escolha um autor", options=autores)
            st.write("Você escolheu", autor)

            # Escolher Tags
            tags_selecionadas = st.multiselect("Quais tags escolhe?", options=tags_clean)
            
            df_tags_autor = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
            
            st.success("Temos " + str(df_tags_autor.shape[0])+ " notas com essas tags simultaneamente feitas por " + str(autor))
            st.write(df_tags_autor[['titulo','dt_creation']])

        # Graf Barras Ranking Tags das Empresas ---------

        st.header("Ranking das Tags de Empresas")

        if st.checkbox("Quero ver as tags de empresas mais comentadas"):
            
            # Quantidade de empresas
            m = st.slider("Selecione a quantidade de empresas a mostrar",1,20)

            df_rnk_empresa = df
            df_qtd_empresa = pd.DataFrame({
                'empresa':'',
                'qtd':''
            }, index=[0])

            for i in tags_empresas:
                qtd = 0
                qtd = df_rnk_empresa[df_rnk_empresa['tag_1']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_2']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_3']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_4']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_5']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_6']==i].shape[0]
                aux = pd.DataFrame({
                        'empresa':i,
                        'qtd':qtd
                    }, index=[0])
                df_qtd_empresa = df_qtd_empresa.append(aux)
                df_qtd_empresa = df_qtd_empresa[df_qtd_empresa['qtd']!=""]
                df_qtd_empresa = df_qtd_empresa.sort_values(by='qtd', ascending = False)

            df_qtd_empresa = df_qtd_empresa[df_qtd_empresa['qtd']>0]
            
            # Gráfico Altair
            bars = alt.Chart(df_qtd_empresa.iloc[0:m,:]).mark_bar().encode(
                alt.X('qtd'),
                alt.Y("empresa",sort=alt.EncodingSortField(field="qtd", op="count", order='ascending'))
            )
            text = bars.mark_text(
                align='left',
                baseline='middle',
                dx=3  # Nudges text to right so it doesn't appear on top of the bar
            ).encode(
                text='qtd'
            )
            f_empresas = (bars + text).properties(height=50*m+30, width = 700)
            st.write(f_empresas)
            

        # Graf Barras Ranking Tags das Setores ---------
        st.header("Ranking das Tags de Setores")

        if st.checkbox("Quero ver as tags de setores mais comentadas"):
            
            df_rnk_setor = df

            df_qtd_setores = pd.DataFrame({
                'setor':'',
                'qtd':''
            }, index=[0])

            for i in tags_setores:
                qtd = 0
                qtd = df_rnk_setor[df_rnk_setor['tag_1']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_2']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_3']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_4']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_5']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_6']==i].shape[0]
                aux = pd.DataFrame({
                        'setor':i,
                        'qtd':qtd
                    }, index=[0])
                df_qtd_setores = df_qtd_setores.append(aux)
                df_qtd_setores = df_qtd_setores[df_qtd_setores['qtd']!=""]
                df_qtd_setores = df_qtd_setores.sort_values(by='qtd', ascending = False)

            df_qtd_setores = df_qtd_setores[df_qtd_setores['qtd']>0]
            n = st.slider("Selecione a quantidade de setores a mostrar",1,df_qtd_setores.shape[0])

            # Gráfico Altair
            bars = alt.Chart(df_qtd_setores.iloc[0:n,:]).mark_bar().encode(
                alt.X('qtd'),
                alt.Y("setor",sort=alt.EncodingSortField(field="qtd", op="count", order='ascending'))
            )
            text = bars.mark_text(
                align='left',
                baseline='middle',
                dx=3  # Nudges text to right so it doesn't appear on top of the bar
            ).encode(
                text='qtd'
            )
            f_setores = (bars + text).properties(height=50*n+30, width = 700)
            st.write(f_setores)
            

        # Geração de conteúdo no tempo ---------
        st.header("Geração de notas ao longo do tempo")

        if st.checkbox("Quero ver a evolução de criação de notas"):
            
            df_evolucao = df

            # Escolher autor
            autores.append("Todos")
            autor = st.selectbox("Qual o autor?", options=autores)
            st.write("Você escolheu", autor)

            # Escolher Tags
            tags_selecionadas = st.multiselect("Escoha as tags de interesse", options=tags_clean)
            # Filtrar as tags
            for tag in tags_selecionadas:
                filtro_1 = df_evolucao['tag_1']==tag
                filtro_2 = df_evolucao['tag_2']==tag
                filtro_3 = df_evolucao['tag_3']==tag
                filtro_4 = df_evolucao['tag_4']==tag
                filtro_5 = df_evolucao['tag_5']==tag
                filtro_6 = df_evolucao['tag_6']==tag

                # Tirar as News
                filtro_7 = df_evolucao['tag_1']!="News"
                filtro_8 = df_evolucao['tag_2']!="News"
                filtro_9 = df_evolucao['tag_3']!="News"
                filtro_10 = df_evolucao['tag_4']!="News"
                filtro_11 = df_evolucao['tag_5']!="News"
                filtro_12 = df_evolucao['tag_6']!="News"

                df_evolucao = df_evolucao[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)]
                df_evolucao = df_evolucao[(filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)]

            # Filtrar pelo autor
            if autor != "Todos":
                df_evolucao = df_evolucao[df_evolucao['autor']==autor]

            # Plotar gráfico
            df_evolucao = df_evolucao.groupby(['dt_creation'], as_index=False)['titulo'].count()
            df_evolucao.columns = ['Data','Notas']
            f_evolucao = alt.Chart(df_evolucao).mark_bar().encode(
                x='Data',
                y='Notas'
            ).properties(height=500, width = 800)
            st.write(f_evolucao)
            

else:
    st.warning("Senha errada. Acesso não autorizado.")








