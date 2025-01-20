import getpass

# 使用卢氏算法检查卡号是否为有效
def validator(pan):
    rd1 = list(int(i)*2 for i in pan[-2::-2])
    rd2 = 0 
    for i in rd1: 
        if i < 10: rd2 += i
        else: rd2 += (int(str(i)[0]) + int(str(i)[1]))
    rd3 = list(int(i) for i in pan[-1::-2])
    return (sum(rd3) + rd2) % 10 == 0

# 获取卡号
def getPan(raw,start,end):
    pan = ''
    for char in raw[start:]:
        if char == end: break
        pan += char
    # 如果卡片为非银联卡且卡号长度大于16位，截取前16位（只有银联卡可能有超过16位的卡号）
    if pan[0] != '6' and len(pan) > 16:
        pan = pan[:16]
    return pan

# 获取卡片有效期
def getExp(raw,start):
    if raw[0] == '%':
        exp = raw[raw.find(start,raw.find(start) + 1) + len(start) : raw.find(start,raw.find(start) + 1) + len(start) + 4]
    else: 
        exp =  raw[raw.find(start) + len(start) : raw.find(start) + len(start) + 4]
    if exp == '0000': return 'N/A'
    return exp

# 获取持卡人姓名
def getCH(raw):
    if raw[0] == '%':
        ch = raw[raw.find('^') + 1 : raw.find('^',raw.find('^') + 1)].strip()
        if ch == '': return 'N/A'
        return ch
    else: return 'N/A'

def reader():
    try:
        # 在终端界面隐藏磁信息
        raw = getpass.getpass(prompt='Swipe the card ==>', stream=None)
        pan, exp, ch  = 'N/A','N/A','N/A'
        if raw[0] == '%':
            pan = getPan(raw,2,'^')
            exp = getExp(raw,'^')
            ch = getCH(raw)
        elif raw[0] ==  ';':
            pan = getPan(raw,1,'=')
            exp = getExp(raw,'=')
            ch = getCH(raw)
        elif raw[0] == '+':
            pan = getPan(raw,3,'=')
            exp = getExp(raw,'==')
            ch = getCH(raw)
        elif raw == "exit":
            return {'status':'exit'}
        else: 
            return {'status':'Invalid card'}

        if validator(pan) == False:
            return {'status':'Invalid card'}
        return {'status':'OK','pan':pan,'exp':exp,'ch':ch}
    except:
        return {'status':'failure'}
