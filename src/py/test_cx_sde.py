import os
import unittest
import pathlib

import cx_sde


class UtilsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.sdeconn = os.environ['SDEFILE']
        self.dummytab = 'test_dual' 

    @classmethod
    def tearDownClass(self):

        sql = """drop table {0}""".format(self.dummytab)
        
        try:
            sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                                 sql)
        except:
            pass

    def test_aexecute_immediate(self):

        #sql returns a single X

        sql = """SELECT 'X'"""
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.assertEqual(len(sdereturn), 1)

        self.assertEqual(sdereturn[0], 'X')


    def test_bexecute_immediate(self):

        #sql returns a list with 2 Xs

        sql = """SELECT 'X' UNION ALL SELECT 'X'"""
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

        self.assertIsInstance(sdereturn, list)

        self.assertEqual(len(sdereturn), 2)


    def test_cselectavalue(self):

        sql = """SELECT 'X'"""

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)

        self.assertEqual(sdereturn, 'X')


    def test_dselectnull(self):

        # should error.  Its select a value, not select the void
        sql = """SELECT NULL"""

        try:
            sdereturn = cx_sde.selectavalue(self.sdeconn,
                                            sql)
        except:
            pass
        else:
            self.assertFalse(sdereturn)


    def test_eselectacolumn(self):

        sql = """SELECT 'X'"""

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], 'X')

        sql = """SELECT 'X' UNION ALL SELECT 'X'"""
        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], 'X')
        self.assertEqual(output[1], 'X')

    def test_fselectabadcolumn(self):

        sql = """SELECT boo FROM dual"""

        print(f"Expected sql fail on next line from {sql}")

        try:
            output = cx_sde.selectacolumn(self.sdeconn,
                                          sql)
        except:
            pass
        else:
            raise ValueError('Shoulda failed')


    def test_gselectanumbercolumn(self):

            sql = """SELECT 1"""

            output = cx_sde.selectacolumn(self.sdeconn,
                                          sql)

            self.assertIsInstance(output, list)
            self.assertEqual(len(output), 1)
            self.assertEqual(output[0], 1)

            sql = """select 1 union all select 1"""

            output = cx_sde.selectacolumn(self.sdeconn,
                                            sql)

            self.assertIsInstance(output, list)
            self.assertEqual(len(output), 2)
            self.assertEqual(output[0], 1)
            self.assertEqual(output[1], 1)

    
    def test_hselectanullcolumn(self):

        sql = 'SELECT 1 UNION ALL SELECT NULL'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], 1)
        self.assertIsNone(output[1])

        sql = 'SELECT NULL'

        output = cx_sde.selectacolumn(self.sdeconn,
                                      sql)

        self.assertIsInstance(output, list)
        self.assertEqual(len(output), 1)
        self.assertIsNone(output[0])

    def test_ianonymousblock(self):

        #sqlserver term is Dynamic SQL
        dummyfile = os.path.join(pathlib.Path(__file__).parent.parent,
                                 'sql',
                                 'dummy.sql')

        # avoid stripping new lines and other formatting here, allow comments     
        with open(dummyfile, 'r') as sqlfile:
            sql = sqlfile.read() 

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

    def test_jdmlcommit(self): 

        # wut. CTAS
        sql = """select * into {0} from (SELECT 'X' as dummy) as dummy""".format(self.dummytab)

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                            sql)

        # youre killing me here.  Update with alias
        sql = """update a set a.dummy = 'Z' from {0} a""".format(self.dummytab)

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                            sql)

        sql = """select count(*) from {0} a where a.dummy = 'Z'""".format(self.dummytab)

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 1)

        sql = """drop table {0}""".format(self.dummytab)
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

    def test_kexecutestatements(self): 

        sql = """select * into {0} from (SELECT 'X' as dummy) as dummy""".format(self.dummytab)

        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)
        sqls = []
        sqls.append("""insert into {0} values('A') """.format(self.dummytab))
        sqls.append("""insert into {0} values('B') """.format(self.dummytab))
        sqls.append("""insert into {0} values('C') """.format(self.dummytab))
        
        sdereturn = cx_sde.execute_statements(self.sdeconn,
                                              sqls)

        sql = """select count(*) from {0} """.format(self.dummytab)

        sdereturn = cx_sde.selectavalue(self.sdeconn,
                                        sql)
    
        self.assertEqual(sdereturn, 4)

        sql = """drop table {0}""".format(self.dummytab)
        sdereturn = cx_sde.execute_immediate(self.sdeconn,
                                             sql)

if __name__ == '__main__':
    unittest.main()