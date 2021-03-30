# encoding: utf-8
import logging
from typing import Callable, Any
from google.protobuf import any_pb2
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException, InvalidArgument, NotFound, Unknown
import grpc
import marshmallow
import mongoengine


# setup logger
FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class ExceptionToStatusInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        """Override this method to implement a custom interceptor.
         You should call method(request, context) to invoke the
         next handler (either the RPC method implementation, or the
         next interceptor in the list).
         Args:
             method: The next interceptor, or method implementation.
             request: The RPC request, as a protobuf message.
             context: The ServicerContext pass by gRPC to the service.
             method_name: A string of the form
                 "/protobuf.package.Service/Method"
         Returns:
             This should generally return the result of
             method(request, context), which is typically the RPC
             method response, as a protobuf message. The interceptor
             is free to modify this in some way, however.
         """
        try:
            return method(request, context)
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            logger.error(e.details)
            return any_pb2.Any()

        except marshmallow.ValidationError as e:
            context.set_code(InvalidArgument.status_code)
            context.set_details(e.__str__())
            logger.error(e)
            return any_pb2.Any()

        except mongoengine.errors.DoesNotExist as e:
            context.set_code(NotFound.status_code)
            context.set_details(str(e))
            logger.error(str(e))
            return any_pb2.Any()

        except Exception as e:
            context.set_code(Unknown.status_code)
            context.set_details(str(e))
            logger.error(str(e))
            return any_pb2.Any()