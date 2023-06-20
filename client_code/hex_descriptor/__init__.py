from ._anvil_designer import hex_descriptorTemplate
from anvil import *

class hex_descriptor(hex_descriptorTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
