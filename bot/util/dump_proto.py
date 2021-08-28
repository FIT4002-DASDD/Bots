"""
A utility tool to parse and dump a serialized proto to the console as text.
"""
import proto.ad_pb2 as ad_pb2
from absl import app
from absl import flags
from absl import logging
from google.protobuf import text_format

FLAGS = flags.FLAGS

flags.DEFINE_string('serialized_proto', None, 'Pass in full path to the serialized proto file for dumping (required).')

flags.mark_flags_as_required(['serialized_proto'])


def main(argv):
    with open(FLAGS.serialized_proto, 'rb') as serialized_proto_file:
        ad_collection = ad_pb2.AdCollection()
        ad_collection.ParseFromString(serialized_proto_file.read())

        ad_collection_text_proto = text_format.MessageToString(ad_collection)
        # TODO: image bytestrings are huge!
        logging.info(ad_collection_text_proto)

        with open(f'{FLAGS.serialized_proto}.textproto', 'w') as text_proto_out_file:
            text_proto_out_file.write(ad_collection_text_proto)


if __name__ == '__main__':
    app.run(main)
