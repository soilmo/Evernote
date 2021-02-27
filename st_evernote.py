import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import altair as alt
import spacy
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import yfinance as yf
import numpy as np 

# Importar dataset
url_dataset = 'https://github.com/soilmo/Evernote/blob/main/notas_historico_new.xlsx?raw=true'
@st.cache(show_spinner=False)
def importar_base(url):
    df = pd.read_excel(url, usecols=['dt_creation', 'titulo', 'autor', 'tag_1', 'tag_2',
       'tag_3', 'tag_4', 'tag_5', 'tag_6', 'tag_7', 'tag_8',
       'tag_9', 'tag_10', 'tag_11', 'tag_12', 'texto', 'conclusao', 'pager'])
    return df

# Importar tickers
url_tickers = 'https://raw.githubusercontent.com/soilmo/Evernote/main/tickers.csv'
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def importar_tickers(url):
    tickers = pd.read_csv(url)
    tickers = pd.read_csv('tickers.csv')
    tickers['ticker']=tickers['ticker'].apply(lambda x:x.replace(" BZ EQUITY",""))
    tickers['tag']=tickers['ticker'].apply(lambda x:("@"+str(x[0:4])))
    return tickers, list(tickers['ticker'])

# Pegar preços
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False, allow_output_mutation=True)
def get_prices(ticker, dt_i, dt_f, df, tickers):
    aux = yf.Ticker(ticker+str(".SA"))

    #get the historical prices for this ticker
    aux = aux.history(period='1d', start=dt_i, end=dt_f)
    aux = aux.reset_index()
    aux['ticker']=ticker

    aux = aux[['Date','ticker',"Close"]]
    aux['interacao']=0

    for i in range(0,aux.shape[0]):
        
        ticker = aux.iloc[i,1]
        dt = aux.iloc[i,0]
        tag = tickers[tickers['ticker']==ticker]['tag'].iloc[0]
        interacao = get_interacao(tag, dt, df)
        if interacao > 0:
            print(ticker, dt, tag, interacao)
        
        aux.iloc[i,3]=interacao

    return aux

# Contar interações
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def get_interacao(tag, dt, df_notas):
    
    interacao = 0
    aux = df_notas
    
    # Tirar as News
    filtro_7 = aux['tag_1']!="News"
    filtro_8 = aux['tag_2']!="News"
    filtro_9 = aux['tag_3']!="News"
    filtro_10 = aux['tag_4']!="News"
    filtro_11 = aux['tag_5']!="News"
    filtro_12 = aux['tag_6']!="News"
    filtro_13 = aux['tag_7']!="News"
    filtro_14 = aux['tag_8']!="News"
    filtro_15 = aux['tag_9']!="News"
    filtro_16 = aux['tag_10']!="News"
    filtro_17 = aux['tag_11']!="News"
    filtro_18 = aux['tag_12']!="News"

    aux = aux[(filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)&
                (filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)]

    filtro = aux['dt_creation']==dt
    try:
        tag_1 = aux[filtro]['tag_1'].iloc[0]
        tag_2 = aux[filtro]['tag_2'].iloc[0]
        tag_3 = aux[filtro]['tag_3'].iloc[0]
        tag_4 = aux[filtro]['tag_4'].iloc[0]
        tag_5 = aux[filtro]['tag_5'].iloc[0]
        tag_6 = aux[filtro]['tag_6'].iloc[0]
        tag_7 = aux[filtro]['tag_7'].iloc[0]
        tag_8 = aux[filtro]['tag_8'].iloc[0]
        tag_9 = aux[filtro]['tag_9'].iloc[0]
        tag_10 = aux[filtro]['tag_10'].iloc[0]
        tag_11 = aux[filtro]['tag_11'].iloc[0]
        tag_12 = aux[filtro]['tag_12'].iloc[0]

        if (tag_1 == tag):
            interacao += 1
        if (tag_2 == tag):
            interacao += 1
        if (tag_3 == tag):
            interacao += 1
        if (tag_4 == tag):
            interacao += 1
        if (tag_5 == tag):
            interacao += 1
        if (tag_6 == tag):
            interacao += 1
        if (tag_7 == tag):
            interacao += 1
        if (tag_8 == tag):
            interacao += 1
        if (tag_9 == tag):
            interacao += 1
        if (tag_10 == tag):
            interacao += 1
        if (tag_11 == tag):
            interacao += 1
        if (tag_12 == tag):
            interacao += 1
    except:
        pass
 
    return interacao

# Qtd de Notas por autor
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def notas_por_autor(df_autor, dt_i, dt_f):

    # Tirar as news
    filtro_1 = df_autor['tag_1']!="News"
    filtro_2 = df_autor['tag_2']!="News"
    filtro_3 = df_autor['tag_3']!="News"
    filtro_4 = df_autor['tag_4']!="News"
    filtro_5 = df_autor['tag_5']!="News"
    filtro_6 = df_autor['tag_6']!="News"
    filtro_7 = df_autor['tag_7']!="News"
    filtro_8 = df_autor['tag_8']!="News"
    filtro_9 = df_autor['tag_9']!="News"
    filtro_10 = df_autor['tag_10']!="News"
    filtro_11 = df_autor['tag_11']!="News"
    filtro_12 = df_autor['tag_12']!="News"

    df_autor = df_autor[(filtro_1)&(filtro_2)&(filtro_3)&(filtro_4)&(filtro_5)&(filtro_6)&
                        (filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)]

    df_autor = df_autor.groupby(['autor'], as_index=False)['tag_1'].count()
    df_autor.columns = ["Autor","Quantidade"]
    
    return df_autor

# Notas por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def notas_por_tags(df_tags, dt_i, dt_f, tags_selecionadas):
    
    for tag in tags_selecionadas:
        filtro_1 = df_tags['tag_1']==tag
        filtro_2 = df_tags['tag_2']==tag
        filtro_3 = df_tags['tag_3']==tag
        filtro_4 = df_tags['tag_4']==tag
        filtro_5 = df_tags['tag_5']==tag
        filtro_6 = df_tags['tag_6']==tag
        filtro_7 = df_tags['tag_7']==tag
        filtro_8 = df_tags['tag_8']==tag
        filtro_9 = df_tags['tag_9']==tag
        filtro_10 = df_tags['tag_10']==tag
        filtro_11 = df_tags['tag_11']==tag
        filtro_12 = df_tags['tag_12']==tag

        # Tirar as News
        filtro_13 = df_tags['tag_1']!="News"
        filtro_14 = df_tags['tag_2']!="News"
        filtro_15 = df_tags['tag_3']!="News"
        filtro_16 = df_tags['tag_4']!="News"
        filtro_17 = df_tags['tag_5']!="News"
        filtro_18 = df_tags['tag_6']!="News"
        filtro_19 = df_tags['tag_7']!="News"
        filtro_20 = df_tags['tag_8']!="News"
        filtro_21 = df_tags['tag_9']!="News"
        filtro_22 = df_tags['tag_10']!="News"
        filtro_23 = df_tags['tag_11']!="News"
        filtro_24 = df_tags['tag_12']!="News"

        df_tags = df_tags[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]
        
        df_tags = df_tags[(filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)&
                            (filtro_19)&(filtro_20)&(filtro_21)&(filtro_22)&(filtro_23)&(filtro_24)]

    return df_tags
    
# Notas por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def notas_por_tags_autor(df_tags_autor, dt_i, dt_f, tags_selecionadas, autor):
    
    # Filtrar as tags
    for tag in tags_selecionadas:
        filtro_1 = df_tags_autor['tag_1']==tag
        filtro_2 = df_tags_autor['tag_2']==tag
        filtro_3 = df_tags_autor['tag_3']==tag
        filtro_4 = df_tags_autor['tag_4']==tag
        filtro_5 = df_tags_autor['tag_5']==tag
        filtro_6 = df_tags_autor['tag_6']==tag
        filtro_7 = df_tags_autor['tag_7']==tag
        filtro_8 = df_tags_autor['tag_8']==tag
        filtro_9 = df_tags_autor['tag_9']==tag
        filtro_10 = df_tags_autor['tag_10']==tag
        filtro_11 = df_tags_autor['tag_11']==tag
        filtro_12 = df_tags_autor['tag_12']==tag
        
        # Tirar as News
        filtro_13 = df_tags_autor['tag_1']!="News"
        filtro_14 = df_tags_autor['tag_2']!="News"
        filtro_15 = df_tags_autor['tag_3']!="News"
        filtro_16 = df_tags_autor['tag_4']!="News"
        filtro_17 = df_tags_autor['tag_5']!="News"
        filtro_18 = df_tags_autor['tag_6']!="News"
        filtro_19 = df_tags_autor['tag_7']!="News"
        filtro_20 = df_tags_autor['tag_8']!="News"
        filtro_21 = df_tags_autor['tag_9']!="News"
        filtro_22 = df_tags_autor['tag_10']!="News"
        filtro_23 = df_tags_autor['tag_11']!="News"
        filtro_24 = df_tags_autor['tag_12']!="News"

        df_tags_autor = df_tags_autor[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]
        
        df_tags_autor = df_tags_autor[(filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)&
                            (filtro_19)&(filtro_20)&(filtro_21)&(filtro_22)&(filtro_23)&(filtro_24)]
    # Filtrar pelo autor
    if autor != "Todos":
        df_tags_autor = df_tags_autor[df_tags_autor['autor']==autor]

    return df_tags_autor

# Criar lista com tags
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def lista_tags_clean(df):

    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).append(df['tag_7']).append(df['tag_8']).append(df['tag_9']).append(df['tag_10']).append(df['tag_11']).append(df['tag_12']).unique())
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
            if i[0]=="#":
                tags_clean.append(i)
        except:
            pass
    for i in tags:
        try:
            if i=="News" or i=="Participants" or i == "Management" or i == "ESG":
                tags_clean.append(i)
        except:
            pass
    return tags_clean

# Lista com tags setoriais
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def lista_tags_setoriais(df):
    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).append(df['tag_7']).append(df['tag_8']).append(df['tag_9']).append(df['tag_10']).append(df['tag_11']).append(df['tag_12']).unique())
    
    tags_setores = []
    for i in tags:
        try:
            if i[0]==".":
                tags_setores.append(i)
        except:
            pass
    return tags_setores

# Lista com tags empresas
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def lista_tags_empresas(df):
    tags = list(df['tag_1'].append(df['tag_2']).append(df['tag_3']).append(df['tag_4']).append(df['tag_5']).append(df['tag_6']).append(df['tag_7']).append(df['tag_8']).append(df['tag_9']).append(df['tag_10']).append(df['tag_11']).append(df['tag_12']).unique())
    
    tags_empresas = []
    for i in tags:
        try:
            if i[0]=="@":
                tags_empresas.append(i)
        except:
            pass
    return tags_empresas

# Funções para word cloud -------------------------------------
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def stop_lemma(texto, palavras_inuteis):
    nlp = spacy.load('pt_core_news_sm-2.3.0')
    doc = nlp(texto)
    # Tirar Stop Words e Lematização
    filtered_tokens = [token.lemma_ for token in doc if not token.is_stop]
    
    return filtered_tokens

# Define a function to plot word cloud
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")

@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def minusculo(tokens):
    tokens_low = []
    for i in tokens:
        tokens_low.append(i.lower())
    return tokens_low

# Definir tokens e str_word para word cloud
@st.cache(persist=True, max_entries = 20, ttl = 1800, suppress_st_warning=True, show_spinner=False)
def token_and_str_word(df):

    # Montar tokens
    
    palavras_inuteis = [',',';','a','o','O','as','os','e','para','por','?','!','Não','nao','Nao','não','E','.','-','/',
                    '..','...','<','>','(',')',':','&','$','%','§','pra', ' ','a','b','c','d','e','f','g','h','i','j',
                    'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ano','hoje','ontem','yoy','"','mercar',
                    'ficar','ter','entrar','empresar','the','ser','and','to','is','are','on','in','the','it','of','ir','group','ex',
                    '*','"','dar','lixar','ciar','haver','dia','riscar','receitar','“','”','falar','etc','eh','fm','achar',
                    'ja','já','fazer','conseguir','R$','r$','passar','+','-','that','per','mt','with','by','pq','cent',
                    'br','us','hj','dp','ver','contar','estao','mto','=','share','volumar','mm','1x1','sp','en-export',
                    'port','n-export','iv','tesar','rgb','varejar','width','ha','dele','dela','desse','outro']
    my_bar = st.progress(0)
    t = 1
    tokens = []
    erros = 0
    aux = df
    
    for texto in aux['texto']:
        try:
            tokens = tokens + minusculo(stop_lemma(texto, palavras_inuteis))
        except:
            erros = erros + 1

        evol = t/len(aux['texto'])
        my_bar.progress(evol)
        #st.write("Evolução do processo: {0:1.1f}%".format(100*i/len(aux['texto'])))
        t+=1

    tokens_clean = ['']

    for i in tokens:
        if (i in palavras_inuteis)==False:
            tokens_clean.append(i)
    tokens = tokens_clean

    # Filtrar numeros
    tokens_clean = []
    for i in tokens:
        if i.isnumeric()==False:
            tokens_clean.append(i)
    tokens = tokens_clean
            
    str_word = ''
    for i in tokens:
        str_word = str_word + " " + i
    
    return tokens, str_word

# -----------------------------------------------------------

# Title
st.title("Análises das notas do Evernote")
st.header("Digite a senha para ter acesso às análises")
senha = st.text_input("Senha","Digite aqui")
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
        df = importar_base(url_dataset)

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

        if st.checkbox("Ver a quantidade de notas com tags específicas em dado período"):
            
            # Escolher tags
            tags_selecionadas = st.multiselect("Quais tags quer?", options=tags_clean)
            
            if st.button("Ver notas por tag"):
                df_tags = notas_por_tags(df, dt_i, dt_f, tags_selecionadas)
                st.success("Temos " + str(df_tags.shape[0])+ " notas com essas tags simultaneamente.")
                st.write(df_tags[['titulo','autor']])

        # Qtd de Notas por autor e por tag ----------

        st.header("Notas por Tag e Autor")

        if st.checkbox("Ver a quantidade de notas com tags específicas em dado período e de um determinado autor"):
            
            # Escolher autor
            autor = st.selectbox("Escolha um autor", options=autores)
            st.write("Você escolheu", autor)

            # Escolher Tags
            tags_selecionadas = st.multiselect("Quais tags escolhe?", options=tags_clean)
            if st.button("Ver notas por tags e autor"):
                df_tags_autor = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
                st.success("Temos " + str(df_tags_autor.shape[0])+ " notas com essas tags simultaneamente feitas por " + str(autor))
                st.write(df_tags_autor[['titulo']])

        # Graf Barras Ranking Tags das Empresas ---------

        st.header("Ranking das Tags de Empresas")

        if st.checkbox("Ver as tags de empresas mais comentadas"):
            
            # Quantidade de empresas
            m = st.slider("Selecione a quantidade de empresas a mostrar",1,20)

            df_rnk_empresa = df
            df_qtd_empresa = pd.DataFrame({
                'empresa':'',
                'qtd':''
            }, index=[0])

            for i in tags_empresas:
                qtd = 0
                qtd = df_rnk_empresa[df_rnk_empresa['tag_1']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_2']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_3']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_4']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_5']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_6']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_7']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_8']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_9']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_10']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_11']==i].shape[0]+df_rnk_empresa[df_rnk_empresa['tag_12']==i].shape[0]
                aux = pd.DataFrame({
                        'empresa':i,
                        'qtd':qtd
                    }, index=[0])
                df_qtd_empresa = df_qtd_empresa.append(aux)
                df_qtd_empresa = df_qtd_empresa[df_qtd_empresa['qtd']!=""]
                df_qtd_empresa = df_qtd_empresa.sort_values(by='qtd', ascending = False)

            df_qtd_empresa = df_qtd_empresa[df_qtd_empresa['qtd']>0]
            
            if st.button("Ver gráfico de ranking das tags de empresas"):

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
                qtd = df_rnk_setor[df_rnk_setor['tag_1']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_2']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_3']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_4']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_5']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_6']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_7']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_8']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_9']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_10']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_11']==i].shape[0]+df_rnk_setor[df_rnk_setor['tag_12']==i].shape[0]
                aux = pd.DataFrame({
                        'setor':i,
                        'qtd':qtd
                    }, index=[0])
                df_qtd_setores = df_qtd_setores.append(aux)
                df_qtd_setores = df_qtd_setores[df_qtd_setores['qtd']!=""]
                df_qtd_setores = df_qtd_setores.sort_values(by='qtd', ascending = False)

            df_qtd_setores = df_qtd_setores[df_qtd_setores['qtd']>0]
            n = st.slider("Selecione a quantidade de setores a mostrar",1,df_qtd_setores.shape[0])

            if st.button("Ver gráfico de ranking das tags de setores"):

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

        if st.checkbox("Ver a evolução de criação de notas"):
            
            # Escolher autor
            autores.append("Todos")
            autor = st.selectbox("Qual o autor?", options=autores)
            st.write("Você escolheu", autor)

            # Escolher Tags
            tags_selecionadas = st.multiselect("Escoha as tags de interesse", options=tags_clean)

            if st.button("Ver evolução"):

                df_evolucao = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
                # Plotar gráfico
                df_evolucao = df_evolucao.groupby(['dt_creation'], as_index=False)['titulo'].count()
                df_evolucao.columns = ['Data','Notas']
                f_evolucao = alt.Chart(df_evolucao).mark_bar().encode(
                    alt.X('Data', axis=alt.Axis(
                        format='%d/%m/%y',
                        labelAngle=-45
                    )),
                    alt.Y('Notas')
                ).properties(height=500, width = 700)
                st.write(f_evolucao)
            
        # Mapa de palavras ---------
        st.header("Análise de conteúdo")
        if st.checkbox("Criar um mapa de palavras das notas"):
            
            # Escolher autor
            autores.append("Todos")
            autor = st.selectbox("Qual o autor das notas?", options=autores)
            st.write("Você escolheu", autor)

            # Escolher Tags
            tags_selecionadas = st.multiselect("Quais suas tags?", options=tags_clean)
            
            if st.button("Gerar Mapa de Palavras"):
                df_mapa = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
                tokens, str_word = token_and_str_word(df_mapa)
                # Generate word cloud
                wordcloud = WordCloud(width = 700, height = 500, random_state=1, background_color='white', colormap='seismic', collocations=False, stopwords = STOPWORDS).generate(str_word)
                st.image(wordcloud.to_array())

        # Preços vs interação ---------
        '''st.header("Preços vs Interações")
        if st.checkbox("Ver as interações ao longo do Price Action"):
            # Ler tickers disponíveis
            tickers, lista_tickers = importar_tickers(url_tickers)
            empresa = st.selectbox("Qual empresa quer olhar?", options=lista_tickers)
            st.write("Você escolheu", empresa, ". As linhas verticais indicam os dias das interações.")

            if st.button("Gerar gráfico de Preços vs Interações"):
                df_ticker = get_prices(empresa, dt_i, dt_f, df, tickers)
                #st.write(df_ticker)
                df_ticker['base']=0
                df_ticker['marca']=np.where(df_ticker['interacao']>0,df_ticker['Close'],0)
                #st.write(df_ticker)
                base = alt.Chart(df_ticker).encode(
                alt.X('Date',
                    axis=alt.Axis(
                        format='%d/%m/%y',
                        labelAngle=-45
                    )
                ))
                rule = base.mark_rule().encode(
                    alt.Y(
                        'base',
                        title='Preço',
                        scale=alt.Scale(zero=False),
                    ),
                    alt.Y2("marca")
                ).interactive()
                line =  base.mark_line(color='blue', point = True).encode(
                    y='Close'
                ).interactive()

                st.write((rule + line).properties(height=500, width = 700).configure_axis(
                            labelFontSize=15,
                            titleFontSize=15
                        ))
'''

else:
    st.warning("Senha errada. Acesso não autorizado.")

