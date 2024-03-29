import tkinter as tk
from tkinter import Scrollbar
from tkinter import messagebox

import sys
import os
config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(config_dir)

from services.language_dict import Language
from config.firebase import Firebase

class History(tk.Tk):
    def __init__(self, automation_name:str, automation_developer:str, automation_requester:str, language:str):
        super().__init__()
        self.language = Language(language)
        self.automation_name = automation_name
        self.automation_developer = automation_developer
        self.automation_requester = automation_requester
        self.title(self.automation_name)
        self.geometry("500x500")
        self.result = False

        fire = Firebase()
        datas = fire.get_realtime(self.automation_name)

        if datas == None:
            messagebox.showinfo(title=self.language.search('history_automation_title'), message=self.language.search('history_automation_body'))
            self.destroy()
        else:
            self.executions = self.language.search('history_executed')
            for data in datas:
                self.executions = f"{self.executions}{datas[data]['quantidade']} {self.language.search('history_executed_in')} {str(datas[data]['horaExec']).split('.')[0]}\n"

            self.components_styles()
            self.components_position()
    
    # Declare the components styles
    def components_styles(self):
        self.title_label = tk.Label(self, text=f"{self.language.search('history_for_user').replace('$automation_name',self.automation_name)}", font=("Helvetica", 15, "bold"), wraplength=500)
        
        self.text_frame = tk.Frame(self)
        self.text_scroll = Scrollbar(self.text_frame, orient="vertical")
        self.text_field = tk.Text(self.text_frame, height=20, width=50, yscrollcommand=self.text_scroll.set)

        self.automation_credits = tk.Label(self, text=f"{self.automation_name}, {self.language.search('requested')} {self.automation_requester} {self.language.search('developed')} {self.automation_developer}", wraplength=500, font=("Helvetica", 12, 'bold'), fg='#0078D7')

    # Put the components into the Application interface
    def components_position(self):
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")

        self.text_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.text_scroll.pack(side="right", fill="y")
        self.text_field.pack(side="left", fill="both", expand=True)
        self.text_scroll.config(command=self.text_field.yview)
        self.text_field.insert("1.0", self.executions)

        self.automation_credits.pack(pady=5, side="bottom")

if __name__ == "__main__":
    app = History('Python Default Script','Robert Aron Zimmermann','Robert Aron Zimmermann','EN')
    app.mainloop()
