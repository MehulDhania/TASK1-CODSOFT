import mysql.connector as sql
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime

mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com')
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS contact_book")
mycursor.execute("USE contact_book")
mycursor.execute("CREATE TABLE IF NOT EXISTS contact (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), phone_number VARCHAR(11),\
    email VARCHAR(50), address VARCHAR(100), date DATE, time TIME);")
mydb.commit()

mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
day = datetime.date.today()
time = datetime.datetime.now()
str_today = time.date().isoformat()
str_now = time.time().isoformat()
mycursor = mydb.cursor()


def add_contact(name, phone_number, email, address, str_today, str_now):
    mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
    mycursor = mydb.cursor()
    query = "INSERT INTO contact (name, phone_number, email, address, date, time) VALUES ('{}','{}' ,'{}', '{}', '{}','{}')".format(name, phone_number, email, address, str_today, str_now)
    mycursor.execute(query)
    mydb.commit()
    mydb.close()


# Search contact function
def search_contact(search_term):
    mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
    mycursor = mydb.cursor()
    query = "SELECT * FROM contact WHERE name LIKE '{}' OR phone_number LIKE '{}'".format(search_term,search_contact)
    mycursor.execute(query)
    myrecord = mycursor.fetchall()
    mydb.close()
    return myrecord  



def update_contact(contact_id, name, phone_number, email, address):
    mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
    mycursor = mydb.cursor()
    query = "UPDATE contact SET name='{}', phone_number='{}', email='{}', address='{}' WHERE id='{}'".format(name, phone_number, email, address, contact_id)
    mycursor.execute(query)
    mydb.commit()
    mydb.close()
    messagebox.showinfo("Success", "Contact updated successfully!")


def view_contacts():
    mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, name, phone_number, email, address FROM contact")
    myrecord = mycursor.fetchall()
    mydb.close()
    return myrecord 


def delete_contact(contact_id):
    mydb = sql.connect(host='localhost', user='root', passwd='mehul02@.com', database='contact_book')
    mycursor = mydb.cursor()
    query = "DELETE FROM contact WHERE id = '{}'".format(contact_id)
    mycursor.execute(query)
    mydb.commit()
    mydb.close()
    messagebox.showinfo("Success", "Contact deleted successfully!")


def contact_management_gui():
    root = tk.Tk()
    root.title("Contact Management System")
    root.geometry("800x600")


    img = Image.open(r'C:\Users\mehul\OneDrive\Desktop\Contact Book\images.jpeg')  # Correct image path
    img = img.resize((800, 600), Image.ANTIALIAS) 
    background_image = ImageTk.PhotoImage(img)

 
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)

 
    form_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge")
    form_frame.place(x=50, y=30, width=700, height=250)

    tk.Label(form_frame, text="Contact Management", font=("Helvetica", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

    # Name Input
    tk.Label(form_frame, text="Name", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5)
    name_var = tk.StringVar()
    name_entry = ttk.Entry(form_frame, textvariable=name_var, width=30)
    name_entry.grid(row=1, column=1, pady=5)

    # Phone Number Input
    tk.Label(form_frame, text="Phone Number", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
    phone_var = tk.StringVar()
    phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
    phone_entry.grid(row=2, column=1, pady=5)

    # Email Input
    tk.Label(form_frame, text="Email", font=("Helvetica", 12), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5)
    email_var = tk.StringVar()
    email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
    email_entry.grid(row=3, column=1, pady=5)

    # Address Input
    tk.Label(form_frame, text="Address", font=("Helvetica", 12), bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5)
    address_var = tk.StringVar()
    address_entry = ttk.Entry(form_frame, textvariable=address_var, width=30)
    address_entry.grid(row=4, column=1, pady=5)

    # Add Contact Function
    def submit_add_contact():
        name = name_var.get()
        phone = phone_var.get()
        email = email_var.get()
        address = address_var.get()
        if name and phone:
            add_contact(name, phone, email, address, str_today, str_now)
            clear_form()
            show_contacts() 
        else:
            messagebox.showwarning("Input Error", "Name and Phone are required fields!")

    # Clear Form Function
    def clear_form():
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

    # Function to fill the form with selected contact's data
    def fill_form(contact):
        name_var.set(contact[1])
        phone_var.set(contact[2])
        email_var.set(contact[3])
        address_var.set(contact[4])

    # Function to handle updating a contact
    def update_contact_in_db():
        selected = contact_list.selection()
        if selected:
            contact_id = contact_list.item(selected, 'values')[0]
            name = name_var.get()
            phone = phone_var.get()
            email = email_var.get()
            address = address_var.get()
            if name and phone:
                update_contact(contact_id, name, phone, email, address)
                clear_form()
                show_contacts()  # Refresh the contact list
            else:
                messagebox.showwarning("Input Error", "Name and Phone are required fields!")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to update!")

    # Function to delete a contact
    def delete_contact_from_db():
        selected = contact_list.selection()
        if selected:
            contact_id = contact_list.item(selected, 'values')[0]
            delete_contact(contact_id)
            clear_form()
            show_contacts()  # Refresh the contact list
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete!")

    # Buttons for Add, Update, Delete, and Clear
    button_frame = tk.Frame(form_frame, bg="#ffffff")
    button_frame.grid(row=1, column=4, columnspan=2, pady=10)

    ttk.Button(button_frame, text="Add Contact", command=submit_add_contact).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Update Contact", command=update_contact_in_db).grid(row=0, column=1, padx=10)
    ttk.Button(button_frame, text="Delete Contact", command=delete_contact_from_db).grid(row=1, column=0, padx=10)
    ttk.Button(button_frame, text="Clear Form", command=clear_form).grid(row=1, column=1, padx=10)

    # Search Frame
    search_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge")
    search_frame.place(x=50, y=270, width=700, height=100)

    tk.Label(search_frame, text="Search Contacts", font=("Helvetica", 14, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_frame, textvariable=search_var, width=50)
    search_entry.grid(row=1, column=0, pady=5)

    # Search Function
    def search_contacts():
        search_term = search_var.get()
        contact_list.delete(*contact_list.get_children())
        contacts = search_contact(search_term)
        for contact in contacts:
            contact_list.insert('', 'end', values=(contact[0], contact[1], contact[2], contact[3], contact[4]))

    ttk.Button(search_frame, text="Search", command=search_contacts).grid(row=1, column=1, padx=10)

    # Contacts List Frame
    list_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge")
    list_frame.place(x=50, y=370, width=700, height=200)

    contact_list = ttk.Treeview(list_frame, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
    contact_list.column("ID", width=30)
    contact_list.column("Name", width=150)
    contact_list.column("Phone", width=100)
    contact_list.column("Email", width=150)
    contact_list.column("Address", width=200)

    contact_list.heading("ID", text="ID")
    contact_list.heading("Name", text="Name")
    contact_list.heading("Phone", text="Phone")
    contact_list.heading("Email", text="Email")
    contact_list.heading("Address", text="Address")

    contact_list.pack(fill="both", expand=True)

    # Function to display all contacts in the list
    def show_contacts():
        contact_list.delete(*contact_list.get_children())  # Clear previous entries
        contacts = view_contacts()
        for contact in contacts:
            contact_list.insert('', 'end', values=(contact[0], contact[1], contact[2], contact[3], contact[4]))

    # Bind the list to allow selection of a contact for update/delete
    def on_select(event):
        selected = contact_list.selection()
        if selected:
            contact_id = contact_list.item(selected, 'values')[0]
            contact = search_contact(contact_id)
            if contact:
                fill_form(contact[0])  # Prepopulate form with contact details

    contact_list.bind('<<TreeviewSelect>>', on_select)

    show_contacts()  # Display all contacts on start

    root.background_image = background_image  # Prevent garbage collection of the image
    root.mainloop()


if __name__ == "__main__":
    contact_management_gui()
