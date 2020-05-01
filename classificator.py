class Classificator:
    pass

class Memory:   # Будем настраивать связь с базой данных. 
    pass        # Хранить результаты, а также брать информацию для обучения.
        
if __name__ == '__main__':
    classificator = Classificator
    memory = Memory
    classificator.learn(memory.get_data())
    request = 'Не показывает канал матч';
    respone = classificator.define_category(request)
    memory.remember(request, respone)
    print(respone)