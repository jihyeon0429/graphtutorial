# -*- coding: utf8 -*-

from AgensConnector import * 
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import json
import streamlit.components.v1 as components
from pyvis.network import Network
import networkx as nx
from streamlit_option_menu import option_menu
import base64
import os

st.set_page_config(
    page_title="AGENS TUTORIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Pathes
image_path = './images'
nx_html  = './htmls/nx.html'
html_path = './htmls'
data_path = './data'

#db_connection
default_conninfo={'host' : '127.0.0.1',
                  'port' : '5432',
                  'database' : 'agens_tutorial', 
                  'user' : 'puser',
                  'password' : '0000'}
           
agconn = AgensConnector(**default_conninfo)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
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

def img_2_centre(imgpath, caption=None, width=None):
    col1, col2, col3 = st.columns([0.5,13,4])
    with col1:
        st.write(' ')
    with col2:
        image = Image.open(imgpath)
        if caption:
            caption=caption
        if width:
            width=width
        st.image(image, caption=caption, width=width)
    with col3:
        st.write(' ')


        
        
def wt_graph():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title('그래프데이터베이스 (GraphDatabase) 는')
        st.subheader('점(Node)과 선(Edge)으로 이루어진 그래프 구조로 데이터를 저장, 표현 및 처리하는 데이터베이스입니다.')
        st.write('-------------------------------------------------------------------')
        text="""
 현실세계를 반영한 네트워크 중심의 데이터베이스 시스템으로 고도의 분석이 요구되는 컴퓨팅 환경에 맞는 **관계 중심의 데이터 구조**를 갖습니다.\n
 그래프데이터베이스의 관계는 **점**, **관계선**, 점과 선이 비슷한 경우 하나로 표현할 수 있는 **묶음**으로 이루어집니다.\n
            """
        st.write(text)
        
        text="""
**구성요소** \n
    - 점 (Vertex 혹은 Node)
      객체 하나에 대해 표현합니다. 데이터의 이름-값 쌍을 포함합니다.
    - 관계선 (Edge 혹은 Link)
      객체 간 관계를 표현합니다.
    - 묶음 (Group 혹은 Label)
      유사한 속성을 가진 그룹을 표현합니다.
      사람, 동물, 자동차와 같이 각 객체에 대해 공통적으로 정의할 수 있는 이름으로 표현할 수 있습니다.
            """
        st.write(text)
    st.subheader(' ')
    img_2_centre(imgpath='./images/0_intro/그림1_그래프의 개념.jpg', caption='그래프 구성', width=600)

    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        text="""
그렇다면 그래프 데이터는 어떻게 만들까요?👀\n
**👉상단에서 보여지는 다음 메뉴를 통해 데이터를 다양한 모양의 그래프로 바꾸어 보세요!👉**
            """
        st.subheader(' ')
        st.write(text)
        

def graph_modeling():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title("그래프 생성 과정")
        st.subheader('테이블 데이터로부터 그래프를 생성하는 방법에 대해서 알아봅니다.')
        st.text(' ')
        st.write('-------------------------------------------------------------------')
        text="""
그래프를 만들기 위해 먼저 데이터로부터 물어보고싶은, 알아보고싶은 내용을 정의합니다.\n
다음으로 알맞은 골격을 지정하면 원하는 정보를 저장하고 표현하고 처리할 수 있습니다.\n
해당 메뉴에서는 **항공 예약 데이터 관리 시스템**을 예시로 그래프를 만들어봅니다.\n
기존에 있던 RDB구조로부터 그래프로 변환하는 과정을 아래 순차적으로 설명합니다.\n
            """
        st.write(text)
        st.write('-------------------------------------------------------------------')
        st.subheader("**1. 요구사항 확인**")
        text="""
기존에 있던 RDB의 구조로부터 어떤 내용을 그래프로 담을 지 생각해봅니다.\n
항공 예약 시스템에서 보이는 **각각의 고객이 항공을 예약하는 일련의 과정**을 중심으로 그래프를 만들어봅시다! 
            """
        st.write(text)
    img_2_centre(imgpath='./images/0_intro/그림2-1_RDB.png', caption='항공예약 시스템 RDB ERD확인', width=500)
    
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.header('  ')
        st.write('-------------------------------------------------------------------')
        st.subheader("**2. 화이트보드 모델링**")
        text="""
요구사항을 토대로 그래프를 어떻게 구성할지 생각해봅니다.\n
고객이 항공을 예약하는 일련의 과정을 화이트보드에 자유롭게 그려봅니다!\n
해당 그래프는 승객의 사용자계정으로 항공예약을 진행하는 과정을 담습니다.\n
항공예약 중 비행기 정보는 따로 노드 객체로 빼내었고, 승객이 어디에 예약하는지 바로 알 수 있도록 관계를 추가합니다.
            """
        st.write(text)
    img_2_centre(imgpath='./images/0_intro/그림2-2_화이트보드모델링.png', caption='화이트보드 모델링', width=500)
    
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.header('  ')
        st.write('-------------------------------------------------------------------')
        st.subheader("**3. 논리적 구조 설계**")
        text="""
화이트보드 모델링에서 어떤 객체간의 관계가 두드러지게 보여져야 할지 기존 테이블과 테이블명, 속성명을 참고하여 좀 더 상세하게 작성합니다.\n
아래와 같은 흐름으로 다양한 관계를 생각해보고 각각의 점, 관계선, 묶음의 이름이 고유한지, 관계의 정의가 중복되어 있지는 않은지 확인해 볼 수 있습니다.
            """
        st.write(text)
    img_2_centre(imgpath='./images/0_intro/그림2-3_논리적모델링.png', caption='항공 예약 시스템 논리적 데이터 설계', width=600)
    
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.header('  ')
        st.write('-------------------------------------------------------------------')
        st.subheader("**4. 물리적 구조 설계**")
        text="""
앞서 설정한 각각의 객체에서의 속성을 세부적으로 정의합니다.\n
속성의 이름, 타입, 인덱싱 여부 등을 생각해 볼 수 있습니다.\n
다음과 같은 간단한 구조로 실행활에서 일어나는 다양한 관계들을 그대로 컴퓨터에 저장할 수 있습니다!🙃
            """
        st.write(text)
    img_2_centre(imgpath='./images/0_intro/그림2-4_결과.png', caption='그래프 완성🎉', width=500)
    
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        text="""
모델링한 내용을 바탕으로 그래프데이터베이스에 저장해 볼 수 있습니다!\n
**👉이제 상단에서 보여지는 다음 메뉴를 통해 다양한 구조의 데이터를 저장해봅시다!👉**
            """
        st.write(text)
        
def load_graph():  
    #-----------------------------------------------------------------------------------------------------------------------------------#
    # 필요 함수 정의 START
    #-----------------------------------------------------------------------------------------------------------------------------------#
    def save_upload_file(directory, file):
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(os.path.join(directory, file.name), 'wb') as f:
            f.write(file.getbuffer())
        return st.success('Save file : {} in {}'.format(file.name, directory))

    def view_graph(query):
        # 쿼리 조회
        with st.expander('쿼리 보기') :
            st.code(query, language="sql")
        #그래프데이터전처리
        G = nx.Graph()
        result = set(agconn.execute_query_withresult(query))
        users = set([str(i[0]) for i in result])
        tmp_user = set([str(i[1]) for i in result])
        users.update(tmp_user)
        for user in users:
            G.add_node(user, nodetype='user', group=1, size=20)
        for edge in result:
            G.add_edge(edge[0], edge[1])
        #화면표기
        nt = Network(height='490px', width='100%', directed=False)
        nt.from_nx(G)
        nt.save_graph(nx_html)
        nt.show(nx_html)
        #html저장
        HtmlFile = open(nx_html,'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)
        
    def display_graph(G):
        #화면표기
        nt = Network(height='490px', width='100%', directed=False)
        nt.from_nx(G)
        nt.save_graph(nx_html)
        nt.show(nx_html)
        #html저장
        HtmlFile = open(nx_html,'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)

    def view_graph_1depth_all(query):
        # 쿼리 조회
        with st.expander('쿼리 보기') :
            st.code(query, language="sql")
            
        result = set(agconn.execute_query_withresult(query))
        node_1 = list(set([str(i[0]) for i in result]))
        node_2 = list(set([str(i[1]) for i in result]))
        edges = [[str(i[0]), str(i[1])] for i in result]
        G = nx.MultiDiGraph()
        for node in node_1:
            G.add_node(node, nodetype='1', group=1, size=10)
        for node in node_2:
            G.add_node(node, nodetype='2', group=2, size=20)
        # color='#f08080'  color='#1E90FF'
        for edge in result:
            G.add_edges_from([(edge[0], edge[1])], color='f08080')
        display_graph(G)

    # 필요 함수 정의 END
    #-----------------------------------------------------------------------------------------------------------------------------------#

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    st.sidebar.markdown("""
    # 그래프 만들어보기
    - [1. 데이터 확인](#step-1)
    - [2. 데이터베이스 접속](#step-2)
    - [3. 그래프 생성 대상 테이블 불러오기](#step-3)
    - [4. 그래프 생성](#step-4)
    - [5. GRAPH_PATH 설정](#step-4)
    - [6. 노드 생성](#step-5)
    - [7. 엣지 생성](#step-5)
    - [8. 그래프 생성 결과 확인]( #step-6)
    """, unsafe_allow_html=True)
    st.sidebar.write('-------------------------------------------------------------------')
    #화면정의
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
    #-----------------------------------------------------------------------------------------------------------
    # 샘플데이터 설명 
    #-----------------------------------------------------------------------------------------------------------
        st.title('이제 그래프를 직접 만들어 보세요!')
        st.subheader('아래의 과정을 차근차근 따라하며 내가 갖고 있는 데이터로 직접 그래프를 만들어볼 수 있습니다. 샘플 예제를 참고하여 그래프를 직접 만들어 보세요!')
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 1')
        st.subheader('1. 데이터 확인')
        st.write("**그래프로 생성할 대상이 되는 데이터를 준비합니다. 예제로 사용할 데이터는 다음과 같습니다.**")
    img_2_centre(imgpath='./images/0_intro/karate_club.png', width=500)
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        text="""
        Network Science 분야에서 가장 유명한 데이터 중 하나인 Zachary's Karate Club 데이터를 그래프로 만들어 보겠습니다.\n
        Zachary's Karate Club 데이터는 가라데 클럽 회원 34명의 관계를 나타낸 소셜 네트워크 데이터입니다.\n
        person_id는 각 회원의 id를 의미하며, 관계가 있는 회원들 사이에 엣지가 연결됩니다.
        """
        st.write(text)
    col_2_0, col_2_1, col_2_2, col_2_3 = st.columns([0.5, 9, 9, 2])
    with col_2_1:
        st.write('[회원 목록]')
        st.write(pd.read_csv(data_path+'/karate_club/karate_nodelist.csv')[['person_id']])
    with col_2_2:
        st.write('[관계 목록]')
        st.write(pd.read_csv(data_path+'/karate_club/karate_edgelist.csv'))
        
        st.write('')

    #-----------------------------------------------------------------------------------------------------------
    # 데이터베이스 접속
    #-----------------------------------------------------------------------------------------------------------
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.write('-------------------------------------------------------------------')
        st.header('STEP 2')
        st.subheader('2. 데이터베이스 접속')
        st.write('**접속하고자 하는 데이터베이스 정보입니다. 기본적으로 연결되어있는 데이터베이스 정보는 아래와 같으며, 변경을 원할 경우 수정 후 Ctrl+Enter 키를 눌러주세요.**')
        connect_info = st.text_area(
            '접속 정보 입력', 
            str(default_conninfo)
        )
        connect_info = json.loads(connect_info.replace("'",'"'))
        agconn = AgensConnector(**connect_info)
        user = connect_info['user']
        host = connect_info['host']
        port = connect_info['port']
        database = connect_info['database']
        st.write(f'**You are not Connected to** {user}@{host}:{port}/{database}')
        
    #-----------------------------------------------------------------------------------------------------------
    # 적재 대상 데이터 불러오기 
    #-----------------------------------------------------------------------------------------------------------
        st.write('-------------------------------------------------------------------')
        st.header('STEP 3')
        st.subheader('3. 그래프 생성 대상 테이블 불러오기') 
        # 파일 업로드하기
        st.write('**그래프로 만들고자 하는 파일을 csv 형태로 올려주세요. 한 번에 한 개의 파일만 올리는 것이 좋습니다.**')
#         st.write('*- 업로드한 csv파일은 "/home/agens/tutorial/AgensConnecter_v1/data/" 경로에 저장됩니다.*')
        st.write('*- 그래프에 담기 위한 정보는 미리 DataFrame 형태로 저장되어 있어야 하며, DataFrame 컬럼명은 대문자를 포함해서는 안됩니다.*')
        st.write('*- 엣지에 집계성 정보 등 가공된 데이터를 담고 싶다면 해당 테이블도 미리 생성하여 저장해둡니다.*')
        st.write(' ')
        
        uploaded_files = st.file_uploader("그래프로 만들고자 하는 데이터 파일을 끌어와 보세요."
                                          , accept_multiple_files=True
                                          , type=(["tsv","csv","txt","tab","xlsx","xls"]))
        
        # 기본 데이터 
        df_default = '/home/agens/agens_tutorial/AgensConnecter_v1/data/karate_club/karate_edgelist.csv'
        df = pd.read_csv(df_default)
        agconn.load_dataframe(df)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                save_upload_file('data', uploaded_file)
                df = pd.read_csv(uploaded_file)
                agconn.load_dataframe(df)
                st.write('**Currently Connected Data :**', uploaded_file)
                
        else:
            df_default = '/home/agens/agens_tutorial/AgensConnecter_v1/data/karate_club/karate_edgelist.csv'
            df = pd.read_csv(df_default)
            agconn.load_dataframe(df)
            st.write('**Currently Connected Data :** karate_edgelist.csv (default)')
        st.write(df)
        
#         file_nm = st.text_input('그래프로 만들고자 하는 csv의 파일명을 입력하세요', 'karate_club/karate_edgelist.csv')
#         path = '/home/agens/agens_tutorial/AgensConnecter_v1/data/'+file_nm
#         ## '../data/ecommerce_sample_filtered.csv'
#         if path:
#             st.write('**LOADED DATA** : \'', path ,' \'')
#             df = pd.read_csv(path)
#             st.write(df.head(100))
#             agconn.load_dataframe(df)
    st.write('-------------------------------------------------------------------')
    st.header('STEP 4')
    #----------------------------------------------------------------------------------------------------------------------------------------
    # 그래프 적재
    #----------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3, col_4 = st.columns([4.5, 0.5, 4.5, 0.5])
    #-----------------------------------------------------------------------------------------------------------
    # 그래프 생성
    #-----------------------------------------------------------------------------------------------------------
    with col_1:
        st.subheader('4. 그래프 생성')
        graph_name = st.text_input("생성하고자 하는 그래프 이름을 입력해주세요. (영문 소문자와 '_'의 조합만 가능합니다.)", )
        st.write('**Graph Name to be Created** : '+ graph_name )

        def st_create_graph():
            if st.button(graph_name + ' 그래프 생성'):
                agconn.create_graph(graph_name)
                agconn.set_graph(graph_name)
                st.write('\-' + graph_name + ' 그래프 생성이 완료되었습니다!')

        if graph_name:
            try:
                st_create_graph()
            except:
                st.write('해당 그래프 이름은 이미 존재합니다. 다른 이름을 선택해 주세요.')
    #-----------------------------------------------------------------------------------------------------------
    # GRAPH PATH 설정
    #-----------------------------------------------------------------------------------------------------------
    with col_3:
        st.subheader('5. GRAPH PATH 설정')
        graph_name_set = st.text_input('사용할 그래프명으로 GRAPH PATH를 설정해야 합니다. 설정된 그래프로 변경사항이 적용될 것입니다. (지정 안했을 경우: karate_club)'
                                       , 'karate_club')
        
#         def st_set_graphpath():
#             if st.button('SET GRAPH_PATH to '+ graph_name_set):
#                 agconn.set_graph(graph_name_set)
#                 st.write(graph_name_set + '로 graph_path가 지정되었습니다.')
        
        graph_name = 'karate_club'
        agconn.set_graph(graph_name)
        if graph_name_set:
#             if st.button('SET GRAPH_PATH to '+ graph_name_set):
            agconn.set_graph(graph_name_set)
            st.write(graph_name_set + '로 graph_path가 지정되었습니다.')
#             st_set_graphpath()
            graph_name = graph_name_set

            
            
            
            
    st.write('-------------------------------------------------------------------')
    st.header('STEP 5')
    st.write("**여러 개의 노드/엣지를 생성하고자 하는 경우, 순차적으로 입력 후 진행하면 됩니다. 적재된 결과는 'STEP 6' 에서 확인할 수 있습니다.**")
    st.write("**\*중요 :  '5.GRAPH PATH'에서 지정된 그래프에 변경사항이 적용됩니다.**")
    agconn.set_graph(graph_name)
    st.write("**Currently Connected Graph :**", graph_name)
    st.header(' ')
    #----------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3, col_4 = st.columns([5.0, 0.5, 5.0, 0.5])
    #-----------------------------------------------------------------------------------------------------------
    # 노드 적재
    #-----------------------------------------------------------------------------------------------------------
    with col_1:
        st.subheader('6. 노드 생성') 
        st.write('*그래프모델의 노드를 하나씩 생성합니다. 그림의 번호를 참고하여 정보를 하나씩 입력해 주세요.*')
        image = Image.open(image_path + '/vt_person.png')
        st.image(image, caption='노드 적재 참고')

        #----------------------------------------#
        # 노드 적재 함수
        #----------------------------------------#
        def st_create_vertex():
            if st.button(label_name + ' 노드 적재'):
                if graph_name:
                    agconn.set_graph(graph_name)
                    # col_nm : str, label_name : str , vt_properties : list , set_properties_nm : dict
                    agconn.create_vertex(label_name      = label_name,
                                         col_nm          = col_name, 
                                         vt_properties   = vt_properties, #df의 컬럼리스트
                                         set_properties_nm = set_properties_nm_vt,
                                        )
                    st.write(' ')
                    st.write('\'' + col_name + '\' 컬럼으로 \''+  label_name + '\' 노드 적재를 완료하였습니다.')

                else:
                    st.write("지정된 그래프가 없습니다. '5.GRAPH_PATH' 설정을 진행해주세요.")
        #----------------------------------------#
        # 1. 노드 라벨 입력
        #----------------------------------------#
        agconn.set_graph(graph_name)
        label_name = st.text_input('1)생성하고자 하는 노드라벨을 입력해주세요 (Graph)'
                                   ,)
        #----------------------------------------#
        # 2. Key-Property가 되는 대상 컬럼명 선택
        #----------------------------------------#
        col_name = st.selectbox(
            '2)노드의 Key-Property가 되는 컬럼을 선택해주세요 (from DataFrame)',
            ['컬럼을 선택하세요'] + list(df.columns))


        #----------------------------------------#
        # 3. 추가할 노드 프로퍼티들 선택
        #----------------------------------------#
        # 형식 예시: vt_properties = ['user_id','event_type','count']
        if '선택' in col_name:
            vt_properties = st.multiselect(
                '3)노드에 추가할 프로퍼티들을 선택해주세요 (from DataFrame, 없을 경우 pass)',
                ['Key - Property를 먼저 선택하세요.']
            )
        else:
            properties = list(df.columns)
            properties.remove(col_name)
            vt_properties = st.multiselect(
                '3)노드에 추가할 프로퍼티들을 선택해주세요 (from DataFrame, 없을 경우 pass)',
                properties
            )
        st.write(' ')
        if '선택' not in col_name:
            rename_properties = [col_name]+vt_properties
            set_properties_nm_vt = '{'+str(['"'+i+'": "'+i+'"' for i in rename_properties]).replace('[','').replace(']','').replace("'",'')+'}'
            set_properties_nm_vt = st.text_input('4)노드 프로퍼티명 변경을 원한다면 입력해주세요. (변경을 원치 않을 경우 pass)', set_properties_nm_vt)
            set_properties_nm_vt = json.loads(set_properties_nm_vt)
        else:
            set_properties_nm_vt = {}
            st.text_input('4)노드 프로퍼티명 변경을 원한다면 입력해주세요.', '{}')
        st.write('- *예시: "category_code_2": "category1" → 테이블의 "category_code_2" 컬럼을 노드 프로퍼티 "category1"로 적재*')

        ## 노드 적재 함수 수행
        try:
            st_create_vertex()
        except OSError:
            st.write('해당 노드라벨은 이미 존재합니다. 노드라벨을 변경해주세요.')
        st.write(' ')   
    #-----------------------------------------------------------------------------------------------------------
    # 엣지 적재 
    #-----------------------------------------------------------------------------------------------------------
    with col_3:
        st.subheader('7. 엣지 생성') 
        st.write('*노드를 모두 생성했다면 연관된 노드들을 엣지로 연결합니다. 그림의 번호를 참고하여 Start Node와 End Node의 정보들을 차례로 입력해 주세요.*')
        image = Image.open(image_path+'/edg_friend_with.png')
        st.image(image, caption='엣지 적재 참고')
        #----------------------------------------#
        # 엣지 적재 함수
        #----------------------------------------#
        def st_create_edge():
            if st.button(edg_label_nm + ' 엣지적재'):
                if graph_name:
                    agconn.set_graph(graph_name)
                    agconn.create_edge(st_col_nm = st_col_nm, 
                                       ed_col_nm = ed_col_nm, 
                                       edg_label_nm = edg_label_nm, 
                                       st_label_name = st_label_name, 
                                       ed_label_name = ed_label_name,
                                       edg_properties = edg_properties, 
                                       set_properties_nm = set_properties_nm_edg,
                                       st_property_name = st_property_name,
                                       ed_property_name = ed_property_name
                                      )
                    st.write(' ')
                    st.write('엣지 적재가 완료되었습니다.')

                else:
                    st.write('지정된 그래프가 없습니다. SET GRAPH_PATH를 진행해주세요.')

        #----------------------------------------#
        # 엣지명 입력
        #----------------------------------------#
        agconn.set_graph(graph_name)
        edg_label_nm = st.text_input('1)생성하고자 하는 엣지명을 입력해주세요.')   
        st.write('')

        #----------------------------------------#
        # 스타트 노드 
        #----------------------------------------#
        st.write('')
        st.subheader('- START NODE ')
        ## 스타트 노드라벨
        st_label_name = st.selectbox(
            '2-1)스타트노드 라벨을 선택해주세요 (from Graph)',
            ['스타트노드라벨선택'] + [i[0] for i in agconn.execute_query_withresult('match (v) return distinct label(v)')]
        ) 

        ## 스타트 노드 키 프로퍼티 선택
        if st_label_name and st_label_name != '스타트노드라벨선택':
            st_properties = agconn.execute_query_withresult(f"match (v:{st_label_name}) return distinct jsonb_object_keys(properties(v))")
            st_properties = [i[0] for i in st_properties]

            st_property_name = st.selectbox(
                '2-2)스타트노드 Key-Property 선택 (from Graph)',
                st_properties
            )
        else:
            st.text_input(
            '2-2)스타트노드 Key-Property 선택 (from Graph)',
            '스타트노드 라벨을 먼저 선택해 주세요.'
            )

        ## 스타트노드 컬럼
        st_col_nm = st.selectbox(
            '2-2)스타트노드의 Key-Property가 되는 컬럼을 선택해주세요 (from DataFrame)',
            ['st_eg_col 선택하세요']+list(df.columns))


        #----------------------------------------#
        # 엔드 노드 
        #----------------------------------------#
        st.write('')
        st.write('')
        st.subheader('- END NODE ')

        ## 엔드 노드라벨
        ed_label_name = st.selectbox(
            '3-1)엔드노드 라벨을 선택해주세요 (from Graph)',
            ['엔드노드라벨선택'] + [i[0] for i in agconn.execute_query_withresult('match (v) return distinct label(v)')]
        ) 
        # st.write('You Selected: ', ed_label_name)

        ## 엔드 노드 키 프로퍼티 선택
        if ed_label_name and ed_label_name != '엔드노드라벨선택':
            ed_properties = agconn.execute_query_withresult(f"match (v:{ed_label_name}) return distinct jsonb_object_keys(properties(v))")
            ed_properties = [i[0] for i in ed_properties]

            ed_property_name = st.selectbox(
                '3-2)엔드노드 Key-Property 선택 (from Graph)',
                ed_properties
            )
        else:
            st.text_input(
            '3-2)엔드노드 Key-Property 선택 (from Graph)',
            '엔드노드 라벨을 먼저 선택해 주세요.'
            )

        ## 엔드 노드 컬럼
        ed_col_nm = st.selectbox(
            '3-2)엔드노드의 Key-Property가 되는 컬럼을 선택해주세요 (from DataFrame)',
            ['ed_eg_col 선택하세요']+list(df.columns))


        st.write('')
        #----------------------------------------#
        # 엣지 프로퍼티 선택
        #----------------------------------------#
        st.write('')
        st.write('')
        st.subheader('**엣지 프로퍼티 선택**')
        # 형식 예시: edg_properties = ['user_id','event_type','count']
        edg_properties = st.multiselect(
            '4)엣지 프로퍼티가 되는 컬럼들을 선택해주세요 (from DataFrame, 없을 경우 pass)',
            df.columns
            )

        st.write(' ')

        #----------------------------------------#
        # 엣지 프로퍼티 네임 선택
        #----------------------------------------#
        # 형식 예시: set_properties_nm = {'event_type' : 'eventtypetype'}
        set_properties_nm_edg = '{'+str(['"'+i+'": "'+i+'"' for i in edg_properties]).replace('[','').replace(']','').replace("'",'')+'}'
        set_properties_nm_edg = st.text_input('5)엣지 프로퍼티명 변경을 원한다면 입력해주세요 (변경을 원치 않을 경우 pass) ', set_properties_nm_edg)
        st.write('- *예시: "category_code_2": "category1" → 테이블의 "category_code_2" 컬럼을 엣지 프로퍼티 "category1"로 적재*')
        set_properties_nm_edg = json.loads(set_properties_nm_edg)

        #-----------------------------------------------------------------------------#
        # 엣지 적재 함수 실행 
        #-----------------------------------------------------------------------------#
        try:
            st_create_edge()
        except OSError:
            st.write('해당 엣지라벨은 이미 존재합니다. 엣지라벨을 변경해주세요.')

    st.title('   ')
    st.write('-------------------------------------------------------------------')
    st.header('STEP 6')
    st.subheader('8. 그래프 생성 결과 확인')
    st.write("**'5. GRAPH PATH 설정' 에서 그래프명을 변경하면 해당 그래프에 대한 정보를 확인할 수 있습니다.**")
    st.write("**Currently Connected Graph :**", graph_name)
    st.write("**[그래프 조회]**")
    #----------------------------------------------------------------------------------------------------------------------------------------
    
    agconn.set_graph(graph_name)
    query   = "match (v) return distinct label(v)"
    vlabels = [i[0] for i in agconn.execute_query_withresult(query)]
    
    col_1, col_2, col_3, col_4 = st.columns([4.5, 0.5, 4.5, 0.5])
    with col_1:
        start_node = st.selectbox(
            'Start Node를 선택해 주세요.'
            , vlabels
        )

        query = f"match (v:{start_node}) return distinct jsonb_object_keys(properties(v));"
        properties = [i[0] for i in agconn.execute_query_withresult(query)]
        start_node_property = st.selectbox(
            '조회를 원하는 Start Node의 값을 선택해 주세요.'
            , properties
        )
        
    with col_3:
        end_node = st.selectbox(
            'End Node를 선택해 주세요'
            , vlabels
        )
        
        query = f"match (v:{end_node}) return distinct jsonb_object_keys(properties(v));"
        properties = [i[0] for i in agconn.execute_query_withresult(query)]
        
        end_node_property = st.selectbox(
            '조회를 원하는 End Node의 값을 선택해 주세요.'
            , properties
        )
        
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        query = f"""
match (v1:{start_node})-[r]-(v2:{end_node}) 
return v1.{start_node_property}, v2.{end_node_property}, ' '
limit 100
        """
        if start_node == end_node:
            view_graph(query)
        else:
            view_graph_1depth_all(query)
        
    
    st.write("**[그래프 적재 결과]**")
    col_1, col_2, col_3, col_4 = st.columns([4.5, 0.5, 4.5, 0.5])
    #-----------------------------------------------------------------------------------------------------------
    # 노드 적재 결과
    #-----------------------------------------------------------------------------------------------------------
    agconn.set_graph(graph_name)
    with col_1:
        st.write('- 노드 생성 결과')
        query1 = """
        match (v) 
        return distinct (label (v)) as node, count(1)
        order by node
        """
        res_node = agconn.execute_query_withresult(query1)
        res_node = pd.DataFrame(res_node, columns =['node', 'count'])
        st.write(res_node)
    #-----------------------------------------------------------------------------------------------------------
    # 엣지 적재 결과
    #-----------------------------------------------------------------------------------------------------------
    with col_3:
        st.write('- 엣지 생성 결과')
        query2 = """
        match (v1)-[r]->(v2)
        return distinct label(v1) as start_node
            , label(r) as edge
            , label(v2) as end_node
            , count(1)
        order by edge, start_node, end_node
        """
        res_edge = agconn.execute_query_withresult(query2)
        res_edge = pd.DataFrame(res_edge, columns=['start_node', 'edge', 'end_node', 'count'])
        st.write(res_edge)


selected_menu = option_menu(None, 
                        ["GDB란?", "그래프 생성 과정", "그래프 만들어보기"], 
                        icons=['house', "search", "cursor"], 
                        menu_icon="cast", 
                        default_index=0, 
                        orientation="horizontal"
                       )



if selected_menu == 'GDB란?':
    wt_graph()
elif selected_menu == '그래프 생성 과정':
    graph_modeling()
elif selected_menu == '그래프 만들어보기':
    load_graph()
    
    
    
    
    
    
    
