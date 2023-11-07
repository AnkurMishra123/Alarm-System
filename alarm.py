import cv2
import threading
import winsound
import requests
import imutils

#start camera

cap= cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

_, start_frame=cap.read()
start_frame=imutils.resize(start_frame,width=500)
start_frame=cv2.cvtColor(start_frame,cv2.COLOR_BGR2GRAY)
start_frame=cv2.GaussianBlur(start_frame,(21,21),0)

alarm=False
alarm_mode=False
alarm_counter=0


def message_bot(bot_message):
    
    TOKEN = "<Enter your token for the telegram bot>"
    chat_id = "<Enter the token for the chat bot>"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={bot_message}"
    print(requests.get(url).json()) # this sends the message


    
def beep_alarm():
    global alarm

    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        # We have to send the alert
        winsound.Beep(2500, 1000)
    alarm = False

    if alarm_counter >= 5:  # Add this condition to trigger the message_bot function
        message_bot("Alarm has been hit 5 times!")


while True:

    _, frame= cap.read()
    frame= imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw=cv2.GaussianBlur(frame_bw, (5,5),0)

        difference= cv2.absdiff(frame_bw, start_frame)
        thresold=cv2.threshold(difference, 25, 255,cv2.THRESH_BINARY)[1]
        start_frame=frame_bw

        if thresold.sum()>300:
            alarm_counter +=1
        else :
            if alarm_counter > 0:
                alarm_counter -=1

        cv2.imshow("Cam", thresold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter>20:
        if not alarm:
            alarm=True
            
            threading.Thread(target=beep_alarm).start()
    
    key_pressed= cv2.waitKey(30)
    if key_pressed==ord('t'):
        alarm_mode=not alarm_mode
        alarm_counter=0
    if key_pressed == ord('q'):
        alarm_mode=False
        break

cap.release()
cv2.destroyAllWindows()

        
        
            
