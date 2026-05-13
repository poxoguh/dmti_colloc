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
import readline
import traceback

from typing import List, Tuple

# ──────────────────────────────────────────────
# ОПРЕДЕЛЕНИЕ ТИПОВ (для IDE и читаемости)
# ──────────────────────────────────────────────
Natural = Tuple[int, List[int]]
Integer = Tuple[int, int, List[int]]
Rational = Tuple[Integer, Natural]
Polynomial = Tuple[int, List[Rational]] 

HELP = """
╔══════════════════════════════════════════════════════════╗
║********** CAS — Система компьютерной алгебры ************║
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
  DIV_NN_DK <a> <b> <k>    первая цифра деления
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

Модуль P — Многочлены с рациональными коэффициентами (формат: 3/2*x^2 + x - 1/4)
  ADD_PP_P   <a>  <b>        сложение многочленов
  SUB_PP_P   <a>  <b>        вычитание
  MUL_PQ_P   <a>  <q>        умножение на рациональное число
  MUL_PXK_P  <a>  <k>        умножение на x^k (k >= 0)
  LED_P_Q    <a>            старший коэффициент
  DEG_P_N    <a>            степень многочлена
  FAC_P_Q    <a>            контент (НОД коэффициентов)
  MUL_PP_P   <a>  <b>        умножение многочленов
  DIV_PP_P   <a>  <b>        частное от деления
  MOD_PP_P   <a>  <b>        остаток от деления
  GCF_PP_P   <a>  <b>        НОД многочленов
  DER_P_P    <a>            производная
  NMR_P_P    <a>            удаление кратных корней

Введите 'help' для справки, 'exit' для выхода.
"""
# ──────────────────────────────────────────────
# ПАРСИНГ АРГУМЕНТОВ
# ──────────────────────────────────────────────
def parse_nat(s: str) -> Natural:
    s = s.strip()
    if not s.isdigit(): raise ValueError(f"Натуральное: '{s}'")
    digits = [int(c) for c in reversed(s)]
    while len(digits) > 1 and digits[-1] == 0: digits.pop()
    return (len(digits) - 1, digits)

def parse_int(s: str) -> Integer:
    s = s.strip()
    sign = 1 if s.startswith('-') else 0
    nat = parse_nat(s.lstrip('+-'))
    n, digits = nat
    if n == 0 and digits == [0]: sign = 0
    return (sign, n, digits)

def parse_rat(s: str) -> Rational:
    s = s.strip()
    if '/' not in s:
        return (parse_int(s), parse_nat('1'))
    num_str, den_str = s.split('/', 1)
    if not den_str.isdigit() or den_str == '0':
        raise ValueError(f"Некорректный знаменатель: '{den_str}'")
    return (parse_int(num_str), parse_nat(den_str))

def parse_poly(s: str) -> Polynomial:
    s = s.strip().replace(' ', '')
    if s == '0': return (-1, [])
    if not s.startswith('+') and not s.startswith('-'): s = '+' + s
    
    terms = re.findall(r'[+-][^+-]+', s)
    zero_r = (parse_int('0'), parse_nat('1'))
    coeffs = {}
    max_deg = -1
    
    for term in terms:
        if not term: continue
        if 'x' not in term:
            deg, coef_str = 0, term
        elif '^' in term:
            base, exp = term.split('^', 1)
            deg = int(exp) # Здесь может быть ошибка, если exp не int (напр. 7/2)
            coef_str = base.replace('*', '').replace('x', '')
        else:
            deg = 1
            coef_str = term.replace('x', '').replace('*', '')
            
        if coef_str in ('', '+', '+1'): coef_str = '1'
        if coef_str in ('-', '-1'): coef_str = '-1'
        
        max_deg = max(max_deg, deg)
        coeffs[deg] = parse_rat(coef_str)
        
    C = [coeffs.get(i, zero_r) for i in range(max_deg + 1)]
    while max_deg >= 0 and C[max_deg] == zero_r: max_deg -= 1
    return (-1, []) if max_deg < 0 else (max_deg, C[:max_deg + 1])

def parse_arg(arg: str, typ: str):
    if typ == "N":   return parse_nat(arg)
    if typ == "Z":   return parse_int(arg)
    if typ == "Q":   return parse_rat(arg)
    if typ == "P":   return parse_poly(arg) 
    if typ == "int": return int(arg)
    raise ValueError(f"Неизвестный тип: '{typ}'")

def detect_type(s: str) -> str:
    if 'x' in s or '^' in s: return "P"
    if '/' in s: return "Q"
    if re.match(r'^-\d+$', s): return "Z"
    if re.match(r'^\d+$', s): return "N"
    raise ValueError(f"Тип: '{s}'")

# ──────────────────────────────────────────────
# ФОРМАТИРОВАНИЕ
# ──────────────────────────────────────────────
def format_nat(a) -> str: return ''.join(str(d) for d in reversed(a[1])) or '0'
def format_int(a) -> str:
    s = ''.join(str(d) for d in reversed(a[2])) or '0'
    return ('-' + s) if (a[0] == 1 and s != '0') else s
def format_rat(a) -> str:
    n, d = format_int(a[0]), format_nat(a[1])
    return f"{n}/{d}" if d != '1' else n

def format_poly(p: Polynomial) -> str:
    m, C = p
    if m < 0: return '0'
    zero_r = (parse_int('0'), parse_nat('1'))
    terms = []
    for i in range(m, -1, -1):
        c = C[i]
        if c == zero_r: continue
        coef = format_rat(c)
        if i > 0:
            if coef == '1': coef = ''
            elif coef == '-1': coef = '-'
        terms.append(f"{coef}x" if i == 1 else (coef if i == 0 else f"{coef}x^{i}"))
    res = '+'.join(terms).replace('+-', '-').strip('+')
    return res if res else '0'

def format_value(x) -> str:
    if not isinstance(x, tuple): return str(x)
    if len(x) == 2 and isinstance(x[0], int) and isinstance(x[1], list) and len(x[1]) > 0 and isinstance(x[1][0], tuple):
        return format_poly(x)
    if len(x) == 2 and isinstance(x[1], list): return format_nat(x)
    if len(x) == 3 and isinstance(x[2], list): return format_int(x)
    if len(x) == 2 and isinstance(x[0], tuple) and isinstance(x[1], tuple): return format_rat(x)
    return str(x)

# ──────────────────────────────────────────────
# ОБЁРТКА И ЛЕКСЕР
# ──────────────────────────────────────────────
def wrap(func, types: list):
    def wrapped(*args):
        if len(args) != len(types):
            raise ValueError(f"Ожидается {len(types)} аргумент(а), получено {len(args)}")
        return func(*[parse_arg(a, t) for a, t in zip(args, types)])
    return wrapped

def tokenize(expr: str) -> list:
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        if ch.isspace(): i += 1; continue
        if ch in '()+*/': tokens.append(ch); i += 1; continue
        
        # Обработка минуса (унарный или бинарный)
        if ch == '-':
            prev = tokens[-1] if tokens else None
            if prev is None or prev in ('+', '-', '*', '('):
                # Унарный минус: читаем всё слово целиком
                i += 1; token = '-'
                while i < n and expr[i] not in '+*/()' and not expr[i].isspace():
                    token += expr[i]; i += 1
                if token == '-': raise ValueError("Одиночный минус")
                tokens.append(token)
            else:
                tokens.append('-'); i += 1
            continue
            
        # Чтение числа или многочлена (слово)
        if ch.isdigit() or ch == 'x':
            token = ''
            while i < n and expr[i] not in '+*/()' and not expr[i].isspace():
                token += expr[i]; i += 1
            if token: tokens.append(token)
            continue
            
        raise ValueError(f"Символ: '{ch}'")
    return tokens

def apply_op(left: str, op: str, right: str) -> str:
    t_left, t_right = detect_type(left), detect_type(right)
    # P (многочлены) имеют приоритет выше всех
    rank = {"N": 0, "Z": 1, "Q": 2, "P": 3}
    t = t_left if rank.get(t_left, 0) >= rank.get(t_right, 0) else t_right

    def promote(s, from_t, to_t):
        if from_t == to_t: return s
        if to_t == "Z": return s
        if to_t == "Q": return s + "/1" if '/' not in s else s
        if to_t == "P": return s  # parse_poly("1") работает корректно
        return s

    l, r = promote(left, t_left, t), promote(right, t_right, t)
    ops = {
        "N": {'+': "ADD_NN_N", '-': "SUB_NN_N", '*': "MUL_NN_N"},
        "Z": {'+': "ADD_ZZ_Z", '-': "SUB_ZZ_Z", '*': "MUL_ZZ_Z"},
        "Q": {'+': "ADD_QQ_Q", '-': "SUB_QQ_Q", '*': "MUL_QQ_Q", '/': "DIV_QQ_Q"},
        "P": {'+': "ADD_PP_P", '-': "SUB_PP_P", '*': "MUL_PP_P", '/': "DIV_PP_P"},
    }
    if op == '/': t = "Q" if t != "P" else "P"; l, r = promote(left, t_left, t), promote(right, t_right, t)
    
    if t not in ops or op not in ops[t]: raise NotImplementedError(f"Операция '{op}' для '{t}'")
    return format_value(COMMANDS[ops[t][op]](l, r))

def eval_parentheses(tokens: list) -> list:
    while '(' in tokens:
        o = next(i for i, t in enumerate(tokens) if t == '(')
        c = next(i for i in range(o+1, len(tokens)) if tokens[i] == ')')
        tokens = tokens[:o] + [eval_flat(tokens[o+1:c])] + tokens[c+1:]
    return tokens

def eval_flat(tokens: list) -> str:
    """
    Вычисляет плоский список токенов (без скобок) с учётом приоритета.
    Сначала * и /, потом + и -.
    Возвращает строку-результат.
    """
    if not tokens:
        raise ValueError("Пустое выражение")

    # шаг 1: свёртка умножения и деления (одинаковый приоритет)
    result = []
    i = 0
    while i < len(tokens):
        if tokens[i] in ('*', '/') and result:
            left = result.pop()
            right = tokens[i + 1]
            result.append(apply_op(left, tokens[i], right))
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
    tokens = tokenize(expr)
    if not tokens: raise ValueError("Пустое выражение")
    depth = 0
    for t in tokens:
        if t == '(': depth += 1
        elif t == ')': depth -= 1
        if depth < 0: raise ValueError("Лишняя ')'")
    if depth != 0: raise ValueError("Незакрытая '('")
    return eval_flat(eval_parentheses(tokens))

# ──────────────────────────────────────────────
# РЕГИСТРАЦИЯ
# ──────────────────────────────────────────────
def build_commands() -> dict:
    from natural import (COM_NN_D, NZER_N_B, ADD_1N_N, ADD_NN_N, SUB_NN_N, MUL_ND_N, MUL_NK_N, MUL_NN_N, SUB_NDN_N, DIV_NN_DK, DIV_NN_N, MOD_NN_N, GCF_NN_N, LCM_NN_N)
    from integer import (ABS_Z_N, POZ_Z_D, MUL_ZM_Z, TRANS_N_Z, TRANS_Z_N, ADD_ZZ_Z, SUB_ZZ_Z, MUL_ZZ_Z, DIV_ZZ_Z, MOD_ZZ_Z)
    from rational import (RED_Q_Q, INT_Q_B, TRANS_Z_Q, TRANS_Q_Z, ADD_QQ_Q, SUB_QQ_Q, MUL_QQ_Q, DIV_QQ_Q)
    from polynomial import (ADD_PP_P, SUB_PP_P, MUL_PQ_P, MUL_PXK_P, LED_P_Q, DEG_P_N, FAC_P_Q, MUL_PP_P, DIV_PP_P, MOD_PP_P, GCF_PP_P, DER_P_P, NMR_P_P)

    return {
        "COM_NN_D": wrap(COM_NN_D, ["N", "N"]), "NZER_N_B": wrap(NZER_N_B, ["N"]), "ADD_1N_N": wrap(ADD_1N_N, ["N"]),
        "ADD_NN_N": wrap(ADD_NN_N, ["N", "N"]), "SUB_NN_N": wrap(SUB_NN_N, ["N", "N"]), "MUL_ND_N": wrap(MUL_ND_N, ["N", "int"]),
        "MUL_Nk_N": wrap(MUL_NK_N, ["N", "int"]), "MUL_NN_N": wrap(MUL_NN_N, ["N", "N"]), "SUB_NDN_N": wrap(SUB_NDN_N, ["N", "int", "N"]),
        "DIV_NN_Dk": wrap(DIV_NN_DK, ["N", "N", "int"]), "DIV_NN_N": wrap(DIV_NN_N, ["N", "N"]), "MOD_NN_N": wrap(MOD_NN_N, ["N", "N"]),
        "GCF_NN_N": wrap(GCF_NN_N, ["N", "N"]), "LCM_NN_N": wrap(LCM_NN_N, ["N", "N"]),
        "ABS_Z_N": wrap(ABS_Z_N, ["Z"]), "POZ_Z_D": wrap(POZ_Z_D, ["Z"]), "MUL_ZM_Z": wrap(MUL_ZM_Z, ["Z"]),
        "TRANS_N_Z": wrap(TRANS_N_Z, ["N"]), "TRANS_Z_N": wrap(TRANS_Z_N, ["Z"]), "ADD_ZZ_Z": wrap(ADD_ZZ_Z, ["Z", "Z"]),
        "SUB_ZZ_Z": wrap(SUB_ZZ_Z, ["Z", "Z"]), "MUL_ZZ_Z": wrap(MUL_ZZ_Z, ["Z", "Z"]), "DIV_ZZ_Z": wrap(DIV_ZZ_Z, ["Z", "Z"]),
        "MOD_ZZ_Z": wrap(MOD_ZZ_Z, ["Z", "Z"]), "RED_Q_Q": wrap(RED_Q_Q, ["Q"]), "INT_Q_B": wrap(INT_Q_B, ["Q"]),
        "TRANS_Z_Q": wrap(TRANS_Z_Q, ["Z"]), "TRANS_Q_Z": wrap(TRANS_Q_Z, ["Q"]), "ADD_QQ_Q": wrap(ADD_QQ_Q, ["Q", "Q"]),
        "SUB_QQ_Q": wrap(SUB_QQ_Q, ["Q", "Q"]), "MUL_QQ_Q": wrap(MUL_QQ_Q, ["Q", "Q"]), "DIV_QQ_Q": wrap(DIV_QQ_Q, ["Q", "Q"]),
        "ADD_PP_P": wrap(ADD_PP_P, ["P", "P"]), "SUB_PP_P": wrap(SUB_PP_P, ["P", "P"]), "MUL_PQ_P": wrap(MUL_PQ_P, ["P", "Q"]),
        "MUL_PXK_P": wrap(MUL_PXK_P, ["P", "int"]), "LED_P_Q": wrap(LED_P_Q, ["P"]), "DEG_P_N": wrap(DEG_P_N, ["P"]),
        "FAC_P_Q": wrap(FAC_P_Q, ["P"]), "MUL_PP_P": wrap(MUL_PP_P, ["P", "P"]), "DIV_PP_P": wrap(DIV_PP_P, ["P", "P"]),
        "MOD_PP_P": wrap(MOD_PP_P, ["P", "P"]), "GCF_PP_P": wrap(GCF_PP_P, ["P", "P"]), "DER_P_P": wrap(DER_P_P, ["P"]),
        "NMR_P_P": wrap(NMR_P_P, ["P"])
    }

COMMANDS = build_commands()

def dispatch(cmd: str, args: list):
    if cmd not in COMMANDS: raise NotImplementedError(f"Команда '{cmd}' не найдена.")
    return COMMANDS[cmd](*args)

def repl():
    print(HELP)
    cmd_list = list(COMMANDS.keys())
    def completer(text, state):
        buffer = readline.get_line_buffer()
        if ' ' not in buffer:
            matches = [c for c in cmd_list if c.startswith(text.upper())]
            try: return matches[state]
            except IndexError: return None
        return None
    readline.set_completer(completer)
    readline.set_completer_delims(' ')
    readline.parse_and_bind('tab: complete')

    while True:
        try: line = input("cas> ").strip()
        except (EOFError, KeyboardInterrupt): print("\nВыход."); break
        if not line: continue
        if line.lower() in ("exit", "quit", "q"): print("Выход."); break
        if line.lower() == "help": print(HELP); continue
        try:
            parts = line.split()
            cmd = parts[0].upper()
            
            one_poly_cmds = {"LED_P_Q", "DEG_P_N", "FAC_P_Q", "DER_P_P", "NMR_P_P"}
            # Если команда с 1 аргументом-полиномом, склеиваем аргументы с пробелами
            args = ["".join(parts[1:])] if cmd in one_poly_cmds and len(parts) > 1 else parts[1:]
            
            if cmd in COMMANDS:
                print("  =", format_value(dispatch(cmd, args)))
            else:
                print("  =", eval_expression(line))
        except Exception as e:
            print(f"  [!] Ошибка: {e}")
            # traceback.print_exc()

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv: print(HELP)
    else: repl()