import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    list_of_dicts = []
    restaurants = db_filename
    cur.execute(""" SELECT restaurants.name, categories.category, buildings.building, restaurants.rating
        FROM restaurants JOIN categories
        ON restaurants.category_id = categories.id
        JOIN buildings
        ON restaurants.building_id = buildings.id
        """)
    data = cur.fetchall()
    for tuple in data:
        dic = {}
        dic['name'] = tuple[0]
        dic['category'] = tuple[1]
        dic['building'] = tuple[2]
        dic['rating'] = tuple[3]
        list_of_dicts.append(dic)
    return list_of_dicts

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories along the y-axis and the counts of each category along the
    x-axis.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    category_list = []
    num_of_category = []
    restaurants = db_filename

    cur.execute("""SELECT category, COUNT(*)
    FROM restaurants JOIN categories
    ON restaurants.category_id = categories.id
    GROUP BY category""")
    data = cur.fetchall()
    for i in data:
        category_list.append(i[0])
        num_of_category.append(i[1])
    plt.barh(category_list, num_of_category)
    plt.ylabel("Restaurant Categories")
    plt.xlabel("Number of Restaurants")
    plt.title("Types of Restaurants on South U Ave")
    plt.tight_layout()
    plt.show()
    result = dict(data)
    return result


#EXTRA CREDIT
def highest_rated_building(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each building and returns a tuple containing the
    building number with the highest rated restaurants and the average rating of the restaurants
    in that building. This function should also create a bar chart that displays the buildings along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_building = ((1335, 4.8), ('1335', 4.8))

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_building(self):
        best_building = highest_rated_building('South_U_Restaurants.db')
        self.assertIsInstance(best_building, tuple)
        self.assertIn(best_building, self.best_building)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)