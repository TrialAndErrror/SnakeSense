# SnakeSense

SnakeSense is a sentiment analysis prototype built on SpaCy and TextBlob to enable quick sorting and processing of text reviews.

Goal of project: Identify the best places for Fried Chicken in Northwest Arkansas.
 
Best rated means:
* Category A) Highest % of positive reviews that mention fried chicken
* Category B) Highest average polarity of positive reviews that mention fried chicken
* Category C) Highest ratio of positive to negative reviews across all reviews with a minimum of 0.5 polarity

Results of top 3 in each category to be amended to this readme.

Setup:
* python -m textblob.download_corpora
* python -m spacy download en_core_web_sm

Documentation:
* SpaCy Docs: https://spacy.io/
* SpaCy TextBlob: https://spacy.io/universe/project/spacy-textblob
* Learn about TextBlob: https://textblob.readthedocs.io/en/dev/
* Yelp API: https://github.com/gfairchild/yelpapi

Link to Movie Dataset: https://ai.stanford.edu/~amaas/data/sentiment/

Notes:

* Polarity: {doc._.blob.polarity}
    * Polarity measures whether the expressed opinion is positive (1.0), negative (-1.0), or neutral.
* Subjectivity: {doc._.blob.subjectivity}
    * Subjectivity measures how objective (0.0) or subjective (1.0) a statement is.
* Assessments: {doc._.blob.sentiment_assessments.assessments}


[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/TrialAndErrror/SnakeSense)
