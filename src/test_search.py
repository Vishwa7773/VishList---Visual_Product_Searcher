from search import Search_Products
import numpy as np
import pandas as pd

embeddings=np.load(r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\embeddings\fashion_embeddings.npy')
# data=pd.read_csv(r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\data\fashion_data.csv')
# print(data.columns)
engine=Search_Products(
    index_path=r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\models\Fashion_products.index',
    data_path=r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\data\fashion_data.csv'
)

query=embeddings[110].reshape(1,-1)
results=engine.search(query,10)

for result in results:
    print(result)