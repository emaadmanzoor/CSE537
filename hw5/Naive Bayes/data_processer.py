__author__ = 'aliselmanaydin'


from digit import Digit

class DatasetParser:
    def __init__(self,data_dir,labels_dir):
        self.data_dir = data_dir
        self.labels_dir = labels_dir



    def read(self):
        f_data = open(self.data_dir,"r")
        f_labels = open(self.labels_dir,"r")

        raw_data = f_data.read()
        raw_labels = f_labels.read()

        labels = raw_labels.split("\n")
        raw_data_lines = raw_data.split("\n")
        del labels[-1]


        digits = []

        for i in range(len(labels)):
            train_digit = raw_data_lines[i*28:(i+1)*28]
            train_digit_array = [];
            for line in train_digit:
                digit_integers = [0] * len(line)

                chars = list(line)

                for j in range(len(chars)):
                    if chars[j] == " ":
                        digit_integers[j] = 0
                    elif chars[j] == "+":
                        digit_integers[j] = 1
                    else:
                        digit_integers[j] = 2

                train_digit_array.extend(digit_integers)
            #print labels[i]
            digits.append(Digit(train_digit_array,int(labels[i])))

        f_data.close()
        f_labels.close()
        return digits



