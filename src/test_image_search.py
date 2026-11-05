from image_search import Image_Searcher

searcher=Image_Searcher(index_path=r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\models\Fashion_products.index',
                        data_path=r'C:\Users\HP\OneDrive\Desktop\Study\Projects\Visual_Product_Search\data\fashion_data.csv')

result=searcher.search(r'C:\Users\HP\OneDrive\Pictures\Screenshots\Screenshot 2026-09-30 202740.png')

print(result)