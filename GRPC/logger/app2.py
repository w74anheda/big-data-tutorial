import datetime
import random
import time

import grpc
from logger_pb2 import Log
import logger_pb2_grpc
from concurrent import futures


class LoggerService(logger_pb2_grpc.LoggerServicer):
    def LogStore(self, request, context):
        while True:
            yield self.fakeOrderGenerator()
            time.sleep(1)

    def fakeOrderGenerator(self):
        return Log(user_id=random.randint(0, 100))


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
logger_pb2_grpc.add_LoggerServicer_to_server(LoggerService(), server)
server.add_insecure_port("[::]:5000")
server.start()
server.wait_for_termination()
