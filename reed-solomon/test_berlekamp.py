from numpy.random import randint

from reedsolomon import ReedSolomon
import random
import matplotlib.pyplot as plt
import numpy as np

def encode_test(message):
    reed_solomon = ReedSolomon(31,11)
    return reed_solomon.encode(message)

def simple_decode_test(message):
    reed_solomon = ReedSolomon(31,11)
    return reed_solomon.simple_decode(message)

def random_number(forbiden_number):
    #nie powtarza sie ta sama cyfra w miejscu, w ktorym była przed uszkodzeniem
    number = forbiden_number
    while number == forbiden_number:
        number = random.randint(-1,30)
        if number == -1:
            number = float('-inf')
    return number

def get_random_error(encoded_message, numbers_of_erros):
    """
    :param encoded_message: nazwa mówi sama za siebie
    :param numbers_of_erros: liczba błędów
    :return: wiadomość z losowymi błędami
    """
    encoded_message_length = len(encoded_message)
    list_of_indexes = list(range(0, encoded_message_length)) # range nie bierze ostatniego wyrazu
    for i in range(numbers_of_erros):
        index = random.choice(list_of_indexes)
        forbiden_number = encoded_message[index]
        encoded_message[index] = random_number(forbiden_number)
        list_of_indexes.remove(index)
    return encoded_message

def get_bundle_error(encoded_message, numbers_of_erros, start_index, end_index):
    """"
    :param encoded_message: nazwa mówi sama za siebie
    :param numbers_of_erros: liczba błędów
    :param start_index: lewy skrajny indeks
    :param end_index: prawy skrajny indeks
    :return: wiadoomość z błędami wiązkowymi
    """
    list_of_allowed_indexes = list(range(start_index, end_index + 1))
    encoded_message = list(encoded_message)
    for i in range(numbers_of_erros):
        index = random.choice(list_of_allowed_indexes)
        forbiden_number = encoded_message[index]
        encoded_message[index] = random_number(forbiden_number)
        list_of_allowed_indexes.remove(index)
    return encoded_message

def test_of_simple_decoder(message, numbers_of_erros, neighbourhood, number_of_test):
    encoded_message = encode_test(message)
    print(encoded_message)
    number_of_failrules = 0
    number_of_undecodable = 0  #o ile istnieje to slowo xd
    for i in range(number_of_test):
        harmed_message = get_random_error(encoded_message, numbers_of_erros, neighbourhood)
        decoded_message = simple_decode_test(harmed_message)
        if decoded_message != encoded_message:
            if decoded_message == None:
                number_of_undecodable += 1
            else:
                number_of_failrules += 1

            #print(harmed_message)
            #print(decoded_message)
            #print("")
    return number_of_failrules, number_of_undecodable

def test_with_bundle_errors(encoded_message, numbers_of_erros, distance_between_errors, number_of_test):
    number_of_failrules = 0
    number_of_undecodable = 0  #oile istnieje to slowo xd
    reed_solomon = ReedSolomon(31, 11)
    for i in range(number_of_test):
        start_index = random.randint(0, len(encoded_message) - distance_between_errors - 1)
        end_index = start_index + distance_between_errors
        harmed_message = get_bundle_error(encoded_message, numbers_of_erros, start_index, end_index)
        decoded_message = reed_solomon.berlekamp_welch_decode(harmed_message)
        #print(decoded_message)
        if decoded_message != encoded_message:
            if decoded_message == None:
                number_of_undecodable += 1
            else:
                number_of_failrules += 1

            #print(harmed_message)
            #print(decoded_message)
            #print("")
    return number_of_failrules, number_of_undecodable

def generate_random_message(message_length):
    return [(randint(0, 31)) for i in range(message_length)]

#-----------TESTY--------------------------------------------------------

Num_of_errors = [1,2,3,4,5,6,7,8,9,10,11,12,20,25]
num_of_tests = 1000
Percent_of_corrected = []
message = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
reed_solomon = ReedSolomon(31,11)
encoded_message = reed_solomon.encode_as_evaluations(message)
total_number_of_failrules = 0
total_number_of_undecodable = 0


for i in range(num_of_tests):
    encoded_message = reed_solomon.encode_as_evaluations(generate_random_message(11))
    num_of_f, num_of_und  = test_with_bundle_errors(encoded_message, 10, 10+3, 1)
    total_number_of_failrules += num_of_f
    total_number_of_undecodable += num_of_und

print("Found but not corrected: ",total_number_of_undecodable)
print("Corrected but wrong: ",total_number_of_failrules)
# for num in Num_of_errors:
#     message = generate_random_message(num)
#     encoded_message = reed_solomon.encode_as_evaluations(message)
#     num_of_f, num_of_und  = test_with_bundle_errors(encoded_message, num, num+3, num_of_tests)
#     Percent_of_corrected.append((num_of_tests - num_of_f - num_of_und)/num_of_tests)
#
# plt.title("BERLEKAMP-WELCH DECODER")
# plt.xlabel("Number of errors")
# plt.ylabel("Percent of corrected")
# plt.plot(Num_of_errors, 100*np.array(Percent_of_corrected),color = 'blue')
# plt.scatter(Num_of_errors, 100*np.array(Percent_of_corrected), color = 'blue')
# plt.grid(True)
# plt.show()

print(Percent_of_corrected)
print(Num_of_errors)

