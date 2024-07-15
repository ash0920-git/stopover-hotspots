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

    # 获取所有词向量
    word_vectors = {word: model_w2v.wv[word] for word in model_w2v.wv.key_to_index.keys()}
    save_word_vectors_to_file(word_vectors, 'word_vectors.csv')

    # 取出词和对应的向量
    words = list(word_vectors.keys())
    vectors = np.array(list(word_vectors.values()))

    # 使用 t-SNE 将 100 维向量降维到 2 维
    tsne = TSNE(n_components=2, random_state=42)
    vectors_2d = tsne.fit_transform(vectors)

    # 将降维后的结果保存成文件
    df = pd.DataFrame(vectors_2d, columns=['x', 'y'])
    df['word'] = words
    df.to_csv('word_vectors_2d.csv', index=False)

    # 计算余弦距离
    cosine_dist_matrix = cosine_distances(vectors)

    # 保存余弦距离到文件
    dist_df = pd.DataFrame(cosine_dist_matrix, index=words, columns=words)
    dist_df.to_csv('cosine_distances.csv')

    # 画二维散点图
    plt.figure(figsize=(10, 10))
    plt.scatter(df['x'], df['y'])

    for i in range(len(df)):
        plt.text(df['x'][i], df['y'][i], df['word'][i])

    plt.title("Word Vectors projected to 2D space using t-SNE")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

    # 画余弦距离热图
    plt.figure(figsize=(12, 10))
    sns.heatmap(dist_df, cmap='viridis')
    #sns.heatmap(dist_df, annot=True, vmax=1, square=True, cmap='viridis', fmt='.2g')
    plt.title("Cosine Distance Heatmap")
    plt.xlabel("cell-ID")
    plt.ylabel("cell-ID")
    plt.show()


if __name__ == '__main__':
    sentences, all_words = get_dataset()
    print("All words in the training corpus:", all_words)  # 打印用于训练语料中的所有单词
    save_words_to_file(all_words, 'training_words.txt')  # 保存所有单词到文件
    model_w2v = train(sentences, sg=1, seed=42)  # 设置 sg=1 使用 Skip-Gram 方法，并设置随机种子
    test()