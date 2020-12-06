from data import Dataset
from data import Evaluator

# Ignore 'future warnings' from the toolkit.
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

# sklearn tools
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

# Global Variables #
# Logistic regression Classifier #
# vectorizer = CountVectorizer(strip_accents='ascii'analyzer='word', min_df=1, ngram_range=(1,3))
logit = LogisticRegression(solver="saga", max_iter=100)
vectorizer = TfidfVectorizer(strip_accents='ascii',analyzer='word',
        stop_words='english', ngram_range=(1,3), min_df=4)

# List of illegal characters #
illegal = ['(', ')', '{', '}', '[', ']', ' - ', '?', '!', '.', ';', ':']


'''
Given a string, this method processes it and returns it "clean"
lyric: (str) the string to be processed
Returns: a string with no bad input
'''
def preProcess(lyric):
    for x in illegal:
        lyric = lyric.lower()
        lyric = lyric.replace(x, '')

    lyric = lyric.replace("doesn't", "does not")
    lyric = lyric.replace("can't", "cannot")
    lyric = lyric.replace("i'm", "i am")
    lyric = lyric.replace("there's", "there is")
    lyric = lyric.replace("that's", "that is")
    return lyric

'''
Given a list of song titles and their known genre, train logistic regression classifier.
trainset: a list of triples, where each triple is (genre, author, song's lyric) 
Returns: void
'''
def train(trainset) :
    
    # Y_train -> List of genres for each song
    # X_train -> List of song's lyrics
    Y_train = []
    X_train = []

    # fill lists #
    for triple in trainset :
        Y_train.append(triple[0])
        X_train.append( preProcess(triple[2]) )
    
    # Create Matrix #
    X_train_counts = vectorizer.fit_transform(X_train)

    # Train #
    logit.fit(X_train_counts, Y_train)


'''
Given a list of song titles and their genres, predict the
genre for each song title.
testset: a List of triples, where each triple is (genre, artist, song's lyric)
Returns: a list of genre names, which are the classifier's prediction for each given song title.
'''
def test(testset):
    
    # X_test -> list of song's lyrics #
    X_test = []

    # Fill List #
    for triple in testset:
        X_test.append( preProcess(triple[2]) )

    # Transform Unseen Text #
    X_test_counts = vectorizer.transform(X_test)

    # Get Predictions #
    guesses = logit.predict(X_test_counts)
    return guesses


'''
Below is the main
'''
if __name__ == "__main__":
    # Create trainset and testset #
    dt = Dataset()
    trainset = dt.getTrainingSet()
    testset  = dt.getTestingSet()
    
    # Train Logistic Regression Classifier #
    train(trainset)

    # Test Logistic Regression Classifier #
    predicted_labels = test(testset)

    # Evaluate #
    evaluator = Evaluator()
    accuracy = evaluator.evaluateLabels(predicted_labels, testset)
    print('Accuracy: %.2f%%\n' % (accuracy))
