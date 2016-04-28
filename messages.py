import struct
import typing


Message = typing.NamedTuple('Message', [
    ('name', str),
    ('length', int),
    ('id', int),
    ('payload', bytes)
])


class MessageParser(object):
    MSG_TYPES = [
        'choke',
        'unchoke',
        'interested',
        'not_interested',
        'have',
        'bitfield',
        'request',
        'piece',
        'cancel',
        'port'
    ]

    @classmethod
    def parse(cls, bytestring, msg_length):

        if bytestring[0:4] == b'\x00\x00\x00\x00':
            return Message(name='keep_alive', length=msg_length, id=-1, payload=b'')

        msg_id = bytestring[4]
        msg_payload = bytestring[5:]

        if msg_id == 255:
            import pdb; pdb.set_trace()
        print('msg len {}'.format(msg_length))
        print('msg id {}'.format(msg_id))

        return Message(
            name=cls.MSG_TYPES[msg_id],
            length=msg_length,
            id=msg_id,
            payload=msg_payload
        )

    @classmethod
    def encode_msg(cls, msg_type, payload=b''):
        if msg_type == 'keep alive':
            msg = ''
        else:
            msg = struct.pack('B', cls.MSG_TYPES.index(msg_type)) + payload
        return struct.pack('>I', len(msg)) + msg
