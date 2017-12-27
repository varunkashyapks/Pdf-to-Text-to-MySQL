
# coding: utf-8

# # Zauba Question

# Parse the attached pdf files and save the data in MySQL database. Provide complete functional code along with a dump of mysql db containing parsed data.

# Pdf file to text for this we used pdfminer. First open the pdf file and parse the object then strat begin to analysis on layouts. from text box extract the text to string 

# In[1]:


# Importing the required file 
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

fp = open('/home/varun/PDFParsing/U16571275.pdf', 'rb')

parser = PDFParser(fp)

document = PDFDocument(parser)

if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
rsrcmgr = PDFResourceManager()

device = PDFDevice(rsrcmgr)

laparams = LAParams()

device = PDFPageAggregator(rsrcmgr, laparams=laparams)

#PDF interpreter object
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Make a list for further process
d = []

def parse_obj(lt_objs):

    for obj in lt_objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            another= "%s" % ( obj.get_text().replace('\n', ''))
            d.append(another)
            print another
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)

for page in PDFPage.create_pages(document):

    interpreter.process_page(page)
    layout = device.get_result()

    parse_obj(layout._objs)


# The data is not in the arranged way so for making key, value pair i used normal regular expression(regex) and python list functions then dictionary to store the key, value pair

# In[2]:


# Title processing Title as key 
Title = str(d[0])
Title


# In[3]:


# Service_Request_Date as key
d2=d[2].split(':') 
d20 = str(d2[0])
Service_Request_Date = str(d2[1])
Service_Request_Date


# In[4]:


# SRN for the storing into key
import re
pay = re.compile(u'Payment(.*)')
d3 = pay.sub('',d[3])
d3 = d3.split(':')
S_NO = str(d3[1])
S_NO


# In[5]:


#Payment_made_into bank name 
Payment_made_into = str(d[4])
Payment_made_into


# In[6]:


# Name of comapny 
pay2 = re.compile(u'No(.*)')
d6 = str(d[6])
d6 = d6.split(',')
Name = pay2.sub('',d6[0])
Name


# In[7]:


#Address
d61 = d6[3]+d6[4]
Address = re.findall('[A-Z][^A-Z]*',d61)
Address=" ".join(Address)
Address


# In[8]:


#Service Type
stype=re.compile(u'(.*)Service Type')
d7=stype.sub('',d[7])
d7=d7.split(':')
Service_Type = str(d7[1])
Service_Type


# In[9]:


#Service Description
Service_Description=str(d[11])+str(d[12])


# In[10]:


#Type of Fee
Type_of_Fee = str(d[13])
Type_of_Fee
# OR 
d
for i, val in enumerate(d):
    if 'Type of Fee' in val:
        obj = i+4
        Type_of_Fee = str(d[obj])
        print Type_of_Fee


# In[11]:


# Amount of Rs
d
for i, val in enumerate(d):
    if 'Amount(Rs.)' in val:
        obj = i+4
        Amount_Rs = float(d[obj])
        print Amount_Rs


# In[12]:


# Total Amount of Rs
d
for i, val in enumerate(d):
    if 'Total' in val:
        obj = i+1
        Total = float(d[obj])
        print Total


# In[13]:


# Mode of Payment
d
for i, val in enumerate(d):
    if 'Mode of Payment:' in val:
        obj = i+1
        Mode_of_Payment = str(d[obj])
        print Mode_of_Payment


# In[14]:


# Received Payment Rupees
d
for i, val in enumerate(d):
    if 'Received Payment Rupees:' in val:
        obj = i
        Received_Payment_Rupees = str(d[obj]).split(':')[2]
        print Received_Payment_Rupees


# ## The new_dic created for storing the key value pair , it is for csv file now i have shown for the two files similarly we can do it for n number of file in single click 

# In[15]:


# Only for first file 
new_dic1 = {'Address':Address,'Amount_Rs':Amount_Rs,'Mode_of_Payment':Mode_of_Payment,'Name':Name,
       'Payment_made_into':Payment_made_into,'Received_Payment_Rupees':Received_Payment_Rupees,'S_NO':S_NO,'Service_Description':Service_Description,
       'Service_Request_Date':Service_Request_Date,'Service_Type':Service_Type,
       'Title':Title,'Total':Total,'Type_of_Fee':Type_of_Fee}
new_dic1


# In[16]:


# For second file sample i shown here
new_dic2 = {'Address':Address,'Amount_Rs':Amount_Rs,'Mode_of_Payment':Mode_of_Payment,'Name':Name,
       'Payment_made_into':Payment_made_into,'Received_Payment_Rupees':Received_Payment_Rupees,'S_NO':S_NO,'Service_Description':Service_Description,
       'Service_Request_Date':Service_Request_Date,'Service_Type':Service_Type,
       'Title':Title,'Total':Total,'Type_of_Fee':Type_of_Fee}


# ## This below is shown how we combine two files into csv final

# In[17]:


from tabulate import tabulate
import pandas as pd

df1 = pd.Series(new_dic1,name='Value 1').to_frame()
df2 = pd.Series(new_dic2,name='Value 2').to_frame()
df=pd.concat([df1, df2], axis=1)
print(tabulate(df, headers= 'keys', tablefmt= 'grid'))
df.to_csv('filenamehere.csv',header = False)


# ### Like the above in csv file it will be storing now we want to transpose into row to column because in 
# ### order to store in the MySql database , from csv we can easily store the csv values now transposing csv file as we requuired 

# In[18]:


import pandas as pd
ano_tr = pd.read_csv("filenamehere.csv",header=None)
tt = ano_tr.T
tt=tt.iloc[1:]

tt.to_csv('aaaaaa.csv',header= False,index=False)


# ### Now transpose has done then we need to push into mysql database
# ### Note please keep all files in the root home work directory or else specify the path for all csv

#  We use the Mysql package in python, before this some pacakges are required download from internt or
#  use in terminal $ sudo apt-get install mysql-server mysql-client or $ easy_install-2.7 mysql-python , before that  $ sudo apt-get update && sudo apt-get upgrade
# 
# After inastalling required package create localhost host="localhost",user="root",
# the give as you required passwd="*******", then create database db='pdf_data'
# 

# ## Craeting the database (run below commond only once)

# In[21]:


# Craeting the database
import MySQLdb
db = MySQLdb.connect(host="localhost",user="root",passwd="9482029664")
cursor = db.cursor()
sql = 'CREATE DATABASE pdf_data'
cursor.execute(sql)


# In[22]:


# Craeting the database
import MySQLdb

# Open database connection and give your password username host database name
db = MySQLdb.connect(host="localhost",user="root",passwd="9482029664",db='pdf_data')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS test_csv3")

# Create table as per requirement
sql = """CREATE TABLE test_csv3 (
         Address CHAR(250),
         Amount_Rs CHAR(250),
         Mode_of_Payment CHAR(250),
         Name CHAR(250),
         Payment_made_into CHAR(250),
         Received_Payment_Rupees CHAR(250),
         S_NO CHAR(250) NOT NULL,
         Service_Type CHAR(250),
         Service_Description CHAR(250),
         Service_Request_Date CHAR(250),
         Title CHAR(250),
         Total CHAR(250),
         Type_of_Fee CHAR(250))"""
    


cursor.execute(sql)
# disconnect
db.close()


# ## Inserting values into data bases

# In[24]:


import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='9482029664',
    db='pdf_data')
cursor = mydb.cursor()

#csv_data = csv.reader(file('pdf_test_zuba.csv'))
csv_data = csv.reader(file('aaaaaa.csv'))

for row in csv_data:
    cursor.execute('INSERT INTO test_csv3(Address,Amount_Rs,Mode_of_Payment,Name,Payment_made_into,Received_Payment_Rupees,S_NO,                  Service_Type,Service_Description,Service_Request_Date,Title,Total,Type_of_Fee)'                   'VALUES("%s", "%s", "%s","%s","%s","%s","%s", "%s", "%s","%s","%s","%s","%s")',row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"


# ## Now we will do it for all file if folder has several pdf file means we can iterate through it. By for loop and python module os.list directory we can pass the file .
# ## The below file run and directly appending into the main mysql database(already created database)

# In[26]:


# Importing the required file 
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

fp = open('/home/varun/PDFParsing/U16573131.pdf', 'rb')

parser = PDFParser(fp)

document = PDFDocument(parser)

if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
rsrcmgr = PDFResourceManager()

device = PDFDevice(rsrcmgr)

laparams = LAParams()

device = PDFPageAggregator(rsrcmgr, laparams=laparams)

#PDF interpreter object
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Make a list for further process
d = []

def parse_obj(lt_objs):

    for obj in lt_objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            another= "%s" % ( obj.get_text().replace('\n', ''))
            d.append(another)
            #print another
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)

for page in PDFPage.create_pages(document):

    interpreter.process_page(page)
    layout = device.get_result()

    parse_obj(layout._objs)
    
# Title processing Title as key 
Title = str(d[0])
print Title

# Service_Request_Date as key
d2=d[2].split(':') 
d20 = str(d2[0])
Service_Request_Date = str(d2[1])
print Service_Request_Date

# SRN for the storing into key
import re
pay = re.compile(u'Payment(.*)')
d3 = pay.sub('',d[3])
d3 = d3.split(':')
S_NO = str(d3[1])
print S_NO

#Payment_made_into bank name 
Payment_made_into = str(d[4])
print Payment_made_into

# Name of comapny 
pay2 = re.compile(u'No(.*)')
d6 = str(d[6])
d6 = d6.split(',')
Name = pay2.sub('',d6[0])
print Name

#Address
d61 = d6[3]+d6[4]
Address = re.findall('[A-Z][^A-Z]*',d61)
Address=" ".join(Address)
print Address
#Service Type
stype=re.compile(u'(.*)Service Type')
d7=stype.sub('',d[7])
d7=d7.split(':')
Service_Type = str(d7[1])
print Service_Type
#Service Description
Service_Description=str(d[11])+str(d[12])
print Service_Description
#Type of Fee
Type_of_Fee = str(d[13])
print Type_of_Fee
# OR 

for i, val in enumerate(d):
    if 'Type of Fee' in val:
        obj = i+4
        Type_of_Fee = str(d[obj])
        print Type_of_Fee
# Amount of Rs

for i, val in enumerate(d):
    if 'Amount(Rs.)' in val:
        obj = i+4
        Amount_Rs = float(d[obj])
        print Amount_Rs
# Total Amount of Rs
for i, val in enumerate(d):
    if 'Total' in val:
        obj = i+1
        Total = float(d[obj])
        print Total
# Mode of Payment

for i, val in enumerate(d):
    if 'Mode of Payment:' in val:
        obj = i+1
        Mode_of_Payment = str(d[obj])
        print Mode_of_Payment
# Received Payment Rupees

for i, val in enumerate(d):
    if 'Received Payment Rupees:' in val:
        obj = i
        Received_Payment_Rupees = str(d[obj]).split(':')[2]
        print Received_Payment_Rupees
        
# Only for first file 
new_dic3 = {'Address':Address,'Amount_Rs':Amount_Rs,'Mode_of_Payment':Mode_of_Payment,'Name':Name,
       'Payment_made_into':Payment_made_into,'Received_Payment_Rupees':Received_Payment_Rupees,'S_NO':S_NO,'Service_Description':Service_Description,
       'Service_Request_Date':Service_Request_Date,'Service_Type':Service_Type,
       'Title':Title,'Total':Total,'Type_of_Fee':Type_of_Fee}
new_dic3

# Tabulating the data for better csv
from tabulate import tabulate
import pandas as pd

df = pd.Series(new_dic3,name='Value 1').to_frame()
print(tabulate(df, headers= 'keys', tablefmt= 'grid'))
df.to_csv('filenamehere1.csv',header = False)
#Now transpose has to do
import pandas as pd
ano_tr = pd.read_csv("filenamehere1.csv",header=None)
tt = ano_tr.T
tt=tt.iloc[1:]

tt.to_csv('aaaaaa1.csv',header= False,index=False)

#Inserting values into data bases
import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='9482029664',
    db='pdf_data')
cursor = mydb.cursor()

#csv_data = csv.reader(file('pdf_test_zuba.csv'))
csv_data = csv.reader(file('aaaaaa1.csv'))

for row in csv_data:
    cursor.execute('INSERT INTO test_csv3(Address,Amount_Rs,Mode_of_Payment,Name,Payment_made_into,Received_Payment_Rupees,S_NO,                  Service_Type,Service_Description,Service_Request_Date,Title,Total,Type_of_Fee)'                   'VALUES("%s", "%s", "%s","%s","%s","%s","%s", "%s", "%s","%s","%s","%s","%s")',row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"   

