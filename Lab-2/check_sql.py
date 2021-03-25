

# RE library to match correct syntactic structures of SQL statements
import re


class SQL_Parser:
    def __init__(self, s):
        self.stmt = s

    def parse_select(self,s):
        regex = 'select\s+(distinct|all)?\s*(\*|((\w+)\s*,\s*)*\s*(\w+))\s+from\s+(\w+)\s*(where\s+(((\w+)\s+between\s+(\w+)\s+and\s+(\w+))|((\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+)(\s*(and|or)\s+(\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+))*)))?\s*(having\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(<|>|<=|>=|=|<>)\s*([a-zA-Z0-9][a-zA-Z0-9]*) )?\s*(order\s+by\s+((\w+)\s*(asc|desc)?\s*,\s*)*\s*(\w+)\s+(asc|desc)?)?\s*(limit\s+(\d+))?\s*;?'
        return bool(re.match(regex, s))

    def parse_create(self,s):
        regex = "create table ([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*(([a-zA-Z_][a-zA-Z0-9_]*)\s+(int|varchar|text)\s*(,)\s*)*(([a-zA-Z_][a-zA-Z0-9_]*)\s+(int|varchar|text))\)\s*;"
        return bool(re.match(regex, s))

    def parse_drop(self,s):
        regex = "drop table (([a-zA-Z_][a-zA-Z0-9_]*),)*([a-zA-Z_][a-zA-Z0-9_]*)(;)?"
        return bool(re.match(regex, s))

    def parse_insert(self,s):
        regex = 'insert\s+into\s+(\w+)\s*(\(\s*((([a-zA-Z0-9][a-zA-Z0-9_]*)\s*,\s*)*\s*([a-zA-Z0-9][a-zA-Z0-9_]*))\s*\))?\s+values\s*(\(\s*((((".*")|([a-zA-Z0-9][a-zA-Z0-9]*))\s*,\s*)*\s*([a-zA-Z0-9][a-zA-Z0-9]*))\s*\));?'
        return bool(re.match(regex, s))

    def parse_update(self,s):
        regex = 'update\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+set\s+(([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(".*"|[0-9][0-9]*)\s*,\s*)*\s*(([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(".*"|[0-9][0-9]*))\s*(where\s+(([a-zA-Z_][a-zA-Z0-9_]*)\s*((between\s+([0-9][0-9]*)\s+and\s+([0-9][0-9]*))|(is\s+(not)?\s+ null)|(<|>|<=|>=|=|<>)\s*(".*"|[0-9][0-9]*))))\s*;?'
        return bool(re.match(regex, s))

    def parse_delete(self,s):
        regex = 'delete\s+from\s+(\w+)\s*(where\s+(((\w+)\s+between\s+(\w+)\s+and\s+(\w+))|((\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+)(\s*(and|or)\s+(\w+)\s*(<|>|<=|>=|=|<>)\s*(\w+))*)))?\s*(order\s+by\s+((\w+)\s*(asc|desc)?\s*,\s*)*\s*((\w+)\s*(asc|desc))?)?\s*(limit\s+(\d+));?'
        return bool(re.match(regex, s))

    def check_semicolon(self,s):
        if (s[len(s) - 1] != ';'):
            return False
        return True

    def tokenize(self, s):
        return s.split(" ")

    def check_keywords(self,tokens):
        keywords = ["select", "create", "drop", "insert", "update", "delete"]
        if (tokens[0] not in keywords):
            return False
        return True

    def clean(self,s):
        stmt = s.strip("\n")
        # coverting the sql statement to lower case for ease of checking
        stmt = stmt.lower()
        sql_keywords = ["select", "create", "drop", "insert", "update", "delete"]
        # converting all multiple white spaces into single space in the statement
        stmt = ' '.join(stmt.split())
        return stmt

    def parse_query(self):
        s = self.clean(self.stmt)
        # tokenizing the sql query
        tokens = self.tokenize(s)
        if (self.check_semicolon(s) == False or self.check_keywords(tokens) == False):
            return False
        query_type = tokens[0]
        if (query_type == "select"):
            return(self.parse_select(s))

        if (query_type == "update"):
            return(self.parse_update(s))

        if (query_type == "insert"):
            return(self.parse_insert(s))

        if (query_type == "delete"):
            return(self.parse_delete(s))

        if (query_type == "create"):
            return(self.parse_create(s))

        if (query_type == "drop"):
            return(self.parse_drop(s))


def main():
    print("\n************* Welcome to SQL Synctactic Parser made by Yukti Khurana ****************\n\n")
    # reading the sql statement
    stmt = "SELECT colname FROM table1, table2 WHERE condition_list ORDER BY colname ;"
    sql_parser = SQL_Parser(stmt)
    print(sql_parser.parse_query())


