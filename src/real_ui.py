import tkinter as tk
import os,watchdog,json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OrderDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Order Display")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.scale_factor = min(screen_width / 1920, screen_height / 1080)
        
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#FDFDFD")

        self.header_color = "#FFAE00"
        self.visible = True
        self.font = 'Space Mono'
        self.primary_font_color = "#ffffff"
        self.sec_font_color = "#000000"
        self.header_order_color = "#111827"

        self.create_widgets()
        self.current_order_id = None
        self.current_items = []
        self.setup_order_watcher()
        self.check_for_new_orders()

    def scale(self, value):
        """Scale a pixel value based on screen resolution"""
        return int(value * self.scale_factor)

    def create_widgets(self):
        # -------------------------------------------HEADER------------------------------------------------------
        self.header_frame = tk.Frame(self.root, bg=self.header_color, height=self.scale(120))
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)

        self.logo_label = tk.Label(self.header_frame, text="🍹 Kmitl Drive-Thru", 
                                   font=(self.font, self.scale(32), "bold"),
                                   fg=self.primary_font_color,bg=self.header_color)

        self.logo_label.pack(side=tk.LEFT, padx=self.scale(20), pady=self.scale(15))

        self.time_label = tk.Label(self.header_frame, font=(self.font, self.scale(22)), 
                                   fg="white", bg=self.header_color)
        self.time_label.pack(side=tk.RIGHT, padx=self.scale(20), pady=self.scale(15))
        tk.Frame(self.root, bg="#E69D00", height=self.scale(5)).pack(fill=tk.X)

        # -------------------------------------------Body------------------------------------------------------
        self.content_frame = tk.Frame(self.root, bg="#374151")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------LEFT------------------------------------------------------
        self.order_frame = tk.Frame(self.content_frame, bg="#000000")
        self.order_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        self.header_order_frame = tk.Frame(self.order_frame, bg=self.header_order_color, 
                                          height=self.scale(100))
        self.header_order_frame.pack(fill=tk.X)
        self.header_order_frame.pack_propagate(False)

        tk.Frame(self.order_frame, bg=self.header_color, height=self.scale(3)).pack(fill=tk.X)

        self.order_number_frame = tk.Frame(self.header_order_frame, bg=self.header_order_color, 
                                          width=self.scale(20))
        self.order_number_frame.pack(side=tk.LEFT,padx=self.scale(10))

        self.order_number_label = tk.Label(self.order_number_frame, text=f"ORDER #000", 
                                          font=(self.font, self.scale(24)),
                                          fg=self.sec_font_color,bg=self.header_color)
        self.order_number_label.pack(side=tk.LEFT, padx=(self.scale(20),self.scale(5)), 
                                     pady=self.scale(15))

        self.len_item_label = tk.Label(self.header_order_frame, text=f"0 ITEMS", 
                                      font=(self.font, self.scale(20)),
                                      fg=self.header_color,bg=self.header_order_color)
        self.len_item_label.pack(side=tk.LEFT, padx=self.scale(20), pady=self.scale(15))

        self.status = tk.Label(self.header_order_frame, text=f"● PROCESSING", 
                              font=(self.font, self.scale(16)),
                              fg="#33ff00",bg=self.header_order_color)
        self.status.pack(side=tk.RIGHT, padx=self.scale(20), pady=self.scale(15))
        self.update_time()

        self.items_frame = tk.Frame(self.order_frame,bg="#000000")
        self.items_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # -------------------------------------------RIGHT------------------------------------------------------
        self.summary_frame_color = "#030712"
        self.summary_frame = tk.Frame(self.content_frame, bg=self.summary_frame_color, 
                                     width=self.scale(600))
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.BOTH,padx=self.scale(3))
        self.summary_frame.pack_propagate(False)

        tk.Frame(self.summary_frame, bg=self.summary_frame_color, 
                height=self.scale(100)).pack(fill=tk.X)

        self.sub_total_frame = tk.Frame(self.summary_frame, bg=self.summary_frame_color, 
                                       height=self.scale(50))
        self.sub_total_frame.pack(fill=tk.X)

        self.sub_total_label = tk.Label(self.sub_total_frame, text=f"SUBTOTAL", 
                                       font=(self.font, self.scale(28)),
                                       fg=self.primary_font_color,bg=self.summary_frame_color)
        self.sub_total_label.pack(side=tk.LEFT,padx=self.scale(20), pady=self.scale(25))

        self.subtotal_label = tk.Label(self.sub_total_frame, text=f"$0000.00", 
                                      font=(self.font, self.scale(28)),
                                      fg=self.primary_font_color,bg=self.summary_frame_color)
        self.subtotal_label.pack(side=tk.RIGHT,padx=self.scale(20), pady=self.scale(15))

        tk.Frame(self.summary_frame, bg="#3d3d3d",height=self.scale(5)).pack(fill=tk.X,
                                                                             padx=self.scale(20))
        tk.Frame(self.summary_frame, bg=self.summary_frame_color, 
                height=self.scale(50)).pack(fill=tk.X)

        self.Tax_frame = tk.Frame(self.summary_frame, bg=self.summary_frame_color, 
                                 height=self.scale(50))
        self.Tax_frame.pack(fill=tk.X)

        self.tax_label = tk.Label(self.Tax_frame, text=f"TAX", 
                                 font=(self.font, self.scale(28)),
                                 fg=self.primary_font_color,bg=self.summary_frame_color)
        self.tax_label.pack(side=tk.LEFT,padx=self.scale(20), pady=self.scale(25))

        self.Tax = tk.Label(self.Tax_frame, text=f"$0000.00", 
                           font=(self.font, self.scale(28)),
                           fg=self.primary_font_color,bg=self.summary_frame_color)
        self.Tax.pack(side=tk.RIGHT,padx=self.scale(20), pady=self.scale(25))

        tk.Frame(self.summary_frame, bg="#3d3d3d",height=self.scale(5)).pack(fill=tk.X,
                                                                             padx=self.scale(20))
        tk.Frame(self.summary_frame, bg=self.summary_frame_color, 
                height=self.scale(150)).pack(fill=tk.X)

        self.Total_frame = tk.Frame(self.summary_frame, bg='#22c55e', height=self.scale(200))
        self.Total_frame.pack(fill=tk.X,padx=self.scale(20))

        self.xx = tk.Frame(self.Total_frame, bg="#16a34a", height=self.scale(200))
        self.xx.pack(fill=tk.BOTH,padx=self.scale(10),pady=(self.scale(10), 0))

        self.Total_label = tk.Label(self.xx, text=f"TOTAL", 
                                   font=(self.font, self.scale(28)),
                                   fg=self.primary_font_color,bg="#16a34a")
        self.Total_label.pack(side=tk.LEFT,padx=self.scale(15), pady=(self.scale(10),0))

        self.yy = tk.Frame(self.Total_frame, bg="#16a34a", height=self.scale(200))
        self.yy.pack(fill=tk.BOTH,padx=self.scale(10),pady=(0, self.scale(10)))

        self.total_label = tk.Label(self.yy, text=f"$0000.00", 
                                   font=(self.font, self.scale(60)),
                                   fg=self.primary_font_color,bg="#16a34a")
        self.total_label.pack(side=tk.LEFT,padx=self.scale(20), pady=(0,self.scale(10)))

    def update_time(self):
        current_time = datetime.now().strftime("%I:%M:%S %p")
        self.time_label.config(text=current_time)

        if self.visible:
            self.status.config(fg=self.header_order_color)
            self.visible = False
        else:
            self.status.config(fg="#33ff00")
            self.visible = True
    
        self.root.after(1000, self.update_time)

    def display_order(self, order_data):
        self.clear_items_frame()

        self.order_number_label.config(text=f'ORDER #{int(order_data.get("order_id", "--")):03d}')

        for i, item in enumerate(order_data.get("items", [])):
            if i % 2:
                bg_color="#030712"
            else:
                bg_color='#000000'
            item_frame = tk.Frame(self.items_frame, bg=bg_color, 
                                 padx=self.scale(10), pady=self.scale(10))
            item_frame.pack(fill=tk.X)

            header_frame = tk.Frame(item_frame, bg=bg_color)
            header_frame.pack(fill=tk.X)

            a = tk.Frame(header_frame, bg=self.header_color,
                        height=self.scale(60),width=self.scale(75))
            a.pack(side=tk.LEFT,padx=(self.scale(25),self.scale(20)))
            a.pack_propagate(False)

            tk.Label(a, text=item.get("quantity", 1), 
                    font=(self.font, self.scale(30)),
                    fg="#000000",bg=self.header_color).pack()
            
            tk.Label(header_frame, text=item.get("item", "").upper(), 
                    font=(self.font, self.scale(24), "bold"), 
                    fg="white", bg=bg_color, anchor="w").pack(side=tk.LEFT)
            
            tk.Label(header_frame, text=f"${item.get('line_total', 0):.2f}", 
                    font=(self.font, self.scale(28)), 
                    fg=self.primary_font_color, bg=bg_color).pack(side=tk.RIGHT)

            customizations = item.get("customizations", {})
            for section, selections in customizations.items():
                if isinstance(selections, list) and selections:
                    custom_text = f"▸ {', '.join(selections)}"
                    tk.Label(item_frame, text=custom_text, 
                           font=(self.font, self.scale(16)), fg=self.header_color, 
                           bg=bg_color, anchor="w").pack(fill=tk.X,
                                                         padx=(self.scale(120),self.scale(20)))
                elif isinstance(selections, str) and selections != self.get_default_option(section, item.get("category", "")):
                    custom_text = f"▸ {selections}"
                    tk.Label(item_frame, text=custom_text, 
                           font=(self.font, self.scale(16)), fg=self.header_color, 
                           bg=bg_color, anchor="w").pack(fill=tk.X,
                                                         padx=(self.scale(120),self.scale(20)))

            tk.Frame(self.items_frame, bg="#374151",
                    height=self.scale(2)).pack(fill=tk.X)

        self.len_item_label.config(text=f"{sum(item['quantity'] for item in order_data['items'])} ITEMS")
        self.subtotal_label.config(text=f"${order_data.get('subtotal', 0):.2f}")
        self.Tax.config(text=f"${order_data.get('tax', 0):.2f}")
        self.total_label.config(text=f"${order_data.get('total', 0):.2f}")

        self.items_frame.update_idletasks()

    def clear_items_frame(self):
        for widget in self.items_frame.winfo_children():
            widget.destroy()

    def get_default_option(self, section, category):
        default_options = {
            "Size": "Regular",
            "Ice": "Regular Ice",
            "Extras": "No Extras",
        }
        return default_options.get(section, "")

    def setup_order_watcher(self):
        if not os.path.exists("temp"):
            os.makedirs("temp")
        
        class OrderHandler(FileSystemEventHandler):
            def __init__(self, app):
                self.app = app
            
            def on_created(self, event):
                if event.is_directory:
                    return
                if event.src_path.endswith(".json"):
                    self.app.process_order_file(event.src_path)
            
            def on_modified(self, event):
                if event.is_directory:
                    return
                if event.src_path.endswith(".json"):
                    self.app.process_order_file(event.src_path)

        self.event_handler = OrderHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path="temp", recursive=False)
        self.observer.start()
    
    def process_order_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                order_data = json.load(f)
                self.display_order(order_data)
                self.current_order_id = order_data.get("order_id")
        except Exception as e:
            print(f"Error processing order file: {e}")
    
    def check_for_new_orders(self):
        try:
            order_files = [f for f in os.listdir("temp") if f.startswith("order_") and f.endswith(".json")]
            if order_files:
                order_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))
                latest_order = order_files[-1]

                order_id = int(latest_order.split('_')[1].split('.')[0])
                if self.current_order_id is None or order_id > self.current_order_id:
                    self.process_order_file(os.path.join("temp", latest_order))
        except Exception as e:
            print(f"Error checking for new orders: {e}")

        self.root.after(500, self.check_for_new_orders)
    
    def on_closing(self):
        self.observer.stop()
        self.observer.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderDisplayApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()