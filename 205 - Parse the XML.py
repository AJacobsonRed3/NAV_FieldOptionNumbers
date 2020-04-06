import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd

# Creating an empty Dataframe with column names only
dfNAVFieldNames = pd.DataFrame(columns=['TableNo','TableName','FieldNo',
                                        'FieldName'])
dfNAVFieldOptions = pd.DataFrame(columns=['TableNo','TableName','FieldNo',
                                           'FieldName','OptionNo','OptionName'])

tree = ET.parse("NAVTable-15.xml")
root = tree.getroot()

# this gets me all the field level attributes from the XML. It creates row in our
# dataframe.  One row for each distinct field name and one row for each option

for child in root.iter('{urn:schemas-microsoft-com:dynamics:NAV:MetaObjects}Field'):
    dfNAVFieldNames = dfNAVFieldNames.append(
             {'TableNo'   : 15,
              'TableName' : 'G/L Account',
              'FieldNo'   : child.attrib.get('ID'),
              'FieldName' : child.attrib.get('Name')},ignore_index=True)
    OptionString = child.attrib.get('OptionString') 
    if (OptionString is not None):
        # print(OptionString.split(","))
        OptionNo = 0        
        for Option in OptionString.split(","):
            dfNAVFieldOptions = dfNAVFieldOptions.append(
             {'TableNo'   : 15,
              'TableName' : 'G/L Account',
              'FieldNo'   : child.attrib.get('ID'),
              'FieldName' : child.attrib.get('Name'),
              'OptionNo'  : OptionNo,
              'OptionName' : Option},ignore_index=True)
            OptionNo += 1    
# the below just show examples
print(dfNAVFieldNames.head())
print(dfNAVFieldOptions.head())



