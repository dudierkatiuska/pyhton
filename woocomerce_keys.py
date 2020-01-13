import psycopg2
from psycopg2 import Error
connection = psycopg2.connect(user = "postgres",
                                  password = "fabi17501515",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "dbpg_akipartes")
    
class Woocomerce():

    def __init__(self):
        self.url = []
        self.key = []
        self.secret = []
        self.name_store = []
        self.city_store = []
        self.logo_store = []
        
        cursor = connection.cursor()
        cursor.execute( "SELECT stor_name, stor_url, stor_userkey, stor_secretkey, stor_city, stor_logo FROM tbl_store" )
        for stor_name, stor_url, stor_userkey , stor_secretkey, stor_city, stor_logo in cursor.fetchall() :
            self.name_store.append(stor_name)
            self.url.append(stor_url)
            self.key.append(stor_userkey)
            self.secret.append(stor_secretkey)
            self.city_store.append(stor_city)
            self.logo_store.append(stor_logo)
            
        # self.url.append(urls)
        # self.key.append(userkey)
        # self.secret.append(secretkey)
        # self.name_store.append(name)
        # self.city_store.append(city)
        
        # self.url.append("http://localhost/correcaminosworld/")
        # self.key.append("ck_fd0965fe69941047cf6eebb00783208ff19d42a8")
        # self.secret.append("cs_008b54d5487d4d9e661f722f350dd5d2ba385849")
        # self.name_store.append("Correcaminos World")
        # self.city_store.append("Medellín")
        
        # self.url.append("http://localhost/camping/")
        # self.key.append("ck_b4becb92459564f1727be8160e04692c26040798")
        # self.secret.append("cs_b26edcbae3f078533ecb7bceebc65a3521f20f9b")
        # self.name_store.append("Camping")
        # self.city_store.append("Bogota")
            
        # self.url.append("http://www.correcaminosworld.com/")
        # self.key.append("ck_9f5ace33cd4ea981080d7f7e3d71422c14ce19ff")
        # self.secret.append("cs_3769ac28d14d283bc9f55069f981cf700859a25a")
        # self.name_store.append("Correcaminos World")
        # self.city_store.append("Bogotá")
            
            
    def get_key(self):
        return self.key

    def get_secret(self):
        return self.secret
        
    def get_url(self):
        return self.url
