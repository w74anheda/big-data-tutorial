import grpc
from logger_pb2 import FRequest
from logger_pb2_grpc import LoggerStub


channel = grpc.insecure_channel('localhost:5000')
client = LoggerStub(channel)
request = FRequest(token='fghdjfg435we')

for result in client.LogStore(request):
    print(result)