<h1 align="center"> 
  Нейропсихолог - твой личный психолог 🔮
</h1>

# Навигация и информация
 + [x] Полное логирование в `datebase.db`.
 + [x] Полное логирование в `sessions.xlsx`.
 + [x] Озвучка разными голосами.
 + [x] Настройки 

- [Установка](#установка)
- [Предпросмотр](#предпросмотр)
- [Использование](#использование)
- [Настройки](#настройки-приложения)

# Установка
0. Установите [Python3.10](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe]) и выше, если у вас его нету
1. Файлы
   - Скопируйте проект с GitHub к себе на компьютер
   - Установите все зависимости
    ```
    pip install -r requamerents.txt
    ```
2. API
   - В файле [`.env`](.env) установите API-keys модулей `SHUTTLE` и `MANDRILL`, без `< >`. Получить ключи можно [здесь](#api)

3. VOSK\
   В проекте есть малая модель `vosk`, но для коректной работы большой модели её требуется [установить](https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip).
   Также можно [установить](https://alphacephei.com/vosk/models) и другие похожие модели.

### API
- ShuttleAI
   - Перейдите на дискорд сервер [ShuttleAI](https://discord.gg/a6CpU7tG)
   - Пройдите верефикацию по их стандартам.
   - Перейдите в канал [#commands](https://discord.com/channels/1152262611291869237/1152270639672086599)
   - Пропишите команду ```/getkey```. И скопируйте полученый ключ от бота.
   - Вставте ключ в графу `SHUTTLE` в файле [`.env`](.env)

+ Mandrill
   - Перейдите на дискорд сервер [ShuttleAI](https://discord.gg/SM38TEf8)
   - Пройдите верефикацию по их стандартам.
   - Перейдите в канал [#commands](https://discord.com/channels/1158163844959571989/1177105424303013970)
   - Пропишите команду ```/key get```. И скопируйте полученый ключ от бота.
   - Вставте ключ в графу `MANDRILL` в файле [`.env`](.env)
> [!NOTE]
> Если вы являетесь модерацией talent.kruzhok.org open-source, то напишите мне, для получения ключей.

# Запуск
  - Запускаем приложение. Основной файл `main.py` через
  PyCharm или другой IDE

или

Windows cmd:
```
python3.10 main.py
```
___
# Предпросмотр
| ![image](https://github.com/RRozi/NeuroPsychologist/assets/111123403/586b4102-a148-406e-83f5-a2b8f16c2dab) | ![image](https://github.com/RRozi/NeuroPsychologist/assets/111123403/ffe2588b-7769-44f4-8eaf-41ebda3ff0d3) | ![image](https://github.com/RRozi/NeuroPsychologist/assets/111123403/2666481a-3f1f-4fc1-a767-700ce1b72520)|
|:--------------------------:|:--------------------------:|:--------------------------:
|     Домашняя страница     |      Основная страница    |      Оценка по завершению    |
##### Пример [озвучки](https://drive.google.com/file/d/1HvA810jcJnC3Tf7ikf-NGe4NhGl-icE_/view?usp=sharing) с скриншота `Основной страницы`
> [!CAUTION]
> Обратите внимание! На данный момент могут возникнуть проблемы при озвучке **большого текста**, ответа от бота

## Настройки приложения
Вы сможете:
 - Переключить модель **GPT**. `GPT-3.5-turbo`, `GPT-4`
 - Переключить модель **VOSK**. Доступна Маленькая и [Большая](#установка) модель.
 - Менять **голос** озвучки текста

![image](https://github.com/RRozi/NeuroPsychologist/assets/111123403/f77b70a6-9b62-497f-89a3-13877c0bf330)

___
# Использование
- Начало.
  - [Запустите](#запуск) проект.
  - Нажмите клавишу - `Запустить сессию`
- Общение.
  - Введите желаемый запрос в поле `Введите сообщение...` и нажмите `Enter` или на кнопку правее.
  - **!ВАЖНО!** Для ввода голосом, нажмите на значок `микрофона` и начните задавать свой вопрос, дождитесь как ваш текст введется, после чего нажмите на `крестик`
  - Если хотите выключить озвучку, нажмите на кнопку `*Динамика`.
  - Если хотите прослушать последнее сообщение, нажмите на кнопку `*Воспроизвести`(левее от кнопки `*Динамика`)
  - Если хотите удалить `историю` общения, нажмите на соответствующую кнопку.
- Настройки.
   - Можете настроить приложение под себя. [Подробнее](#настройки-приложения)
- Оценка.
   - После работы с приложением, нажмите на кнопку `Завершить сессию`.
   - В следующем окне выберите желаемую оценку и напишите доп. коментарий по желанию.





