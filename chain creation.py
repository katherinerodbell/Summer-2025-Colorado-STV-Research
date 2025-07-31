from gerrychain import Graph, Partition
from gerrychain.updaters import Tally, cut_edges
import shapely .geos
import geopandas as gpd
import maup
from maup import doctor
import random
from gerrychain import MarkovChain
from gerrychain.constraints import single_flip_contiguous
from gerrychain.proposals import propose_random_flip
from gerrychain.accept import always_accept
from gerrychain import constraints
from functools import partial
from gerrychain.proposals import recom
from gerrychain.constraints import contiguous
from gerrychain import Election
from gerrychain.constraints import contiguous
import pandas

#repairs data frame
data_frame = gpd.read_file("C:\\Users\\i_pixler2023\\Desktop\\2021_Approved_House_Plan_w_Final_Adjustments\\2021_Approved_House_Plan_w_Final_Adjustments.shp")
repaired_df = maup.smart_repair(data_frame)
maup.doctor(repaired_df)
repaired_df.plot(cmap = "tab20", alpha=0.7)

#creates dual graph
dual_graph = Graph.from_geodataframe(repaired_df)

#reads election file

precinct_data = open("C:\\Users\\i_pixler2023\\Desktop\\25580_table.csv", 'r')
precinct_data_list = precinct_data.readlines()

clean_list = []
precinct_dict = {}
single_dem_dict = {}
single_rep_dict = {}

for i in precinct_data_list:
    if i[0] == 'P':
        clean_list.append(i)

for i in clean_list:
    split_string = i.split(',')
    house_district = split_string[1][3:5]
    precinct_dict[split_string[1]]=[house_district,split_string[2],split_string[3]]
    
for key in precinct_dict:
    if precinct_dict[key][0] not in single_dem_dict:
        single_dem_dict[precinct_dict[key][0]] = int(precinct_dict[key][1])
    else:
        single_dem_dict[precinct_dict[key][0]] += int(precinct_dict[key][1])

for key in precinct_dict:
    if precinct_dict[key][0] not in single_rep_dict:
        single_rep_dict[precinct_dict[key][0]] = int(precinct_dict[key][2])
    else:
        single_rep_dict[precinct_dict[key][0]] += int(precinct_dict[key][2])

#updates nodes with election data

i=1

for key in dual_graph.nodes:
    i = str(i)
    if len(i)<2:
        new_key = '0'+i
    else:
        new_key = i
    str(new_key)
    dual_graph.nodes[key]['dem'] = single_dem_dict[new_key]
    dual_graph.nodes[key]['rep'] = single_rep_dict[new_key]
    i = int(i)
    i+=1
    
#add election

election = Election("AG22", {"Dem": "dem", "Rep": "rep"})

#sets up inital partition

assignment_dict = {0:8, 1:8, 2:8, 3:9, 4:9, 5:9, 6:11, 7:9, 8:8, 9:12, 10:12, 11:12, 12:2, 13:5, 14:4, 15:4, 16:4, 17:4, 18:12, 19:5, 20:4, 21:5, 22:10, 23:10, 24:6, 25:2, 26:10, 27:6, 28:10, 29:8, 30:11, 31:11, 32:11, 33:11, 34:10, 35:7, 36:6, 37:6, 38:5, 39:7, 40:7, 41:9, 42:6, 43:7, 44:5, 45:1, 46:3, 47:3, 48:12, 49:3, 50:13, 51:13, 52:13, 53:2, 54:2, 55:3, 56:2, 57:1, 58:1, 59:1, 60:7, 61:1, 62:3, 63:13, 64:13}
my_updaters = {
        "population": Tally("population", alias="population"),
        "dem_votes": Tally("dem", alias="dem_votes"),
        "rep_votes": Tally("rep", alias="rep_votes"),
        "cut_edges": cut_edges,
        "AG22": election
    }

initial_partition = Partition(
    dual_graph,
    assignment = assignment_dict,
    updaters=my_updaters
)

#add constraints

def cut_edges_length(p):
  return len(p["cut_edges"])

compactness_bound = constraints.UpperBound(
  cut_edges_length,
  1.5*len(initial_partition["cut_edges"]) #maybe try 1.5 or smaller
)

pop_constraint = constraints.within_percent_of_ideal_population(initial_partition, 0.02)

#makes proposal

ideal_population = sum(initial_partition["population"].values()) / len(initial_partition)

proposal = partial(
    recom,
    pop_col="population",
    pop_target=ideal_population,
    epsilon=0.02, #% off from target pop
    node_repeats=2 #how many times you try...
)

#makes chain

chain = MarkovChain(
    proposal=proposal,
    constraints=[contiguous, pop_constraint, compactness_bound],
    accept=always_accept,
    initial_state=initial_partition,
    total_steps=10000
)

#runs chain

steps = 0
dem_list = []
rep_list = []

for (i, partition) in enumerate(chain):
    steps = str(steps)
    dem_list.append('step')
    dem_list.append(steps)
    rep_list.append('step')
    rep_list.append(steps)
    dem_list.append(f"Dem pop: {partition['dem_votes']}")
    rep_list.append(f"Rep pop: {partition['rep_votes']}")
    steps = int(steps)
    steps += 1
    
#cleans results list

clean_dem_list = []
for i in dem_list:
    clean_i = i.replace(" ","").replace("{","").replace("}","")
    clean_dem_list.append(clean_i)
    
clean_rep_list = []
for i in rep_list:
    clean_i = i.replace(" ","").replace("{","").replace("}","")
    clean_rep_list.append(clean_i)
        
#writes into csv

import csv

dem_write = open('C:\\Users\\i_pixler2023\\Desktop\\dem_results.csv', 'w')
dem_write.write(str(clean_dem_list))

rep_write = open('C:\\Users\\i_pixler2023\\Desktop\\rep_results.csv', 'w')
rep_write.write(str(clean_rep_list))

