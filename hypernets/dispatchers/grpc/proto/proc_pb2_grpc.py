# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from hypernets.dispatchers.grpc.proto import proc_pb2 as hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2


class ProcessBrokerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.run = channel.stream_stream(
                '/hypernets.dispatchers.proto.ProcessBroker/run',
                request_serializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.ProcessRequest.SerializeToString,
                response_deserializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.FromString,
                )
        self.download = channel.unary_stream(
                '/hypernets.dispatchers.proto.ProcessBroker/download',
                request_serializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DownloadRequest.SerializeToString,
                response_deserializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.FromString,
                )


class ProcessBrokerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def run(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def download(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProcessBrokerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'run': grpc.stream_stream_rpc_method_handler(
                    servicer.run,
                    request_deserializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.ProcessRequest.FromString,
                    response_serializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.SerializeToString,
            ),
            'download': grpc.unary_stream_rpc_method_handler(
                    servicer.download,
                    request_deserializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DownloadRequest.FromString,
                    response_serializer=hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hypernets.dispatchers.proto.ProcessBroker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProcessBroker(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def run(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/hypernets.dispatchers.proto.ProcessBroker/run',
            hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.ProcessRequest.SerializeToString,
            hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def download(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/hypernets.dispatchers.proto.ProcessBroker/download',
            hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DownloadRequest.SerializeToString,
            hypernets_dot_dispatchers_dot_grpc_dot_proto_dot_proc__pb2.DataChunk.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
