from kivy.lang import Builder
from kivymd.app import MDApp, App
from kivymd.uix.pickers import MDDatePicker
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivymd.uix.list import OneLineListItem
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.behaviors import ButtonBehavior, TouchRippleBehavior
from kivymd.uix.behaviors import CircularRippleBehavior, ScaleBehavior
from kivy.clock import Clock
from datetime import datetime
import calendar

kv = '''
#: import Window kivy.core.window.Window

<CustomLabel>:
    halign:'center'
    canvas.after:
        Color:
            rgba:app.theme_cls.primary_color
        Line:
            rectangle:[*self.pos, *self.size]
<TextIconButton>:
    size_hint:(None,None)
    width:dp(120)
    height:dp(38)
    
    canvas.after:
        Color:
            rgba:app.theme_cls.primary_color
        Line:
            width:1
            rectangle:[*self.pos, *self.size]
    MDLabel:
        text:root.text
        size_hint_y:None
        height:self.parent.height
        
    MDIcon:
        icon:root.icon
        size_hint_y:None
        font_size:dp(36)
        height:self.parent.height+dp(8)
<WeekDayLabels>:
                
                
MDScreen:
   
    MDRelativeLayout:
        MDIcon:
            icon:'menu'
            font_size:self.parent.children[1].height-dp(20)
            pos_hint:{'top':0.98, 'center_x':0.1}
        MDDropDownItem:
            on_release:app.show_years(self)
            id:year_label
            pos_hint:{'top':0.985, 'center_x':0.3}
        MDDropDownItem:
            on_release:app.show_months(self)
            id:month_label
            pos_hint:{'top':0.985, 'center_x':0.5}
            
    CalendarView:
        pos_hint:{'top':0.9}
        orientation:'vertical'
        WeekDayLabels:
            size_hint_y:None
            height:dp(56)
        CalendarLayout:
            size_hint_y:None
            height:dp(500)
            cols:7
            id:calendar_layout
            canvas.after:
                Color:
                    rgba:app.theme_cls.primary_color
                Line:
                    width:1
                    rectangle:[*self.pos,*self.size]
        Widget:
    
    MDBottomSheet:    
        type:'standard'
        size_hint_y:None
        height:Window.size[1]
        id:bottom_sheet
        MDBottomSheetDragHandle:
            on_touch_move:app.move_bottomsheet(*args)
            drag_handle_color:[0,0,0,0.5]
            md_bg_color:app.theme_cls.primary_color
            radius:[dp(25),dp(25),0,0]
            MDBottomSheetDragHandleTitle:
                id:bottom_title
                text:'Events'
                adaptive_height:True
                bold:True
                font_size:dp(36)
                pos_hint:{'center_x':0.5}
            MDBottomSheetDragHandleButton:
                on_release: app.close_bottomsheet()
                icon:'close'
                theme_text_color:'Custom'
                text_color:[0,0,0,0.5]
        
        MDBottomSheetContent:
            size_hint_y:None
            height:Window.size[1]
            MDScrollView:
                MDList:
                    id:event_list
    MDFloatingActionButton:
        icon:'pencil'
        pos_hint:{'right':0.9, 'top':0.15}
        on_release:app.show_date_picker()
                    
            
    
    
            
        
    
'''
def get_month_name(month_int):
    return calendar.month_name[month_int]
    
def get_day_name(year, month, day_int):
    if day_int > 0:
        date = datetime(year, month, day_int)
        day_name = date.strftime('%a')
        return day_name
    else:
        return 'Not a day in this month'
def check_if_today( year, month, day):
    if day == 0:
        return False
    else:
        today = datetime.today()
        if today.year == year and today.month == month and today.day == day:
            return True
        else:
            return False
    

class CustomLabel(CircularRippleBehavior, ButtonBehavior, MDLabel):
    today = BooleanProperty(False)
    year = NumericProperty()
    month = NumericProperty()
    day = NumericProperty()
    event_list = ListProperty(['Happy Birthay','Mashujaa Day'])
    
    def on_today(self, instance, value):
        Clock.schedule_once(self.update, 1/10)
    def on_release(self, *args):
        app = App.get_running_app()
        Clock.schedule_once(self.show_selection, 1/10)
        app.open_bottomsheet(self)
    def show_selection(self, interval):
        app = App.get_running_app()
        with self.canvas.before:
            Color(rgba=app.theme_cls.primary_dark)
            Rectangle(pos=self.pos,size=self.size)
         
    
        
    def update(self, interval):
        app = App.get_running_app()
        if self.today:
            with self.canvas.before:
                Color(rgba=app.theme_cls.primary_color)
                Line(
                    width=1.8,
                    rectangle=[*self.pos,*self.size]
                )
                    
                Ellipse(
                pos=(self.pos[0]+(self.width*0.336), self.pos[1]+(self.height*0.35)),
                size=(self.size[0]*0.35,self.size[0]*0.35)
                )
                    

class WeekDayLabels(ScaleBehavior, MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        days = calendar.Calendar().iterweekdays()
        for day in days:
            self.add_widget(CustomLabel(
            text=calendar.day_name[day][0].upper(),                                
            ))
            
class TextIconButton(TouchRippleBehavior, ButtonBehavior, MDBoxLayout):
    text = StringProperty('January')
    icon = StringProperty('menu-down')
    
class CalendarView(MDBoxLayout):
    pass
    
class CalendarLayout(MDGridLayout):
    _today = datetime.today()
    year = NumericProperty(_today.year-1)
    month = NumericProperty(_today.month)
    def on_year(self, instance, value):
        Clock.schedule_once(self.update_layout, 0.2)
        
    def on_month(self, instance, value):
        Clock.schedule_once(self.update_layout, 0.2)
        
    def update_layout(self, interval):
        self.update_calendar_layout(self.year, self.month)
        
    def update_calendar_layout(self, year,month):
        app = App.get_running_app()
        dates_of_month = calendar.Calendar().itermonthdays(year, month)
        app.root.ids.month_label.text = calendar.month_name[month]
        app.root.ids.year_label.text =str(year)
        if self.children[:]:
            self.clear_widgets()
        for date in dates_of_month:
            self.add_widget(CustomLabel(text=str(date) if not date==0 else '', 
                                            year=year,
                                            month=month,
                                            day=date,
                                            today=check_if_today(year, month, date)))
    
    
class CalendarApp(MDApp):
    prev_pos = ListProperty([0,0])
    def build(self):
        return Builder.load_string(kv)
    def on_start(self):
        month_name = list(calendar.month_name)
        self.menu_items = [{  'viewclass':'OneLineListItem',
                                            'text':str(i),
                                            'on_release':lambda x=f'{i}':self.set_month(x)
                                        } for i in month_name]
                                        
        self.root.ids.calendar_layout.year = 2024
        self.year_items = [{  'viewclass':'OneLineListItem',
                                            'text':str(i),
                                            'on_release':lambda x=f'{i}':self.set_year(x)
                                        } for i in range(1990,2030)]
    def show_months(self, instance):
       self.menu = MDDropdownMenu(
                       items=self.menu_items,
                       width_mult=4  )  
       self.menu.caller = instance
       self.menu.open()
    def show_years(self, instance):
        self.menu_year = MDDropdownMenu(
                                           items=self.year_items,
                                           width_mult=3
       )
        self.menu_year.caller = instance
        self.menu_year.open()
       
    def set_year(self, year):
       self.root.ids.calendar_layout.year = int(year)
       self.menu_year.dismiss()
       
       
    def set_month(self, name):
        months = list(calendar.month_name)
        self.root.ids.calendar_layout.month = months.index(name)
        self.menu.dismiss()
        
    def open_bottomsheet(self, instance):
        event_list = instance.event_list
        event_container = self.root.ids.event_list
        event_container.clear_widgets()
        handle_title = self.root.ids.bottom_title
        handle_title.font_size = 34
        handle_title.text = 'Today'if check_if_today(instance.year, instance.month, instance.day) else f'{instance.day} {get_day_name(instance.year, instance.month, instance.day)}, {get_month_name(instance.month)} {instance.year} '
        
        for event in event_list:
            event_container.add_widget(OneLineListItem(text=str(event)))
        self.bottomsheet = self.root.ids.bottom_sheet
        
        self.bottomsheet.open()
    def close_bottomsheet(self):
        self.bottomsheet.dismiss()
        
    def move_bottomsheet(self, instance, touch):
       bottom_sheet = self.root.ids.bottom_sheet
       current_pos = (touch.ox,touch.oy)
       delta = current_pos[1]-self.prev_pos[1]
       print(delta)
       self.prev_pos = (touch.px,touch.py)
       s = (touch.dx,touch.dy)
       
       
       if delta < 1:
           if instance.collide_point(*touch.pos):
               self.root.ids.bottom_sheet.pos = (bottom_sheet.pos[0], bottom_sheet.pos[1]+s[0]+15)
               
       else:
           
            if instance.collide_point(*touch.pos):
               self.root.ids.bottom_sheet.pos = (bottom_sheet.pos[0], bottom_sheet.pos[1]-s[0]-25)
               
       
    
  
    
    def save_date(self, *args):
        print(args)
    def cancel_date(self, *args):
        print(args)
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_date, on_cance=self.cancel_date)
        date_dialog.open()
        
if __name__ == '__main__':
        CalendarApp().run()
        