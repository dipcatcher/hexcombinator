from ._anvil_designer import aboutTemplate
from anvil import *
import anvil.server

class about(aboutTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    get_open_form().menu_click(sender=get_open_form().link_mint)

