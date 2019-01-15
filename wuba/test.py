import random

import execjs
import requests

r = "21,136,0|22,136,139|24,134,162|26,132,185|27,130,205|28,129,222|29,127,258|31,126,278|32,125,315|32,124,352|33,123,368|33,122,391|33,122,407|33,121,418|34,121,433|34,119,469|35,118,489|37,117,524|38,117,543|39,114,580|40,112,617|41,110,639|43,108,659|43,107,676|44,106,712|44,104,734|46,102,770|47,100,791|47,99,810|48,97,827|50,96,864|50,94,885|51,92,902|52,91,922|53,90,939|53,88,959|53,88,976|54,87,995|55,85,1012|55,84,1034|56,84,1049|56,83,1067|57,82,1084|58,80,1103|59,80,1121|59,79,1144|60,78,1168|61,78,1188|61,77,1212|62,76,1250|63,76,1286|63,76,1323|64,76,1344|67,75,1382|68,75,1402|70,75,1439|71,75,1461|78,75,1497|83,75,1533|85,77,1552|91,78,1588|94,78,1624|95,79,1644|98,80,1681|100,81,1718|102,81,1737|104,83,1774|106,84,1795|108,86,1831|111,88,1868|113,88,1889|114,90,1926|115,91,1945|117,92,1982|121,96,2019|122,96,2039|123,97,2076|124,98,2096|125,99,2113|128,101,2148|129,102,2169|131,104,2206|133,106,2225|136,108,2261|139,110,2281|143,112,2318|144,113,2353|146,114,2372|152,117,2408|154,117,2429|156,117,2445|158,118,2482|159,118,2503|165,118,2540|169,118,2561|172,118,2598|172,118,2716|174,119,2740|176,120,2758|177,120,2766|179,121,2783|179,122,2792|181,122,2809|182,123,2818|183,124,2834|184,124,2852|185,125,2879|187,127,2895|189,127,2913|192,128,2929|192,129,2945|194,129,2962|195,130,2995|196,130,3036|198,131,3062|199,131,3080|199,132,3100|199,132,3300|"
tnum = 1
finish_r = ''
firstandsecondnumlist = []
for i in r.split('|')[:-1]:
    firstnum = i.split(',')[0]
    secondnum = i.split(',')[1]
    firstandsecondnumlist.append((firstnum,secondnum))
for i in r.split('|')[:-1]:
    (firstnum,secondnum) = random.choice(firstandsecondnumlist)
    firstandsecondnumlist.remove((firstnum,secondnum))
    print(len(firstandsecondnumlist))
    finish_r = finish_r+firstnum+','+secondnum+','+str(tnum)+'|'
    # tnum += random.choice([i for i in range(70,90)])
print(finish_r)


x = '170'
finger = "gkqaY0nLpbAs80tI3gmqRRGjqNdlJ4zMFl+UavbHyiT6D16o3PrvZ+bnhThDreglin35brBb//eSODvMgkQULA=="
responseId = 'e5b85d6a652c4280bb7fa65331f5883a'
sessionId = '5bd3389af2b64230a2a736c45a5e0636'

def get_jiami_data(responseId, fpToken, lastXpos, trace):
    jsCode = execjs.compile(open("./jiami.js", "r").read())
    jiami_data = jsCode.call("getSlideAnswer", responseId, fpToken, lastXpos, trace)
    return jiami_data
data = get_jiami_data(responseId,finger,x,finish_r)
print('data:',data)

pa = {
    'responseId':responseId,
    'sessionId':sessionId,
    'data':data
}
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}
req = requests.get('https://verifycode.58.com/captcha/checkV3',params=pa,headers=headers)
print(req.text)