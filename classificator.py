from sys import stderr
import elasticsearch 

class ArgumentException(Exception):
    pass

class Classificator:


    def learn(data):
        if data:
            pass
        else:
            raise ArgumentException()

    def define_category(request):
        if request:
            return request
        else:
            raise ArgumentException()


class Memory:
    'Хранит результаты, а также предоставляет информацию для обучения.'   

    category = []

    all_words = set()

    category_words = dict() 

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

            if self.category_words.get(category) is not None:
                self.category_words[category].update(words)
            else:
                self.category_words[category] = set(words)

        return self.category_words

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
        classificator = Classificator
        memory = Memory('http://localhost:9200')
        data = memory.get_data()
        print(memory.category)
        print(memory.all_words)
        print(data)
        classificator.learn(memory.get_data())
        request = 'Не показывает канал матч';
        response = classificator.define_category(request)
        assert response == request  # Поменяю когда будет готов define_category()
        memory.remember(request, response)
        print(response)
    except Exception as e:
        print(type(e), file=stderr)