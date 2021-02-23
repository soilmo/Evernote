import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

# Importar dataset
url = 'https://github.com/soilmo/Evernote/blob/main/notas_historico_new.xlsx?raw=true'

@st.cache(persist=True)
def importar_base(url):
    df = pd.read_excel(url)
    return df

# Importar base
df = importar_base(url)

# Criar lista com tags
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

# Lista com tags setoriais
tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).unique())
tags_setores = []
for i in tags:
    try:
        if i[0]==".":
            tags_setores.append(i)
    except:
        pass


# Lista com tags empresas
tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).unique())
tags_empresas = []
for i in tags:
    try:
        if i[0]=="@":
            tags_empresas.append(i)
    except:
        pass

# Criar lista com autores
autores = list(df['autor'].unique())

# Title
st.title("Análises das notas do Evernote")
st.header("Preview da base")

# Preview da base
if st.checkbox("Mostrar 5 primeiras linhas"):
    st.write(df.head())
if st.checkbox("Mostrar 5 últimas linhas"):
    st.write(df.tail())
if st.checkbox("Mostrar base inteira"):
    st.write(df)
if st.checkbox("Dimensões da base"):
    st.write("A base contém", df.shape[0],"linhas e",df.shape[1],"colunas.")
if st.checkbox("Informações para cada nota"):
    st.write("As colunas de informações são",df.columns)

# Período de análise
st.header("Período de análise")
dt_i = st.date_input("Qual o dia inicial do período?", datetime.datetime.now())
dt_i = dt_i.strftime('%Y-%m-%d')
st.write("A data inicial é",dt_i)

dt_f = st.date_input("Qual o dia final do período?", datetime.datetime.now())
dt_f = dt_f.strftime('%Y-%m-%d')
st.write("A data final é",dt_f)


# Graf Qtd de Notas por autor -------
st.header("Notas por autor")

if st.checkbox("Quero ver a quantidade de notas que cada analista fez em dado período"):
    
    # Filtros de datas para o perído
    filtro_1 = df['dt_creation']>=dt_i
    filtro_2 = df['dt_creation']<=dt_f

    df_autor = df[(filtro_1) & (filtro_2)]

    # Tirar as news
    filtro_1 = df_autor['tag_1']!="News"
    filtro_2 = df_autor['tag_2']!="News"
    filtro_3 = df_autor['tag_3']!="News"
    filtro_4 = df_autor['tag_4']!="News"
    filtro_5 = df_autor['tag_5']!="News"
    filtro_6 = df_autor['tag_6']!="News"
    df_autor = df_autor[(filtro_1)&(filtro_2)&(filtro_3)&(filtro_4)&(filtro_5)&(filtro_6)]
    
    

    st.success("Temos " + str(df_autor.shape[0])+ " notas")
    df_autor = df_autor.groupby(['autor'], as_index=False)['tag_1'].count()
    df_autor.columns = ["Autor","Quantidade"]
    st.write(df_autor.sort_values(by='Quantidade',ascending = False))


# Graf Qtd de Notas por tag ----------
st.header("Notas por Tag")

if st.checkbox("Quero ver a quantidade de notas com tags específicas em dado período"):
    
    # Escolher tags
    tags_selecionadas = st.multiselect("Quais tags quer?", options=tags_clean)
    
    filtro_1 = df['dt_creation']>=dt_i
    filtro_2 = df['dt_creation']<=dt_f

    df_tags = df[(filtro_1) & (filtro_2)]
    
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
    
    st.success("Temos " + str(df_tags.shape[0])+ " notas com essas tags simultaneamente.")
    st.write(df_tags[['titulo','dt_creation','autor']])


# Graf Qtd de Notas por autor e por tag ----------

st.header("Notas por Tag e Autor")

if st.checkbox("Quero ver a quantidade de notas com tags específicas em dado período e de um determinado autor"):
    
    
    filtro_1 = df['dt_creation']>=dt_i
    filtro_2 = df['dt_creation']<=dt_f
    df_tags_autor = df[(filtro_1) & (filtro_2)]
    
    # Escolher Tags
    tags_selecionadas = st.multiselect("Quais tags quer?", options=tags_clean)
    # Escolher autor
    autor = st.selectbox("Escolha um autor", options=autores)
    st.write("Você escolheu", autor)

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
    
    st.success("Temos " + str(df_tags_autor.shape[0])+ " notas com essas tags simultaneamente feitas por " + str(autor))
    st.write(df_tags_autor[['titulo','dt_creation']])



# Graf Barras Ranking Tags das Empresas ---------

st.header("Ranking das Tags de Empresas")

if st.checkbox("Quero ver as tags de empresas mais comentadas"):
    
    filtro_1 = df['dt_creation']>=dt_i
    filtro_2 = df['dt_creation']<=dt_f
    df_rnk_empresa = df[(filtro_1) & (filtro_2)]

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

    m = st.slider("Selecione a quantidade de empresas a mostrar",1,df_qtd_empresa.shape[0])

    # Montar gráfico
    sns.set_color_codes("pastel")

    f_empresa, ax = plt.subplots(figsize=(df_qtd_empresa['qtd'].max(), m+2))

    sns.barplot(x="qtd", y="empresa", data=df_qtd_empresa.iloc[0:m,],color="b")

    ax.set(xlim=(0, df_qtd_empresa['qtd'].max() + 2), ylabel="Setor",
        xlabel="Quantidade de Notas")

    for p in ax.patches:
        width = p.get_width()    # get bar length
        ax.text(width + 0.3,       # set the text at 1 unit right of the bar
                p.get_y() + p.get_height() / 2, # get Y coordinate + X coordinate / 2
                '{:1.0f}'.format(width), # set variable to display, 2 decimals
                ha = 'left',   # horizontal alignment
                va = 'center')  # vertical alignment

    # Plotar gráfico no streamlit
    st.pyplot(f_empresa)


# Graf Barras Ranking Tags das Setores ---------
st.header("Ranking das Tags de Setores")

if st.checkbox("Quero ver as tags de setores mais comentadas"):
    
    filtro_1 = df['dt_creation']>=dt_i
    filtro_2 = df['dt_creation']<=dt_f
    df_rnk_setor = df[(filtro_1) & (filtro_2)]

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

    # Montar gráfico
    sns.set_color_codes("pastel")

    f_setores, ax = plt.subplots(figsize=(df_qtd_setores['qtd'].max(), n+2))

    sns.barplot(x="qtd", y="setor", data=df_qtd_setores.iloc[0:n,],color="b")

    ax.set(xlim=(0, df_qtd_setores['qtd'].max() + 2), ylabel="Setor",
        xlabel="Quantidade de Notas")

    for p in ax.patches:
        width = p.get_width()    # get bar length
        ax.text(width + 0.3,       # set the text at 1 unit right of the bar
                p.get_y() + p.get_height() / 2, # get Y coordinate + X coordinate / 2
                '{:1.0f}'.format(width), # set variable to display, 2 decimals
                ha = 'left',   # horizontal alignment
                va = 'center')  # vertical alignment

    # Plotar gráfico no streamlit
    st.pyplot(f_setores)


