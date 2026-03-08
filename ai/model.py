from sklearn.ensemble import RandomForestClassifier

class MarketAI:

    def __init__(self):

        self.model = RandomForestClassifier(
            n_estimators=600,
            max_depth=14
        )

    def train(self,X,y):

        self.model.fit(X,y)

    def predict(self,X):

        return self.model.predict_proba(X)
