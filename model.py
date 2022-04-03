# will receive updates to the model from the presenter
# should send state-change events to the presenter

from urllib.request import urlopen
from bs4 import BeautifulSoup
from json import dump, load, loads, dumps
from presenter import Presenter
from functools import partial

class Model:
  recipes = None
  datafilename = None
  presenter = None

  def __init__(self, datafilename):
    self.datafilename = datafilename
    try:
      with open(self.datafilename, 'r') as infile:
        self.recipes = load(infile)
    except FileNotFoundError:
      print("Warning: data file not found")
      self.recipes = []
    self.presenter = Presenter(partial(Model.edit_recipe, self), partial(Model.delete_recipe, self), partial(Model.add_recipe_url, self), partial(Model.get_recipes, self), partial(Model.save, self), partial(Model.add_recipe_json, self), partial(Model.dump_recipe_json, self))


  def make_recipe(self, name, ingredients, directions):
    """Creates a recipe object with the given name, ingredients, and directions"""
    return {"name": name, "ingredients": ingredients, "directions": directions}

  def delete_recipe(self, index):
    """Deletes the recipe at the given index"""
    del self.recipes[index]

  def add_recipe(self, recipe):
    """Adds a recipe to the end of the list"""
    self.recipes.append(recipe)

  def edit_recipe(self, index, name, ingredients, directions):
    """Replaces the recipe at the given index with a new one with the given parts"""
    self.recipes[index] = self.make_recipe(name, ingredients, directions)

  def get_recipes(self):
    """Returns the current set of recipes"""
    return self.recipes

  def add_recipe_url(self, url):
    """Reads a recipe page from allrecipes.com at the given url and adds it to the list"""
    page = urlopen(url)
    soup = BeautifulSoup(page, "lxml")
    name = soup.find('h1', {'class': 'headline'}).string.strip()
    ingredients = []
    for ingredient in soup.find_all('span', {'class': "ingredients-item-name"}):
      ingredients.append(ingredient.string.strip())
    directions = []
    for container in soup.find_all('li', {'class': 'instructions-section-item'}):
      directions.append(container.find('div').find('p').text)
    recipe = self.make_recipe(name, ingredients, directions)
    self.add_recipe(recipe)

  def add_recipe_json(self, json):
    """Adds the given JSON recipe to the list"""
    recipe = loads(json)
    self.add_recipe(recipe)

  def dump_recipe_json(self, recipe):
    """Dumps the given recipe into JSON and returns"""
    json = dumps(recipe)
    return json

  def save(self):
    """Saves the current recipe list into the datafilename"""
    with open(self.datafilename, 'w') as outfile:
      dump(self.recipes, outfile)

  def start_loop(self):
    """Starts the main loop"""
    self.presenter.start_loop()
