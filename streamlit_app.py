import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents new Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 and Oatmeal')
streamlit.text('🥗 Kale,Spinch & Rocket smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New selection to display frutyvice api response
streamlit.header('Frutyvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
       Streamlit.error("Please select a fruit to get the information.")
   else:
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()

#import requests



# Don't run anything past here while we trubleshoot
streamlit.stop()
#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select FRUIT_NAME from PC_RIVERY_DB.PUBLIC.fruit_load_list")
my_data_row = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load lists contains:")
streamlit.dataframe(my_data_row)
# Allow the end user to add the fruit to the List
Add_my_fruit = streamlit.text_input('What fruit would you like to insert?','Kiwi')
streamlit.write('The user entered ', Add_my_fruit)

# Streamlit.write("Thanks for adding",Add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values('from streamlit') ")

