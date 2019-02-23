from tkinter import ttk
from tkinter import *
import sqlite3
import time #time.strftime("%d/%m/%y")


class Gestor:

    db_name = 'database.db'
    
    def __init__(self, win):
        self.wind = win
        self.wind.title("PRODUCTS APPLICATION")

        #Creating a Frame Container
        frame = LabelFrame(self.wind, text="Resgistrar nuevo producto")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        #Name input
        Label(frame, text= "Nombre: ").grid(row=1, column = 0)
        self.name = Entry(frame)
        self.name.grid(row=1, column=1)
        self.name.focus()

        #Price input
        Label(frame, text= "Precio: ").grid(row=2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        #Button Add Product
        ttk.Button(frame, text = "Save Product", command = self.add_product).grid(row=3, columnspan=2, sticky= W+E)

        #Output Messages
        self.message = Label(text = '', fg='red')
        self.message.grid(row= 3, column=0, columnspan=2, sticky= W+E)
       
        #Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column= 0, columnspan=2)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="Price", anchor=CENTER)

        #Buttons 
        ttk.Button(text='DELETE', command= self.delete_product).grid(row=5,column=0,sticky= W+E)
        ttk.Button(text='EDIT', command= self.edit_product).grid(row=5,column=1,sticky= W+E)

        #Filling the ROWS
        self.get_product()


    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            result = cursor.execute(query, parameters)
            con.commit()
            return result

    def get_product(self):
        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #Quering data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)

        #Print database in the table
        for row in db_rows:
            self.tree.insert('',0,text=row[1], values=row[2])


    def validate(self):
        return len(self.name.get())!= 0 and len(self.price.get())!=0

    def add_product(self):
        self.message['text']=''
        if self.validate():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['fg']= 'green'
            self.message['text'] = 'Product {} added succesfully'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['fg']= 'red'
            self.message['text'] = 'Name and price is required'
        self.get_product()

    def delete_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['fg']= 'purple'
            self.message['text'] = 'Please select a Record'
            return

        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name,)) #Coloco una coma para que el programa vea que se trata de una tupla
        self.message['fg']= 'red'
        self.message['text'] = 'Record {} Deleted'.format(name)
        self.get_product()
        

    def edit_product(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['fg']= 'purple'
            self.message['text'] = 'Please select a Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_win = Toplevel()
        self.edit_win.title = "Edit product"

        #Old Name
        Label(self.edit_win, text="Old Name: ").grid(row=0, column=1)
        Entry(self.edit_win, textvariable= StringVar(self.edit_win, value=name), state= "readonly").grid(row=0, column=2)

        #New Name
        Label(self.edit_win, text="New Name: ").grid(row=1, column=1)
        new_name = Entry(self.edit_win)
        new_name.grid(row=1, column=2)

        #Old Price
        Label(self.edit_win, text="Old Price: ").grid(row=2, column=1)
        Entry(self.edit_win, textvariable= StringVar(self.edit_win, value=old_price), state= "readonly").grid(row=2, column=2)
        
        #New Price
        Label(self.edit_win, text="New Price: ").grid(row=3, column=1)
        new_price = Entry(self.edit_win)
        new_price.grid(row=3, column=2)

        #Button
        Button(self.edit_win, text="Update", command= lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)

    def edit_records(self, new_name, name, new_price, old_price):
        if new_name == "":
            new_name = name
        if new_price == "":
            new_price = old_price

        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_win.destroy()
        self.message['fg']= 'green'
        self.message['text'] = 'Product {} updated succesfully'.format(name)
        self.get_product()


if __name__ == '__main__':
    root = Tk()
    app = Gestor(root)
    root.mainloop()