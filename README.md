# fias-converter
Универсальный конвертер xml-файлов ФИАС (в формате ГАР).

# Возможности
- Конвертация в любую из [поддерживаемых SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/index.html) баз данных
- Поддержка файлов изменений (gar_delta)
- Простота расширения (создание собственных адаптеров)
- Использование в качестве библиотеки

# Установка
```
pip install git+https://github.com/llistochek/fias-converter
```

# Быстрый старт
Внимание: вы должны вручную указать соответствующие схемы. Например,
если вы конвертируете данные `AS_ADDR_OBJ_*.xml` - вам необходимо указать
схему `AS_ADDR_OBJ_*.xsd`.

`<Файлы с данными>` - файлы из архива gar_xml.zip\
`<Файлы со схемами>` - файлы из архива gar_schemas.zip
```
fias-converter --data-files <Файлы с данными> --schema-files <Файлы со схемами> --out-url "sqlite://out.db"
```
Данные будут сохранены в БД sqlite3 под именем out.db.

# Обработка delta файлов
`<Файлы изменений>` - файлы из архива gar_delta_xml.zip
```
fias-converter --delta-files <Файлы изменений>
```

# Создание собственного адаптера
Внимание: на данный момент библиотека находится в стадии разработки. API
может измениться в будущем.

Для создания собственного адаптера унаследуйте класс
`fias_converter.adapters.BaseAdapter` и переопределите все
необходимые методы. В качестве примера можете опираться на класс [SqlalchemyAdapter](./fias_converter/adapters/sqlalchemy.py).

Не забудьте добавить в файл вашего адаптера переменную
fias_converter_adapter, в качестве значения указав класс адаптера.
Например:
```
from fias_converter.adapters import BaseAdapter
class CustomAdapter(BaseAdapter):
    ...

fias_converter_adapter = CustomAdapter
```
Для конвертации данных с помощью вашего адаптера воспользуйтесь
аргументом `--adapter`, например: `--adapter custom_adapter.py`.
