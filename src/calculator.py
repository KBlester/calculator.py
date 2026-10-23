import math
from typing import Union


class CalculatorError(Exception):
    pass


class Calculator:
    def __init__(self):
        self.current = "0"
        self.previous = None
        self.operation = None
        self.memory = 0
        self.history = []
        self.should_reset = False

    def input_digit(self, digit: str):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        if self.current == "0":
            self.current = digit
        else:
            self.current += digit

    def input_decimal(self):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        if "." not in self.current:
            self.current += "."

    def clear(self):
        self.current = "0"
        self.previous = None
        self.operation = None
        self.should_reset = False

    def clear_entry(self):
        self.current = "0"

    def backspace(self):
        if self.should_reset:
            return
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"

    def negate(self):
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current

    def percent(self):
        try:
            value = float(self.current)
            self.current = str(value / 100)
        except ValueError:
            raise CalculatorError("Valor inválido")

    def square_root(self):
        try:
            value = float(self.current)
            if value < 0:
                raise CalculatorError("Não é possível calcular raiz de número negativo")
            self.current = str(math.sqrt(value))
        except ValueError:
            raise CalculatorError("Valor inválido")

    def power(self, exponent: float = 2):
        try:
            value = float(self.current)
            self.current = str(math.pow(value, exponent))
        except ValueError:
            raise CalculatorError("Valor inválido")

    def set_operation(self, op: str):
        try:
            value = float(self.current)
        except ValueError:
            raise CalculatorError("Valor inválido")

        if self.previous is not None and self.operation and not self.should_reset:
            try:
                self.current = str(self._compute(self.previous, value, self.operation))
            except CalculatorError:
                pass
            self.previous = float(self.current)
        else:
            self.previous = value

        self.operation = op
        self.should_reset = True

    def compute(self) -> str:
        if self.previous is None or self.operation is None or self.should_reset:
            return self.current

        try:
            value = float(self.current)
            result = self._compute(self.previous, value, self.operation)
            self._add_to_history(self.previous, self.operation, value, result)
            self.current = self._format_result(result)
            self.previous = None
            self.operation = None
            self.should_reset = True
            return self.current
        except ZeroDivisionError:
            raise CalculatorError("Divisão por zero")
        except ValueError:
            raise CalculatorError("Valor inválido")

    def _compute(self, a: float, b: float, op: str) -> float:
        if op == "add":
            return a + b
        if op == "subtract":
            return a - b
        if op == "multiply":
            return a * b
        if op == "divide":
            if b == 0:
                raise ZeroDivisionError()
            return a / b
        if op == "modulo":
            return a % b
        raise CalculatorError("Operação inválida")

    def _format_result(self, value: float) -> str:
        if value == int(value):
            return str(int(value))
        formatted = f"{value:.10f}".rstrip("0").rstrip(".")
        return formatted

    def _add_to_history(self, a: float, op: str, b: float, result: float):
        op_symbols = {"add": "+", "subtract": "-", "multiply": "×", "divide": "÷", "modulo": "%"}
        symbol = op_symbols.get(op, op)
        entry = f"{self._format_result(a)} {symbol} {self._format_result(b)} = {self._format_result(result)}"
        self.history.append(entry)
        if len(self.history) > 50:
            self.history.pop(0)

    def memory_add(self):
        self.memory += float(self.current)

    def memory_subtract(self):
        self.memory -= float(self.current)

    def memory_recall(self):
        self.current = str(self._format_result(self.memory))
        self.should_reset = True

    def memory_clear(self):
        self.memory = 0

    def get_history(self):
        return list(self.history)

    def clear_history(self):
        self.history.clear()
