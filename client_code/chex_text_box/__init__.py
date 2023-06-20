from ._anvil_designer import chex_text_boxTemplate
from anvil import *
import anvil.server

class chex_text_box(chex_text_boxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def text_box_1_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.text = event_args['sender'].text
    self.raise_event('change_box', **event_args)

