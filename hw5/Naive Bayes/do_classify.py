__author__ = 'aliselmanaydin'

from digit import Digit
from data_processer import DatasetParser
from naive import NaiveBayes
import time

beg = time.time()

parser_train = DatasetParser("trainingimages.txt","traininglabels.txt")
parser_test = DatasetParser("testimages.txt","testlabels.txt")



train_samples = parser_train.read()
test_samples = parser_test.read()

classifier = NaiveBayes(train_samples,test_samples)


print "Training starts..."
classifier.train()

print "Testing starts..."
predictions = classifier.test()

digit_counts = 10*[0]

digit_predicted_counts  = 10*[0]
true_positives = 10*[0]

confusion_matrix = [[0 for x in range(10)] for x in range(10)] ;

for key in predictions:
    (predicted,actual) = predictions[key]
    digit_counts[actual] += 1
    digit_predicted_counts[predicted] += 1
    if actual == predicted:
        true_positives[actual] += 1
    confusion_matrix[actual][predicted] += 1


precisions = 10*[0]
recalls = 10*[0]
f1s = 10*[0]

#confusion_matrix = [[0]*10]*10;
print "\n\n\n"
print "class statistics:"

for i in range(len(digit_counts)):
    precision = float(confusion_matrix[i][i])/sum([x[i] for x in confusion_matrix])
    recall = float(confusion_matrix[i][i])/sum(confusion_matrix[i])
    f1 = 2 * precision * recall / (precision + recall)

    print "For class %d"%(i)
    print "precision: %f"%(precision)
    print "recall %f"%(recall)
    print "F1 score: %f"%(f1)
    print "\n"

    precisions[i] = precision
    recalls[i] = recall
    f1s[i] = f1



print "confusion matrix (rows: actual, columns: predicted)"
print "\n"
print "==============================="

for line in confusion_matrix:
    print line

print "\n\n"
print "Total classification accuracy: %f"%(float(sum([confusion_matrix[i][i] for i in range(10)]))/len(predictions))
print "Average precision: %f"%(sum(precisions)/len(precisions))
print "Average recall: %f"%(sum(recalls)/len(recalls))
print "Average f1s: %f"%(sum(f1s)/len(f1s))

end = time.time()

print "Time elapsed: %f"%(end - beg)

pass

