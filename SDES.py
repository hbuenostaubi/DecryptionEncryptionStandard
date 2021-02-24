#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 21:32:45 2021

@author: hbueno2
"""
import pandas as pd

def splitInts(intList):
    if(type(intList)!=str):
        strList=str(intList)
        intList=map(int, strList)
    else:
        intList=map(int, intList)
    return list(intList)

def getKeys(tenBitKey):
    tenBitKey=splitInts(tenBitKey)
    pTen= [3,5,2,7,4,10,1,9,8,6]
    leftS=[2,3,4,5,1, 7,8,9,10,6]
    leftSS=[3,4,5,1,2, 8,9,10,6,7]
    pEight=[6,3,7,4,8,5,10,9]
    keyOne=[]
    keyTwo=[]
    keyTwoo=[]
    keyO=[] 
    keyT=[]
    for i in range(0,10):
        keyOne.append(tenBitKey[pTen[i]-1])
    for i in range(0,10):
        keyTwo.append(keyOne[leftS[i]-1])
    keyOne=keyTwo
    pTen=keyTwo
    for i in range(0,10):
        keyTwoo.append(pTen[leftSS[i]-1])
    for i in range(0,8):
        keyO.append(keyOne[pEight[i]-1])
        keyT.append(keyTwoo[pEight[i]-1])
    return keyO,keyT

#### start the process after getting key

def IP(plainText):
    text=plainText
    ip=[2,6,3,1,4,8,5,7]
    new=[]
    for i in range(8):
        new.append(text[ip[i]-1])
    return new

def EP(text):
    text=text[4:8]
    ep=[4,1,2,3 ,2,3,4,1]
    new=[]
    for i in range(8):
        new.append(text[ep[i]-1])
    return new

def Fk(key, ip_t):
    ep=EP(ip_t)
    xor=[]

    for i in range(8):
        if(ep[i]==key[i]): 
            xor.append(0) 
        else: xor.append(1)
    return xor

#### XOR part
def bitCount(bitText):
    if (bitText=="00"):
        return 0
    elif bitText=="01":
        return 1
    elif bitText=="10":
        return 2
    else:
        return 3

def xorCkr(xorT):
    row=bitCount(str(xorT[0])+str(xorT[3]))
    col=bitCount(str(xorT[1])+str(xorT[2]))
    row2=bitCount(str(xorT[4])+str(xorT[7]))
    col2=bitCount(str(xorT[5])+str(xorT[6]))

    return row, col, row2, col2
    
def bit(df_result):
    if df_result==0:
        return "00"
    elif df_result==1:
        return "01"
    elif df_result==2:
        return "10"
    else: return "11"
    
def xor(xorText):
    d={0:[1,3,0,3], 1:[0,2,2,1],2:[3,1,1,3],3:[2,0,3,2]}
    d2={0:[0,2,3,2], 1:[1,0,0,1],2:[2,1,1,0],3:[3,3,0,3]}
    df1=pd.DataFrame(data=d)
    df2=pd.DataFrame(data=d2)
    row,col,row2,col2=xorCkr(xorText)
    
    return splitInts(bit(df1[col][row])+bit(df2[col2][row2]))

def p4(text):
    p4=[2,4,3,1]
    new=[]
    for i in range(4):
        new.append(text[p4[i]-1])
    return new
    
def xor4(p4,ip):
    xor=[]
    for i in range(4):
        if(ip[i]==p4[i]): 
            xor.append(0) 
        else: xor.append(1)
    for i in range(4,8):
        xor.append(ip[i])            
    return xor
    
def SW(xor):
    sw=[]
    for i in range(4,8):
        sw.append(xor[i])
    for i in range(4):
        sw.append(xor[i])
    
    return sw

def ip_inv(txt):
    ip_inv=[4,1,3,5, 7,2,8,6]
    new_inv=[]
    for i in range(8):
        new_inv.append(txt[ip_inv[i]-1])
    return new_inv
    

###### Key Generation
tenBitKey="1010111111"
keyOne,keyTwo=getKeys(tenBitKey)

print("K1:", keyOne, "K2:", keyTwo)

###### start of main 
x="00000000"
plainText=splitInts(x)
print("Plaintext: ",plainText)
plainText2=IP(plainText)       ### IP
print("IP:", plainText2)
fkOne=Fk(keyOne,plainText2)    ### fk(k1)
print("Fk1:", fkOne)
ckr=xor(fkOne)      

ckrp4=p4(ckr)
sw=SW(xor4(ckrp4,plainText2))   #### sw
print("SW:",sw)
fkTwo=Fk(keyTwo, sw)         ### fk(k2)
print("fkTwo", fkTwo)

ckr2=xor(fkTwo)
ckr2p4=p4(ckr2)

encryption=ip_inv(xor4(ckr2p4,sw))

print("Encrypted PlainText: ",encryption)

###### Decryption
print("-----------------------------------")
x="01010101"
plainText=splitInts(x)
encryption=plainText

plainText=IP(encryption)       ### IP
print("IP:",plainText)
fkOne=Fk(keyTwo, plainText)         ### fk(k2)
print("fk2:",fkOne)
ckr=xor(fkOne)      

ckrp4=p4(ckr)
sw=SW(xor4(ckrp4,plainText))   #### sw
print("SW:",sw)
fkTwo=Fk(keyOne, sw)         ### fk(k1)
print("fk1:",fkTwo)
ckr2=xor(fkTwo)
ckr2p4=p4(ckr2)

encryption=ip_inv(xor4(ckr2p4,sw))
print("Decrypted Plaintext:",encryption)
print("Are they equal?", encryption==splitInts(x))





  
# Recursive function to get all bits
def returnBitStr(arr, n):  
    bitStr=''
    for i in range(0, n):
        bitStr+=str(arr[i])
    return bitStr
  
# Recursive permutation
def generateAllBinaryStrings(n, arr, i, arr2):  
    
    if i == n: 
        arr2.append(returnBitStr(arr, n))  
        return arr2
      
    arr[i] = 0
    generateAllBinaryStrings(n, arr, i + 1,arr2)  
  
    arr[i] = 1
    generateAllBinaryStrings(n, arr, i + 1, arr2)  
  
# driver
if __name__ == "__main__":  
  
    n = 10
    arr = [None] * n  
    arr2=[]
    #Get all binary strings modifier
    generateAllBinaryStrings(n, arr, 0, arr2)  




