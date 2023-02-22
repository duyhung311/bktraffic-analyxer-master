import Levenshtein as lev
from src.utils.path import STREETS_FILE

def locationMapping(street):
    with open(STREETS_FILE, 'r') as f:
        streets = [line.rstrip() for line in f]
    return min(streets, key=lambda x: lev.distance(x, street))

def numberMapping(text):
    """
    NOTICE: Can only handle from 0 to 99
    """

    mapper = {
        'không' :   0,
        'một'   :   1,
        'mốt'   :   1,
        'hai'   :   2,
        'ba'    :   3,
        'tư'    :   4,
        'bốn'   :   4,
        'năm'   :   5,
        'lăm'   :   5,
        'sáu'   :   6,
        'bảy'   :   7,
        'tám'   :   8,
        'chín'  :   9,
        'mười'  :   10
    }

    tokens = text.split()
    out = 0
    contain_number = False

    for idx in range(len(tokens)):
        if tokens[idx] in mapper.keys():
            contain_number = True
            out = out + mapper[tokens[idx]]
            if idx != len(tokens) - 1 and tokens[idx] != 'mười':
                out = out * 10
    
    return int(out) if contain_number else None

def sf2json(sf, text):
    text = text.split(' ')
    location = []
    reason = []
    velocity = ''
    length = len(sf[0])
    for i in range(0, length):
        if sf[0][i] == 'B-location':
            word = text[i]
            for j in range(i + 1, len(sf[0])):
                if sf[0][j] != 'I-location' or j == length - 1:
                    location.append(word)
                    i = j
                    break
                word = word + ' ' + text[j]
        elif sf[0][i] == 'B-reason':
            word = text[i]
            for j in range(i + 1, len(sf[0])):
                if sf[0][j] != 'I-reason' or j == length - 1:
                    reason.append(word)
                    i = j
                    break
                word = word + ' ' + text[j]
        elif sf[0][i] == 'B-velocity':
            word = text[i]
            for j in range(i + 1, len(sf[0])):
                if sf[0][j] != 'I-velocity' or j == length - 1:
                    velocity = word
                    i = j
                    break
                word = word + ' ' + text[j]
    # return location, reason, velocity
    velocity = velocity[:velocity.find('ki')-1]
    v = numberMapping(velocity)

    return {
        'location': location,
        'street': locationMapping(' '.join(location)),
        'velocity': v,
        'causes': reason,
        'description': 'bktraffic-analyxer'
    }

if __name__ == '__main__':
    sf = [['O', 'B-location', 'I-location', 'I-location', 'I-location', 'I-location', 'I-location', 'I-location', 'I-location', 'I-location', 'I-location', 'O', 'B-location', 'I-location', 'I-location', 'I-location', 'O', 'O', 'O', 'O', 'O', 'B-reason', 'I-reason', 'I-reason', 'O', 'O', 'O', 'O', 'O', 'B-velocity', 'I-velocity', 'I-velocity', 'I-velocity', 'I-velocity', 'I-velocity']]
    text = 'từ trường đại học bách khoa thành phố hồ chí minh đến ngã tư bảy hiền bị kẹt xe do có quá nhiều xe vận tốc đạt được khoảng sáu mươi ki lô mét trên giờ'
    print(sf2json(sf, text))
    # print(numberMapping('không'))
    # print(numberMapping('một'))
    # print(numberMapping('hai'))
    # print(numberMapping('ba'))
    # print(numberMapping('bốn'))
    # print(numberMapping('năm'))
    # print(numberMapping('sáu'))
    # print(numberMapping('bảy'))
    # print(numberMapping('tám'))
    # print(numberMapping('chín'))
    # print(numberMapping('mười'))
    # print(numberMapping('mười một'))
    # print(numberMapping('mười hai'))
    # print(numberMapping('hai mươi'))
    # print(numberMapping('hai mươi mốt'))
    # print(numberMapping('hai mươi hai'))
    # print(numberMapping('ba mươi mốt'))
    # print(numberMapping('ba mươi hai'))
    # print(numberMapping('bốn mươi lăm'))
    # print(numberMapping('bốn mươi tư'))
    # print(numberMapping('bốn mươi bốn'))
