
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config
import pymorphy2
import re

import config.tables as vTable
import config.functions as vFunc

morph = pymorphy2.MorphAnalyzer()

Config.set("graphics", "width", 300)
Config.set("graphics", "height", 100)

class Morphology(App):

    def atext(self, text):
        self.label.text += text

    def writeout(self, table):
        self.atext(", ".join(table) + "; \n")

    def __button_event__(self, instance):
        if len(self.input.text) > 0 and self.input.text.isalpha() and vFunc.is_russian(self.input.text):
            v = morph.parse(self.input.text.lower())[0]
            vall, vnever = [], []
            self.label.text = "Разбор слова \"" + str(self.input.text.lower()) + "\" ( " + vTable.pos[v.tag.POS] + " )\n"
            if v.tag.POS == "NOUN":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Именительный падеж, Единственное число\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, 
                    vFunc.cmain(v.tag), 
                    vTable.anim[v.tag.animacy], 
                    vTable.gender[v.tag.gender] + " род"
                )
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                vFunc.rappend(vnever, 
                    vTable.number[v.tag.number], 
                    vTable.case[v.tag.case]
                )
                self.writeout(vnever)
            elif v.tag.POS == "ADJF" or v.tag.POS == "ADJS":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Именительный падеж, Единственное число, Мужской род\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, getpril(v.tag))
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                if getpril(v.tag) == "Качественное":
                    vFunc.rappend(vnever, 
                        vFunc.getprilpart(v.tag.POS),
                        vFunc.checkprilstep(v),
                        vTable.number[v.tag.number] + " число",
                        vTable.gender[tofirstnumber(v).tag.gender] + " род",
                        vTable.case[tofullform(v).tag.case] + " падеж"
                    )
                else:
                    vFunc.rappend(vnever, 
                        vTable.number[v.tag.number] + " число",
                        vTable.gender[tofirstnumber(v).tag.gender] + " род",
                        vFunc.checkexistedcase(v)
                    )
                self.writeout(vnever)
            elif v.tag.POS == "NUMR":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Именительный падеж\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, 
                    vFunc.getnumbertype(v.tag),
                    vFunc.sobirnumber(v.tag),
                    "Простое"
                )
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                vFunc.rappend(vnever, 
                    vTable.case[v.tag.case] + " падеж",
                    vFunc.checknumber(v.tag),
                    vFunc.checkgender(v.tag)
                )
                self.writeout(vnever)
            elif v.tag.POS == "NPRO":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Именительный падеж\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, vFunc.getrazr(v.tag))
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                vFunc.rappend(vnever, 
                    vFunc.checknumber(v.tag),
                    vFunc.checkgender(v.tag),
                    vTable.case[v.tag.case] + " падеж"
                )
                self.writeout(vnever)
            elif v.tag.POS == "VERB" or v.tag.POS == "INFN":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Именительный падеж\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, 
                    vFunc.vozvglag(v.tag),
                    vTable.sov[v.tag.aspect] + " вид",
                    "Спряжение неизвестно",
                    vTable.perexod[v.tag.transitivity]
                )
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                if v.tag.mood != None:
                    vFunc.rappend(vnever, 
                        vTable.mood[v.tag.mood] + " наклонение"
                    )
                    if v.tag.mood == 'indc':
                        vFunc.rappend(vnever, 
                            vTable.dtime[v.tag.tense] + " время",
                            vTable.number[v.tag.number] + " число"
                        )
                        if v.tag.tense == "pres" or v.tag.tense == "futr":
                            vFunc.rappend(vnever, v.tag.person[:1] + " лицо")
                        if v.tag.tense == "past":
                            vFunc.rappend(vnever, vFunc.checkgender(v.tag))
                    elif v.tag.mood == 'impr':
                        vFunc.rappend(vnever, vTable.number[v.tag.number] + " число")
                    else:
                        vFunc.rappend(vnever, vTable.number[v.tag.number] + " число")
                        if vFunc.tofirstnumber(v).tag != None and vFunc.tofirstnumber(v).tag.gender != None:
                            vFunc.rappend(vnever, vTable.gender[tofirstnumber(v).tag.gender] + " род")
                else:
                    vFunc.rappend(vnever, "Нет")
                self.writeout(vnever)
            elif v.tag.POS == "PRTF" or v.tag.POS == "PRTS":
                self.atext("Начальная форма: ( " + str(v.normal_form) + " ) - Полное, Мужской род, Единственное число, Именительный падеж\n")
                self.atext("Образовано от глагола " + str(v.normal_form) + "\n")
                self.atext("Постоянные признаки:\n")
                vFunc.rappend(vall, 
                    vFunc.vozvglag(v.tag),
                    vTable.pvoice[v.tag.voice] + " залог",
                    vTable.sov[v.tag.aspect] + " вид",
                    vTable.dtime[v.tag.tense] + " время"
                )
                self.writeout(vall)
                self.atext("Непостоянные признаки:\n")
                vFunc.rappend(vnever, "Полное" if v.tag.POS == "PRTF" else "Краткое" if v.tag.POS == "PRTS" else "Неизвестно")
                vFunc.rappend(vnever, 
                    vTable.number[v.tag.number] + " число",
                    vTable.gender[vFunc.tofirstnumber(v).tag.gender] + " род"
                )
                if v.tag.POS == "PRTF":
                    vFunc.rappend(vnever, vTable.case[tofullform(v).tag.case] + " падеж")
                self.writeout(vnever)
            elif v.tag.POS == "GRND":
                self.atext("Образовано от слова - " + str(v.normal_form) + "\n")
                self.atext("Морфологические признаки:\n")
                vFunc.rappend(vall, 
                    vTable.sov[v.tag.aspect] + " вид",
                    vFunc.vozvglag(v.tag)
                )
                self.writeout(vall)
            elif v.tag.POS == "ADVB":
                self.atext("Морфологические признаки:\n")
                vFunc.rappend(vall, 
                    vFunc.unchanched(v.tag),
                    vFunc.getrazrdouble(v.tag) + " разряд(а)",
                    vFunc.checkprilstep(v)
                )
                self.writeout(vall)
            elif v.tag.POS == "PRCL":
                self.atext("Разряд: " + vFunc.getrazr(v.tag))
        else:
            self.label.text = "Слово имеет некорректное содержание"

    def build(self):
        sone = BoxLayout(size_hint_y=8)
        stwo = BoxLayout(size_hint_y=92)
        grid = GridLayout(cols=1)
        self.input = TextInput(
            text='Write word here', 
            size_hint=(.1, .90), 
            pos_hint={'top':1},
            multiline=False,
            font_size=25
        )
        button = Button(
            text="Разобрать", 
            size_hint=(.1, .90), 
            pos_hint={'top':1},
            on_press=self.__button_event__,
            font_size=20,
            background_color=(0,1,0,1)
        )
        self.label = Label(text="Результат будет находиться здесь", pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=19)
        self.label.bind(text_size=self.label.setter("size"))
        sone.add_widget(self.input)
        sone.add_widget(button)
        stwo.add_widget(self.label)
        grid.add_widget(sone)
        grid.add_widget(stwo)
        return grid

if __name__ == "__main__":
    Morphology().run()
