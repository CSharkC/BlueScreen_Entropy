import math # needed for logs

def get_bin(filename):
    """Takes a filename and reads the binary of the file"""
    # opens the file
    with open(f"{filename}", "rb") as file:
        # reads the binary of the file
        data = file.read()
    # return the binary
    return data

def count(file_array):
    """Takes the binary from the file and counts how many times a character appears"""
    # creates a list of 0s 225 long
    count_list = [0] * 255
    # itterates over the binary data and counts
    # how many times a character appears
    for value in file_array:
        value -= 1
        count_list[value] += 1
    return count_list

def shannon(count_list, file_length):
    """Caluclates the entropy of the file"""
    entropy = 0
    for i_count in count_list:
        if file_length == 0:
            continue
        # calcuates the probality of a character
        prob = i_count / file_length
        # if statement to avoid log error
        if prob > 0:
            # logs the probability
            logprob = math.log(prob, 2)
            # Adds the probability and log of the probability
            # to match the entropy calculation
            entropy += abs(prob * logprob)
        # if probability is 0, there's no reason to add to sum
        else:
            continue
    return entropy

def quick(file_name):
    """Takes a file and returns the entropy of it"""
    # grabs the binary of the file
    data = get_bin(file_name)
    # gets the length of the file for prob calculations
    file_len = len(data)
    # turns the file into a list
    file_array = list(data)
    # list of how many times a character appears
    count_list = count(file_array)
    # calcuating the probability
    return shannon(count_list, file_len)
