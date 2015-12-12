__author__ = 'aliselmanaydin'



class NaiveBayes:
    def __init__(self,training_data,testing_data):

        self.training_data = training_data
        self.testing_data = testing_data





    def train(self):
        num_samples = len(self.training_data)
        num_classes = 10
        probability_distributions = dict()
        sample_counts = dict()
        for i in range(num_classes):
            probability_distributions[i] = [784*[0],784*[0],784*[0]];
            sample_counts[i] = 0;


        cnt = 0;

        for sample in self.training_data:
            #counts = [0,0,0];
            #current_dist = probability_distributions[sample.label]
            cnt += 1
            if cnt % 100 == 0:
                print cnt

            sample_counts[sample.label] += 1
            for j in range(len(sample.data)):
                #print sample.data[j],j

                probability_distributions[sample.label][sample.data[j]][j] += 1


        # smoothing etc
        for i in range(10):
            for j in range(len(sample.data)):
                for k in range(3):
                    probability_distributions[i][k][j] = (probability_distributions[i][k][j] + 1.0)/(sample_counts[i]+ 11)

        self.probability_distributions = probability_distributions

        sm = float(sum(sample_counts.values()));

        for i in range(len(sample_counts)):
            sample_counts[i] = sample_counts[i] / sm;

        self.sample_counts = sample_counts


    def test(self):
        correct = 0;

        #statistics = {}

        predictions = {}


        for i in range(len(self.testing_data)):
            probabilities = 10*[0.0]
            for label in range(10):
                multiplication = 1.0;
                for feature in range(len(self.testing_data[i].data)):
                    multiplication = multiplication * self.probability_distributions[label][self.testing_data[i].data[feature]][feature]

                multiplication *= self.sample_counts[label]
                probabilities[label] = multiplication

            max_idx = probabilities.index(max(probabilities))
            actual = self.testing_data[i].label

            predictions[i] = (max_idx,actual)

            if max_idx == actual:
                correct += 1


            if i % 100 == 0:
                print i
            #print "actual %d"%(self.testing_data[i].label)
            #print "predicted %d"%(max_idx)

        #return float(correct)/len(self.testing_data)
        return predictions




