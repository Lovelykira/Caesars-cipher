import collections

start_letter = ord('a')
end_letter = ord('z')
letters_range = range(start_letter, end_letter + 1)

def algorithm(text, offset, encrypt):
    res = ''
    for letter in text:
        upper_letter = False
        if ord(letter.lower()) not in letters_range:
            res += letter
            continue
        if letter.upper() == letter:
            upper_letter = True
            letter = letter.lower()
        if encrypt:
            letter_offset = ord(letter) + (ord(offset) - start_letter)
        else:
            letter_offset = ord(letter) + (start_letter - ord(offset))
        if letter_offset > end_letter:
           letter_offset -= end_letter - start_letter + 1

        if letter_offset < start_letter:
            letter_offset += end_letter - start_letter + 1

        letter = chr(letter_offset)
        if upper_letter:
            letter = letter.upper()
        res += letter

    return res


def calc_freq(text):
    freq = dict()
    all_letters = 0
    for i in range(start_letter, end_letter+1):
        freq[chr(i)] = 0.0
    for letter in text:
        letter = letter.lower()
        if ord(letter) not in letters_range:
            continue
        freq[letter] += 1
        all_letters += 1
    if all_letters == 0:
        return {}
    for key in freq.keys():
        freq[key] /= all_letters
    od = collections.OrderedDict(sorted(freq.items()))
    return od


def prediction(text):
    freq = calc_freq(text)
    max_freq = 0.0
    max_freq_letter = ''
    for key in freq.keys():
        if max_freq < freq[key] and ord(key) in letters_range:
            max_freq_letter = key
            max_freq = freq[key]
    if max_freq_letter == '' or ord('e') == ord(max_freq_letter):
        return 'a'
    else:
        if ord(max_freq_letter) < ord('e'):
            return_letter = ord(max_freq_letter) + ord('z') - ord('e')+ 1
        else:
            return_letter = start_letter + ord(max_freq_letter) - ord('e')
        return chr(return_letter)

def diagram_data(text):
    data = list()
    data.append(['letter', 'frequency'])
    freq = calc_freq(text)
    if freq == {}:
        return []
    for key in freq.keys():
        data.append([key, freq[key]])
    return data

def diagram_options():
    options = {
     'title': 'Frequency of the letters in the text',
     'hAxis': {'title': 'Letter',
                'viewWindowMode' : 'maximized'},
     'vAxis': {'title': 'Frequency'}
    }
    return options
