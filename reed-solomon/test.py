from reedsolomon import ReedSolomon
import random

def encode_test(message):
    reed_solomon = ReedSolomon(31,11)
    return reed_solomon.encode(message)

def simple_decode_test(message):
    reed_solomon = ReedSolomon(31,11)
    return reed_solomon.simple_decode(message)

def random_number(forbiden_number):
    #nie powtarza sie ta sama cyfra wmiejscu, w ktorym była przed uszkodzeniem
    number = forbiden_number
    while number == forbiden_number:
        number = random.randint(-1,30)
        if number == -1:
            number = float('-inf')
    return number

def get_error(encoded_message, numbers_of_erros, neighbourhood):
    message_length = len(encoded_message)
    if neighbourhood:
        #randint bierze ostatni wyraz
        index = random.randint(0, message_length - numbers_of_erros)
        for i in range(index,index + numbers_of_erros):
            encoded_message[i] = random_number(encoded_message[i])
    else:
        # range nie bierze ostatniego wyrazu
        list_of_indexes = list(range(0, message_length))
        for i in range(numbers_of_erros):
            index = random.choice(list_of_indexes)
            encoded_message[index] = random_number(encoded_message[index])
            list_of_indexes.remove(index)
    return encoded_message

def test_of_simple_decoder(message, numbers_of_erros, neighbourhood, number_of_test):
    encoded_message = encode_test(message)
    print(encoded_message)
    number_of_failrules = 0
    number_of_undecodable = 0  #oile istnieje to slowo xd
    for i in range(number_of_test):
        harmed_message = get_error(encoded_message, numbers_of_erros, neighbourhood)
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

num_of_tests = 1000
num_of_f, num_of_und  = test_of_simple_decoder([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 7, False, num_of_tests)
print("Prosty nieodkodowane",num_of_und)
print("Prosty niepoprawnie odkodowane",num_of_f)
print("Prosty poprawnie odkodowane", num_of_tests - num_of_f - num_of_und )
