import re
import string


def decode(data_str):
    def _decode(data_str):
        if data_str.startswith('i'):  # Match integers
            match = re.match("i(-?\\d+)e", data_str)
            match_start, match_end = match.span()
            return int(match.group(1)), data_str[match_end:]

        elif data_str.startswith('l'):
            pass

        elif any(str(i) for i in string.digits):  # Match integers
            match = re.match("(\\d+):", data_str)
            str_len = int(match.group(1))
            print(match.span())
            _, match_end = match.span()

            start = match_end
            end = match_end + str_len
            return data_str[start:end], data_str[end:]


    res, extra = _decode(data_str)
    if extra:
        raise Exception
    return res