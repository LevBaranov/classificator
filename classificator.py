class Classificator:

    def learn(self, data):
        pass

class Memory:
    'Хранить результаты, а также предоставляет информацию для обучения.'   
    pass
        
if __name__ == '__main__':
    classificator = Classificator
    memory = Memory
    classificator.learn(memory.get_data())
    request = 'Не показывает канал матч';
    respone = classificator.define_category(request)
    memory.remember(request, respone)
    print(respone)