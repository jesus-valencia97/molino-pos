#%%
import sqlite3

conn = sqlite3.connect('molino.db')

c = conn.cursor()

c.execute('SELECT * FROM products')
print(c.fetchall())

#%%

import pandas as pd

products = pd.read_excel(r"G:\Mi unidad\molino\Etiquetas KG.xlsx",sheet_name='KG')
products.columns = ['id_producto','descripcion','precio_kg','inventario_kg']

print(products.columns)

# %%
products.to_sql('products',conn,if_exists='replace',index=False)