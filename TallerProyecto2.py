import tkinter as tk
from tkinter import END, messagebox, ttk
import mysql.connector
import datetime
from mysql.connector import Error
import re

class DBManager:
    def __init__(self):
        self.user = "root"
        self.password = "" 
        self.database = "taller"
        self.host = "localhost"
        self.open()


# Crear la tablas en sql para classapp pero ya directo en sql estan en taller bd-----------------------------
    def open(self):
        try:
            self.conn = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password)
            self.cursor = self.conn.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.conn.close()
            self.conn = mysql.connector.connect(host=self.host, user=self.user, passwd=self.password,
                                                database=self.database)
            self.cursor = self.conn.cursor()

            # Crear la tabla de usuarios (users) si no existe SQL-----------------------------------------
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    username VARCHAR(255),
                    password VARCHAR(255),
                    profile VARCHAR(255)
                )
            """)

            # Crear la tabla de clientes (customers) si no existe
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    phone VARCHAR(20),
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                    license_plate VARCHAR(20),
                    brand VARCHAR(255),
                    model VARCHAR(255),
                    registration_date DATE DEFAULT CURRENT_TIMESTAMP,
                    customer_id INT,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS piezas (
                    pieza_id INT AUTO_INCREMENT PRIMARY KEY,
                    descripcion varchar(50),
                    stock INT
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reparaciones(
                    reparacion_id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha_ingreso DATE DEFAULT CURRENT_TIMESTAMP,
                    fecha_salida DATE DEFAULT CURRENT_TIMESTAMP,
                    cantidad INT,
                    falla VARCHAR(255),
                    pieza_id INT,
                    FOREIGN KEY (pieza_id) REFERENCES piezas(pieza_id),
                    vehicle_id INT,
                    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
                )
            """)
#SQL ERRORS EXCEPTIONS--------------------------------------------------------------------
            self.conn.commit()
        except Error as e:
            print("Error while connecting to MySQL", e)
#USER CRUD--------------------------------------------------------------------
    def search_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        user = self.cursor.fetchone()
        return user

    def search_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        user = self.cursor.fetchone()
        return user

    def update_user(self, user):
        query = "UPDATE users SET name=%s, username=%s, password=%s, profile=%s WHERE user_id=%s"
        values = (user['name'], user['username'], user['password'], user['profile'], user['user_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def save_user(self, user):
        query = "INSERT INTO users (user_id, name, username, password, profile) VALUES (%s, %s, %s, %s, %s)"
        values = (user['user_id'], user['name'], user['username'], user['password'], user['profile'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_next_user_id(self):
        query = "SELECT MAX(user_id) FROM users"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
        #/////////////////////////////////////////////////////////////////////////////////////////


#Customercurd--------------------------------------------------------------------
    def search_customer_by_id(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = %s"
        self.cursor.execute(query, (customer_id,))
        customer = self.cursor.fetchone()
        return customer

    def search_customer_by_name(self, customer_name):
        query = "SELECT * FROM customers WHERE name = %s"
        self.cursor.execute(query, (customer_name,))
        customer = self.cursor.fetchone()
        return customer

    def update_customer(self, customer):
        query = "UPDATE customers SET name=%s, phone=%s, user_id=%s WHERE customer_id=%s"
        values = (customer['name'], customer['phone'], customer['user_id'], customer['customer_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def delete_customer(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = %s"
        self.cursor.execute(query, (customer_id,))
        self.conn.commit()

    def save_customer(self, customer):
        query = "INSERT INTO customers (customer_id, name, phone, user_id) VALUES (%s, %s, %s, %s)"
        values = (customer['customer_id'], customer['name'], customer['phone'], customer['user_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_next_customer_id(self):
        query = "SELECT MAX(customer_id) FROM customers"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    #///////////////////////////////////////////////////////////////////////////////////////////////////
        
#CARROS CRUD--------------------------------------------------------------------
    def save_vehicle(self, vehicle):
        if 'license_plate' not in vehicle:
            print("Error: 'license_plate' key is missing in the vehicle dictionary")
            return
        query = "INSERT INTO vehicles (license_plate, brand, model, customer_id) VALUES (%s, %s, %s, %s)"
        values = (vehicle['license_plate'], vehicle['brand'], vehicle['model'], vehicle['customer_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def update_vehicle(self, vehicle):
        query = "UPDATE vehicles SET license_plate=%s, brand=%s, model=%s, registration_date=%s, customer_id=%s WHERE vehicle_id=%s"
        values = (vehicle['license_plate'], vehicle['brand'], vehicle['model'], vehicle['registration_date'], vehicle['customer_id'], vehicle['vehicle_id'])
        self.cursor.execute(query, values)
        self.conn.commit()


    def delete_vehicle(self, vehicle_id):
        query = "DELETE FROM vehicles WHERE vehicle_id = %s"
        self.cursor.execute(query, (vehicle_id,))
        self.conn.commit()

    def search_vehicle_by_license_plate(self, license_plate):
        query = "SELECT * FROM vehicles WHERE license_plate = %s"
        self.cursor.execute(query, (license_plate,))
        vehicle = self.cursor.fetchone()
        return vehicle

    def search_vehicle_by_brand(self, brand):
        query = "SELECT * FROM vehicles WHERE brand = %s"
        self.cursor.execute(query, (brand,))
        vehicle = self.cursor.fetchone()
        return vehicle

    def search_vehicle_by_model(self, model):
        query = "SELECT * FROM vehicles WHERE model = %s"
        self.cursor.execute(query, (model,))
        vehicle = self.cursor.fetchone()
        return vehicle

    def get_next_car_id(self):
        query = "SELECT MAX(vehicle_id) FROM vehicles"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
        
    def get_all_customer_names(self):
        query = "SELECT c.name FROM customers c LEFT JOIN vehicles v ON c.customer_id = v.customer_id WHERE v.customer_id IS NULL"
        self.cursor.execute(query)
        customer_names = [row[0] for row in self.cursor.fetchall()]
        return customer_names

    
    def get_customer_id_by_index(self, index):
        query = "SELECT customer_id FROM customers LIMIT %s, 1"
        self.cursor.execute(query, (index,))
        customer_id = self.cursor.fetchone()[0]
        return customer_id
    #agregado nuevo
    def get_customer_id_by_name(self, customer_name):
        query = "SELECT customer_id FROM customers WHERE name = %s"
        self.cursor.execute(query, (customer_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def get_available_customer_names(self):
        # Obtener todos los nombres de clientes
        all_customer_names = self.get_all_customer_names()
        # Obtener los IDs de clientes que ya tienen un vehículo registrado
        customers_with_vehicle = self.get_customers_with_vehicle()
        # Filtrar los nombres de clientes para excluir aquellos que ya tienen un vehículo
        available_customer_names = [name for name in all_customer_names if name not in customers_with_vehicle]
        return available_customer_names
        #//////////////////////////////////////////////////////////////////////////////////////777

    def save_pice(self,pice):
        query = "INSERT INTO piezas (pieza_id, descripcion, stock) VALUES (%s, %s, %s)"
        values = (pice['pieza_id'], pice['descripcion'], pice['stock'])
        self.cursor.execute(query, values)
        self.conn.commit()
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def get_next_pice_id(self):
        query = "SELECT MAX(pieza_id) FROM piezas"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
        
    def search_pice_by_id(self, pice_id):
        query = "SELECT * FROM piezas WHERE pieza_id = %s"
        self.cursor.execute(query, (pice_id,))
        pice_id = self.cursor.fetchone()
        return pice_id

    def update_pieza(self,pice):
        query = "UPDATE piezas SET descripcion=%s, stock=%s WHERE pieza_id=%s"
        values = (pice['descripcion'], pice['stock'],pice['pieza_id'])
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_pice(self,pice_id):
        query = "DELETE FROM piezas WHERE pieza_id = %s"
        self.cursor.execute(query, (pice_id,))
        self.conn.commit()
    #//////////////////////////////////////////////////////////////////////////////////////
    

    def save_repair(self, repair):
        # Obtener el ID de la pieza utilizando la descripción de la pieza
        pieza_id = self.get_piece_id_by_description(repair['pieza'])
        # Obtener el ID del vehículo utilizando la matrícula del vehículo
        vehicle_id = self.get_vehicle_id_by_license_plate(repair['matricula'])

        # Convertir repair['stock'] a un entero
        stock = int(repair['stock'])

        query = "INSERT INTO reparaciones (fecha_ingreso, fecha_salida, cantidad, falla, pieza_id, vehicle_id) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (repair['fecha_ingreso'], repair['fecha_salida'], stock, repair['falla'], pieza_id, vehicle_id)
        self.cursor.execute(query, values)
        self.conn.commit()

        # Actualizar el stock de la pieza
        self.update_piece_stock(pieza_id, stock)

    def update_piece_stock(self, piece_id, difference):
        # Obtener el stock actual de la pieza
        current_stock = self.get_piece_stock_by_id(piece_id)

        # Convertir a entero si el stock actual es None
        current_stock = int(current_stock) if current_stock is not None else 0

        # Calcular el nuevo stock
        new_stock = current_stock - difference

        # Verificar si hay suficientes piezas en stock
        if new_stock < 0:
            messagebox.showerror("Error", "No hay suficientes piezas en stock.")
            return

        # Actualizar el stock de la pieza en la base de datos
        query = "UPDATE piezas SET stock=%s WHERE pieza_id=%s"
        values = (new_stock, piece_id)
        self.cursor.execute(query, values)
        self.conn.commit()


    def get_piece_stock_by_id(self, pieza_id):
        query = "SELECT stock FROM piezas WHERE pieza_id = %s"
        self.cursor.execute(query, (pieza_id,))
        result = self.cursor.fetchone()
        if result:
            return int(result[0])  # Convertir el valor a entero
        else:
            return None

    def get_piece_id_by_description(self, description):
        query = "SELECT pieza_id FROM piezas WHERE descripcion = %s"
        self.cursor.execute(query, (description,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_vehicle_id_by_license_plate(self, license_plate):
        query = "SELECT vehicle_id FROM vehicles WHERE license_plate = %s"
        self.cursor.execute(query, (license_plate,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def get_next_repair_id(self):
        query = "SELECT MAX(reparacion_id) FROM reparaciones"
        self.cursor.execute(query)
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            return 1
        else:
            return max_id + 1
    
    def search_repair_by_id(self, repair_id):
        query = """
            SELECT r.reparacion_id, v.license_plate, p.descripcion, r.fecha_ingreso, r.fecha_salida, r.cantidad, r.falla
            FROM reparaciones r
            INNER JOIN vehicles v ON r.vehicle_id = v.vehicle_id
            INNER JOIN piezas p ON r.pieza_id = p.pieza_id
            WHERE r.reparacion_id = %s
        """
        self.cursor.execute(query, (repair_id,))
        return self.cursor.fetchone()

    def update_repair(self, repair):
        query = "UPDATE reparaciones SET fecha_ingreso=%s, fecha_salida=%s, cantidad=%s, falla=%s WHERE reparacion_id=%s"
        values = (repair['fecha_ingreso'], repair['fecha_salida'], repair['stock'], repair['falla'], repair['reparacion_id'])
        self.cursor.execute(query, values)
        self.conn.commit()

    def get_all_vehicles(self):
        try:
            query = "SELECT * FROM vehicles"
            self.cursor.execute(query)
            vehicles = self.cursor.fetchall()
            return vehicles
        except Exception as e:
            print("Error while fetching all vehicles:", e)
            return None

    def get_all_pieces(self):
        try:
            query = "SELECT * FROM piezas"
            self.cursor.execute(query)
            pieces = self.cursor.fetchall()
            return pieces
        except Exception as e:
            print("Error while fetching all pieces:", e)
            return None
        
    def check_stock_availability(self, pieza_id, requested_quantity):
        current_stock = self.get_piece_stock_by_id(pieza_id)
        if current_stock is None:
            messagebox.showerror("Error", "La pieza especificada no se encontró en la base de datos.")
            return False
        
        current_stock = int(current_stock)
        requested_quantity = int(requested_quantity)
        return current_stock >= requested_quantity
    
    def delete_repair(self, repair_id):
        query = "DELETE FROM reparaciones WHERE reparacion_id = %s"
        self.cursor.execute(query, (repair_id,))
        self.conn.commit()

    def check_vehicle_existence(self, license_plate):
        query = "SELECT COUNT(*) FROM vehicles WHERE license_plate = %s"
        self.cursor.execute(query, (license_plate,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def check_piece_existence(self, descripcion):
        query = "SELECT COUNT(*) FROM piezas WHERE descripcion = %s"
        self.cursor.execute(query, (descripcion,))
        count = self.cursor.fetchone()[0]
        return count > 0

        

#~~~~~~~~~~~~~~~~~~~ClassAPP-------------USERS---------------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios")
        self.db = DBManager()
        self.current_user_id = None

        # Crear widgets
        self.lbl_user_id = tk.Label(root, text="ID de Usuario:")
        self.lbl_user_id.place(x=10, y=10)
        self.ent_user_id = tk.Entry(root, state="readonly")
        self.ent_user_id.place(x=130, y=10)

        self.lbl_name = tk.Label(root, text="Nombre:")
        self.lbl_name.place(x=10, y=40)
        self.ent_name = tk.Entry(root,state="disabled")
        self.ent_name.place(x=130, y=40)

        self.lbl_username = tk.Label(root, text="Nombre de usuario:")
        self.lbl_username.place(x=10, y=70)
        self.ent_username = tk.Entry(root,state="disabled")
        self.ent_username.place(x=130, y=70)

        self.lbl_password = tk.Label(root, text="Contraseña:")
        self.lbl_password.place(x=10, y=100)
        self.ent_password = tk.Entry(root, show="*",state="disabled")
        self.ent_password.place(x=130, y=100)

        self.lbl_profile = tk.Label(root, text="Perfil:")
        self.lbl_profile.place(x=10, y=130)
        self.ent_profile = ttk.Combobox(root, values=["Admin", "Secre","Mecanico"],state="disabled")
        self.ent_profile.place(x=130, y=130)

        self.btn_insert = tk.Button(root, text="Guardar", command=self.insert,state="disabled")
        self.btn_insert.place(x=80, y=160)

        self.btn_cancel = tk.Button(root, text="Cancelar", command=self.cancel, state="disabled")
        self.btn_cancel.place(x=150, y=160)

        self.btn_new = tk.Button(root, text="Nuevo", command=self.new_user)
        self.btn_new.place(x=10, y=160)

        self.btn_search = tk.Button(root, text="Buscar", command=self.search)
        self.btn_search.place(x=370, y=40)

        self.btn_edit = tk.Button(root, text="Editar", command=self.edit, state="disabled")
        self.btn_edit.place(x=230, y=160)

        self.btn_delete = tk.Button(root, text="Eliminar", command=self.delete, state="disabled")
        self.btn_delete.place(x=300, y=160)

        # Crear el nuevo cuadro de texto para buscar usuarios por ID
        self.lbl_search_id = tk.Label(root, text="Buscar por ID:")
        self.lbl_search_id.place(x=290, y=10)
        self.ent_search_id = tk.Entry(root)
        self.ent_search_id.place(x=380, y=10)

    def new_user(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        # Obtener el siguiente ID de usuario de la base de datos
        self.current_user_id = self.db.get_next_user_id()
        self.ent_user_id.insert(0, self.current_user_id)

    def insert(self):
        if not self.validate_fields():
            return
        user = {
            'user_id': self.ent_user_id.get(),
            'name': self.ent_name.get(),
            'username': self.ent_username.get(),
            'password': self.ent_password.get(),
            'profile': self.ent_profile.get()
        }
        self.db.save_user(user)
        messagebox.showinfo("Éxito", "Usuario insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search(self):
        user_id = self.ent_search_id.get()
        user = self.db.search_user_by_id(user_id)
        if user:
            self.ent_user_id.delete(0, END)
            self.ent_name.delete(0, END)
            self.ent_username.delete(0, END)
            self.ent_password.delete(0, END)
            self.ent_profile.set("")

            self.ent_user_id.insert(0, user[0])
            self.ent_name.insert(0, user[1])
            self.ent_username.insert(0, user[2])
            self.ent_password.insert(0, user[3])
            self.ent_profile.set(user[4])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete])
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
            # Habilitar el botón "Editar"
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Usuario no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        user = {
            'user_id': self.ent_user_id.get(),
            'name': self.ent_name.get(),
            'username': self.ent_username.get(),
            'password': self.ent_password.get(),
            'profile': self.ent_profile.get()
        }
        self.db.update_user(user)
        messagebox.showinfo("Éxito", "Usuario actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_user_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de usuario.")
            return
        user_id = self.ent_user_id.get()
        self.db.delete_user(user_id)
        messagebox.showinfo("Éxito", "Usuario eliminado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_user_id.get()
            or not self.ent_name.get()
            or not self.ent_username.get()
            or not self.ent_password.get()
            or not self.ent_profile.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_user_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_username.delete(0, END)
        self.ent_password.delete(0, END)
        self.ent_profile.set("")

    def enable_entries(self):
        self.ent_user_id["state"] = "normal"
        self.ent_name["state"] = "normal"
        self.ent_username["state"] = "normal"
        self.ent_password["state"] = "normal"
        self.ent_profile["state"] = "normal"

    def disable_entries(self):
        self.ent_user_id["state"] = "disabled"
        self.ent_name["state"] = "disabled"
        self.ent_username["state"] = "disabled"
        self.ent_password["state"] = "disabled"
        self.ent_profile["state"] = "disabled"
#~~~~~~~~~~~~~ClassAPP---------Customers/clientes~~~~~~~~~~~~~
class CustomerApp:
    def __init__(self, root, db, user_id, username):
        self.root = root
        self.root.title("Gestión de Clientes")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username  # Nuevo atributo username


        # Crear widgets
        self.lbl_customer_id = tk.Label(root, text="ID de Cliente:")
        self.lbl_customer_id.place(x=10, y=10)
        self.ent_customer_id = tk.Entry(root, state="readonly")
        self.ent_customer_id.place(x=130, y=10)

        self.lbl_name = tk.Label(root, text="Nombre:")
        self.lbl_name.place(x=10, y=40)
        self.ent_name = tk.Entry(root, state= "disabled")
        self.ent_name.place(x=130, y=40)

        self.lbl_phone = tk.Label(root, text="Teléfono:")
        self.lbl_phone.place(x=10, y=70)
        self.ent_phone = tk.Entry(root, state= "disabled")
        self.ent_phone.place(x=130, y=70)

        self.lbl_user_id = tk.Label(root, text="ID de Usuario:")
        self.lbl_user_id.place(x=10, y=100)
        self.ent_user_id = tk.Entry(root, state= "normal")
        self.ent_user_id.place(x=130, y=100)
        self.ent_user_id.insert(0, self.user_id)

        self.lbl_username = tk.Label(root, text="Nombre de usuario:")
        self.lbl_username.place(x=10, y=130)
        self.ent_username = tk.Entry(root, state="normal")
        self.ent_username.place(x=130, y=130)
        self.ent_username.insert(0, self.username)  # Rellena automáticamente con el nombre de usuario

        self.btn_insert = tk.Button(root, text="Guardar", command=self.insert, state= "disabled")
        self.btn_insert.place(x=80, y=160)

        self.btn_cancel = tk.Button(root, text="Cancelar", command=self.cancel, state= "disabled")
        self.btn_cancel.place(x=150, y=160)

        self.btn_new = tk.Button(root, text="Nuevo", command=self.new_customer)
        self.btn_new.place(x=10, y=160)

        self.btn_search = tk.Button(root, text="Buscar", command=self.search_customer)
        self.btn_search.place(x=370, y=40)

        self.btn_edit = tk.Button(root, text="Editar", command=self.edit, state= "disabled")
        self.btn_edit.place(x=230, y=160)

        self.btn_delete = tk.Button(root, text="Eliminar", command=self.delete, state= "disabled")
        self.btn_delete.place(x=300, y=160)

        # Crear el nuevo cuadro de texto para buscar clientes por ID
        self.lbl_search_id = tk.Label(root, text="Buscar por ID:")
        self.lbl_search_id.place(x=290, y=10)
        self.ent_search_id = tk.Entry(root)
        self.ent_search_id.place(x=380, y=10)

    def new_customer(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        # Obtener el siguiente ID de cliente de la base de datos
        self.current_customer_id = self.db.get_next_customer_id()
        self.ent_customer_id.insert(0, self.current_customer_id)

    def insert(self):
        if not self.validate_fields():
            return
        user_id = self.ent_user_id.get()
        if not self.db.search_user_by_id(user_id):
            messagebox.showerror("Error", f"El usuario con ID {user_id} no está registrado.")
            return
        customer = {
            'customer_id': self.ent_customer_id.get(),
            'name': self.ent_name.get(),
            'phone': self.ent_phone.get(),
            'user_id': self.ent_user_id.get()
        }
        self.db.save_customer(customer)
        messagebox.showinfo("Éxito", "Cliente insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search_customer(self):
        customer_id_or_name = self.ent_search_id.get()
        if customer_id_or_name.isdigit():  # Si la entrada es un número, buscar por ID
            customer = self.db.search_customer_by_id(customer_id_or_name)
        else:  # Si no, buscar por nombre
            customer = self.db.search_customer_by_name(customer_id_or_name)
        
        if customer:
            self.ent_customer_id.delete(0, END)
            self.ent_name.delete(0, END)
            self.ent_phone.delete(0, END)
            self.ent_user_id.delete(0, END)

            self.ent_customer_id.insert(0, customer[0])
            self.ent_name.insert(0, customer[1])
            self.ent_phone.insert(0, customer[2])
            self.ent_user_id.insert(0, customer[3])

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete])
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
            # Habilitar el botón "Editar"
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Cliente no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        customer = {
            'customer_id': self.ent_customer_id.get(),
            'name': self.ent_name.get(),
            'phone': self.ent_phone.get(),
            'user_id': self.ent_user_id.get()
        }
        self.db.update_customer(customer)
        messagebox.showinfo("Éxito", "Cliente actualizado con éxito.")
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_customer_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de cliente.")
            return
        customer_id = self.ent_customer_id.get()
        self.db.delete_customer(customer_id)
        messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_customer_id.get()
            or not self.ent_name.get()
            or not self.ent_phone.get()
            or not self.ent_user_id.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_customer_id.delete(0, END)
        self.ent_name.delete(0, END)
        self.ent_phone.delete(0, END)
        #self.ent_user_id.delete(0, END)

    def enable_entries(self):
        self.ent_customer_id["state"] = "normal"
        self.ent_name["state"] = "normal"
        self.ent_phone["state"] = "normal"
        self.ent_user_id["state"] = "normal"

    def disable_entries(self):
        self.ent_customer_id["state"] = "disabled"
        self.ent_name["state"] = "disabled"
        self.ent_phone["state"] = "disabled"
        self.ent_user_id["state"] = "disabled"

def open_customer_menu(self):
        customer_window = tk.Tk()
        customer_window.title("Menú de Clientes")
        customer_window.geometry("600x400")
        customer_app = CustomerApp(customer_window, self.db, self.user_id, self.username)
        
        customer_window.mainloop()

#~~~~~~~~~~~~ClassAPP-------------CARROS/VEHICLES~~~

class CarApp:
    def __init__(self, root, db, customer_names):
        self.root = root
        self.root.title("Gestión de Vehículos")
        self.db = db
        self.current_car_id = None
        self.selected_customer_id = None
        #customer_names = self.db.get_all_customer_names()


        # Crear widgets
        self.lbl_car_id = tk.Label(root, text="ID de Vehículo:")
        self.lbl_car_id.place(x=10, y=10)
        self.ent_car_id = tk.Entry(root)
        self.ent_car_id.place(x=130, y=10)

        self.lbl_matricula = tk.Label(root, text="Matrícula:")
        self.lbl_matricula.place(x=10, y=40)
        self.ent_matricula = tk.Entry(root, state= "disabled")
        self.ent_matricula.place(x=130, y=40)

        self.lbl_marca = tk.Label(root, text="Marca:")
        self.lbl_marca.place(x=10, y=70)
        self.ent_marca = tk.Entry(root, state= "disabled")
        self.ent_marca.place(x=130, y=70)

        self.lbl_modelo = tk.Label(root, text="Modelo:")
        self.lbl_modelo.place(x=10, y=100)
        self.ent_modelo = tk.Entry(root)
        self.ent_modelo.place(x=130, y=100)

        self.lbl_fecha = tk.Label(root, text="Fecha:")
        self.lbl_fecha.place(x=10, y=130)
        self.ent_fecha = tk.Entry(root)  # Campo de solo lectura para la fecha
        self.ent_fecha.place(x=130, y=130)
    
        self.lbl_cliente = tk.Label(root, text="Cliente:")
        self.lbl_cliente.place(x=10, y=160)
        self.combo_cliente = ttk.Combobox(root)
        self.combo_cliente.place(x=130, y=160)
        self.combo_cliente['values'] = customer_names
        
        self.lbl_cliente_id = tk.Label(root, text="ID del Cliente:")
        self.lbl_cliente_id.place(x=280, y=160)
        self.lbl_cliente_info = tk.Entry(root, text ="")
        self.lbl_cliente_info.place(x=400, y=160)

        # Crear el nuevo cuadro de texto para mostrar el ID del cliente seleccionado
        self.lbl_cliente_info = tk.Entry(root)
        self.lbl_cliente_info.place(x=400, y=160)

        # Asociar evento de selección de la Combobox con la actualización del ID del cliente
        self.combo_cliente.bind("<<ComboboxSelected>>", self.update_customer_id)

        # Botones
        self.btn_insert = tk.Button(root, text="Guardar", command=self.insert, state= "disabled")
        self.btn_insert.place(x=80, y=190)

        self.btn_cancel = tk.Button(root, text="Cancelar", command=self.cancel, state= "disabled")
        self.btn_cancel.place(x=150, y=190)

        self.btn_new = tk.Button(root, text="Nuevo", command=self.new_car)
        self.btn_new.place(x=10, y=190)

        self.btn_search = tk.Button(root, text="Buscar", command=self.search_car)
        self.btn_search.place(x=370, y=40)

        self.btn_edit = tk.Button(root, text="Editar", command=self.edit, state= "disabled")
        self.btn_edit.place(x=230, y=190)

        self.btn_delete = tk.Button(root, text="Eliminar", command=self.delete, state= "disabled")
        self.btn_delete.place(x=300, y=190)

        # Crear el nuevo cuadro de texto para buscar vehículos por ID, matrícula o nombre de cliente
        self.lbl_search = tk.Label(root, text="Buscar:")
        self.lbl_search.place(x=290, y=10)
        self.ent_search = tk.Entry(root)
        self.ent_search.place(x=380, y=10)


    def update_customer_id(self, event):
        # Obtener el índice seleccionado en la Combobox
        selected_index = self.combo_cliente.current()
        if selected_index != -1:  # Asegurarse de que se haya seleccionado un cliente
            # Obtener el ID del cliente correspondiente al índice seleccionado
            customer_id = self.db.get_customer_id_by_index(selected_index)
            # Mostrar el ID del cliente en el Entry correspondiente
            self.lbl_cliente_info.delete(0, tk.END)
            self.lbl_cliente_info.insert(0, str(customer_id))

    def new_car(self):
    # Verificar el perfil del usuario actual
        #if self.user_profile in ["Secre", "Mecanico"]:
            # Si el usuario es "Secre" o "Mecanico", desactivar los botones
        #   self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        #else:
            # Si el usuario no es "Secre" ni "Mecanico", permitir la creación de un nuevo vehículo
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_insert, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])
        self.current_car_id = self.db.get_next_car_id()
        self.ent_car_id.insert(0, self.current_car_id)
        self.ent_fecha.insert(0, datetime.datetime.now().strftime("%d-%m-%Y"))


    
    def insert(self):
        if not self.validate_fields():
            return
        
        matricula = self.ent_matricula.get()
        # Consultar si la matrícula ya existe en la base de datos
        existing_vehicle = self.db.search_vehicle_by_license_plate(matricula)
        if existing_vehicle:
            messagebox.showerror("Error", "La matrícula ya existe en la base de datos.")
            return
        
        cliente_seleccionado = self.combo_cliente.get()
        cliente_id = self.db.get_customer_id_by_name(cliente_seleccionado)
        if cliente_id is None:
            messagebox.showerror("Error", "No se encontró el ID del cliente.")
            return
        car = {
            'license_plate': self.ent_matricula.get(),
            'brand': self.ent_marca.get(),
            'model': self.ent_modelo.get(),
            'registration_date': datetime.datetime.now().strftime("%Y-%m-%d"),  # Fecha actual
            'customer_id': cliente_id
        }
        self.db.save_vehicle(car)
        messagebox.showinfo("Éxito", "Vehículo insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

            
    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

    def search_car(self):
        matricula = self.ent_search.get()
        car = self.db.search_vehicle_by_license_plate(matricula)
        if car:
            self.enable_entries()
            self.ent_car_id.delete(0, END)
            self.ent_matricula.delete(0, END)
            self.ent_marca.delete(0, END)
            self.ent_modelo.delete(0, END)
            self.ent_fecha.delete(0, END)
            self.combo_cliente.delete(0, END)

            self.ent_car_id.insert(0, car[0])  # Indice 0 para vehicle_id
            self.ent_matricula.insert(0, car[1])  # Indice 1 para license_plate
            self.ent_marca.insert(0, car[2])  # Indice 2 para brand
            self.ent_modelo.insert(0, car[3])  # Indice 3 para model
            self.ent_fecha.insert(0, car[4])  # Indice 4 para registration_date

            cliente_id = car[5]  # Indice 5 para customer_id
            cliente = self.db.search_customer_by_id(cliente_id)
            cliente_nombre = cliente[1] if cliente else ""
            self.combo_cliente.insert(0, f" {cliente_nombre}")
            # Insertar el ID del cliente en el Entry correspondiente
            self.lbl_cliente_info.delete(0, tk.END)
            self.lbl_cliente_info.insert(0, cliente_id)

            self.disable_buttons([self.btn_new, self.btn_insert])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])
            self.enable_entries()
            # Actualizar el contenido del Label con el ID y nombre del cliente seleccionado
            self.lbl_cliente_info.config(text=f"{cliente_id}: {cliente_nombre}")
            self.ent_matricula.config(state="readonly")
        else:
            messagebox.showinfo("Error", "Vehículo no encontrado.")


    def edit(self):
        if not self.validate_fields():
            return

        # Obtener los valores de las cajas de texto y combobox
        car_id = self.ent_car_id.get()
        matricula = self.ent_matricula.get()
        # Consultar si la matrícula ya existe en la base de datos
        existing_vehicle = self.db.search_vehicle_by_license_plate(matricula)
        if existing_vehicle and existing_vehicle[0] != car_id:  # Se compara el ID del vehículo en la posición 0 de la tupla
            messagebox.showerror("Error", "La matrícula ya existe en la base de datos.")
            return

        marca = self.ent_marca.get()
        modelo = self.ent_modelo.get()
        fecha = self.ent_fecha.get()
        cliente_info = self.lbl_cliente_info.get()  # Obtener el ID del cliente desde lbl_cliente_info
        car = {
            'vehicle_id': car_id,
            'license_plate': matricula,
            'brand': marca,
            'model': modelo,
            'registration_date': fecha,
            'customer_id': cliente_info.split(':')[0]  # Separar el ID del cliente del nombre y obtener solo el ID
        }
        # Llamar al método update_vehicle para actualizar los datos en la base de datos
        self.db.update_vehicle(car)
        messagebox.showinfo("Éxito", "Vehículo actualizado con éxito.")


    def delete(self):
        car_id = self.ent_car_id.get()
        if messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar este vehículo?"):
            self.db.delete_car(car_id)
            messagebox.showinfo("Éxito", "Vehículo eliminado con éxito.")
            self.cancel()

    def clear_entries(self):
        self.ent_car_id.delete(0, END)
        self.ent_matricula.delete(0, END)
        self.ent_marca.delete(0, END)
        self.ent_modelo.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.combo_cliente.delete(0, END)

    def enable_entries(self):
        self.ent_matricula.config(state="normal")
        self.ent_marca.config(state="normal")
        self.ent_modelo.config(state="normal")
        self.combo_cliente.config(state="normal")

    def disable_entries(self):
        self.ent_matricula.config(state="readonly")
        self.ent_marca.config(state="readonly")
        self.ent_modelo.config(state="readonly")
        self.combo_cliente.config(state="readonly")

    def enable_buttons(self, buttons):
        for btn in buttons:
            btn.config(state="normal")

    def disable_buttons(self, buttons):
        for btn in buttons:
            btn.config(state="disabled")

    def validate_fields(self):
        if (not self.ent_matricula.get()) or (not self.ent_marca.get()) or (not self.ent_modelo.get()) or \
                (not self.combo_cliente.get()):
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return False
        return True

def open_cars_menu(self):
    cars_window = tk.Tk()
    cars_window.title("Menú de Vehículos")
    cars_window.geometry("600x400")
    # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
    customer_names = self.db.get_all_customer_names()
    cars_app = CarApp(cars_window, self.db, customer_names)    
    cars_window.mainloop()

#~~~~~~~~~~~~ClassAPP-------------PIECES~~~~~~~~~
class PiceApp:
    def __init__(self, root, db, user_id, username=None):
        self.root = root
        self.root.title("Gestión de Piezas")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username  # Nuevo atributo username
        
        #Crear widgets
        self.lbl_pice = tk.Label(root, text="Descripcion:")
        self.lbl_pice.place(x=10, y=100)
        self.ent_desc = tk.Entry(root)
        self.ent_desc.place(x=130, y=100)
        
        self.lbl_pice = tk.Label(root, text="ID:")
        self.lbl_pice.place(x=30, y=70)
        self.ent_pice_id = tk.Entry(root, state="readonly")
        self.ent_pice_id.place(x=130, y=70)
        
        self.lbl_pice = tk.Label(root, text="Stock:")
        self.lbl_pice.place(x=30, y=130)
        self.ent_stock = tk.Entry(root)
        self.ent_stock.place(x=130, y=130)
        
        # Crear el nuevo cuadro de texto para buscar clientes por ID
        self.lbl_search_id = tk.Label(root, text="Buscar pieza por ID:")
        self.lbl_search_id.place(x=30, y=10)
        self.ent_search_id = tk.Entry(root)
        self.ent_search_id.place(x=150, y=10)
        self.btn_search = tk.Button(root, text="Buscar", command=self.search)
        self.btn_search.place(x=280, y=10)
    
        #Botones CRUD
        self.btn_new = tk.Button(root, text="Nuevo", command=self.new_pice)
        self.btn_new.place(x=10, y=160)
        self.btn_save = tk.Button(root, text="Guardar", command=self.insert,state="disabled")
        self.btn_save.place(x=70, y=160)
        self.btn_cancel = tk.Button(root, text="Cancelar", command=self.cancel,state="disabled")
        self.btn_cancel.place(x=140, y=160)
        self.btn_edit = tk.Button(root, text="Editar", command=self.edit,state="disabled")
        self.btn_edit.place(x=220, y=160)
        self.btn_delete = tk.Button(root, text="Eliminar", command=self.delete,state="disabled")
        self.btn_delete.place(x=270, y=160)
        
    def new_pice(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_save, self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        # Obtener el siguiente ID de usuario de la base de datos
        self.current_pice_id = self.db.get_next_pice_id()
        self.ent_pice_id.insert(0, self.current_pice_id)

    def insert(self):
        if not self.validate_fields():
            return
        pice = {
            'pieza_id': self.ent_pice_id.get(),
            'descripcion': self.ent_desc.get(),
            'stock': self.ent_stock.get()
        }
        # Verificar si el stock es un número entero
        if not pice['stock'].isdigit():
            messagebox.showerror("Error", "El stock debe ser un número entero.")
            return
        # Convertir el stock a entero
        new_stock = int(pice['stock'])
        # Verificar si el nuevo stock es negativo
        if new_stock <= 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return
        # Guardar la pieza en la base de datos
        self.db.save_pice(pice)
        messagebox.showinfo("Éxito", "Pieza insertada con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.enable_buttons([self.btn_new])

    def validate_fields(self):
        if (
            not self.ent_pice_id.get()
            or not self.ent_desc.get()
            or not self.ent_stock.get().isdigit()  # Verificar si es un número entero
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios y el stock debe ser un número entero.")
            return False
        return True

    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_insert, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_id["state"] = "normal"

    def search(self):
        pice_id = self.ent_search_id.get()
        pice = self.db.search_pice_by_id(pice_id)
        if pice:
            self.ent_pice_id.delete(0, END)
            self.ent_desc.delete(0, END)
            self.ent_stock.delete(0, END)

            self.ent_pice_id.insert(0, pice[0])
            self.ent_desc.insert(0, pice[1])
            self.ent_stock.insert(0, pice[2])

            self.disable_buttons([self.btn_new, self.btn_save])
            self.enable_buttons([self.btn_edit, self.btn_delete, self.btn_cancel])
            self.enable_entries()
            self.ent_search_id["state"] = "normal"
            
            # Habilitar el botón "Editar"
            self.btn_edit["state"] = "normal"
        else:
            messagebox.showinfo("Error", "Pieza no encontrado.")

    def edit(self):
        if not self.validate_fields():
            return
        
        pice = {
            'pieza_id': self.ent_pice_id.get(),
            'descripcion': self.ent_desc.get(),
            'stock': self.ent_stock.get(),
        }
        # Verificar si el stock es un número entero
        # Verificar si la cantidad contiene solo dígitos
        if not re.match(r'^\d+$', pice['stock']):
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        if not pice['stock'].isdigit():
            messagebox.showerror("Error", "El stock debe ser un número entero.")
            return
        # Convertir el stock a entero
        new_stock = int(pice['stock'])
        # Verificar si el nuevo stock es negativo
        if new_stock <= 0:
            messagebox.showerror("Error", "El stock no puede ser negativo.")
            return
        self.db.update_pieza(pice)
        messagebox.showinfo("Éxito", "Pieza actualizada correctamente.")
        self.disable_entries()
        #self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])
        self.clear_entries()

    def delete(self):
        if not self.ent_pice_id.get():  # Aquí se cambió de ent_pice_id a ent_fol_id
            messagebox.showerror("Error", "Debe ingresar un ID de pieza valido.")
            return
        pice_id = self.ent_pice_id.get()  # También se cambió de ent_pice_id a ent_fol_id
        self.db.delete_pice(pice_id)
        messagebox.showinfo("Éxito", "Pieza eliminada con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_new, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])


    def validate_fields(self):
        if (
            not self.ent_pice_id.get()
            or not self.ent_desc.get()
            or not self.ent_stock.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        return True

    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_pice_id.delete(0, END)
        self.ent_desc.delete(0, END)
        self.ent_stock.delete(0, END)

    def enable_entries(self):
        self.ent_pice_id["state"] = "normal"
        self.ent_desc["state"] = "normal"
        self.ent_stock["state"] = "normal"

    def disable_entries(self):
        self.ent_pice_id["state"] = "disabled"
        self.ent_desc["state"] = "disabled"
        self.ent_stock["state"] = "disabled"

    def open_pice_menu(self):
        pice_window = tk.Tk()
        pice_window.title("Menú de Piezas")
        pice_window.geometry("600x400")
        # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
        customer_names = self.db.get_all_customer_names()
        pice_app = PiceApp(pice_window, self.db, customer_names)    
        pice_window.mainloop()
#~~~~~~~~~~ClassAPP-------------reparaciones~~~~~~~~~~~~
class RepairApp:
    def __init__(self, root, db, user_id, username=None):
        self.root = root
        self.root.title("Reparaciones")
        self.db = db
        self.current_customer_id = None
        self.user_id = user_id
        self.username = username  # Nuevo atributo username
        
        #Crear widgets
        self.lbl_folio_id = tk.Label(root, text="Folio:", state= "disabled")
        self.lbl_folio_id.place(x=20, y=40)
        self.ent_fol_id = tk.Entry(root)
        self.ent_fol_id.place(x=60, y=40)
        
        self.lbl_matricula = tk.Label(root, text="Matricula:", state= "disabled")
        self.lbl_matricula.place(x=20, y=70)
        self.combo_mat = ttk.Combobox(root)
        self.combo_mat.place(x=80, y=70)
        #falta por terminar
        #self.combo_mat['values'] = customer_names
        
        self.lbl_pieza = tk.Label(root, text="Seleccione una pieza:", state= "disabled")
        self.lbl_pieza.place(x=5, y=100)
        self.combo_pza = ttk.Combobox(root)
        self.combo_pza.place(x=120, y=100)
        #falta por terminar
        #self.combo_mat['values'] = pieza_names
        # Cargar datos en los combobox
        self.load_vehicle_data()
        self.load_piece_data()
        
        self.lbl_fecha = tk.Label(root, text="Fecha entrada:", state= "disabled")
        self.lbl_fecha.place(x=20, y=130)
        self.ent_fecha = tk.Entry(root)  # Campo de solo lectura para la fecha
        self.ent_fecha.place(x=110, y=130)
        self.lbl_fecha_salida = tk.Label(root, text="Fecha salida:", state="disabled")
        self.lbl_fecha_salida.place(x=20, y=160)
        self.ent_fecha_salida = tk.Entry(root)  # Campo de solo lectura para la fecha
        self.ent_fecha_salida.place(x=90, y=160)
        
        self.lbl_pice = tk.Label(root, text="Cantidad:", state= "disabled")
        self.lbl_pice.place(x=20, y=200)
        self.ent_stock = tk.Entry(root)
        self.ent_stock.place(x=80, y=200)
        
        self.lbl_falla = tk.Label(root, text="Falla:", state= "disabled")
        self.lbl_falla.place(x=20, y=240)
        self.ent_fall = tk.Entry(root)
        self.ent_fall.place(x=50, y=240)
        
        # Crear el nuevo cuadro de texto para buscar clientes por ID
        self.lbl_search_folio = tk.Label(root, text="Ingrese folio a buscar:")
        self.lbl_search_folio.place(x=90, y=10)
        self.ent_search_fol = tk.Entry(root)
        self.ent_search_fol.place(x=220, y=10)
        self.btn_search = tk.Button(root, text="Buscar", command=self.search)
        self.btn_search.place(x=360, y=10)
    
        #Botones CRUD
        self.btn_new = tk.Button(root, text="Nuevo", command=self.new_repair)
        self.btn_new.place(x=10, y=300)
        self.btn_save = tk.Button(root, text="Guardar", command=self.insert,state="disabled")
        self.btn_save.place(x=70, y=300)
        self.btn_cancel = tk.Button(root, text="Cancelar", command=self.cancel,state="disabled")
        self.btn_cancel.place(x=140, y=300)
        self.btn_edit = tk.Button(root, text="Editar", command=self.edit,state="disabled")
        self.btn_edit.place(x=220, y=300)
        self.btn_delete = tk.Button(root, text="Eliminar", command=self.delete,state="disabled")
        self.btn_delete.place(x=270, y=300)


        
    def open_repair_menu(self):
        repair_window = tk.Tk()
        repair_window.title("Menú de Reparaciones")
        repair_window.geometry("600x400")
        # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
        customer_names = self.db.get_all_customer_names()
        repair_app = RepairApp(repair_window, self.db, customer_names)    
        repair_window.mainloop()
            
    def new_repair(self):
        self.clear_entries()
        self.enable_entries()
        self.enable_buttons([self.btn_save,self.btn_cancel])
        self.disable_buttons([self.btn_new, self.btn_edit, self.btn_delete])

        # Obtener el siguiente ID de reparacion de la base de datos
        self.current_repair_id = self.db.get_next_repair_id()
        self.ent_fol_id.insert(0, self.current_repair_id)
        # Establecer la fecha de ingreso como la fecha actual
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        self.ent_fecha.insert(0, today)
        # Calcular la fecha de salida (un día después de la fecha de ingreso)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        self.ent_fecha_salida.insert(0, tomorrow.strftime("%Y-%m-%d"))
        self.ent_fol_id.config(state="readonly")
        
    
    def insert(self):
        if not self.validate_fields():
            return

        repair = {
            'reparacion_id': self.ent_fol_id.get(),
            'fecha_ingreso': self.ent_fecha.get(),
            'fecha_salida': self.ent_fecha_salida.get(),
            'stock': self.ent_stock.get(),
            'falla': self.ent_fall.get(),
            'pieza': self.combo_pza.get(),  # Aquí deberías usar el nombre de la pieza en lugar del ID si tienes solo el nombre en el combobox
            'matricula': self.combo_mat.get()  # Aquí deberías usar la matrícula del vehículo en lugar del ID si tienes solo la matrícula en el combobox
        }
        # Verificar si la cantidad contiene solo dígitos
        if not re.match(r'^\d+$', repair['stock']):
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        if int(repair['stock']) <= 0:
            messagebox.showerror("Error", "Cantidad no valida.")
            return

        # Verificar si la matrícula del vehículo existe en la base de datos
        if not self.db.check_vehicle_existence(repair['matricula']):
            messagebox.showerror("Error", "La matrícula del vehículo no existe en la base de datos.")
            return

        # Verificar si la pieza existe en la base de datos
        if not self.db.check_piece_existence(repair['pieza']):
            messagebox.showerror("Error", "La pieza no existe en la base de datos.")
            return

        
        # Validar que la fecha de salida sea mayor que la fecha de ingreso
        if repair['fecha_salida'] <= repair['fecha_ingreso']:
            messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de ingreso.")
            return

        # Obtener el ID de la pieza utilizando la descripción de la pieza
        pieza_id = self.db.get_piece_id_by_description(repair['pieza'])
        # Verificar si hay suficientes piezas en stock
        if pieza_id is not None and not self.db.check_stock_availability(pieza_id, repair['stock']):
            messagebox.showerror("Error", "No hay suficientes piezas en stock.")
            return
        self.db.save_repair(repair)
        messagebox.showinfo("Éxito", "Reparacion insertado con éxito.")
        self.clear_entries()
        self.disable_entries()
        #self.disable_buttons([self.btn_insert, self.btn_cancel])
        self.enable_buttons([self.btn_new])

            
    def cancel(self):
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_save, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])
        self.ent_search_fol["state"] = "normal"
            
        
        
    def validate_fields(self):
        if (
            not self.ent_fol_id.get()
            or not self.combo_mat.get()
            or not self.combo_pza.get()
            or not self.ent_fecha.get()
            or not self.ent_fecha_salida.get()
            or not self.ent_stock.get()
            or not self.ent_fall.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return False
        return True

    def search(self):
        repair_id = self.ent_search_fol.get()
        repair = self.db.search_repair_by_id(repair_id)
        if repair:
            self.ent_fol_id.delete(0, END)
            self.combo_mat.delete(0, END)
            self.combo_pza.delete(0, END)
            self.ent_fecha.delete(0, END)
            self.ent_fecha_salida.delete(0, END)
            self.ent_stock.delete(0, END)
            self.ent_fall.delete(0, END)

            self.ent_fol_id.insert(0, repair[0])  # reparacion_id
            self.combo_mat.insert(0, repair[1])    # matricula
            self.combo_pza.insert(0, repair[2])    # pieza
            self.ent_fecha.insert(0, repair[3])    # fecha_ingreso
            self.ent_fecha_salida.insert(0, repair[4])  # fecha_salida
            self.ent_stock.insert(0, repair[5])     # stock
            self.ent_fall.insert(0, repair[6])      # falla


            self.disable_buttons([self.btn_new, self.btn_save])
            self.enable_buttons([self.btn_edit, self.btn_delete])
            self.enable_entries()
            #self.ent_search_id["state"] = "normal"
                
            # Habilitar el botón "Editar"
            self.btn_edit["state"] = "normal"
            self.ent_fol_id.config(state="readonly")
        else:
            messagebox.showinfo("Error", "Reparacion no encontrado.")


    def edit(self):
        if not self.validate_fields():
            return
            
        repair = {
            'reparacion_id': self.ent_fol_id.get(),
            'matricula': self.combo_mat.get(),
            'pieza': self.combo_pza.get(),
            'fecha_ingreso': self.ent_fecha.get(),
            'fecha_salida': self.ent_fecha_salida.get(),
            'stock': self.ent_stock.get(),
            'falla': self.ent_fall.get(),
            'matricula': self.combo_mat.get(),
            'pieza': self.combo_pza.get(),
        }

        # Obtener el ID de la pieza utilizando la descripción de la pieza antes de la edición
        original_pieza_id = self.db.get_piece_id_by_description(self.combo_pza.get())

            # Verificar si la cantidad contiene solo dígitos
        if not re.match(r'^\d+$', repair['stock']):
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return

        if int(repair['stock']) <= 0:
            messagebox.showerror("Error", "Cantidad no válida.")
            return

        # Verificar si la matrícula del vehículo existe en la base de datos
        if not self.db.check_vehicle_existence(repair['matricula']):
            messagebox.showerror("Error", "La matrícula del vehículo no existe en la base de datos.")
            return

        # Verificar si la pieza existe en la base de datos
        if not self.db.check_piece_existence(repair['pieza']):
            messagebox.showerror("Error", "La pieza no existe en la base de datos.")
            return

        # Verificar que la fecha de salida no sea menor que la fecha de entrada
        if repair['fecha_salida'] < repair['fecha_ingreso']:
            messagebox.showerror("Error", "La fecha de salida no puede ser menor que la fecha de entrada.")
            return

        # Actualizar la reparación en la base de datos
        self.db.update_repair(repair)

        messagebox.showinfo("Éxito", "Reparación actualizada correctamente.")
        self.clear_entries()
        self.disable_entries()
        self.enable_buttons([self.btn_new])

    def delete(self):
        if not self.ent_fol_id.get():
            messagebox.showerror("Error", "Debe ingresar un ID de reparación válido.")
            return
        repair_id = self.ent_fol_id.get()
        self.db.delete_repair(repair_id)
        messagebox.showinfo("Éxito", "Reparación eliminada con éxito.")
        self.clear_entries()
        self.disable_entries()
        self.disable_buttons([self.btn_new, self.btn_cancel, self.btn_edit, self.btn_delete])
        self.enable_buttons([self.btn_new])

        
    def enable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "normal"

    def disable_buttons(self, buttons):
        for button in buttons:
            button["state"] = "disabled"

    def clear_entries(self):
        self.ent_fol_id.delete(0, END)
        self.combo_mat.delete(0, END)
        self.combo_pza.delete(0, END)
        self.ent_fecha.delete(0, END)
        self.ent_fecha_salida.delete(0, END)
        self.ent_stock.delete(0, END)
        self.ent_fall.delete(0, END)

    def enable_entries(self):
        self.ent_fol_id["state"] = "normal"
        self.combo_mat["state"] = "normal"
        self.combo_pza["state"] = "normal"
        self.ent_fecha["state"] = "normal"
        self.ent_fecha_salida["state"] = "normal"
        self.ent_stock["state"] = "normal"
        self.ent_fall["state"] = "normal"

    def disable_entries(self):
        self.ent_fol_id["state"] = "disabled"
        self.combo_mat["state"] = "disabled"
        self.combo_pza["state"] = "disabled"
        self.ent_fecha["state"] = "disabled"
        self.ent_fecha_salida["state"] = "disabled"
        self.ent_stock["state"] = "disabled"
        self.ent_fall["state"] = "disabled"

    def load_vehicle_data(self):
        # Obtener matrículas de vehículos desde la base de datos
        vehicles = self.db.get_all_vehicles()
        # Obtener solo las matrículas
        license_plates = [vehicle[1] for vehicle in vehicles]
        # Configurar los valores del combobox de matrículas
        self.combo_mat['values'] = license_plates

    def load_piece_data(self):
        # Obtener nombres de piezas desde la base de datos
        pieces = self.db.get_all_pieces()
        # Obtener solo los nombres de las piezas
        piece_names = [piece[1] for piece in pieces]
        # Configurar los valores del combobox de piezas
        self.combo_pza['values'] = piece_names

#~~~~~~~~~ClassAPP-------------LoginsPantalla~~~~~~~~~~~~~
class LoginWindow:
    def __init__(self, root, db):
        self.root = root
        self.root.title("Login")
        self.db = db
        self.user_db = None
        self.username = None
        self.user_id = None
        
        self.label_username = tk.Label(root, text="Usuario:")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()
        
        self.label_password = tk.Label(root, text="Contraseña:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()
        
        self.button_login = tk.Button(root, text="Iniciar sesión", command=self.login)
        self.button_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        # Verificar si las credenciales son para el usuario "admin"
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Exitoso", "Bienvenido, admin!")
            self.root.destroy()
            self.open_menu()
        else:
            # Verificar si las credenciales corresponden a un usuario registrado en la base de datos
            user = self.db.search_user_by_username(username)
            if user and user[3] == password:
                # Establecer los atributos user_id y username aquí
                self.user_id = user[0]
                self.username = user[2]
                # Si el usuario es "Admin", abrir el menú completo
                if user[4] == "Admin":
                    messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
                    self.root.destroy()
                    self.open_menu()
                # Si el usuario es "Secre", abrir un menú específico para secretarios
                elif user[4] == "Secre":
                    messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
                    self.root.destroy()
                    self.open_secre_menu()
                # Si el usuario es "Mecanico", mostrar un mensaje de error
                elif user[4] == "Mecanico":
                    messagebox.showinfo("Login Exitoso", "Bienvenido, {}!".format(username))
                    self.root.destroy()
                    self.open_mecanico_menu()
                    
            else:
                messagebox.showerror("Error de inicio de sesión", "Datos incorrectos.")

    def open_menu(self):
        
        menu_window = tk.Tk()
        menu_window.title("Menú")
        
        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Users", command=self.open_user_menu)
        file_menu.add_command(label="Customers", command=self.open_customer_menu)
        file_menu.add_command(label="Cars", command= self.open_cars_menu)
        file_menu.add_command(label="Pieces", command= self.open_pice_menu)
        file_menu.add_command(label="Repairs", command= self.open_repair_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=menu_window.destroy)
        menu_bar.add_cascade(label="Menú", menu=file_menu)


        #  Botón "Login" para regresar a la pantalla de inicio de sesión
        login_button = tk.Button(menu_window, text="Login", command=self.show_login_window)
        login_button.pack()

        menu_window.geometry("400x350")
        menu_window.mainloop()


    def open_secre_menu(self):
        menu_window = tk.Tk()
        menu_window.title("Menú")
        
        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        #file_menu.add_command(label="User", command=self.open_user_menu)
        file_menu.add_command(label="Customers", command=self.open_customer_menu)
        file_menu.add_command(label="Cars", command= self.open_cars_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=menu_window.destroy)
        menu_bar.add_cascade(label="Menú", menu=file_menu)


        # Agregar un botón "Login" para regresar a la pantalla de inicio de sesión
        login_button = tk.Button(menu_window, text="Login", command=self.show_login_window)
        login_button.pack()

        menu_window.geometry("300x200")
        menu_window.mainloop()

    def open_mecanico_menu(self):
        menu_window = tk.Tk()
        menu_window.title("Menú")
        
        menu_bar = tk.Menu(menu_window)
        menu_window.config(menu=menu_bar)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        #file_menu.add_command(label="User", command=self.open_user_menu)
        #file_menu.add_command(label="Customers", command=self.open_customer_menu)
        file_menu.add_command(label="Cars", command= self.open_cars_menu)
        file_menu.add_command(label="Repair", command= self.open_repair_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=menu_window.destroy)
        menu_bar.add_cascade(label="Menú", menu=file_menu)


        # Agregar un botón "Login" para regresar a la pantalla de inicio de sesión
        login_button = tk.Button(menu_window, text="Login", command=self.show_login_window)
        login_button.pack()

        menu_window.geometry("300x200")
        menu_window.mainloop()


    def open_user_menu(self):
        #user_window = tk.Tk()
        #user_window.title("Menú de Usuario")
        
        app_root = tk.Tk()  # Crea una nueva ventana
        app = App(app_root)  # Crea una instancia de App en la nueva ventana
        app_root.geometry("600x400")
        app_root.mainloop()

        #user_window.mainloop()

    def open_customer_menu(self):
        customer_window = tk.Tk()
        customer_window.title("Menú de Clientes")
        customer_window.geometry("600x400")
        customer_app = CustomerApp(customer_window, self.db, self.user_id, self.username)
        
        customer_window.mainloop()

    def show_login_window(self):
        login_window = tk.Tk()
        login_app = LoginWindow(login_window, self.db)
        login_window.geometry("600x400")
        login_window.mainloop()

    def open_cars_menu(self):
        cars_window = tk.Tk()
        cars_window.title("Menú de Vehículos")
        cars_window.geometry("600x400")
        # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
        customer_names = self.db.get_all_customer_names()
        cars_app = CarApp(cars_window, self.db, customer_names)    
        cars_window.mainloop()
    
    def open_pice_menu(self):
        pice_window = tk.Tk()
        pice_window.title("Menú de Piezas")
        pice_window.geometry("600x400")
        # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
        customer_names = self.db.get_all_customer_names()
        pice_app = PiceApp(pice_window, self.db, customer_names)    
        pice_window.mainloop()
        
    def open_repair_menu(self):
        repair_window = tk.Tk()
        repair_window.title("Menú de Reparaciones")
        repair_window.geometry("600x400")
        # Crear una instancia de CustomerApp y pasarle la ventana de vehículos y la instancia de DBManager
        customer_names = self.db.get_all_customer_names()
        repair_app = RepairApp(repair_window, self.db, customer_names)    
        repair_window.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    db = DBManager()
    login_app = LoginWindow(root,db)
    root.geometry("600x400")
    root.mainloop()
