import re
import string


def decode(data):
    def _decode(data):
        if data.startswith(b'i'):  # Match integers
            match = re.match(b"i(-?\\d+)e", data)
            match_start, match_end = match.span()
            return int(match.group(1)), data[match_end:]

        elif data.startswith(b'l'):  # Match list
            res = []
            remainder = data[1:]
            while not remainder.startswith(b'e'):
                elem, remainder = _decode(remainder)
                res.append(elem)
            return res, remainder[1:]

        elif data.startswith(b'd'):  # Match dict
            vals = []
            remainder = data[1:]
            while not remainder.startswith(b'e'):
                elem, remainder = _decode(remainder)
                vals.append(elem)

            res = {key: value for key, value in zip(vals[::2], vals[1::2])}

            return res, remainder[1:]

        elif any(str(i) for i in string.digits):  # Match strings
            match = re.match(b"(\\d+):", data)
            str_len = int(match.group(1))
            _, match_end = match.span()

            start = match_end
            end = match_end + str_len
            return data[start:end], data[end:]

        else:
            raise Exception("Unable to decode: {}".format(data))


    res, extra = _decode(data)
    if extra:
        raise ValueError("Malformed Input Recieved")
    return res