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

    def __init__(self, address):
        self.address = address
        self.es = self._connect_elastic(address)

    def __repr__(self):
        return "Memory('%s')" % (self.address)

    def get_data(self):
        query = {"query": {"match_all": {}}}
        index_name = 'category'
        results = self.es.search(index=index_name, body=query, size=999)
        data = dict()
        for hit in results['hits']['hits']:
            category = hit['_source']['category']
            string = hit['_source']['string']
            if data.get(category) is not None:
                data[category].append(string)
            else:
                data[category] = [string]
        return data

    def remember(self, request, respone):
        if request and respone:
            return respone
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
        classificator.learn(memory.get_data())
        request = 'Не показывает канал матч';
        respone = classificator.define_category(request)
        memory.remember(request, respone)
        print(respone)
    except Exception as e:
        print(type(e), file=stderr)