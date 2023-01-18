import grpc
from product_recommendations_pb2 import Category, RRequest
from product_recommendations_pb2_grpc import RecommendationsStub


channel = grpc.insecure_channel('localhost:3000')
client = RecommendationsStub(channel)

request = RRequest(userID=2, cat_id=Category.CAR, per_page=10)
response = client.Recommend(request)


print(response)