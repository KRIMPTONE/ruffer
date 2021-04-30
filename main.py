# Создание и запуск приложения, программирование интерфейса экранов и действий на них

# Здесь должен быть твой код
# готовый ThirsScr
#я хз что писвть
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView

from scrollLabel import *
from instructions import *
from seconds import *
from sits import *
from runner import *
from ruffier import * 


age = 20
name = ''
pulse1 = 0
pulse2 = 0
pulse3 = 0


def get_result():
    res = test(pulse1, pulse2, pulse3, age)
    return name + '\n' + res[0] + '\n' + res[1]

class MainScr(Screen):
    def __init__(self, name = 'main'):
        super().__init__(name=name)

        scroll_text = ScrollLabel(txt_instruction)

        name_lab = Label(text='Ваша имя: ')
        self.name_value = TextInput(text='', multiline = False)

        age_lab = Label(text='Ваш возраст: ')
        self.age_value = TextInput(text='0', multiline = False)

        btn_next = Button(text='Вперёд',size_hint=(1,0.1))
        btn_next.on_press = self.next

        hor_layout1 = BoxLayout(size_hint=(1,0.1))
        hor_layout1.add_widget(name_lab)
        hor_layout1.add_widget(self.name_value)   

        hor_layout2 = BoxLayout(size_hint=(1,0.1))
        hor_layout2.add_widget(age_lab)
        hor_layout2.add_widget(self.age_value)  

        ver_layout = BoxLayout(orientation='vertical')
        ver_layout.add_widget(scroll_text)
        ver_layout.add_widget(hor_layout1)
        ver_layout.add_widget(hor_layout2)
        ver_layout.add_widget(btn_next)

        self.add_widget(ver_layout)

    def next(self):
        global name, age
        name = self.name_value.text
        age = int(self.age_value.text)
        print(age)
        self.manager.current = 'first'


class FirstScr(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name)

        self.next_screen = False
        instr1 = ScrollLabel(txt_test1)
        instr2 = ScrollLabel('Считайте пульт')

        self.sec = Seconds(15)
        self.sec.bind(done = self.sec_finished)

        res_label = Label(text='Введите результат: ')
        self.res_value = TextInput(text='0')
        self.res_value.set_disabled(True)

        self.but = Button(text='Начать', size_hint=(1,0.2))
        self.but.background_color = (0,0.9,0.5,1)
        self.but.on_press = self.next

        hor = BoxLayout(size_hint=(1,0.2))
        hor.add_widget(res_label)
        hor.add_widget(self.res_value)

        ver = BoxLayout(orientation = "vertical")

        ver.add_widget(instr1)
        ver.add_widget(instr2)
        ver.add_widget(self.sec)
        ver.add_widget(hor)
        ver.add_widget(self.but)

        self.add_widget(ver)

    def sec_finished(self, *args):
        self.but.set_disabled(False)
        self.but.text = 'Продолжить'
        self.res_value.set_disabled(False)
        self.next_screen = True

    def next(self):
        if self.next_screen == False:
            self.but.set_disabled(True)
            self.sec.start()
        else:
            global pulse1
            pulse1 = int(self.res_value.text)
            self.manager.current = 'second'


class SecondScr(Screen):
    def __init__(self, name='second'):
        super().__init__(name=name)

        self.next_screen = False

        instr = ScrollLabel(txt_sits,size_hint=(1,0.1))

        self.sits_value = Sits(30,size_hint=(1,0.1))
        self.run = Runner(total=30, steptime=1.5)
        self.run.bind(finished = self.run_finished)

        self.but = Button(text='Начать',size_hint=(1,0.1))
        self.but.on_press = self.next

        ver = BoxLayout(orientation = 'vertical')
        ver.add_widget(instr)
        ver.add_widget(self.sits_value)
        ver.add_widget(self.run)
        ver.add_widget(self.but)

        self.add_widget(ver)

    def next(self):
        if self.next_screen == False:
            self.but.set_disabled(True)
            self.run.start()
            self.run.bind(value = self.sits_value.next)
        else:
            self.manager.current = 'third'
    
    def run_finished(self, *args):
        self.next_screen = True
        self.but.text = 'Продолжить'
        self.but.set_disabled(False)
   

class ThirdScr(Screen):
    def __init__(self, name='third'):
        super().__init__(name=name)
        self.next_screen = False
        self.stage = 0
        instr1 = ScrollLabel(txt_test3)
        self.instr2 = ScrollLabel('Считайте пульс')
        self.sec = Seconds(15)
        self.sec.bind(done = self.sec_finished)

        res1_label = Label(text='Результат:')
        self.res1_value = TextInput(text='0')
        self.res1_value.set_disabled(True)

        res2_label = Label(text='Результат после отдыха:')
        self.res2_value = TextInput(text='0')
        self.res2_value.set_disabled(True)

        self.but = Button(text='Начать',size_hint=(1,0.2))
        self.but.on_press = self.next

        hor1 = BoxLayout(size_hint=(1,0.2))
        hor1.add_widget(res1_label)
        hor1.add_widget(self.res1_value)

        hor2 = BoxLayout(size_hint=(1,0.2))
        hor2.add_widget(res2_label)
        hor2.add_widget(self.res2_value)

        ver = BoxLayout(orientation = 'vertical')
        ver.add_widget(instr1)
        ver.add_widget(self.instr2)
        ver.add_widget(self.sec)
        ver.add_widget(hor1)
        ver.add_widget(hor2)
        ver.add_widget(self.but)

        self.add_widget(ver)

        
    def sec_finished(self, instance, value):
        if value:
            self.stage += 1
            if self.stage == 1:
                self.instr2.set_text('Отдыхайте')
                self.sec.restart(30)
                self.res1_value.set_disabled(False)
            elif self.stage == 2:
                self.instr2.set_text('Считайте пульт')
                self.sec.restart(15)
            elif self.stage == 3:
                self.res2_value.set_disabled(False)
                self.but.text = 'Завершить'
                self.but.set_disabled(False)
                self.next_screen = True

    def next(self):
        if self.next_screen == False:
            self.but.set_disabled(True)
            self.sec.start()
        else:
            global pulse2, pulse3
            pulse2 = int(self.res1_value.text)
            pulse3 = int(self.res2_value.text)
            self.manager.current = 'fourth'

class FourthScr(Screen):
    def __init__(self, name='fourth'):
        super().__init__(name=name)

        ver = BoxLayout(orientation='vertical', padding=8, spacing=8)

        self.instr = ScrollLabel('')
        
        ver.add_widget(self.instr)

        self.add_widget(ver)
        self.on_enter = self.before
    
    
    def before(self):
        self.instr.set_text(get_result())

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScr(name='main'))
        sm.add_widget(FirstScr(name='first'))
        sm.add_widget(SecondScr(name='second'))
        sm.add_widget(ThirdScr(name='third'))
        sm.add_widget(FourthScr(name='fourth'))

        return sm

MyApp().run()
