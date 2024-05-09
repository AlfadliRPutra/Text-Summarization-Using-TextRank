import streamlit as st
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import string
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Fungsi-fungsi preprocessing dan ringkasan dari skrip sebelumnya
# Pastikan untuk menambahkan fungsi-fungsi tersebut di sini
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
    kalimat = pre1[i]  # Ubah pre1[1] menjadi pre1[i]
    pre2= []
    kalimat = stemmer.stem(kalimat)
    tokens = word_tokenize(kalimat)
    for kata in tokens:
      if (kata not in arrTdBaca) and (kata not in arrSwindo) and bukannum(kata):
        pre2.append(kata)
    hasil.append(' '.join(pre2))
  return hasil




from ast import If
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

teks = "Taiyuan (ANTARA) - Menurut sebuah laporan yang dirilis oleh Tongcheng Travel baru-baru ini, lebih dari 60 persen warga China yang disurvei menuturkan keinginan dan rencana mereka untuk melakukan wisata lintas perbatasan pada 2024, dan hal itu mencerminkan potensi pemulihan industri pariwisata, yang diiringi oleh sejumlah konsumsi terkait. Laporan tersebut juga menyebutkan bahwa kebijakan pembebasan visa yang diterapkan oleh beberapa negara juga berkontribusi pada pulihnya pariwisata mancanegara. Data dari platform pariwisata China Tuniu menunjukkan bahwa jumlah perjalanan lintas perbatasan yang dilakukan warga China saat lima hari masa liburan Hari Buruh yang berakhir pada 5 Mei, melonjak 190 persen secara tahunan (year on year). Ctrip, platform lainnya, mengungkapkan bahwa destinasi pariwisata lintas perbatasan pada periode liburan ini mencakup Daerah Administratif Khusus (Special Administrative Region/SAR) Hong Kong serta Makau di China selatan dan juga negara-negara yang tidak terlalu jauh lokasinya seperti Jepang, Korea Selatan, dan negara-negara Asia Tenggara. Wisatawan asal Beijing Zhan Long baru saja berwisata ke Thailand selama lima hari."
teks1 = split_text(teks)
print(teks1)

graph = create_graph(teks1, hasil_pre)

print(graph.edges)

nx.draw_circular(graph, with_labels=True)
plt.show()

import random
import math

toleransi = 1/10000
debug = {'textrank': False, 'textrank2': False}

def textrank(graph, d=0.85):
  nsimpul = []
  s = [random.randint(1,3) for x in range(len(graph.nodes))]
  iterasi = 0
  ilanjut = True

  print(s)
  while ilanjut:
    if debug['textrank2']:
      print('iterasi', iterasi)
    nsimpul = []

    for i in graph.nodes():
      wij = 0
      wjk = 0
      sigma = 0

      for j in graph.neighbors(i):
        if debug['textrank']:
          print('simpul', i, 'dan simpul', j )
        wij = graph[j][i]['weight']
        if debug['textrank']:
          print('wij', wij)
        wjk = sum(graph[i][j]['weight'] for i in graph.neighbors(j))
        if debug['textrank']:
          print('wjk', wjk)
          print('s[', j, '] = ', s[j])
        sigma += (wij *s[j])/wjk
        if debug['textrank']:
          print('sigma', sigma)

      #sigma
      if debug['textrank']:
        print('wij', wij, 'wjk', wjk)
        print('sigma', sigma)

      if wjk > 0:
        txtrank = (1 - d) + d * sigma
        if debug['textrank']:
          print('s[i] = s[',i, ']=', s[i])
          print('txt', txtrank)
      #hitung error
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

#contoh penggunaan
graph = create_graph(teks1, hasil_pre)
result = textrank(graph)

for node in result:
  print('simpul', node[0])
  print('nilai textrank:', node[1]['nilai'])
  # print('nilai textrank:', node[1]['nilai'])
  print()




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

hasil_perankingan = get_top_ranked_graphs(hasil_listSimpul)

def get_sentences(graf):
    sentences = []
    for node in graf:
        kalimat = node[1]['kalimat']
        sentences.append(kalimat)
    return '. '.join(sentences)


# Fungsi untuk membuat ringkasan
def summarize_text(text):
    pre1 = split_text(text)
    preprocessed_text = preprocess(pre1)
    graph = create_graph(pre1, preprocessed_text)
    result = textrank(graph)
    top_ranked_nodes = descending_sort(result)[:len(result)//2]  # Ambil setengah simpul teratas
    summary = get_sentences(top_ranked_nodes)
    return summary

# Antarmuka pengguna Streamlit
def main():
    st.title("Sistem Tekstualisasi")

    # Input teks pengguna
    input_text = st.text_area("Masukkan teks untuk diringkas")

    # Tombol untuk memproses teks dan menampilkan ringkasan
    if st.button("Ringkaskan"):
        if input_text:
            summary = summarize_text(input_text)
            st.subheader("Ringkasan:")
            st.write(summary)
        else:
            st.warning("Masukkan teks terlebih dahulu")

if __name__ == "__main__":
    main()
