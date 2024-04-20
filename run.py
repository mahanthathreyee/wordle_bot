from wordle import words
from wordle import first_guess_ig

if __name__ == "__main__":
    # words.reset_all_data()
    word = first_guess_ig.compute_word_patterns('slate')
    print(word.information_gain)
