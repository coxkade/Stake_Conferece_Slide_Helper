from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

def rgb_shift(val):
    ''' Change 0-256 Rgb Value to a number between 0 and 1 '''
    return val/255.0

class SlideTextBox(TextInput):
    def __init__(self, **kwargs):
        TextInput.__init__(self, **kwargs)

    def __Get_Parrent_Window_Size(self):
        rv = {}
        rv["height"] = App.get_running_app().layout.height
        rv["width"] = App.get_running_app().layout.width
        return rv

    def __Set_Padding(self):
        box_width = self.width
        max_size = max(self._lines_rects, key=lambda r: r.size[0]).size
        left_pad = (box_width - max_size[0])/2
        self.padding_x = [left_pad, left_pad]
        top_pad = (self.height - max_size[1])/2
        self.padding_y = [top_pad, top_pad]

    def make_text_invisible(self):
        self.background_color = (0, 0, 0, 0)
        self.foreground_color = (1, 1, 1, 0)

    def make_text_visible(self):
        self.background_color = (0, 0, 0, 1)
        self.foreground_color = (1, 1, 1, 1)

    def set_text(self,text):
        W_Ratio = 0.8
        T_Ratio = 0.05
        if(0 == len(text)):
            self.make_text_invisible()
        else:
            window_size = self.__Get_Parrent_Window_Size()
            box_width = window_size["width"]*W_Ratio
            box_height = 150
            box_position_x = (window_size["width"] - box_width)/2
            box_position_y = window_size["height"] - window_size["height"]*T_Ratio - box_height
            self.text = text
            self.size = (box_width, box_height)
            self.pos = (box_position_x, box_position_y)
            self.__Set_Padding()
            self.make_text_visible()
            

class SlideLayout(FloatLayout):
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.slide_num -= 1
            self.__update_text()
        elif keycode[1] == 'right':
            self.slide_num += 1
            self.__update_text()
        elif keycode[1] == 'up':
            self.slide_num += 1
            self.__update_text()
        elif keycode[1] == 'spacebar':
            self.slide_num += 1
            self.__update_text()
        elif keycode[1] == 'down':
            self.slide_num -= 1
            self.__update_text()
        return True

    def __update_text(self):
        text = "Slide Num is Now: {}".format(self.slide_num)
        print(text)
        print(self.ids)
        if 0 == self.slide_num:
            self.ids.slidetext.set_text('')
        else:
            self.ids.slidetext.set_text(text)

    def __init__(self, **kwargs):
        # self.background_color_set = False
        FloatLayout.__init__(self, **kwargs)
        self.slide_num = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def do_layout(self, *largs, **kwargs):
        # if False == self.background_color_set:
        #     for gitem in self.ids.main_Canvas.canvas.get_group('background'):
        #         if isinstance(gitem, Color):
        #             gitem.rgba = (0, 0, 0, 1)
        #             self.background_color_set = True
        FloatLayout.do_layout(self, *largs, **kwargs)


class SongSlide(App):
    def build(self):
        self.layout = SlideLayout()
        return self.layout
    
    def run(self):
        print("SongSlide Run")
        App.run(self)

    def on_start(self, **kwargs):
        print("SongSlide on Start")
        App.on_start(self, **kwargs)

if __name__ == "__main__":
    Window.clearcolor = (rgb_shift(0), rgb_shift(71), rgb_shift(187), 1)
    print("Creating the Application")
    Main_Object = SongSlide()
    print("Running the Application")
    Main_Object.run()
    print("Got Passed the Run")