def extract_location(input_text: str, input_locations: list):
    '''
    returns the list of locations
    args:
        input_text: the string from the data
    '''
    for location in input_locations:
        if '-' in location:
            places = location.split("-")
            if 'between' in input_text:
                temp = input_text.split("between")
                temp = temp[1].strip().split(" ")
                temp = temp[0]+"-" + temp[2]
                return temp
        else:
            if 'between' not in input_text:
                return input_text.split(" ")[-1]


def extract_location_text(input_text: str):
    '''
    returns the list of locations
    args:
        input_text: the string from the data
    '''
    if 'between' in input_text:
        temp = input_text.split("between")
        temp = temp[1].strip().split(" ")
        temp = temp[0]+"-" + temp[2]
        return temp
    else:
        return input_text.split(" ")[-1]
