import csv
import json
import time
import datetime
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime as dt

def create_graph():
	interval = 5 # time between exams
	graph = []
	graph_json = {}
	with open('exam_data.csv') as File1:
		reader1 = csv.DictReader(File1, delimiter=';')
		path = 0
		pathlists = [[] for j in range(numpaths+1)]
		for row1 in reader1:
			start1  = time.mktime(datetime.datetime.strptime(row1['start'], "%d/%m/%Y %H:%M").timetuple())
			finish1 = time.mktime(datetime.datetime.strptime(row1['finish'], "%d/%m/%Y %H:%M").timetuple())
			grade1 = float(row1['grade'])
			time1 = int(row1['minutes'])
			with open('exam_data.csv') as File2:
				reader2 = csv.DictReader(File2, delimiter=';')
				for row2 in reader2:
					start2  = time.mktime(datetime.datetime.strptime(row2['start'], "%d/%m/%Y %H:%M").timetuple())
					finish2  = time.mktime(datetime.datetime.strptime(row2['finish'], "%d/%m/%Y %H:%M").timetuple())
					grade2 = float(row2['grade'])
					time2 = int(row2['minutes'])

					if finish1 <= start2 and start2 <= finish1 + (60*interval) and (grade1-1.25 <= grade2) and time1 > time2:
						graph.append((row1['user'],row2['user']))
						if (graph_json.get(row1['user'])):
							graph_json[row1['user']]['adjacent'].append(row2['user'])
							path2 = graph_json[row1['user']]['path']	
						else:
							path = path+1		
							path2 = path	
							graph_json[row1['user']] = {'start': row1['start'], 'finish': row1['finish'], 'time': time1, 'grade': grade1, 'path': path, 'adjacent': [row2['user']]}
						if (not(graph_json.get(row2['user']))):
							graph_json[row2['user']] = {'start': row2['start'], 'finish': row2['finish'], 'time': time2, 'grade': grade2, 'path': path2, 'adjacent': []}
						
	with open('cheat.json', 'w') as outfile:
		json.dump(graph_json, outfile)

	timeline_graph(graph_json, path)

	return graph

def timeline_graph(jg, numpaths):
	init_exam = "22/05/2020 11:00"
	end_exam = "22/05/2020 14:00"

	plt.figure(1, figsize=(11, 7))
	plt.clf()
	
	count = 0
	for user in jg:
		exam_student = time.mktime(datetime.datetime.strptime(jg[user]['start'], "%d/%m/%Y %H:%M").timetuple())
		exam_start = time.mktime(datetime.datetime.strptime(init_exam, "%d/%m/%Y %H:%M").timetuple())
		exam_finish = time.mktime(datetime.datetime.strptime(end_exam, "%d/%m/%Y %H:%M").timetuple())
		exam_duration = exam_finish - exam_start
		count = count + 7
		x = 0 + ((exam_student - exam_start)/exam_duration)
		y = 0 + (count%100)/100
		jg[user]['position'] = (float(x), float(y))
		plt.text(x,y,user)
	
	g = []

	pathlists = [[] for j in range(numpaths+1)]
	
	for student in jg:
		pathlists[jg[student]['path']].append(student)

	for path in pathlists:	
		G = nx.Graph()
		i = 0
		G.pos = {}  # location
		G.pop = {}  # size
		last = None
		for student in path:	
			if jg[student]['path'] < 100:	
				x, y = jg[student]['position']
				p = float(jg[student]['grade'])
				r = "A"
				n = jg[student]['path']
				G.pos[i] = (float(x), float(y))
				G.pop[i] = float(p)
				if last is None:
					last = i
				else:
					G.add_edge(i, last, **{r: int(n)})
					last = i
				i = i + 1
		g.append(G)

	colors = ["b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", 
	"k", "w", "b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", 
	"k", "w", "b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", "k", "w",
	"b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", "k", "w",
	"b", "g", "r", "c", "m", "y", "k", "w", "b", "g", "r", "c", "m", "y", "k", "w"]
	for G in g:
		c = colors.pop(0)
		node_size = [float(G.pop[n] / 0.03) for n in G]		
		nx.draw_networkx_edges(G, G.pos, edge_color=c, width=4, alpha=0.5)
		nx.draw_networkx_nodes(G, G.pos, node_size=node_size, node_color=c, alpha=0.5)
		nx.draw_networkx_nodes(G, G.pos, node_size=5, node_color="k")

	plt.show()
			

def process():
	# Code for printing to a file 
	interval = 5 # time between exams
	path = 0 # different paths
	simfile = open('result.csv', 'w') 
	nodesfile = open('nodes.csv', 'w')
	with open('exam_data.csv') as File1:
		reader1 = csv.DictReader(File1, delimiter=';')
		print("path;source;start;finish;minutes;weight;target;Interval", file = simfile)
		print("Id;Label;Category", file = nodesfile)
		print("INIT;INIT;G0", file = nodesfile)
		print("END;END;G0", file = nodesfile)
		#print("name,parent", file = simfile)
		for row1 in reader1:
			start1  = time.mktime(datetime.datetime.strptime(row1['start'], "%d/%m/%Y %H:%M").timetuple())
			finish1 = time.mktime(datetime.datetime.strptime(row1['finish'], "%d/%m/%Y %H:%M").timetuple())
			grade1 = float(row1['grade'])
			time1 = int(row1['minutes'])
			with open('../sources/exam_data.csv') as File2:
				reader2 = csv.DictReader(File2, delimiter=';')
				for row2 in reader2:
					start2  = time.mktime(datetime.datetime.strptime(row2['start'], "%d/%m/%Y %H:%M").timetuple())
					finish2  = time.mktime(datetime.datetime.strptime(row2['finish'], "%d/%m/%Y %H:%M").timetuple())
					grade2 = float(row2['grade'])
					time2 = int(row2['minutes'])

					if finish1 <= start2 and start2 <= finish1 + (60*interval) and (grade1-1.25 <= grade2) and time1 > time2:
						
						with open('../sources/exam_data.csv') as File3:
							reader3 = csv.DictReader(File3, delimiter=';')
							for row3 in reader3:
								start3  = time.mktime(datetime.datetime.strptime(row3['start'], "%d/%m/%Y %H:%M").timetuple())
								finish3  = time.mktime(datetime.datetime.strptime(row3['finish'], "%d/%m/%Y %H:%M").timetuple())
								grade3 = float(row3['grade'])
								time3 = int(row3['minutes'])

								if finish2 <= start3 and start3 <= finish2 + (60*interval) and (grade2-1.25 <= grade3) and time2 > time3:
						
									with open('../sources/exam_data.csv') as File4:
										reader4 = csv.DictReader(File4, delimiter=';')
										for row4 in reader4:
											start4  = time.mktime(datetime.datetime.strptime(row4['start'], "%d/%m/%Y %H:%M").timetuple())
											finish4  = time.mktime(datetime.datetime.strptime(row4['finish'], "%d/%m/%Y %H:%M").timetuple())
											grade4 = float(row4['grade'])
											time4 = int(row4['minutes'])

											if finish3 <= start4 and start4 <= finish3 + (60*interval) and (grade3-1.25 <= grade4) and time3 > time4:
						
												with open('../sources/exam_data.csv') as File5:
													reader5 = csv.DictReader(File5, delimiter=';')
													for row5 in reader5:
														start5  = time.mktime(datetime.datetime.strptime(row5['start'], "%d/%m/%Y %H:%M").timetuple())
														finish5  = time.mktime(datetime.datetime.strptime(row5['finish'], "%d/%m/%Y %H:%M").timetuple())
														grade5 = float(row5['grade'])
														time5 = int(row5['minutes'])

														if finish4 <= start5 and start5 <= finish4 + (60*interval) and (grade4-1.25 <= grade5) and time4 > time5:
						
															with open('../sources/exam_data.csv') as File6:
																reader6 = csv.DictReader(File6, delimiter=';')
																for row6 in reader6:
																	start6  = time.mktime(datetime.datetime.strptime(row6['start'], "%d/%m/%Y %H:%M").timetuple())
																	finish6  = time.mktime(datetime.datetime.strptime(row6['finish'], "%d/%m/%Y %H:%M").timetuple())
																	grade6 = float(row6['grade'])
																	time6 = int(row6['minutes'])
																	
																	if finish5 <= start6 and start6 <= finish5 + (60*interval) and (grade5-1.25 <= grade6) and time5 > time6:
						
																		path = path + 1

																		interv = 1
																		# print(row1['user'] + "," + "null", file = simfile)
																		# print(row2['user'] + "," + row1['user'], file = simfile)
																		# print(row3['user'] + "," + row2['user'], file = simfile)
																		# print(row4['user'] + "," + row3['user'], file = simfile)
																		# print(row5['user'] + "," + row4['user'], file = simfile)
																		# print(row6['user'] + "," + row5['user'], file = simfile)
																		
																		print(str(path) + ";INIT;" + str(dt.fromtimestamp(start1)) + ";" + str(dt.fromtimestamp(finish1))  + ";" + row1['minutes'] + ";1;" + row1['user'] + ";" + str(interv), file = simfile)
																		interv = interv + 1
																		print(str(path) + ";" + row1['user'] + ";" + str(dt.fromtimestamp(start1)) + ";" + str(dt.fromtimestamp(finish1))  + ";" + row1['minutes'] + ";" + row1['grade'] + ";" + row2['user'] + ";" + str(interv), file = simfile)					
																		interv = interv + 1
																		print(str(path) + ";" + row2['user'] + ";" + str(dt.fromtimestamp(start2)) + ";" + str(dt.fromtimestamp(finish2))  + ";" + row2['minutes'] + ";" + row2['grade'] + ";" + row3['user'] + ";" + str(interv), file = simfile)
																		interv = interv + 1
																		print(str(path) + ";" + row3['user'] + ";" + str(dt.fromtimestamp(start3)) + ";" + str(dt.fromtimestamp(finish3))  + ";" + row3['minutes'] + ";" + row3['grade'] + ";" + row4['user'] + ";" + str(interv), file = simfile)					
																		interv = interv + 1
																		print(str(path) + ";" + row4['user'] + ";" + str(dt.fromtimestamp(start4)) + ";" + str(dt.fromtimestamp(finish4))  + ";" + row4['minutes'] + ";" + row4['grade'] + ";" + row5['user'] + ";" + str(interv), file = simfile)					
																		interv = interv + 1
																		print(str(path) + ";" + row5['user'] + ";" + str(dt.fromtimestamp(start5)) + ";" + str(dt.fromtimestamp(finish5))  + ";" + row5['minutes'] + ";" + row5['grade'] + ";" + row6['user'] + ";" + str(interv), file = simfile)					
																		interv = interv + 1
																		print(str(path) + ";" + row6['user'] + ";" + str(dt.fromtimestamp(start6)) + ";" + str(dt.fromtimestamp(finish6))  + ";" + row6['minutes'] + ";" + row6['grade'] + ";" + "END" + ";" + str(interv), file = simfile)		

																		print(row1['user'] + ";" + row1['user'] + ";" + row1['group'], file=nodesfile)
																		print(row2['user'] + ";" + row2['user'] + ";" + row2['group'], file=nodesfile)
																		print(row3['user'] + ";" + row3['user'] + ";" + row3['group'], file=nodesfile)
																		print(row4['user'] + ";" + row4['user'] + ";" + row4['group'], file=nodesfile)
																		print(row5['user'] + ";" + row5['user'] + ";" + row5['group'], file=nodesfile)
																		print(row6['user'] + ";" + row6['user'] + ";" + row6['group'], file=nodesfile)			
																		

					

def draw_graph(graph):

	# extract nodes from graph
	nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

	# create networkx graph
	G=nx.Graph()

	# add nodes
	for node in nodes:
		G.add_node(node)

	# add edges
	for edge in graph:
		G.add_edge(edge[0], edge[1])

	# draw graph
	pos = nx.spring_layout(G,2)
	nx.draw(G, pos)

	# show graph
	plt.show()

# draw example
# graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20),(20,21)]
draw_graph(create_graph())

#timeline_graph()