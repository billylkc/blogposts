from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import yake


# Input
class Paragraph(BaseModel):
    text: str


# Output
class Response(BaseModel):
    keywords: List[str]


app = FastAPI()


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


@app.post("/keywords", response_model=Response)
def keywords_two(p: Paragraph):
    kw = ExtractKeywords(p.text)
    return Response(keywords=kw)
