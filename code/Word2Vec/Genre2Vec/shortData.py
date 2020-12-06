'''
Python script that given a
fixed number of training songs
and testing songs for each genre, 
and also specific artists to 
train and test with, will 
produce datasets
'''

import pathlib
import csv

'''
This class instance will create a training
and testing dataset from the 'data' folder
in github
'''
class Dataset :
    
    # constructor for defining class variables #
    def __init__(self) :
        
        # these 2 dict map genres to a list of 
        # artists for  #
        self.trainingData = dict()
        self.testingData = dict()
        
        # specify Rock training data #
        self.trainingData['rock'] = [ 'pink floyd', 'alice in chains', 
        'kiss', 'the beatles', 'eric clapton', 
        'red hot chili peppers', 'metallica', 'foo fighters', 
        'aerosmith']

        # specify Pop training data #
        self.trainingData['pop'] = ['nicki minaj', 'madonna', 
        'lady gaga', 'katy perry', 'glee']

        # specify Hip Hop training data #
        self.trainingData['hip hop'] = ['sean paul', 'mac miller', 
        'drake', 'eminem', 'iggy azalea', 'chris brown', '2 chainz']
        
        # specify Rock test data #
        self.testingData['rock'] = ['arctic monkeys', 'jimi hendrix', 
        'john lennon', 'led zeppelin']

        # specify Pop test data #
        self.testingData['pop'] = ['george michael', 'jason derulo',
        'michael jackson']

        # specify Hip Hop test data #
        self.testingData['hip hop'] = ['kanye west', 'meek mill', 
        'gucci mane', 'tyga']

    def getDataSet(self, tag) :
        '''
        returns a list of triples, where each triple is
        (genre, author, song's lyrics)
        '''
        dataset = list()
        data = None
        if tag == "train" :
          data = self.trainingData
        else :
          data = self.testingData

        for genre in ['rock', 'pop', 'hip hop'] :
            # get list of artists #
            artists = data[genre]
            songs ="" 
            for artist in artists :
                
                # open each artist's file #
                fname = '../../../data/'+genre+'/'+artist+'.csv'
                fp = open(fname, 'r', newline='')
                reader = csv.reader( fp, delimiter=',')

                # store song's lyrics #
                for song in reader :
                  songs += song[1]

                # close file #
                fp.close()
            # add all genre lyrics to dataset #
            dataset.append((genre, artist, songs))
        
        # return the list #
        return dataset

    def getTrainingSet(self) :
        ''' 
        returns a list of triples where each triple is 
        (genre, author, song's lyrics)
        '''
        # get Training Data
        dataset = self.getDataSet("train")
        
        # return training set #
        return dataset

    def getTestingSet(self) :
        '''
        returns a list of triples, where each triple is
        (genre, author, song's lyrics)
        '''
        # get Testing Data #
        dataset = self.getDataSet("test")
        
        # return test set #
        return dataset
   
    

'''
This class instance will be able to evaluate
a set of genre guesses with a set of the correct
genres and output the accuracy percent.
It has methods for our logustic regression
classifier and for our word2Vec model
'''
class Evaluator :
    
    
    def evaluateLabels(self, my_guesses, gold_guesses):
        # Sanity Check (should never print error) #
        if len(my_guesses) != len(gold_guesses):
          print("ERROR IN EVALUATE: you gave me ", len(my_guesses), " guessed labels, but there are ", len(gold_guesses)," genres.")
          return 0.0

        # Compare my guesses with the gold labels #
        # Save wrong prediction in wrong.txt #
        fp = open('wrong.txt', 'w')
        numRight = 0
        numWrong = 0
        xx = 0;
        for guess in my_guesses:
          gold_guess = gold_guesses[xx]
          if guess == gold_guess[0]:
            numRight += 1
          else:
            numWrong += 1
            fp.write(guess+"\t"+gold_guess[1]+"\n")
          xx += 1

        # Compute accuracy.
        print("Correct:   " + str(numRight))
        print("Incorrect: " + str(numWrong))
        accuracy = numRight / (numRight+numWrong)
        return accuracy * 100.0

    
    def evaluateVectors(self, scores, testset, trainset):
        fp = open('badVectors.txt', 'w')
        numRight = 0
        numWrong = 0
        xx = 0;
        for index, set_of_scores in enumerate(scores):

            # Sort List #
            set_of_scores.sort(reverse=True, key=lambda x:x[0])

            # Compare my guesses with the gold labels #
            # I'll use only my top score #
            
            # get the index stored for the top score #
            top_index = set_of_scores[0][1]
            my_guess = trainset[top_index][0]
            gold_guess = testset[index][0]
            if  my_guess == gold_guess:
                numRight += 1
            else:
                numWrong += 1
            fp.write(my_guess+"\t"+gold_guess+"\n")

        # Compute accuracy.
        print("Correct:   " + str(numRight))
        print("Incorrect: " + str(numWrong))
        accuracy = numRight / (numRight+numWrong)
        return accuracy * 100.0

  
