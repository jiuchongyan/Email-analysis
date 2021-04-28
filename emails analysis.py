__author__ = 'samsung'
# ��PageRank�ھ�ϣ�����ʼ��е���Ҫ�����ϵ
import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

# ���ݼ���
emails = pd.read_csv("./Emails.csv")
# ��ȡ�����ļ�
file = pd.read_csv("./Aliases.csv")
aliases = {}
for index, row in file.iterrows():
    aliases[row['Alias']] = row['PersonId']
# ��ȡ�����ļ�
file = pd.read_csv("./Persons.csv")
persons = {}
for index, row in file.iterrows():
    persons[row['Id']] = row['Name']

# ��Ա�������ת��
def unify_name(name):
    # ����ͳһСд
    name = str(name).lower()
    # ȥ��, ��@���������
    name = name.replace(",","").split("@")[0]
    # ����ת��
    if name in aliases.keys():
        return persons[aliases[name]]
    return name
# ������ͼ
def show_graph(graph, type = 'spring_layout'):
    if type == 'spring_layout':
        # ʹ��Spring Layout���֣��������ķ���״
        positions=nx.spring_layout(graph)
    if type == 'circular_layout':
        # ʹ��Circular Layout���֣���һ��Բ���Ͼ��ȷֲ�
        positions=nx.circular_layout(graph)

    # ��������ͼ�еĽڵ��С����С��pagerankֵ��أ���Ϊpagerankֵ��С������Ҫ*20000
    nodesize = [x['pagerank']*20000 for v,x in graph.nodes(data=True)]
    # ��������ͼ�еı߳���
    edgesize = [np.sqrt(e[2]['weight']) for e in graph.edges(data=True)]
    # ���ƽڵ�
    nx.draw_networkx_nodes(graph, positions, node_size=nodesize, alpha=0.4)
    # ���Ʊ�
    #nx.draw_networkx_edges(graph, positions, edge_size=edgesize, alpha=0.2)
    nx.draw_networkx_edges(graph, positions, alpha=0.2)
    # ���ƽڵ��label
    nx.draw_networkx_labels(graph, positions, font_size=10)
    # ���ϣ�����ʼ��е����������ϵͼ
    plt.show()

# ���ļ��˺��ռ��˵��������й淶��
emails.MetadataFrom = emails.MetadataFrom.apply(unify_name)
emails.MetadataTo = emails.MetadataTo.apply(unify_name)

# ���ñߵ�Ȩ�ص��ڷ��ʼ��Ĵ���
edges_weights_temp = defaultdict(list)
for row in zip(emails.MetadataFrom, emails.MetadataTo, emails.RawText):
    temp = (row[0], row[1])
    if temp not in edges_weights_temp:
        edges_weights_temp[temp] = 1
    else:
        edges_weights_temp[temp] = edges_weights_temp[temp] + 1

print(edges_weights_temp)
print('-'*100)
# ת����ʽ (from, to), weight => from, to, weight
edges_weights = [(key[0], key[1], val) for key, val in edges_weights_temp.items()]

# ����һ������ͼ
graph = nx.DiGraph()
# ��������ͼ�е�·����Ȩ��(from, to, weight)
graph.add_weighted_edges_from(edges_weights)
# ����ÿ���ڵ㣨�ˣ���PRֵ������Ϊ�ڵ��pagerank����
pagerank = nx.pagerank(graph)
# ��ȡÿ���ڵ��pagerank��ֵ
pagerank_list = {node: rank for node, rank in pagerank.items()}
# ��pagerank��ֵ��Ϊ�ڵ������
nx.set_node_attributes(graph, name = 'pagerank', values=pagerank_list)
# ������ͼ
show_graph(graph)

# ��������ͼ�׽��о���
# ����PRֵ����ֵ��ɸѡ������ֵ����Ҫ���Ľڵ�
pagerank_threshold = 0.005
# ����һ�ݼ���õ�����ͼ
small_graph = graph.copy()
# ����PRֵС��pagerank_threshold�Ľڵ�
for n, p_rank in graph.nodes(data=True):
    if p_rank['pagerank'] < pagerank_threshold:
        small_graph.remove_node(n)
# ������ͼ
show_graph(small_graph, 'circular_layout')
