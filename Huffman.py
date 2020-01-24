#!/usr/bin/env python

#modules
import os
import sys

#open file
nom = sys.argv[1]
if os.path.isfile(nom) == True:
	with open(nom,'r') as archivo:
		sec = archivo.read()
		archivo.close()
else:
	sec = nom
print('\nSequence:\n',sec)
	
#Get character frequency
sect = set(sec) #set del texto
lista_car = []
lon = len(sec)
for i in sect:
    lista_car.append([i,round(sec.count(i)/lon,2)])

print('\nCharacter frequency: \n',lista_car)
lista_car.sort(key=lambda x: x[1]) 

#make Huffman tree
nodo = 0
valor = 0
i = 0
lista = list(lista_car)
size = len(lista)
num_nodo = 0
nivel = 0
id_nodo = ''
dicc_arbol = dict({0:lista_car})


while i < size:
	if len(lista) == 1:
		break      
	else:
	    lista.sort(key=lambda x: x[1]) 
	    valor = round(lista[0][1] + lista[1][1],2)
	    nodo = round(nodo + valor,2)
	    if len(lista[0][0]+lista[1][0]) > len(id_nodo):
	        nivel += 1
	        dicc_arbol[nivel] =[]
	            
	    id_nodo = lista[0][0]+lista[1][0]
	    lista.insert(0,[id_nodo,valor])
	    dicc_arbol[nivel].append([id_nodo,valor])
	    del(lista[1:3])
	    num_nodo += 1
	i += 1

## Get codes 
num = 0
for i in dicc_arbol.values():
	for j in i:
	        if num % 2 == 0:
	            j.append('0')
	        else:
	            j.append('1')
	        num += 1	


#get inverted dict
new_niv = nivel*1
new_dict = dict()
for i in dicc_arbol.values():
    new_dict.update({new_niv:i})
    new_niv += -1
new_dict[0][0][2] = '' 

print('\nHuffman tree: ')
for k in sorted(new_dict.keys()):
	print('Nivel ',k, new_dict[k])

#Non-canonic tree codes
dict_claves = {}
for i in sect:
    dict_claves.update({i : ''})
    for j in new_dict.values():
        for h in j: 
            if i in h[0]:
                dict_claves[i] += h[2]

dict_ord = sorted(dict_claves.items(), key=lambda x: len(x[1]))

#binary sum
def add_binary_nums(x, y): 
        max_len = max(len(x), len(y)) 
  
        x = x.zfill(max_len) 
        y = y.zfill(max_len) 
          
        # initialize the result 
        result = '' 
          
        # initialize the carry 
        carry = 0
  
        # Traverse the string 
        for i in range(max_len - 1, -1, -1): 
            r = carry 
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result 
            carry = 0 if r < 2 else 1     # Compute the carry. 
          
        if carry !=0 : result = '1' + result 
  
        return result.zfill(max_len) 


#Get canonic tree codes
lista_ord = [list(i) for i in dict_ord]
lista_ord[0][1] = '0'*len(lista_ord[0][1])
long = len(lista_ord)
bit = len(dict_ord[0][1])

for i in range(1,long):
    new_bit = len(dict_ord[i][1])
    if new_bit >= bit:
        lista_ord[i][1] = add_binary_nums(lista_ord[i-1][1],'1')
        if new_bit > bit:
            lista_ord[i][1] += '0'*(new_bit - bit)
    bit = len(lista_ord[i][1])

print('\nCanonic tree codes: \n',lista_ord)

#Get binary sequence
for i in lista_ord:
	sec = sec.replace(i[0],i[1])

print('\nBinary Sequence: ',sec)