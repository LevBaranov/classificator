from sys import stderr 

class ArgumentException(Exception):
    pass

class Classificator:


    def learn(data):
        if(data):
            pass
        else:
            raise ArgumentException()

    def define_category(request):
        if(request):
            pass
        else:
            raise ArgumentException()


class Memory:
    'Хранит результаты, а также предоставляет информацию для обучения.'   

    def get_data():
        pass

    def remember(request, respone):
        if(request and respone):
            pass
        else:
            raise ArgumentException()

   
if __name__ == '__main__':
    try:
        classificator = Classificator
        memory = Memory
        classificator.learn(memory.get_data())
        request = 'Не показывает канал матч';
        respone = classificator.define_category(request)
        memory.remember(request, respone)
        print(respone)
    except Exception as e:
        print(type(e), file=stderr)