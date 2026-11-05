from Visual_Product_Search.src.embedding import Embedder

embedder=Embedder()

embeddings=embedder.embedd(r'C:\Users\HP\OneDrive\Pictures\Screenshots\Screenshot 2026-09-30 202740.png')

print(embeddings.shape)