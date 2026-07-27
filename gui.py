import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from core import add_device, update_status, delete_device, find_device,find_devices_by_name, save_to_csv, load_from_csv, devices
from tkcalendar import DateEntry

# ---------------------- Main Window ----------------------

window = tk.Tk()
window.title("Medical Devices Manager")
window.geometry("1150x500")
window.resizable(False, False)

# ---------------------- Title ----------------------

title_label = tk.Label(window, text="Medical Devices Manager", font=("Arial", 20, "bold"))
title_label.pack(pady=10)
# ---------------------- Buttons Frame ----------------------

buttons_frame = tk.Frame(window)
buttons_frame.pack(pady=10)

add_btn = tk.Button(buttons_frame, text="Add Device", width=15, command=lambda: open_add_window())
add_btn.grid(row=0, column=0, padx=10)

update_btn = tk.Button(buttons_frame, text="Update Status", width=15, command=lambda: open_update_window())
update_btn.grid(row=0, column=1, padx=10)

delete_btn = tk.Button(buttons_frame, text="Delete Device", width=15, command=lambda: open_delete_window())
delete_btn.grid(row=0, column=2, padx=10)

search_btn = tk.Button(buttons_frame, text="Search by ID", width=15, command=lambda: open_search_window())
search_btn.grid(row=0, column=3, padx=10)

search_name_btn = tk.Button(buttons_frame, text="Search by Name", width=15, command=lambda: open_search_by_name_window())
search_name_btn.grid(row=0, column=4, padx=10)

save_btn = tk.Button(buttons_frame, text="Save to CSV", width=15, command=lambda: save_devices_gui())
save_btn.grid(row=0, column=5, padx=10)

load_btn = tk.Button(buttons_frame, text="Load from CSV", width=15, command=lambda: load_devices_gui())
load_btn.grid(row=0, column=6, padx=10)

# ---------------------- Table Frame ----------------------

table_frame = tk.Frame(window)
table_frame.pack(pady=10)

# ---------------------- Treeview (Table) ----------------------

columns = ("name", "id", "type", "status", "maintenance")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

tree.heading("name", text="Name")
tree.heading("id", text="ID")
tree.heading("type", text="Type")
tree.heading("status", text="Status")
tree.heading("maintenance", text="Maintenance Date")

tree.column("name", width=200)
tree.column("id", width=80)
tree.column("type", width=150)
tree.column("status", width=100)
tree.column("maintenance", width=150)

# Scrollbar
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(side="left")

def open_add_window():
    add_window = tk.Toplevel(window)
    add_window.title("Add Device")

    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()

    tk.Label(add_window, text="ID:").pack()
    id_entry = tk.Entry(add_window)
    id_entry.pack()

    tk.Label(add_window, text="Type:").pack()
    type_entry = tk.Entry(add_window)
    type_entry.pack()

    tk.Label(add_window, text="Maintenance Date:").pack()

    from tkcalendar import DateEntry
    date_entry = DateEntry(add_window, date_pattern="yyyy-mm-dd")
    date_entry.pack()

    tk.Button(
        add_window,
        text="Add",
        command=lambda: add_device_from_gui(
            name_entry.get(),
            id_entry.get(),
            type_entry.get(),
            date_entry.get(),
            add_window
        )
    ).pack()

def open_update_window():
    update_win = tk.Toplevel(window)
    update_win.title("Update Device Status")
    update_win.geometry("350x250")
    update_win.resizable(False, False)

    tk.Label(update_win, text="Device ID:", font=("Arial", 12)).pack(pady=5)
    id_entry = tk.Entry(update_win, width=30)
    id_entry.pack()

    tk.Label(update_win, text="New Status (ok / warning / error):", font=("Arial", 12)).pack(pady=5)
    status_entry = tk.Entry(update_win, width=30)
    status_entry.pack()

    tk.Button(
        update_win,
        text="Update Status",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        command=lambda: update_status_from_gui(
            id_entry.get(),
            status_entry.get(),
            update_win
        )
    ).pack(pady=15)

def open_delete_window():
    delete_win = tk.Toplevel(window)
    delete_win.title("Delete Device")
    delete_win.geometry("300x200")
    delete_win.resizable(False, False)

    tk.Label(delete_win, text="Device ID:", font=("Arial", 12)).pack(pady=10)
    id_entry = tk.Entry(delete_win, width=30)
    id_entry.pack()

    tk.Button(
        delete_win,
        text="Delete",
        font=("Arial", 12, "bold"),
        bg="#F44336",
        fg="white",
        width=20,
        command=lambda: delete_device_from_gui(
            id_entry.get(),
            delete_win
        )
    ).pack(pady=20)


def open_search_window():
    search_win = tk.Toplevel(window)
    search_win.title("Search Device by ID")
    search_win.geometry("300x200")
    search_win.resizable(False, False)

    tk.Label(search_win, text="Device ID:", font=("Arial", 12)).pack(pady=10)
    id_entry = tk.Entry(search_win, width=30)
    id_entry.pack()

    tk.Button(
        search_win,
        text="Search",
        font=("Arial", 12, "bold"),
        bg="#9C27B0",
        fg="white",
        width=20,
        command=lambda: search_device_from_gui(
            id_entry.get(),
            search_win
        )
    ).pack(pady=20)   

def open_search_by_name_window():
    search_win = tk.Toplevel(window)
    search_win.title("Search Device by Name")
    search_win.geometry("300x200")
    search_win.resizable(False, False)

    tk.Label(search_win, text="Device Name:", font=("Arial", 12)).pack(pady=10)
    name_entry = tk.Entry(search_win, width=30)
    name_entry.pack()

    tk.Button(
        search_win,
        text="Search",
        font=("Arial", 12, "bold"),
        bg="#9C27B0",
        fg="white",
        width=20,
        command=lambda: search_by_name_from_gui(
            name_entry.get(),
            search_win
        )
    ).pack(pady=20)    

def save_devices_gui():
    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if filename:
        save_to_csv(filename)
        messagebox.showinfo("Success", "Devices saved successfully!")

def load_devices_gui():
    filename = filedialog.askopenfilename(
        filetypes=[("CSV Files", "*.csv")]
    )

    if filename:
        success, message = load_from_csv(filename)

        if not success:
            messagebox.showerror("Error", message)
            return

        refresh_table()
        messagebox.showinfo("Success", message)           

def add_device_from_gui(name, device_id, device_type, date, window_to_close):
    

    if not name.strip() or not device_id.strip() or not device_type.strip() or not date.strip():
        messagebox.showerror("Error", "All fields are required!")
        return

    success, message = add_device(name, device_id, device_type, date)

    if not success:
        messagebox.showerror("Error", message)
        return

    refresh_table()
    window_to_close.destroy()
    messagebox.showinfo("Success", message)

def update_status_from_gui(device_id, new_status, window_to_close):
    

    success, message = update_status(device_id, new_status)

    if not success:
        messagebox.showerror("Error", message)
        return

    refresh_table()
    window_to_close.destroy()
    messagebox.showinfo("Success", message) 

def delete_device_from_gui(device_id, window_to_close):
    
    success, message = delete_device(device_id)

    if not success:
        messagebox.showerror("Error", message)
        return

    refresh_table()
    window_to_close.destroy()
    messagebox.showinfo("Success",message )

def search_device_from_gui(device_id, window_to_close):
    

    device = find_device(device_id)

    if device:
        info = (
            f"Name: {device['name']}\n"
            f"ID: {device['id']}\n"
            f"Type: {device['type']}\n"
            f"Status: {device['status']}\n"
            f"Maintenance: {device['maintenance_date']}"
        )
        messagebox.showinfo("Device Found", info)
    else:
        messagebox.showerror("Not Found", "Device not found!")

    window_to_close.destroy()   

def search_by_name_from_gui(name_query, window_to_close):
   

    if not name_query.strip():
        messagebox.showerror("Error", "Please enter a name to search!")
        return

    results = find_devices_by_name(name_query)

    if results:
        info = ""
        for device in results:
            info += (
                f"Name: {device['name']}\n"
                f"ID: {device['id']}\n"
                f"Type: {device['type']}\n"
                f"Status: {device['status']}\n"
                f"Maintenance: {device['maintenance_date']}\n"
                f"{'-' * 30}\n"
            )
        messagebox.showinfo(f"Found {len(results)} Device(s)", info)
    else:
        messagebox.showerror("Not Found", "No devices found with that name!")

    window_to_close.destroy()


def refresh_table():
    # del old rows
    for row in tree.get_children():
        tree.delete(row)

    # refill table
    for d in devices:
        tree.insert("", "end", values=(
            d["name"],
            d["id"],
            d["type"],
            d["status"],
            d["maintenance_date"]
        ))



# ---------------------- Start GUI ----------------------

window.mainloop()