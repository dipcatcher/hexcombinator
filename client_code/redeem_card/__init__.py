from ._anvil_designer import redeem_cardTemplate
from anvil import *
from .. import contract_hub as ch
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False
import anvil.js
pulsechain_url = "https://rpc.pulsechain.com"
ethereum_url = "http://localhost:8545"# "https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"
from anvil.js.window import ethers
from anvil.js.window import ethers
class redeem_card(redeem_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def textbox_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.display_amount = self.textbox_input.text
    if self.textbox_input.text in [None, "0", ""]:
      self.input_amount = 0
      self.button_redeem.text = "Redeem"
      self.button_redeem.enabled = False
      return False
    else:
      self.input_amount = ethers.utils.parseUnits(str(self.textbox_input.text), 8)
      self.button_redeem.text = "Redeem: {:,f} Native HEX and {:,f} Bridged HEX".format(self.display_amount, self.display_amount)
      '''if get_open_form().metamask.address in [None]:
        alert("You must connect your wallet first to mint CHEX.")
        return False
      else:
        pass'''
    balance = self.user_data['CHEX Balance']

    if int(self.input_amount.toString())>0 and balance>=int(self.input_amount.toString()):
      self.button_redeem.enabled=True
    else:
      self.button_redeem.enabled=False
    

  
  def button_redeem_click(self, **event_args):
    """This method is called when the button is clicked"""
    success= False
    try:
      event_args['sender'].enabled = False
      a = anvil.js.await_promise(get_open_form().get_contract_write("CHEX").redeem(self.input_amount))
      a.wait()
      success=True
    except Exception as e:
      if 'object Object' in str(e):
        alert("Transaction not completed.")
        event_args['sender'].enabled = False
        return False
    if success:
      get_open_form().menu_click(sender=get_open_form().latest)
      

    

  
  def refresh_display(self):
    self.user_data = get_open_form().refresh()
    self.label_native_hex_balance.text = "{} HEX".format(self.user_data['Native HEX Balance']/(10**8))
    self.label_bridged_hex_balance.text = "{} {}".format(self.user_data['Bridged HEX Balance']/(10**8), get_open_form().bridged_token or "Bridged HEX")
    self.label_chex_balance.text = "{} CHEX".format(self.user_data['CHEX Balance']/(10**8))


  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.refresh_display()
    print('ok')

  def link_1_click(self, **event_args):
    from ..hex_descriptor import hex_descriptor
    alert(hex_descriptor(), large=True)


  

