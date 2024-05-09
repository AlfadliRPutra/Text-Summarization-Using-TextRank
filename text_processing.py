import re
import string
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import math
nltk.download('punkt')



factory = StemmerFactory()
stemmer = factory.create_stemmer()
stop_factory = StopWordRemoverFactory()

arrTdBaca = string.punctuation
arrSwindo = stop_factory.get_stop_words()

def bukannum(string):
    pattern = r"[^\d]+"
    return re.match(pattern, string) is not None

def split_text(text):
    text = text.replace("\n", "")
    pre1 = re.split(r"[.!?]\s", text)
    pre1 = [s.strip() for s in pre1 if s!= ""]
    return pre1

def preprocess(pre1):
    hasil=[]
    for i in range(0,len(pre1)):
        kalimat = pre1[i]
        pre2= []
        kalimat = stemmer.stem(kalimat)
        tokens = word_tokenize(kalimat)
        for kata in tokens:
            if (kata not in arrTdBaca) and (kata not in arrSwindo) and bukannum(kata):
                pre2.append(kata)
        hasil.append(' '.join(pre2))
    return hasil

def create_graph(sentences, preprocessed_sentences):
    graph = nx.Graph()

    for i, sentence in enumerate(sentences):
        graph.add_node(i, kalimat=sentence)

    vectorizer = CountVectorizer()
    sentence_vectors = vectorizer.fit_transform(preprocessed_sentences)

    for i, node in enumerate(graph.nodes()):
        for j, node2 in enumerate(graph.nodes()):
            if i == j:
                continue
            similarity = cosine_similarity(sentence_vectors[i], sentence_vectors[j])[0][0]
            if similarity>0:
                graph.add_edge(i,j,weight=similarity)
    return graph

toleransi = 1/10000
debug = {'textrank': False, 'textrank2': False}
def textrank(graph, d=0.85):
    nsimpul = []
    s = [random.randint(1,3) for x in range(len(graph.nodes))]
    iterasi = 0
    ilanjut = True

    print(s)
    while ilanjut:
        nsimpul = []

        for i in graph.nodes():
            wij = 0
            wjk = 0
            sigma = 0

            for j in graph.neighbors(i):
                wij = graph[j][i]['weight']
                wjk = sum(graph[i][j]['weight'] for i in graph.neighbors(j))
                sigma += (wij *s[j])/wjk

            if wjk > 0:
                txtrank = (1 - d) + d * sigma

            error = math.fabs(txtrank - s[i])
            if error > toleransi:
                s[i] = txtrank
            elif i == (len(graph.nodes) -1):
                ilanjut = False
                graph.nodes[i]['nilai'] = txtrank
            nsimpul.append([i, graph.nodes[i]])
            graph.nodes[i]['nilai'] = txtrank
        iterasi +=1
        if iterasi == 100:
            break
    return nsimpul

def descending_sort(node):
    for t in range(0, len(node)):
        temp = t
        for i in range(1+t, len(node)):
            if node[temp][1]['nilai'] < node[i][1]['nilai']:
                temp = i
        node[t], node[temp] = node[temp], node[t]
    return node

def get_top_ranked_graphs(graf_list):
    top_ranked_graphs = []
    for graf in graf_list:
        top_ranked_nodes = descending_sort(graf)[:len(graf)//2]
        top_ranked_graphs.append(top_ranked_nodes)
    return top_ranked_graphs

def get_sentences(graf):
    sentences = []
    for node in graf:
        kalimat = node[1]['kalimat']
        sentences.append(kalimat)
    return '. '.join(sentences) + ' '

# Summarize text
def summarize_text(text):
    pre1 = split_text(text)
    preprocessed_text = preprocess(pre1)
    graph = create_graph(pre1, preprocessed_text)
    result = textrank(graph)
    top_ranked_nodes = descending_sort(result)[:len(result)//2]  # Ambil setengah simpul teratas
    summary = get_sentences(top_ranked_nodes)
    return summary
