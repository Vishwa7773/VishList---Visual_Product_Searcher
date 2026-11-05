import faiss
import pandas as pd
import numpy as np

class Search_Products :
    def __init__(self,index_path,data_path):
        self.index=faiss.read_index(index_path)
        self.data=pd.read_csv(data_path)
        print("Search Engine in action!!")

    def search(self,query_embedding,k=5):
        query_embedding=query_embedding.astype('float32')
        faiss.normalize_L2(query_embedding)
        distance,index=self.index.search(query_embedding,k)

        distance = distance.astype(float).tolist()
        index=index.astype(int).tolist()
        results=[]

        for i in range(k):
            indx=index[0][i]
            similarity=distance[0][i]

            result={
                "index": int(indx),
                "similarity": similarity,
                "product":self.data.iloc[indx]['productDisplayName'],
                "articletype":self.data.iloc[indx]['articleType'],
                'usage':self.data.iloc[indx]['usage'],
                "gender":self.data.iloc[indx]['gender'],
                "color":self.data.iloc[indx]['baseColour'],
                "image":self.data.iloc[indx]['path']
            }

            results.append(result)
        
        return results
