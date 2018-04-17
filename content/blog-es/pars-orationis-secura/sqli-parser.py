"""
Module sqli-parser.py
Module to detect SQL insertions and selections that include
PHP variables or function calls in concatenations,
which is considered dangerous. Also finds other occurrences
of the dangerously concatenated variable in the same file.
"""

import os
from pyparsing import (Combine, Literal, CaselessKeyword, Word, alphanums,
                       delimitedList, Group, Optional, ZeroOrMore, line,
                       lineno, col, ParseException)

KW_INSERT = Combine(Literal('"') + CaselessKeyword("INSERT INTO"))
KW_VALUES = CaselessKeyword("VALUES")
KW_END = Literal('"')
KW_SELECT = CaselessKeyword("SELECT")
KW_FROM = CaselessKeyword("FROM")
KW_WHERE = CaselessKeyword("WHERE")
# $var_name_3
PHP_IDENTIFIER = Combine(Literal('$')
                         + Word(alphanums+"_")).setResultsName("phpvar")
# db2_table_1, column_1
SQL_IDENTIFIER = Word(alphanums + "_")
COLUMN_NAMES = Literal("(") + delimitedList(SQL_IDENTIFIER) + Literal(")")
VARCHAR = Literal("'").suppress() + Word(alphanums) + Literal("'").suppress()
# now(), mysqli_real_escape_string($link, $secret)
PHP_FUNCALL = Combine(Word(alphanums + "_") + Literal("(")
                      + Optional(delimitedList(PHP_IDENTIFIER)) + Literal(")"))
# '" . validate($user_input) . "' or LIKE '%" . $var . "%'
DANGER_CONCAT = (Literal("'").suppress() + Optional("%")
                 + Literal('"').suppress() + Literal(".").suppress()
                 + (PHP_IDENTIFIER | PHP_FUNCALL)
                 + Literal(".").suppress() + Literal('"').suppress()
                 + Optional("%") + Literal("'").suppress()
                ).setResultsName("danger identifier")
VALUE = VARCHAR ^ PHP_FUNCALL ^ DANGER_CONCAT
VALUES = Group(Literal("(").suppress() + delimitedList(VALUE)
               + Literal(")").suppress()).setResultsName("values")
WHAT_TO_SELECT = Literal("*") ^ delimitedList(SQL_IDENTIFIER)
# name='" . $name . "'
COND_COL_EQ_VAL = SQL_IDENTIFIER + Literal("=") + VALUE
# name LIKE '%".$name."%'
COND_COL_LIKE_VAL = SQL_IDENTIFIER + Literal("LIKE") + DANGER_CONCAT
ATOM_COND = COND_COL_EQ_VAL | COND_COL_LIKE_VAL
CONNECTOR = CaselessKeyword("OR") ^ CaselessKeyword("AND")
# col_user = '" . $user . "' AND password = '" . hash($password) . "'
CONDITION = Group(ATOM_COND + ZeroOrMore(CONNECTOR + ATOM_COND)
                 ).setResultsName("values")
# "INSERT INTO blog VALUES (now(), 'a', '" . $inj1 . "','" . $inj2 . "')";
SQL_INSERT = (KW_INSERT + SQL_IDENTIFIER + Optional(COLUMN_NAMES)
              + KW_VALUES + VALUES + KW_END)
# "SELECT * FROM ta_ble WHERE name = '" . $name . "'";
SQL_SELECT = (KW_SELECT + WHAT_TO_SELECT + KW_FROM
              + SQL_IDENTIFIER + Optional(KW_WHERE + CONDITION))
SQL_INJECTION = SQL_INSERT ^ SQL_SELECT

def scan_test_file(path='test-cases.lst'):
    """ Scan an entire file to test for occurrences of SQL_INJECTION parser,
    determine what the injectable variables are and parse again looking for
    other occurrences of that variable."""
    with open(path) as test_file:
        content = test_file.read()
        print("\nScanning file {}".format(path))
        queries = 0
        for tokens, start, _end in SQL_INJECTION.scanString(content):
            sqli_line = line(start, content)
            print("In file {0}, line {1}, col {2}:\n{3:^}"
                  .format(path.split("/")[-1], lineno(start, content),
                          col(start, content), sqli_line.strip()))
            try:
                injectable_variables = tokens["values"]
                for injectable_variable in injectable_variables:
                    try:
                        # Re-parsing is ugly but necessary since a PHP_FUNCALL
                        # might not contain any PHP_IDENTIFIERs.
                        res = (PHP_IDENTIFIER ^ PHP_FUNCALL
                              ).parseString(injectable_variable)
                        injectable_variable = res["phpvar"]
                        print(" Injectable variable {0}. Other ocurrences:"
                              .format(injectable_variable))
                        # Make a parser on-the-fly to detect other
                        # occurrences of the injectable variable
                        tpar = Literal(injectable_variable)
                        for _tokens2, start2, _end2 in tpar.scanString(content):
                            print("  L{0:<3} {1}"
                                  .format(lineno(start2, content),
                                          line(start2, content).strip()))
                        queries += + 1
                    except (ParseException, KeyError):
                        # If parse fails or key "phpvar" does not exist,
                        # there is simply no danger variable.
                        pass
            except (ParseException, KeyError): # Same as above
                print(" No dangerous concatenations in this query.")
        print("Found {0} SQL injections in {1}.".format(queries, path))
        return queries

def test_directory():
    """ Iterate scan_test_file() for all source files in a directory
    and report total number of SQL injection vulnerabilities."""
    path = "./"
    vulns = 0
    for filename in sorted(os.listdir(path)):
        if filename.split('.')[-1] == "php":
            vulns += scan_test_file(path + filename)
    print("\nTotal SQL injections found: {}".format(vulns))

scan_test_file()
#test_directory()
