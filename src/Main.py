import json
import math


def find_close(new_arg,yazar,stri):
    high=new_arg
    low=new_arg
    while low not in yazar[stri] and high not in yazar[stri]:
        low=low-1
        high=high+1
    if low in yazar:
        return low
    else:
        return high


data=[]
with open('books.json') as json_file1:
    data=json.load(json_file1)
    json_file1.close()
train=[]
test=[]
counter=0


for i in range(5000):
    try:
        if data[i]['page_count'] == 0:
            counter=counter+1
        else:
             train.append(data[i])
    except:
        counter=counter+1

#Test edilecek verinin ayrıldığı yer
for j in range(5000,len(data)):
    try:
        if data[j]['page_count'] == 0:
            counter=counter+1
        else:
            test.append(data[j])
    except:
        counter=counter+1

ms=0
#Yazar-sayfa sayısına göre eğitilen verimiz.
yazar={}
for x in range(len(train)):
    try:
        if train[x]['author'] in yazar:
            #Burada sayfa sayısına göre bölmelere ayırıyoruz
            #Arg sayfa sayısının indexsidir bu da sayfa sayısı 100 e bölünüp
            #yukarı yuvarlanarak alınmıştır.
            arg=int(math.ceil(train[x]['page_count']/100))
            if arg in yazar[train[x]['author']]:
                pass
            else:
                 yazar[train[x]['author']][arg]=0
                 yazar[train[x]['author']][arg+0.5]=0
                 
            yazar[train[x]['author']][arg]=yazar[train[x]['author']][arg] + train[x]['price']['current']
            yazar[train[x]['author']][arg+0.5]=yazar[train[x]['author']][arg+0.5]+1
        else:
            yazar[train[x]['author']] = {}
            arg=int(math.ceil(train[x]['page_count']/100))
            yazar[train[x]['author']][arg]=0
            yazar[train[x]['author']][arg+0.5]=0
            #Değerleri atıyoruz Kitap miktarı ve toplam fiyat
            yazar[train[x]['author']][arg]=yazar[train[x]['author']][arg] +train[x]['price']['current']
            yazar[train[x]['author']][arg+0.5]=yazar[train[x]['author']][arg+0.5]+1
    except:
        pass
    
yayin={}
country=0
#Yayinevi-sayfa sayısına göre eğitilen verilerimiz.
for x in range(len(train)):
    try:
        if train[x]['publisher'] in yayin:
            #Burada sayfa sayısına göre bölmelere ayırıyoruz
            #Arg sayfa sayısının indexsidir bu da sayfa sayısı 100 e bölünüp
            #yukarı yuvarlanarak alınmıştır.
            arg=int(math.ceil(train[x]['page_count']/100))
            if arg in yayin[train[x]['publisher']]:
                pass
            else:
                yayin[train[x]['publisher']][arg]=0
                yayin[train[x]['publisher']][arg+0.5]=0
                
            yayin[train[x]['publisher']][arg]=yayin[train[x]['publisher']][arg]+train[x]['price']['current']
            yayin[train[x]['publisher']][arg+0.5]= yayin[train[x]['publisher']][arg+0.5]+1
        else:
            yayin[train[x]['publisher']] = {}
            arg=int(math.ceil(train[x]['page_count']/100))
            yayin[train[x]['publisher']][arg]=0
            yayin[train[x]['publisher']][arg+0.5]=0
            yayin[train[x]['publisher']][arg]=yayin[train[x]['publisher']][arg]+train[x]['price']['current']
            yayin[train[x]['publisher']][arg+0.5]= yayin[train[x]['publisher']][arg+0.5]+1
    except:
        pass
genel={}    
#Sadece safya sayısına göre eğitilen verimiz
for x in range(len(train)):
    try:
        arg=int(math.ceil(train[x]['page_count']/100))
        if arg in genel:
            genel[arg]=train[x]['price']['current']+genel[arg]
        else:
            genel[arg]=0
            genel[arg]=train[x]['price']['current']+genel[arg]
        if arg+0.5 in genel:
            genel[arg+0.5]=genel[arg+0.5]+1
        else:
            genel[arg+0.5]=0
            genel[arg+0.5]=genel[arg+0.5]+1
    except:
        pass

#Buradaki değerler her test için toplam hata ve yapılan testi tutmakta
yayin_value=0
yazar_value=0
yayin_counter=0
yazar_counter=0
yazyay_value=0
yazyay_counter=0
sayfa_toplam=0
sayfa_count=0
hatalar={}
#Yazar hata fiyatı için
#Yayınevi hata fiyatı için
hatalar2={}
for x in range(len(test)):
    try:
        #Yazar
        if test[x]['author'] in yazar:
            new_arg=int(math.ceil(test[x]['page_count']/100))
            if new_arg in yazar[test[x]['author']]:
                value=0
                value=yazar[test[x]['author']][new_arg]/yazar[test[x]['author']][new_arg+0.5]
                yazar_value=yazar_value+abs(value-test[x]['price']['current'])
                yazar_counter=yazar_counter+1
                if  test[x]['author'] in hatalar:
                    hatalar[test[x]['author']][0]=hatalar[test[x]['author']][0]+abs(value-test[x]['price']['current'])
                    hatalar[test[x]['author']][1]=hatalar[test[x]['author']][1]+1
                else:
                    hatalar[test[x]['author']]={}
                    hatalar[test[x]['author']][0]=0
                    hatalar[test[x]['author']][1]=0
                    hatalar[test[x]['author']][0]=hatalar[test[x]['author']][0]+abs(value-test[x]['price']['current'])
                    hatalar[test[x]['author']][1]=hatalar[test[x]['author']][1]+1
            else:
                flow=find_close(new_arg,yazar,test[x]['author'])
                value=0
                value=yazar[test[x]['author']][flow]/yazar[test[x]['author']][flow+0.5]
                value=value - value*(abs(flow-new_arg)/flow)
                yazar_value=yazar_value+abs(value-test[x]['price']['current'])
                yazar_counter=yazar_counter+1
                if  test[x]['author'] in hatalar:
                    hatalar[test[x]['author']][0]=hatalar[test[x]['author']][0]+abs(value-test[x]['price']['current'])
                    hatalar[test[x]['author']][1]=hatalar[test[x]['author']][1]+1
                else:
                    hatalar[test[x]['author']]={}
                    hatalar[test[x]['author']][0]=0
                    hatalar[test[x]['author']][1]=0
                    hatalar[test[x]['author']][0]=hatalar[test[x]['author']][0]+abs(value-test[x]['price']['current'])
                    hatalar[test[x]['author']][1]=hatalar[test[x]['author']][1]+1
        #Yayın
        if test[x]['publisher'] in yayin:
            new_arg=int(math.ceil(test[x]['page_count']/100))
            if new_arg in yayin[test[x]['publisher']]:
                value=0
                value=yayin[test[x]['publisher']][new_arg]/yayin[test[x]['publisher']][new_arg+0.5]
                yayin_value=yayin_value+abs(value-test[x]['price']['current'])
                yayin_counter=yayin_counter+1
                if test[x]['publisher'] in hatalar2:
                    hatalar2[test[x]['publisher']][0]=hatalar2[test[x]['publisher']][0]+abs(value-test[x]['price']['current'])
                    hatalar2[test[x]['publisher']][1]=hatalar2[test[x]['publisher']][1]+1
                else:
                    hatalar2[test[x]['publisher']]={}
                    hatalar2[test[x]['publisher']][0]=0
                    hatalar2[test[x]['publisher']][1]=0
                    hatalar2[test[x]['publisher']][0]=hatalar2[test[x]['publisher']][0]+abs(value-test[x]['price']['current'])
                    hatalar2[test[x]['publisher']][1]=hatalar2[test[x]['publisher']][1]+1
            else:
                flow=find_close(new_arg,yayin,test[x]['publisher'])
                value=0
                value=yayin[test[x]['publisher']][flow]/yayin[test[x]['publisher']][flow+0.5]
                value=value - value*(abs(flow-new_arg)/flow)
                yayin_value=yayin_value+abs(value-test[x]['price']['current'])
                yayin_counter=yayin_counter+1
                if  test[x]['publisher'] in hatalar2:
                    hatalar2[test[x]['publisher']][0]=hatalar2[test[x]['publisher']][0]+abs(value-test[x]['price']['current'])
                    hatalar2[test[x]['publisher']][1]=hatalar2[test[x]['publisher']][1]+1
                else:
                    hatalar2[test[x]['publisher']]={}
                    hatalar2[test[x]['publisher']][0]=0
                    hatalar2[test[x]['publisher']][1]=0
                    hatalar2[test[x]['publisher']][0]=hatalar2[test[x]['publisher']][0]+abs(value-test[x]['price']['current'])
                    hatalar2[test[x]['publisher']][1]=hatalar2[test[x]['publisher']][1]+1
        #İkili
        if test[x]['author'] in yazar and test[x]['publisher'] in yayin:
            new_arg=int(math.ceil(test[x]['page_count']/100))
            if new_arg in yazar[test[x]['author']] and new_arg in yayin[test[x]['publisher']]:
                value=0
                value=yayin[test[x]['publisher']][new_arg]+yazar[test[x]['author']][new_arg]
                value=value/(yazar[test[x]['author']][new_arg+0.5]+yayin[test[x]['publisher']][new_arg+0.5])
                yazyay_value=yazyay_value+abs(value-test[x]['price']['current'])
                yazyay_counter=yazyay_counter+1
            else:
                flow=find_close(new_arg,yayin,test[x]['publisher'])
                flow2=find_close(new_arg,yazar,test[x]['publisher'])
                value=0
                value1=yayin[test[x]['publisher']][flow]
                value2=yazar[test[x]['author']][flow2]
                value1=value1 - value1*(abs(flow-new_arg)/flow)
                value2=value2 - value2*(abs(flow2-new_arg)/flow2)
                value=value1+value2
                value=value/(yazar[test[x]['author']][flow2+0.5]+yayin[test[x]['publisher']][flow+0.5])
                yazyay_value=yazyay_value+abs(value-test[x]['price']['current'])
                yazyay_counter=yazyay_counter+1
                pass
        #Sayfa sayısına göre.
        n_arg=int(math.ceil(test[x]['page_count']/100))
        if n_arg in genel:
            value=0
            value=genel[n_arg]/genel[n_arg+0.5]       
            sayfa_toplam=sayfa_toplam+abs(value-test[x]['price']['current']) 
            sayfa_count=sayfa_count+1        
    except:
        pass
print(yazar_value/yazar_counter)
print(yayin_value/yayin_counter)
print(yazyay_value/yazyay_counter)
print(sayfa_toplam/sayfa_count)
toplami=0
hata_graf={}
#Yazara göre hata payını tutan dictionary.
for x in range(len(train)):
    try:
        if train[x]['author'] in hatalar:
           hata_graf[train[x]['author']]=hatalar[train[x]['author']][0]/hatalar[train[x]['author']][1]
           toplami=toplami+hata_graf[train[x]['author']]
           
    except:
        pass
