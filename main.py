from flask import Flask, request
import yake

app = Flask(__name__)


def ExtractKeywords(text):
    """ Extract 20 keywords from the input text """

    language = "en"
    max_ngram_size = 2
    deduplication_thresold = 0.3
    deduplication_algo = "seqm"
    windowSize = 1
    numOfKeywords = 20

    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_thresold,
        dedupFunc=deduplication_algo,
        windowsSize=windowSize,
        top=numOfKeywords,
        features=None,
    )
    kws = custom_kw_extractor.extract_keywords(text)
    keywords = [x[0] for x in kws]  # kws is in tuple format, extract the text part

    return keywords


@app.route("/keywords", methods=["POST", "GET"])
def keywords():
    if request.method == "POST":
        json_data = request.json
        text = json_data["text"]
        kws = ExtractKeywords(text)

        # return a dictionary
        response = {"keyowrds": kws}
        return response

    elif request.method == "GET":
        response = """
        Extract 20 keywords from a long text. Try with curl command. <br/><br/>

        curl -X POST http://127.0.0.1:2005/keywords -H 'Content-Type: application/json' \
        -d '{"text": "Logistic regression is a statistical model that in its basic form uses a logistic function to model a binary dependent variable, although many more complex extensions exist. In regression analysis, logistic regression[1] (or logit regression) is estimating the parameters of a logistic model (a form of binary regression). Mathematically, a binary logistic model has a dependent variable with two possible values, such as pass/fail which is represented by an indicator variable, where the two values are labeled 0 and 1. In the logistic model, the log-odds (the logarithm of the odds) for the value labeled 1 is a linear combination of one or more independent variables (predictors); the independent variables can each be a binary variable (two classes, coded by an indicator variable) or a continuous variable (any real value). The corresponding probability of the value labeled 1 can vary between 0 (certainly the value 0) and 1 (certainly the value 1), hence the labeling; the function that converts log-odds to probability is the logistic function, hence the name. The unit of measurement for the log-odds scale is called a logit, from logistic unit, hence the alternative names. Analogous models with a different sigmoid function instead of the logistic function can also be used, such as the probit model; the defining characteristic of the logistic model is that increasing one of the independent variables multiplicatively scales the odds of the given outcome at a constant rate, with each independent variable having its own parameter; for a binary dependent variable this generalizes the odds ratio."}'
        """
        return response

    else:
        return "Not supported"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2005, debug=True)
