import tkinter as tk
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OrderDisplayApp:
    def __init__(self, root):
        if not os.path.exists("Chat"):
            os.makedirs("Chat")
        
        self.root = root
        self.root.title("A-POS Chat Screen")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.scale_factor = min(screen_width / 1920, screen_height / 1080)

        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#FDFDFD")
        self.header_color = "#FDFDFD"
        self.primary_font_color = "#000000"

        self.font = 'Space Mono'
        self.create_widgets()
        self.setup_order_watcher()

    def scale(self, value):
        return int(value * self.scale_factor)
    
    def create_widgets(self):
        self.header_frame = tk.Frame(self.root, bg=self.header_color, height=self.scale(120))
        self.header_frame.pack(fill=tk.X)

        self.operator = tk.Label(self.header_frame, text="🍹 Real-Time Transcription Chat", 
                                   font=(self.font, self.scale(26), "bold"),
                                   fg=self.primary_font_color,bg=self.header_color)
        
        self.operator.pack(side=tk.LEFT, padx=self.scale(20), pady=self.scale(15))


        # -------------------------------------------Body------------------------------------------------------
        content_frame = tk.Frame(self.root, bg="#374151")
        content_frame.pack(fill=tk.BOTH, expand=True)
        content_frame.pack_propagate(False)

        # -------------------------------------------Upper------------------------------------------------------
        self.primary_font_color_2 = '#FFFFFF'
        half = 400
        mid = 860
        upper_color = "#0062FF"
        ai = tk.Frame(content_frame, bg=upper_color, height=self.scale(half))
        ai.pack(side=tk.TOP, fill=tk.X)
        ai.pack_propagate(False)
        tk.Label(ai,text="🐋>",font=(self.font, self.scale(64)),fg=self.primary_font_color_2,bg=upper_color).pack(side=tk.LEFT,padx=(self.scale(350),0))
        ai_text_box = tk.Frame(ai,bg=upper_color,highlightbackground=self.primary_font_color_2,highlightthickness=2,width=self.scale(mid))
        ai_text_box.pack(side=tk.LEFT,fill=tk.Y,pady=self.scale(15))
        ai_text_box.pack_propagate(False)
        self.ai_text = tk.Label(ai_text_box,text='',bg=upper_color,wraplength=self.scale(mid),fg=self.primary_font_color_2,font=(self.font,self.scale(24)))
        self.ai_text.pack(side=tk.LEFT)




        # -------------------------------------------LOWER------------------------------------------------------    
        lower_color = upper_color
        human_response = tk.Frame(content_frame, bg=lower_color,height=self.scale(half))
        human_response.pack(fill=tk.BOTH)
        human_response.pack_propagate(False)
        tk.Label(human_response,text="<👤",font=(self.font, self.scale(64)),fg=self.primary_font_color_2,bg=lower_color).pack(side=tk.RIGHT,padx=(0,self.scale(350)))
        human_response_textbox = tk.Frame(human_response,bg=upper_color,highlightbackground=self.primary_font_color_2,highlightthickness=2,width=self.scale(mid))
        human_response_textbox.pack(side=tk.RIGHT,fill=tk.Y,pady=self.scale(15))
        human_response_textbox.pack_propagate(False)
        self.human_response_text = tk.Label(human_response_textbox,text='',bg=upper_color,fg=self.primary_font_color_2,wraplength=self.scale(mid),font=(self.font,self.scale(24)))
        self.human_response_text.pack(side=tk.RIGHT)
        

        #-------------------------------------------Footer------------------------------------------------------
        
        footer_frame = tk.Frame(self.root, bg=self.header_color, height=self.scale(120))
        footer_frame.pack(fill=tk.X,side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        self.operator = tk.Label(footer_frame, text="Made with ❤️", 
                                   font=(self.font, self.scale(26), "bold"),
                                   fg=self.primary_font_color,bg=self.header_color)
        
        self.operator.pack(side=tk.RIGHT, padx=self.scale(20))

    def update_ai_box(self,text):
        self.ai_text.config(text=text)

    def update_human_box(self,text):
        self.human_response_text.config(text=text)

    def process_text(self, filepath):
        try:
            with open(filepath, 'r') as f:
                if filepath.endswith("Customer.txt"):
                    self.update_human_box(f.read())
                elif filepath.endswith("Ai.txt"):
                    self.update_ai_box(f.read())
        except Exception as e:
            print(f"Error processing order file: {e}")
    

    def setup_order_watcher(self):
        chat_location = os.path.join(os.getcwd(),'Chat')
        with open(os.path.join(chat_location,'Customer.txt'), 'w') as file:
            file.write('')
        with open(os.path.join(chat_location,'Ai.txt'), 'w') as file:
            file.write('')
        
        class OrderHandler(FileSystemEventHandler):
            def __init__(self, app):
                self.app = app
            
            def on_modified(self, event):
                if event.is_directory:
                    return
                if event.src_path.endswith(".txt"):
                    self.app.process_text(event.src_path)

        self.event_handler = OrderHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path="Chat", recursive=False)
        self.observer.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderDisplayApp(root)
    root.mainloop()
    