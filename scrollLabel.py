# Модуль с классом-наследником ScrollView для создания инструкции, у которой при необходимости включается полоса прокрутки

# Здесь должен быть твой код
# Модуль с классом-наследником ScrollView для создания инструкции, у которой при необходимости включается полоса прокрутки

# Здесь должен быть твой код

from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

class ScrollLabel(ScrollView):
    def __init__(self, ltext, **kwargs):
        super().__init__(**kwargs)

        t = '[color=#FFFFFF]'+ltext+'[/color]'
        self.label = Label(text=t, markup=True,
        size_hint_y=None, font_size='18sp',
        halign='left', valign='top')

        self.add_widget(self.label)

        self.label.bind(size=self.resize)

    def resize(self, *args):
        self.label.text_size = (self.label.width, None)
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]
    
    def set_text(self,ltext):
        ftext = '[color=#FFFFFF]'+ ltext +'[/color]'
        self.label.text = ftext
        self.resize()