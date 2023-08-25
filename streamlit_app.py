import streamlit as s
import pandas as p
import requests as r
import snowflake.connector as sf



my_fruit_list = p.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

s.title('New Healthy Diner')

s.header('Breakfast Favorites')
s.text('🥣 Omega 3 & Blueberry Oatmeal')
s.text('🥗 Kale, Spinach & Rocket Smoothie')
s.text('🐔 Hard-Boiled Free-Range Egg')
s.text('🥑🍞 Avocado Toast')

s.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = s.multiselect("Pick some fruits:", list(my_fruit_list.index), default = ["Avocado","Strawberries"] )
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
s.dataframe(fruits_to_show)

s.header('Fruityvice Fruit Advice!')
fruit_choice = s.text_input("What fruit you'd like to have info about?", "Kiwi")
s.write('The user entered ', fruit_choice)

fruityvice_response = r.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#s.text(fruityvice_response.json())

fruityvice_norm = p.json_normalize(fruityvice_response.json())
s.dataframe(fruityvice_norm)



my_cnx = sf.connect(**s.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
s.text("The fruit load list contains:")
s.dataframe(my_data_row)

fruit_choice = s.text_input("What would you like to add?", "jackfruit")
s.write('Thanks for adding ', fruit_choice)
