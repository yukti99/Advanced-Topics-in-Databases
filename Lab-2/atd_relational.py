import sql_metadata
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where
from check_sql import *


def get_columns(sql_tokens):
    # access the identifier list of parsed sql tokens
    item = sql_tokens[2]
    if isinstance(item, IdentifierList):
        for ident in item.get_identifiers():
            yield ident.get_name()
    elif isinstance(item, Identifier):
        yield item.get_name()

def get_where_condition(parsed_stmt):
    try:
        for item in parsed_stmt.tokens:
            if isinstance(item, Where):
                #where = parsed_stmt[-1]
                where = item.value
                wl = str(where).strip().split("where ")[1]
                wl = wl.replace(";","")
                wl = wl.replace(" and ", " ∩ ")
                wl = wl.replace(" or ", " ∪ ")
                return wl
    except:
        return None


def clean_stmt(s):
    s = s.lower()
    s = s.replace(";","")
    s = s.replace("distinct ", "")
    s = s.replace("inner join", "join")
    s = s.replace("outer join", "join")
    s = s.replace("left join", "join")
    s = s.replace("right join", "join")
    s = s.replace("natural join", "join")
    return s


def get_RelationalAlgebra(stmt, column_names,condition, table_names):

    # for  projection of columns
    if ('*' in stmt):
        s1 = ""
    else:
        s1 = " π ("+column_names+")"
    # for conditional selection of tuples
    if (condition):
        s2 = "( σ ("+condition+")"
    else:
        s2 = ""
    # for table names in relational algebra
    s3 = "("+table_names+")"
    if (s2!=""):
        s3 += ")"
    ra = s1+s2+s3
    return ra

def main():
    # SQL QUERIES FOR TESTING

    #stmt = "SELECT FROM table1 ;"
    stmt = "SELECT movieTitle, studioName FROM StarsIn , Movie  WHERE movieYear >= 2000 AND movieTitle = title ORDER BY movieTitle ;"
    #stmt = "SELECT department, lastname FROM employees natural join dept WHERE order_id > 100 OR emp_id = 2 ;"
    #stmt = "select a, b from bank natural join truck ;"
    #stmt = "SELECT * FROM tab1, tab2 ; "
    #stmt = "SELECT * FROM tab1, tab2 WHERE tab1.x = tab2.y ;"


    # Parsing the query to check if it is correct or not
    sql_parser = SQL_Parser(stmt)
    is_correct_sql = sql_parser.parse_query()

    if (is_correct_sql == False):
        print("Sorry! Given SQL Query is incorrect...Parsing Failed!!!")
        exit(1)
    else:
        print("\nParsing Successfull!!")
    stmt_original = stmt
    # cleaning the sql query
    stmt = clean_stmt(stmt)

    # parsing the sql statement using sqlparse library
    parsed_stmt = sqlparse.parse(stmt)[0]
    sql_tokens = parsed_stmt.tokens

    # getting table names using sql_metadata library
    tables = sql_metadata.get_query_tables(stmt)
    # joining tables using join symbol
    tables = " ⋈ ".join(tables)

    # getting column names for projection
    cols = list(get_columns(sql_tokens))
    cols = ",".join(cols)

    # getting the where condition for selection
    where_condition = get_where_condition(parsed_stmt)
    # sql query converted to relational algebra
    ra = get_RelationalAlgebra(stmt, cols, where_condition, tables)

    # printing the results
    print("{}{}\n".format("\nSQL Query : \n\n\t", stmt_original))
    print("{}{}\n".format("RELATIONAL ALGEBRA : \n\n\t",ra))

main()




