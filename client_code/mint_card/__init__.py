from ._anvil_designer import mint_cardTemplate
from anvil import *
from .. import contract_hub as ch
import time
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
class mint_card(mint_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.

  def textbox_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.display_amount = event_args['sender'].text
    if event_args['sender'].text in [None, "0", ""]:
      self.show_approval = False
      self.input_amount = 0
      self.button_mint.text = "Mint"
      self.button_mint.enabled = False
    else:
      self.input_amount = ethers.utils.parseUnits(str(event_args['sender'].text), 8)
      self.show_approval = True
      self.label_approve_amount.text = "Amount: {:,f} Native HEX and Bridged HEX".format(self.display_amount)
      self.button_mint.text = "Mint {:,f} CHEX".format(self.display_amount)
      if get_open_form().metamask.address in [None]:
        self.show_approval=False
      else:
        try:
          self.check_approvals()
        except:
          time.sleep(.5)
          self.check_approvals()
    self.column_panel_approve.visible = self.show_approval
    
  def check_approvals(self):
    if self.input_amount ==0:
      return False
    is_hex_approved = False
    is_bridged_hex_approved = False
    chex_address = ch.contract_data['CHEX']['address']
    self.native_approval = int(get_open_form().get_contract_read('HEX').allowance(get_open_form().metamask.address, chex_address).toString())
    self.bridged_approval = int(get_open_form().get_contract_read(get_open_form().bridged_token).allowance(get_open_form().metamask.address, chex_address).toString())
    if self.native_approval<int(self.input_amount.toString()):
      self.button_approve_hex.text = "Approve {} HEX".format(self.display_amount)
      self.button_approve_hex.enabled = True
    else:
      self.button_approve_hex.text = "Succesfully Approved {} HEX".format(self.display_amount)
      self.button_approve_hex.enabled = False
      self.button_approve_hex.icon='fa:check'
      is_hex_approved = True
    if self.bridged_approval<int(self.input_amount.toString()):
      self.button_approve_bridged_hex.text = "Approve {} {}".format(self.display_amount, get_open_form().bridged_token)
      self.button_approve_bridged_hex.enabled = True
    else:
      self.button_approve_bridged_hex.text = "Succesfully Approved {} {}".format(self.display_amount, get_open_form().bridged_token)
      self.button_approve_bridged_hex.enabled = False
      self.button_approve_bridged_hex.icon='fa:check'
      is_bridged_hex_approved = True
    
    self.button_mint.enabled=True if all([is_bridged_hex_approved, is_hex_approved]) else False
    
  def button_mint_click(self, **event_args):
    """This method is called when the button is clicked"""
    event_args['sender'].enabled=False
    success=False
    throttle =int(get_open_form().get_contract_read("CHEX").arbitrage_throttle().toString())
    self.refresh_display()
    warning = ""
    if self.user_data['Native HEX Balance'] < int(self.input_amount.toString()):
      warning +='Insufficient Native HEX Balance.\n'
    if self.user_data['Bridged HEX Balance'] < int(self.input_amount.toString()):
      warning +='Insufficient Bridged HEX Balance.\n'
    if int(get_open_form().metamask.provider.getBalance(get_open_form().metamask.address).toString())<throttle:
      warning +="Insufficient {} Balance.".format(get_open_form().link_switch.text)
    if warning!="":
      alert(warning, title="Unable to request transaction")
      return False
    try:
      a = anvil.js.await_promise(get_open_form().get_contract_write("CHEX").mint(self.input_amount, {"value":throttle}))
      a.wait()
      success=True
    except Exception as e:
      if 'object Object' in str(e):
        alert("Transaction not completed")
    if success:
      get_open_form().menu_click(sender=get_open_form().latest)

  def button_approve_click(self, **event_args):
    """This method is called when the button is clicked"""
    token = "HEX" if event_args['sender']==self.button_approve_hex else get_open_form().bridged_token
    a = anvil.js.await_promise(get_open_form().get_contract_write(token).approve(ch.contract_data['CHEX']['address'],self.input_amount))
    a.wait()
    self.check_approvals()
  def refresh_display(self):
    self.user_data = get_open_form().refresh()
    self.label_native_hex_balance.text = "{} HEX".format(self.user_data['Native HEX Balance']/(10**8))
    self.label_bridged_hex_balance.text = "{} {}".format(self.user_data['Bridged HEX Balance']/(10**8), get_open_form().bridged_token or "Bridged HEX")
    self.label_chex_balance.text = "{} CHEX".format(self.user_data['CHEX Balance']/(10**8))
    if get_open_form().metamask.address is None:
      eth_throttle =int(get_open_form().get_contract_read("CHEX", "ETH").arbitrage_throttle().toString())
      ethereum_throttle = "Ethereum Arbitrage Throttle: {:.8f} ETH".format(eth_throttle/(10**18))
      pls_throttle=int(get_open_form().get_contract_read("CHEX", "PLS").arbitrage_throttle().toString())
      pulsechain_throttle = "PulseChain Arbitrage Throttle: {:.8f} PLS".format(pls_throttle/(10**18))
      self.label_throttle.text = "{}\n{}".format(ethereum_throttle, pulsechain_throttle)
    else:
      if get_open_form().link_switch.text == "ETH":
        eth_throttle =int(get_open_form().get_contract_read("CHEX", "ETH").arbitrage_throttle().toString())
        ethereum_throttle = "Ethereum Arbitrage Throttle: {:.8f} ETH".format(eth_throttle/(10**18))
        self.label_throttle.text = ethereum_throttle
      else:
        pls_throttle=int(get_open_form().get_contract_read("CHEX", "PLS").arbitrage_throttle().toString())
        pulsechain_throttle = "PulseChain Arbitrage Throttle: {:,} PLS".format(int(pls_throttle/(10**18)))
        self.label_throttle.text = pulsechain_throttle
        


  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.refresh_display()
    

  def link_more_info_click(self, **event_args):
    """This method is called when the link is clicked"""
    from ..hex_descriptor import hex_descriptor
    alert(hex_descriptor(), large=True)

  def link_throttle_click(self, **event_args):
    """This method is called when the link is clicked"""
    d = '''An arbitrage throttle is set by the Combinator DAO to introduce a small fixed cost to minting CHEX, paid in ETH or PLS. It was initialized to be close to $10 at current prices. \nThe arbitrage throttle only applies to minting, not redeeming.\nThe arbitrage throttle is designed so that users below some value threshold can get a better deal buying CHEX instead of minting, which helps foster an active market.\nThe arbitrage throttle is also a type of size bonus, where the more CHEX you mint, the smaller percent of the total the arbitrage throttle is. \nThe arbitrage throttle can be changed at any time by the Combinator DAO. A 24 hour delay is implemented between when a change is scheduled to when it is implemented. The Combinator DAO collects this ETH or PLS and there should be no expectations for what Combinator DAO does with it.'''
    alert(d, title="Arbitrage Throttle", large=True)



  

