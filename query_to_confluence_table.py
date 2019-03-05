#!/usr/bin/env python
# title           :query_to_confluence_table module
# description     : this module takes a query and a db and returns a nicely formatted confluence/JIRA table
# author          :Chris Sprance / Entrada Interactive
# usage           : print QueryToConfluenceTable(query[str], db[atlas_db_class])
# instantiate and print all in one line methods are called when converted to str()
# python_version  :2.7.5
# ==============================================================================


class QueryToConfluenceTable(object):
    """
    Class used to query the atlas db and then return a formatted table
    for use in Confluence or JIRA
    """

    def __init__(self, query, db):
        super(QueryToConfluenceTable, self).__init__()
        self.db = db
        self.query = query

    def __str__(self):
        """
        formats and returns the query results
        """
        results = self.db.c.execute(self.query)
        table_headers = [desc[0] for desc in results.description]
        rows = [row for row in results]
        str_headers = self.create_headers_row(table_headers)
        str_rows = self.create_rows(rows)
        return str_headers + '\n' + '\n'.join(str_rows)

    @staticmethod
    def create_headers_row(table_headers):
        return '|| ' + ' || '.join(table_headers) + ' || '

    @staticmethod
    def create_rows(rows):
        ret = list()
        for row in rows:
            column = [str(col).replace('{', '').replace('}', '').replace('|', ',') for col in row]
            ret.append('| ' + ' | '.join(column) + ' | ')
        return ret
