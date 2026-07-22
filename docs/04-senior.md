## Итерация 4 — Senior

Цель этапа — заменить жёстко заданную логику `Fizz`/`Buzz` на **расширяемый движок правил**, в котором новое поведение добавляется через создание и подключение правила, а не через изменение ядра.

Текущая Middle-реализация уже разделяет вычисление одного значения, генерацию диапазона, ошибки и CLI. Однако `evaluate()` по-прежнему непосредственно содержит проверки кратности `3` и `5`. Именно эту зависимость Senior-этап должен устранить. fileciteturn0file3

Предполагаемая структура пакета:

```text
src/fizzbuzz_evolution/senior/
├── __init__.py
├── __main__.py
├── cli.py
├── engine.py
├── errors.py
├── generator.py
├── presets.py
└── rules/
    ├── __init__.py
    ├── protocol.py
    └── divisibility.py
```

## 1. Контракт правила

Будет определён общий контракт, которому должен соответствовать любой объект правила.

Для текущего проекта оптимален структурный контракт через `Protocol`:

```python
from typing import Protocol


class Rule(Protocol):
    def matches(self, number: int) -> bool:
        """Return whether the rule matches the number."""
        ...

    def render(self, number: int) -> str:
        """Return the text produced for a matching number."""
        ...
```

Движок будет зависеть только от этого контракта и не будет знать:

- что правило проверяет кратность;
- какой у него делитель;
- возвращает ли оно `Fizz`, `Buzz` или другое значение;
- реализовано ли правило классом, dataclass или другим объектом.

### Почему `matches()` и `render()`

Разделение двух операций позволяет в дальнейшем создавать не только статические замены:

```text
кратно 3 → Fizz
```

но и правила, чей результат зависит от самого числа:

```text
отрицательное число → Negative(<number>)
```

При этом в рамках Senior будет реализовано только правило кратности. Другие типы правил понадобятся преимущественно для проверки расширяемости.

### Почему не абстрактный базовый класс

`Protocol` лучше показывает идею слабой связанности:

- пользовательское правило не обязано наследоваться от библиотечного класса;
- движку важно поведение объекта, а не его место в иерархии;
- пользователь может реализовать собственное правило без зависимости от внутренней реализации пакета.

Это заметное отличие Senior от Middle: зависимость строится от абстракции, а не от конкретной функции.

---

## 2. Правило кратности

Будет реализован конкретный тип правила:

```python
@dataclass(frozen=True, slots=True)
class DivisibilityRule:
    divisor: int
    replacement: str

    def matches(self, number: int) -> bool:
        return number % self.divisor == 0

    def render(self, number: int) -> str:
        return self.replacement
```

Примеры:

```python
DivisibilityRule(3, "Fizz")
DivisibilityRule(5, "Buzz")
DivisibilityRule(7, "Bazz")
```

### Валидация

Конструктор должен отклонять некорректное состояние:

- делитель `0`;
- пустую строку замены;
- строку, состоящую только из пробельных символов.

Для этого будут добавлены ошибки уровня Senior:

```python
class FizzBuzzError(Exception):
    """Base exception for expected Senior-stage failures."""


class InvalidDivisorError(FizzBuzzError):
    """Raised when a rule uses zero as its divisor."""


class InvalidReplacementError(FizzBuzzError):
    """Raised when a rule has no meaningful replacement."""
```

Правило должно быть неизменяемым после создания. Это исключает ситуацию, когда конфигурация движка неожиданно меняется во время обработки последовательности.

### Отрицательный делитель

Отрицательные делители можно считать допустимыми:

```python
DivisibilityRule(-3, "Fizz")
```

Для проверки кратности они имеют ту же математическую семантику, что и положительные. Запрещать необходимо только ноль.

---

## 3. Движок правил

Основным компонентом станет `RuleEngine`:

```python
class RuleEngine:
    def __init__(self, rules: Iterable[Rule]) -> None:
        ...

    def evaluate(self, number: int) -> str:
        ...
```

Алгоритм:

1. последовательно обойти правила;
2. выбрать все правила, для которых `matches(number)` вернул `True`;
3. получить результат каждого совпавшего правила через `render(number)`;
4. объединить результаты в порядке регистрации;
5. вернуть строковое представление числа, если не совпало ни одно правило.

Пример:

```python
engine = RuleEngine(
    [
        DivisibilityRule(3, "Fizz"),
        DivisibilityRule(5, "Buzz"),
    ]
)

engine.evaluate(3)   # "Fizz"
engine.evaluate(5)   # "Buzz"
engine.evaluate(15)  # "FizzBuzz"
engine.evaluate(7)   # "7"
```

### Порядок правил

Порядок подключения будет частью публичного контракта.

```python
RuleEngine(
    [
        DivisibilityRule(5, "Buzz"),
        DivisibilityRule(3, "Fizz"),
    ]
).evaluate(15)
```

Результат:

```text
BuzzFizz
```

Движок не должен самостоятельно сортировать правила по делителю, названию или внутреннему приоритету. Это делает поведение простым и предсказуемым:

> порядок результата равен порядку зарегистрированных правил.

Явный `priority` на этом этапе не нужен. Он добавит дополнительную политику сортировки, но не даст новой принципиальной возможности. Более сложное управление порядком лучше оставить Enterprise-конфигурации.

### Хранение правил

Полученный набор желательно сразу преобразовывать в кортеж:

```python
self._rules = tuple(rules)
```

Это:

- позволяет принимать списки, кортежи и генераторы;
- фиксирует состав движка после создания;
- предотвращает изменение через исходный внешний список;
- позволяет безопасно переиспользовать движок.

### Пустой движок

Пустой набор правил должен быть допустим:

```python
engine = RuleEngine([])

engine.evaluate(15) == "15"
```

Это естественное поведение универсального движка: если правил нет, каждое значение возвращается без замены.

---

## 4. Presets

Чтобы пользователь не собирал классический FizzBuzz вручную при каждом вызове, будет добавлен модуль `presets.py`.

Базовый preset:

```python
CLASSIC_RULES: tuple[Rule, ...] = (
    DivisibilityRule(3, "Fizz"),
    DivisibilityRule(5, "Buzz"),
)
```

Также удобнее предоставить фабрику движка:

```python
def create_fizzbuzz_engine() -> RuleEngine:
    return RuleEngine(CLASSIC_RULES)
```

Пример использования:

```python
from fizzbuzz_evolution.senior import create_fizzbuzz_engine

engine = create_fizzbuzz_engine()
engine.evaluate(15)
```

### Зачем одновременно правила и фабрика

`CLASSIC_RULES` позволяет:

- расширить стандартный набор;
- переиспользовать правила в собственном движке;
- показать конфигурационную природу решения.

Фабрика позволяет:

- получить готовый движок;
- скрыть детали его сборки;
- использовать стандартное поведение в CLI и генераторе.

### Расширение preset

Пользователь сможет создать расширенный набор без изменения пакета:

```python
extended_rules = (
    *CLASSIC_RULES,
    DivisibilityRule(7, "Bazz"),
)

engine = RuleEngine(extended_rules)
```

Результаты:

```text
3   → Fizz
5   → Buzz
7   → Bazz
21  → FizzBazz
35  → BuzzBazz
105 → FizzBuzzBazz
```

Именно этот сценарий станет основным доказательством расширяемости Senior-версии.

---

## 5. Генерация диапазона

Генератор перестанет напрямую зависеть от конкретного evaluator и будет принимать движок:

```python
def generate(
    engine: RuleEngine,
    start: int = 1,
    end: int = 100,
) -> list[str]:
    ...
```

Использование:

```python
engine = create_fizzbuzz_engine()

generate(engine, 3, 5)
# ["Fizz", "4", "Buzz"]
```

Таким образом:

- `RuleEngine` отвечает за одно число;
- `generate()` отвечает за диапазон;
- preset отвечает за стандартную конфигурацию;
- CLI отвечает за ввод и вывод.

Проверка обратного диапазона и `InvalidRangeError`, реализованные в Middle, сохраняются. Однако ошибки Senior должны принадлежать пакету `senior`, а не импортироваться из `middle`: этап должен быть самостоятельной реализацией, а не оболочкой над предыдущим пакетом.

---

## 6. Публичный API

В `senior/__init__.py` планируется экспортировать основные строительные блоки:

```python
from .engine import RuleEngine
from .generator import generate
from .presets import CLASSIC_RULES, create_fizzbuzz_engine
from .rules import DivisibilityRule, Rule

__all__ = [
    "CLASSIC_RULES",
    "DivisibilityRule",
    "Rule",
    "RuleEngine",
    "create_fizzbuzz_engine",
    "generate",
]
```

Это даст два способа использования.

### Готовый классический вариант

```python
engine = create_fizzbuzz_engine()
engine.evaluate(15)
```

### Собственная конфигурация

```python
engine = RuleEngine(
    [
        DivisibilityRule(2, "Foo"),
        DivisibilityRule(7, "Bar"),
    ]
)
```

---

## 7. CLI

CLI Senior-этапа сохранит знакомое поведение Middle:

```bash
python -m fizzbuzz_evolution.senior
python -m fizzbuzz_evolution.senior --start -5 --end 15
```

По умолчанию он будет использовать классический preset.

На этом этапе CLI не должен принимать правила через JSON, YAML или аргументы вида:

```bash
--rule 3:Fizz
```

Причина — разделение этапов:

- Senior демонстрирует программную расширяемость;
- Enterprise добавит внешнюю конфигурацию и инфраструктурные адаптеры.

То есть правила Senior конфигурируются в Python-коде, но ядро уже не требует изменения при их расширении.

---

## 8. Тестирование контракта правила

Планируемая структура тестов:

```text
tests/senior/
├── test_cli.py
├── test_divisibility_rule.py
├── test_engine.py
├── test_generator.py
├── test_presets.py
└── test_rule_extensions.py
```

### `test_divisibility_rule.py`

Будут проверены:

- совпадение для кратного числа;
- отсутствие совпадения;
- ноль как проверяемое число;
- отрицательные числа;
- отрицательный делитель;
- возвращаемая замена;
- запрет нулевого делителя;
- запрет пустой замены;
- неизменяемость объекта.

Примеры:

```python
rule = DivisibilityRule(3, "Fizz")

assert rule.matches(3)
assert rule.matches(0)
assert rule.matches(-3)
assert not rule.matches(4)
assert rule.render(3) == "Fizz"
```

---

## 9. Тестирование движка

Для `RuleEngine` будут зафиксированы следующие сценарии:

### Ни одно правило не совпало

```python
engine.evaluate(2) == "2"
```

### Одно правило совпало

```python
engine.evaluate(3) == "Fizz"
```

### Несколько правил совпали

```python
engine.evaluate(15) == "FizzBuzz"
```

### Порядок регистрации сохраняется

```python
engine = RuleEngine(
    [
        DivisibilityRule(5, "Buzz"),
        DivisibilityRule(3, "Fizz"),
    ]
)

assert engine.evaluate(15) == "BuzzFizz"
```

### Пустой набор правил

```python
RuleEngine([]).evaluate(15) == "15"
```

### Входной iterable материализуется

Будет проверено, что движок корректно принимает генератор правил и не зависит от его повторного обхода.

### Внешний список не изменяет движок

```python
rules = [DivisibilityRule(3, "Fizz")]
engine = RuleEngine(rules)

rules.append(DivisibilityRule(5, "Buzz"))

assert engine.evaluate(5) == "5"
```

Так фиксируется неизменяемость конфигурации движка после создания.

---

## 10. Проверка расширения правил

Это центральная часть итерации.

В тестах будет создано пользовательское правило, которое не наследуется от `DivisibilityRule` и не требует изменения `RuleEngine`.

Например:

```python
@dataclass(frozen=True)
class ExactMatchRule:
    expected: int
    replacement: str

    def matches(self, number: int) -> bool:
        return number == self.expected

    def render(self, number: int) -> str:
        return self.replacement
```

Использование:

```python
engine = RuleEngine(
    [
        DivisibilityRule(3, "Fizz"),
        ExactMatchRule(10, "Ten"),
    ]
)

assert engine.evaluate(3) == "Fizz"
assert engine.evaluate(10) == "Ten"
```

Можно дополнительно проверить динамический результат:

```python
class SquareRule:
    def matches(self, number: int) -> bool:
        return number >= 0 and isqrt(number) ** 2 == number

    def render(self, number: int) -> str:
        return f"Square({number})"
```

Это докажет, что контракт правила не ограничивает реализацию статической строкой или проверкой делимости.

Главная проверяемая идея:

> Для добавления нового поведения создаётся новый объект правила.  
> Код `RuleEngine` при этом не изменяется.

---

## 11. Общий контракт этапов

Senior preset будет добавлен в общий поведенческий тест:

```python
senior_engine = create_fizzbuzz_engine()
senior_evaluate = senior_engine.evaluate
```

Общий контракт продолжит проверять:

```text
1  → "1"
3  → "Fizz"
5  → "Buzz"
15 → "FizzBuzz"
```

То есть архитектура существенно меняется, но классическое пользовательское поведение остаётся совместимым.

Дополнительно в общий контракт разумно включить уже зафиксированные Middle-граничные значения:

```text
0   → "FizzBuzz"
-3  → "Fizz"
-5  → "Buzz"
-15 → "FizzBuzz"
```

---

## 12. Отличие Senior от Middle

| Аспект | Middle | Senior |
|---|---|---|
| Логика FizzBuzz | Зашита в `evaluate()` | Передаётся набором правил |
| Абстракция правила | Отсутствует | Явный `Rule`-контракт |
| Делители | Жёстко заданы: `3`, `5` | Параметры `DivisibilityRule` |
| Замены | Жёстко заданы | Параметры правила |
| Совпадения | Две конкретные проверки | Обход произвольного набора |
| Расширение | Изменение evaluator | Добавление нового правила |
| Порядок | Задан кодом функции | Задан конфигурацией движка |
| Стандартный FizzBuzz | Непосредственная реализация | Готовый preset |
| Пользовательские правила | Не поддерживаются | Поддерживаются через контракт |
| Конфигурация из файла | Нет | Пока нет |
| DI-контейнер | Нет | Нет |
| DDD и инфраструктура | Нет | Нет |

Главная мысль этапа:

> Middle разделяет существующий алгоритм на компоненты.  
> Senior делает сам алгоритм открытым для расширения.

---

## 13. Документация

Будет добавлен файл:

```text
docs/04-senior.md
```

В нём следует описать:

- контракт правила;
- выбор `Protocol`;
- устройство `DivisibilityRule`;
- алгоритм движка;
- порядок объединения результатов;
- назначение presets;
- пример пользовательского правила;
- принцип Open/Closed;
- границу между Senior и Enterprise.

README будет обновлён:

```text
senior | 04-senior | Extensible rule engine | Implemented
```

Также будут добавлены примеры программного использования:

```python
from fizzbuzz_evolution.senior import (
    CLASSIC_RULES,
    DivisibilityRule,
    RuleEngine,
)

engine = RuleEngine(
    (
        *CLASSIC_RULES,
        DivisibilityRule(7, "Bazz"),
    )
)

print(engine.evaluate(105))
# FizzBuzzBazz
```

---

## 14. Что намеренно не входит в Senior

Чтобы не смешивать этап с Enterprise, здесь не планируются:

- загрузка правил из JSON или YAML;
- DI-контейнер;
- репозиторий правил;
- доменные сущности и агрегаты;
- идентификаторы и версии правил;
- логирование;
- метрики и tracing;
- HTTP API;
- OpenAPI;
- хранение конфигурации;
- плагины и динамическая загрузка модулей;
- приоритеты и конфликтные политики;
- асинхронное выполнение;
- кэширование;
- сериализация результатов.

Senior должен быть расширяемой **Python-библиотекой**, а Enterprise превратит это ядро в конфигурируемое приложение с инфраструктурой.

---

## Ожидаемый результат итерации

После реализации пакет будет выглядеть примерно так:

```text
senior/
├── __init__.py
├── __main__.py
├── cli.py
├── engine.py
├── errors.py
├── generator.py
├── presets.py
└── rules/
    ├── __init__.py
    ├── protocol.py
    └── divisibility.py
```

Итерация считается завершённой, когда:

- классический preset полностью повторяет поведение предыдущих этапов;
- движок не содержит упоминаний `Fizz`, `Buzz`, `3` или `5`;
- новое правило подключается без изменения движка;
- порядок правил явно определён и покрыт тестами;
- некорректные правила отклоняются при создании;
- генератор и CLI используют готовый preset;
- Senior включён в общий поведенческий контракт;
- документация показывает практическое отличие от Middle;
- успешно проходят:

```bash
ruff check .
ruff format --check .
mypy
python -m pytest
```

Текущая версия проекта, на основе которой составлен план: [архив FizzBuzz Evolution](sandbox:/mnt/data/fizzbuzz-evolution-2026-07-22-20-40-21-main-16dfbae.zip).