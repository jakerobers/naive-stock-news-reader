import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import glob

train = glob.glob('train/*.xml')
test = glob.glob('test/*.xml')
train_features = []
train_labels = []
test_features = []
test_labels = []

def parse_xml(tree):
    features = [];
    labels = [];
    
    root = tree.getroot()
    for child in root:
        #print str(child.tag), str(child.attrib)
        if child.tag == 'channel':
            for items in child:
                if items.tag == 'item':
                    content = ''
                    rating = 1
                    for item in items:
                        if item.tag == 'title':
                            content = content + item.text
                        elif item.tag == 'description' and item.text != None:
                            content = content + item.text
                        elif item.tag == 'rating':
                            # 0 = bad, 1 = neutral/irrelevent, 2 = good
                            # content is feature ; rating is label
                            rating = int(item.text)
                    features.append(content)
                    labels.append(rating) 
    return (features, labels)

#training the classifier 
for stock in train:
    f, l = parse_xml(ET.parse(stock))
    train_features += f
    train_labels += l


vec = TfidfVectorizer()
clf = MultinomialNB()
vec.fit(train_features)
train_data = vec.transform(train_features)
clf.fit(train_data, train_labels)

#evaluating the classifier
for stock in test:
    f, l = parse_xml(ET.parse(stock))
    test_features += f
    test_labels += l

test_features = vec.transform(test_features)

#print clf.score(test_features, test_labels)
test_results = clf.predict(test_features)
print test_results
amount_correct = 0;
total = len(test_labels)
for t in test_results:
    for l in test_labels:
        if t == l:
            amount_corrent = amount_correct+1

print amount_correct / total

