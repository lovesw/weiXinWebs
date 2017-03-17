from django.test import TestCase

# Create your tests here.
import xml.etree.ElementTree as Etree

xml_str = """<root><ot><title>i am title</title></ot></root>"""
notify_data_tree = Etree.fromstring(xml_str)
str_value = notify_data_tree.find("ot/title").text
print(str_value)
