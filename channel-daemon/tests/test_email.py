
import sys
sys.path.append('../')  

from mail import send as mail

if __name__ == '__main__':
    mail('localhost:25', 'something@example.com', 'dummy@example.com', 'Hellooooooooooooo') 

