import unittest
from cry_utils import XForm
import xml.etree.ElementTree as ET


class TestLayerParser(unittest.TestCase):
    def setUp(self):
        test_layer = r"D:\perforce\dev\EI\Tools\Atlas\tests\layers_test_data\atlas_layerparser_test.lyr"
        with open(test_layer) as xml_file:
            tree = ET.parse(xml_file).getroot()
        objs = tree.findall('./Layer/LayerObjects/Object')
        parent = objs[5]
        child = list(list(parent)[0])[0]
        self.p_xforms = XForm(parent)
        self.c_xforms = XForm(child)

    def test_01(self):
        print self.p_xforms
        print self.c_xforms
        x = self.p_xforms + self.c_xforms
        y = self.c_xforms + self.p_xforms
        a = self.p_xforms - self.c_xforms
        b = self.c_xforms - self.p_xforms
        print x
        print y
        print a
        print b
        print self.p_xforms
        print self.c_xforms

    def test_02(self):
        print self.p_xforms.rot
        print self.p_xforms.pos
        print self.p_xforms.scale
        self.p_xforms.rot = [0.000000, 0.000000, 0.000000]
        self.p_xforms.pos = [0.000000, 0.000000, 0.000000]
        self.p_xforms.scale = [0.000000, 0.000000, 0.000000]
        print self.p_xforms.rot
        print self.p_xforms.pos
        print self.p_xforms.scale


if __name__ == '__main__':
    unittest.main(verbosity=2)
