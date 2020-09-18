import re

# Class class for a single class (or column)
class actual_class:
    def __init__(self, name, accuracy, attribute_names):
        self.name = name
        self.attribute_names = attribute_names
        self.attribute_list = []
        self.accuracy = accuracy


# Attribute class for a single attribute
class attribute:
    def __init__(self, name, count, yes, no):
        self.name = name
        self.count = count
        self.yes = yes
        self.no = no


# OneR function. It extracts data  from the file and performs the calculations
def oneR(file_name):
    with open(file_name, 'r') as input_file: # read the file
        line = input_file.readline()
        classes = []
        data_arr = []
        flag = ''

        while line:
            line = input_file.readline()
            # get the values for each class
            if line.partition(' ')[0] == '@attribute':
                string1 = ((' '.join(line.split()[2:])).strip('{}')).replace(',', ' ')
                separate_str = string1.split()
                classes.append(actual_class(line.split()[1], '', separate_str))
            # get the data
            if flag == '@data':
                string2 = (line.replace(',', ' ')).strip('\n')
                data_arr.append(string2)
            if line.startswith('@data'):
                flag = '@data'

        input_file.close()  # close the file

        # For each class attributes will be stored
        # with their names, actual count, yes count, and no count
        col_idx = 0
        data_arr = list(filter(None, data_arr))
        attr_count = len(data_arr)
        br_total = 0
        br_results = []

        for cls in classes:
            attr_hash = []
            attr_list = []

            for row in data_arr:
                attr_names = list(row.split('\n'))
                number_classes = len(row.split())  # number of classes (columns)
                if attr_names[0].split()[col_idx] in cls.attribute_names:
                    if attr_names[0].split()[col_idx] not in attr_hash:
                        attr_hash.append(attr_names[0].split()[col_idx])
                        # create new attribute and adjust its values
                        new_attr = attribute('', 0, 0, 0)  # new attribute
                        new_attr.name = attr_names[0].split()[col_idx]  # name
                        new_attr.count += 1  # count
                        # below is the yes or no value
                        if attr_names[0].split()[len(attr_names[0].split()) - 1].lower() == 'yes':
                            new_attr.yes += 1
                        if attr_names[0].split()[len(attr_names[0].split()) - 1].lower() == 'no':
                            new_attr.no += 1
                        attr_list.append(new_attr)  # add the new attribute to the list with the values
                    else:  # otherwise find its index in the hash list
                        index = attr_hash.index(attr_names[0].split()[col_idx])
                        # increment the values of the attribute
                        attr_list[index].count += 1
                        if attr_names[0].split()[len(attr_names[0].split()) - 1].lower() == 'yes':
                            attr_list[index].yes += 1
                        if attr_names[0].split()[len(attr_names[0].split()) - 1].lower() == 'no':
                            attr_list[index].no += 1
            col_idx += 1

            # class calculating
            yn_total = 0
            tuples = []

            for a in attr_list:
                majority = 0
                if a.yes > a.no:
                    majority = a.yes
                    outcome = 'Yes'
                else:
                    majority = a.no
                    outcome = 'No'

                yn_total += majority
                accuracy = yn_total / attr_count

                tuples.append((a.name + ':  Count: ' + str(a.count) + ' Yes: ' + str(a.yes) + ' No: '
                               + str(a.no) + ' ---> ' + str(outcome)))

            if yn_total > br_total:
                br_class = cls.name
                br_total = yn_total
                br_error = attr_count - yn_total
                br_count = attr_count
                br_results = tuples

            if col_idx == len(attr_names[0].split()) - 1:
                break

        # print results
        print(number_classes, 'attributes')
        print(attr_count, 'examples')
        print('File name: ', file_name)
        print('\nBest oneR rule:')
        print(br_class)
        for r in br_results:
            print('\t', r)
        print('Correctly classified: ', br_total)
        print('Error rate: ', br_error, '/', br_count)


# main function: prompts for file name and calls oneR function
def main():
    user_input = input('Enter the name of the file: ')
    oneR(user_input)


if __name__ == "__main__":
    main()
