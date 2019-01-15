from _md5 import md5

import numpy as np
import requests
from numpy import *
import matplotlib.pyplot as plt

class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode('utf-8')).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        return r.json()

def plot_line(x,y,xrange=None,yrange=None):
    '''

    :param x: x list
    :param y: y list
    :param xrange:x坐标范围
    :param yrange:y坐标范围
    :return: 画出折线图
    '''
    fig = plt.figure()
    ax = fig.add_subplot(3, 2, 1)
    ax.plot(np.array(x), np.array(y))

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    if xrange!=None:
        ax.set_xlim(xrange)
    if yrange!=None:
        ax.set_ylim(yrange)

    ax.invert_yaxis()
    plt.show()

def get_func(x,y):
    '''
    传入xlist  ,  ylist  list长度3
    生成一个一元二次方程
    :return: [a,b,c]
    '''
    if len(x) != len(y):
        print("Error: len(x) != len(y)")
    tempMat = mat(zeros((3, 3)))
    for i in range(0, 3):
        tempMat[0, i] = pow(x[i], 2)
        tempMat[1, i] = x[i]
        tempMat[2, i] = 1
    tempMatInv = np.linalg.inv(tempMat)
    tempY = mat(array(y))
    parameterAbc = tempY * tempMatInv
    listAbc = []
    for i in range(0, 3):
        listAbc.append(parameterAbc[0, i])
    return listAbc

def product_trace(res):

    x = []
    y = []
    for i in res:
        x.append(int(i.split(',')[0]))
        y.append(int(i.split(',')[1]))

    trace_x = []
    trace_y = []
    for _ in range(0,2):
        tepx = [x[_],x[_+1],x[_+2]]
        tepy = [y[_],y[_+1],y[_+2]]
        [a,b,c] = get_func(tepx,tepy)
        if _==0:
            for i in range(x[0],x[1]):
                trace_x.append(i)
                trace_y.append(a*i*i+b*i+c)
            for i in range(x[1],x[2]):
                trace_x.append(i)
                if random.randint(1,5) == 1:
                    trace_y.append((((float)(y[2]-y[1]))/(x[2]-x[1]))*(i-x[1])+y[1]+random.randint(-1,1))
                else:
                    trace_y.append((((float)(y[2] - y[1])) / (x[2] - x[1])) * (i - x[1]) + y[1])
        else:
            for i in range(x[2],x[3]):
                trace_x.append(i)
                trace_y.append(a*i*i+b*i+c)
    trace_x = [int(i) for i in trace_x]
    trace_y = [int(i) for i in trace_y]
    last_trace_x = []
    last_trace_y = []
    plot_line(trace_x,trace_y,[0,284],[0,160])
    xx = 0
    while xx<len(trace_x)-1:
        last_trace_x.append(trace_x[xx])
        last_trace_y.append(trace_y[xx])
        xx+=random.randint(1,4)
    last_trace_x.append(trace_x[-1])
    last_trace_y.append(trace_y[-1])

    trace_str = ''
    for i in range(0,len(last_trace_x)):
        trace_str += str(last_trace_x[i])+','+str(last_trace_y[i])+','+'1'+'|'

    return x[3]-x[0],trace_str


if __name__ == '__main__':
    res = ['60,130', '92,88', '139,135', '184,78']
    product_trace(res)