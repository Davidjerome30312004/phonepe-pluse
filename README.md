# PHONEPE-PLUSE VISUALIZATION

phonepe-pluse using A user friendly tool using streamlit and plotly



![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/3a81c0b2-439f-4899-9fad-6b79676bfb49)


Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly

# What is PhonePe Pulse?
![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/f0438dab-8774-4d7c-abf2-1b353a5c6a0c)

The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.


# Workflow
# Step 1:
## Importing the required Libraries:
Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/fbc7647f-bc3d-463b-872e-e2bbcacc171f)


!pip install ["Name of the library"]
If the libraries are already installed then we have to import those into our script by mentioning the below codes.

# Step 2:
# Data extraction from git :
Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

![Screenshot 2024-04-28 234009](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/6825e845-4017-46ad-ac16-f7e65058f12f)

# step 3
# Data transformation:
In this step the JSON files that are available in the folders are converted into the readeable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used os, json and pandas packages. And finally converted the dataframe into CSV file and storing in the local drive.

# path1 = "Path of the JSON files" agg_trans_list = os.listdir(path1)

Give any column names that you want
(required)columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/341780b5-b88a-4469-b8de-54beda04b88c)

# Step 4:
# Database insertion:
To insert the datadrame into SQL first I've created a new database and tables using "mysql-connector-python" library in Python to connect to a MySQL database and insert the transformed data using SQL commands.
![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/6e1a9a5a-1c70-47b7-8605-7150aa9abe52)


Creating the connection between python and mysql

![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/b08380ba-933d-418b-ac3c-abb64571fe01)

# step 5:
# Data Visualization

Visualize the data by your ownmethods like in bar,pie or in geo mqp etc...

# GEO MAP-FOR INDIA
https://stackoverflow.com/questions/60910962/is-there-any-way-to-draw-india-map-in-plotly

![image](https://github.com/Davidjerome30312004/phonepe-pluse/assets/153855550/91b34132-4956-4781-b3f6-3f94d5e63a0e)

# step 6:
import to streamlit

# import streamlit as st


# LICENSE:

mit-license

If you guys have any suggestions please let me know and we can make it together.






