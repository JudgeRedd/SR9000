from termcolor2 import c

def log(msg: str, level: str='info') -> None:
    if(level == 'error'):
        print(c(msg).red.bold)
    elif(level == 'warning'):
        print(c(msg).yellow.bold)
    elif(level == 'success'):
        print(c(msg).green)
    elif(level == 'action'):
        print(c(msg).magenta)
    elif(level == 'info'):
        print(c(msg).cyan)