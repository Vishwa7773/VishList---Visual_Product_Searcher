# VishList – Visual Product Search Engine

VishList is a visual product search engine that finds similar fashion products using an uploaded image. Instead of searching through products using text or keywords, users can upload an image of a product and get visually similar products from a fashion dataset.

This project was built as a learning project to understand computer vision, image embeddings, similarity search, API development, and deployment.

## Demo

**Live Application:** https://vishlist.streamlit.app/

**Backend API:** https://vishlist-api.onrender.com

**API Documentation:** https://vishlist-api.onrender.com/docs

**GitHub Repository:** https://github.com/Vishwa7773/VishList---Visual_Product_Searcher

---

## How It Works

1. The user uploads a JPG or JPEG image through the Streamlit application.
2. The image is sent to the FastAPI backend.
3. MobileNetV2 processes the uploaded image and generates a feature embedding.
4. The embedding is normalized and passed to the FAISS search index.
5. FAISS finds the most similar product embeddings using cosine similarity.
6. The matching product details and image URLs are returned by the API.
7. Streamlit displays the similar products along with their details and images.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| TensorFlow / Keras | Image feature extraction |
| MobileNetV2 | Pretrained CNN model |
| NumPy | Numerical operations |
| Pandas | Dataset handling |
| FAISS | Similarity search |
| FastAPI | Backend API |
| Streamlit | Frontend application |
| Supabase Storage | Product image hosting |
| Git and GitHub | Version control |
| Render | Backend deployment |
| Streamlit Community Cloud | Frontend deployment |
| Google Colab | Feature extraction and resource-intensive work |

## Dataset

The project uses the **Fashion Product Images (Small)** dataset from Kaggle.

- Dataset: Fashion Product Images (Small)
- Author: Param Aggarwal
- Dataset contains approximately 44,000 fashion product images and their associated metadata.
- Metadata includes product ID, gender, master category, subcategory, article type, base colour, season, year, usage, and product display name.

For the initial version of VishList, I used 5,000 products to build and test the visual search system.

Dataset source: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small

## Project Development

### 1. Dataset Preparation

The dataset was downloaded from Kaggle and the metadata was loaded using Pandas.

The original dataset contained thousands of product images along with a CSV file containing product information.

I selected the first 5,000 records for the initial search engine. The metadata order was kept consistent with the embedding order so that each FAISS index result points to the correct product.

### 2. Feature Extraction using MobileNetV2

I used MobileNetV2 with pretrained ImageNet weights to extract visual features from product images.

Model configuration:

- `weights='imagenet'`
- `include_top=False`
- `pooling='avg'`
- Input image size: 224 × 224
- Embedding dimension: 1280

The images were resized and preprocessed using MobileNetV2's `preprocess_input()` function.

The pretrained model was used as a feature extractor. Its weights were frozen, so no model training or fine-tuning was performed.

The extracted embeddings were saved for further use.

### 3. Similarity Search using FAISS

After extracting the embeddings, I used FAISS to build a similarity search index.

The embeddings were converted to `float32` and L2-normalized.

I used:

`faiss.IndexFlatIP(1280)`

Since the embeddings were normalized, inner product similarity gives the same ranking as cosine similarity.

When a user uploads an image, its embedding is generated using the same MobileNetV2 model and compared against the stored embeddings.

FAISS returns the closest matches based on similarity scores.

### 4. Product Image Hosting using Supabase

The original product images were stored locally during development.

For deployment, I needed a way to access the product images from the online application. I used Supabase Storage for this.

A public storage bucket named `fashion-images` was created.

The product images were uploaded to Supabase, and their public URLs were stored in a CSV file.

I then merged these URLs with the metadata of the first 5,000 products to create the final metadata file used by the backend.

The FAISS index and metadata CSV maintain the same product order.

### 5. Backend Development using FastAPI

I developed the backend using FastAPI.

The backend loads the FAISS index and metadata and initializes the MobileNetV2 feature extractor.

The main endpoint is:

`POST /search`

It accepts:
- An uploaded JPG/JPEG image.
- The number of similar products to return (`k`).

The backend saves the uploaded image temporarily, generates its embedding, performs similarity search, and returns the matching product information as JSON.

The temporary file is deleted after processing.

The API also provides interactive documentation through Swagger UI.

### 6. Frontend Development using Streamlit

I used Streamlit to create the user interface.

The application allows users to:

- Upload a product image.
- Preview the uploaded image.
- Select the number of similar products to retrieve.
- Fetch visually similar products.
- View product names, categories, colours, similarity scores, and product images.

The Streamlit frontend communicates with the FastAPI backend through HTTP requests.

### 7. Deployment

The project was deployed using separate frontend and backend services.

**Backend – Render**

The FastAPI application, MobileNetV2 model, FAISS index, and metadata CSV were deployed on Render.

**Frontend – Streamlit Community Cloud**

The Streamlit application was deployed on Streamlit Community Cloud.

**Image Storage – Supabase**

Product images are hosted in a public Supabase Storage bucket, and their URLs are used by the frontend to display search results.

## Project Structure

```text
Visual_Product_Search/
│
├── app.py
│
├── data/
│   ├── fashion_data.csv
│   └── fashion_data_5000.csv
│
├── models/
│   └── Fashion_products.index
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── embedding.py
│   ├── search.py
│   └── image_search.py
│
├── requirements.txt
├── requirements-backend.txt
├── .gitignore
└── README.md
```

Note: The original image dataset, generated embeddings, environment files, and other large or sensitive files are not included in the GitHub repository.

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Vishwa7773/VishList---Visual_Product_Searcher.git
cd VishList---Visual_Product_Searcher
```

### 2. Create a virtual environment

```bash
python -m venv .myenv
```

Activate it on Windows:

```bash
.myenv\Scripts\activate
```

### 3. Install dependencies

For the backend:

```bash
pip install -r requirements-backend.txt
```

For the frontend:

```bash
pip install -r requirements.txt
```

### 4. Start the FastAPI backend

```bash
python -m uvicorn src.main:app --workers 1
```

The API will be available at:

`http://127.0.0.1:8000`

Swagger documentation:

`http://127.0.0.1:8000/docs`

### 5. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

The application will open in your browser.

## Important Notes

- The current search index contains 5,000 product embeddings.
- The metadata CSV must maintain the same order as the FAISS index.
- The backend requires the FAISS index and matching metadata CSV.
- Product images are served through public Supabase URLs.
- The pretrained MobileNetV2 model is used for feature extraction, not custom training.
- The application currently accepts JPG/JPEG uploads.
- The first request after the backend has been idle may take longer because of service startup.

## Limitations and Future Improvements

There are several things I would like to improve in future versions:

- Expand the search index to include the complete dataset.
- Improve visual similarity using fashion-specific pretrained models.
- Experiment with models such as EfficientNet and other image embedding architectures.
- Add filters for gender, category, colour, and product type.
- Improve the UI and product result presentation.
- Explore faster similarity search methods for larger datasets.
- Add support for more image formats.
- Improve error handling and application performance.

## Credits and Acknowledgements

I would like to acknowledge the following resources and tools that helped me build this project:

**Dataset**
- [Param Aggarwal – Fashion Product Images (Small) dataset on Kaggle](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)

**Machine Learning**
- TensorFlow and Keras for the deep learning framework.
- MobileNetV2 and its pretrained ImageNet weights for image feature extraction.
- Facebook AI Similarity Search (FAISS) for vector similarity search.
- NumPy and Pandas for data processing.

**Development and Deployment**
- FastAPI for backend development.
- Streamlit for frontend development.
- Supabase for image storage.
- Render for backend hosting.
- Streamlit Community Cloud for frontend hosting.
- Google Colab for running resource-intensive feature extraction.
- GitHub for version control and project hosting.

I also referred to the official documentation of these technologies while developing and debugging the project.

Finally, this project was an opportunity for me to learn by building something end to end. I worked through dataset preparation, feature extraction, vector indexing, backend and frontend development, cloud storage, deployment, and debugging along the way.
  
## Screenshots  
### Home Page
![Home Page](screenshots/Screenshot%202026-11-07%20151319.png)    
### Visual Search
![Visual Search](screenshots/Screenshot%202026-11-07%20151414.png)  
  
  
---

**Built as a learning and portfolio project.**