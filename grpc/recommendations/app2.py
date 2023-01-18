import grpc
from product_recommendations_pb2 import Category, RRequest, Product, Products
import product_recommendations_pb2_grpc
from concurrent import futures

data = {
    Category.DIGITAL: [
        Product(id=1, title='pr01', price=1000, stock=10),
        Product(id=1, title='pr02', price=1000, stock=10),
        Product(id=1, title='pr03', price=1000, stock=10),
    ],
    Category.CAR: [
        Product(id=1, title='pr04', price=1000, stock=10),
    ],
}


class RecommendationService(product_recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        result = data[request.cat_id]
        return Products(items=result)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
product_recommendations_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
server.add_insecure_port("[::]:3000")
server.start()
server.wait_for_termination()
