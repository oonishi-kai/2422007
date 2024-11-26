import flet as ft
import math

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text

class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE

class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE

class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK

class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.is_initial_state = True  # 初期状態フラグを設定
        self.width = 700
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="(", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text=")", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="e", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="x²", button_clicked=self.button_clicked
                        ),
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="sin", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="x³", button_clicked=self.button_clicked
                        ),
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="cos", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="xʸ", button_clicked=self.button_clicked
                        ),
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="tan", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="π", button_clicked=self.button_clicked
                        ),
                        DigitButton(text="0", button_clicked=self.button_clicked, expand=2),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked)
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        text = e.control.data
        
        if self.is_initial_state and text not in "+-*/%.)":
            self.result.value = text
            self.is_initial_state = False
        else:
            if text in "0123456789":
                self.result.value += text
            elif text == "AC":
                self.result.value = "0"
                self.is_initial_state = True  # リセット後、次の入力を初期状態とする
            elif text == ".":
                if "." not in self.result.value:
                    self.result.value += "."
            elif text == "+/-":
                if self.result.value.startswith("-"):
                    self.result.value = self.result.value[1:]
                else:
                    self.result.value = "-" + self.result.value
            elif text == "%":
                self.result.value = str(float(self.result.value) / 100)
            elif text == "e" or text == "π":
                if self.result.value == "0":
                    self.result.value = text
                else:
                    self.result.value += text
            elif text in "+-*/":
                self.result.value += text
            elif text == "x²":
                if self.result.value != "0":
                    self.result.value = str(float(self.result.value) ** 2)
            elif text == "x³":
                if self.result.value != "0":
                    self.result.value = str(float(self.result.value) ** 3)
            elif text == "xʸ":
                self.result.value += "**"
            elif text == "sin":
                self.result.value = str(math.sin(float(self.result.value)))
            elif text == "cos":
                self.result.value = str(math.cos(float(self.result.value)))
            elif text == "tan":
                self.result.value = str(math.tan(float(self.result.value)))
            elif text == "(":
                self.result.value += "("
            elif text == ")":
                self.result.value += ")"
            elif text == "=":
                try:
                    # π と e を適切な値に置き換える
                    expression = self.result.value.replace('π', str(math.pi)).replace('e', str(math.e))
                    self.result.value = str(eval(expression))
                    self.is_initial_state = True  # 結果表示後、次の入力を初期状態とする
                except Exception as e:
                    self.result.value = "Error"

        self.update()

    def reset(self):
        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.is_initial_state = True  # 最初の入力へのリセット


def main(page: ft.Page):
    page.title = "Calculator"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    calc = CalculatorApp()
    page.add(calc)


ft.app(main)