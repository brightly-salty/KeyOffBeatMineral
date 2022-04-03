# should send all updates to the view
# should send updates to the model
# will receive user events from the view
# will receive state changes from the model

from view import View
from functools import partial
import validators
import pyperclip

class Presenter:
  view = None
  current_edit = None
  model_edit = None
  model_delete = None
  model_url = None
  model_get = None
  model_save = None
  model_json = None
  model_dump_json = None
  
  def __init__(self, model_edit, model_delete, model_url, model_get, model_save, model_json, model_dump_json):
    """Creates a Presenter object with the given functions to access the model"""
    self.view = View(partial(Presenter.import_url, self), partial(Presenter.import_json, self), partial(Presenter.back_import_url, self), partial(Presenter.add_url, self), partial(Presenter.back_import_json, self), partial(Presenter.add_json, self), partial(Presenter.back_view, self), partial(Presenter.back_edit, self), partial(Presenter.save_changes, self), partial(Presenter.delete, self))
    self.model_edit = model_edit
    self.model_delete = model_delete
    self.model_url = model_url
    self.model_get = model_get
    self.model_save = model_save
    self.model_json = model_json
    self.model_dump_json = model_dump_json
    self.reload_recipes()

  def reload_recipes(self):
    """Reloads the list of recipes and their buttons for the main screen after the recipes are changed"""
    recipes = self.model_get()
    data = []
    index = 0
    for recipe in recipes:
      name = recipe['name']
      view = partial(Presenter.view_recipe, self, index, recipe)
      edit = partial(Presenter.edit_recipe, self, index, recipe)
      export = partial(Presenter.export_recipe, self, index, recipe)
      data.append((name, view, edit, export))
      index += 1
    self.view.change_recipe_objects(data)
  
  def view_recipe(self, index, recipe):
    """Gives information to the view with which to view the given recipe"""
    name = recipe['name']
    ingredients = ''
    for ingredient in recipe['ingredients']:
      ingredients += ingredient + '\n'
    directions  = ''
    for step in recipe['directions']:
      directions += step + '\n\n'
    self.view.fill_view(name, ingredients.strip(), directions.strip())
    self.view.clean_main()
    self.view.start_view()

  def edit_recipe(self, index, recipe):
    """Gives information to the view with which to edit the given recipe"""
    self.current_edit = index
    name = recipe['name']
    ingredients = ''
    for ingredient in recipe['ingredients']:
      ingredients += ingredient + '\n'
    directions  = ''
    for step in recipe['directions']:
      directions += step + '\n\n'
    self.view.fill_edit(name, ingredients.strip(), directions.strip())
    self.view.clean_main()
    self.view.start_edit()

  def export_recipe(self, index, recipe):
    """Copies the JSON of the given recipe to the paste buffer"""
    json = self.model_dump_json(recipe)
    pyperclip.copy(json)
    self.view.show_copied()
  
  def import_url(self):
    """Goes from the main screen to the import url screen"""
    self.view.clean_main()
    self.view.start_import_url()

  def import_json(self):
    """Goes from the main screen to the import json screen"""
    self.view.clean_main()
    self.view.start_import_json()

  def back_import_url(self):
    """Goes back from the import url screen to the main screen"""
    self.view.clean_import_url()
    self.view.start_main()

  def add_url(self, *args):
    """Adds the entered URL to the recipe list="""
    url = self.view.get_url_status()
    if not validators.url(url):
      self.view.show_url_error()
    else:
      self.model_url(url)
      self.model_save()
      self.reload_recipes()
      self.view.clean_import_url() 
      self.view.start_main()

  def back_import_json(self):
    """Goes back from the import json screen to the main screen"""
    self.view.clean_import_json()
    self.view.start_main()

  def add_json(self, *args):
    """Adds the entered JSON to the recipe list"""
    json = self.view.get_json_status()
    try:
      self.model_json(json)
      self.model_save()
      self.reload_recipes()
      self.view.clean_import_json() 
      self.view.start_main()
    except:
      self.view.show_json_error()

  def back_view(self):
    """Goes back from the view screen to the main screen"""
    self.view.clean_view() 
    self.view.start_main()

  def back_edit(self):
    """Goes back from the edit screen to the main screen"""
    self.current_edit = None
    self.view.clean_edit() 
    self.view.start_main()

  def save_changes(self):
    """Saves the changes in the current edit frame"""
    name, new_ingredients, new_directions = self.view.get_edit_status()
    ingredients = []
    for line in new_ingredients.splitlines():
        if line != "":
            ingredients.append(line.strip())
    directions = []
    for line in new_directions.splitlines():
        if line != "":
            directions.append(line.strip())
    self.model_edit(self.current_edit, name, ingredients, directions)
    self.model_save()
    self.current_edit = None
    self.reload_recipes()
    self.view.clean_edit() 
    self.view.start_main()

  def delete(self):
    """Deletes a recipe but asks for confirmation first"""
    if self.view.get_confirmation():
      self.model_delete(self.current_edit)
      self.model_save()
      self.reload_recipes()
      self.view.clean_edit()
      self.view.start_main()

  def start_loop(self):
    """Starts the main loop"""
    self.view.start_loop()
