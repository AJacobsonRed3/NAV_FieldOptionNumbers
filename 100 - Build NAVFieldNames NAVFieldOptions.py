# Example Using Python 3.x
import zlib, sys, struct
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import pyodbc
import sqlalchemy as sa # 1.3.6
import urllib           # 1.25.3
import xml.etree.ElementTree as ET

def ParseXML():
    print("Processing " + str(TableNo) + " " + TableName)
    dfNAVFieldNames = pd.DataFrame(columns=['TableNo','TableName','FieldNo',
                                        'FieldName'])
    dfNAVFieldOptions = pd.DataFrame(columns=['TableNo','TableName','FieldNo',
                                           'FieldName','OptionNo','OptionName'])
    tree = ET.fromstring(output.decode("utf-8"))
    # root = tree.getroot()
    for child in tree.iter('{urn:schemas-microsoft-com:dynamics:NAV:MetaObjects}Field'):
        # print(child.attrib.get("ID"))
        dfNAVFieldNames  = dfNAVFieldNames.append(
             {'TableNo'   : TableNo,
              'TableName' : TableName,
              'FieldNo'   : child.attrib.get('ID'),
              'FieldName' : child.attrib.get('Name')},ignore_index=True)
        OptionString = child.attrib.get('OptionString') 
        if (OptionString is not None):
        # print(OptionString.split(","))
            OptionNo = 0        
            for Option in OptionString.split(","):
                dfNAVFieldOptions = dfNAVFieldOptions.append(
                {'TableNo'   : TableNo,
                'TableName' : TableName,
                'FieldNo'   : child.attrib.get('ID'),
                'FieldName' : child.attrib.get('Name'),
                'OptionNo'  : OptionNo,
                'OptionName' : Option},ignore_index=True)
                OptionNo += 1    
    dfNAVFieldNames.to_sql("NAVFieldNames",con=engine,schema=Schema,if_exists="append",index=False)
    dfNAVFieldOptions.to_sql("NAVFieldOptions",con=engine,schema=Schema,if_exists="append",index=False)
    
# 1 -Create a connection string
Driver      = "ODBC Driver 17 for SQL Server"
Server      = "ADAM2019"
Database    = "NAVReportingTest"
Schema      = "dbo"
ConnectionString = "Driver={" + Driver + "};Server="+Server+";Database="+Database+";Trusted_Connection=yes;"
params              = urllib.parse.quote_plus(ConnectionString)
engine = sa.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params, fast_executemany=True)

# 2 - The query we want to use
SQLQuery = """
SELECT meta.[Object ID] AS TableNo,
       obj.Name AS TableName,
       meta.Metadata
FROM NAVDemo.dbo.[Object Metadata] meta
    JOIN NAVDemo.dbo.Object obj
        ON meta.[Object Type] = obj.Type
           AND meta.[Object ID] = obj.ID
WHERE obj.Type = 1
--aND meta.[Object ID] <= 40
ORDER BY obj.ID"""
# 2A - the dataframes that will actually store all the output
# From our parsing of the Metadata
# Creating empty dataframe one for each table we will eventually write

# 3 -Load the Data From NAV to a Python Pandas Dataframe
ObjectMetaData = pd.read_sql(sql=SQLQuery,con=engine)#,params=params)
# 4 - loop throught the output (Note - in the initial test I have 
#     limited this to just table 15)
for Name, TableNo, TableName, MetaData in ObjectMetaData.itertuples():
    MetaDataToDecompress = bytearray(MetaData)
    # we need to skip the first four characters
    MetaDataToDecompress = MetaDataToDecompress[4:]
    # now we decompress the data
    output = zlib.decompress(MetaDataToDecompress,-15)
    # we are going to take the output data and pass it to our python function
    ParseXML()


