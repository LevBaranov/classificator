from sys import stderr
import numpy as np
import elasticsearch 
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import ClassificationDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter, NetworkReader
from pybrain.structure import TanhLayer, SoftmaxLayer, LinearLayer


class ArgumentException(Exception):
    pass

class Classificator:


    data_for_training = []
    
    def learn(self):
        try:
            mem = Memory('http://localhost:9200')
            data = mem.get_data()
            categories = list(data.keys())
            for category in data:
                for req in data[category]:
                    self.data_for_training.append([req.token, [categories.index(category)]])

            net = buildNetwork(
                len(self.data_for_training[0][0]), 
                15, 
                1, 
                hiddenclass=SoftmaxLayer, 
                recurrent=False
                )
            ds = ClassificationDataSet(
                len(self.data_for_training[0][0]), 
                nb_classes=len(categories),
                class_labels=categories
                )
            for data in self.data_for_training:
                ds.addSample(data[0], data[1])

            trainer = BackpropTrainer(net, ds, momentum=0.1, learningrate=0.01, verbose=True)
            trainer.trainUntilConvergence(maxEpochs=500)
            NetworkWriter.writeToFile(net, 'net.xml')
        except Exception as e:
            raise e
        return net

    def define_category(self, request):
        if type(request) == Request:
            net = NetworkReader.readFrom('net.xml')
            return net.activate(request.token)
        else:
            raise ArgumentException()


class Memory:
    'Хранит результаты, а также предоставляет информацию для обучения.'   

    def __init__(self, address):
        self.address = address
        self.es = self._connect_elastic(address)

    def __repr__(self):
        return "Memory('%s')" % (self.address)

    def get_data(self):
        self.all_words = set()
        self.data_templates = dict()
        query = {"query": {"match_all": {}}}
        index_name = 'category'
        results = self.es.search(index=index_name, body=query, size=999)

        for hit in results['hits']['hits']:
            category = hit['_source']['category']
            string = hit['_source']['string']
            words = {w.lower() for w in string.split(' ')}
            self.all_words.update(words)

            if self.data_templates.get(category) is not None:
                self.data_templates[category].append(string)
            else:
                self.data_templates[category] = [string]
        for cat in self.data_templates:
            for i, val in enumerate(self.data_templates[cat]):
                self.data_templates[cat][i] = Request(
                    val, self.all_words
                    )
        return self.data_templates

    def remember(self, request, response):
        if request and response:
            return response
        else:
            raise ArgumentException()
    
    def _connect_elastic(self, address):
        try:
            _es = elasticsearch.Elasticsearch([address])
            return _es
        except Exception as e:
            raise e

class Request:
    'Класс который будет обрабатывать запрос и предоставлять вместо слов токен'

    def __init__(self, string, dictionary):
        self.text_request, self.dictionary = string, dictionary
        self.token = self._tokenization(string, dictionary)

    def __repr__(self):
        return "Request('%s', %s)" % (self.text_request, self.dictionary)

    def _tokenization(self, string, dictionary):
        token_string = []
        list_words = string.lower().split(' ')
        for word in dictionary:
            if word in list_words:
                token_string.append(1)
            else:
                token_string.append(0)
        return token_string


if __name__ == '__main__':
    #try:
        classificator = Classificator()
        memory = Memory('http://localhost:9200')
        data = memory.get_data()
        all_words = memory.all_words
        category = list(data.keys())
        #print(data)
        print(classificator.learn())
        request = Request('нет изображение на камере', all_words);
        response = classificator.define_category(request)
        #assert response == request  # Поменяю когда будет готов define_category()
        #memory.remember(request, response)
        print(category)
        print(response)
        print(category[int(response)])
    #except Exception as e:
    #    print(e, file=stderr)