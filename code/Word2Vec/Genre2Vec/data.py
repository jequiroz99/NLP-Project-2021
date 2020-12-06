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
        self.trainingData['rock'] = ['deep purple', 'smashing pumpkins', 
        'pink floyd', 'alice in chains', 'kiss', 'the beatles', 'the cure', 
        'system of a down', 'lynyrd skynyrd', 'the strokes', 'u2', 'queen', 
        'arctic monkeys', 'korn', 'red hot chili peppers', 'metallica', 
        'foo fighters', 'aerosmith']

        # specify Pop training data #
        self.trainingData['pop'] = ['nicki minaj', 'demi lovato', 'jason derulo', 
        'katy perry', 'glee', 'britney spears', 'maroon 5', 'selena gomez', 
        'nick jonas', 'ellie goulding', 'mariah carey', 'jackson 5', 
        'michael jackson', 'adele', 'justin bieber', 'kesha']

        # specify Hip Hop training data #
        self.trainingData['hip hop'] = ['sean paul', 'mac miller', 
        'black eyed peas', 'drake', 'usher', 'tyga', '2 chainz', 'beastie boys', 
        'kevin gates', 'gucci mane', 'ice cube', 'meek mill', 'kanye west', 
        'kid cudi', 'eminem', 'iggy azalea']
        
        # specify Rock test data #
        self.testingData['rock'] = ['scorpions', 'van halen', 
        'thirty seconds to mars', 'john lennon', 'jimi hendrix', 'ozzy osbourne', 
        'papa roach', 'black sabbath', 'bon jovi', 'led zeppelin']

        # specify Pop test data #
        self.testingData['pop'] = ['george michael', 'lady gaga', 'madonna', 
        'rihanna', 'cher']

        # specify Hip Hop test data #
        self.testingData['hip hop'] = ['wiz khalifa', 'flo rida', 'fergie', 
        '50 cent']

    
    
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
            
            songs = ""
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
            
            # store all songs in genre in dataset #
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
        
        # For Hip Hop training, save only Chris Brown's first 510 songs #
        fp = open('../../../data/hip hop/chris brown.csv', 'r', newline='')
        songs = csv.reader(fp, delimiter=',')
        for x in range(510):
          song = next(songs)
          dataset.append(('hip hop', 'chris brown', song[1]))
        
        # return training set #
        return dataset

    def getTestingSet(self) :
        '''
        returns a list of triples, where each triple is
        (genre, author, song's lyrics)
        '''
        # get Testing Data #
        dataset = self.getDataSet("test")
        
        # For Hip Hop testing, save only Chris Brown's last 664 songs #
        cb = open('../../../data/hip hop/chris brown.csv', 'r', newline='')
        songs = csv.reader(cb, delimiter=',')
        count = 0
        for row in songs :
          if count > 510 :
            dataset.append(('hip hop', 'chris brown', row[1]))
          count += 1
        
        # return test set #
        return dataset


'''
This class instance will be able to evaluate
a set of genre guesses with a set of the correct
genres and output the accuracy percent.
It has methods for our logistic regression
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
            fp.write(guess+"\t"+gold_guess[0]+"\t"+
            gold_guess[1]+"\n")
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

   
