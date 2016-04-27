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
    def parse(cls, arg):
        if isinstance(arg, bytes):
            return cls.create_from_bytestring(arg)

    @classmethod
    def create_from_bytestring(cls, bytestring):
        if bytestring[0:4] == b'\x00\x00\x00\x00':
            return Message(name='keep_alive', length=0, id=-1, payload=b'')

        msg_length = struct.unpack('>I', bytestring[0:4])[0]
        print('seen msg len ', msg_length)

        # Keep Alive message; do nothing
        if not msg_length:
            return

        msg_id = bytestring[4]
        print('seen msg id ', msg_id)
        msg_payload = bytestring[5:]

        return Message(
            name=cls.MSG_TYPES[msg_id],
            length=msg_length,
            id=msg_id,
            payload=msg_payload
        )
