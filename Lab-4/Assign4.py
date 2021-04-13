"""
ATD Assignment-4
Concurrent Schedules

Author:  Yukti Khurana
Date: 13-04-2021

"""

# helper functions to read the input file

# to return the transaction id  of transactions in each schedule
def transaction_id(op):
    index = op.find("(")
    # transaction id can be find on index after the starting bracket
    t = int(op[1:index])
    return t

# to return the type of operation
def op_type(op):
    d = {'R':"read", 'W':"write"}
    t = str(op[0]).upper()
    # returns "read" if R is in op, otherwise "write" for W
    return d[t]

# to return the data item used by the operation
def data_item(op):
    index1 = op.find("(")
    index2 = op.find(")")
    # to extract the data item inside the bracket
    return str(op[index1+1:index2])

# to display the schedule in readable format
def display_schedule(t,d,schedule):
    print("\n#################### SCHEDULE ############################\n")
    for i in range(t):
        print("T"+str(i+1), end="\t\t\t\t")
    print()
    for i in schedule:
        t_no = transaction_id(i)
        d = data_item(i)
        s = "\t\t\t\t"*(t_no-1)
        op = op_type(i)+"("+d+")"
        print(s+op)
    print("\n\n##########################################################\n")


# to convert the schedule into the list of all transactions
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

# function to calculate the read-write ratio of each transaction of a schedule
def read_write_ratio(s):
    # dictionary to store ratio for each transaction in the schedule
    rwr = {}
    for ti in s:
        r, w = 0, 0
        trans = ""
        for ops in ti:
            if ops != 'vacant':
                trans = transaction_id(ops)
                optype = op_type(ops)
                if (optype == 'read'):
                    r+=1
                elif (optype == 'write'):
                    w+=1
        tr = "T"+str(trans)
        if (w!=0):
            rwr[tr] = (1.0*r/w)
        else:
            # if num of writes are zero, the ratio will become infinity
            rwr[tr] = (None)
    return rwr

# function to find the transactions using each data item of the schedule
def common_data(s):
    data_dict = {}
    for op in s:
        # getting the transaction id and data item name for each operation in a transaction
        d =  data_item(op)
        ti = transaction_id(op)
        # appending the Transaction id using the current data item in the declared dictionary
        if d not in data_dict.keys():
            data_dict[d] = [ti]
        else:
            if ti not in data_dict[d]:
                data_dict[d].append(ti)
        data_dict[d].sort()
    return(data_dict)


# Reading the input
f = open("assign4_input.txt")
schedules = f.readlines()

# to count the total number of schedules
counter = 0

# iterating through all the schedules
for i in schedules:
    counter += 1
    print("Schedule - ", counter)
    # reading various elements of the input file
    t = str(i).strip().split(",")
    no_transactions = int(t[0])
    no_data = int(t[1])
    schedule = t[2].split(" ")
    slen = len(schedule)

    # to display the schedule
    display_schedule(no_transactions,no_data,schedule)

    # to get the list of transactions of schedule
    s = read_schedule(no_transactions, no_data, schedule)

    print(s)
    print()

    # dictionary containing read writes of each transaction
    rwr = read_write_ratio(s)

    # displaying the data items which have been accessed by 2 or more transactions
    # and the names of the transactions accessing them
    print("The read-write ratio of all transactions of this schedule are: ")
    for i in rwr:
        if (rwr[i] is None):
            print(i," : ","infinity")
        else:
            print(i," : ",rwr[i])

    data_item_info = common_data(schedule)
    print("\nData items that are accessed commonly by two or more transactions are as follows : ")
    for i in data_item_info.keys():
        if len(data_item_info[i]) >= 2:
            print("Data item-",i, ":")
            for ti in data_item_info[i]:
                tstr = "T"+str(ti)
                print(tstr, end=",")
            print("\n")
    print("-------------------------------------------------------------------------------------------------------------")


