"""
CAS — Система компьютерной алгебры
Точка входа: python main.py

Использование:
  python main.py              — интерактивный режим
  python main.py --help       — справка
"""

"""
Aвтор модуля: <Крепышев М.М>
"""

import sys
import re

HELP = """
╔══════════════════════════════════════════════════════════╗
║           CAS — Система компьютерной алгебры            ║
╚══════════════════════════════════════════════════════════╝

Два режима ввода:

1) Вызов функции напрямую:
   COM_NN_D 123 456
   ADD_ZZ_Z -123 456
   DIV_QQ_Q 3/4 1/2

2) Математическое выражение:
   123 + 456 * 2
   -5 + 10
   3/4 + 1/2
   (100 - 20) * 3

Модуль N — Натуральные числа
  COM_NN_D  <a> <b>        сравнение: 2(a>b), 0(a=b), 1(a<b)
  NZER_N_B  <a>            проверка на ноль
  ADD_1N_N  <a>            прибавить 1
  ADD_NN_N  <a> <b>        сложение
  SUB_NN_N  <a> <b>        вычитание (a >= b)
  MUL_ND_N  <a> <d>        умножение на цифру d
  MUL_Nk_N  <a> <k>        умножение на 10^k
  MUL_NN_N  <a> <b>        умножение
  SUB_NDN_N <a> <d> <b>    a - d*b (результат >= 0)
  DIV_NN_Dk <a> <b> <k>    первая цифра деления
  DIV_NN_N  <a> <b>        целая часть a/b
  MOD_NN_N  <a> <b>        остаток a mod b
  GCF_NN_N  <a> <b>        НОД
  LCM_NN_N  <a> <b>        НОК

Модуль Z — Целые числа  (формат: -123 или 123)
  ABS_Z_N   <a>            модуль
  POZ_Z_D   <a>            знак: 2=полож, 0=ноль, 1=отриц
  MUL_ZM_Z  <a>            умножить на -1
  TRANS_N_Z <a>            натуральное → целое
  TRANS_Z_N <a>            целое >= 0 → натуральное
  ADD_ZZ_Z  <a> <b>        сложение
  SUB_ZZ_Z  <a> <b>        вычитание
  MUL_ZZ_Z  <a> <b>        умножение
  DIV_ZZ_Z  <a> <b>        частное
  MOD_ZZ_Z  <a> <b>        остаток

Модуль Q — Рациональные числа  (формат: 3/4 или -1/2)
  RED_Q_Q   <a>            сокращение дроби
  INT_Q_B   <a>            проверка на целое
  TRANS_Z_Q <a>            целое → дробное
  TRANS_Q_Z <a>            дробное (целое) → целое
  ADD_QQ_Q  <a> <b>        сложение
  SUB_QQ_Q  <a> <b>        вычитание
  MUL_QQ_Q  <a> <b>        умножение
  DIV_QQ_Q  <a> <b>        деление

Введите 'help' для справки, 'exit' для выхода.
"""

# ──────────────────────────────────────────────
# ПАРСИНГ АРГУМЕНТОВ
# ──────────────────────────────────────────────

def parse_nat(s: str):
    """'123' → (2, [3, 2, 1])"""
    s = s.strip()
    if not s.isdigit():
        raise ValueError(f"Ожидается натуральное число, получено: '{s}'")
    digits = [int(c) for c in reversed(s)]
    while len(digits) > 1 and digits[-1] == 0:
        digits.pop()
    return (len(digits) - 1, digits)


def parse_int(s: str):
    """'-123' → (1, 2, [3,2,1])   '123' → (0, 2, [3,2,1])"""
    s = s.strip()
    sign = 1 if s.startswith('-') else 0
    nat = parse_nat(s.lstrip('+-'))
    n, digits = nat
    if n == 0 and digits == [0]:
        sign = 0  # ноль всегда положительный
    return (sign, n, digits)


def parse_rat(s: str):
    """'3/4' → (Integer(3), Natural(4))   '-1/2' → (Integer(-1), Natural(2))"""
    s = s.strip()
    if '/' not in s:
        return (parse_int(s), parse_nat('1'))
    num_str, den_str = s.split('/', 1)
    den = parse_nat(den_str)
    if den == (0, [0]):
        raise ValueError("Знаменатель не может быть нулём")
    return (parse_int(num_str), den)


def parse_arg(arg: str, typ: str):
    """Разбор одного строкового аргумента в нужный тип."""
    if typ == "N":   return parse_nat(arg)
    if typ == "Z":   return parse_int(arg)
    if typ == "Q":   return parse_rat(arg)
    if typ == "int": return int(arg)
    raise ValueError(f"Неизвестный тип: '{typ}'")


# ──────────────────────────────────────────────
# ОПРЕДЕЛЕНИЕ ТИПА ПО СТРОКЕ
# ──────────────────────────────────────────────

def detect_type(s: str) -> str:
    """Определяет тип значения по его строковому представлению."""
    if 'x' in s:
        return "P"
    if '/' in s:
        return "Q"
    if re.match(r'^-\d+$', s):
        return "Z"
    if re.match(r'^\d+$', s):
        return "N"
    raise ValueError(f"Не удалось определить тип: '{s}'")


# ──────────────────────────────────────────────
# ФОРМАТИРОВАНИЕ РЕЗУЛЬТАТА
# ──────────────────────────────────────────────

def format_nat(a) -> str:
    _, digits = a
    return ''.join(str(d) for d in reversed(digits)) or '0'


def format_int(a) -> str:
    sign, _, digits = a
    s = ''.join(str(d) for d in reversed(digits)) or '0'
    return ('-' + s) if (sign == 1 and s != '0') else s


def format_rat(a) -> str:
    num, den = a
    n = format_int(num)
    d = format_nat(den)
    return f"{n}/{d}" if d != '1' else n


def format_value(x) -> str:
    """Определяет тип результата и форматирует его в строку."""
    if not isinstance(x, tuple):
        return str(x)
    # Natural = (int, list)
    if len(x) == 2 and isinstance(x[1], list):
        return format_nat(x)
    # Integer = (int, int, list)
    if len(x) == 3 and isinstance(x[2], list):
        return format_int(x)
    # Rational = (Integer, Natural)
    if len(x) == 2 and isinstance(x[0], tuple) and isinstance(x[1], tuple):
        return format_rat(x)
    return str(x)


# ──────────────────────────────────────────────
# ОБЁРТКА ФУНКЦИЙ
# ──────────────────────────────────────────────

def wrap(func, types: list):
    """Возвращает функцию, принимающую строки и парсящую их по типам."""
    def wrapped(*args):
        if len(args) != len(types):
            raise ValueError(
                f"Ожидается {len(types)} аргумент(а), получено {len(args)}"
            )
        parsed = [parse_arg(a, t) for a, t in zip(args, types)]
        return func(*parsed)
    return wrapped


# ──────────────────────────────────────────────
# ЛЕКСЕР
# ──────────────────────────────────────────────

def tokenize(expr: str) -> list:
    """
    Разбивает строку на токены: числа, дроби, операторы, скобки.

    Примеры:
      '123 + 456'   → ['123', '+', '456']
      '3/4 * -1/2'  → ['3/4', '*', '-1/2']
      '(10 - 2) * 3' → ['(', '10', '-', '2', ')', '*', '3']
    """
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        # пробелы — пропускаем
        if ch.isspace():
            i += 1
            continue

        # скобки
        if ch in '()':
            tokens.append(ch)
            i += 1
            continue

        # операторы + и * — всегда бинарные
        if ch in '+*/':
            tokens.append(ch)
            i += 1
            continue

        # минус: унарный если в начале или после оператора/открывающей скобки
        if ch == '-':
            prev = tokens[-1] if tokens else None
            is_unary = prev is None or prev in ('+', '-', '*', '(')
            if is_unary:
                # читаем число вместе с минусом
                i += 1
                num = '-'
                while i < n and expr[i].isdigit():
                    num += expr[i]
                    i += 1
                # проверяем на дробь: -3/4
                if i < n and expr[i] == '/':
                    num += '/'
                    i += 1
                    while i < n and expr[i].isdigit():
                        num += expr[i]
                        i += 1
                if num == '-':
                    raise ValueError("Одиночный минус без числа")
                tokens.append(num)
            else:
                tokens.append('-')
                i += 1
            continue

        # число (целое или дробь)
        if ch.isdigit():
            num = ''
            while i < n and expr[i].isdigit():
                num += expr[i]
                i += 1
            # дробь только если / идёт СРАЗУ после цифры (без пробела)
            if i < n and expr[i] == '/' and (i + 1 < n and expr[i + 1].isdigit()):
                num += '/'
                i += 1
                while i < n and expr[i].isdigit():
                    num += expr[i]
                    i += 1
            tokens.append(num)
            continue
        raise ValueError(f"Недопустимый символ: '{ch}'")

    return tokens


# ──────────────────────────────────────────────
# ПАРСЕР ВЫРАЖЕНИЙ
# ──────────────────────────────────────────────

def apply_op(left: str, op: str, right: str) -> str:
    """Применяет операцию к двум строковым операндам, возвращает строку."""
    t_left  = detect_type(left)
    t_right = detect_type(right)

    # повышение типа: N < Z < Q
    rank = {"N": 0, "Z": 1, "Q": 2}
    t = t_left if rank.get(t_left, 0) >= rank.get(t_right, 0) else t_right

    # приводим оба операнда к нужному типу
    def promote(s, from_t, to_t):
        if from_t == to_t:
            return s
        if to_t == "Z":
            # N → Z: просто добавляем знак +
            return s  # parse_int справится с "123"
        if to_t == "Q":
            # N или Z → Q: добавляем знаменатель /1
            return s + "/1" if '/' not in s else s
        return s

    left  = promote(left,  t_left,  t)
    right = promote(right, t_right, t)

    ops = {
        "N": {'+': "ADD_NN_N", '-': "SUB_NN_N", '*': "MUL_NN_N"},
        "Z": {'+': "ADD_ZZ_Z", '-': "SUB_ZZ_Z", '*': "MUL_ZZ_Z"},
        "Q": {'+': "ADD_QQ_Q", '-': "SUB_QQ_Q", '*': "MUL_QQ_Q", '/': "DIV_QQ_Q"},
    }
    if op == '/':
        t = "Q"
        left  = promote(left,  t_left,  "Q")
        right = promote(right, t_right, "Q")

    if t not in ops:
        raise NotImplementedError(f"Выражения для типа '{t}' не поддерживаются")
    if op not in ops[t]:
        raise ValueError(f"Неизвестная операция: '{op}'")

    result = COMMANDS[ops[t][op]](left, right)
    return format_value(result)

def eval_parentheses(tokens: list) -> list:
    """
    Рекурсивно вычисляет скобочные подвыражения.
    Заменяет '(' ... ')' на результат вычисления содержимого.
    """
    while '(' in tokens:
        # находим последнюю открывающую скобку (самую глубокую)
        open_idx = None
        for i, tok in enumerate(tokens):
            if tok == '(':
                open_idx = i

        # находим соответствующую закрывающую скобку
        close_idx = None
        for i in range(open_idx + 1, len(tokens)):
            if tokens[i] == ')':
                close_idx = i
                break

        if close_idx is None:
            raise ValueError("Незакрытая скобка '('")

        # вычисляем подвыражение внутри скобок
        inner = tokens[open_idx + 1 : close_idx]
        result_tok = eval_flat(inner)

        # заменяем '(' ... ')' на результат
        tokens = tokens[:open_idx] + [result_tok] + tokens[close_idx + 1:]

    return tokens


def eval_flat(tokens: list) -> str:
    """
    Вычисляет плоский список токенов (без скобок) с учётом приоритета.
    Сначала *, потом + и -.
    Возвращает строку-результат.
    """
    if not tokens:
        raise ValueError("Пустое выражение")

    # шаг 1: свёртка умножения
    result = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '*' and result:
            left = result.pop()
            right = tokens[i + 1]
            result.append(apply_op(left, '*', right))
            i += 2
        else:
            result.append(tokens[i])
            i += 1
    tokens = result

    # шаг 2: свёртка сложения и вычитания
    acc = tokens[0]
    i = 1
    while i < len(tokens) - 1:
        op    = tokens[i]
        right = tokens[i + 1]
        acc   = apply_op(acc, op, right)
        i += 2

    return acc


def eval_expression(expr: str) -> str:
    """
    Точка входа для вычисления выражения.
    Поддерживает: +, -, *, скобки, натуральные/целые/рациональные числа.
    """
    tokens = tokenize(expr)
    if not tokens:
        raise ValueError("Пустое выражение")

    # проверяем баланс скобок
    depth = 0
    for tok in tokens:
        if tok == '(':   depth += 1
        elif tok == ')': depth -= 1
        if depth < 0:
            raise ValueError("Лишняя закрывающая скобка ')'")
    if depth != 0:
        raise ValueError("Незакрытая скобка '('")

    tokens = eval_parentheses(tokens)
    return eval_flat(tokens)


# ──────────────────────────────────────────────
# РЕГИСТРАЦИЯ КОМАНД
# ──────────────────────────────────────────────

def build_commands() -> dict:
    from natural import (
        COM_NN_D, NZER_N_B, ADD_1N_N, ADD_NN_N,
        SUB_NN_N, MUL_ND_N, MUL_Nk_N, MUL_NN_N,
        SUB_NDN_N, DIV_NN_Dk, DIV_NN_N, MOD_NN_N,
        GCF_NN_N, LCM_NN_N
    )
    from integer import (
        ABS_Z_N, POZ_Z_D, MUL_ZM_Z, TRANS_N_Z,
        TRANS_Z_N, ADD_ZZ_Z, SUB_ZZ_Z, MUL_ZZ_Z,
        DIV_ZZ_Z, MOD_ZZ_Z
    )
    from rational import (
        RED_Q_Q, INT_Q_B, TRANS_Z_Q, TRANS_Q_Z,
        ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q
    )

    return {
        # — Модуль N —
        "COM_NN_D":  wrap(COM_NN_D,  ["N", "N"]),
        "NZER_N_B":  wrap(NZER_N_B,  ["N"]),
        "ADD_1N_N":  wrap(ADD_1N_N,  ["N"]),
        "ADD_NN_N":  wrap(ADD_NN_N,  ["N", "N"]),
        "SUB_NN_N":  wrap(SUB_NN_N,  ["N", "N"]),
        "MUL_ND_N":  wrap(MUL_ND_N,  ["N", "int"]),
        "MUL_Nk_N":  wrap(MUL_Nk_N,  ["N", "int"]),
        "MUL_NN_N":  wrap(MUL_NN_N,  ["N", "N"]),
        "SUB_NDN_N": wrap(SUB_NDN_N, ["N", "int", "N"]),
        "DIV_NN_Dk": wrap(DIV_NN_Dk, ["N", "N", "int"]),
        "DIV_NN_N":  wrap(DIV_NN_N,  ["N", "N"]),
        "MOD_NN_N":  wrap(MOD_NN_N,  ["N", "N"]),
        "GCF_NN_N":  wrap(GCF_NN_N,  ["N", "N"]),
        "LCM_NN_N":  wrap(LCM_NN_N,  ["N", "N"]),
        # — Модуль Z —
        "ABS_Z_N":   wrap(ABS_Z_N,   ["Z"]),
        "POZ_Z_D":   wrap(POZ_Z_D,   ["Z"]),
        "MUL_ZM_Z":  wrap(MUL_ZM_Z,  ["Z"]),
        "TRANS_N_Z": wrap(TRANS_N_Z, ["N"]),
        "TRANS_Z_N": wrap(TRANS_Z_N, ["Z"]),
        "ADD_ZZ_Z":  wrap(ADD_ZZ_Z,  ["Z", "Z"]),
        "SUB_ZZ_Z":  wrap(SUB_ZZ_Z,  ["Z", "Z"]),
        "MUL_ZZ_Z":  wrap(MUL_ZZ_Z,  ["Z", "Z"]),
        "DIV_ZZ_Z":  wrap(DIV_ZZ_Z,  ["Z", "Z"]),
        "MOD_ZZ_Z":  wrap(MOD_ZZ_Z,  ["Z", "Z"]),
        # — Модуль Q —
        "RED_Q_Q":   wrap(RED_Q_Q,   ["Q"]),
        "INT_Q_B":   wrap(INT_Q_B,   ["Q"]),
        "TRANS_Z_Q": wrap(TRANS_Z_Q, ["Z"]),
        "TRANS_Q_Z": wrap(TRANS_Q_Z, ["Q"]),
        "ADD_QQ_Q":  wrap(ADD_QQ_Q,  ["Q", "Q"]),
        "SUB_QQ_Q":  wrap(SUB_QQ_Q,  ["Q", "Q"]),
        "MUL_QQ_Q":  wrap(MUL_QQ_Q,  ["Q", "Q"]),
        "DIV_QQ_Q":  wrap(DIV_QQ_Q,  ["Q", "Q"]),
    }


# ──────────────────────────────────────────────
# DISPATCH И REPL
# ──────────────────────────────────────────────

def dispatch(cmd: str, args: list):
    if cmd not in COMMANDS:
        raise NotImplementedError(f"Команда '{cmd}' не найдена. Введите 'help'.")
    return COMMANDS[cmd](*args)


def repl():
    print(HELP)
    while True:
        try:
            line = input("cas> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not line:
            continue
        if line.lower() in ("exit", "quit", "q"):
            print("Выход.")
            break
        if line.lower() == "help":
            print(HELP)
            continue

        try:
            parts = line.split()
            cmd = parts[0].upper()

            if cmd in COMMANDS:
                # Режим команды: ADD_NN_N 123 456
                result = dispatch(cmd, parts[1:])
                print("  =", format_value(result))
            else:
                # Режим выражения: (100 - 20) * 3
                result = eval_expression(line)
                print("  =", result)

        except NotImplementedError as e:
            print(f"  [!] {e}")
        except ValueError as e:
            print(f"  [!] Ошибка ввода: {e}")
        except Exception as e:
            print(f"  [!] Ошибка: {e}")


# ──────────────────────────────────────────────
# ТОЧКА ВХОДА
# ──────────────────────────────────────────────

COMMANDS = build_commands()

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print(HELP)
    else:
        repl()
