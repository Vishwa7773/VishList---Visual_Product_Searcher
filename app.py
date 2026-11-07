import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os


API_URL='https://vishlist-api.onrender.com/search'

st.set_page_config(page_title='Visual Product Searcch - VishList',
                   layout="wide",
                   initial_sidebar_state='auto')

st.title('VishList')
st.write(
    "Vishlist is a Visual Product Searcher.",
    "Upload the image of the product you want and see VishList Feth similar product from our Data Base"
)

uploaded_file=st.file_uploader(label='Upload your product image',
                               type=['jpg','jpeg'])
k=st.slider(label='Number of Similar Product',
            max_value=10,
            min_value=1,
            value=5)

if uploaded_file is not None:
    image_bytes=uploaded_file.getvalue()
    st.subheader('Your uploaded image!!!')
    st.image(image_bytes,width=250)

    if st.button(label='Fetch Similar Products',type='primary'):
        with st.spinner(text='Finding something for you'):
            try:
                response=requests.post(API_URL,files={"file":(uploaded_file.name,image_bytes,uploaded_file.type)},
                                       params={"k":k},timeout=120)
                if response.status_code !=200:
                    try:
                        detail=response.json().get("detail",response.text)
                    except:
                        detail=response.text
                    st.error(f'finder crashed into a problem {detail}')
                else:
                    data=response.json()
                    result=data.get("results",data.get("Results",[]))

                    if not result:
                        st.warning("No similar products were found!!!")
                    else:
                        st.subheader("Similar Products")
                        st.caption(f"Found {len(result)} products")

                        columns=st.columns(3)

                        for i,product in enumerate(result):
                            with columns[i%3]:
                                st.markdown(f'Product {i+1}')
                                name = product.get(
                                    "product",
                                    product.get(
                                        "productDisplayName",
                                        "Unnamed product"
                                    )
                                )

                                category = product.get(
                                    "articletype",
                                    product.get(
                                        "articleType",
                                        "Unknown"
                                    )
                                )

                                color = product.get(
                                    "color",
                                    product.get(
                                        "baseColour",
                                        "Unknown"
                                    )
                                )

                                similarity = product.get(
                                    "similarity",
                                    product.get("score")
                                )

                                image_path = product.get(
                                    "image",
                                    product.get("path", "")
                                )

                                if image_path :
                                    try:
                                        st.image(image_path,use_container_width=True)
                                    except Exception as  e :
                                        st.warning("Image URL was not available!")
                                        st.caption(str(e))
                                else:
                                    st.info("Product image is not available"
                                            "on the device")
                                    st.write(f"**{name}**")
                                    st.write(f"Category: {category}")
                                    st.write(f"Color : {color}")

                                    if similarity is not None:
                                        st.write(f"Similarity : {similarity}")


            except requests.exceptions.ConnectionError:
                st.error("Not able to connect with FastAPI"
                         "The backend port must be 8000")
            except requests.exceptions.Timeout:
                st.error("The search took too long. "
                    "Try again after checking your backend.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")