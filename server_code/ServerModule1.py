import anvil.server
import anvil.http
@anvil.server.callable
def send_tweet(amount, minter, chain):
  text = "{:,} CHEX on {} minted by {}...{} at https://hexcombinator.com".format(int(amount),chain ,minter[0:4], minter[-4:])
  data={}
  data['text']=text
  url = "https://hooks.zapier.com/hooks/catch/10571278/33o7rxr/"
  anvil.http.request(url, method="POST", data=data)