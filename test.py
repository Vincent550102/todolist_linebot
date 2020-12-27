
from time import sleep
import configparser,requests,json,datetime
Y = datetime.datetime.now().year
M = datetime.datetime.now().month
D = datetime.datetime.now().day
T = datetime.datetime.now().time()
Y_M_D = Y+M+D
Ts = datetime.datetime.now().time().second+datetime.datetime.now().time().minute*60+datetime.datetime.now().time().hour*3600
Ts_minal_Y_M_D = Ts//Y_M_D
num = 14
print('現在是{}年{}月{}日{}'.format(str(Y),str(M),str(D),str(T)))
sleep(1)
print('{}+{}+{}是{}'.format(str(Y),str(M),str(D),str(Y_M_D)))
sleep(1)
print('今天已過了{}秒'.format(str(Ts)))
sleep(1)
print('{}除以{}是{}餘{}'.format(str(Ts),str(Y_M_D),str(Ts_minal_Y_M_D),str(Ts%Y_M_D)))
sleep(1)
print('{}加上{}減去{}是{}'.format(str(Y_M_D),str(Ts_minal_Y_M_D),str(Ts%Y_M_D),str(Y_M_D+Ts_minal_Y_M_D-Ts%Y_M_D)))
final = Y_M_D+Ts_minal_Y_M_D-Ts%Y_M_D
sleep(1)
if final >= num:
    print('最後{}減去{} 所以...'.format(str(final),str(final-num)))
else:
    print('最後{}加上{} 所以...'.format(str(final),str(num-final)))