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

st.set_page_config(
    page_title="AGENS TUTORIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

#변수설정
# Pathes
image_path = './images'
html_path = './htmls'
nx_html  = './htmls/nx.html'
data_path = './data/'

#gragph_path
graph_name = 'test'
#db_connection
default_conninfo={'host' : '127.0.0.1',
                  'port' : '5432',
                  'database' : 'agens_tutorial', 
                  'user' : 'puser',
                  'password' : '0000'}
           
agconn = AgensConnector(**default_conninfo)
agconn.set_graph(graph_name)

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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 함수 정의
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 유저와 카테고리1만 조회하는 함수
# ONE-DEPTH ; query MUST return  user_id, category1, event_type, count in order. 
def view_graph_ecommerce_user_ctgry1(query):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query, language="sql")
    
    #그래프데이터전처리
    result = set(agconn.execute_query_withresult(query))
    users     = list(set([i[0] for i in result]))
    category1 = list(set([i[1] for i in result]))
    edges_weight = list(result)
    G = nx.DiGraph()
    # 노드 추가
    for user in users:
        G.add_node(user, nodetype='user', group=1, size=20)
    for ctgry1 in category1:
        G.add_node(ctgry1, nodetype='category1', group=2, size=10)
    # 엣지 추가
    for edge in edges_weight:
        G.add_edge(edge[0], edge[1], event_type=edge[2], count=edge[3])
    #화면표기
    nt = Network(height='490px', width='100%', directed=True)
    nt.from_nx(G)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)


def view_graph_ecommerce_user_ctgry1_multilabeled(query,weighted=0):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query, language="sql")
    
    #그래프데이터전처리
    G = nx.MultiDiGraph()
    result = set(agconn.execute_query_withresult(query))
    users     = list(set([i[0] for i in result]))
    category1 = list(set([i[1] for i in result]))
    for user in users:
        G.add_node(user, nodetype='user', group=1, size=20)
    for ctgry1 in category1:
        G.add_node(ctgry1, nodetype='category1', group=2, size=10)
    for edge in result:
        edge = list(edge)
        stdt=tuple([edge[0],edge[1]])
        if edge[2]=='view':    color='#f08080'
        elif edge[2]=='purchase':    color='#1E90FF'
        else:    color='#ff6347'
        if weighted==1:    G.add_edges_from([stdt],label=edge[2],weight=edge[3],color=color)
        else:    G.add_edges_from([stdt],label=edge[2],color=color)
    #화면표기
    nt = Network(height='490px', width='100%', directed=True)
    nt.from_nx(G)
    nt.set_options("""
    const options = {
      "physics": {
        "minVelocity": 0.75,
        "solver": "repulsion"
      }
    }
    """)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)

# 유저와 모든 카테고리를 조회하는 함수
def view_graph_ecommerce_user_ctgrs(query):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        st.code(query, language="sql")
    
    #그래프데이터전처리
    G = nx.DiGraph()
    result = set(agconn.execute_query_withresult(query))
    users     = list(set([i[0] for i in result]))
    category1 = list(set([i[1] for i in result]))
    category2 = list(set([i[2] for i in result]))
    category3 = list(set([i[3] for i in result]))
    for user in users:
        G.add_node(user, nodetype='user', group=1, size=20)
    for ctgry1 in category1:
        G.add_node(ctgry1, nodetype='category1', group=2, size=10)
    for ctgry2 in category2:
        G.add_node(ctgry2, nodetype='category2', group=3, size=10)
    for ctgry3 in category3:
        G.add_node(ctgry3, nodetype='category3', group=4, size=10)
    for edge in result:
        edge = list(edge)
        stdt=[tuple([edge[0],edge[1]]),tuple([edge[1],edge[2]]),tuple([edge[2],edge[3]])]
        G.add_edges_from(stdt)

    #화면표기
    nt = Network(height='490px', width='100%', directed=True)
    nt.from_nx(G)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)

def view_graph_multy_path(query):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        st.code(query, language="sql")
        
    #그래프데이터전처리
    G = nx.MultiDiGraph()
    edges_u1,edges_12,edges_23=[],[],[]
    result = set(agconn.execute_query_withresult(query))
    users     = list(set([i[0] for i in result]))
    category1 = list(set([i[1] for i in result]))
    category2 = list(set([i[2] for i in result]))
    category3 = list(set([i[3] for i in result]))
    for user in users:
        G.add_node(user, nodetype='user', group=1, size=20)
    for ctgry1 in category1:
        G.add_node(ctgry1, nodetype='category1', group=2, size=20)
    for ctgry2 in category2:
        G.add_node(ctgry2, nodetype='category2', group=3, size=10)
    for ctgry3 in category3:
        G.add_node(ctgry3, nodetype='category3', group=4, size=10)
    for edge in result:
        edge = list(edge)
        edges_u1.append(tuple([edge[0],edge[1]]))
        edges_12.append(tuple([edge[1],edge[2]]))
        edges_23.append(tuple([edge[2],edge[3]]))
    edges_u1 = list(set(edges_u1))
    edges_12 = list(set(edges_12))
    edges_23 = list(set(edges_23))
    G.add_edges_from(edges_u1)
    G.add_edges_from(edges_12)
    G.add_edges_from(edges_23)
    #데이터 추가
    tmp_q = "match (a:vt_category1{category1:'vacuum'})-[r1{event_type:'purchase'}]-(b:vt_brand) return a.category1,b.brand,r1.user_id;"
    result = set(agconn.execute_query_withresult(tmp_q))
    brand = list(set([i[1] for i in result]))
    edges_weight = list(result)
    # 노드 추가
    for brnd in brand:
        G.add_node(brnd, nodetype='brand', group=5, size=30)
    # 엣지 추가
    for edge in edges_weight:
#         label_tmp = 'user_id:'+str(edge[2])+', count:'+str(edge[3])
        G.add_edge(edge[0], edge[1], label=str(edge[2]))
    
    #화면표기
    nt = Network(height='490px', width='100%', directed=True)
    nt.from_nx(G)
    nt.set_options("""
    const options = {
      "physics": {
        "minVelocity": 0.75,
        "solver": "repulsion"
      }
    }
    """)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)

def view_graph_multy_3(query):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        st.code(query, language="sql")
    #그래프데이터전처리
    G = nx.DiGraph()
    result = set(agconn.execute_query_withresult(query))
    users     = list(set([i[0] for i in result]))
    category1 = list(set([i[1] for i in result]+[i[3] for i in result]))
    category2 = list(set([i[2] for i in result]))
    for user in users:
        G.add_node(user, nodetype='user', group=1, size=20)
    for ctgry1 in category1:
        G.add_node(ctgry1, nodetype='category1', group=2, size=20)
    for ctgry2 in category2:
        G.add_node(ctgry2, nodetype='category2', group=3, size=10)
    for edge in result:
        edge = list(edge)
        stdt=[tuple([edge[0],edge[1]]),tuple([edge[1],edge[2]]),tuple([edge[3],edge[2]])]
        G.add_edges_from(stdt)
    #화면표기
    nt = Network(height='490px', width='100%', directed=True)
    nt.from_nx(G)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def intro():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # 사이드바
    add_logo('./images/common/company_logo.png')
    #화면정의
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title('E-Commerce 튜토리얼')
        st.subheader('그래프데이터베이스를 통해 이커머스데이터에 대한 탐색, 조회, 활용을 수행합니다.')
        st.write('-------------------------------------------------------------------')
        text="""
E-commerce 데이터는 계속해서 고객, 아이템간의 새로운 데이터가  발생합니다. 이때 각 특성 데이터 뿐만아니라 고객이 아이템을 확인할 경우, 장바구니에 추가하는 경우, 구매하는 경우 등 관계로 표현될 수 있습니다.\n
이 때 그래프데이터베이스를 활용하면 고객과 상품간의 관계를 통해 사용자의 특성을 이해하고 아이템을 추천해 줄 수 있습니다. \n
이 튜토리얼에서는 OPEN CDP(고객 데이터 플랫폼)에 공개된 e-commerce 데이터를 통해 csv파일에 담겨있는 데이터를 그래프로 적재하고, 조회하며 데이터를 이해합니다. 네트워크에 담긴 고객데이터를 통해 그래프 추천 로직의 기초를 체험합니다.\n
상단의 메뉴를 통해 튜토리얼을 진행해보세요!
        """
        st.write(text)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# view() START
def view():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    graph_name='test'
    add_logo('./images/common/company_logo.png')
    st.sidebar.markdown("""
    # 그래프 조회
    - [1. 데이터베이스 접속](#step-1)
    - [2. 노드 조회](#step-2)
    - [3. 관계 조회](#step-3)
    """, unsafe_allow_html=True)
    st.sidebar.write('-------------------------------------------------------------------')
    #streamlit_code_1_start
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 1 : 데이터베이스 접속 
    #------------------------------------------------------------------------------------------------------------------------------------------------
        st.title('E-Commerce 그래프 조회')
        st.subheader('E-Commerce 데이터로 생성한 그래프를 조회해 볼 수 있도록 안내하는 튜토리얼입니다.')
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 1')
        st.subheader('데이터베이스 접속 및 그래프 선택')
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
#         st.text_input("조회할 그래프명 ('test'를 입력하면 미리 생성되어 있는 샘플그래프 조회 가능)", graph_name)
    #-----------------------------------------------------------------------------#
    # 사용할 그래프  
    #-----------------------------------------------------------------------------#
    graph_name = 'test'
    agconn.set_graph(graph_name)   
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 2 : 노드 조회
    #------------------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title('  ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 2')
        st.subheader('노드 조회')
        st.markdown('**E-Commerce 그래프에 생성한 노드를 조회합니다.**')
        #--------------------------------------------------------------------------
        # 조회하고자하는 노드라벨 및 프로퍼티 선택 
        #--------------------------------------------------------------------------
        query   = "match (v) return distinct label(v)"
        vlabels = [i[0] for i in agconn.execute_query_withresult(query)]
        vlabel = st.selectbox(
            '조회를 원하는 노드명을 선택해 주세요.',
            ['노드 종류 선택'] + vlabels
        )

        if '선택' in vlabel:
            st.text_input('조회를 원하는 노드 속성명을 선택해주세요.', '노드 종류를 먼저 선택해 주세요.')
            vproperty = ''
        else:
            query   = f"match (v:{vlabel}) return distinct jsonb_object_keys(properties(v))"
            vproperties = [i[0] for i in agconn.execute_query_withresult(query)]
            vproperty = st.selectbox(
                '조회를 원하는 노드 속성명을 선택해주세요.',
                ['노드 속성명 선택'] + vproperties
            )
        #--------------------------------------------------------------------------
        # 그래프 시각화
        #--------------------------------------------------------------------------    
        if '선택' not in vlabel and '선택' not in vproperty:
            query = f"match (v:{vlabel}) return v.{vproperty}::text limit 20"

            result = [i[0] for i in agconn.execute_query_withresult(query)]

            G = nx.DiGraph()
            G.add_nodes_from(result, nodetype=vlabel, group=1, size=30)

            nt = Network('490px', '100%')
            nt.from_nx(G)
            nt.save_graph(nx_html)
            nt.show(nx_html)

            HtmlFile = open(nx_html,'r', encoding='utf-8')
            components.html(HtmlFile.read(), height=500)

        else:
            query = f"match (v:vt_user) where v.user_id='-' return v "

            result = [i[0] for i in agconn.execute_query_withresult(query)]

            G = nx.DiGraph()
            G.add_nodes_from(result, nodetype=vlabel, group=1, size=30)

            nt = Network('490px', '100%')
            nt.from_nx(G)
            nt.save_graph(html_path + '/nx.html')
            nt.show(html_path + '/nx.html')

            HtmlFile = open(html_path + '/nx.html','r', encoding='utf-8')
            components.html(HtmlFile.read(), height=500)

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 3 : 관계 조회 - 1 depth
    #------------------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:
        st.write('-------------------------------------------------------------------')
        st.header('STEP 3')
        st.subheader('관계 조회')
        st.write('**이커머스 그래프에 생성된 노드들 간의 관계를 조회합니다.**')
        #--------------------------------------------------------------------------
        # 특정 물건을 구매한 사람들 조회
        #-------------------------------------------------------------------------- 
        st.markdown('**1. 특정 상품에 관심을 보인 사람들 조회**')
        st.write("**- 각 상품에 가장 많이 관심을 보인 사람들 조회합니다. 구매, 조회, 장바구니 등 이벤트 유형별로 각각 조회할 수 있습니다.**")

        ctgry1 = st.text_input('구매) 조회를 원하는 상품군(카테고리1)을 입력해주세요. 상품 예시: washer, tv, headphone, refrigerators, vacuum, keds, kettle, microwave, bed, oven 등'
                               , 'washer')
        st.write("'" + ctgry1 + "\'를 가장 많이 '구매'한 고객들")
        
        if ctgry1:
            query = f"""
match (v1:vt_user)-[r:eg_interested]->(v2: vt_category1)
where r.event_type = 'purchase'
  and v2.category1 = '{ctgry1}'
return v1.user_id::text, v2.category1, r.event_type, r.count 
order by count desc
limit 100; 
            """
        else:
            query = 'match (v:vt_user) where v.user_id=1 return *'
            

        if __name__=='__main__':
            view_graph_ecommerce_user_ctgry1_multilabeled(query)

                
        #--------------------------------------------------------------------------
        # 특정 물건을 조회한 사람들 조회
        #-------------------------------------------------------------------------- 

        ctgry1 = st.text_input('장바구니) 조회를 원하는 상품군(카테고리1)을 입력해주세요. 상품 예시: washer, tv, headphone, refrigerators, vacuum, keds, kettle, microwave, bed, oven 등'
                               , 'washer')
        st.write("'" + ctgry1 + "\'를 가장 많이 '장바구니'에 담은 고객들")
        
        if ctgry1:
            query = f"""
                match (v1:vt_user)-[r:eg_interested]->(v2: vt_category1)
where r.event_type = 'cart'
  and v2.category1 = '{ctgry1}'
return v1.user_id::text, v2.category1, r.event_type, r.count 
order by count desc
limit 100; 
            """
        else:
            query = 'match (v:vt_user) where v.user_id=1 return *'
            
        if __name__=='__main__':
            view_graph_ecommerce_user_ctgry1_multilabeled(query)
                
        #--------------------------------------------------------------------------
        # 특정 사람들이 구매한 물품 조회
        #--------------------------------------------------------------------------  
        st.markdown('**2. 특정 사람들이 관심을 보인 상품 조회**')

        st.write("**- 고객별로 어떤 상품에 관심을 보였는지 확인합니다. 조회를 원하는 고객ID와 이벤트 유형을 선택해 주세요.**")
        user_id = st.text_input("""조회를 원하는 사용자의 아이디를 입력해주세요(복수 입력 가능)
                                (고객ID 예시: 533316379, 512670642, 533074223, 525351013, 518957516, 514948520, 547029219, 556747652 등..)"""
                                , str([533316379, 512670642]))
        event_type = st.multiselect('조회를 원하는 event_type을 선택해주세요.'
                                    , ['purchase', 'cart', 'view'])
        
        if event_type:
            query = f"""
                match (v1: vt_user)-[r: eg_interested]->(v2: vt_category1)
where v1.user_id in {user_id}
and r.event_type in {event_type}
return v1.user_nm::text, v2.category1, r.event_type, r.count 
            """
        else:
            query = 'match (v:vt_user) where v.user_id=1 return *'
        
        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgry1_multilabeled(query)
    return
# retrieve() END

#util() START
def util():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    st.sidebar.markdown("""
    # 그래프 활용
    - [1. 데이터베이스 접속](#step-1)
    - [2. 사용자 탐색](#step-2)
    - [3. 그래프 기반 추천](#step-3)
    - [4. 사용자별 추천 상품 조회](#step-4)
    """, unsafe_allow_html=True)
    st.sidebar.write('-------------------------------------------------------------------')
    #streamlit_code_1_start
    graph_name='test'    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 1 : 데이터베이스 접속 
    #------------------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title('E-Commerce 그래프 활용')
        st.subheader('E-Commerce 그래프의 사용자와 아이템간의 관계를 통해 그래프 기반 추천 로직을 이해할 수 있도록 안내하는 튜토리얼입니다.')
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 1')
        st.subheader('데이터베이스 접속')
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
#         st.text_input("조회할 그래프명 ('test'를 입력하면 미리 생성되어 있는 샘플그래프 조회 가능)", graph_name)
    #--------------------------------------------------------------------------
    # 사용할 그래프
    #--------------------------------------------------------------------------
    graph_name = 'test'
    agconn.set_graph(graph_name)
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 2 : 관심 상품에 따른 고객 메타 정의
    #------------------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:
        st.title('  ')    
        st.write('-------------------------------------------------------------------')
        st.header('STEP 2')
        st.subheader('사용자 탐색')  
        text="""**판매자는 사용자가 관심을 보인 상품을 확인할 수 있습니다.**"""
        st.markdown(text)
        #------------------------------------------------------------------------------#
        st.write('**1) 첫 번째 사용자**')
        text="""ㅤㅤ문시원 사용자는 의류나 가구와 같은 상품을 조회하였고 육아용품을 구매하였습니다.\n
ㅤㅤ위의 행동을 통해 키즈/육아에 관심있는 사용자로 분류할 수 있습니다."""
        st.write(text)
        
        user_id = 533316379
        query = f"""
match (v1: vt_user)-[r: eg_interested]->(v2: vt_category1)
where v1.user_id = {user_id}
return v1.user_nm, v2.category1, r.event_type as event, r.cnt
        """
        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgry1_multilabeled(query,weighted=1)


        #------------------------------------------------------------------------------#
        st.write('**2) 두 번째 사용자**')
        text="""ㅤㅤ남태호 사용자는 여러 상품을 조회하였지만 그 중 'tv', '세탁기', '청소기'를 장바구니에 담았고 '냉장고', 'tv', '세탁기', '청소기'를 최종 구매하였습니다.\n
ㅤㅤ따라서 해당 사용자는 가전제품을 중심으로 행동하는 홈퍼니싱 관심고객으로 분류됩니다.
        """
        st.write(text)

        user_id = 533074223
        query = f"""
match (v1: vt_user)-[r: eg_interested]->(v2: vt_category1)
where v1.user_id = {user_id}
return v1.user_nm, v2.category1, r.event_type as event
        """
        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgry1_multilabeled(query)


        #------------------------------------------------------------------------------#
        st.write('**3) 세 번째 사용자**')
        text="""ㅤㅤ이에 반해 배으뜸 사용자가 구매한 상품은 'tv', '에어컨', '전자레인지', '냉장고', '세탁기'와 같습니다. \n
ㅤㅤ남태호 사용자와 유사하게 가전제품을 중심으로 관심을 나타내는 홈퍼니싱 관심고객으로 분류합니다.
        """
        st.write(text)

        user_id = 512386086
        query = f"""
match (v1: vt_user)-[r: eg_interested]->(v2: vt_category1)
where v1.user_id = {user_id}
return v1.user_nm, v2.category1, r.event_type as event
        """
        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgry1_multilabeled(query)


    st.title('  ')

    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 3 : 그래프 기반 추천
    #------------------------------------------------------------------------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------------------------------
    # 유사 사용자와의 관계
    #-------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])
    with col_2:    
        st.write('-------------------------------------------------------------------')
        st.header('STEP 3')
        st.subheader('그래프 기반 추천')

        st.markdown('**1. 판매자는 각 구매자의 취향에 따라 유사한 구매자를 찾을 수 있습니다.**')
        text="""ㅤㅤ각 사용자들의 행동을 독립적으로 분석하는 것이 아닌, 여러 사용자들의 행동을 복합적으로 분석함으로써, 고객과 상품간의 보다 폭넓은 관계를 파악합니다.\n
ㅤㅤ그래프 추천시스템은 사용자들과 관심 상품의 관계를 통해서 추천 상품을 직관적이고 효과적으로 선정합니다.\n
ㅤㅤ"""
        st.write(text)
        

        user_id = st.text_input(
            '조회하고자 하는 사용자의 ID를 입력해주세요.',
            str([512386086, 533074223])
        )
#         user_id = str([512386086, 533074223])
#         event_type = str(['purchase', 'view', 'cart'])

        query = f"""
match (v1:vt_user)-[r:eg_interested]->(v2:vt_category1)-[r2]->(v3)-[r3]->(v4)
where v1.user_id in [512386086, 533074223]  
and r.event_type='purchase'
return v1.user_nm,v2.category1,v3.category2,v4.category3;
        """

        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgrs(query)
            wording='남태호 사용자와 구매 패턴이 유사한 배으뜸 사용자의 구매내역을 바탕으로, 남태호 사용자에게 vacuum 아이템을 추천해 줄 수 있습니다.'
            reccomend = f'<font color="blue"><center><b>{wording}</b></center></font>'
            st.write(reccomend, unsafe_allow_html=True)
            # 컬러 블루 왜안먹혀...
            st.write("   ")
    #-------------------------------------------------------------------------------------------------------
    # 추천해줄 제품 선정 1
    #-------------------------------------------------------------------------------------------------------
        st.title('  ')

        st.markdown('**2. 판매자는 사용자가 구매한 것과 유사한 범주의 트랜디한 제품을 추천할 수 있습니다.**')
        text="""ㅤㅤ앞서 vacuum 을 추천받은 사용자에게 어떤 vacuum 아이템을 추천해줘야 하는지 확인해봅시다.\n
ㅤㅤvacuum을 판매하는 브랜드별 구매한 사용자와 몇 개를 구매했는지 관계의 속성으로 확인할 수 있습니다."""
        st.write(text)

        query = f"""
match (v1:vt_user)-[r:eg_interested]->(v2:vt_category1)-[r2]->(v3)-[r3]->(v4),
(v2)-[r4]->(v5:vt_brand)
where v1.user_id in [512386086, 533074223] 
and r.event_type='purchase'
return v1.user_nm,v2.category1,v3.category2,v4.category3,r4.user_id,v5.brand;
        """
        if __name__=='__main__':
            if user_id:
                view_graph_multy_path(query)

            wording='samsung 브랜드는 다수의 사람이 여러번 구매하였으므로 해당 브랜드의 아이템을 추천할 수 있습니다.'
            reccomend = f'<font color="blue"><center><b>{wording}</b></center></font>'
            st.write(reccomend, unsafe_allow_html=True)
            st.write("   ")

    #-------------------------------------------------------------------------------------------------------
    # 추천해줄 제품 선정 2
    #-------------------------------------------------------------------------------------------------------
        st.title('  ')

        st.markdown('**3. 판매자는 구매자가 구매한 제품과 유사한 제품을 찾아 추천할 수 있습니다.**')
        text="""ㅤㅤ배으뜸 사용자가 구매한 아이템의 카테고리 확인 및 같은 카테고리의 다른 아이템 확인합니다.\n
ㅤㅤtv와 같은 카테고리로 분류되는 projector, washer와 같은 카테고리로 분류되는 dish washer와 같이\n
ㅤㅤ사용자가 구매한 아이템과 유사한 아이템을 제안할 수 있습니다."""
        st.write(text)
        
        user_id = '512386086'
        query = f"""
match (a:vt_user)-[r1]->(b:vt_category1)-[r2]->(c:vt_category2),(e:vt_category1)-[r4]->(c)
where a.user_id=512386086 
return a.user_id,b.category1,c.category2,e.category1;
        """
        if __name__=='__main__':
            if user_id:
                view_graph_multy_3(query)
    st.title('  ')
    st.write('-------------------------------------------------------------------')
    
    
    #------------------------------------------------------------------------------------------------------------------------------------------------
    # STEP 4 : Interactive 추천
    #------------------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3 = st.columns([0.5, 18, 2])

    with col_2: 
        st.header('STEP 4')
        st.subheader('사용자별 추천 상품 조회')
        
        # Step 1 : 입력 받은 User_ID와(사용자1) 상품 취향이 유사한 사용자(사용자2) 탐색
        user_id = st.text_input('상품을 추천 받고자 하는 사용자 ID를 직접 입력해 주세요.', 512386086)

        query1=f"""
        select *
from ( 
    select q.user_nm, q.target_id target_id, q.target_nm target_nm, q.items items, q.cnt cnt,
        rank() over (order by cnt desc) as rank
    from (
        match (v1:vt_user)-[r1]->(v2:vt_category1)<-[r2]-(v3:vt_user)
        where id(v1)<>id(v3)
          and v1.user_id={user_id}
        return v1.user_nm, v3.user_id as target_id, v3.user_nm as target_nm, count(distinct v2) as cnt
            , collect(distinct v2.category1) as  items
        ) q
    ) qq
where qq.rank=1 
order by random() 
limit 1;
        """
        
        res = agconn.execute_query_withresult(query1)
        user_nm = res[0][0]          # 입력받은 사용자 이름
        target_user_id = res[0][1]   # 관심 상품이 비슷한 사용자 ID
        target_user_nm = res[0][2]   # 관심 상품이 비슷한 사용자명
        not_in_item = str(res[0][3]) # 공통으로 관심을 보인 상품 
        
        # 사용자1과 사용자2가 관심을 보인 상품들 조회
        query=f"""
match (v1)-[r1]->(v2:vt_category1)
where v1.user_id in [{user_id}, {target_user_id}]
return v1.user_nm::text, v2.category1, r1.event_type, r1.cnt
        """
        
        
        if __name__=='__main__':
            if user_id:
                view_graph_ecommerce_user_ctgry1_multilabeled(query)
            
            # 추천상품 선택 쿼리
            query2 = f"""
            match (v1:vt_user)-[r1]->(v2:vt_category1)
            where v1.user_id in [{target_user_id}]
            and not v2.category1 in {not_in_item}
            return distinct v2.category1, sum(r1.cnt) as sum_cnt
            order by sum_cnt desc
            limit 10
            """
#             recc_item = agconn.execute_query_withresult(query2)[0][0]
            res = agconn.execute_query_withresult(query2)
            recc_item = [i[0] for i in res]
            
            wording = f"""'{user_nm}'와/과 관심 상품이 가장 유사한 사용자는 '{target_user_nm}'이며, \n
'{target_user_nm}'이/가 관심을 보인 {recc_item}들과 같은 상품을 추천해줄 수 있습니다."""
            reccomend = f'<font color="blue"><center><b>{wording}</b></center></font>'
            st.write(reccomend, unsafe_allow_html=True)
            
            with st.expander('참고: 비슷한 취향의 사용자 추출 쿼리') :
                st.code(query1, language="sql")
            
    
    
    return
#util() END


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# load() START   
def load():
    
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
    
    
    #streamlit_code_1_start    
    #화면정의
    col_1, col_2, col3 = st.columns([0.5, 18, 2])
    with col_2:
    #-----------------------------------------------------------------------------------------------------------
    # 샘플데이터 설명 
    #-----------------------------------------------------------------------------------------------------------
        st.title('E-Commerce 데이터 그래프 만들어보기')
        st.subheader('E-Commerce 데이터를 통해 사용자가 테이블로부터 손쉽게 그래프를 만들어볼 수 있도록 안내하는 튜토리얼입니다.')
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 1')
        st.subheader('1. 데이터 확인')
        st.write("- E-Commerce 데이터로 고객들이 구매한 상품과 카테고리 정보를 담고 있는 데이터입니다.")
        st.write("- 구매한 물품을 통해서 사용자들의 취향을 파악하고 정의해볼 수 있습니다.")
        st.write("- 그래프를 통해 관심 상품을 기반으로 한 다른 고객들과의 관계까지 파악할 수 있습니다.")
        st.write("- 튜토리얼을 활용하여 아래 그래프 모델과 같이 그래프를 적재해보세요!")

        image = Image.open(image_path + '/ecommerce_model.png')
        st.image(image, caption='출처: https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store')
        st.write('')

    #-----------------------------------------------------------------------------------------------------------
    # 데이터베이스 접속
    #-----------------------------------------------------------------------------------------------------------
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
        st.title('   ')
    #-----------------------------------------------------------------------------------------------------------
    # 적재 대상 데이터 불러오기 
    #-----------------------------------------------------------------------------------------------------------
        st.title('   ')
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
        df_default = '/home/agens/agens_tutorial/AgensConnecter_v1/data/df_eg_interested.csv'
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
        graph_name_set = st.text_input('사용할 그래프명으로 GRAPH PATH를 설정해야 합니다. 설정된 그래프로 변경사항이 적용될 것입니다. (지정 안했을 경우: test)'
                                       , 'test')
        
#         def st_set_graphpath():
#             if st.button('SET GRAPH_PATH to '+ graph_name_set):
#                 agconn.set_graph(graph_name_set)
#                 st.write(graph_name_set + '로 graph_path가 지정되었습니다.')
        
        graph_name = 'test'
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
    st.write("**Currently Connected Graph :**", graph_name)
    st.header(' ')
    #----------------------------------------------------------------------------------------------------------------------------------------
    col_1, col_2, col_3, col_4 = st.columns([4.5, 0.5, 4.5, 0.5])
    #-----------------------------------------------------------------------------------------------------------
    # 노드 적재
    #-----------------------------------------------------------------------------------------------------------
    with col_1:
        st.subheader('6. 노드 생성') 
        st.write('*그래프모델의 노드를 하나씩 생성합니다. 그림의 번호를 참고하여 정보를 하나씩 입력해 주세요.*')
        image = Image.open(image_path + '/USER_NODE.png')
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
        label_name = st.text_input('1)생성하고자 하는 노드라벨을 입력해주세요 (Graph)')
        
        #----------------------------------------#
        # 2. Key-Property가 되는 대상 컬럼명 선택
        #----------------------------------------#
        col_name = st.selectbox(
            '2)노드의 Key-Property가 되는 컬럼을 선택해주세요 (from DataFrame)',
            ['컬럼을 선택하세요 (ex: person_id)'] + list(df.columns))

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
            rename_properties = [col_name] + vt_properties
            set_properties_nm_vt = '{'+str(['"'+i+'": "'+i+'"' for i in rename_properties]).replace('[','').replace(']','').replace("'",'')+'}'
            set_properties_nm_vt = st.text_input('4) 노드 프로퍼티명 변경을 원한다면 입력해주세요. (변경을 원치 않을 경우 pass)', set_properties_nm_vt)
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
        image = Image.open(image_path+'/RELATION.png')
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
    
    #----------------------------------------------------------------------------------------------------------------------------------------
    # STEP 6 : 적재 결과 확인
    #----------------------------------------------------------------------------------------------------------------------------------------
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


    return
# load() END
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 함수 실행
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# #화면변수설정
# page_names_to_funcs = {
#     "이커머스 튜토리얼 소개" : intro,
#     "데이터 적재": load,
#     "데이터 조회": retrieve,
#     "데이터 활용": util,
# }

# #dropbox표기
# selected_page = st.sidebar.selectbox("Select a tutorial", page_names_to_funcs.keys())
# page_names_to_funcs[selected_page]()

selected_menu = option_menu(None, 
                        ["E-Commerce 튜토리얼 소개", "그래프 조회", "그래프 활용", "그래프 만들어보기"],
                        icons=['house', 'cloud-upload', "search", "cursor"], 
                        menu_icon="cast", 
                        default_index=0, 
                        orientation="horizontal"
                       )


if selected_menu == 'E-Commerce 튜토리얼 소개':
    intro()
elif selected_menu == '그래프 조회':
    view()
elif selected_menu == '그래프 활용':
    util()
elif selected_menu == '그래프 만들어보기':
    load()






