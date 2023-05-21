import socket
import threading
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [23, 24, 25, 1]
for i in leds:
    GPIO.setup(i, GPIO.OUT)
    pass

HOST = 'localhost'
PORT = 9999

send_message:str = ''

def sending_message(clnt):
    while True:
        if GPIO.input(leds[0]):
            pass 
        elif GPIO.input(leds[1]):
            pass


def received_message(clnt):
    GPIO.output(leds[0], GPIO.LOW)
    GPIO.output(leds[1], GPIO.LOW)
    GPIO.output(leds[2], GPIO.LOW)
    GPIO.output(leds[3], GPIO.LOW)
    while True:
        data = clnt.recv(1024).decode(encoding='utf-8')
        data = data.strip()
        print(f'client Data : {data}')
        for i in leds:
            GPIO.output(i, GPIO.LOW)  # 매번 LED 초기화  
        
        if data =='Strikes: 0, Balls: 1':
            GPIO.output(leds[0], GPIO.HIGH)
            print("Strikes: 0, Balls: 1")
            pass
        elif data == 'Strikes: 0, Balls: 2':
            GPIO.output(leds[1], GPIO.HIGH)
            print("Strikes: 0, Balls: 2")
            pass
        elif data =='Strikes: 0, Balls: 3':
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[1], GPIO.HIGH)
            print("Strikes: 0, Balls: 3")
            pass
        elif data == 'Strikes: 1, Balls: 0':
            GPIO.output(leds[2], GPIO.HIGH)
            print("Strikes: 1, Balls: 0")
            pass
        elif data == 'Strikes: 1, Balls: 1':
            GPIO.output(leds[2], GPIO.HIGH)
            GPIO.output(leds[0], GPIO.HIGH)
            print("Strikes: 1, Balls: 1")
            pass
        elif data == 'Strikes: 1, Balls: 2':
            GPIO.output(leds[2], GPIO.HIGH)
            GPIO.output(leds[1], GPIO.HIGH)
            print("Strikes: 1, Balls: 2")
            pass
        elif data == 'Strikes: 2, Balls: 0':
            GPIO.output(leds[3], GPIO.HIGH)
            print("Strikes: 2, Balls: 0")
            pass
        elif data == 'Strikes: 2, Balls: 1':
            GPIO.output(leds[3], GPIO.HIGH)
            GPIO.output(leds[0], GPIO.HIGH)
            print("Strikes: 2, Balls: 1")
            pass

        elif data == 'Congratulations, you guessed the correct numbers!':
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[1], GPIO.HIGH)
            GPIO.output(leds[2], GPIO.HIGH)
            GPIO.output(leds[3], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(leds[1], GPIO.LOW)
            GPIO.output(leds[3], GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(leds[0], GPIO.LOW)
            GPIO.output(leds[1], GPIO.HIGH)
            GPIO.output(leds[2], GPIO.LOW)
            GPIO.output(leds[3], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(leds[1], GPIO.LOW)
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[3], GPIO.LOW)
            GPIO.output(leds[2], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(leds[0], GPIO.LOW)
            GPIO.output(leds[1], GPIO.HIGH)
            GPIO.output(leds[2], GPIO.LOW)
            GPIO.output(leds[3], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(leds[1], GPIO.LOW)
            GPIO.output(leds[0], GPIO.HIGH)
            GPIO.output(leds[3], GPIO.LOW)
            GPIO.output(leds[2], GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(leds[0], GPIO.LOW)
            GPIO.output(leds[1], GPIO.LOW)
            GPIO.output(leds[2], GPIO.LOW)
            GPIO.output(leds[3], GPIO.LOW)
            print('Congratulations, you guessed the correct numbers!')
            pass        
        
        #print(data)
    
with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0) as clnt:
    try:
        clnt.connect((HOST, PORT))
        t1 = threading.Thread(target=sending_message, args=(clnt,))
        t2 = threading.Thread(target=received_message, args=(clnt,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()