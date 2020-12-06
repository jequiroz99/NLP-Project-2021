import math
from data import Dataset
from data import Evaluator

# word 2 vec tools #
import numpy
from gensim.models.word2vec import Word2Vec
from nltk.tokenize import word_tokenize

# Word2Vec global Variables
vSongs = list()
scores = list()

illegal = ['(', ')', '[', ']', '{', '}',',', '"', "'", ' - ', '?', '!', '.', ';',':']

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
    lyric = lyric.replace("wanna", "want to") 
    return lyric


'''
Trains a Word2Vec model to have vector words for each song title
and then fills a Vector for all song titles!!
trainset (list) : list of triples (genre, artist, song lyric)
Return: void 
'''
def train(trainset):
    
    # songs -> List of Lists of Tokens #
    # every song is a list #
    songs = []

    # Fill List #
    for triple in trainset :
        song = []
        lyric = preProcess(triple[2])

        # use NLTK word tokenizer # 
        for token in word_tokenize(lyric) :
            if token.isalpha() :
                song.append(token)
        songs.append(song)
    

    # Create and Train Model #
    embeds = Word2Vec(sentences=songs, size=25)

    # Add Up Every Lyric in songs and Make It a Vector #
    for song in songs:
        
        # Create Vector for the song's lyrics #
        vSong = get_sentence_vector(embeds ,song)
        vSongs.append(vSong)
    
    return embeds

'''
Computes a Score for each song lyrics in testset
and then returns a list of scores for each testset!
testset (list): a list of triples (genre, artist, song's lyric)
'''
def test(embeds, testset):
    
    # Loop over every song in testset #
    for triple in testset :
        
        # list will contain score for each song # 
        song_score = []
        
        # Pre process the song's lyrics #
        lyric = preProcess(triple[2])
        clean_lyrics = []
        for token in word_tokenize(lyric) :
            if token.isalpha() :
                clean_lyrics.append(token)


        # Add up every lyric and Make it a Vector #
        vSong = get_sentence_vector(embeds, clean_lyrics)
        
        ''' Compute Score using Cosine function.
        For each song in the testset, compute a score
        between that song and all songs in trainingset.
        save that score (along with the index, for 
        error checking purposes later) '''
        song_score = []
        for index, vector in enumerate(vSongs):
            # Compute Score #
            score = cosine(vSong, vector)

            if not numpy.isnan(score):
                song_score.append((score, index))
            else :
                song_score.append((0, index))
        scores.append(song_score)


def get_sentence_vector(embeds, words):
    '''
    Returns vector representation of the given list of words
    embeds: contains Twitter-trained embeddings
    words: list of words (strings)
    '''
    v = numpy.zeros(25)
    for word in words:
        if word in embeds:
            vWord = embeds[word]
            v = v + vWord

    return v


def cosine(vA, vB):
    ''' Returns the cosine similarity of two numpy ndarray objects. '''
    upper  = numpy.dot(vA, vB) 
    div = (numpy.sqrt(numpy.dot(vA,vA)) * numpy.sqrt(numpy.dot(vB,vB)))
    if numpy.isnan(upper) or numpy.isnan(div) or div == 0 :
        return 0
    score = upper/div
    return score



'''
Below is the main
'''
if __name__ == "__main__":
    # Create trainset and testset #
    dt = Dataset()
    trainset = dt.getTrainingSet() 
    testset  = dt.getTestingSet()

    # For time purposes (since it takes a lot of
    # time to create the word embeds) just load them from memory
    
    # Call Train to create the vectors #
    embeds = train(trainset)
    
    # Test by Computing Scores #
    test(embeds, testset)

    # Evaluate in a certain way #
    evaluator = Evaluator()
    accuracy = evaluator.evaluateVectors(scores, testset, trainset)
    print('Accuracy: %.2f%%\n' % (accuracy))
