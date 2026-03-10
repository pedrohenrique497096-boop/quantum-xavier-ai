import pandas as pd
from sklearn.linear_model import LogisticRegression
from database.trades import get_dataset

model=None

def train_model():

    global model

    data=get_dataset()

    if len(data)<10:
        return None

    df=pd.DataFrame(data)

    X=df[["confidence"]]

    y=df["result"]

    model=LogisticRegression()

    model.fit(X,y)

    return model


def predict_success(confidence):

    global model

    if model is None:

        return confidence

    prob=model.predict_proba([[confidence]])[0][1]

    return prob*100
