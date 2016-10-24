
INSPIRATION:
What suppliers have my "hard to find" parts? What suppliers have of most of the parts that I need? Is it worth shopping? When putting together "kits" used to build electronic products, these are so…

POTENTIAL S/W development modules and tools:
-Anaconda 
-python prompt and nano, python prompt and notepad++, or pycharm
-Python 2.x or Python 3.x
-sql alchemy
-Flask or Django 
-scrapi or Soapbox

SPECIFICATION
Data Input from Purchasing Agent:
- Web page with upload button
- up to 100 rows of text, in .csv format, including ...
- columns: Part Number, Manufacturer, Description, Quantity, Notes
- Web page with search button returns rows previously input and output

Data Collecting Web Scraping / harvesting:
- Up to 15,000 rows of text, in convenient format, including ...
- Part Number, Manufacturer, Description, Qty of Inventory, price@qtyA, price@qtyB, ... price@qtyG, link to "buy-now"
- Data obtained through API provided by octopart.com for $
- Data obtained through API of selected willing distributors and mfgs   
- Data obtained through web scraping (of non-password protected web sites)

Data Storage:
- Data is stored in the form of SQL tables
- Data is stored in the form of HTML pages
- Data is stored in the form supplied by Octopart's API  
- Data is stored in the form supplied by distributors' APIs

Data Parsing / Selection / Display :
- Display Potential:  Minimum Cost of Items ($), Maximum of parts needed divided by parts available from inventory (%)  
- Display Actual Selected: Cost of Items Selected ($), Number of Items Selected (count), Number of items in Basket (count)
- Display all data collected, but filtered by (Purchasing Agent's radio button) selection of desired suppliers
- Display above, but filtered to show imprecise matches including part numbers with dashes misplaced
- Display above, but filtered by suppliers having the hardest to find parts
- Display above, but filtered by suppliers having the most parts
- Display above, but filtered by (Purchasing Agent's radio button) selection of desired rows

Data Output:
- web page with download button provides the current parsed/analyzed display
   
