import hashlib
from datetime import datetime


def get_md5(username, password):
    """
    >>> get_md5("braund",'1234')
    '3186cbdbdeea28d452f1fcc3889ad5cb'
    >>> get_md5("password", '1234')
    '3b07f8d52653e3ebcb013a67e3467d84'
    """
    """
    # :param username:
    # :param password:
    # :return:
    """
    m = hashlib.md5()
    m.update(bytes(username + password + 'the salt' + str(datetime.now())
                   , encoding='utf-8'))
    return m.hexdigest()




