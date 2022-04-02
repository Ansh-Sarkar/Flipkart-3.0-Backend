from elasticsearch import Elasticsearch
import requests

# trying to use the Elasetisearch library / module
client = Elasticsearch()
client.create(index = "ansh-sarkar", id = 9 ,body = {'haha':'noice','message':'added again'}, params=None, headers=None)

# data = {
#     'name':'ansh',
#     'friend':'binit',
#     'role model':'elon musk'
# }
# params = data
# request = requests.post(url = 'http://localhost:9200/my-index-000001/_doc/' , data=data , params=params)
# print(request)
