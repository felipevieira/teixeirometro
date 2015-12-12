import requests
from datetime import date

BID_URL = 'http://bid.cbf.com.br'
BID_REQ_URL = 'http://bid.cbf.com.br/a/bid/carregar/json/'

def bid_get_data_for_date(d):
   s = requests.Session()
   s.get(BID_URL)
   r = s.post(BID_REQ_URL, data={'uf':'',
                                        'dt_pesquisa':d.strftime('%d/%m/%Y'),
                                        'tp_contrato':'TODOS',
                                        'n_atleta':''})

   return r


print bid_get_data_for_date(date(2015,3,2))
