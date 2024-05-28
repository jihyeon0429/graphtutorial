import pandas as pd
import psycopg2 as pg2
from datetime import datetime as dt
from sqlalchemy import create_engine
from tqdm import tqdm

#20230109 : 관계 추가 시 reindex쿼리 실행하도록 sql구문 실행 추가

class AgensConnector:
    def __init__(self, host, port, database, user, password, graph_path = None, autocommit=True):
        self.db_params = self.agconfig(host, port, database, user, password)
        self.graph_path = graph_path
        self.conn = pg2.connect(**self.db_params)
        self.cur = self.conn.cursor()
        self.conn.autocommit = autocommit
        print('Successful connection to agensgraph!')
        print('connection_info')
        print(self.db_params)

    def __del__(self):
        self.close_agens()
        print('close the agensgraph connection!')

    def agconfig(self, host, port, database, user, password):
        db_config = {"host":host, "port":port, "database":database, "user":user, "password":password}
        return db_config

#     def create_graph(self, graph_path):
#         self.graph_path = graph_path
#         check_graph = f"select nspname from pg_catalog.pg_namespace where nspname='{graph_path}';"
#         self.cur.execute(check_graph)
#         rows = self.cur.fetchall()
#         if len(rows)>=1:
#             print('Set '+graph_path+'.')
#             return self.set_graph(graph_path)
#         else:
#             init_graph = f'CREATE GRAPH {graph_path}; SET GRAPH_PATH = {graph_path};'
#             print('Create and set '+graph_path+'.')
#             return self.cur.execute(init_graph)            

        
    def create_graph(self, graph_path):
        init_graph = f'CREATE GRAPH {graph_path}; SET GRAPH_PATH = {graph_path};'
        print('Create and set '+graph_path+'.')
        return self.cur.execute(init_graph) 

        
    def drop_graph(self, graph_path):
        self.graph_path = graph_path
        init_graph = f'DROP GRAPH IF EXISTS {graph_path} CASCADE;'
        print('Drop graph ',graph_path,'.')
        return self.cur.execute(init_graph)

    def set_graph(self,graph_path):
        self.graph_path = graph_path
        if not graph_path:
            print(graph_path+' is not exsists.')
            return
        return self.cur.execute("SET graph_path="+graph_path+";")

    #Fill '' in dataframe nan value
    def load_dataframe(self, df):
        self.df = df.fillna('')
        print('Load data')
        return

    def close_agens(self):
        if not self.conn:
            return
        if not self.conn.closed:
            self.conn.close()

    def commit_agens(self):
        if not self.conn:
            return
        self.conn.commit() 
#------------------------------------------------------------------------#
    def execute_query_withresult(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
    
    def execute_query(self, query):
        self.cur.execute(query)
        
#------------------------------------------------------------------------#
    
    def query_exe(self,query,graph_path=None,iterable = None,autocommit=True):
        try:    
            self.query = query
            self.iterable=iterable
            conn = self.conn
            cur = self.cur
            conn.autocommit = autocommit
            if graph_path:
                set_graph = self.set_graph(graph_path)
                print(cur.statusmessage)
            if iterable: 
                cur.executemany(self.query,self.iterable)
                print(cur.statusmessage)
            else:
                cur.execute(self.query)
                print(cur.statusmessage)
            return
        except (Exception, pg2.DatabaseError) as error:
            print('[%s][ERR|query_exe] %s' % (str(dt.now()), error))
            print(query)
            conn.rollback()

    # Load the data frame as a table
    def pandas_exe(self, df, tb_name, db_schema ='public', exists = 'replace'):
        db_params=self.db_params
        self.tb_name = tb_name
        self.db_schema = db_schema
        self.exists = exists
        engine_info = db_params['user']+':'+ db_params['password']+'@'+ db_params['host']+':'+ db_params['port']+'/'+ db_params['database']
        engine = create_engine('postgresql://' + engine_info)
        df.to_sql(  
                    name = self.tb_name,
                    con = engine,
                    schema = self.db_schema,
                    if_exists = self.exists,
                    index = False
          ) 
        return
    
    # Returns 1 if the element of col_li exists as label_name in the graph
    def check_label(self, graph_path , col_li):
        query = f"""select tablename from pg_tables
                where schemaname not in ('pg_catalog', 'informationschama') and schemaname='{graph_path}';"""
        self.cur.execute(query)
        rows = self.cur.fetchall()
        res=set()
        col_li = set(col_li)
        for row in rows:
            res.add(list(row)[0])
        if res==res|col_li:
            return 1
        else:
            return 0
        return

    # Return b if b
    def set_value(self, a, b=None):
        if b:
            return b
        else:
            return a
    
    # Convert column name of df to set_properties_nm specified
    def rename_pdf(self, df, properties, set_properties_nm = None):
        if set_properties_nm:
            tmp = dict(zip(vt_properties, set_properties_nm))
            tmp_df.rename(columns = tmp, inplace=True)
            return tmp_df
        else:
            return df
    

#     {컬럼:프로퍼티명} 
    # col_nm : str, label_name : str , vt_properties : list , set_properties_nm : dict
    def create_vertex(self, col_nm, label_name=None, vt_properties=None, set_properties_nm=None):
        graph_path = self.graph_path
        df = self.df
        vt_nm = self.set_value(col_nm, b=label_name)
        res = self.check_label(graph_path , [vt_nm])
        flag = 0
        stat = 'create'
        if res == 1:
            print(f'Vertex label {vt_nm} is already exsists.\n')
            flag = input('1.Drop cascade and create vertex\n2.Add vertex\n3.Exit function : ')
            flag = int(flag)
            if flag==1:
                self.set_graph(graph_path)
                drop_vt = f'drop vlabel {vt_nm} cascade;'
                self.query_exe(drop_vt)
                res=0
            elif flag==2:
                res=0
                stat = 'merge'
            else:
                print('Exit function.\n')
                return
        # load_vertex
        if res==0:
            self.set_graph(graph_path)
            tmp_tb_nm = 'tmp_tb'
            if vt_properties:
                tmp = [col_nm]+vt_properties
                tmp_df = df[tmp].drop_duplicates().reset_index(drop=True)
                if set_properties_nm:
                    tmp_df.rename(columns = set_properties_nm, inplace=True)
            else:
                tmp = [col_nm]
                tmp_df = df[tmp].drop_duplicates().reset_index(drop=True)
                if set_properties_nm:
                    tmp_df.rename(columns = set_properties_nm, inplace=True)
            self.pandas_exe(tmp_df,tmp_tb_nm)
            if flag<=1:
                create_vt = f'create vlabel if not exists {vt_nm};'
                self.query_exe(create_vt)
                load_vt = f'load from {tmp_tb_nm} as tb {stat} (a:{vt_nm}) set properties(a) = row_to_json(tb);'
                self.query_exe(load_vt)
            elif flag==2:
                set_properties=[]
                for i in range(len(tmp_df.columns)):
                    set_properties.append(tmp_df.columns[i]+" : tb."+tmp_df.columns[i])
                set_properties = ', '.join(set_properties)
                load_vt = f'load from {tmp_tb_nm} as tb {stat} (a:{vt_nm}{{{set_properties}}});'
                self.query_exe(load_vt)
            drop_table = f'drop table {tmp_tb_nm};'
            self.query_exe(drop_table)
            return
        else:
            return

    # st_col_nm : str , ed_col_nm : str , edg_label_nm : str , st_label_name : str , st_property_nm : str, ed_label_name : str, ed_property_nm : str, 
    # edg_properties : list , set_properties_nm : dict {column_nm : setting_column_nm}
    def create_edge(self, st_col_nm, ed_col_nm, edg_label_nm, st_label_name = None, st_property_name = None, ed_label_name = None, ed_property_name = None, edg_properties=None, set_properties_nm=None, set_flag=None):
        # Return 1 if input_dict has input_val
        def check_keys(input_dict, input_val):
            if input_val in input_dict.keys():
                return 1
            else:
                return 0
        graph_path = self.graph_path
        df = self.df
        st_vt_nm = self.set_value(st_col_nm, b=st_label_name)
        st_pt_nm = self.set_value(st_col_nm, b=st_property_name)
        ed_vt_nm = self.set_value(ed_col_nm, b=ed_label_name)
        ed_pt_nm = self.set_value(ed_col_nm, b=ed_property_name)
        flag = self.set_value(0,b=set_flag)
        stat = 'create'
        res_vt = self.check_label(graph_path , [st_vt_nm, ed_vt_nm])
        res_edg = self.check_label(graph_path , [edg_label_nm])
        if res_vt == 0:
            print('vertex_label is not exsists!\n')
            return
        else:
            # If edg_label exists
            if res_edg == 1:
                print(f'Edge label {edg_label_nm} is already exsists.\n')
                if flag==0:
                    flag = input('1.Drop cascade and create edge\n2.Add edge\n3.Exit function : ')
                    flag = int(flag)
                if flag==1:
                    self.set_graph(graph_path)
                    drop_edg = f'drop elabel {edg_label_nm} cascade;'
                    self.query_exe(drop_edg)
                    res_edg = 0
                elif flag==2:
                    res_edg = 0
                    stat = 'merge'
                else:
                    print('Exit function.\n')
                    return
            if res_edg == 0:
                # load_edge
                self.set_graph(graph_path)
                if flag<=1:
                    create_edg = f'create elabel if not exists {edg_label_nm};'
                    self.query_exe(create_edg)

                if edg_properties:
                    tmp = [st_col_nm, ed_col_nm] + edg_properties
                    tmp = df[tmp].drop_duplicates().reset_index(drop=True)
                    tmp_df = tmp.iloc[:,2:]
                    # df rename
                    if set_properties_nm:
                        tmp_df.rename(columns = set_properties_nm, inplace=True)
                        if check_keys(set_properties_nm, st_col_nm):
                            st_col_nm = set_properties_nm[st_col_nm]
                        if check_keys(set_properties_nm, ed_col_nm):
                            ed_col_nm = set_properties_nm[ed_col_nm]
                    tmp_df = pd.concat([tmp.iloc[:,:2],tmp_df],axis=1)
                    tmp_tb_nm = 'tmp_tb'
                    self.pandas_exe(tmp_df,tmp_tb_nm)
                    set_properties=[]
                    for i in range(2,len(tmp_df.columns)):
                        set_properties.append(tmp_df.columns[i]+" : tb."+tmp_df.columns[i])
                    set_properties = ', '.join(set_properties)
                    load_edge = f'''
                                    load from {tmp_tb_nm} as tb 
                                    match(a:{st_vt_nm}),(b:{ed_vt_nm}) 
                                    where a.{st_pt_nm} = tb.{st_col_nm} and b.{ed_pt_nm} = tb.{ed_col_nm}    
                                    {stat}(a)-[r:{edg_label_nm}{{{set_properties}}}]->(b);
                                '''     
                else:
                    tmp = [st_col_nm, ed_col_nm]
                    tmp_df = df[tmp].drop_duplicates().reset_index(drop=True)
                    if set_properties_nm:
                        tmp_df.rename(columns = set_properties_nm, inplace=True)
                        if check_keys(set_properties_nm, st_col_nm):
                            st_col_nm = set_properties_nm[st_col_nm]
                        if check_keys(set_properties_nm, ed_col_nm):
                            ed_col_nm = set_properties_nm[ed_col_nm]
                    tmp_tb_nm = 'tmp_tb'
                    self.pandas_exe(tmp_df,tmp_tb_nm)
                    load_edge = f'''
                                    load from {tmp_tb_nm} as tb 
                                    match(a:{st_vt_nm}),(b:{ed_vt_nm}) 
                                    where a.{st_pt_nm} = tb.{st_col_nm} and b.{ed_pt_nm} = tb.{ed_col_nm}    
                                    {stat}(a)-[r:{edg_label_nm}]->(b);
                                '''            
                drop_table = f'drop table {tmp_tb_nm};'
                self.query_exe(load_edge)
                self.query_exe(drop_table)
                reindex_query=f"REINDEX SCHEMA {graph_path};"
                self.query_exe(reindex_query)
                return
            else:
                return