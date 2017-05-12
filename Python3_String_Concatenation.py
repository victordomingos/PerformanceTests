#!/usr/bin/env python3.6
# encoding: utf-8
"""
Test some different ways to achieve string concatenation in order to 
see how much time it takes.

© 2017 Victor Domingos
Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
"""

import sys
from timeit import default_timer as timer
print(sys.version)

TEST_SIZE = 1_000_000_000
print(f"Testing a {TEST_SIZE} times loop...")

appstart = timer()


def maisigual(a,abc):
    for i in range(TEST_SIZE):
        a += abc
    return a

def mais(a,abc):
    for i in range(TEST_SIZE):
        a = a + abc
    return a

def mais2(a,abc):
    return a + abc

def aformat(a,abc):
    for i in range(TEST_SIZE):
        a = '{}{}'.format(a, 'abc')
    return a

def aformat2(a,abc):
    return '{}{}'.format(a, 'abc')

def vezes(a,abc):
    return (a + TEST_SIZE*abc)

def join2(a,abc):
    lista = ['abc' for i in range(TEST_SIZE)]
    a = ''.join(lista)
    return a

def append1(a,abc):
    lista = [a]
    for i in range(TEST_SIZE):
        lista.append(abc)
    return ''.join(lista)


start = timer()
maisigual('','abc')
end = timer()
delta = end - start
print('a += abc:', delta)

start = timer()
mais('','abc')
end = timer()
delta2 = end - start
print('a + abc: ', delta2)

start = timer()
for i in range(TEST_SIZE):
    a = mais2('','abc')
end = timer()
delta22 = end - start
print('a + abc(): ', delta22)

"""
start = timer()
aformat('','abc')
end = timer()
delta3 = end - start
print('=format: ', delta3)
"""
print('=format: ', "---skipped---")


start = timer()
for i in range(TEST_SIZE):
    a = aformat2('','abc')
end = timer()
delta33 = end - start
print('=format2(): ', delta33)


start = timer()
vezes('','abc')
end = timer()
delta5 = end - start
print('=vezes():', delta5)

start = timer()
x = '' + TEST_SIZE*'abc'
end = timer()
delta6 = end - start
print('=vezes:  ', delta6)

start = timer()
join2('','abc')
end = timer()
deltaj2 = end - start
print('=join(): ', deltaj2)

start = timer()
append1('','abc')
end = timer()
delta7 = end - start
print('append1: ', delta7)


print('>>> total:', timer()-appstart)

