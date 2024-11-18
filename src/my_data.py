from src.base_db import BaseDB
import pandas as pd
import numpy as np

PATH_DB = 'src/data/animals.sqlite'
PATH_RAW = 'src/data/raw_data.csv'

def get_random_data():
    data = pd.DataFrame(data=np.random.random(size=(100,2)), columns=['x', 'y'])
    return data

class AnimalDB(BaseDB):
    def __init__(self):
        super().__init__(path=PATH_DB, create=True)
        if not self._existed:
            pass
            #self._create_tables()
        return
    
    def get_category_list(self) -> list:
        return self.run_query("SELECT category FROM tCategory;")['category'].tolist()
    
    def get_subcategory_list(self, category: str) -> list:
        return self.run_query("SELECT subcategory FROM tSubcategory WHERE category = :category;", 
                              {'category': category})['subcategory'].tolist()
    
    def get_item_list(self, 
                      category: str, 
                      subcategory: str
                      ) -> list:
        sql = """
            SELECT item
            FROM tItem
            WHERE category = :category
              AND subcategory = :subcategory
        ;"""
        params = {'category': category,
                  'subcategory': subcategory
                  }
        return self.run_query(sql, params)['item'].tolist()