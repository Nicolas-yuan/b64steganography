'''
Author: 拾柒
Date: 2020-11-12 21:17:24
LastEditTime: 2020-11-14 18:29:23
Description: Base64 steganography
'''
'''
隐写原理:
base64将二进制以6bit为一个字符编码进行重新编码，如果二进制长度为6的倍数，则编码无冗余,
若长度不是6的倍数，则存在2bit（或4bit）长度的二进制无法编码，此时需要填充长度为4bit（或2bit）的0完成编码，
而后填充长度为12bit（或6bit）的0表示前面的数据填充了几个0，用于解码，最后填充的0编码为‘=’,
此时可把长度为4bit（或2bit）的填充数据0替换为要隐写的数据二进制值，然后再编码完成隐写.
'''
'''
提取原理1：
base64根据等号数量判断隐写bit长度，读取等号前一个字符的base64编码，提取尾部对应长度的bit，组合后解码.
提取原理2：
base64隐写的数据对解密无影响，但隐写后加密的字符与未隐写加密的字符不一样，
差值(不能用ASCII码的差值，要用base64编码的差值)是隐写的二进制对应的十进制值.
使用方法：
cmd中输入“ python b64stegano.py [filename] [a,b]”
'''
import sys
import base64

def to_bin(value, num):#十进制数据，二进制位宽
	bin_chars = ""
	temp = value
	for i in range(num):
		bin_char = bin(temp % 2)[-1]
		temp = temp // 2
		bin_chars = bin_char + bin_chars
	return bin_chars.upper()#输出指定位宽的二进制字符串

base64_dica={
    'A':'000000','B':'000001','C':'000010','D':'000011','E':'000100','F':'000101','G':'000110','H':'000111',
    'I':'001000','J':'001001','K':'001010','L':'001011','M':'001100','N':'001101','O':'001110','P':'001111',
    'Q':'010000','R':'010001','S':'010010','T':'010011','U':'010100','V':'010101','W':'010110','X':'010111',
    'Y':'011000','Z':'011001','a':'011010','b':'011011','c':'011100','d':'011101','e':'011110','f':'011111',
    'g':'100000','h':'100001','i':'100010','j':'100011','k':'100100','l':'100101','m':'100110','n':'100111',
    'o':'101000','p':'101001','q':'101010','r':'101011','s':'101100','t':'101101','u':'101110','v':'101111',
    'w':'110000','x':'110001','y':'110010','z':'110011','0':'110100','1':'110101','2':'110110','3':'110111',
    '4':'111000','5':'111001','6':'111010','7':'111011','8':'111100','9':'111101','+':'111110','/':'111111'
}#base64编码对应表,用于提取原理1

base64_dicb={
    'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
    'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,
    'Q':16,'R':17,'S':18,'T':19,'U':20,'V':21,'W':22,'X':23,
    'Y':24,'Z':25,'a':26,'b':27,'c':28,'d':29,'e':30,'f':31,
    'g':32,'h':33,'i':34,'j':35,'k':36,'l':37,'m':38,'n':39,
    'o':40,'p':41,'q':42,'r':43,'s':44,'t':45,'u':46,'v':47,
    'w':48,'x':49,'y':50,'z':51,'0':52,'1':53,'2':54,'3':55,
    '4':56,'5':57,'6':58,'7':59,'8':60,'9':61,'+':62,'/':63
}#base64编码对应表，用于提取原理2

hidebit = ''#存储隐写的bit数据
m = ''#存储结果
argvs = sys.argv#获取命令行参数
fc = open(argvs[1],'r')#打开文件
lines = fc.read().split('\n')#读取内容，并按行分割

##################提取原理1
if argvs[2] == 'a':
#判断每行是否有隐写数据，有读取存入hidebit
    for line in lines:
        if line != '':
            if line[-1] == '=':#判断最后一个字符是不是‘=’，
                if line[-2] == '=':#判断倒数第二个字符是不是‘=’              
                        hidebit += base64_dica[line[-3]][2:]                  
                else:
                        hidebit += base64_dica[line[-2]][4:]
            else:
                pass
###################提取原理2
elif argvs[2] == 'b':
    #判断每行是否有隐写数据，有计算差值后转为二进制存入hidebit
    for line in lines:
        line_row = base64.b64encode(base64.b64decode(line)).decode('utf-8')
        if line != '':
            if line[-1] == '=':#判断最后一个字符是不是‘=’，
                if line[-2] == '=':#判断倒数第二个字符是不是‘=’
                    temp = to_bin(base64_dicb[line[-3]]-base64_dicb[line_row[-3]],4)
                    hidebit += temp
                else:
                    temp = to_bin(base64_dicb[line[-2]]-base64_dicb[line_row[-2]],2)
                    hidebit += temp
            else:
                pass
#将二进制转化十进制，即ASCII码，再转化为字符
for i in range(0,len(hidebit),8):
    m += chr(int(hidebit[i:i+8],2))
print(m)