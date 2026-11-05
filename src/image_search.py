from .embedding import Embedder
from .search import Search_Products

class Image_Searcher:
    def __init__(self,index_path,data_path):
        
        self.embedder=Embedder()
        self.searcher=Search_Products(index_path,data_path)

        print("Image hunt in action!!")

    def search(self,image_path,k=5):

        embedding=self.embedder.embedd(image_path)
        result=self.searcher.search(embedding,k)

        return result
