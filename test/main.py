import configparser

conf = configparser.ConfigParser()  # 类的实例化

path = r'D:\Desktop\test\config.ini'


# conf.read(path, encoding='utf-8-sig')
value = conf.get("",'auth_code')
# print("通过read方法取得的值为：", value)

exit()

import configparser

file = r'config.ini'
conf = configparser.ConfigParser()
conf.read(file, "UTF-8")

print(conf.get('cookies'))


def add(opt, key, value):
    conf.add_section(opt)
    for i in range(len(key)):
        conf.set(opt, key[i], value[i])

# add(opt='xzb', key=['name', 'qq'], value=['xzb', '123'])
# conf.write(open(file, "w"))
