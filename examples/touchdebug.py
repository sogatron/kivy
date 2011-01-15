from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Point
from random import random
from math import sqrt

def calculate_points(x1, y1, x2, y2, steps=2):
    dx = x2 - x1
    dy = y2 - y1
    dist = sqrt(dx * dx + dy * dy)
    if dist < steps:
        return None
    o = []
    m = dist / steps
    for i in xrange(int(m)):
        mi = i / m
        o.extend([x1 + dx * mi, y1 + dy * mi])
    return o


class Touchdebug(Widget):
    def on_touch_down(self, touch):
        win = self.get_parent_window()
        ud = touch.userdata
        ud['group'] = g = str(touch.uid)
        with self.canvas:
            ud['color'] = Color(random(), 1, 1, mode='hsv', group=g)
            ud['lines'] = (
                Rectangle(pos=(touch.x, 0), size=(1, win.height), group=g),
                Rectangle(pos=(0, touch.y), size=(win.width, 1), group=g),
                Point(points=(touch.x, touch.y), source='particle.png',
                      pointsize=5, group=g)
            )

        ud['label'] = Label()
        self.update_touch_label(ud['label'], touch)
        self.add_widget(ud['label'])
        ud['oldtouch'] = touch.x, touch.y

    def on_touch_move(self, touch):
        ud = touch.userdata
        ud['lines'][0].pos = touch.x, 0
        ud['lines'][1].pos = 0, touch.y

        oldx, oldy = ud['oldtouch']
        points = calculate_points(oldx, oldy, touch.x, touch.y)
        if points:
            ud['oldtouch'] = touch.x, touch.y
            ud['lines'][2].points = ud['lines'][2].points + points
        ud['label'].pos = touch.pos
        self.update_touch_label(ud['label'], touch)

    def on_touch_up(self, touch):
        ud = touch.userdata
        self.canvas.remove_group(ud['group'])
        self.remove_widget(ud['label'])

    def update_touch_label(self, label, touch):
        label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (
            touch.id,
            touch.x,
            touch.y,
            touch.__class__.__name__
        )
        label.pos = touch.pos
        label.size = label.texture_size[0] + 20, label.texture_size[1] + 20


class TouchdebugApp(App):
    def build(self):
        return Touchdebug()

if __name__ == '__main__':
    TouchdebugApp().run()