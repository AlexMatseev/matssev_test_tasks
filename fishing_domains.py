import socket
from queue import Queue
from threading import Thread
import homoglyphs as hg


def replace_num_to_char(donor, current_index=0, combos=None):
    global similar_symbols
    if combos is None:
        combos = []
    if current_index == len(donor):
        combos.append(donor)
        return

    current_char = donor[current_index]
    if current_char in similar_symbols.keys():
        fake_donor = donor[:current_index] + similar_symbols[current_char] + donor[current_index + 1:]
        replace_num_to_char(fake_donor, current_index + 1, combos)
        replace_num_to_char(donor, current_index + 1, combos)
    else:
        replace_num_to_char(donor, current_index + 1, combos)
    return combos


def add_dots(donor):
    subdomains = []
    for i in range(1, len(donor)):
        if donor[i - 1] == '-' or donor[i] == '-':
            continue
        else:
            subdomains.append(donor[:i] + '.' + donor[i:])
    return subdomains


def delete_one_char(donor):
    return [donor[:i] + donor[i + 1:] for i in range(len(donor))]


def confirm_strategy(donor):
    fishing_list = []
    alphabet = ''.join([chr(i) for i in range(48, 58)])
    alphabet += ''.join([chr(i) for i in range(97, 123)])
    alphabet += ''.join([chr(i) for i in range(1072, 1104)])

    for char in alphabet:
        fishing_list.append(donor + char)

    homoglyphs = hg.Homoglyphs(alphabet=alphabet)
    fishing_list.extend(homoglyphs.get_combinations(donor))
    fishing_list.extend(replace_num_to_char(donor))

    fishing_list.extend(add_dots(donor))

    fishing_list.extend(delete_one_char(donor))

    return fishing_list


def get_ip(queue):
    for site in iter(queue.get, None):
        try:
            result = ': '
            for info in socket.getaddrinfo(site, 80):
                result += str(info[-1][0]) + ' '
        except IOError:
            pass
        else:
            result = site + ' ' + result
            print(result)


if __name__ == "__main__":
    donors_list = ['wikipedia']
    domains = ['ru', 'com', 'org', 'biz']
    similar_symbols = {'a': '4', 'g': '9', 'i': '1', 'l': '1', 'o': '0', 's': '5', 't': '7', 'z': '2',
                    'а': '4', 'б': '6', 'в': '8', 'з': '3', 'о': '0', 'т': '7'}
    combo_donor_list = []
    sites_list = []

    for donor in donors_list:
        combo_donor_list.extend(confirm_strategy(donor))

    for donor in combo_donor_list:
        for domain in domains:
            sites_list.append(donor + '.' + domain)

    queue = Queue()
    threads = [Thread(target=get_ip, args=(queue,)) for _ in range(50)]
    for t in threads:
        t.daemon = True
        t.start()

    for site in sites_list:
        queue.put(site)
    
    for _ in threads:
        queue.put(None)
        
    for t in threads:
        t.join()
