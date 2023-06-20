from ._anvil_designer import combinator_daoTemplate
from anvil import *
import anvil.js
import datetime
from .. import contract_hub as ch
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False
pulsechain_url = "https://rpc.pulsechain.com"
ethereum_url = "http://localhost:8545"# "https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"
from anvil.js.window import ethers
class combinator_dao(combinator_daoTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.chain = properties['chain']
    self.label_chain.text = "Ethereum" if self.chain =='ETH' else "PulseChain"
    units = "gwei" if self.chain =="ETH" else 'beats'
    supply = int(get_open_form().get_contract_read("CHEX", self.chain).totalSupply().toString())/(10**8)
    data_label = "Total CHEX Supply on {}: {} CHEX".format("Ethereum" if self.chain=='ETH' else "PulseChain", supply)
    self.label_data.text = data_label
    raw_throttle = get_open_form().get_contract_read("CHEX", self.chain).arbitrage_throttle().toString()
    simple_throttle = int(raw_throttle)/(10**18)
    self.label_current_arb.text="Current Arbitrage Throttle: {} {} ({} {})".format(raw_throttle,  units,simple_throttle,self.chain)
    st = 1
    unix_timestamp=int(get_open_form().get_contract_read("CHEX", self.chain).scheduled_arbitrage_throttle_change_timestamp().toString())
    dt = datetime.datetime.fromtimestamp(unix_timestamp)
    st = int(get_open_form().get_contract_read("CHEX", self.chain).scheduled_arbitrage_throttle().toString())
    print(unix_timestamp)
    simple_sthrottle = st/(10**18)
    if st ==0:
      self.label_execute.text = "No throttle changes scheduled."
    else:
      self.label_execute.text = "Arbitrage Throttle Scheduled to be changed to {} {} ({} {}) at {}".format(st, units,simple_sthrottle,self.chain, dt.strftime('%Y-%m-%d %H:%M:%S'))
    #alert(get_open_form().get_contract_read("CHEX").COMBINATOR_DAO_ADDRESS())
    self.eth_balance=int(get_open_form().providers[self.chain].getBalance(ch.contract_data['CHEX']['address']).toString())
    bal = "Contract has collected {} {}".format(self.eth_balance/(10**18), self.chain)
    self.label_proceeds.text = bal
    
    for f in dir(get_open_form().get_contract_read("CHEX", self.chain)):
      if "(" in f:
        print(f)
    
    
    # Any code you write here will run before the form opens.
  def is_dao(self):
    print('dao:', get_open_form().get_contract_read("CHEX", self.chain).COMBINATOR_DAO_ADDRESS())
    is_dao = get_open_form().metamask.address==get_open_form().get_contract_read("CHEX", self.chain).COMBINATOR_DAO_ADDRESS()
    if is_dao:
      return True
    else:
      alert("Only the Combinator DAO address can run these functions.")
      return False
    
  def button_update_click(self, **event_args):
    if not self.is_dao():
      return False
    self.write_contract=get_open_form().get_contract_write("CHEX")
    a = anvil.js.await_promise(self.write_contract.scheduleArbitrageThrottleChange(self.text_box_new_arbitrage.text))
    a.wait()
    get_open_form().menu_click(sender=get_open_form().latest)

  def button_execute_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.is_dao():
      return False
    try:
      self.write_contract=get_open_form().get_contract_write("CHEX")
      a = anvil.js.await_promise(self.write_contract.executeArbitrageThrottleChange())
      a.wait()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      alert(e)

  def button_flush_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.is_dao():
      return False
    try:
      self.write_contract=get_open_form().get_contract_write("CHEX")
      a = anvil.js.await_promise(self.write_contract.collectArbitrageThrottle())
      a.wait()
      get_open_form().menu_click(sender=get_open_form().latest)
    except Exception as e:
      alert(e)


