import tkinter as tk
from tkinter import ttk, scrolledtext
import pprint
import traceback

# Пытаемся импортировать рабочую логику из вашего main.py
try:
    from main import dispatch, eval_expression, format_value, COMMANDS, HELP
except ImportError as e:
    print(f"Критическая ошибка: Не удалось импортировать модули из main.py.\n{e}")
    print("Убедитесь, что gui.py находится в одной папке с main.py")
    exit(1)

class CasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CAS — Система компьютерной алгебры (GUI)")
        self.root.geometry("1050x700")
        self.root.minsize(900, 500)
        
        self._setup_styles()
        self._build_ui()
        self._populate_commands_tree()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=6, font=('Segoe UI', 10))
        style.configure("Treeview", font=('Segoe UI', 10), rowheight=25)
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'))

    def _build_ui(self):
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ЛЕВАЯ ПАНЕЛЬ: Консоль и ввод
        left_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=3)

        self.console = scrolledtext.ScrolledText(
            left_frame, wrap=tk.WORD, font=('Consolas', 11), bg="#1e1e1e", fg="#d4d4d4"
        )
        self.console.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.console.config(state=tk.DISABLED)

        # Теги для текста
        self.console.tag_config("input", foreground="#569cd6", font=('Consolas', 11, 'bold'))
        self.console.tag_config("output", foreground="#4af626", font=('Consolas', 12, 'bold'))
        self.console.tag_config("error", foreground="#f44747")
        self.console.tag_config("info", foreground="#ce9178")
        self.console.tag_config("debug", foreground="#8a8a8a", font=('Consolas', 10, 'italic'))

        # Панель ввода
        input_frame = ttk.Frame(left_frame)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="cas>", font=('Consolas', 12, 'bold')).pack(side=tk.LEFT, padx=(0, 5))
        
        self.entry = ttk.Entry(input_frame, font=('Consolas', 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.execute_command)
        self.entry.focus()

        btn_exec = ttk.Button(input_frame, text="Выполнить", command=self.execute_command)
        btn_exec.pack(side=tk.LEFT, padx=(0, 5))

        btn_clear = ttk.Button(input_frame, text="Очистить", command=self.clear_console)
        btn_clear.pack(side=tk.LEFT, padx=(0, 5))

        # ГАЛОЧКА: Подробный вид
        self.show_hood_var = tk.BooleanVar(value=True)
        chk_hood = ttk.Checkbutton(input_frame, text="Подробный вид", variable=self.show_hood_var)
        chk_hood.pack(side=tk.LEFT, padx=(10, 0))

        # ПРАВАЯ ПАНЕЛЬ: Дерево команд
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=1)

        ttk.Label(right_frame, text="Справочник функций", font=('Segoe UI', 11, 'bold')).pack(pady=(0, 5))
        self.tree = ttk.Treeview(right_frame, columns=("desc",), show="tree", selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

        self.print_to_console("=== CAS: Система компьютерной алгебры ===", "info")
        self.print_to_console("Графическая оболочка запущена.\n", "info")

    def _populate_commands_tree(self):
        categories = {
            "N": ("Натуральные числа", ["COM_NN_D", "NZER_N_B", "ADD_1N_N", "ADD_NN_N", "SUB_NN_N", "MUL_ND_N", "MUL_Nk_N", "MUL_NN_N", "SUB_NDN_N", "DIV_NN_Dk", "DIV_NN_N", "MOD_NN_N", "GCF_NN_N", "LCM_NN_N"]),
            "Z": ("Целые числа", ["ABS_Z_N", "POZ_Z_D", "MUL_ZM_Z", "TRANS_N_Z", "TRANS_Z_N", "ADD_ZZ_Z", "SUB_ZZ_Z", "MUL_ZZ_Z", "DIV_ZZ_Z", "MOD_ZZ_Z"]),
            "Q": ("Рациональные числа", ["RED_Q_Q", "INT_Q_B", "TRANS_Z_Q", "TRANS_Q_Z", "ADD_QQ_Q", "SUB_QQ_Q", "MUL_QQ_Q", "DIV_QQ_Q"]),
            "P": ("Многочлены", ["ADD_PP_P", "SUB_PP_P", "MUL_PQ_P", "MUL_Pxk_P", "LED_P_Q", "DEG_P_N", "FAC_P_Q", "MUL_PP_P", "DIV_PP_P", "MOD_PP_P", "GCF_PP_P", "DER_P_P", "NMR_P_P"])
        }
        for cat_id, (cat_name, cmds) in categories.items():
            parent = self.tree.insert("", tk.END, text=f"Модуль {cat_id}: {cat_name}", open=False)
            for cmd in cmds:
                self.tree.insert(parent, tk.END, text=cmd)

    def print_to_console(self, text, tag=None):
        self.console.config(state=tk.NORMAL)
        if tag:
            self.console.insert(tk.END, text + "\n", tag)
        else:
            self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    def clear_console(self):
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)

    def on_tree_double_click(self, event):
        item_id = self.tree.selection()[0]
        item_text = self.tree.item(item_id, "text")
        if "Модуль" in item_text: return
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{item_text} ")
        self.entry.focus()
        self.entry.icursor(tk.END)

    def _parse_string_to_structure(self, s):
        """Интерпретирует строковый результат ручных выражений для генерации подробного вида"""
        s = s.strip()
        
        # 1. Если это многочлен (содержит переменную x)
        if 'x' in s:
            try:
                import re
                clean_s = s.replace(" ", "")
                # Разбиваем строку на отдельные одночлены с сохранением знаков
                tokens = re.findall(r'[+-]?[^+-]+', clean_s)
                
                poly_dict = {}
                for token in tokens:
                    if not token: continue
                    sign = 1
                    if token.startswith('-'):
                        sign = -1
                        token = token[1:]
                    elif token.startswith('+'):
                        token = token[1:]
                    
                    # Извлекаем степень x
                    if 'x^' in token:
                        parts = token.split('x^')
                        coef_str = parts[0]
                        deg = int(parts[1])
                    elif 'x' in token:
                        parts = token.split('x')
                        coef_str = parts[0]
                        deg = 1
                    else:
                        coef_str = token
                        deg = 0
                        
                    # Извлекаем значение коэффициента
                    if not coef_str:
                        coef_val = (sign * 1, 1)
                    else:
                        if '/' in coef_str:
                            num_s, den_s = coef_str.split('/')
                            coef_val = (sign * int(num_s), int(den_s))
                        else:
                            coef_val = (sign * int(coef_str), 1)
                    poly_dict[deg] = coef_val

                if poly_dict:
                    max_deg = max(poly_dict.keys())
                    lines = [f"  [ПОДРОБНЫЙ ВИД: Многочлен (Polynomial)]", 
                             f"  ├─ Степень (m): {max_deg}", 
                             f"  ├─ Коэффициенты (C):"]
                    
                    # Итерируемся по всем степеням от 0 до max_deg (восстанавливая нулевые коэффициенты)
                    for d in range(max_deg + 1):
                        num, den = poly_dict.get(d, (0, 1))
                        
                        # Преобразуем числитель во внутреннюю структуру Integer
                        is_neg = 1 if num < 0 else 0
                        abs_num = abs(num)
                        num_digits = [int(c) for c in reversed(str(abs_num))]
                        num_tuple = (is_neg, len(num_digits) - 1, num_digits)
                        
                        # Преобразуем знаменатель во внутреннюю структуру Natural
                        den_digits = [int(c) for c in reversed(str(den))]
                        den_tuple = (len(den_digits) - 1, den_digits)
                        
                        lines.append(f"  │   x^{d} -> ({num_tuple}, {den_tuple})")
                        
                    lines.append(f"  └─ Текстовый вид: {s}")
                    return "\n".join(lines)
            except Exception:
                pass

            return (f"  [ПОДРОБНЫЙ ВИД: Многочлен (Polynomial)]\n"
                    f"  └─ Текстовый вид    : {s}")

        # 2. Если это дробь (Rational)
        if '/' in s:
            try:
                parts = s.split('/')
                if len(parts) == 2:
                    num_part = parts[0].strip()
                    den_part = parts[1].strip()
                    
                    is_neg = num_part.startswith('-')
                    num_digits_str = num_part.lstrip('-+')
                    num_A = [int(c) for c in reversed(num_digits_str)]
                    num_tuple = (1 if is_neg else 0, len(num_A) - 1, num_A)
                    
                    den_A = [int(c) for c in reversed(den_part)]
                    den_tuple = (len(den_A) - 1, den_A)
                    
                    return (f"  [ПОДРОБНЫЙ ВИД: Рациональная дробь (Rational)]\n"
                            f"  ├─ Числитель (Integer)  : {num_tuple}\n"
                            f"  ├─ Знаменатель (Natural): {den_tuple}\n"
                            f"  └─ Кортеж в памяти      : ({num_tuple}, {den_tuple})")
            except Exception:
                pass

        # 3. Если это обычное число (Natural / Integer)
        try:
            clean_s = s.lstrip('-+')
            if clean_s.isdigit():
                is_neg = s.startswith('-')
                A = [int(c) for c in reversed(clean_s)]
                n = len(A) - 1
                
                if is_neg:
                    return (f"  [ПОДРОБНЫЙ ВИД: Целое число (Integer)]\n"
                            f"  ├─ Знак (sign)       : Отрицательное (1)\n"
                            f"  ├─ Старший индекс (n): {n}\n"
                            f"  ├─ Массив цифр (A)   : {A} (младшие разряды слева)\n"
                            f"  └─ Кортеж в памяти      : (1, {n}, {A})")
                else:
                    return (f"  [ПОДРОБНЫЙ ВИД: Натуральное/Целое число (Natural/Integer)]\n"
                            f"  ├─ Старший индекс (n): {n}\n"
                            f"  ├─ Массив цифр (A)   : {A} (младшие разряды слева)\n"
                            f"  ├─ Как тип Natural   : ({n}, {A})\n"
                            f"  └─ Как тип Integer   : (0, {n}, {A})")
        except Exception:
            pass

        return f"  [ПОДРОБНЫЙ ВИД: Выражение]\n  └─ Значение: {s}"

    def _analyze_structure(self, val):
        """Анализирует сырой кортеж (из прямых функций) и возвращает подробное описание"""
        if isinstance(val, str):
            return self._parse_string_to_structure(val)

        if not isinstance(val, tuple):
            return "  [Данные]:\n  " + pprint.pformat(val).replace("\n", "\n  ")
        
        try:
            # Натуральное число -> (int, list)
            if len(val) == 2 and isinstance(val[0], int) and isinstance(val[1], list) and (not val[1] or isinstance(val[1][0], int)):
                return (f"  [ПОДРОБНЫЙ ВИД: Натуральное число (Natural)]\n"
                        f"  ├─ Старший индекс (n): {val[0]}\n"
                        f"  ├─ Массив цифр (A)   : {val[1]} (младшие разряды слева)\n"
                        f"  └─ Исходный кортеж   : {val}")

            # Целое число -> (int, int, list)
            if len(val) == 3 and isinstance(val[0], int) and isinstance(val[1], int) and isinstance(val[2], list):
                sign = "Отрицательное (1)" if val[0] == 1 else "Положительное/Ноль (0)"
                return (f"  [ПОДРОБНЫЙ ВИД: Целое число (Integer)]\n"
                        f"  ├─ Знак (sign)       : {sign}\n"
                        f"  ├─ Старший индекс (n): {val[1]}\n"
                        f"  ├─ Массив цифр (A)   : {val[2]} (младшие разряды слева)\n"
                        f"  └─ Исходный кортеж   : {val}")

            # Рациональная дробь -> ((sign, n, A), (n, A))
            if len(val) == 2 and isinstance(val[0], tuple) and len(val[0]) == 3 and isinstance(val[1], tuple) and len(val[1]) == 2:
                return (f"  [ПОДРОБНЫЙ ВИД: Рациональная дробь (Rational)]\n"
                        f"  ├─ Числитель (Integer)  : {val[0]}\n"
                        f"  ├─ Знаменатель (Natural): {val[1]}\n"
                        f"  └─ Исходный кортеж      : {val}")

            # Многочлен -> (int, list)
            if len(val) == 2 and isinstance(val[0], int) and isinstance(val[1], list) and (val[1] and isinstance(val[1][0], tuple)):
                lines = [f"  [ПОДРОБНЫЙ ВИД: Многочлен (Polynomial)]", 
                         f"  ├─ Степень (m): {val[0]}", 
                         f"  ├─ Коэффициенты (C):"]
                for i, coef in enumerate(val[1]):
                    lines.append(f"  │   x^{i} -> {coef}")
                lines.append(f"  └─ Исходный кортеж: {val}")
                return "\n".join(lines)
                
        except Exception:
            pass

        return "  [Данные]:\n  " + pprint.pformat(val).replace("\n", "\n  ")

    def execute_command(self, event=None):
        line = self.entry.get().strip()
        if not line: return
        self.entry.delete(0, tk.END)
        self.print_to_console(f"cas> {line}", "input")

        if line.lower() in ("exit", "quit", "q"):
            self.root.quit()
            return
        if line.lower() == "help":
            self.print_to_console(HELP, "info")
            return

        try:
            parts = line.split()
            cmd = parts[0].upper()
            one_poly_cmds = {"LED_P_Q", "DEG_P_N", "FAC_P_Q", "DER_P_P", "NMR_P_P"}
            args = ["".join(parts[1:])] if cmd in one_poly_cmds and len(parts) > 1 else parts[1:]
            
            result = None
            if cmd in COMMANDS:
                result = dispatch(cmd, args)
                self.print_to_console(f"  = {format_value(result)}", "output")
            else:
                result = eval_expression(line)
                if isinstance(result, str):
                    self.print_to_console(f"  = {result}", "output")
                else:
                    self.print_to_console(f"  = {format_value(result)}", "output")

            # Вывод Подробного вида (теперь динамически строит дерево и для строковых полиномов)
            if self.show_hood_var.get() and result is not None:
                debug_info = self._analyze_structure(result)
                self.print_to_console(debug_info, "debug")
                
        except Exception as e:
            self.print_to_console(f"Ошибка: {e}", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = CasGUI(root)
    root.mainloop()