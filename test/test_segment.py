#! /usr/bin/env /usr/local/bin/python

import unittest

import pyx12.segment
from pyx12.errors import *

class ArbitraryDelimiters(unittest.TestCase):

    def setUp(self):
        self.seg_str = 'TST&AA!1!1&BB!5&ZZ'
        self.seg = pyx12.segment.segment(self.seg_str, '+', '&', '!')

    def test_identity(self):
        self.assertEqual(self.seg_str+'+', self.seg.__repr__())

    def test_get_seg_id(self):
        self.assertEqual(self.seg.get_seg_id(), 'TST')

    def test_len(self):
        self.assertEqual(len(self.seg), 3)

    def test_getitem3(self):
        self.assertEqual(self.seg.get_value('TST03'), 'ZZ')
                    
    def test_getitem1(self):
        self.assertEqual(self.seg.get_value('TST01'), 'AA!1!1')
                    
    def test_other_terms(self):
        self.assertEqual(self.seg.format('~', '*', ':'), 'TST*AA:1:1*BB:5*ZZ~')


class Identity(unittest.TestCase):

    def setUp(self):
        pass

    def test_identity1(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str+'~')

    def test_identity2(self):
        seg_str = 'ISA*00*          *00*          *ZZ*ZZ000          *'
        seg_str += 'ZZ*ZZ001          *030828*1128*U*00401*000010121*0*T*:\n'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str+'~')

    def test_identity3(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.assertEqual(seg.__repr__(), seg_str)


class Alter(unittest.TestCase):

    def test_alter_element(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST03', 'YY')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*YY~')

    def test_extend_element_blank(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST05', '')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*ZZ~')

    def test_extend_element(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST05', 'AR')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*ZZ**AR~')

    def test_alter_composite(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST02', 'CC:2')
        self.assertEqual(seg.format(), 'TST*AA:1:1*CC:2*ZZ~')

    def test_extend_composite(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST02-4', 'T')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5::T*ZZ~')

    def test_extend_composite2(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST05-2', 'T')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*ZZ**:T~')

    def test_extend_composite_blank1(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST02-4', '')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*ZZ~')

    def test_extend_composite_blank2(self):
        seg_str = 'TST*AA:1:1*BB:5*ZZ~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        seg.set('TST05-4', '')
        self.assertEqual(seg.format(), 'TST*AA:1:1*BB:5*ZZ~')


class Composite(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA:1:Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def test_composite_is_a(self):
        self.failUnless(self.seg.is_composite('TST01'))
        self.failIf(self.seg.is_element('TST01'))
        
    def test_composite_len(self):
        self.assertEqual(len(self.seg.get('01')), 3)

    def test_composite_indexing(self):
        self.assertEqual(self.seg.get_value('TST01-1'), 'AA')
        self.assertEqual(self.seg.get_value('TST01-3'), 'Y')
        self.assertEqual(self.seg.get_value('TST01-4'), None)
        #self.failUnlessRaises(IndexError, lambda x: self.seg.get('TST01-%i' % (x)), 4)


class Simple(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA*1*Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def test_simple_is_a(self):
        self.failUnless(self.seg.is_element('TST01'))
        self.failIf(self.seg.is_composite('TST01'))
        
    def test_simple_len(self):
        self.assertEqual(len(self.seg.get('01')), 1)

    def test_simple_indexing(self):
        self.assertEqual(self.seg.get_value('TST01'), 'AA')
        self.assertEqual(self.seg.get_value('TST02'), '1')
        self.assertEqual(self.seg.get_value('TST03'), 'Y')
        self.assertEqual(self.seg.get_value('TST05'), 'ZZ')
        self.assertEqual(self.seg.get_value('TST06'), None)
        #self.failUnlessRaises(IndexError, lambda x: self.seg[0][x].get_value(), 1)


class GetValue(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA*1*Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def getElementValueOK(self):
        self.assertEqual(self.seg.get_value('TST01'), self.seg.get('TST01').format())
        self.assertEqual(self.seg.get_value('TST04'), self.seg.get('TST04').format())
        self.assertEqual(self.seg.get_value('TST03'), self.seg.get('TST03').format())
        self.assertEqual(self.seg.get_value('TST05'), self.seg.get('TST05').format())
        self.assertEqual(self.seg.get_value('TST06'), self.seg.get('TST06').format())
        
    def getCompositeValueOK(self):
        self.assertEqual(self.seg.get_value('TST04-1'), self.seg.get('TST04-1').format())
        self.assertEqual(self.seg.get_value('TST04-2'), self.seg.get('TST04-2').format())


class RefDes(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA*1*Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def test_simple1(self):
        self.assertEqual(self.seg.get_value('TST01'), 'AA')
        self.assertEqual(self.seg.get_value('01'), 'AA')

    def test_fail_seg_id(self):
        self.failUnlessRaises(EngineError, self.seg.get_value, 'XXX01')

    def test_simple2(self):
        self.assertEqual(self.seg.get_value('TST02'), '1')
        self.assertEqual(self.seg.get_value('02'), '1')

    def test_composite1(self):
        self.assertEqual(self.seg.get_value('TST04-2'), '5')
        self.assertEqual(self.seg.get_value('04-2'), '5')

    def test_composite2(self):
        self.assertEqual(self.seg.get_value('TST04-1'), 'BB')
        self.assertEqual(self.seg.get_value('04-1'), 'BB')

    def test_composite3(self):
        self.assertEqual(self.seg.get_value('TST04'), 'BB:5')
        self.assertEqual(self.seg.get_value('04'), 'BB:5')

    def test_none(self):
        self.assertEqual(self.seg.get_value('TST15'), None)
        self.assertEqual(self.seg.get_value('15'), None)
        self.assertEqual(self.seg.get_value('TST15-2'), None)
        self.assertEqual(self.seg.get_value('15-2'), None)


class IsEmpty(unittest.TestCase):

    def test_empty_seg(self):
        seg_str = 'AAA'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failUnless(seg.is_empty())

    def test_empty_seg_bad1(self):
        seg_str = 'AAA*1~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failIf(seg.is_empty())

    def test_empty_seg_bad2(self):
        seg_str = 'AAA*:1~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failIf(seg.is_empty())

    def test_empty_comp1(self):
        comp_str = ''
        comp = pyx12.segment.composite(comp_str, ':')
        self.failUnless(comp.is_empty())

    def test_empty_comp2(self):
        comp_str = '::'
        comp = pyx12.segment.composite(comp_str, ':')
        self.failUnless(comp.is_empty())

    def test_empty_comp_bad1(self):
        comp_str = '1::a'
        comp = pyx12.segment.composite(comp_str, ':')
        self.failIf(comp.is_empty())

    def test_empty_comp_bad2(self):
        comp_str = '::a'
        comp = pyx12.segment.composite(comp_str, ':')
        self.failIf(comp.is_empty())

    def test_empty_comp_bad3(self):
        comp_str = 'a'
        comp = pyx12.segment.composite(comp_str, ':')
        self.failIf(comp.is_empty())


class Indexing(unittest.TestCase):

    def setUp(self):
        seg_str = 'TST*AA*1*Y*BB:5*ZZ'
        self.seg = pyx12.segment.segment(seg_str, '~', '*', ':')

    def test_index_simple_1(self):
        self.assertEqual(self.seg.get_value('TST01'), 'AA')

    def test_index_simple_2(self):
        self.assertEqual(self.seg.get_value('TST01-1'), 'AA')

    def test_index_composite_1(self):
        self.assertEqual(self.seg.get_value('TST04-1'), 'BB')

    def test_index_composite_2(self):
        self.assertEqual(self.seg.get_value('TST04-2'), '5')
                    

class IsValidSegID(unittest.TestCase):

    def test_valid_seg_id(self):
        seg_str = 'AAA'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failUnless(seg.is_seg_id_valid())

    def test_empty_seg(self):
        seg_str = ''
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failIf(seg.is_seg_id_valid())

    def test_seg_id_too_long(self):
        seg_str = 'AAAA*1~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failIf(seg.is_seg_id_valid())

    def test_seg_id_too_short(self):
        seg_str = 'A*1~'
        seg = pyx12.segment.segment(seg_str, '~', '*', ':')
        self.failIf(seg.is_seg_id_valid())


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ArbitraryDelimiters))
    suite.addTest(unittest.makeSuite(Identity))
    suite.addTest(unittest.makeSuite(Alter))
    suite.addTest(unittest.makeSuite(Composite))
    suite.addTest(unittest.makeSuite(Simple))
    suite.addTest(unittest.makeSuite(RefDes))
    suite.addTest(unittest.makeSuite(Indexing))
    suite.addTest(unittest.makeSuite(IsEmpty))
    suite.addTest(unittest.makeSuite(IsValidSegID))
    return suite

#if __name__ == "__main__":
#    unittest.main()
try:
    import psyco
    psyco.full()
except ImportError:
    pass
unittest.TextTestRunner(verbosity=2).run(suite())


