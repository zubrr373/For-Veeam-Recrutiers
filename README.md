# For-Veeam-Recrutiers
Добрый день, вот результат выполнения мною тестового задания. Вынужден прокомментировать некоторые моменты.

1) %CPU не совпадает с диспетчером задач, это нормально, т.к. подсчёт идёт вручную по времени и учитывает время простоя процессора при взаимодействии с другими компонентами системы. Также он может быть выше 100% т.к. отображает загруженность без учёта числа задействованных ядер.
2) В качестве формата сохранения данных был выбран JSON. Можно было взять CSV, для конкретной задачи это даже лучше, но пострадала бы масштабируемость.
3) Данные сохраняются в директорию запуска скрипта, т.к. это относительная величина может быть вычислена на любой машине, а вот имена дисков и папок могут различаться.
4) Время опроса задаётся пользователем, но не может быть меньше одной секунды, т.к. время взаимодействия с компонентами системы ощутимо.
5) В связи с долгим взаимодействием и большим временем опроса программа может выдать нулевые значения последним запросом, проверка хэндлов создана чтобы предотвратить попадание этих данных в статистику
6) После отправки мною была замечена очень глупая и критическая ошибка. Прошу строго не судить, благо она уже исправлена.
