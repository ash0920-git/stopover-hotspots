clc ;
clear;
s = xlsread('wl.xlsx','wl','A1:A24245'); 
t = xlsread('wl.xlsx','wl','B1:B24245'); 
%names = {'1', '2', '3', '4', '5', '6'};
G = digraph(s,t,[]);
plot(G)
pg_ranks = centrality(G,'pagerank')
G.Nodes.PageRank = pg_ranks;
G.Nodes