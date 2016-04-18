import re
import string


def decode(data_str):
    def _decode(data_str):
        if data_str.startswith('i'):  # Match integers
            match = re.match("i(-?\\d+)e", data_str)
            match_start, match_end = match.span()
            return int(match.group(1)), data_str[match_end:]

        elif data_str.startswith('l'):
            res = []
            remainder = data_str[1:]
            while not remainder.startswith('e'):
                elem, remainder = _decode(remainder)
                res.append(elem)
            return res, remainder[1:]

        elif data_str.startswith('d'):
            vals = []
            remainder = data_str[1:]
            while not remainder.startswith('e'):
                elem, remainder = _decode(remainder)
                vals.append(elem)

            res = {key: value for key, value in zip(vals[::2], vals[1::2])}

            return res, remainder[1:]

        elif any(str(i) for i in string.digits):  # Match integers
            match = re.match("(\\d+):", data_str)
            str_len = int(match.group(1))
            _, match_end = match.span()

            start = match_end
            end = match_end + str_len
            return data_str[start:end], data_str[end:]

        else:
            raise Exception("Unable to decode: {}".format(data_str))


    res, extra = _decode(data_str)
    if extra:
        raise ValueError("Malformed Input Recieved")
    return res