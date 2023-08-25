import streamlit as s
import pandas as p
import requests as r
import snowflake.connector as sf
from urllib.error import URLError



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

def get_fruityvice_data (fruit_choice):
  fruityvice_response = r.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_norm = p.json_normalize(fruityvice_response.json())
  return fruityvice_norm

s.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = s.text_input("What fruit you'd like to have info about?")
  if not fruit_choice:
    s.error("Please select a fruit to get iniformation")
  else:
    back_from_fn = get_fruityvice_data(fruit_choice)
    s.dataframe(back_from_fn)
except URLError as e:
  s.error()


#s.text(fruityvice_response.json())

s.text("The fruit load list contains:")
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()
    
if s.button('Get Fruit Load List'):
  my_cnx = sf.connect(**s.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  s.dataframe(my_data_row)

s.stop()

fruit_choice = s.text_input("What would you like to add?", "jackfruit")
s.write('Thanks for adding ', fruit_choice)
