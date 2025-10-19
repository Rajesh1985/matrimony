import importlib
modules = ('cryptography','pymysql')
for m in modules:
    try:
        importlib.import_module(m)
        print(m + ' OK')
    except Exception as e:
        print(m + ' FAILED: ' + str(e))
