import tkinter as tk
from tkinter import ttk as ttk
import tkinter.scrolledtext as st
from tkinter import messagebox
from functools import partial

# should send all user events to the presenter
# will receive updates to the view from the presenter

class View:
  root = None 
  start_frame = None
  recipe_frame = None
  button_frame = None
  import_url_frame = None
  import_json_frame = None
  view_frame = None
  ing_dir_frame = None
  edit_frame = None
  edit_ing_dir_frame = None
  url_entry = None
  json_entry = None
  name_entry = None
  edit_instruction_text = None
  edit_directions_text = None
  recipe_objects = []
  name_label = None
  ingredient_label = None
  directions_text = None
  url_error_label = None
  style = None

  pres_add_url = None
  pres_add_json = None
  pres_leetify = None

  def __init__(self, pres_import_url, pres_import_json, pres_back_import_url, pres_add_url, pres_back_import_json, pres_add_json, pres_back_view, pres_back_edit, pres_save_changes, pres_delete, pres_leetify):
    """Creates a Model object with the given presenter functions, initializes tk"""
    self.pres_add_url = pres_add_url
    self.pres_add_json = pres_add_json
    self.pres_leetify = pres_leetify
    self.style = ttk.Style()
    self.style.configure("TButton", foreground="white", background="grey", padding=0, highlightbackground="grey")
    self.root = tk.Tk()
    self.root.geometry('640x360')
    self.root.resizable(False, False)
    self.root.config(bg='gray')
    self.root.title('Recipe Manager')
    self.root.rowconfigure(0, weight=1)
    self.root.columnconfigure(0, weight=1)
    self.start_frame = tk.Frame(self.root, bg='gray')
    self.start_frame.rowconfigure(0, weight=1)
    self.start_frame.rowconfigure(1, weight=1)
    self.start_frame.rowconfigure(2, weight=1)
    self.start_frame.columnconfigure(0, weight=1)
    self.start_frame.grid(sticky='nsew')
    title_label = tk.Label(self.start_frame, text='Recipes', font=('Arial', 20, 'bold'), bg='gray', fg='white')
    title_label.grid(pady=(20, 10), row=0, column=0)
    self.recipe_frame = tk.Frame(self.start_frame, bg='gray')
    self.recipe_frame.grid(row=1, column=0)
    self.button_frame = tk.Frame(self.start_frame, bg='gray')
    self.button_frame.grid(row=2, column=0)
    import_url_button = tk.Button(self.button_frame, text='Import from URL', command=pres_import_url, highlightbackground="grey")
    import_url_button.grid(column=0, row=0)
    import_json_button = tk.Button(self.button_frame, text='Import from JSON', command=pres_import_json, highlightbackground="grey")
    import_json_button.grid(padx=(10,0), column=1, row=0)
    self.import_url_frame = tk.Frame(self.root, bg='gray')
    self.import_url_frame.rowconfigure(0, weight=1)
    self.import_url_frame.rowconfigure(1, weight=1)
    self.import_url_frame.rowconfigure(2, weight=1)
    self.import_url_frame.rowconfigure(3, weight=1)
    self.import_url_frame.rowconfigure(4, weight=1)
    self.import_url_frame.columnconfigure(0, weight=1)
    url_back_button = tk.Button(self.import_url_frame, text='Back', command=pres_back_import_url, highlightbackground="grey")
    url_back_button.grid(sticky='w', pady=10, padx=10, row=0, column=0)
    url_label = tk.Label(self.import_url_frame, text='Enter the URL:', bg='gray', fg='white', font=('Arial', 14, 'bold'))
    url_label.grid(pady=(20, 10), row=1, column=0)
    self.url_entry = ttk.Entry(self.import_url_frame)
    self.url_entry.grid(ipadx=15, ipady=10, row=2, column=0)
    add_url_button = tk.Button(self.import_url_frame, text='Add', command=pres_add_url, highlightbackground="grey")
    add_url_button.grid(pady=10, row=3, column=0)
    self.url_error_label = tk.Label(self.import_url_frame, text='Not a valid URL', font=('Arial', 12, 'bold'), bg='gray', fg='white')
    self.import_json_frame = tk.Frame(self.root, bg='gray')
    self.import_json_frame.rowconfigure(0, weight=1)
    self.import_json_frame.rowconfigure(1, weight=1)
    self.import_json_frame.rowconfigure(2, weight=1)
    self.import_json_frame.rowconfigure(3, weight=1)
    self.import_json_frame.rowconfigure(4, weight=1)
    self.import_json_frame.columnconfigure(0, weight=1)
    json_back_button = tk.Button(self.import_json_frame, text='Back', command=pres_back_import_json, highlightbackground="grey")
    json_back_button.grid(sticky='w', pady=10, padx=10, row=0, column=0)
    json_label = tk.Label(self.import_json_frame, text='Enter the JSON Data:', bg='gray', fg='white', font=('Arial', 14, 'bold'))
    json_label.grid(pady=(20, 10), row=1, column=0)
    self.json_entry = tk.Entry(self.import_json_frame, bd=3)
    self.json_entry.grid(ipadx=15, ipady=10, row=2, column=0)
    add_json_button = tk.Button(self.import_json_frame, text='Add', command=pres_add_json, highlightbackground="grey")
    add_json_button.grid(pady=10, row=3, column=0)
    json_error_label = tk.Label(self.import_url_frame, text='Not valid JSON data', font=('Arial', 12, 'bold'), bg='gray', fg='white')
    self.view_frame = tk.Frame(self.root, bg='gray')
    self.view_frame.rowconfigure(0, weight=1)
    self.view_frame.rowconfigure(1, weight=1)
    self.view_frame.rowconfigure(2, weight=1)
    self.view_frame.columnconfigure(0, weight=1)
    view_back_button = tk.Button(self.view_frame, text='Back', command=pres_back_view, highlightbackground="grey")
    view_back_button.grid(sticky='w', pady=10, padx=10, row=0, column=0)
    self.name_label = tk.Label(self.view_frame, font=('Arial', 16, 'bold'), bg='gray', fg='white')
    self.name_label.grid(pady=(0, 20), row=1, column=0)
    self.ing_dir_frame = tk.Frame(self.view_frame, bg='gray')
    self.ing_dir_frame.grid(row=2, column=0, pady=(10, 20))
    ing_name_label = tk.Label(self.ing_dir_frame, text='Ingredients', font=('Arial', 15, 'bold'), bg='gray', fg='white')
    ing_name_label.grid(row=0, column=0)
    self.ingredient_label = tk.Label(self.ing_dir_frame, font=('Arial', 12), bg='gray', fg='white', wraplength=300, justify=tk.CENTER)
    self.ingredient_label.grid(row=1, column=0, padx=(0, 10))
    dir_name_label = tk.Label(self.ing_dir_frame, text='Directions', font=('Arial', 15, 'bold'), bg='gray', fg='white')
    dir_name_label.grid(row=0, column=1)
    self.directions_text = st.ScrolledText(self.ing_dir_frame, width=25, height=8, wrap=tk.WORD, font=('Arial'))
    self.directions_text.grid(row=1, column=1)
    self.edit_frame = tk.Frame(self.root, bg='gray')
    self.edit_frame.rowconfigure(0, weight=1)
    self.edit_frame.rowconfigure(1, weight=1)
    self.edit_frame.rowconfigure(2, weight=1)
    self.edit_frame.columnconfigure(0, weight=1)
    edit_back_button = tk.Button(self.edit_frame, text='Back', command=pres_back_edit, highlightbackground="grey")
    edit_back_button.grid(sticky='w', pady=10, padx=10, row=0, column=0)
    self.name_entry = tk.Entry(self.edit_frame)
    self.name_entry.grid(pady=(0, 20), row=1, column=0)
    self.edit_ing_dir_frame = tk.Frame(self.edit_frame, bg='gray')
    self.edit_ing_dir_frame.grid(row=2, column=0)
    self.edit_ingredient_text = st.ScrolledText(self.edit_ing_dir_frame, width=25, height=8, font=('Arial'), wrap=tk.WORD)
    self.edit_ingredient_text.grid(row=0, column=0, padx=(0, 10))
    self.edit_directions_text = st.ScrolledText(self.edit_ing_dir_frame, width=25, height=8, wrap=tk.WORD, font=('Arial'))
    self.edit_directions_text.grid(row=0, column=1)
    sv_dlt_button_frame = tk.Frame(self.edit_frame, bg='gray')
    sv_dlt_button_frame.grid()
    save_changes_button = tk.Button(sv_dlt_button_frame, text='Save Changes', command=pres_save_changes, highlightbackground="grey")
    save_changes_button.grid(pady=10, row=0, column=0)
    delete_recipe_button = tk.Button(sv_dlt_button_frame, text='Delete Recipe', command=pres_delete, highlightbackground="grey")
    delete_recipe_button.grid(pady=10, padx=(20, 0), row=0, column=1)
    self.root.bind('1', partial(View.leet_1, self))

  def leet_1(self, _):
    self.root.unbind('1')
    self.root.bind('3', partial(View.leet_2, self))

  def leet_2(self, _):
    self.root.bind('3', partial(View.leet_3, self))

  def leet_3(self, _):
    self.root.unbind('3')
    self.root.bind('7', partial(View.leet_4, self))

  def leet_4(self, _):
    self.pres_leetify()
    
  def clean_import_url(self):
    """Cleans the fields associated with the import url screen and minimizes the screen"""
    self.root.unbind('<Return>')
    self.import_url_frame.grid_forget()
    self.url_error_label.grid_forget()
    self.url_entry.delete(0, tk.END)

  def clean_import_json(self):
    """Cleans the fields associated with the import json screen and minimizes the screen"""
    self.root.unbind('<Return>')
    self.json_entry.delete(0, tk.END)
    self.import_json_frame.grid_forget()

  def clean_edit(self):
    """"Cleans the fields associated with the edit screen and minimizes the screen"""
    self.edit_frame.grid_forget()
    self.name_entry.delete(0, tk.END)
    self.edit_directions_text.delete(1.0, tk.END)
    self.edit_ingredient_text.delete(1.0, tk.END)

  def clean_view(self):
    """Minimizes the view screen"""
    self.view_frame.grid_forget()

  def clean_main(self):
    """Minimizes the main screen"""
    self.start_frame.grid_forget()

  def start_view(self):
    """Maximizes the view screen"""
    self.view_frame.grid(sticky='nsew')

  def start_edit(self):
    """Maximizes the edit screen"""
    self.edit_frame.grid(sticky='nsew')

  def start_import_url(self):
    """Maximizes the import url screen and gives focus to the url field"""
    self.import_url_frame.grid(sticky='nsew')
    self.root.bind('<Return>', self.pres_add_url)
    self.root.after(1, lambda: self.url_entry.focus_set())

  def start_import_json(self):
    """Maximizes the import json screen and gives focus to the json field"""
    self.import_json_frame.grid(sticky='nsew')
    self.root.bind('<Return>', self.pres_add_json)
    self.root.after(1, lambda: self.json_entry.focus_set())
    
  def start_main(self):
    """Maximizes the main screen"""
    self.start_frame.grid(sticky='nsew')

  def show_url_error(self):
    """Shows the error associated with an invalid URL"""
    tk.messagebox.showerror("Error", "Not a valid url. Try again, or else")

  def show_json_error(self):
    """Shows the error associated with an invalid JSON"""
    tk.messagebox.showerror("Error", "Not a valid JSON. Try again, or else")

  def show_copied(self):
    """Shows the info associated with exporting JSON"""
    tk.messagebox.showinfo("Info", "The JSON has been copied to your clipboard")

  def fill_view(self, name, ingredients, directions):
    """Fills the view screen with the given information"""
    self.name_label.config(text=name)
    self.ingredient_label.config(text=ingredients)
    self.directions_text.insert(tk.INSERT, directions)
    self.directions_text.configure(state='disabled') 

  def fill_edit(self, name, ingredients, directions):
    """Fills the edit screen with the given information"""
    self.name_entry.insert(tk.INSERT, name)
    self.edit_ingredient_text.insert(tk.INSERT, ingredients)
    self.edit_directions_text.insert(tk.INSERT, directions)
    
  def get_edit_status(self):
    """Returns the current information associated with the edit screen"""
    name = self.name_entry.get()
    ingredients = self.edit_ingredient_text.get("1.0", tk.END)
    directions = self.edit_directions_text.get("1.0", tk.END)
    return name, ingredients, directions

  def get_url_status(self):
    """Returns the current information associated with the url field"""
    return self.url_entry.get()

  def get_json_status(self):
    """Returns the current information associated with the json field"""
    return self.json_entry.get()

  def get_confirmation(self):
    """Gets the confirmation that we should delete the recipe"""
    return messagebox.askokcancel("Question", "Do you want to delete this recipe? This action cannot be undone.")

  def change_recipe_objects(self, data):
    """Deletes the recipe objects and rebuilds them with new data"""
    for row in self.recipe_objects:
      for item in row:
        item.destroy()
    self.recipe_objects = []
    count = 0
    for (name, view, edit, export) in data:
      temp_label = tk.Label(self.recipe_frame, text=name, bg='gray', fg='white', font=('Arial', 13))
      temp_label.grid(row=count, column=0, padx=(0, 5))
      temp_view = tk.Button(self.recipe_frame, text='View', command=view, highlightbackground="grey")
      temp_view.grid(row=count, column=1, padx=(5, 10), pady=5)
      temp_edit = tk.Button(self.recipe_frame, text='Edit', command=edit, highlightbackground="grey")
      temp_edit.grid(row=count, column=2, padx=(5, 10), pady=5)
      temp_export = tk.Button(self.recipe_frame, text='Export JSON', command=export, highlightbackground="grey")
      temp_export.grid(row=count, column=3, padx=(5, 10), pady=5)
      self.recipe_objects.append([temp_label, temp_view, temp_edit, temp_export])
      count += 1

  def start_loop(self):
    """Starts the main loop"""
    self.root.mainloop()
