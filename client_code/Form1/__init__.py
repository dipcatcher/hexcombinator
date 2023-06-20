from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.js
from .. import contract_hub as ch
from ..mint_card import mint_card
from ..redeem_card import redeem_card
from ..combinator_dao import combinator_dao
try:
  from anvil.js.window import ethereum
  is_ethereum=True
except:
  is_ethereum=False
print(is_ethereum)
pulsechain_url = "https://rpc.pulsechain.com"
ethereum_url = "https://eth-mainnet.g.alchemy.com/v2/CjAeOzPYt5r6PmpSkW-lL1NL7qfZGzIY"
from anvil.js.window import ethers
class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.metamask.button_1.role = 'filled-button'
    self.init_components(**properties)
    self.current_network = None
    urls = {"PLS":pulsechain_url, "ETH":ethereum_url}
    self.bridged_token=None
    self.providers = {}
    self.providers['ETH'] = ethers.providers.JsonRpcProvider(urls["ETH"])
    self.providers["PLS"]= ethers.providers.JsonRpcProvider(urls["PLS"])
    self.menu_click(sender=self.link_mint)
  def menu_click(self, **event_args):
    self.latest = event_args['sender']
    if event_args['sender']==self.link_mint:
      page = mint_card()
    elif event_args['sender'] ==self.link_redeem:
      page = redeem_card()
    elif event_args['sender']==self.link_combinator:
      page = ColumnPanel()
      title = Label(role="headline", text="HEX Combinator DAO")
      explainer = Label(text="The HEX Combinator DAO sets the arbitrage throttle parameter for the system and collects the arbitrage throttle proceeds. Currently the contract deployer is the sole DAO member, but soon this will be decentralized. Combinator DAO tokens will be airdropped to liquidity providers in select CHEX ecosystem liquidity pools on both PulseX and Uniswap. ")
      page.add_component(title)
      page.add_component(explainer)
      if self.metamask.address is None:
        page.add_component(combinator_dao(chain='PLS'))
        page.add_component(combinator_dao(chain="ETH"))
      else:
        page.add_component(combinator_dao(chain=self.link_switch.text))
    self.panel_manage.clear()
    self.panel_manage.add_component(page)
    page.scroll_into_view()
    
  def calc_fee(self):
    usd_per_heart = .02/(10**8)
    usd_per_wei = 1724/(10**18)
    usd_per_beat = (10**-4)/(10**18)
    
    
    target = 10
    ethrottle=int(target/usd_per_wei)
    pthrottle=int(target/usd_per_beat)
    
    
    
    
    
    
    
  def get_contract_read(self, ticker, target_chain=None):
      if target_chain is None:
        chain = self.current_network
      else:
        chain = target_chain
      contract_data = ch.contract_data[ticker]
      return ethers.Contract(contract_data['address'], contract_data['abi'], self.providers[chain])
  def get_contract_write(self, ticker):
    contract_data = ch.contract_data[ticker]
    return ethers.Contract(contract_data['address'], contract_data['abi'],self.metamask.signer)
    # Any code you write here will run before the form opens.
  
  def metamask_connect(self, **event_args):
    
    self.chain_id = self.metamask.provider.getNetwork()['chainId']
    self.connected_chain = self.chain_id
    if self.chain_id in [1, 31337]:
      self.current_network = "ETH"
      self.bridged_token = "HEX from PulseChain"
    elif self.chain_id in [369]:
      self.current_network = "PLS"
      self.bridged_token = "HEX from Ethereum"
    self.link_switch.visible = True
    if self.connected_chain in [1, 31337]:
      self.link_switch.text = "ETH" 
    elif self.connected_chain == 369:
      self.link_switch.text = "PLS"
    self.refresh()
    self.menu_click(sender=self.latest)
    
  
    
  def refresh(self):
    self.user_data = {}
    
    
    if self.current_network is None:
      self.user_data['CHEX Balance']=0
      self.user_data['Native HEX Balance']=0
      self.user_data['Bridged HEX Balance'] = 0
    else:
      self.user_data['CHEX Balance'] = int(self.get_contract_read('CHEX').balanceOf(self.metamask.address).toString())
      self.user_data['Native HEX Balance'] = int(self.get_contract_read('HEX').balanceOf(self.metamask.address).toString())
      self.user_data['Bridged HEX Balance'] = int(self.get_contract_read(self.bridged_token).balanceOf(self.metamask.address).toString())
      
    return self.user_data

  def link_switch_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.metamask.address is None:
      self.current_network = "ETH"
      
    if self.connected_chain in [1, 31337]:
      self.current_network = "ETH" 
    elif self.connected_chain in [369]:
      self.current_network = "PLS"
      
    c = confirm("You are currently connected to {}.".format(self.current_network),title="Choose Network",buttons=[("Ethereum", True), ("Pulsechain", False)])
    if c:
      chain_id = "0x7A69"#"0x1"
    else:
      chain_id = "0x171"
    try:
      a = ethereum.request({
                'method': 'wallet_switchEthereumChain',
                'params': [{ "chainId": chain_id }] 
            })
      b = anvil.js.await_promise(a)
      
    except Exception as e:
      raise e
      alert("Connect to the network you want in your wallet and refresh the page.")
    self.metamask.update_signer()
    self.metamask_connect()
    #self.menu_click(sender=self.latest)   

  def link_add_click(self, **event_args):
   
    """This method is called when the link is clicked"""
    if event_args['sender'].icon == 'fa:check':
      pass
    else:
      try:
        tokenSymbol = "CHEX"
        tokenDecimals = 8
        tokenImage = "{}/_/theme/CHEX%20Logo%20(100px).svg".format(anvil.server.get_app_origin())#'https://watery-decisive-guitar.anvil.app/_/api/name/maxi.jpg';
        print(tokenImage)
        from anvil.js.window import ethereum
        a = ethereum.request({
        'method': 'wallet_watchAsset',
        'params': {
          'type': 'ERC20', 
          'options': {
            'address': ch.contract_data['CHEX']['address'], 
            'symbol': tokenSymbol, 
            'decimals': tokenDecimals, 
            'image': tokenImage, 
          },
        },
      })
        anvil.js.await_promise(a)
        
        
        event_args['sender'].icon = 'fa:check'
        event_args['sender'].text='CHEX Added'
      except Exception as e:
        print(e)


 

  


