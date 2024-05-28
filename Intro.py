## 실행 명령어: python3 -m streamlit run streamlit_test.py

from AgensConnector import *
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import json
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
import base64

# 레이아웃 -----------------------------------------------------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="AGENS TUTORIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

#------------------------------------------------------------------------------------------------------------------------------------------------
# Paths
#------------------------------------------------------------------------------------------------------------------------------------------------

image_path = './images'
html_path = './htmls'
nx_html  = './htmls/nx.html'
data_path = './data/'

#------------------------------------------------------------------------------------------------------------------------------------------------
# 사이드바
#------------------------------------------------------------------------------------------------------------------------------------------------
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def build_markup_for_logo(
    png_file,
    background_position="15% 5%",
    margin_top="0%",
    image_width="85%",
    image_height="",
):
    binary_string = get_base64_of_bin_file(png_file)
    return """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url("data:image/png;base64,%s");
                    background-repeat: no-repeat;
                    background-position: %s;
                    margin-top: %s;
                    background-size: %s %s;
                }
            </style>
            """ % (
        binary_string, background_position, margin_top, image_width, image_height,
    )

def add_logo(png_file):
    logo_markup = build_markup_for_logo(png_file)
    st.markdown(
        logo_markup,
        unsafe_allow_html=True,
    )

add_logo('./images/common/company_logo.png')
#------------------------------------------------------------------------------------------------------------------------------------------------
# Pathes
#------------------------------------------------------------------------------------------------------------------------------------------------
# image_path = './images'
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




st.title('안녕하세요🙌')
st.title('AgensGraph 사용 튜토리얼입니다.')
text = """AgensGraph는 그래프 데이터베이스 솔루션으로, 다양한 데이터를 노드(Node)와 엣지(Edge)의 그래프(Graph) 형태로 저장하고 이를 관리, 분석, 시각화하는 솔루션입니다. \n
해당 튜토리얼을 통해 다양한 샘플 네트워크를 만나고 그래프를 기반으로 어떤 서비스를 제공할 수 있는지 체험합니다."""
st.write(text)
st.write('   ')

st.header('- 목차 -')

st.header('1. 그래프 소개')
st.subheader('ㅤ- 그래프란 무엇인지 이해해보세요.')
st.header(' ')
st.header('2. E-Commerce 데이터 그래프 기반 추천 튜토리얼')
st.subheader('ㅤ- E-Commerce 데이터를 그래프 형태로 표현하고 사용자를 탐색하거나 사용자에게 아이템을 추천해보세요.')
st.header(' ')
st.header('3. 통신데이터 기반 고객 관심사 찾기 튜토리얼')
st.subheader('ㅤ- 통신 데이터를 기반으로 작성된 그래프를 통해서 통신 데이터로 사용자들의 관심사를 알아보세요.')



# text='그래프데이터베이스 솔루션에서는 데이터 자체를 점과 선의 그래프 형태로 저장하고, \n선을 따라 특정 패턴과 이상 현상을 빠르게 추적할 수 있으며 이를 시각화 함으로써 분석을 용이하게 한 것이 특징이다. \n이를 통해 사용 기업은 데이터의 상관 관계를 보다 직관적으로 빠르게 분석할 수 있다.'
# st.text(text)




