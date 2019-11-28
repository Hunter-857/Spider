import hashlib


def md5(str):
    md = hashlib.md5()
    md.update(str.encode('utf-8'))
    print("1", md.digest())
    md.update(str.join('test').encode('utf-8'))
    print("2", md.digest())
    print(md.hexdigest())


def sha(str):
    sha1 = hashlib.sha1()
    sha1.update(str.encode('utf-8'))
    print('这里将是“乱码”：', sha1.digest())
    print('SHA1:', sha1.hexdigest())


if __name__ == '__main__':
    print("hello")
    md5("this is a sentence")
    sha("this is a sentence")
