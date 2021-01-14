import requests


def iin_check(iin):
    url = 'https://stat.gov.kz/api/juridical/gov/?bin={}&lang=ru'.format(iin)
    r = requests.get(url)
    return r.json()['success']
