import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

nltk.download('wordnet')
nltk.download('stopwords')
stopwords_set = set(stopwords.words('english'))

with open(r"C:\Users\Sai Prabhas\OneDrive\Desktop\Mini_project\False_News_Detection\trained\logistic_regression.pkl", 'rb') as model_file:
    model_lr = pickle.load(model_file)

with open(r"C:\Users\Sai Prabhas\OneDrive\Desktop\Mini_project\False_News_Detection\trained\random_forest.pkl", 'rb') as model_rf_file:
    model_rf = pickle.load(model_rf_file)

with open(r"C:\Users\Sai Prabhas\OneDrive\Desktop\Mini_project\False_News_Detection\trained\tfidf_vectorizer_rf.pkl", 'rb') as tfidf_file:
    tfidf_vectorizer = pickle.load(tfidf_file)


#WASHINGTON (Reuters) - The head of a conservative Republican faction in the U.S. Congress, who voted this month for a huge expansion of the national debt to pay for tax cuts, called himself a “fiscal conservative” on Sunday and urged budget restraint in 2018. In keeping with a sharp pivot under way among Republicans, U.S. Representative Mark Meadows, speaking on CBS’ “Face the Nation,” drew a hard line on federal spending, which lawmakers are bracing to do battle over in January. When they return from the holidays on Wednesday, lawmakers will begin trying to pass a federal budget in a fight likely to be linked to other issues, such as immigration policy, even as the November congressional election campaigns approach in which Republicans will seek to keep control of Congress. President Donald Trump and his Republicans want a big budget increase in military spending, while Democrats also want proportional increases for non-defense “discretionary” spending on programs that support education, scientific research, infrastructure, public health and environmental protection. “The (Trump) administration has already been willing to say: ‘We’re going to increase non-defense discretionary spending ... by about 7 percent,’” Meadows, chairman of the small but influential House Freedom Caucus, said on the program. “Now, Democrats are saying that’s not enough, we need to give the government a pay raise of 10 to 11 percent. For a fiscal conservative, I don’t see where the rationale is. ... Eventually you run out of other people’s money,” he said. Meadows was among Republicans who voted in late December for their party’s debt-financed tax overhaul, which is expected to balloon the federal budget deficit and add about $1.5 trillion over 10 years to the $20 trillion national debt. “It’s interesting to hear Mark talk about fiscal responsibility,” Democratic U.S. Representative Joseph Crowley said on CBS. Crowley said the Republican tax bill would require the  United States to borrow $1.5 trillion, to be paid off by future generations, to finance tax cuts for corporations and the rich. “This is one of the least ... fiscally responsible bills we’ve ever seen passed in the history of the House of Representatives. I think we’re going to be paying for this for many, many years to come,” Crowley said. Republicans insist the tax package, the biggest U.S. tax overhaul in more than 30 years,  will boost the economy and job growth. House Speaker Paul Ryan, who also supported the tax bill, recently went further than Meadows, making clear in a radio interview that welfare or “entitlement reform,” as the party often calls it, would be a top Republican priority in 2018. In Republican parlance, “entitlement” programs mean food stamps, housing assistance, Medicare and Medicaid health insurance for the elderly, poor and disabled, as well as other programs created by Washington to assist the needy. Democrats seized on Ryan’s early December remarks, saying they showed Republicans would try to pay for their tax overhaul by seeking spending cuts for social programs. But the goals of House Republicans may have to take a back seat to the Senate, where the votes of some Democrats will be needed to approve a budget and prevent a government shutdown. Democrats will use their leverage in the Senate, which Republicans narrowly control, to defend both discretionary non-defense programs and social spending, while tackling the issue of the “Dreamers,” people brought illegally to the country as children. Trump in September put a March 2018 expiration date on the Deferred Action for Childhood Arrivals, or DACA, program, which protects the young immigrants from deportation and provides them with work permits. The president has said in recent Twitter messages he wants funding for his proposed Mexican border wall and other immigration law changes in exchange for agreeing to help the Dreamers. Representative Debbie Dingell told CBS she did not favor linking that issue to other policy objectives, such as wall funding. “We need to do DACA clean,” she said.  On Wednesday, Trump aides will meet with congressional leaders to discuss those issues. That will be followed by a weekend of strategy sessions for Trump and Republican leaders on Jan. 6 and 7, the White House said. Trump was also scheduled to meet on Sunday with Florida Republican Governor Rick Scott, who wants more emergency aid. The House has passed an $81 billion aid package after hurricanes in Florida, Texas and Puerto Rico, and wildfires in California. The package far exceeded the $44 billion requested by the Trump administration. The Senate has not yet voted on the aid. 
class Preprocessing:
    def __init__(self, data):
        self.data = data
        
    def text_preprocessing_user(self):
        lm = WordNetLemmatizer()
        pred_data = [self.data]    
        preprocess_data = []
        for data in pred_data:
            review = re.sub('[^a-zA-Z0-9]', ' ', data)
            review = review.lower()
            review = review.split()
            review = [lm.lemmatize(x) for x in review if x not in stopwords_set]
            review = " ".join(review)
            preprocess_data.append(review)
        return preprocess_data

def predict_news_log(news_text):
    preprocess_data = Preprocessing(news_text).text_preprocessing_user()
    data = tfidf_vectorizer.transform(preprocess_data)
    prediction = model_lr.predict(data)
    return "The News Is Fake" if prediction[0] == 0 else "The News Is Real"

def predict_news_rf(news_text):
    preprocess_data = Preprocessing(news_text).text_preprocessing_user()
    data = tfidf_vectorizer.transform(preprocess_data)
    prediction = model_rf.predict(data)
    return "The News Is Fake" if prediction[0] == 0 else "The News Is Real"

def main():
    st.title('False News Detection App')

    model_choice = st.radio("Select Model:", ('Random Forest', 'Logistic Regression'))

    news_text = st.text_area('Enter the news text:', '')

    if st.button('Predict'):
        if not news_text.strip():
            st.error("Please enter some text to predict.")
        else:
            if model_choice == 'Random Forest':
                result = predict_news_rf(news_text)
            else:
                result = predict_news_log(news_text)
            st.success(result)

if __name__ == '__main__':
    main()