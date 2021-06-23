from altair.vegalite.v4.schema.core import DictInlineDataset
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import altair as alt
from PIL import Image
import joblib
import nltk
from streamlit.caching import suppress_cached_st_function_warning
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
#nltk.download('stopwords')
from wordcloud import WordCloud, STOPWORDS
import base64
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Importar dataset
url_dataset = 'https://github.com/soilmo/Evernote/blob/main/notas_historico_new.xlsx?raw=true'
@st.cache(show_spinner=False)
def importar_base(url):
    df = pd.read_excel(url, usecols=['dt_creation', 'titulo', 'autor', 'tag_1', 'tag_2',
       'tag_3', 'tag_4', 'tag_5', 'tag_6', 'tag_7', 'tag_8',
       'tag_9', 'tag_10', 'tag_11', 'tag_12', 'texto', 'conclusao', 'pager'])
    return df

# Importar hyperlinks
url_hyperlinks = 'https://github.com/soilmo/Evernote/blob/main/hyperlinks.xlsx?raw=true'
@st.cache(show_spinner=False)
def importar_hyperlinks(url):
    df = pd.read_excel(url)
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
    
    aux = pd.read_csv('https://raw.githubusercontent.com/soilmo/Evernote/main/prices_adj.csv', usecols=["Unnamed: 0",ticker + str(" BZ EQUITY")])[1:]
    aux.columns = ['data']+list(aux.columns)[1:]
    aux['data']=aux['data'].apply(lambda x:str_to_date(x))
    filtro_1 = aux['data']>=dt_i
    filtro_2 = aux['data']<=dt_f
    aux = aux[(filtro_1)&(filtro_2)]

    aux['interacao']=0

    for i in range(0,aux.shape[0]):
        
        dt = aux.iloc[i,0]
        tag = tickers[tickers['ticker']==ticker]['tag'].iloc[0]
        interacao = get_interacao(tag, dt, df)
        aux.iloc[i,2]=interacao

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

    filtro_19 = aux['pager']==0


    aux = aux[(filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)&
                (filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)&(filtro_19)]

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

    # tirar os pagers
    filtro_13 = df_autor['pager']==0

    df_autor = df_autor[(filtro_1)&(filtro_2)&(filtro_3)&(filtro_4)&(filtro_5)&(filtro_6)&
                        (filtro_7)&(filtro_8)&(filtro_9)&(filtro_10)&(filtro_11)&(filtro_12)&(filtro_13)]

    df_autor = df_autor.groupby(['autor'], as_index=False)['dt_creation'].count()
    df_autor.columns = ["Autor","Quantidade"]
    
    return df_autor

# Notas por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def notas_por_tags(df_tags, dt_i, dt_f, tags_selecionadas):

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

    # Tirar os pagers
    filtro_25 = df_tags['pager']==0

    df_tags = df_tags[(filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)&
                        (filtro_19)&(filtro_20)&(filtro_21)&(filtro_22)&(filtro_23)&(filtro_24)&(filtro_25)]
    
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

        df_tags = df_tags[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]
    
    return df_tags
    
# Notas por tags e autor
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
        
        df_tags_autor = df_tags_autor[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]
        
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

    # tirar pagers
    filtro_25 = df_tags_autor['pager']==0

    df_tags_autor = df_tags_autor[(filtro_13)&(filtro_14)&(filtro_15)&(filtro_16)&(filtro_17)&(filtro_18)&
                        (filtro_19)&(filtro_20)&(filtro_21)&(filtro_22)&(filtro_23)&(filtro_24)&(filtro_25)]
    
    # Filtrar pelo autor
    if autor != "Todos":
        df_tags_autor = df_tags_autor[df_tags_autor['autor']==autor]

    return df_tags_autor

# Noticias por tags
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def noticias_por_tags(df_tags, dt_i, dt_f, tags_selecionadas):
    # Deixar as News
    filtro_13 = df_tags['tag_1']=="News"
    filtro_14 = df_tags['tag_2']=="News"
    filtro_15 = df_tags['tag_3']=="News"
    filtro_16 = df_tags['tag_4']=="News"
    filtro_17 = df_tags['tag_5']=="News"
    filtro_18 = df_tags['tag_6']=="News"
    filtro_19 = df_tags['tag_7']=="News"
    filtro_20 = df_tags['tag_8']=="News"
    filtro_21 = df_tags['tag_9']=="News"
    filtro_22 = df_tags['tag_10']=="News"
    filtro_23 = df_tags['tag_11']=="News"
    filtro_24 = df_tags['tag_12']=="News"
    
    df_tags = df_tags[(filtro_13)|(filtro_14)|(filtro_15)|(filtro_16)|(filtro_17)|(filtro_18)|
                        (filtro_19)|(filtro_20)|(filtro_21)|(filtro_22)|(filtro_23)|(filtro_24)]

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

        df_tags = df_tags[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]
    return df_tags

# Six pagers
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def pagers(df,dt_i,dt_f, tags_selecionadas, autor):
    filtro = df['pager']==1
    df = df[filtro]

    for tag in tags_selecionadas:
        filtro_1 = df['tag_1']==tag
        filtro_2 = df['tag_2']==tag
        filtro_3 = df['tag_3']==tag
        filtro_4 = df['tag_4']==tag
        filtro_5 = df['tag_5']==tag
        filtro_6 = df['tag_6']==tag
        filtro_7 = df['tag_7']==tag
        filtro_8 = df['tag_8']==tag
        filtro_9 = df['tag_9']==tag
        filtro_10 = df['tag_10']==tag
        filtro_11 = df['tag_11']==tag
        filtro_12 = df['tag_12']==tag

        df = df[(filtro_1)|(filtro_2)|(filtro_3)|(filtro_4)|(filtro_5)|(filtro_6)|
                            (filtro_7)|(filtro_8)|(filtro_9)|(filtro_10)|(filtro_11)|(filtro_12)]

    # Filtrar pelo autor
    if autor != "Todos":
        df = df[df['autor']==autor]

    return df

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
            if i=="News" or i=="Participants" or i == "Management" or i == "ESG" or i == "PAGER":
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

# Pegar hyperlink
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def get_hyperlink(titulo, df_hyperlinks):
    filtro = df_hyperlinks['titulo']==titulo
    try:
        link = df_hyperlinks[filtro].iloc[0,1]
    except:
        link = 'NA'
    return link

# String to date
def str_to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d')

# Criar link para download
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def get_table_download_link(df, arquivo,dt_i,dt_f):
    
    csvfile = df.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = arquivo + "_" + str(dt_i) + "_" + str(dt_f) + ".csv"
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Download da base desse período</a>'

    return href

# Funções para word cloud -------------------------------------
@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False, suppress_st_warning=True)
def freq_onegrams_substantivo(text):
    
    WNL = nltk.WordNetLemmatizer()
    # Lowercase and tokenize
    text = text.lower()
    # Remove single quote early since it causes problems with the tokenizer.
    text = text.replace("'", "")
    # Remove numbers from text
    digits = '0123456789'
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    # function to test if something is a noun
    is_noun = lambda pos:(pos == 'N')
    
    tokens = nltk.word_tokenize(text, language='portuguese')
    nouns = [word for (word, pos) in teste_tagger.tag(tokens) if is_noun(pos)]

    #nouns = [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]

    text1 = nltk.Text(nouns)
    
    #set the stopwords list
    stopwords_wc = set(STOPWORDS)
    
    # If you want to remove any particular word form text which does not contribute much in meaning
    customised_words_bi = [',',';','a','o','O','as','os','e','para','por','?','!','Não','nao','Nao','não','E','.','-','/',
                        '..','...','<','>','(',')',':','&','$','%','§','pra', ' ','a','b','c','d','e','f','g','h','i','j',
                        'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ano','hoje','ontem','yoy','"','the','and','to','is','are','on','in','it','of','ir','group','ex',
                        '*','"','dia','“','”','etc','eh','fm',
                        'ja','já','R$','r$','+','-','that','per','mt','with','by','pq','cent',
                        'br','us','hj','dp','mto','=','share','volumar','mm','1x1','sp','en-export',
                        'port','n-export','iv','rgb','width','ha','dele','dela','desse','outro','da','de','do',
                       'das','dos','deles','ela','ele','eles','elas','um','uma', 'group', 'large','groups','collapse','border',
                       'grouplarge','grouppresencialremoto','px','fb','ve','nisso','ii','iii']


    new_stopwords = stopwords_wc.union(customised_words_bi)
    text_content = [word for word in text1 if word not in new_stopwords]
    
    # After the punctuation above is removed it still leaves empty entries in the list.
    text_content = [s for s in text_content if len(s) != 0]
    
    # Best to get the lemmas of each word to reduce the number of similar words
    text_content = [WNL.lemmatize(t) for t in text_content]
    
    #Using count vectoriser to view the frequency of bigrams
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    bag_of_words = vectorizer.fit_transform(text_content)
    
    #vectorizer.vocabulary_
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)

    return words_freq, new_stopwords

@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False, suppress_st_warning=True)
def freq_onegrams_adjetivo(text):
    
    WNL = nltk.WordNetLemmatizer()
    # Lowercase and tokenize
    text = text.lower()
    # Remove single quote early since it causes problems with the tokenizer.
    text = text.replace("'", "")
    # Remove numbers from text
    digits = '0123456789'
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    # function to test if something is a noun
    is_noun = lambda pos:(pos == 'ADJ')
    
    tokens = nltk.word_tokenize(text, language='portuguese')
    nouns = [word for (word, pos) in teste_tagger.tag(tokens) if is_noun(pos)]

    #nouns = [word for (word, pos) in nltk.pos_tag(tokens) if is_noun(pos)]

    text1 = nltk.Text(nouns)
    
    #set the stopwords list
    stopwords_wc = set(STOPWORDS)
    
    # If you want to remove any particular word form text which does not contribute much in meaning
    customised_words_bi = [',',';','a','o','O','as','os','e','para','por','?','!','Não','nao','Nao','não','E','.','-','/',
                        '..','...','<','>','(',')',':','&','$','%','§','pra', ' ','a','b','c','d','e','f','g','h','i','j',
                        'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ano','hoje','ontem','yoy','"','the','and','to','is','are','on','in','it','of','ir','group','ex',
                        '*','"','dia','“','”','etc','eh','fm',
                        'ja','já','R$','r$','+','-','that','per','mt','with','by','pq','cent',
                        'br','us','hj','dp','mto','=','share','volumar','mm','1x1','sp','en-export',
                        'port','n-export','iv','rgb','width','ha','dele','dela','desse','outro','da','de','do',
                       'das','dos','deles','ela','ele','eles','elas','um','uma', 'group', 'large','groups','collapse','border',
                       'grouplarge','grouppresencialremoto','px','fb','ve','nisso','ii','iii','jn','me']


    new_stopwords = stopwords_wc.union(customised_words_bi)
    text_content = [word for word in text1 if word not in new_stopwords]
    
    # After the punctuation above is removed it still leaves empty entries in the list.
    text_content = [s for s in text_content if len(s) != 0]
    
    # Best to get the lemmas of each word to reduce the number of similar words
    text_content = [WNL.lemmatize(t) for t in text_content]
    
    #Using count vectoriser to view the frequency of bigrams
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    bag_of_words = vectorizer.fit_transform(text_content)
    
    #vectorizer.vocabulary_
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)

    return words_freq, new_stopwords


@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def freq_bigrams(text):
    
    WNL = nltk.WordNetLemmatizer()
    # Lowercase and tokenize
    text = text.lower()
    # Remove single quote early since it causes problems with the tokenizer.
    text = text.replace("'", "")
    # Remove numbers from text
    digits = '0123456789'
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    # function to test if something is a noun
    is_noun = lambda pos:(pos == 'ADJ') or (pos == 'N')

    tokens = nltk.word_tokenize(text, language='portuguese')
    nouns = [word for (word, pos) in teste_tagger.tag(tokens) if is_noun(pos)]

    text1 = nltk.Text(nouns)

    #set the stopwords list
    stopwords_wc = set(STOPWORDS)

    # If you want to remove any particular word form text which does not contribute much in meaning
    customised_words_bi = [',',';','a','o','O','as','os','e','para','por','?','!','Não','nao','Nao','não','E','.','-','/',
                        '..','...','<','>','(',')',':','&','$','%','§','pra', ' ','a','b','c','d','e','f','g','h','i','j',
                        'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ano','hoje','ontem','yoy','"','the','and','to','is','are','on','in','it','of','ir','group','ex',
                        '*','"','dia','“','”','etc','eh','fm',
                        'ja','já','R$','r$','+','-','that','per','mt','with','by','pq','cent',
                        'br','us','hj','dp','mto','=','share','volumar','mm','1x1','sp','en-export',
                        'port','n-export','iv','rgb','width','ha','dele','dela','desse','outro','da','de','do',
                       'das','dos','deles','ela','ele','eles','elas','um','uma', 'group', 'large','groups','collapse','border',
                       'grouplarge','grouppresencialremoto','px','fb','ve','nisso','ii','iii','jn','me','er','fp','fm']

    new_stopwords = stopwords_wc.union(customised_words_bi)

    text_content = [word for word in text1 if word not in new_stopwords]

    # After the punctuation above is removed it still leaves empty entries in the list.
    text_content = [s for s in text_content if len(s) != 0]

    # Best to get the lemmas of each word to reduce the number of similar words
    text_content = [WNL.lemmatize(t) for t in text_content]

    nltk_tokens = nltk.word_tokenize(text)  
    bigrams_list = list(nltk.bigrams(text_content))

    
    dictionary2 = [' '.join(tup) for tup in bigrams_list]
    # Tirar exceções aqui
    
    excecoes = ['tipo reunião','participante cia','reunião participante','reunião presencial','presencial remoto','participantes externos','remoto participantes',
                'notas reunião','er collapse','externos participantes','border collapse','mercado mercado',
                'cia participantes', 'objetivo conclusão','er collapse','cia ceo','ceo cfo', 'cia cfo', 'border collapse',
                'cia jn','participantes jn','ano ano', 'lojas lojas', 'bi bi', 'me me','cfo participantes','loja loja']
    aux = []

    for i in dictionary2:
        if (i in excecoes)==False:
            aux.append(i)
    
    dictionary2 = aux
    
    #Using count vectoriser to view the frequency of bigrams
    vectorizer = CountVectorizer(ngram_range=(2, 2))
    bag_of_words = vectorizer.fit_transform(dictionary2)
    #vectorizer.vocabulary_
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq, new_stopwords

@st.cache(persist=True, max_entries = 20, ttl = 1800, show_spinner=False)
def freq_trigrams(text):
    
    WNL = nltk.WordNetLemmatizer()
    # Lowercase and tokenize
    text = text.lower()
    # Remove single quote early since it causes problems with the tokenizer.
    text = text.replace("'", "")
    # Remove numbers from text
    digits = '0123456789'
    remove_digits = str.maketrans('', '', digits)
    text = text.translate(remove_digits)

    # function to test if something is a noun
    is_noun = lambda pos:(pos == 'ADJ') or (pos == 'N')  or (pos == 'V')

    tokens = nltk.word_tokenize(text, language='portuguese')
    nouns = [word for (word, pos) in teste_tagger.tag(tokens) if is_noun(pos)]

    text1 = nltk.Text(nouns)

    #set the stopwords list
    stopwords_wc = set(STOPWORDS)

    # If you want to remove any particular word form text which does not contribute much in meaning
    customised_words_bi = [',',';','a','o','O','as','os','e','para','por','?','!','Não','nao','Nao','não','E','.','-','/',
                        '..','...','<','>','(',')',':','&','$','%','§','pra', ' ','a','b','c','d','e','f','g','h','i','j',
                        'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','ano','hoje','ontem','yoy','"','the','and','to','is','are','on','in','it','of','ir','group','ex',
                        '*','"','dia','“','”','etc','eh','fm',
                        'ja','já','R$','r$','+','-','that','per','mt','with','by','pq','cent',
                        'br','us','hj','dp','mto','=','share','volumar','mm','1x1','sp','en-export',
                        'port','n-export','iv','rgb','width','ha','dele','dela','desse','outro','da','de','do',
                       'das','dos','deles','ela','ele','eles','elas','um','uma', 'group', 'large','groups','collapse','border',
                       'grouplarge','grouppresencialremoto','px','fb','ve','nisso','ii','iii']

    new_stopwords = stopwords_wc.union(customised_words_bi)

    #text_content = [word for word in text_content if word not in new_stopwords]
    text_content = [word for word in text1 if word not in new_stopwords]

    # After the punctuation above is removed it still leaves empty entries in the list.
    text_content = [s for s in text_content if len(s) != 0]

    # Best to get the lemmas of each word to reduce the number of similar words
    text_content = [WNL.lemmatize(t) for t in text_content]

    nltk_tokens = nltk.word_tokenize(text)  
    bigrams_list = list(nltk.trigrams(text_content))
    dictionary2 = [' '.join(tup) for tup in bigrams_list]

    #Using count vectoriser to view the frequency of bigrams
    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer(ngram_range=(3, 3))
    bag_of_words = vectorizer.fit_transform(dictionary2)
    #vectorizer.vocabulary_
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq, new_stopwords


# Mudar título
st.set_page_config(page_title = "Evernote Indie", layout='wide')


# Esconder menu canto superior direito
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Title
st.title("Análises Evernote")
senha = st.text_input("Senha","Digite a senha")

if senha=="indie2021":
    #senha = senha.title("Notas até o dia")
    #st.warning()
    # Funcionalidades ------------------------
    # Período de análise
    st.header("Período de análise")

    col1, col2 = st.beta_columns(2)
    
    dt_i = col1.date_input("Qual o dia inicial?", datetime.datetime(2021, 1,1))
    dt_i = dt_i.strftime('%Y-%m-%d')
    
    dt_f = col2.date_input("Qual o dia final?", datetime.datetime.now())
    dt_f = dt_f.strftime('%Y-%m-%d')

    #if st.checkbox("Ver análises do período"):
    # Importar base
    with st.spinner('Importando base...'):
        df = importar_base(url_dataset)

        filtro_1 = df['dt_creation']>=dt_i
        filtro_2 = df['dt_creation']<=dt_f
        df = df[(filtro_1) & (filtro_2)]
        # Importar hyperlinks
        df_hyperlinks = importar_hyperlinks(url_hyperlinks)
    
    # Criar lista com autores
    autores = list(df['autor'].unique())
    autores = [x for x in autores if str(x) != 'nan']
    # Listas com tags
    tags_clean = lista_tags_clean(df)
    tags_setores = lista_tags_setoriais(df)
    tags_empresas = lista_tags_empresas(df)

    col1.write("Base importada. Análises disponíveis.")

    # Download base
    arquivo = 'base_evernote'
    url_base = get_table_download_link(df, arquivo,dt_i,dt_f)
    col2.markdown(url_base, unsafe_allow_html=True)
    
    # Qtd de Notas por autor -------
    with col1.beta_expander("Quantidade de notas por analista"):
        
        df_autor = notas_por_autor(df,dt_i,dt_f)
        
        st.write("Temos " + str(df_autor['Quantidade'].sum())+ " notas")
        st.write(df_autor.sort_values(by='Quantidade',ascending = False).set_index('Autor'))
            
    # Qtd de Notas por autor e por tag ----------
    with col2.beta_expander("Notas por tags e por autor"):
        
        # Escolher autor
        autores.append("Todos")
        autor = st.selectbox("Escolha um autor", options=autores)
        
        # Escolher Tags
        tags_selecionadas = st.multiselect("Quais tags escolhe?", options=tags_clean)
        df_tags_autor = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)

        st.write(str(df_tags_autor.shape[0])+ " notas com essas tags de " + str(autor))

        for t in df_tags_autor['titulo']:
            url_link = get_hyperlink(t, df_hyperlinks)
            link = f'[{t}]({url_link})'
            st.markdown(link, unsafe_allow_html=True)
       
    # Notícias que valem a leitura ----------
    with col1.beta_expander("Notícias que valem a leitura"):
        
        # Escolher tags
        tags_selecionadas = st.multiselect("Marque as tags de interesse. Caso queira todas, não escolha nenhuma.", options=tags_clean)
        
        df_noticias = noticias_por_tags(df, dt_i, dt_f, tags_selecionadas)
        st.write(str(df_noticias.shape[0])+ " notícias com essas tags.")

        for t in df_noticias['titulo']:
            url_link = get_hyperlink(t, df_hyperlinks)
            link = f'[{t}]({url_link})'
            st.markdown(link, unsafe_allow_html=True)
        
    # Six pagers
    with col2.beta_expander("Six pagers"):
        # Escolher autor
        autor = st.selectbox("Qual o autor?", options=autores)
        
        # Escolher tags
        tags_selecionadas = st.multiselect("Escolha as tags. Caso queira todas, não escolha nenhuma.", options=tags_clean)
        
        df_pagers = pagers(df,dt_i,dt_f, tags_selecionadas, autor)
        st.write("Temos " + str(df_pagers.shape[0])+ " pagers nesse período")
        with st.spinner('Procurando pagers...'):
            for t in df_pagers['titulo']:
                url_link = get_hyperlink(t, df_hyperlinks)
                link = f'[{t}]({url_link})'
                st.markdown(link, unsafe_allow_html=True)
            
    # Graf Barras Ranking Tags das Empresas ---------
    with st.beta_expander("Ranking das Tags de Empresas"):
        
        # Quantidade de empresas
        m = st.slider("Quantidade de empresas a mostrar",1,20)

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

        # Gráfico Altair
        bars = alt.Chart(df_qtd_empresa.iloc[0:m,:]).mark_bar().encode(
            alt.X('qtd'),
            alt.Y("empresa",sort=alt.EncodingSortField(field="qtd", op="count", order='ascending')),
            tooltip = ['empresa','qtd']
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='qtd'
        )

        f_empresas = (bars + text).properties(height=50*m+30, width = 1200)
        st.write(f_empresas)
        
    # Graf Barras Ranking Tags das Setores ---------
    with st.beta_expander("Ranking das Tags de Setores"):

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
        n = st.slider("Quantidade de setores a mostrar",1,df_qtd_setores.shape[0])

        # Gráfico Altair
        bars = alt.Chart(df_qtd_setores.iloc[0:n,:]).mark_bar().encode(
            alt.X('qtd'),
            alt.Y("setor",sort=alt.EncodingSortField(field="qtd", op="count", order='ascending')),
            tooltip = ['setor','qtd']
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='qtd'
        )
        f_setores = (bars + text).properties(height=50*n+30, width = 1200)
        st.write(f_setores)

    # Geração de notas conteúdo no tempo ---------
    with st.beta_expander("Geração de notas ao longo do tempo"):
        
        # Escolher autor
        autor = st.selectbox("Qual o autor das notas?", options=autores)
        
        # Escolher Tags
        tags_selecionadas = st.multiselect("Escoha as tags de interesse", options=tags_clean)

        df_evolucao_notas = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
        # Plotar gráfico
        df_evolucao_notas = df_evolucao_notas.groupby(['dt_creation'], as_index=False)['titulo'].count()
        df_evolucao_notas.columns = ['Data','Notas']
        f_evolucao_notas = alt.Chart(df_evolucao_notas).mark_bar().encode(
            alt.X('Data', axis=alt.Axis(
                format='%d/%m/%y',
                labelAngle=-45
            )),
            alt.Y('Notas'),
            tooltip = ['Data', 'Notas']
        ).properties(height=300, width = 1200)
        st.write(f_evolucao_notas)

    # Geração de pagers conteúdo no tempo ---------
    with st.beta_expander("Geração de pagers ao longo do tempo"):
        
        # Escolher autor
        autor = st.selectbox("Qual o autor dos pagers?", options=autores)
        
        # Escolher Tags
        tags_selecionadas = st.multiselect("Escoha as tags dos pagers", options=tags_clean)

        df_evolucao_pagers = pagers(df,dt_i,dt_f, tags_selecionadas, autor)
        # Plotar gráfico
        df_evolucao_pagers = df_evolucao_pagers.groupby(['dt_creation'], as_index=False)['titulo'].count()
        df_evolucao_pagers.columns = ['Data','Notas']
        f_evolucao_pagers = alt.Chart(df_evolucao_pagers).mark_bar().encode(
            alt.X('Data', axis=alt.Axis(
                format='%d/%m/%y',
                labelAngle=-45
            )),
            alt.Y('Notas'),
            tooltip = ['Data', 'Notas']
        ).properties(height=300, width = 1200)
        st.write(f_evolucao_pagers)

    # Mapa de palavras ---------
    with st.beta_expander("Análise textual"):

        # Escolher autor
        autor = st.selectbox("Qual o analista?", options=autores)
        
        # Escolher Tags
        tags_selecionadas = st.multiselect("Quais suas tags?", options=tags_clean)
        
        # Params da nuvem
        WC_height = 500
        WC_width = 750
        WC_max_words = 100
        
        if st.button("Montar análises"):

            folder = 'C:/Dropbox (Indie Capital)/Share Logos/Research/Análise/Evernote/'
            teste_tagger = joblib.load(folder + 'POS_tagger_brill.pkl')
    
            # Montar df do mapa e vetor de texto
            df_mapa = notas_por_tags_autor(df, dt_i, dt_f, tags_selecionadas, autor)
                
            texto = ''
            for i in df_mapa['texto']:
                texto = texto + " " + str(i)
            
            with st.spinner('Processando análises de 1 termo substantivo...'):
                # Tokens
                words_freq_1_s, new_stopwords_1_s = freq_onegrams_substantivo(texto)
                
                col1, col2 = st.beta_columns((3,2))
                # Mapa de palavras ---------
                col1.markdown("Mapa de palavras - 1 Termo - Substantivo")
                    
                # Generate word cloud
                words_dict = dict(words_freq_1_s)
                wordCloud_1_s = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width,stopwords=new_stopwords_1_s, background_color='white', colormap='seismic').generate_from_frequencies(words_dict)
                col1.image(wordCloud_1_s.to_array())

                # tabela de frequencia
                col2.markdown("Frequência de palavras - 1 Termo - Substantivo")
                df_freq_1_s = pd.DataFrame({
                    'termo':'',
                    'qtd':''
                }, index = [0])

                for i in words_freq_1_s:
                    aux = {
                        'termo':i[0],
                        'qtd':i[1]
                    }
                    df_freq_1_s = df_freq_1_s.append(aux, ignore_index = True)

                df_freq_1_s = df_freq_1_s.iloc[1:,]
                arquivo_1_s = 'freq_termos_um_s'
                url_base_1_s = get_table_download_link(df_freq_1_s, arquivo_1_s, dt_i,dt_f)
                col2.markdown(url_base_1_s, unsafe_allow_html=True)
                col2.write(df_freq_1_s.set_index(['termo']))
        
            with st.spinner('Processando análises de 1 termo adjetivo...'):
                # Tokens
                words_freq_1_a, new_stopwords_1_a = freq_onegrams_adjetivo(texto)
                
                col1, col2 = st.beta_columns((3,2))
                # Mapa de palavras ---------
                col1.markdown("Mapa de palavras - 1 Termo - Adjetivo")
                    
                # Generate word cloud
                words_dict = dict(words_freq_1_a)
                wordCloud_1_a = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width,stopwords=new_stopwords_1_a, background_color='white', colormap='seismic').generate_from_frequencies(words_dict)
                col1.image(wordCloud_1_a.to_array())

                # tabela de frequencia
                col2.markdown("Frequência de palavras - 1 Termo - Adjetivo")
                df_freq_1_a = pd.DataFrame({
                    'termo':'',
                    'qtd':''
                }, index = [0])

                for i in words_freq_1_a:
                    aux = {
                        'termo':i[0],
                        'qtd':i[1]
                    }
                    df_freq_1_a = df_freq_1_a.append(aux, ignore_index = True)

                df_freq_1_a = df_freq_1_a.iloc[1:,]
                arquivo_1_a = 'freq_termos_um_a'
                url_base_1_a = get_table_download_link(df_freq_1_a, arquivo_1_a, dt_i,dt_f)
                col2.markdown(url_base_1_a, unsafe_allow_html=True)
                col2.write(df_freq_1_a.set_index(['termo']))

            with st.spinner('Processando análises de 2 termos seguidos...'):
            
                # Tokens
                words_freq_2, new_stopwords_2 = freq_bigrams(texto)
                
                col1, col2 = st.beta_columns((3,2))
                # Mapa de palavras ---------
                col1.markdown("Mapa de palavras - 2 termos seguidos")
                    
                # Generate word cloud
                words_dict = dict(words_freq_2)
                wordCloud_2 = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width,stopwords=new_stopwords_2, background_color='white', colormap='seismic').generate_from_frequencies(words_dict)
                col1.image(wordCloud_2.to_array())

                # tabela de frequencia
                col2.markdown("Frequência de palavras - 2 termos seguidos")
                df_freq_2 = pd.DataFrame({
                    'termo':'',
                    'qtd':''
                }, index = [0])

                for i in words_freq_2:
                    aux = {
                        'termo':i[0],
                        'qtd':i[1]
                    }
                    df_freq_2 = df_freq_2.append(aux, ignore_index = True)

                df_freq_2 = df_freq_2.iloc[1:,]
                arquivo_2 = 'freq_termos_bi'
                url_base = get_table_download_link(df_freq_2, arquivo_2, dt_i,dt_f)
                col2.markdown(url_base, unsafe_allow_html=True)
                col2.write(df_freq_2.set_index(['termo']))
            
else:
    st.warning("Senha errada. Acesso não autorizado.")

