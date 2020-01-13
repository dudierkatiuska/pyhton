import json
from woocommerce import API
from woocomerce_keys import Woocomerce
import psycopg2
from psycopg2 import Error
connection = psycopg2.connect(user = "postgres",
                                  password = "fabi17501515",
                                  host = "localhost",
                                  port = "5432",
                                  database = "dbpg_akipartes")

cursor = connection.cursor()
name=[] 
price=[] 
permalink=[]
woo = Woocomerce()

urls_to_get = woo.url
keys_to_get = woo.key
secrets_to_get = woo.secret
name_store = woo.name_store
city_store = woo.city_store
logo_store = woo.logo_store

url = ''
key = ''
secret = ''
# try: 
print('-------------------------------------------------------------------------------------------------------')
print('------------------------------- SCRAPER OF PRODUCTS IN WORDPRESS STORES -------------------------------')
print('------------------------------------------- BUILT IN PYTHON -------------------------------------------')
print('--------------------------------------- AUTHOR: KATIUSKA DUDIER ---------------------------------------')
print('-------------------------------------------------------------------------------------------------------')
print('-------------------------------- THE PROCESS OF SCRAPING IS STARTING... -------------------------------')
print('-------------------------------------------------------------------------------------------------------')
print('\nWE GET ' + str(len(urls_to_get)) + ' STORES TO SCRAPE, WE ARE STARTING TO SEARCH THE PAGES OF EACH STORE...\n')
for h in range(0, len(urls_to_get)):
    url = urls_to_get[h]
    key = keys_to_get[h]
    secret = secrets_to_get[h]
    wcapi = API(
        url = url,
        consumer_key = key,
        consumer_secret = secret,
        version="wc/v2",
        timeout=60,
        wp_api=True,
        query_string_auth=True 
    )
    try:
        r=wcapi.get("products")
        total_pages = int(r.headers['X-WP-TotalPages'])
        if (total_pages > 0):
            print('\nWE GET ' + str(total_pages) + ' PAGES IN THE STORE ' + str(url) + ', WE ARE STARTING TO SEARCH THE PRODUCTS ON EACH PAGE...')
        elif (total_pages == 0):
            print('\nTHERE\'S NO PAGES AND PRODUCTS TO GET IN THIS STORE' + str(url))
        for i in range(1,total_pages+1):
            r=wcapi.get("products", params = {'per_page' : 100,'page':str(i)}).json()
            if (len(r) > 0):
                print('\nWE GET ' + str(len(r)) + ' PRODUCTS IN PAGE ' + str(i) + ', WE ARE STARTING TO ADD OR UPDATE THE PRODUCTS IN THE DATABASE...\n')
            elif (len(r) == 0):
                print('\nTHERE\'S NO PRODUCTS TO GET IN PAGE ' + str(i))
            for product in r:
                name = product['name']
                price = product['price'] 
                permalink = product['permalink']
                images = product['images']
                categories = product['categories']
                attributes = product['attributes']
                attributes_product = {}
                logo = logo_store[h]
                for attribute in attributes:
                    options = ''
                    for option in attribute['options']:
                        options += option + ','
                    options = options[:-1]
                    attributes_product[str(attribute['name'])] = str(options)
                attributes_product['Ciudad'] = str(city_store[h])
                for image in images:
                    image = image['src']
                    for category in categories:
                        category = category['name']
                sql_find_product = "select prod_ide, prod_name, prod_price, prod_link, prod_src, prod_url, prod_categories, prod_attribute, prod_logo from tbl_product where prod_name=%s and prod_url=%s"
                datos_find = (name, url)
                cursor.execute(sql_find_product, datos_find)
                results_find = cursor.fetchall()
                if len(results_find) > 0:
                    for prod_ide, prod_name, prod_price, prod_link , prod_src, prod_url, prod_categories, prod_attribute, prod_logo in results_find:
                        sql_update ="update tbl_product set prod_name=%s, prod_price=%s, prod_link=%s, prod_src=%s, prod_url=%s, prod_categories=%s, prod_attribute=%s, prod_logo=%s where prod_ide=%s"
                        datos_update = (name, price, permalink, image, url, category, str(attributes_product), logo, prod_ide)
                        cursor.execute(sql_update, datos_update)
                        connection.commit()
                        print('Product ' + prod_name + ' updated in the database')
                else:
                    sql="insert into tbl_product(prod_name, prod_price, prod_link, prod_src, prod_url, prod_categories, prod_attribute, prod_logo) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                    datos=(name, price, permalink, image, url, category, str(attributes_product), logo)
                    cursor.execute(sql, datos)
                    connection.commit()
                    print('Product ' + prod_name + ' added to the database')
    except KeyError:
        print('THERE WAS AN ERROR WITH THE SCRAPING OF THE STORE ' + url + ', THE KEY OF THE STORE IS INVALID, CHECK THE KEY AND THE SECRET KEY AND TRY AGAIN')
    except Exception:
        print('THERE WAS AN ERROR WITH THE CONNECTION WITH THE STORE ' + url + ', CHECK YOUR INTERNET CONNECTION AND TRY AGAIN')
cursor.close()
connection.close()
print('\n-------------------------------------------------------------------------------------------------------')
print('------------------------------ PROCESS OF SCRAPING TERMINATED SUCCESSFULLY ----------------------------')
print('-------------------------------------------------------------------------------------------------------')
# except Exception:
#     print('There was an error with the execution of the scraper')

