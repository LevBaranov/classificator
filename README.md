# Сlassificator
## Описание
Цель: По небольшому тексту (запрос на обслуживание в support) определить категорию проблемы. Категории проблем заранее известны.
Необходимо по тексту понять к какой проблеме относится запрос

Категории:
* Не работает интернет/канал связи
* Деградация услуги интернет/канала связи
* Не работает Телефония
* Плохое качество услуги Телефония
* Не работает видеонаблюдение.
* Не работает ТВ.
* Плохо качество ТВ.

Будем создавать классификатор проблем пользователей . Можно использовать для умного распрделеения по скилл-групам, а также для проведения автодиагностик.
Прототип: https://github.com/LevBaranov/troubleclassificator
Недостатки прототипа: Не Объектно-ориетированый, не интегрирован с БД, меньше категорий проблем.


## Библиотеки
* PyBrain [GIT](https://github.com/pybrain/pybrain) и [Home Page](http://pybrain.org/docs/index.html)
* [numpy](https://numpy.org/)
* [elasticsearch](https://elasticsearch-py.readthedocs.io/en/master/index.html)

## Планируемый вариант работы:
На вход подаём текст. 
На выходе получаем к какой категории относится заявка.
