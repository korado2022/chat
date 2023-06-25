import subprocess

PROCESS = []

while True:
    ANSWER = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ANSWER == 'q':
        break
    elif ANSWER == 's':
        PROCESS.append(subprocess.Popen('python server/server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client/client.py -a 127.0.0.1 -p 8079 -n test_1',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client/client.py -a 127.0.0.1 -p 8079 -n test_2',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client/client.py -a 127.0.0.1 -p 8079 -n test_3',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ANSWER == 'x':
        while PROCESS:
            PROCESS.pop().kill()
