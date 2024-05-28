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
data_path = './data/telecommunication_sample_dataset'


#db_connection
default_conninfo={'host' : '127.0.0.1',
                  'port' : '5432',
                  'database' : 'agens_tutorial', 
                  'user' : 'agens',
                  'password' : '0000'}
           
agconn = AgensConnector(**default_conninfo)

#set general gragph_path
graph_name = 'test_carrier'
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





#-----------------------------------------------------------------------------------------------------------------------------------#
# 그래프 시각화 함수 START
#-----------------------------------------------------------------------------------------------------------------------------------#
def display_graph(G):
    #화면표기
    nt = Network(height='490px', width='100%', directed=False)
    nt.from_nx(G)
    nt.save_graph(nx_html)
    nt.show(nx_html)
    #html저장
    HtmlFile = open(nx_html,'r', encoding='utf-8')
    components.html(HtmlFile.read(), height=500)

def view_property_graph(query):
    result = set(agconn.execute_query_withresult(query))
    node_property = {node[0] : node[1] for node in result}
    node_property = {node[2] : node[3] for node in result}
    G = nx.MultiDiGraph()
    for node in node_property.keys():
        G.add_node(node, nodetype=node_property[node], size=20)
    for edge in result:
        G.add_edges_from([(edge[0], edge[2])], color='f08080')
    display_graph(G)

def view_community_graph(query):
    result = set(agconn.execute_query_withresult(query))
    node_property = {node[0] : node[1] for node in result}
    node_property = {node[2] : node[3] for node in result}
    G = nx.MultiDiGraph()
    for node in node_property.keys():
        G.add_node(node, nodetype=node_property[node], group=node_property[node], size=20)
    for edge in result:
        G.add_edges_from([(edge[0], edge[2])], color='f08080')
    display_graph(G)
    
def view_graph_1depth_all(query):
    result = set(agconn.execute_query_withresult(query))
    node_1 = list(set([i[0] for i in result]))
    node_2 = list(set([i[1] for i in result]))
    edges = [[i[0], i[1]] for i in result]
    G = nx.MultiDiGraph()
    for node in node_1:
        G.add_node(node, nodetype='1', group=1, size=10)
    for node in node_2:
        G.add_node(node, nodetype='2', group=2, size=20)
    # color='#f08080'  color='#1E90FF'
    for edge in result:
        G.add_edges_from([(edge[0], edge[1])], color='f08080')
    display_graph(G)
    
#----------------------------------------------------------------------------------------
# 고객노드와 연결된 노드가 1종류일 때 시각화
#----------------------------------------------------------------------------------------

 #1 depth 그래프 조회 함수.
 # query return 순서 : [start_node, end_node, edge_property]
def view_graph_1depth(query, weighted=0):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query, language="sql")
    
    # 그래프데이터 전처리
    result = set(agconn.execute_query_withresult(query))
    node_1 = list(set([i[0] for i in result]))
    node_2 = list(set([i[1] for i in result]))
    edges = [[i[0], i[1]] for i in result]
    edge_property = [i[2] for i in result]

    G = nx.MultiDiGraph()

    for node in node_1:
        G.add_node(node, nodetype='1', group=1, size=20)

    for node in node_2:
        G.add_node(node, nodetype='2', group=2, size=10)

    # color='#f08080'  color='#1E90FF'
    for edge in result:
        G.add_edges_from([(edge[0], edge[1])], label=edge[2], weight=edge[2], color='f08080')

    display_graph(G)
# end view_graph_1depth()  


#----------------------------------------------------------------------------------------
# 고객노드와 연결된 노드가 2종류일 때 시각화
#----------------------------------------------------------------------------------------
#1 depth 그래프 조회 함수.
# query1 return 순서 : [start_node, end_node, edge_property]
# query2 return 순서 : [start_node, end_node, edge_property]
def view_graph_1depth_2node(query1, query2, weighted=0):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query1+' union '+ query2) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query1+' union '+ query2, language="sql")

    # 그래프데이터 전처리
    result1 = set(agconn.execute_query_withresult(query1))
    result2 = set(agconn.execute_query_withresult(query2))

    
    node_1 = list(set([i[0] for i in result1] + [i[0] for i in result2]))
    node_2 = list(set([i[1] for i in result1]))
    node_3 = list(set([i[1] for i in result2]))

    G = nx.MultiDiGraph()

    for node in node_1:
        G.add_node(node, nodetype='1', group=1, size=20)

    for node in node_2:
        G.add_node(node, nodetype='2', group=2, size=10)
    
    for node in node_3:
        G.add_node(node, nodetype='3', group=3, size=10)

    # color='#f08080'  color='#1E90FF'
    for edge in result1:
        G.add_edges_from([(edge[0], edge[1])], label=edge[2], weight=edge[2], color='f08080')
    
    for edge in result2:
        G.add_edges_from([(edge[0], edge[1])], label=edge[2], weight=edge[2], color='f08080')

    display_graph(G)
# end view_graph_1depth_2node()


#----------------------------------------------------------------------------------------
# 2 depth 시각화
# 고객 - SVC - 고객 
# 고객 - BIZPLC - 고객 
#----------------------------------------------------------------------------------------
# query 순서 : [node1, edge_property1, node2, edgeproperty2, node3]
def view_graph_2depth_2node(query1, query2, weighted=0):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query1+' union '+ query2) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query1+' union '+ query2, language="sql")

    # 그래프데이터 전처리
    result1 = set(agconn.execute_query_withresult(query1))
    result2 = set(agconn.execute_query_withresult(query2))
    
    # 고객1(기준)
    node_1 = list(set([i[0] for i in result1] + [i[0] for i in result2]))
    
    # bizplc or svc
    node_2 = list(set([i[2] for i in result1]))
    node_3 = list(set([i[2] for i in result2]))
    
    # 고객2(다른고객들)
    node_4 = list(set([i[4] for i in result1] + [i[4] for i in result2]))


    G = nx.MultiDiGraph()

    for node in node_1:
        G.add_node(node, nodetype='1', group=1, size=20)

    for node in node_2:
        G.add_node(node, nodetype='2', group=2, size=10)
    
    for node in node_3:
        G.add_node(node, nodetype='3', group=3, size=10)
        
    for node in node_4:
        G.add_node(node, nodetype='4', group=4, size=10)
        
    # color='#f08080'  color='#1E90FF'
    for edge in result1:
        G.add_edges_from([(edge[0], edge[2])], label=edge[1], weight=edge[1], color='f08080')
        
    for edge in result2:
        G.add_edges_from([(edge[0], edge[2])], label=edge[1], weight=edge[1], color='f08080')
    
    for edge in result1:
        G.add_edges_from([(edge[2], edge[4])], label=edge[3], weight=edge[3], color='f08080')
        
    for edge in result2:
        G.add_edges_from([(edge[2], edge[4])], label=edge[3], weight=edge[3], color='f08080')

    display_graph(G)
    
# end view_graph_2depth_2node()


#----------------------------------------------------------------------------------------
# 고객, 메타 노드 시각화
#----------------------------------------------------------------------------------------
#1 depth 그래프 조회 함수.
# query return 순서 : [start_node, end_node, edge_property]
def view_graph_cust_meta(query, user_nm, weighted=0):
    # 쿼리 조회
    with st.expander('쿼리 보기') :
        if agconn.execute_query_withresult(query) == []:
            st.code('  ', language="sql")
        else: 
            st.code(query, language="sql")
    
    # 그래프데이터 전처리
    result = set(agconn.execute_query_withresult(query))
    node_1 = list(set([i[0] for i in result]))
    node_2 = list(set([i[1] for i in result]))
    node_2.remove(user_nm)

    G = nx.MultiDiGraph()
    
    # 기준 되는 고객 노드
    G.add_node(user_nm, nodetype='1', group=1, size=15)  
    
    for node in node_1:
        G.add_node(node, nodetype='2', group=2, size=20)

    for node in node_2:
        G.add_node(node, nodetype='3', group=3, size=10)

    # color='#f08080'  color='#1E90FF'
    for edge in result:
        G.add_edges_from([(edge[0], edge[1])], label=edge[2], weight=edge[2], color='f08080')

    display_graph(G)
# end view_graph_cust_meta()  

# 그래프 시각화 함수 END
#-----------------------------------------------------------------------------------------------------------------------------------#



#-----------------------------------------------------------------------------------------------------------------------------------#
# intro START 
#-----------------------------------------------------------------------------------------------------------------------------------#   
def intro():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    #화면정의
    col_1, col_2 = st.columns([17, 4])
    with col_1:
        st.title('통신데이터 튜토리얼')
        st.subheader('그래프데이터베이스를 통해 통신데이터에 대한 탐색, 조회, 활용을 수행합니다.')
        st.write('-------------------------------------------------------------------')
        text="""
통신사는 고객이 어디에 전화했는지, 어느 서비스에 접속했는지에 대한 통신데이터를 갖습니다. 통신데이터에서는 고객의 정보와 행동 이력을 확인할 수 있어 고객에 대한 특성을 분석할 수 있습니다. \n
단순한 집계/통계 정보만으로는 서로 다른 각각의 고객들에 대한 특성을 이해하기 어렵습니다. 그래프데이터베이스를 활용하면 고객과 서비스간의 관계를 통해 고객의 행동을 이해하고 이를 바탕으로 고객의 메타 정보를 추가할 수 있습니다.\n
해당 시나리오는 고객의 행동 관계를 기반으로 유사성을 확인하고 관심사에 대한 메타정보를 정의합니다. 더 나아가 상점의 메타정보를 확장합니다.\n
상단의 메뉴를 통해 튜토리얼을 진행해보세요!
        """
        st.write(text)
# intro END
#-----------------------------------------------------------------------------------------------------------------------------------#   
        
        
#-----------------------------------------------------------------------------------------------------------------------------------#
# scenario START 
# 사용할 데이터를 확인하고 활용할 분석 기법을 소개
#-----------------------------------------------------------------------------------------------------------------------------------#   
def scenario():
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    add_logo('./images/common/company_logo.png')
    st.sidebar.markdown("""
    # 분석 시나리오
    - [1. 분석목적 설정](#step-1)
    - [2. 데이터 확인 및 EDA](#step-2)
    - [3. 그래프 모델링](#step-3)
    - [4. 그래프 분석](#step-4)
    """, unsafe_allow_html=True)
    st.sidebar.write('-------------------------------------------------------------------')
    col_1, col_2 = st.columns([17, 4])
    with col_1:
        st.title('통신데이터 분석 시나리오')
        st.write('통신데이터를 통해 어떤 분석을 수행할 수 있는지 단계별로 설명합니다.')
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('INTRO')
        st.subheader('분석 배경 및 개요')
        text = """
OO 통신사는 고객이 어디에 전화했는지, 어느 서비스에 접속했는지에 대한 통신데이터를 갖고 있습니다. 통신데이터에서는 고객의 정보와 행동 이력을 확인할 수 있어 고객에 대한 특성을 분석할 수 있습니다. 단순한 집계/통계 정보만으로는 서로 다른 각각의 고객들에 대한 특성을 이해하기 어렵습니다. 그래프데이터베이스를 활용하면 고객과 서비스간의 관계를 통해 고객의 행동을 이해하고 이를 바탕으로 고객의 메타 정보를 추가할 수 있습니다.
해당 시나리오는 고객의 행동 관계를 기반으로 유사성을 확인하고 관심사에 대한 메타정보를 정의합니다.
        """
        st.write(text)
        st.write('   ')
        st.write('-------------------------------------------------------------------')
        st.header('STEP 1')
        st.subheader('1. 분석목적 설정')
        text = """
먼저 분석을 통해 어떤 결과를 얻고 싶은지 정의합니다.\n
해당 튜토리얼에서는 고객의 행동데이터를 그래프로 구축하여 메타 정보를 확장하고자 합니다. 그러므로 아래와 같은 목적을 설정할 수 있습니다.
        """
        st.write(text)
        st.write("- 고객 간 유사성 확인 → 통화를 한 적 있는 사업장들을 바탕으로 유사한 고객군 도출")
        st.write("- 고객 관심사 메타정보 정의 → 전화 통화 내역과 인터넷 접속 내역을 통해서 고객의 관심사 메타 도출")
        
        st.write('-------------------------------------------------------------------')
        st.header('STEP 2')
        st.subheader('2. 데이터 확인')
        st.write('앞서 설정한 분석 목적을 위해서 다음과 같은 가설을 세우고 분석을 진행합니다. ')
        st.write("- 개인 고객이 전화한 사업장은 고객 관심사를 반영하고 있을 것이다.")
        st.write("- 비슷한 관심사를 갖고 있는 고객들은 비슷한 상점에 전화했을 것이다")
        
        st.write('  ')
        st.write('분석에 사용할 데이터는 크게 3종류로 다음과 같습니다. 아래 3종 데이터를 하나의 그래프에 통합하여 고객 성향 분석에 사용합니다.')
        st.write('- 고객 정보')
        st.write(pd.read_csv(data_path + '/user_info.csv').head(5))
        st.write('- 전화 통화 내역')
        st.write(pd.read_csv(data_path + '/cdr_sample.csv').head(5))
        st.write('- 인터넷 접속 내역')
        st.write(pd.read_csv(data_path + '/sgi_sample.csv').head(5))

        st.write('-------------------------------------------------------------------')
        st.header('STEP 3')
        st.subheader('3. 그래프 모델링')
        text="""
분석을 통해 확인하고자 하는 내용을 중심으로 노드와 엣지를 정의해야 합니다.\n
우리는 고객 간의 관계, 고객과 상점간의 관계를 중심으로 확인하기 때문에 다음과 같이 모델링 할 수 있습니다.
        """
        st.write(text)
        image = Image.open('./images/2_telecommunication/carrier_call_model.png')
        st.image(image, caption='고객 통화이력 모델')
        text="""
다음과 같이 적재된 그래프를 통해 간단한 조회가 가능합니다.\n
고객들이 전화한 사업장과 전화한 횟수(or 시간)가 그래프에 나타납니다.
        """
        st.write(text)
#         그래프조회(노드/관계)


        st.write('-------------------------------------------------------------------')
        st.header('STEP_4')
        st.subheader('4. 그래프 분석')
        text = """
모델링 된 그래프를 통해 데이터를 분석하는 방법을 소개합니다. \n
먼저 고객 간의 직접적인 관계를 확인할 수 있도록 그래프 관계 투영 기법을 활용합니다. \n
**- 그래프 관계 투영(Graph projection)이란?** \n
    고객, 상점과 같이 두 개 종류의 라벨을 가진 그래프를 이분 그래프라 불립니다.
    이 때 고객 간의 관계를 직관적으로 확인할 수 있도록 단일 그래프로 변환할 수 있습니다.
    그래프의 구조적 이점을 통해 한다리 건넌 새로운 관계들이 형성되고 이를 기반으로 새롭게 그래프 분석을 시도해볼 수 있는 장점을 갖습니다.
    변환 과정은 아래와 같습니다.
        """
        st.write(text)
        image = Image.open('./images/2_telecommunication/projection_example.png')
        st.image(image, caption='그래프 투영 변환 과정')
        text = """
투영기법을 통해 전체 그래프에서 같은 상점에 전화한 고객 간의 관계를 볼 수 있습니다. 같은 상점에 전화한 고객은 유사하다고 간주합니다.
        """
        st.write(text)
        
    col_1, col_2, col_3, col_4, col_5 = st.columns([8, 0.5, 8, 0.5,4])
    with col_1:
        text="- 고객과 상점을 연결한 이분그래프"
        st.write(text)
        query="""
match (a:vt_cust)-[r]->(b:vt_shop) where a.tel_no in 
['010-0661-6970','010-6571-5182','010-0830-5353','010-0807-7185','010-0077-2466','010-2622-7115','010-8627-3515','010-0310-6270','010-6220-1588','010-5818-4328','010-5732-1855','010-0664-9085','010-0699-7496','010-0571-6955','010-0972-1679','010-1336-7149','010-1452-4769','010-4723-4432','010-7237-2671','010-0492-8945','010-0185-6525','010-7629-8584','010-6604-7531','010-0316-9461','010-5322-1882','010-2632-5861','010-8504-8948','010-0668-5119','010-5723-2833','010-9241-8628','010-0196-9718','010-0112-1787','010-1151-1957','010-8116-4164','010-8230-2434','010-0609-9883','010-9505-2445','010-0148-8451','010-0051-0284','010-2573-5117','010-9564-6552','010-2675-1188','010-5878-2965','010-7286-5653','010-0101-1427','010-1376-9895','010-1360-2252','010-5919-1668','010-9820-1221','010-0191-8818','010-0098-8612','010-0363-9339','010-1452-4769','010-9505-2445','010-0196-9718','010-0609-9883','010-0830-5353','010-6604-7531','010-1336-7149','010-0664-9085','010-0807-7185','010-9820-1221','010-7237-2671','010-0668-5119','010-5878-2965','010-0363-9339','010-5322-1882','010-7629-8584','010-5723-2833','010-2632-5861','010-6220-1588','010-2622-7115','010-0191-8818','010-8230-2434','010-8627-3515','010-2573-5117','010-6571-5182','010-0310-6270','010-0571-6955','010-5818-4328','010-1376-9895','010-0051-0284','010-5732-1855','010-0185-6525','010-8504-8948','010-8116-4164','010-0699-7496','010-0112-1787','010-0148-8451','010-9241-8628','010-7286-5653','010-0101-1427','010-0492-8945','010-0972-1679','010-0316-9461','010-0661-6970','010-4723-4432','010-9564-6552','010-2675-1188','010-5919-1668','010-0077-2466','010-1360-2252','010-1151-1957','010-0098-8612']
return a.tel_no,b.bizplc_nm
        """
        view_graph_1depth_all(query)
    with col_3:
        text="- 고객 간의 관계를 직접 연결한 단일그래프"
        st.write(text)
        query="""match (a:vt_cust)-[r:edg_projection]-(b:vt_cust) 
        where r.type != 'meta' and a.cdr_community is not null and b.cdr_community is not null and r.cnt>1 
        return a.tel_no, a.cdr_community, b.tel_no, b.cdr_community;"""
        view_property_graph(query)

    col_1, col_2 = st.columns([17, 4])
    with col_1:
        text = """
투영된 단일 그래프에서 고객들의 관계를 기반으로 유사성을 확인하기 위한 그래프 군집분석을 수행합니다.\n
같은 군집에 속해있는 고객들이 전화한 상점들은 유사한 성질을 가질 수 있습니다. \n
\n
**- 그래프 군집분석이란?**\n
    전체 고객 그래프를 여러 개의 군집으로 나누어 각 군집이 어떤 특성을 갖고 있는지 살펴봅니다.
    군집분석된 그래프는 아래와 같이 확인할 수 있습니다.\n
        """
        st.write(text)
        
    col_1, col_2, col_3, col_4, col_5 = st.columns([8, 0.5, 8, 0.5, 4])
    with col_1:
        text="""- 아래의 그림은 그래프 투영을 통해서 같은 상점에 전화한 고객 간의 관계를 보여줍니다."""
        st.write(text)
        query="match (a:vt_cust)-[r:edg_projection]-(b:vt_cust) where r.type != 'meta' and a.cdr_community is not null and b.cdr_community is not null and r.cnt>1 return a.tel_no,a.cdr_community,b.tel_no,b.cdr_community;"
        view_property_graph(query)
    
    with col_3:
        text="- 군집분석을 진행하면 유사한 군집으로 묶여있는 고객들을 한눈에 확인할 수 있습니다."
        st.write(text)

        query="""match (a:vt_cust)-[r:edg_projection]-(b:vt_cust) 
    where r.type != 'meta' and a.cdr_community is not null and b.cdr_community is not null and r.cnt>1 
    return a.tel_no, a.meta_community, b.tel_no,b.meta_community;"""        
        view_community_graph(query)
        
    col_1, col_2 = st.columns([17, 4])

    with col_1:
        st.write('같은 군집으로 묶인 고객들의 특성을 파악하여 각 군집을 정의하고, 그래프로 생성하여 활용합니다.')
        wording = ('이제 다음의 그래프 확인 메뉴로 가서 실제 적용했을 때의 그래프는 어떤지 확인해보세요!')
        wording_style = f'<font color="blue"><center><b>{wording}</b></center></font>'
        st.write(wording_style, unsafe_allow_html=True)

# scenario END
#-----------------------------------------------------------------------------------------------------------------------------------# 
        
        
#-----------------------------------------------------------------------------------------------------------------------------------#
# util START
# 구축된 그래프를 기반으로 분석 수행
# 예시 데이터를 활용한 분석, 사용자의 csv 데이터를 가져와서 활용하는 분석
#-----------------------------------------------------------------------------------------------------------------------------------#     
def util():
    #------------------------------------------------------------------------------------#
    # 새로운 데이터 적재 관련 함수들 START
    #------------------------------------------------------------------------------------#
    def store_personalize_creategraph(graph_name):
        agconn.drop_graph(graph_name)
        agconn.create_graph(graph_name)
        st.write('\-' + graph_name + ' 그래프 생성이 완료되었습니다!')
        
    def store_personalize_cust(graph_name,dataframe,custid_col,custnm_col):
        agconn.set_graph(graph_name)
        agconn.create_vertex(label_name      = 'vt_cust',
                             col_nm          = custid_col,
                             vt_properties   = [custnm_col],
                             set_properties_nm = {custid_col : 'tel_no', custnm_col : 'user_nm'}
                            )
        st.write('\- 사용자 노드 생성이 완료되었습니다!')
        
    def store_personalize_usershop(graph_name,dataframe,custid_col,shop_col):
        agconn.set_graph(graph_name)
        agconn.create_vertex(label_name      = 'vt_shop',
                             col_nm          = shop_col,
                             set_properties_nm = {shop_col : 'bizplc_nm'}
                            )
        agconn.create_edge(st_col_nm = custid_col, 
                           ed_col_nm = shop_col, 
                           edg_label_nm = 'edg_call', 
                           st_label_name = 'vt_cust', 
                           ed_label_name = 'vt_shop'
                              )
        st.write('\- 사용자-상점의 연결관계 생성이 완료되었습니다!')
        
    def store_personalize_userservice(graph_name,dataframe,custid_col,service_col):
        agconn.set_graph(graph_name)
        agconn.create_vertex(label_name      = 'vt_service',
                             col_nm          = service_col,
                             set_properties_nm = {service_col : 'bizplc_nm'}
                            )
        agconn.create_edge(st_col_nm = custid_col, 
                           ed_col_nm = service_col, 
                           edg_label_nm = 'edg_visit', 
                           st_label_name = 'vt_cust', 
                           ed_label_name = 'vt_service'
                              )
        # projection edge 생성
        query="""
DROP table tmp_table cascade;
CREATE TABLE tmp_table AS(
    select q.st as st,q.ed as ed,q.cnt::integer as cnt
    from (match (a:vt_cust)-[r1]->(b:vt_shop)<-[r2]-(c:vt_cust)
        where id(a)>id(c) 
        return id(a) as st,id(c) as ed,count(distinct b) as cnt)q
    );
create elabel if not exists edg_projection;
LOAD FROM tmp_table AS ROW
MATCH (a:vt_cust),(b:vt_cust)
WHERE id(a) = ROW.st and id(b) = ROW.ed
merge (a)-[r1:edg_projection{cnt:ROW.cnt,type:'cdr'}]->(b);
                """
        agconn.execute_query(query)
        agconn.commit_agens()
        query="""
DROP table tmp_table cascade;
CREATE TABLE tmp_table AS(
    select q.st as st,q.ed as ed,q.cnt::integer as cnt
    from (match (a:vt_cust)-[r1]->(b:vt_service)<-[r2]-(c:vt_cust)
        where id(a)>id(c) 
        return id(a) as st,id(c) as ed,count(distinct b) as cnt)q
    );
LOAD FROM tmp_table AS ROW
MATCH (a:vt_cust),(b:vt_cust)
WHERE id(a) = ROW.st and id(b) = ROW.ed
merge (a)-[r1:edg_projection{cnt:ROW.cnt,type:'sgi'}]->(b);
                """
        agconn.execute_query(query)
        agconn.commit_agens()
#             군집수행 후 군집정보를 각 노드의 속성으로 저장
        query="match p= (a)-[r:edg_projection{type:'cdr'}]->(b) return a.tel_no, b.tel_no;"
        result = agconn.execute_query_withresult(query)
        node_list = set(item for t in result for item in t)
        g = nx.Graph()
        g.add_nodes_from(node_list)
        g.add_edges_from(result)
        communities = nx.algorithms.community.louvain_communities(G=g, resolution=1.1)
        for comm in range(len(communities)):
            for tel_no in communities[comm]:
                query = f"""MATCH (A:vt_cust {{tel_no:'{tel_no}'}})
                        SET A+= {{'meta_community':{comm}}};"""
                agconn.execute_query(query)
        agconn.commit_agens()
        query="match p= (a)-[r:edg_projection{type:'sgi'}]->(b) return a.tel_no, b.tel_no;"
        result = agconn.execute_query_withresult(query)
        node_list = set(item for t in result for item in t)
        g = nx.Graph()
        g.add_nodes_from(node_list)
        g.add_edges_from(result)
        communities = nx.algorithms.community.louvain_communities(G=g, resolution=1.1)
        for comm in range(len(communities)):
            for tel_no in communities[comm]:
                query = f"""MATCH (A:vt_cust {{tel_no:'{tel_no}'}})
                        SET A+= {{'meta_community':{comm}}};"""
                agconn.execute_query(query)
        agconn.commit_agens()
        st.write('\- 사용자-서비스의 연결관계 생성이 완료되었습니다!')
        
    def store_meta_info(graph_name,user_telno,meta_info):
        agconn.set_graph(graph_name)
        query=f"""
        create vlabel if not exists vt_meta;
        create elabel if not exists edg_meta;
        merge (a:vt_meta {{category:'{meta_info}'}});
        """
        agconn.execute_query(query)
        agconn.commit_agens()
        query=f"""
        match (a:vt_cust {{tel_no:'{user_telno}'}}) return a.meta_community;
        """
        user_comm = agconn.execute_query_withresult(query)[0][0]
        query=f"""
        match (a:vt_cust),(b:vt_meta)
        where a.meta_community='{user_comm}' and b.category='{meta_info}'
        merge (a)-[r:edg_meta]->(b);
        """
        agconn.execute_query(query)
        agconn.commit_agens()
    
    # 새로운 데이터 적재 관련 함수들 END
    #------------------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------------------#
    # 분석 모듈 수행 함수 START
    #------------------------------------------------------------------------------------#
    def util_env(graph_name):
        
        # 예시데이터 사용 시 
        if graph_name == 'test_carrier':
            st.subheader('그래프를 활용한 분석 예시를 확인해 보세요.')
            st.subheader('예시 데이터에서 분석을 원하는 고객을 선택해 보세요.')
            enter_user_telno = st.text_input('아래 고객 정보의 전화번호를 참조하여 조회를 원하는 고객의 전화번호를 입력해 주세요.'
                                       , '010-0664-9085')
            enter_user_nm = agconn.execute_query_withresult(f"match (v:vt_cust) where v.tel_no = '{enter_user_telno}' return v.user_nm")[0][0]
            st.write('고객 정보')
            st.write(pd.read_csv(data_path + '/user_info.csv')[['tel_no', 'user_nm', 'gender']])
            util_contents(graph_name, enter_user_telno, enter_user_nm)
        
        # 새로운 데이터 사용 시
        elif graph_name != 'test_carrier':
            st.header('직접 생성한 그래프로 분석을 수행해보세요!')
            graph_name = st.text_input('분석을 시작할 그래프 이름을 입력하여 환경설정을 해주세요!', graph_name)
            agconn.set_graph(graph_name)
            st.write('**Graph Name To Be Analyzed** : ' + graph_name )          
            
            # 그래프 이름 입력하면 실행
            if len(graph_name)>0:
                data = agconn.execute_query_withresult(f"match (v:vt_cust) return v.tel_no,v.user_nm;")
                df = pd.DataFrame.from_records(data, columns =['tel_no', 'user_nm'])
                st.subheader('입력 데이터에서 분석을 원하는 고객을 직접 선택해 보세요.')
                enter_user_telno = st.text_input('아래 입력된 고객 정보를 참조하여 조회를 원하는 고객의 정보를 입력해 주세요.','')
                st.write('고객 정보')
                st.write(df)
            
            
                if enter_user_telno:
                    enter_user_nm = agconn.execute_query_withresult(f"match (v:vt_cust) where v.tel_no = '{enter_user_telno}' return v.user_nm")[0][0]
                    util_contents(graph_name, enter_user_telno, enter_user_nm)
                
    def util_contents(graph,user_telno, user_nm):
        agconn.set_graph(graph)
        #------------------------------------------------------------------------------------#        
        st.write('**1. 위 고객이 통화했던 곳과 접속했던 사이트를 통해서 관심사를 알아봅니다.**')
        st.write('ㅤㅤ- 고객, 고객이 통화한 사업장, 접속한 앱/웹을 각각 노드로 만들고 연결하여 관계를 표현합니다.')
        
        # 유저 전화번호 입력 시 수행
        if user_telno:
            query1=f"""
    match (v1:vt_cust)-[r:edg_call]-(v2) 
    where v1.tel_no = '{user_telno}'
    return v1.user_nm, v2.bizplc_nm, '  '        
            """
            query2=f"""
    match (v1:vt_cust)-[r:edg_visit]-(v2) 
    where v1.tel_no = '{user_telno}'
    return v1.user_nm, v2.bizplc_nm, '  '        
            """
        else:
            query = 'match (v:vt_user) where v.user_id=1 return *'

        view_graph_1depth_2node(query1, query2)


        #------------------------------------------------------------------------------------# 
        st.write(f"**2. 위 고객이 이용했던 서비스를 이용한 다른 사람들은 누가 있었는 지 알아봅니다.**")
        st.write(f"ㅤㅤ- 이들은 '{user_nm}' 고객과 비슷한 관심사를 갖고 있을 가능성이 높다고 할 수 있습니다.")
        
        # 유저 전화번호 입력 시 수행
        if user_telno:
            query1=f"""
    match (v1:vt_cust)-[r1:edg_call]->(v2)<-[r2:edg_call]-(v3:vt_cust)
    where v1.tel_no = '{user_telno}'
    return v1.user_nm, '  ' , v2.bizplc_nm, '  ', v3.user_nm     
            """
            query2=f"""
    match (v1:vt_cust)-[r1:edg_visit]->(v2)<-[r2:edg_visit]-(v3:vt_cust)
    where v1.tel_no = '{user_telno}'
    return v1.user_nm, '  ' , v2.bizplc_nm, '  ', v3.user_nm      
            """
        else:
            query = 'match (v:vt_user) where v.user_id=1 return *'

        view_graph_2depth_2node(query1, query2)

        #------------------------------------------------------------------------------------#
        st.write('**3. 비슷한 행동 패턴을 보인 고객을 직접 연결시켜서 직관적인 관계를 생성합니다.**')
        st.write('ㅤㅤ- 테이블 데이터로만 확인했을 때에는 고객들 사이의 관계가 드러나지 않지만 그래프로 연결하여 관계를 생성합니다.')
        st.write('ㅤㅤ- 행동 패턴이 비슷한 고객들을 연결하고, 유사한 정도를 엣지로 표현합니다.')
        
        # 유저 전화번호 입력 시 수행
        if user_telno:
            query = f"""
    match (v1:vt_cust)-[r]-(v2:vt_cust)
    where id(v1) <> id(v2)
    and v1.tel_no = '{user_telno}'
    and r.type != 'meta'
    return v1.user_nm, v2.user_nm, r.cnt 
            """
            view_graph_1depth(query)

        #------------------------------------------------------------------------------------#
            st.write('**4. 해당 고객들을 그래프 클러스터링 기법을 사용하여 그룹화합니다.**')
            st.write('ㅤㅤ- 그룹 별 특징을 파악하여 각 클러스터에 속하는 고객들의 관심사 메타를 정의합니다.')
            query = f"""
            match (v1:vt_cust)-[r]-(v2:vt_cust)
            where r.type != 'meta'
              and v1.user_nm = '{user_nm}'
            return v1.user_nm, v2.user_nm
            """
            r = agconn.execute_query_withresult(query)
            custs = list(set([i[0] for i in r] + [i[1] for i in r]))

            query = f"""
            match (a:vt_cust)-[r:edg_projection]-(b:vt_cust) 
            where a.user_nm::text in {custs} and b.user_nm::text in {custs} 
              and r.type != 'meta'
              and r.cnt>1 
            return a.user_nm, a.meta_community, b.user_nm, b.meta_community;
            """
            r = agconn.execute_query_withresult(query)
            if r:
                view_community_graph(query)
            else: 
                # 결과가 너무 빈약하면 카운트 조건 해제
                query = f"""
                match (a:vt_cust)-[r:edg_projection]-(b:vt_cust) 
                where a.user_nm::text in {custs} and b.user_nm::text in {custs} 
                  and r.type != 'meta'
                  --and r.cnt>1 
                return a.user_nm, a.meta_community, b.user_nm, b.meta_community;
                """
                view_community_graph(query)
                
            # 예시데이터일 때만 해당 항목 수행 가능(새로운 데이터일 때는 기존에 메타 정의해 놓은 것이 없어서)
            if graph == 'test_carrier':
                st.write("**5. 각 클러스터의 특징을 파악하여 정의하고 '관심사' 노드를 생성하고 연결합니다.**")
                st.write('ㅤㅤ- 나와 관련 있는 다른 고객들의 관심사를 참고하여 추천해 줄 수도 있습니다.')
                
                query = f"""
    match (v1:vt_cust)-[r]->(v2:vt_meta)
    where v1.user_nm in {custs}
    return v2.category, v1.user_nm, '  '
                """
                # query return 순서 : [start_node, end_node, edge_property]
                view_graph_cust_meta(query, user_nm, weighted=0)

    
    # 분석 모듈 수행 함수 END
    #------------------------------------------------------------------------------------#


    
    #------------------------------------------------------------------------------------#
    # Util 화면 출력
    #------------------------------------------------------------------------------------#
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # 사이드바
    add_logo('./images/common/company_logo.png')
    #화면정의

    st.title('통신데이터 그래프 활용')
    st.write('통신데이터 예제를 통해 사용자가 어떤 분석을 수행할 수 있는지 단계별로 수행해 볼 수 있습니다.')
    st.write('   ')
    st.write('-------------------------------------------------------------------')
    
    # IF PERSONALIZE START
    personalize = st.checkbox('👉데이터 직접 업로드해서 분석해보기!👉')
    if personalize:

        def save_upload_file(directory, file):
            import os
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(os.path.join(data_path, file.name), 'wb') as f:
                f.write(file.getbuffer())
            return st.success('Save file : {} in {}'.format(file.name, directory))

        text="""
ㅤㅤ데이터를 직접 업로드해서 그래프를 구성합니다.\n
ㅤㅤ그래프 이름과 그래프에 넣은 데이터를 지정된 형식으로 불러와야합니다.\n
ㅤㅤ구성한 그래프로 확인하고자 하는 내용을 중심으로 노드와 엣지를 정의해야 합니다.\n
ㅤㅤ우리는 고객과 상점, 서비스 간의 관계를 중심으로 확인하기 때문에 다음과 같이 모델링 할 수 있습니다.\n
ㅤㅤ우선적으로 **1.고객의 정보를 노드로 적재**한 후 **2.상점과의 전화관계**, **3.서비스의 방문관계**를 적재합니다.\n
ㅤㅤ입력 데이터 별 그림에 해당하는 정보를 가진 열 이름을 명시하여 그래프를 만들어보세요!
        """
        st.write(text)
        image = Image.open('./images/2_telecommunication/modeling_example.png')
        st.image(image, caption='통신데이터 전체 그래프 모델')

        graph_name = st.text_input('그래프 이름을 입력해주세요.', 'mini_test_graph')
        st.write("👉 아래의 버튼으로 '" + graph_name + "' 그래프를 새롭게 만들게 됩니다! (같은 이름의 그래프가 기존에 존재한다면 리셋됩니다.)")
        if st.button('CREATE GRAPH :)'):
            store_personalize_creategraph(graph_name)
        
        uploaded_file = st.file_uploader("그래프로 만들고자 하는 데이터 파일을 불러오세요.", type=(["tsv","csv","txt","tab","xlsx","xls"]))
        st.write("*고객정보, 고객-상점정보, 고객-서비스정보에 대해 순차적으로 적재해주시기 바랍니다.*")
        if uploaded_file is None:
            st.session_state["upload_state"] = "Upload a file first!"
        else:
            bytes_data = uploaded_file.getvalue()
            save_upload_file(data_path, uploaded_file)
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe.head(10))
            agconn.load_dataframe(dataframe)

            st.subheader('우선 고객 정보를 추가해보세요')
            custid_col = st.selectbox(
                '데이터에서 고객의 KEY 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            custnm_col = st.selectbox(
                '데이터에서 고객의 부가적인 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            if st.button('SET CUST INFO :)'):
                store_personalize_cust(graph_name,dataframe,custid_col,custnm_col)
            st.subheader('다음으로 고객-상점 관계를 연결해보세요.')
            custid_cdr_col = st.selectbox(
                '전화이력데이터에서 고객의 KEY 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            shop_col = st.selectbox(
                '상점 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            if st.button('SET CUST-SHOP RELATION :)'):
                store_personalize_usershop(graph_name,dataframe,custid_cdr_col,shop_col)
            st.subheader('마지막으로 고객-서비스 관계를 만들어보세요.')
            custid_sgi_col = st.selectbox(
                '서비스방문이력데이터에서 고객의 KEY 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            service_col = st.selectbox(
                '서비스 정보를 포함하는 컬럼을 선택하세요.',
                ['컬럼을 선택하세요'] + list(dataframe.columns))
            if st.button('SET CUST-SERVICE RELATION :)'):
                store_personalize_userservice(graph_name,dataframe,custid_sgi_col,service_col)
                st.write(graph_name + ' 환경에서 그래프가 준비되었습니다.')
        st.write('-------------------------------------------------------------------')
        graph_name = ''
        util_env(graph_name)
    # IF PERSONALIZE END
    else:
        graph_name = 'test_carrier'
        util_env(graph_name)

# util END
#-----------------------------------------------------------------------------------------------------------------------------------#            


#-----------------------------------------------------------------------------------------------------------------------------------#
# 상단 메뉴바 관련
#-----------------------------------------------------------------------------------------------------------------------------------#
selected_menu = option_menu(None, 
                        ["통신 데이터 튜토리얼 소개", "분석 시나리오", "그래프 활용"], 
                        icons = ['house', "cursor"], 
                        menu_icon = "cast", 
                        default_index = 0, 
                        orientation = "horizontal"
                       )

if selected_menu == '통신 데이터 튜토리얼 소개':
    intro()
elif selected_menu == "분석 시나리오":
    scenario()
elif selected_menu == '그래프 활용':
    util()


