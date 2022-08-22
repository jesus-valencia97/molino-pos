#%%
import sqlite3

conn = sqlite3.connect('molino.db')

c = conn.cursor()

table_products = """CREATE TABLE IF NOT EXISTS products (
	id_producto VARCHAR(5) NOT NULL,
	descripcion VARCHAR(30),
	precio_kg FLOAT NOT NULL,
	inventario_kg FLOAT,
	PRIMARY KEY (id_producto)
);"""
#%%
c.execute(table_products)


# %%
c.execute("SELECT * FROM products where precio_kg > 800 ")
print(c.fetchall())


# %%
