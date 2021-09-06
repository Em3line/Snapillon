import streamlit as st
from PIL import Image
import time
import requests
import pickle
import base64
import os
from dotenv import load_dotenv
import glob

load_dotenv() 

DOCKER = 'https://snapillon-dytlcwlbnq-ew.a.run.app'
#CSS

CSS = """
.titre_principal {
    text-align: center; color : white; FONT face='century gothic';
}
"""
st.write('<style>{CSS}</style>', unsafe_allow_html=True)

# Titres et textes introductifs
logo_snapillon = Image.open("scripts/snapillon_logo.png").resize((200,210))
col1, col2, col3 = st.columns(3)
with col1:
    pass
with col2:
    st.image(logo_snapillon )
with col3:
    pass

st.markdown("""
    # Par ici les petits papillons !
    ### Uploader une photo afin de tâcher de déterminer l'espèce de papillons associée
""")

# Set background
def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def background_image_style(path):
    encoded = load_image(path)
    style = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
    }}
    </style>
    '''
    return style

image_path = "scripts/9B2F199E-79BF-4EBD-B729-D518A58D1292_1_105_c.jpeg"
st.write(background_image_style(image_path), unsafe_allow_html=True)

# Drag and drop files
st.set_option('deprecation.showfileUploaderEncoding', False)
uploaded_file = st.file_uploader("", type=['png','jpeg','jpg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    with col1:
        st.image(image)
    with col2:
        st.warning('Photo chargée avec succès !')
        st.markdown("""#### *Vous pouvez lancer une nouvelle prédiction en glissant une nouvelle photo ou bien en fermant avec la croix*
        """)
    st.markdown("""## ... Lancement de l'algorithme Snapillon ... """)
    
    # Update the progress bar with each iteration
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.02)

    st.markdown("""# Par ici les résultats !""")

    parameters2 = dict(string = base64.b64encode(uploaded_file.getbuffer()).decode("utf-8"))
    api_url = os.environ.get("API_URL")
    dico = requests.post(api_url, json = parameters2, headers={"Content-Type": "application/json; charset=utf-8"}).json()
    
    print(f"Retour API : {dico}")
    for j, i in enumerate(dico.keys()):
        st.markdown(f"""## Estimation n°{j+1} : Votre papillon est un *{dico[i][0].replace('_', " ")}*""") #sort le nom de l'espèce en latin
        st.markdown(f"""### *Probabilité de la prédiction : {round(float(i),3)}*""")
        mypath = f"raw_data/Docker/Photos/{dico[i][0]}/"
        images = glob.glob(mypath+'*.JPG')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(images[0])
        with col2:
            st.image(images[1])
        with col3 :
            st.image(images[2])
