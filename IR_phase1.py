from __future__ import unicode_literals
from hazm import *
import pandas as pd

class IR:

    def __init__(self) -> None:
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()

    def preprocess(self, content):
        if not len(content) == 1:
            normalized_content = []
            tokenized_content = []
            for i in range(len(content)):
                normalized_content.append(self.normalizer.normalize(content[i]))

            for i in range(len(normalized_content)):
                tokenized_content.append(word_tokenize(normalized_content[i]))

            for i in range(len(tokenized_content)):
                for j in range(len(tokenized_content[i])):
                    tokenized_content[i][j] = self.stemmer.stem(tokenized_content[i][j])
                    tokenized_content[i][j] = self.lemmatizer.lemmatize(tokenized_content[i][j])
        else:
            normalizer = Normalizer()
            stemmer = Stemmer()
            lemmatizer = Lemmatizer()
            normalized_content = normalizer.normalize(content)
            tokenized_content = word_tokenize(normalized_content)
            for i in range(len(tokenized_content)):
                # tokenized_content[i] = stemmer.stem(tokenized_content[i])
                tokenized_content[i] = lemmatizer.lemmatize(tokenized_content[i])
        return tokenized_content
    
    def get_positional_index(self, content):
        preprocessed_data = self.preprocess(content)
        positional_index = {}
        for docID in range(len(preprocessed_data)):
            for i in range(len(preprocessed_data[docID])):
                if preprocessed_data[docID][i] in positional_index:
                    positional_index[preprocessed_data[docID][i]][0] = positional_index[preprocessed_data[docID][i]][0] + 1
                    if docID in positional_index[preprocessed_data[docID][i]][1]:
                        positional_index[preprocessed_data[docID][i]][1][docID].append(i)
                    else:
                        positional_index[preprocessed_data[docID][i]][1][docID] = [i]
                else:
                    positional_index[preprocessed_data[docID][i]] = []
                    positional_index[preprocessed_data[docID][i]].append(1)
                    positional_index[preprocessed_data[docID][i]].append({})
                    positional_index[preprocessed_data[docID][i]][1][docID] = [i]
        return positional_index

    def delete_stop_words(self, positional_index):
        docs = positional_index.keys()
        freq_docs = sorted(docs, key= lambda x: positional_index[x][0], reverse= True)
        for i in range(10):
            positional_index.pop(freq_docs[i], None)
    
    def search(self, query, positional_index):
        preprocessed_query = self.preprocess(query)

        if len(preprocessed_query) > 1:
            for word in preprocessed_query:
                if word not in positional_index:
                    preprocessed_query.remove(word)

            query_substrings = []
            for i in range(len(preprocessed_query)):
                for j in range(len(preprocessed_query) - i):
                    query_substrings.append(preprocessed_query[j:j+i+1])
            query_substrings.reverse()

            priority = 0
            min_len = len(query_substrings[0])
            related_content = {}
            for q in query_substrings:
                merge_list = positional_index[q[0]][1]
                for i in range(len(q) - 1):
                    tmp = {}
                    for doc in merge_list.keys():
                        if doc in positional_index[q[i+1]][1].keys():
                            tmp[doc] = list(set([x + 1 for x in positional_index[q[i]][1][doc]]) & set(positional_index[q[i+1]][1][doc]))
                    merge_list = tmp
                related_content[priority] = merge_list
                priority += 1

            return [preprocessed_query, related_content]
        else:
            for i in range(len(positional_index)):
                if preprocessed_query[0] in positional_index:
                     related_content = positional_index[preprocessed_query[0]][1].keys()
            return [preprocessed_query, related_content]