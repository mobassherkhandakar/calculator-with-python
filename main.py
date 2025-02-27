from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
import math
import datetime
import random

class CalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []
        self.memory = 0
        self.dark_mode = False
        self.scientific_mode = False
        self.angle_mode = 'deg'
        self.build_ui()
    
    def build_ui(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        self.display = TextInput(font_size=32, readonly=True, halign='right', size_hint=(1, 0.2))
        self.layout.add_widget(self.display)
        
        self.menu_bar = DropDown()
        options = {
            'History': (self.show_history, './icons/history.png'),
            'Dark Mode': (self.toggle_dark_mode, './icons/dark_mode.png'),
            'Scientific Mode': (self.toggle_scientific_mode, './icons/science.png'),
            'Toggle Angle Mode': (self.toggle_angle_mode, './icons/angle.png'),
            'Age Calculator': (self.calculate_age, './icons/age.png'),
            'Currency Converter': (self.convert_currency, './icons/currency.png'),
            'Temperature Converter': (self.convert_temperature, './icons/temperature.png'),
            'Settings': (self.open_settings, './icons/settings.png')
        }
        for label, (func, icon) in options.items():
            btn = Button(text=label, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn, f=func: (f(None), self.menu_bar.dismiss()))
            self.menu_bar.add_widget(btn)
        
        self.menu_btn = Button(text='☰', size_hint=(None, None), size=(150, 60), pos_hint={'right': 1, 'top': 1})
        self.menu_btn.bind(on_release=self.menu_bar.open)
        self.layout.add_widget(self.menu_btn)
        
        self.buttons_layout = GridLayout(cols=4, spacing=2, size_hint=(1, 0.7))
        self.normal_buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+',
            '⌫'
        ]
        self.scientific_buttons = ['sin', 'cos', 'tan', 'log', '√', 'x²', '(', ')', 'exp', 'π', 'e', '!', '^', '%', 'Rand', 'MC', 'MR', 'M+', 'M-']
        
        self.button_widgets = []
        self.add_buttons(self.normal_buttons)
        self.layout.add_widget(self.buttons_layout)
        self.update_theme()
        self.add_widget(self.layout)
    
    def add_buttons(self, buttons):
        self.buttons_layout.clear_widgets()
        for label in buttons:
            button = Button(text=label, font_size=24)
            button.bind(on_press=self.on_button_press)
            self.style_button(button, label)
            self.button_widgets.append(button)
            self.buttons_layout.add_widget(button)
    
    def style_button(self, button, label):
        if label in ['/', '*', '-', '+']: 
            button.background_color = (0.2, 0.6, 0.8, 1)
        elif label == 'C':
            button.background_color = (0.9, 0.1, 0.1, 1)
        elif label == '⌫':
            button.background_color = (0.8, 0.8, 0, 1)
        else:
            button.background_color = (0.9, 0.9, 0.9, 1)
    
    def on_button_press(self, instance):
        text = instance.text
        try:
            if text == 'C':
                self.display.text = ''
            elif text == '⌫':
                self.display.text = self.display.text[:-1]
            elif text == '=':
                result = str(eval(self.display.text))
                self.history.append(self.display.text + ' = ' + result)
                self.display.text = result
            elif text == '√':
                self.display.text = str(math.sqrt(float(self.display.text)))
            elif text == 'x²':
                self.display.text = str(float(self.display.text) ** 2)
            elif text == '!':
                self.display.text = str(math.factorial(int(self.display.text)))
            elif text == '^':
                self.display.text += '**'
            elif text == '%':
                self.display.text += '%'
            elif text == 'Rand':
                self.display.text = str(random.random())
            elif text == 'MC':
                self.memory = 0
            elif text == 'MR':
                self.display.text += str(self.memory)
            elif text == 'M+':
                self.memory += float(self.display.text or 0)
            elif text == 'M-':
                self.memory -= float(self.display.text or 0)
            else:
                self.display.text += text
        except:
            self.display.text = 'Error'
    
    def toggle_scientific_mode(self, instance):
        self.scientific_mode = not self.scientific_mode
        self.button_widgets.clear()
        if self.scientific_mode:
            self.add_buttons(self.normal_buttons + self.scientific_buttons)
        else:
            self.add_buttons(self.normal_buttons)

    def toggle_angle_mode(self, instance):
        self.angle_mode = 'rad' if self.angle_mode == 'deg' else 'deg'
        self.display.text = f'Angle Mode: {self.angle_mode}'

    def show_history(self, instance):
        content = '\n'.join(self.history) if self.history else 'No History'
        popup = Popup(title='History', content=Label(text=content), size_hint=(0.8, 0.8))
        popup.open()
    
    def toggle_dark_mode(self, instance):
        self.dark_mode = not self.dark_mode
        self.update_theme()

    def update_theme(self):
        bg_color = (0, 0, 0, 1) if self.dark_mode else (1, 1, 1, 1)
        fg_color = (1, 1, 1, 1) if self.dark_mode else (0, 0, 0, 1)
        for button in self.button_widgets:
            button.color = fg_color
        self.display.background_color = bg_color
        self.display.foreground_color = fg_color

    def calculate_age(self, instance):
        try:
            birth_year = int(self.display.text)
            current_year = datetime.datetime.now().year
            age = current_year - birth_year
            self.display.text = f'Age: {age}'
        except:
            self.display.text = 'Invalid Input'

    def convert_currency(self, instance):
        try:
            amount = float(self.display.text)
            converted = amount * 110
            self.display.text = f'Converted: {converted} BDT'
        except:
            self.display.text = 'Invalid Input'

    def convert_temperature(self, instance):
        try:
            temp = float(self.display.text)
            converted = (temp * 9/5) + 32
            self.display.text = f'{converted} °F'
        except:
            self.display.text = 'Invalid Input'

    def open_settings(self, instance):
        content = BoxLayout(orientation='vertical')
        dark_mode_switch = Button(text='Toggle Dark Mode')
        dark_mode_switch.bind(on_press=self.toggle_dark_mode)
        content.add_widget(dark_mode_switch)
        scientific_mode_switch = Button(text='Toggle Scientific Mode')
        scientific_mode_switch.bind(on_press=self.toggle_scientific_mode)
        content.add_widget(scientific_mode_switch)
        popup = Popup(title='Settings', content=content, size_hint=(0.8, 0.8))
        popup.open()

class ScientificCalculatorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorScreen(name='calculator'))
        return sm

if __name__ == '__main__':
    ScientificCalculatorApp().run()
