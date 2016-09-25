from unittest import TestCase
from parser import Lexer


data = '''inin        all
    as principaladmin password "admin" do
    setrecords=[]localx
    append to records with { name = "mike", date = "1-1-90" }
    filtereach rec in records with equal(rec.date, "1-1-90")
    return records
    ***
    '''


class TestLexer(TestCase):
    def test_space(self):
        data = """
            as prinipal admin     "asasasa" do sasasa
        """
        print [[i.value, i.type] for i in Lexer(data).gen]
        self.assertListEqual([[i.value, i.type] for i in Lexer(data).gen],
                             [['\n', 'NEWLINE'], ['as', 'ID'], ['prinipal', 'ID'], ['admin', 'ID'],
                              ['asasasa', 'STRING'], ['do', 'DO'], ['sasasa', 'ID'], ['\n', 'NEWLINE']])
