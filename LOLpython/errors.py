class LOLPythonError(Exception):
    """Базовий клас для всіх помилок в інтерпретаторі."""
    pass

class LexerError(LOLPythonError):
    """Помилка на етапі лексичного аналізу."""
    pass

class ParserError(LOLPythonError):
    """Помилка на етапі синтаксичного аналізу."""
    pass

class InterpreterError(LOLPythonError):
    """Помилка під час виконання (runtime)."""
    pass
