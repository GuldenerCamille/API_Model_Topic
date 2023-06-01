import gensim
from gensim import corpora, models
import re
import heapq


physics_keywords = ["galaxy","mass","star","planet","stellar","gas",
                    "formation", "magnetic","time","light","temperature","energy","black hole","space",
                    "theory","structure","weight","quantum","system","structure","property","star",
                    "observation","cluster","effect","stat","earth","cosmology","astrophysic","theory","electrons",
                    "science","fluid","dynamic","methods","science","source","methodology"]
computer_science_keywords = [
    "Artificial intelligence", "Machine learning", "Data Science", "Big Data", "Cloud Computing",
    "Cybersecurity", "Information security", "Network security", "Blockchain", "Cryptocurrency",
    "Internet of things", "IoT", "Web development", "Mobile development", "Frontend development",
    "Backend development", "Software engineering", "Software development", "Programming",
    "Database", "Data analytics", "DevOps", "IT consulting", "IT service management",
    "ERP", "CRM", "SaaS", "PaaS", "IaaS", "Virtualization", "Artificial reality", "AR", "Virtual reality",
    "VR", "Gaming", "E-commerce", "Digital marketing", "SEO", "SEM",
    "Social media marketing", "User experience", "UX design", "UI design", "Cloud-native",
    "Microservices", "Serverless", "Containerization", "data","network","prediction","computer vision","language",
    "system","control","performance"]
mathematics_keywords = ["trigonometry","geometry","algebra","abstract","reciprocity","fondamental","commutative","linear","complex",
                        "equation","coefficient","function","expression","variable","line","angle","circle","quadrilateral","perimeter","derivative",
                       "integral","limit","addition","substraction","solution","multiplication","division","absolute value","algorithm",
                       "array","base","binomial","cone","congruent","denominator","difference","ellipse","hyperbola","integer",
                       "inequality","irrational","logarithm","slope","translation"]
statistics_keywords = ["variable","Maximum","minimum","growth","decay","series","central limit theorem","univariate",
                       "bivariate","probability","conditional","mean","mode","median","random","variance","distribution",
                      "interval","hypothesis","test","significance","statistic","continuity","categorical","proof","calculus",
                      "confidence","anamysis","bias","expectation","discrete","dependence","independence","matrice","event"]

industries = {
    "Mathematics" : mathematics_keywords,
    "Statistics" : statistics_keywords,
    "Computer science" : computer_science_keywords,
    "Physics" : physics_keywords
}





# fonction permettant de classer larticle dans le topic correspondant
def label_topic(text):
    counts = {}
    for industry, keywords in industries.items():
        count = sum([1 for keyword in keywords if re.search(r"\b{}\b".format(keyword), text, re.IGNORECASE)])
        counts[industry] = count
        top_industries = heapq.nlargest(2, counts, key=counts.get)
    if len(top_industries) == 1:
        return top_industries[0]
    else:
        return top_industries
    ############

# fonction de preprocessing
def preprocess_text(text):
    tokens = gensim.utils.simple_preprocess(text)
    stop_words = gensim.parsing.preprocessing.STOPWORDS
    preprocessed_text = [[token for token in tokens if token not in stop_words]]
    return preprocessed_text

#fonction de modelisation
def perform_topic_modeling(transcript_text, num_topics=5, num_words=10):
    """
    This function perfoms topic modeling on a given text.
    """
    preprocessed_text = preprocess_text(transcript_text)
    dictionary = corpora.Dictionary(preprocessed_text)
    corpus = [dictionary.doc2bow(text) for text in preprocessed_text]
    lda_model = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)

    # extraire les mots les plus courants pour chacun des topic

    topics = []
    for idx,topic in lda_model.print_topics(-1,num_words=num_words):
        topic_words = [word.split('*')[1].replace('"','').strip() for word in topic.split('+')]
        topics.append((f"Topic {idx}", topic_words))

    return topics
