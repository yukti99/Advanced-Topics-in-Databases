"""
ADVANCED TOPICS IN DATABASES
YUKTI KHURANA 
2017UCP1234

"""

# RE library to match correct syntactic structures of SQL statements
import re


def clean(stmt):
    stmt = stmt.strip("\n")
    # coverting the sql statement to lower case for ease of checking
    stmt = stmt.lower()
    sql_keywords = ["select", "create", "drop", "insert", "update", "delete"]
    # converting all multiple white spaces into single space in the statement
    stmt = ' '.join(stmt.split())
    return stmt

def check_semicolon(stmt):
    if(stmt[len(stmt)-1]!=';'):
        return False
    return True

def tokenize(stmt):
    return stmt.split(" ")


def check_keywords(tokens):
    keywords = ["select", "create", "drop", "insert","update","delete" ]
    if (tokens[0] not in keywords):
        return False
    return True


def display_error(msg):
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Error! Parsing Failed...")
    print("Error Message : ")   
    print(msg)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")

def parsing_success(x):
    print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    s = "Correct Syntax of "+x.upper()+" SQL query!"
    print(s)
    print("SQL Parsing Successful!")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")


""" FUNCTIONS WHICH USE CORRESPONDING REGEX TO CHECK THE SYNTAX OF SQL QUERY """

def parse_select(stmt):
    """
    regex1 = "select\s+([count|avg|sum])([a-zA-Z_]([a-zA-Z0-9_])*)(,[a-zA-Z_]([a-zA-Z0-9_])*)*\s+from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(where .*)?;"
    regex2 = "select\s+(\*)\s+from\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(where .*)?;"
    #g = 'select\s+(((count|avg|sum)\(\s*(distinct|all)?\s*[a-zA-Z_][a-zA-Z0-9_]\s\)|(\s*(distinct|all)?\s*[a-zA-Z_][a-zA-Z0-9_]\s)),\s*)\s(((count|avg|sum)\(\s*(distinct|all)?\s*[a-zA-Z_][a-zA-Z0-9_]\s\)|(\s*(distinct|all)?\s*[a-zA-Z_][a-zA-Z0-9_]\s)))\s+from\s+[a-zA-Z_][a-zA-Z0-9_](\s+where\s+((\d+|([a-zA-Z_][a-zA-Z0-9_]\s*(>|<|=|<=|>=)\s*(("[a-zA-Z_]+")|[0-9]+))\s+(and|or)\s+)(\d+|([a-zA-Z_][a-zA-Z0-9_]\s*(>|<|=|<=|>=)\s*(("[a-zA-Z_]+")|[0-9]+)))))?(\s+group\s+by\s+([a-zA-Z_][a-zA-Z0-9_]\s,\s*)\s[a-zA-Z_][a-zA-Z0-9_]\s(\s*having\s+(count|sum|avg)\(\s*[a-zA-Z_][a-zA-Z0-9_]\s\)\s*(>|<|=|<=|>=)\s*(\d)+)?)?(\s+order\s+by\s+([a-zA-Z_][a-zA-Z0-9_](\s+asc|\s+desc)?\s,\s*)[a-zA-Z_][a-zA-Z0-9_](\s+asc|\s+desc)?)?(;)?'
    r1 = bool(re.match(regex1, stmt))    
    r2 = bool(re.match(regex2, stmt))    
    return (r1 or r2)
    """
    regex = 'select\s+(distinct|all)?\s*(\*|((\w+)\s*,\s*)*\s*(\w+))\s+from\s+(\w+)\s*(where\s+(((\w+)\s+between\s+(\w+)\s+and\s+(\w+))|((\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+)(\s*(and|or)\s+(\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+))*)))?\s*(having\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(<|>|<=|>=|=|<>)\s*([a-zA-Z0-9][a-zA-Z0-9]*) )?\s*(order\s+by\s+((\w+)\s*(asc|desc)?\s*,\s*)*\s*(\w+)\s+(asc|desc)?)?\s*(limit\s+(\d+))?\s*;?'
    return bool(re.match(regex, stmt))

def parse_create(stmt):
    regex = "create table ([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*(([a-zA-Z_][a-zA-Z0-9_]*)\s+(int|varchar|text)\s*(,)\s*)*(([a-zA-Z_][a-zA-Z0-9_]*)\s+(int|varchar|text))\)\s*;"
    return bool(re.match(regex, stmt))

def parse_drop(stmt):
    regex = "drop table (([a-zA-Z_][a-zA-Z0-9_]*),)*([a-zA-Z_][a-zA-Z0-9_]*)(;)?"
    return bool(re.match(regex, stmt))

def parse_insert(stmt):
    regex ='insert\s+into\s+(\w+)\s*(\(\s*((([a-zA-Z0-9][a-zA-Z0-9_]*)\s*,\s*)*\s*([a-zA-Z0-9][a-zA-Z0-9_]*))\s*\))?\s+values\s*(\(\s*((((".*")|([a-zA-Z0-9][a-zA-Z0-9]*))\s*,\s*)*\s*([a-zA-Z0-9][a-zA-Z0-9]*))\s*\));?'
    return bool(re.match(regex, stmt))

def parse_update(stmt):
    regex = 'update\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+set\s+(([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(".*"|[0-9][0-9]*)\s*,\s*)*\s*(([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(".*"|[0-9][0-9]*))\s*(where\s+(([a-zA-Z_][a-zA-Z0-9_]*)\s*((between\s+([0-9][0-9]*)\s+and\s+([0-9][0-9]*))|(is\s+(not)?\s+ null)|(<|>|<=|>=|=|<>)\s*(".*"|[0-9][0-9]*))))\s*;?'
    return bool(re.match(regex, stmt))

def parse_delete(stmt):
    regex = 'delete\s+from\s+(\w+)\s*(where\s+(((\w+)\s+between\s+(\w+)\s+and\s+(\w+))|((\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+)(\s*(and|or)\s+(\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+))*)))?\s*(order\s+by\s+((\w+)\s*(asc|desc)?\s*,\s*)*\s*((\w+)\s*(asc|desc))?)?\s*(limit\s+(\d+));?'
    return bool(re.match(regex, stmt))



# Program driver
def main():
    print("\n************* Welcome to SQL Synctactic Parser made by Yukti Khurana ****************\n\n")
    # reading the sql statement
    f = open("sql_stmt.txt","r")
    stmts = f.readlines()
    cnt=0
    for i in stmts:
        cnt+=1
        if(len(i)==0):
            break
        # cleaning the SQL Query for checking 
        sql_stmt = clean(i)

        # printing cleaned stmt
        print"SQL Query - ",cnt," : "
        print(sql_stmt)

        # checking for semicolon
        if (check_semicolon(sql_stmt)==False):     
            display_error("SQL Queries must have a semicolon at the end")       
            continue

        # tokenizing the sql query
        tokens = tokenize(sql_stmt)
        
        # checking keywords in sql query
        if (check_keywords(tokens)==False):
            display_error("The Sql query must be either of the following : select, create, drop, delete or insert")
            continue  

        query_type = tokens[0]
        if (query_type == "select"):
            ans = parse_select(sql_stmt)
            if (ans == False):
                display_error("Error in parsing select query...")
            else:
                parsing_success("select")

        if (query_type == "update"):
            ans = parse_update(sql_stmt)
            if (ans == False):
                display_error("Error in parsing update query...")
            else:
                parsing_success("update")

        if (query_type == "insert"):
            ans = parse_insert(sql_stmt)
            if (ans == False):
                display_error("Error in parsing insert query...")
            else:
                parsing_success("insert")

        if (query_type == "delete"):
            ans = parse_delete(sql_stmt)
            if (ans == False):
                display_error("Error in parsing delete query...")
            else:
                parsing_success("delete")

        if (query_type == "create"):
            ans = parse_create(sql_stmt)
            if (ans == False):
                display_error("Error in parsing create query...")
            else:
                parsing_success("create")
        if (query_type == "drop"):
            ans = parse_drop(sql_stmt)
            if (ans == False):
                display_error("Error in parsing drop query...")
            else:
                parsing_success("drop")  

            
        
            
        print("---------------------------------------------------------------------------------")
    

    
main()
"""
ADVANCED TOPICS IN DATABASES
YUKTI KHURANA 
2017UCP1234

"""
