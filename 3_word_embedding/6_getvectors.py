import sys
import gensim
import numpy as np
import codecs
import xlwings as xw
import xlrd
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
import seaborn as sns


def get_dataset():
    cf = codecs.open('xs.txt', 'r', 'utf-8-sig')
    docs = cf.readlines()
    sentences = []
    all_words = set()
    for text in docs:
        word_list = text.split(' ')
        word_list = [word.strip() for word in word_list]
        sentences.append(word_list)
        all_words.update(word_list)
    return sentences, all_words


def save_words_to_file(words, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for word in words:
            f.write(word + '\n')


def save_word_vectors_to_file(word_vectors, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for word, vector in word_vectors.items():
            vector_str = ','.join(map(str, vector))
            f.write(f"{word},{vector_str}\n")


def train(sentences, vector_size=100, epoch_num=5, sg=1, seed=42):
    model_w2v = Word2Vec(sentences, vector_size=vector_size, window=5, min_count=1, sg=sg, workers=4, seed=seed)
    model_w2v.train(sentences, total_examples=model_w2v.corpus_count, epochs=epoch_num)
    model_w2v.save('model_w2v')
    return model_w2v


def test():
    model_w2v = Word2Vec.load("model_w2v")

    # get all word vectors
    word_vectors = {word: model_w2v.wv[word] for word in model_w2v.wv.key_to_index.keys()}
    save_word_vectors_to_file(word_vectors, 'word_vectors.csv')

    
    words = list(word_vectors.keys())
    vectors = np.array(list(word_vectors.values()))

    # t-SNE 
    tsne = TSNE(n_components=2, random_state=42)
    vectors_2d = tsne.fit_transform(vectors)

    
    df = pd.DataFrame(vectors_2d, columns=['x', 'y'])
    df['word'] = words
    df.to_csv('word_vectors_2d.csv', index=False)

    # calculate cosine distance
    cosine_dist_matrix = cosine_distances(vectors)

    
    dist_df = pd.DataFrame(cosine_dist_matrix, index=words, columns=words)
    dist_df.to_csv('cosine_distances.csv')

    # plot figures
    plt.figure(figsize=(10, 10))
    plt.scatter(df['x'], df['y'])

    for i in range(len(df)):
        plt.text(df['x'][i], df['y'][i], df['word'][i])

    plt.title("Word Vectors projected to 2D space using t-SNE")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    # plot the heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(dist_df, cmap='viridis')
    #sns.heatmap(dist_df, annot=True, vmax=1, square=True, cmap='viridis', fmt='.2g')
    plt.title("Cosine Distance Heatmap")
    plt.xlabel("cell-ID")
    plt.ylabel("cell-ID")
    plt.show()


if __name__ == '__main__':
    sentences, all_words = get_dataset()
    print("All words in the training corpus:", all_words)  
    save_words_to_file(all_words, 'training_words.txt')  
    model_w2v = train(sentences, sg=1, seed=42)  # set sg=1 for Skip-Gram 
    test()
