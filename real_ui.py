import tkinter as tk
import os,watchdog,json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OrderDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Order Display")
        self.root.geometry("1920x1080")
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
        #self.check_for_new_orders()

    def create_widgets(self):
        # -------------------------------------------HEADER------------------------------------------------------
        self.header_frame = tk.Frame(self.root, bg=self.header_color, height=120)
        self.header_frame.pack(fill=tk.X)
        self.header_frame.pack_propagate(False)

        self.logo_label = tk.Label(self.header_frame, text="🍹 Kmitl Drive-Thru", font=(self.font, 32, "bold"),fg=self.primary_font_color,bg=self.header_color)

        self.logo_label.pack(side=tk.LEFT, padx=20, pady=15)

        self.time_label = tk.Label(self.header_frame, font=(self.font, 22), fg="white", bg=self.header_color)
        self.time_label.pack(side=tk.RIGHT, padx=20, pady=15)
        tk.Frame(self.root, bg="#E69D00", height=5).pack(fill=tk.X)



        # -------------------------------------------Body------------------------------------------------------
        self.content_frame = tk.Frame(self.root, bg="#374151")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------LEFT------------------------------------------------------
        self.order_frame = tk.Frame(self.content_frame, bg="#000000")
        self.order_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header
        
        self.header_order_frame = tk.Frame(self.order_frame, bg=self.header_order_color, height=100)
        self.header_order_frame.pack(fill=tk.X)
        self.header_order_frame.pack_propagate(False)

        tk.Frame(self.order_frame, bg=self.header_color, height=3).pack(fill=tk.X)

        self.order_number_frame = tk.Frame(self.header_order_frame , bg=self.header_order_color, width=20)
        self.order_number_frame.pack(side=tk.LEFT,padx=10)

        self.order_number_label = tk.Label(self.order_number_frame, text=f"ORDER #000", font=(self.font, 24),fg=self.sec_font_color,bg=self.header_color,)
        self.order_number_label.pack(side=tk.LEFT, padx=(20,5), pady=15)

        self.len_item_label = tk.Label(self.header_order_frame, text=f"0 ITEMS", font=(self.font, 20),fg=self.header_color,bg=self.header_order_color)
        self.len_item_label.pack(side=tk.LEFT, padx=20, pady=15)

        self.status = tk.Label(self.header_order_frame, text=f"● PROCESSING", font=(self.font, 16),fg="#33ff00",bg=self.header_order_color,)
        self.status.pack(side=tk.RIGHT, padx=20, pady=15)
        self.update_time()


        # -------------------------------------------RIGHT------------------------------------------------------

        self.summary_frame_color = "#030712"
        self.summary_frame = tk.Frame(self.content_frame, bg=self.summary_frame_color, width=600)
        self.summary_frame.pack(side=tk.RIGHT, fill=tk.BOTH,padx=3)
        self.summary_frame.pack_propagate(False)

        tk.Frame(self.summary_frame, bg=self.summary_frame_color, height=100).pack(fill=tk.X)

        self.sub_total_frame = tk.Frame(self.summary_frame, bg=self.summary_frame_color, height=50)
        self.sub_total_frame.pack(fill=tk.X)

        
        self.sub_total_label = tk.Label(self.sub_total_frame, text=f"SUBTOTAL", font=(self.font, 28),fg=self.primary_font_color,bg=self.summary_frame_color,)
        self.sub_total_label.pack(side=tk.LEFT,padx=20, pady=25)

        self.subtotal = tk.Label(self.sub_total_frame, text=f"$0000.00", font=(self.font, 28),fg=self.primary_font_color,bg=self.summary_frame_color,)
        self.subtotal.pack(side=tk.RIGHT,padx=20, pady=15)

        tk.Frame(self.summary_frame, bg="#3d3d3d",height=5).pack(fill=tk.X,padx=20)
        tk.Frame(self.summary_frame, bg=self.summary_frame_color, height=50).pack(fill=tk.X)


        self.Tax_frame = tk.Frame(self.summary_frame, bg=self.summary_frame_color, height=50)
        self.Tax_frame.pack(fill=tk.X)

        self.Tax_label = tk.Label(self.Tax_frame, text=f"TAX", font=(self.font, 28),fg=self.primary_font_color,bg=self.summary_frame_color,)
        self.Tax_label.pack(side=tk.LEFT,padx=20, pady=25)

        self.Tax = tk.Label(self.Tax_frame, text=f"$0000.00", font=(self.font, 28),fg=self.primary_font_color,bg=self.summary_frame_color,)
        self.Tax.pack(side=tk.RIGHT,padx=20, pady=25)

        tk.Frame(self.summary_frame, bg="#3d3d3d",height=5).pack(fill=tk.X,padx=20)
        tk.Frame(self.summary_frame, bg=self.summary_frame_color, height=150).pack(fill=tk.X)

        self.Total_frame = tk.Frame(self.summary_frame, bg='#22c55e', height=200)
        self.Total_frame.pack(fill=tk.X,padx=20)

        self.xx = tk.Frame(self.Total_frame, bg="#16a34a", height=200)
        self.xx.pack(fill=tk.BOTH,padx=10,pady=(10, 0))

        self.Total_label = tk.Label(self.xx, text=f"TOTAL", font=(self.font, 28),fg=self.primary_font_color,bg="#16a34a")
        self.Total_label.pack(side=tk.LEFT,padx=15, pady=(10,0))


        self.yy = tk.Frame(self.Total_frame, bg="#16a34a", height=200)
        self.yy.pack(fill=tk.BOTH,padx=10,pady=(0, 10))

        self.Total = tk.Label(self.yy, text=f"$0000.00", font=(self.font, 60),fg=self.primary_font_color,bg="#16a34a")
        self.Total.pack(side=tk.LEFT,padx=20, pady=(0,10))

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


root = tk.Tk()
app = OrderDisplayApp(root)
root.mainloop()

