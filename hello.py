'''hello

!!!! IMPORTANT !!!!
vvvvvvvvvvvvvvvvvvvv

Please don't view this file directly.
Run it and complete this simple quest escalating root privileges.
(getting source code is part of quest).
'''

import time
import sys
import random

# for security reasons, we generate root password in run-time.
ROOT_PASSWORD = random.randbytes(10).hex()

default_delay = 0.1
current_user = None
current_prev = None

def output(text):
    '''output some text'''
    global default_delay

    i = 0
    while i < len(text):
        if text[i] == '$':
            i += 1
            if text[i] == '$':
                i += 1
                continue

            j = text.index('$', i)
            time.sleep(float(text[i:j]))
            i = j + 1
            continue
        if text[i] == '#':
            i += 1
            if text[i] == '#':
                i += 1
                continue

            j = text.index('#', i)
            sys.stdout.write(text[i:j])
            sys.stdout.flush()
            i = j + 1
            continue
        if text[i] == '%':
            i += 1
            if text[i] == '%':
                i += 1
                continue

            j = text.index('%', i)
            key, value = text[i:j].split(':')
            try:
                value = float(value)
            except ValueError:
                pass
            globals()[key] = locals()[key] = value
            i = j + 1
            continue
        if text[i] == '@':
            i += 1
            if text[i] == '@':
                i += 1
                continue

            j = text.index('@', i)
            default_delay = float(text[i:j])
            i = j + 1
            continue

        sys.stdout.write(text[i])
        sys.stdout.flush()

        time.sleep(default_delay * random.uniform(0.5, 2.0))

        i += 1


# TODO: replace all usages of legacy %-syntax with new modern @-syntax
output(
    '$0.5$'
    '#' + '\n' * 100 + '#'
    '@0.1@'
    '> $1.0$booting up@0.5@...@0.1@\n'
    '#\r#'
    '#\033[32m#'
    '$0.1$'
    '@0.005@'
    + ''.join(random.choice('01\n') for _ in range(100)) +
    '@0.1@'
    '#' + '\n' * 100 + '#'
    '$0.5$'
    '@0.01@> booting complete.'
    '$1.0$'
    '%default_delay:0.03%'
    '\n> welcome to hello, the most modern operating system'
    '$1.0$\n> we aim to provide you a simple$0.5$, fast$0.5$, and$0.5$ the most important$0.5$, secure operating system'
    '$0.5$\n> we suggest you try our system$0.5$, guest user credentials are hello$0.5$:hello'
)


def login():
    '''login'''
    global current_user, current_prev

    while True:
        try:
            output('$0.7$\n> enter your username: ')
            username = input()
            output('$0.7$> enter your password: ')
            password = input()

            if (username == 'hello' and password == 'hello'
                    or username == 'root' and password == ROOT_PASSWORD):
                current_user = username
                current_prev = 0 if username == 'root' else 1

            if current_user is not None:
                motd()
                shell()
            else:
                output('$2.0$> invalid credentials, try again')
        except KeyboardInterrupt:
            pass


def motd():
    '''message of the day'''

    output(f'@0.01@welcome back, {current_user}!')
    output('$2.0$\nno mail.\n\n')


def shell():
    '''shell emulator'''

    while True:
        try:
            output(f'{current_user}> ')
            cmd = input()
            args = cmd.split()
            if not args:
                continue
            cmd, args = args[0], args[1:]

            match cmd:
                case 'ls':
                    output('directory listing:\n')
                    output('@0.01@-------------------------\n@0.03@')
                    output('1. help.txt (file)\n')
                    output('2. hello.py (file)\n')
                    output('3. secret.txt (file, protected)\n')
                case 'opt':
                    output('@0.1@speeding up the system@2.0@....\n@0.00001@done, system has been optimized!\n')
                case 'help':
                    output('ERROR: can\'t execute "prrint help.txt", unknown command "prrint"\n')
                case 'logout':
                    break
                case 'print':
                    if not args:
                        output('usage: print <filename>\n')
                    else:
                        filename = args[0]
                        match filename:
                            case 'help.txt':
                                output('---- help.txt ----\n')
                                output('Welcome to hello! Our system is under active development, but we have the necessary minimum:\n')
                                output('> ls\n')
                                output('this command will kindly print you all the files on the system\n')
                                output('> print\n')
                                output('this command will kindly print you file contents\n')
                                output('> opt\n')
                                output('this command is the embodiment of our latest cutting-edge developments!\n')
                                output('run it and your system will be optimized and run fast\n')
                                output('> logout\n')
                                output('log out thr system\n')
                                output('---- cut here ----\n')
                            case 'hello.py':
                                output('---- hello.py ----\n')
                                with open('hello.py') as f:
                                    c = f.read()
                                for i, b in enumerate(c):
                                    print(b, end='')
                                    sys.stdout.flush()
                                    time.sleep(0.03 * default_delay * i)
                                output('---- cut here ----\n')
                            case 'secret.txt':
                                if current_prev == 0:
                                    output('---- secret.txt ----\n')
                                    output('KEEP THIS FILE SECURE!!!\n')
                                    with open('secret.txt') as f:
                                        c = f.read()
                                    sys.stdout.write(c)
                                    sys.stdout.flush()
                                    output('---- cut here ----\n')
                                    output('\n$1.0$\n$1.0$')
                                    output('@0.1@')
                                    output('> Congratulations, you\'ve just completed this game.$1.0$\n')
                                    output('> I hope it wasn\'t *too* easy *blinking face*$2.0$\n')
                                    output('> @1.0@...\n')
                                    output('>\n@0.5@')
                                    shutdown()
                                else:
                                    output('insufficient privileges to perform this operation\n')
                            case other:
                                output(f'no such file: {other}\n')
                case 'logout':
                    logout()
                case command:
                    output(f'unknown command {command}\n')
        except KeyboardInterrupt:
            try:
                output('cancelled.\n')
            except KeyboardInterrupt:
                pass

    logout()


def logout():
    '''log out'''
    global current_user, current_prev

    output(f'@0.01@bye, {current_user}!\n\n\n\n')

    current_user = None
    current_prev = None

def shutdown():
    '''shutdown'''
    output(
        '> system is shutting down\n'
        '@0.005@'
        + ''.join(random.choice('01\n') for _ in range(100)) +
        '#\033[00m#'
    )
    exit(0)


login()
shutdown()
