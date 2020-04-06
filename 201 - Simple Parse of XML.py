import xml.etree.ElementTree as ET

with open('NAVTable-36.xml', 'r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()

for child in root.iter('{urn:schemas-microsoft-com:dynamics:NAV:MetaObjects}Field'):
    #print(child.attrib)
    # uncomment the next lines to see a few columns
    print(child.attrib.get('ID'),
          child.attrib.get('Name'),
          child.attrib.get('Datatype'),
          child.attrib.get('OptionString'))
