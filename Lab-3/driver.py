from display_cycles import *
from transactions_graph import *
import pydotplus
import cv2

# helper functions to read the input file
def transaction_id(op):
    index = op.find("(")
    t = int(op[1:index])
    return t

def op_type(op):
    d = {'R':"read", 'W':"write"}
    t = str(op[0]).upper()
    return d[t]

def data_item(op):
    index1 = op.find("(")
    index2 = op.find(")")
    return str(op[index1+1:index2])

def display_schedule(t,d,schedule):
    print("\n\n#################### SCHEDULE ######################\n")
    for i in range(t):
        print("T"+str(i+1), end="\t\t\t\t")
    print()
    for i in schedule:
        t_no = transaction_id(i)
        d = data_item(i)
        s = "\t\t\t\t"*(t_no-1)
        op = op_type(i)+"("+d+")"
        print(s+op)
    print("\n\n####################################################\n")


def read_schedule(t,d,schedule):
    # make 2-d array of lists for different transactions
    s = [[] for _ in range(t)]
    # filling array for each transaction
    for i in range(len(schedule)):
        t = schedule[i]
        tid = transaction_id(t)
        for j in range(len(s)):
            if (tid == j+1):
                s[j].append(t)
            else:
                s[j].append("vacant")

    return s
"""
A function that checks if two instructions - a and b are conflicting or not
Conditions for conflict :
1. Atleast one of them should be write
2. They should operate on the same data
"""
def isConflict(a,b):
    if (a=="vacant" or b=="vacant"):
        return False
    else:
        op1 = op_type(a)
        op2 = op_type(b)
        if (op1 == 'write' or op2=='write'):
            if (data_item(a) == data_item(b)):
                return True
    return False


# Reading the input

f = open("schedule_inputs.txt")
schedules = f.readlines()
counter = 0
for i in schedules:
    counter+=1
    t = str(i).strip().split(",")
    no_transactions = int(t[0])
    no_data = int(t[1])
    schedule = t[2].split(" ")
    slen = len(schedule)
    display_schedule(no_transactions,no_data,schedule)

    # creating the graph for each schedule
    no_nodes = 0
    no_edges = 0
    g = Graph(no_transactions)
    # Create a pydotplus graph
    pgraph = pydotplus.Dot(graph_type="digraph", ordering="out")
    s = read_schedule(no_transactions,no_data,schedule)
    cycle_graph = {}  # declared as a dictionary
    # an edge in graph is Ti->Tj when Ti and Tj operate
    # on the same data type and at least one operation is Write(W)
    # traverse all the operations in the schedule to construct the graph
    node_list = []
    for ti in range(no_transactions):
        if (ti not in node_list):
            node_list.append(ti)
            pgraph.add_node(pydotplus.Node(ti,label="T" + str(ti+1), shape='ellipse', color='purple', style='filled', fillcolor='pink', fontname='Consolas', fontcolor='black'))
        for i in range(slen):
            op = s[ti][i]
            # for each transaction, we will construct conflict graph with all other transactions to find conflicts
            for j in range(no_transactions):
                if (j == ti):
                    continue # the transaction is itself so continue
                else: # find conflicting instructions
                    for k in range(i+1, slen):
                        if (isConflict(op,s[j][k])):
                            if (not g.isEdge(ti,j)):
                                if len(pgraph.get_edge(ti, j)) == 0:
                                    pgraph.add_edge(pydotplus.Edge(ti, j, color='blue'))
                                g.addEdge(ti, j)  # add an edge from transaction i to transaction j in conflict graph
                            if (ti not in cycle_graph.keys()):
                                cycle_graph[ti] = [j]
                            else:
                                cycle_graph[ti].append(j)

    # now since graph is contructed, we check if it has any cycles or not
    # if it has cycles then the schedule is not conflict serializable
    if (g.isCyclic()):
        print("The Schedule is NOT Conflict Serializable!")
        # displaying the list of transactions involved in conflicts/cycles in graph
        print_cycles_in_graph(cycle_graph)

    else:
        print("The Schedule is Conflict Serializable!")
        # since it's conflict serializable, we print serializability order i.e. topolgical sort of the graph
        print("The Serializability Order: ")
        s_order = g.topologicalSort()
        c = 0
        for item in s_order:
            if (c==len(s_order)-1):
                print("T" + str(item + 1))
            else:
                print("T" + str(item + 1), end='->')
            c += 1
        print()
    pgraph.write_png("images/Graph_S"+str(counter)+".png")
    # Show that image on the screen
    img = cv2.imread("images/Graph_S"+str(counter)+".png")
    cv2.imshow("Graph - " + str(counter), img)
    cv2.waitKey(0)
