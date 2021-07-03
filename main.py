from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List
import yake


# Input with string field, e.g. {"text":"blah blah"}
class Paragraph(BaseModel):
    text: str

    class Config:
        schema_extra = {
            "example": {
                "text": "Logistic regression is a statistical model that in its basic form uses a logistic function to model a binary dependent variable, although many more complex extensions exist. In regression analysis, logistic regression[1] (or logit regression) is estimating the parameters of a logistic model (a form of binary regression). Mathematically, a binary logistic model has a dependent variable with two possible values, such as pass/fail which is represented by an indicator variable, where the two values are labeled 0 and 1. In the logistic model, the log-odds (the logarithm of the odds) for the value labeled 1 is a linear combination of one or more independent variables (predictors); the independent variables can each be a binary variable (two classes, coded by an indicator variable) or a continuous variable (any real value). The corresponding probability of the value labeled 1 can vary between 0 (certainly the value 0) and 1 (certainly the value 1), hence the labeling; the function that converts log-odds to probability is the logistic function, hence the name. The unit of measurement for the log-odds scale is called a logit, from logistic unit, hence the alternative names. Analogous models with a different sigmoid function instead of the logistic function can also be used, such as the probit model; the defining characteristic of the logistic model is that increasing one of the independent variables multiplicatively scales the odds of the given outcome at a constant rate, with each independent variable having its own parameter; for a binary dependent variable this generalizes the odds ratio.",
            }
        }


# Output with list of string, e.g. {"keywords":["a", "b"]}
class Response(BaseModel):
    keywords: List[str]

    class Config:
        schema_extra = {
            "example": {
                "keywords": """["logistic model","variable","regression","binary dependent","labeled"]""",
            }
        }


app = FastAPI()

# Our simple model
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


# endpoint
@app.post("/keywords", response_model=Response)
def keywords(
    p: Paragraph = Body(
        default={
            "normal": {
                "summary": "A normal example",
                "description": "Just a normal example",
                "value": {"keywords": ["logistic model", "variable", "regression"]},
            },
        },
    )
):
    kw = ExtractKeywords(p.text)
    return Response(keywords=kw)
