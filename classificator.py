from sys import stderr
import numpy as np
import elasticsearch 
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter
from pybrain.structure import TanhLayer, SoftmaxLayer, LinearLayer


class ArgumentException(Exception):
    pass

class Classificator:


    data_for_training = []
    
    def learn(self, data, all_words):
        if data:
            categories = list(data.keys())
            for category in data:
                for string in data[category]:
                    out_layer = [0] * len(categories)
                    in_layer = self._tokenization(string, all_words)
                    out_layer[categories.index(category)] = 1
                    self.data_for_training.append([in_layer, out_layer])
            self.data_for_training = np.array(self.data_for_training)
            self.net = buildNetwork(
                len(self.data_for_training[:, 0][0]), 
                5, 
                len(self.data_for_training[:, 1][0]), 
                hiddenclass=LinearLayer, 
                recurrent=False
                )
            ds = SupervisedDataSet(
                len(self.data_for_training[:, 0][0]), 
                len(self.data_for_training[:, 1][0])
                )
            i = 0
            for inp in self.data_for_training[:, 0]:
                ds.addSample(inp, self.data_for_training[:, 1][i])
                i += 1

            trainer = BackpropTrainer(self.net, ds, learningrate=0.05)
            trainer.trainEpochs(500)
            NetworkWriter.writeToFile(self.net, 'net.xml')
        else:
            raise ArgumentException()

    def define_category(self, request):
        if request:
            return request
        else:
            raise ArgumentException()

    def _tokenization(self, string, all_words):
        token_string = []
        list_words = string.lower().split(' ')
        for word in all_words:
            if word in list_words:
                token_string.append(1)
            else:
                token_string.append(0)
        return token_string

    

class Memory:
    'Хранит результаты, а также предоставляет информацию для обучения.'   

    category = []

    all_words = set()

    data_templates = dict() 

    def __init__(self, address):
        self.address = address
        self.es = self._connect_elastic(address)

    def __repr__(self):
        return "Memory('%s')" % (self.address)

    def get_data(self):
        query = {"query": {"match_all": {}}}
        index_name = 'category'
        results = self.es.search(index=index_name, body=query, size=999)

        for hit in results['hits']['hits']:
            category = hit['_source']['category']
            self.category.append(category)
            string = hit['_source']['string']
            words = {w.lower() for w in string.split(' ')}
            self.all_words.update(words)

            if self.data_templates.get(category) is not None:
                self.data_templates[category].append(string)
            else:
                self.data_templates[category] = [string]

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


if __name__ == '__main__':
    try:
        classificator = Classificator()
        memory = Memory('http://localhost:9200')
        data = memory.get_data()
        all_words = memory.all_words
        print(data)
        print(classificator.learn(data, all_words))
        request = 'Не показывает канал матч';
        response = classificator.define_category(request)
        assert response == request  # Поменяю когда будет готов define_category()
        memory.remember(request, response)
        print(response)
    except Exception as e:
        print(e, file=stderr)