import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar, ttk  
from PIL import Image, ImageTk

LARGEFONT = ("Verdana", 20)

class DmartApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")

        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menubar) 
        self.title("D-Mart App")
        self.geometry("1280x800")  
        self.configure(bg="white")
        self.resizable(True, True)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.wishlist = []
        self.frames = {}

        for F in (LogoPage, SignupPage, CustomerDashboard, EmployeeDashboard, GroceryPlanner, WishlistPage, Billing, StockAndQuality, OffersCouponsPage, MonthlyReport):
            frame =F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(LogoPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

class LogoPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.configure(bg="white")
        self.controller = controller

        bg_image = Image.open("images/logo_bg.png")
        bg_image = bg_image.resize((1280, 800))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self, text="🛒 Welcome to D-Mart!", font=("Helvetica", 22, "bold"),
                         fg="white", bg="#000000")  
        label.place(relx=0.5, rely=0.3, anchor="center")

        button = tk.Button(self, text="Continue", font=("Helvetica", 14, "bold"),
                           bg="#00cec9", fg="white", padx=20, pady=10,
                           command=lambda: controller.show_frame(SignupPage)) 
        button.place(relx=0.5, rely=0.45, anchor="center")

class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        bg_image = Image.open("images/signup_bg.png")  
        bg_image = bg_image.resize((1280, 800))              
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
       
        self.role_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        title_label = ttk.Label(self, text="🛒 Login", font=LARGEFONT)
        title_label.pack(pady=20)

        role_label = ttk.Label(self, text="Register as:")
        role_label.pack()
        role_combo = ttk.Combobox(self, textvariable=self.role_var, state="readonly",
                                  values=["Customer", "Employee"])
        role_combo.pack(pady=5)

        name_label = ttk.Label(self, text="Full Name:")
        name_label.pack()
        name_entry = ttk.Entry(self, textvariable=self.name_var)
        name_entry.pack(pady=5)

        email_label = ttk.Label(self, text="Email:")
        email_label.pack()
        email_entry = ttk.Entry(self, textvariable=self.email_var)
        email_entry.pack(pady=5)

        password_label = ttk.Label(self, text="Password:")
        password_label.pack()
        password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)

        confirm_password_label = ttk.Label(self, text="Confirm Password:")
        confirm_password_label.pack()
        confirm_password_entry = ttk.Entry(self, textvariable=self.confirm_password_var, show="*")
        confirm_password_entry.pack(pady=5)

        signup_button = ttk.Button(self, text="Sign Up", command=self.signup)
        signup_button.pack(pady=20)

    def signup(self):
        role = self.role_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if not role or not name or not email or not password or not confirm_password:
            messagebox.showwarning("Missing Fields", "Please fill all fields!")
        elif password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match!")
        else:
            messagebox.showinfo("Success", f"Account created successfully as {role}.")
            if role == "Customer":
                self.controller.show_frame(CustomerDashboard)
            else:
                self.controller.show_frame(EmployeeDashboard)

class CustomerDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        bg_image = Image.open("images/customer_dashboard_bg.png")  
        bg_image = bg_image.resize((1280, 800))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(self, text="Welcome to DMart", font=("Arial", 24, "bold"),
                         bg="#000000", fg="white")
        title.place(relx=0.5, rely=0.1, anchor="center")

        subtitle = tk.Label(self, text="Customer Dashboard", font=("Arial", 16),
                            bg="#000000", fg="white")
        subtitle.place(relx=0.5, rely=0.18, anchor="center")

        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_style = {"font": ("Arial", 12), "width": 30, "padx": 5, "pady": 5}

        tk.Button(button_frame, text="🛒 Grocery Planner",
                  command=lambda: controller.show_frame(GroceryPlanner), **btn_style).pack(pady=5)
        tk.Button(button_frame, text="❤ Wishlist",
                  command=lambda: controller.show_frame(WishlistPage), **btn_style).pack(pady=5)
        tk.Button(button_frame, text="🧾 Billing",
                  command=lambda: controller.show_frame(Billing), **btn_style).pack(pady=5)

        tk.Button(button_frame, text="🚪 Logout", bg="#f44336", fg="white",
                  command=lambda: controller.show_frame(LogoPage), **btn_style).pack(pady=20)

class EmployeeDashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)  
        self.controller = controller

        bg_image = Image.open("images/employee_dashboard_bg.png") 
        bg_image = bg_image.resize((1280, 800))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(self, text="Welcome to DMart", font=("Arial", 24, "bold"),
                         bg="#000000", fg="white")
        title.place(relx=0.5, rely=0.1, anchor="center")

        subtitle = tk.Label(self, text="Employee Dashboard", font=("Arial", 16),
                            bg="#000000", fg="white")
        subtitle.place(relx=0.5, rely=0.18, anchor="center")

        button_frame = tk.Frame(self, bg="#ffffff")
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_style = {"font": ("Arial", 12), "width": 30, "padx": 5, "pady": 5}

        def open_stock_quality_page():
            controller.show_frame(StockAndQuality)

        tk.Button(button_frame, text="📦 Stock & Quality", command=open_stock_quality_page, **btn_style).pack(pady=5)
        tk.Button(button_frame, text="🏷 Offers & Coupons", command=lambda: controller.show_frame(OffersCouponsPage), **btn_style).pack(pady=5)
        tk.Button(button_frame, text="📊 Monthly Report", command=lambda: controller.show_frame(MonthlyReport), **btn_style).pack(pady=5)

        tk.Button(button_frame, text="🚪 Logout", bg="#f44336", fg="white",
                  command=lambda: controller.show_frame(LogoPage), **btn_style).pack(pady=20)
        
class GroceryPlanner(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.products = [
            {"name": "apple", "price": 100, "image": "images/apple.png"},
            {"name": "banana", "price": 42, "image": "images/banana.png"},
            {"name": "milk", "price": 208, "image": "images/milk.png"},
            {"name": "bread", "price": 149, "image": "images/bread.png"},
            {"name": "eggs", "price": 249, "image": "images/eggs.png"},
            {"name": "cheese", "price": 374, "image": "images/cheese.png"},
            {"name": "tomato", "price": 83, "image": "images/tomato.png"},
            {"name": "potato", "price": 58, "image": "images/potato.png"},
            {"name": "carrot", "price": 75, "image": "images/carrot.png"},
            {"name": "yogurt", "price": 91, "image": "images/yogurt.png"},
            {"name": "chicken", "price": 540, "image": "images/chicken.png"},
            {"name": "beef", "price": 623, "image": "images/beef.png"},
            {"name": "orange", "price": 108, "image": "images/orange.png"},
            {"name": "grapes", "price": 183, "image": "images/grapes.png"},
            {"name": "rice", "price": 166, "image": "images/rice.png"},
            {"name": "pasta", "price": 125, "image": "images/pasta.png"},
            {"name": "cereal", "price": 266, "image": "images/cereal.png"},
            {"name": "butter", "price": 232, "image": "images/butter.png"},
            {"name": "juice", "price": 199, "image": "images/juice.png"},
            {"name": "onion", "price": 50, "image": "images/onion.png"},
        ]

        self.product_images = {}

        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)

        ttk.Label(header_frame, text="Grocery Planner", font=("Arial", 20, "bold")).pack(side="top", padx=20)

        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side="right", padx=20)
        ttk.Button(button_frame, text="Go to Wishlist", command=lambda: controller.show_frame(WishlistPage)).pack(pady=(0, 5))
        back_btn = tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame(CustomerDashboard))
        back_btn.pack(pady=10)

        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg="white")
        left_frame.pack(side="right", fill="both", expand=True, padx=(20, 10))

        canvas = tk.Canvas(left_frame, bg="white")
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.display_products_grid(self.scroll_frame)

        self.right_preview = tk.Frame(main_frame, width=300, bg="white", bd=2, relief="groove")
        self.right_preview.pack(side="left", fill="y", padx=(10, 20), pady=10)
        tk.Label(self.right_preview, text="Wishlist Preview", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        self.preview_list = tk.Frame(self.right_preview, bg="white")
        self.preview_list.pack(fill="y", expand=True)

        self.refresh_wishlist_preview()

    def display_products_grid(self, parent_frame):
        columns = 4
        image_size = (180, 180)

        for idx, product in enumerate(self.products):
            row = idx // columns
            col = idx % columns

            card = ttk.Frame(parent_frame, relief="raised", borderwidth=2, padding=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="w")

            try:
                img = Image.open(product["image"]).resize(image_size)
                photo = ImageTk.PhotoImage(img)
                self.product_images[product["name"]] = photo
                ttk.Label(card, image=photo).pack()
            except Exception:
                ttk.Label(card, text="[Image Missing]", font=("Arial", 14)).pack()

            ttk.Label(card, text=product["name"].title(), font=("Arial", 14, "bold")).pack(pady=(10, 0))
            ttk.Label(card, text=f"Price: ₹{product['price']}", foreground="green", font=("Arial", 13)).pack()

            ttk.Button(card, text="Add to Wishlist", command=lambda p=product: self.add_to_wishlist(p)).pack(pady=8)

    def add_to_wishlist(self, product):
        if product not in self.controller.wishlist:
            self.controller.wishlist.append(product)
            print(f"✅ Added to Wishlist: {product['name']}")
            self.refresh_wishlist_preview()
        else:
            print(f"⚠ {product['name']} is already in wishlist!")

    def refresh_wishlist_preview(self):
        for widget in self.preview_list.winfo_children():
            widget.destroy()

        image_size = (60, 60)
        for product in self.controller.wishlist:
            row = tk.Frame(self.preview_list, bg="white")
            row.pack(pady=5, anchor="w")

            try:
                img = Image.open(product["image"]).resize(image_size)
                photo = ImageTk.PhotoImage(img)
                self.product_images[product["name"] + "_small"] = photo
                tk.Label(row, image=photo, bg="white").pack(side="right", padx=5)
            except Exception:
                tk.Label(row, text="[No Img]", bg="white").pack(side="right", padx=5)

            tk.Label(row, text=product["name"].title(), font=("Arial", 12), bg="white").pack(side="left", padx=5)

class WishlistPage(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        self.product_images = {}

        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)
        ttk.Label(header_frame, text="Wishlist", font=("Arial", 20, "bold")).pack(side="top", padx=20)
        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side="right", padx=20)
        ttk.Button(header_frame, text="Back to Grocery Planner", command=lambda: controller.show_frame(GroceryPlanner)).pack(side="right", padx=20)
        ttk.Button(header_frame, text="Go to Billing", command=lambda: controller.show_frame(Billing)).pack(side="right", padx=20)

        self.canvas = tk.Canvas(self, bg="white")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas)

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="top", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.bind("<<ShowFrame>>", lambda e: self.display_wishlist())
        self.display_wishlist()

    def display_wishlist(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        columns = 4
        image_size = (180, 180)

        wishlist = self.controller.wishlist
        if not wishlist:
            ttk.Label(self.scroll_frame, text="Your wishlist is empty.", font=("Arial", 16)).pack(pady=50)
            return

        for idx, product in enumerate(wishlist):
            row = idx // columns
            col = idx % columns

            card = ttk.Frame(self.scroll_frame, relief="raised", borderwidth=2, padding=15)
            card.grid(row=row, column=col, padx=20, pady=20, sticky="n")

            try:
                img = Image.open(product["image"]).resize(image_size)
                photo = ImageTk.PhotoImage(img)
                self.product_images[product["name"]] = photo
                ttk.Label(card, image=photo).pack()
            except Exception:
                ttk.Label(card, text="[Image Missing]", font=("Arial", 14)).pack()

            ttk.Label(card, text=product["name"].title(), font=("Arial", 14, "bold")).pack(pady=(10, 0))
            ttk.Button(card, text="Remove", command=lambda p=product: self.remove_from_wishlist(p)).pack(pady=8)

    def remove_from_wishlist(self, product):
        if product in self.controller.wishlist:
            self.controller.wishlist.remove(product)
            print(f"🗑 Removed from Wishlist: {product['name']}")
            self.display_wishlist()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.event_generate("<<ShowFrame>>")

class Billing(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill="x", pady=10)

        button_frame = tk.Frame(header_frame, bg="white")
        button_frame.pack(side="right", padx=20)
        ttk.Label(header_frame, text="Billing Section", font=("Arial", 20, "bold")).pack(side="top", padx=20)
        ttk.Button(header_frame, text="Back to Wishlist", command=lambda: controller.show_frame(WishlistPage)).pack(side="right", padx=20)
        back_btn = tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame(CustomerDashboard))
        back_btn.pack(pady=10)

        self.total_label = ttk.Label(self, text="", font=("Arial", 16, "bold"))
        self.total_label.pack(pady=20)

        self.billing_items_frame = tk.Frame(self, bg="white")
        self.billing_items_frame.pack(fill="both", expand=True)

        ttk.Button(self, text="Checkout", command=self.checkout).pack(pady=10)

        self.bind("<<ShowFrame>>", lambda e: self.display_bill())
        self.display_bill()

    def display_bill(self):
        for widget in self.billing_items_frame.winfo_children():
            widget.destroy()

        total = 0.0
        image_size = (60, 60)
        self.product_images = {}

        for product in self.controller.wishlist:
            name = product["name"].title()
            price = product["price"]
            total += price

            row = ttk.Frame(self.billing_items_frame)
            row.pack(fill="x", pady=5, padx=20)

            try:
                from PIL import Image, ImageTk
                img = Image.open(product["image"]).resize(image_size)
                photo = ImageTk.PhotoImage(img)
                self.product_images[product["name"]] = photo  # Store reference
                tk.Label(row, image=photo, bg="white").pack(side="left", padx=10)
            except Exception:
                tk.Label(row, text="[No Image]", bg="white").pack(side="left", padx=10)

            ttk.Label(row, text=name, width=20).pack(side="left")
            ttk.Label(row, text=f"₹{price:.2f}").pack(side="right")

        self.total_label.config(text=f"Total Amount: ₹{total:.2f}")

    def checkout(self):
        if not self.controller.wishlist:
            self.total_label.config(text="Your wishlist is empty.")
            return

        self.total_label.config(text="Checkout successful! Thank you for shopping.")
        self.controller.wishlist.clear()
        self.display_bill() 

nutrition_data = {
    "Apple": {"Calories": 95, "Fat": "0.3g", "Sugar": "19g", "Protein": "0.5g", "Vitamin C": "14%"},
    "Banana": {"Calories": 105, "Fat": "0.4g", "Sugar": "14g", "Protein": "1.3g", "Vitamin B6": "20%"},
    "Milk": {"Calories": 150, "Fat": "8g", "Sugar": "12g", "Protein": "8g", "Calcium": "30%"},
    "Bread": {"Calories": 80, "Fat": "1g", "Sugar": "2g", "Protein": "3g", "Iron": "8%"},
    "Eggs": {"Calories": 70, "Fat": "5g", "Sugar": "0g", "Protein": "6g", "Cholesterol": "62%"},
    "Cheese": {"Calories": 113, "Fat": "9g", "Sugar": "0.5g", "Protein": "7g", "Calcium": "20%"},
    "Tomato": {"Calories": 22, "Fat": "0.2g", "Sugar": "3g", "Protein": "1g", "Vitamin C": "28%"},
    "Potato": {"Calories": 110, "Fat": "0g", "Sugar": "1g", "Protein": "3g", "Potassium": "620mg"},
    "Carrot": {"Calories": 25, "Fat": "0g", "Sugar": "3g", "Protein": "0.5g", "Vitamin A": "184%"},
    "Yogurt": {"Calories": 59, "Fat": "0.4g", "Sugar": "3g", "Protein": "10g", "Calcium": "15%"},
    "Chicken": {"Calories": 165, "Fat": "3.6g", "Sugar": "0g", "Protein": "31g", "Iron": "7%"},
    "Beef": {"Calories": 250, "Fat": "15g", "Sugar": "0g", "Protein": "26g", "Iron": "15%"},
    "Orange": {"Calories": 62, "Fat": "0.2g", "Sugar": "12g", "Protein": "1.2g", "Vitamin C": "116%"},
    "Grapes": {"Calories": 62, "Fat": "0.3g", "Sugar": "15g", "Protein": "0.6g", "Vitamin K": "18%"},
    "Rice": {"Calories": 206, "Fat": "0.4g", "Sugar": "0g", "Protein": "4.3g", "Iron": "2%"},
    "Pasta": {"Calories": 221, "Fat": "1.3g", "Sugar": "1g", "Protein": "8g", "Iron": "10%"},
    "Cereal": {"Calories": 120, "Fat": "1.5g", "Sugar": "9g", "Protein": "2g", "Fiber": "3g"},
    "Butter": {"Calories": 102, "Fat": "12g", "Sugar": "0g", "Protein": "0g", "Vitamin A": "11%"},
    "Juice": {"Calories": 110, "Fat": "0g", "Sugar": "22g", "Protein": "1g", "Vitamin C": "100%"},
    "Onion": {"Calories": 44, "Fat": "0.1g", "Sugar": "5g", "Protein": "1g", "Vitamin C": "12%"},
}

def show_nutrition(name):
    data = nutrition_data.get(name.title())
    if not data:
        messagebox.showinfo("Info", "Nutrition data not available.")
        return

    win = tk.Toplevel()
    win.title(f"{name} - Nutrition Info")
    win.geometry("300x250")
    tk.Label(win, text=f"{name} Nutrition Facts", font=("Arial", 14, "bold")).pack(pady=10)

    for k, v in data.items():
        tk.Label(win, text=f"{k}: {v}", font=("Arial", 10), anchor="w").pack(fill="x", padx=20)

class StockAndQuality(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.photos = []
        self.grid(row=0, column=0, sticky="nsew")
        self.controller = controller

        offers = {
            "apple":   "Buy 1 Get 1 Free", "banana":  "10% Off", "milk":    "Buy 2 Get 1 Free",
            "bread":   "Flat ₹10 Off", "eggs":    "₹5 Off on dozen", "cheese":  "15% Off",
            "tomato":  "Buy 1kg, Get 500g Free", "potato":  "₹2 Off per kg", "carrot":  "Free with ₹500 Cart",
            "yogurt":  "Buy 4, Pay for 3", "chicken": "Flat ₹30 Off", "beef":    "₹50 Off 1kg Pack",
            "orange":  "10% Off", "grapes":  "₹10 Off 500g", "rice":    "₹5 Off per kg",
            "pasta":   "Buy 2 Get 1", "cereal":  "Free Spoon Set", "butter":  "20% Off",
            "juice":   "₹10 Off 1L", "onion":   "Buy 3kg, Pay for 2",
        }

        canvas = tk.Canvas(self)
        scroll_frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        back_btn = tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame(EmployeeDashboard))
        back_btn.pack(pady=10)

        offers_btn = tk.Button(self, text="Go to Offers and Coupons", command=lambda: self.controller.show_frame(OffersCouponsPage))
        offers_btn.pack(pady=5)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_configure)

        items = [  
            {"name": "apple", "price": 100, "desc": "Fresh red apples", "image": "images/apple.png", "stock": 5, "quality": "Fresh"},
            {"name": "banana", "price": 42, "desc": "Organic bananas", "image": "images/banana.png", "stock": 8, "quality": "Fresh"},
            {"name": "milk", "price": 208, "desc": "Whole milk 1L", "image": "images/milk.png", "stock": 6, "quality": "Fresh"},
            {"name": "bread", "price": 149, "desc": "Wheat bread loaf", "image": "images/bread.png", "stock": 4, "quality": "Fresh"},
            {"name": "eggs", "price": 249, "desc": "Dozen eggs", "image": "images/eggs.png", "stock": 7, "quality": "Fresh"},
            {"name": "cheese", "price": 374, "desc": "Cheddar cheese 200g", "image": "images/cheese.png", "stock": 3, "quality": "Fresh"},
            {"name": "tomato", "price": 83, "desc": "Fresh tomatoes", "image": "images/tomato.png", "stock": 9, "quality": "Fresh"},
            {"name": "potato", "price": 58, "desc": "Brown potatoes", "image": "images/potato.png", "stock": 10, "quality": "Fresh"},
            {"name": "carrot", "price": 75, "desc": "Organic carrots", "image": "images/carrot.png", "stock": 5, "quality": "Fresh"},
            {"name": "yogurt", "price": 91, "desc": "Greek yogurt cup", "image": "images/yogurt.png", "stock": 4, "quality": "Fresh"},
            {"name": "chicken", "price": 540, "desc": "Chicken breast 500g", "image": "images/chicken.png", "stock": 6, "quality": "Fresh"},
            {"name": "beef", "price": 623, "desc": "Beef steak 500g", "image": "images/beef.png", "stock": 3, "quality": "Fresh"},
            {"name": "orange", "price": 108, "desc": "Juicy oranges", "image": "images/orange.png", "stock": 7, "quality": "Fresh"},
            {"name": "grapes", "price": 183, "desc": "Green seedless grapes", "image": "images/grapes.png", "stock": 5, "quality": "Fresh"},
            {"name": "rice", "price": 166, "desc": "Basmati rice 1kg", "image": "images/rice.png", "stock": 8, "quality": "Fresh"},
            {"name": "pasta", "price": 125, "desc": "Spaghetti 500g", "image": "images/pasta.png", "stock": 7, "quality": "Fresh"},
            {"name": "cereal", "price": 266, "desc": "Oats cereal box", "image": "images/cereal.png", "stock": 4, "quality": "Fresh"},
            {"name": "butter", "price": 232, "desc": "Salted butter 250g", "image": "images/butter.png", "stock": 6, "quality": "Fresh"},
            {"name": "juice", "price": 199, "desc": "Orange juice 1L", "image": "images/juice.png", "stock": 5, "quality": "Fresh"},
            {"name": "onion", "price": 50, "desc": "Red onions 1kg", "image": "images/onion.png", "stock": 9, "quality": "Fresh"},
        ]

        for index, item in enumerate(items):
            item_frame = tk.Frame(scroll_frame, bd=1, relief="solid", padx=5, pady=5)
            item_frame.grid(row=index, column=0, pady=5, padx=10, sticky="w")

            try:
                photo = tk.PhotoImage(file=item["image"]).subsample(6, 6)
                self.photos.append(photo)
                img_label = tk.Label(item_frame, image=photo)
                img_label.grid(row=0, column=0, rowspan=3, padx=5)
            except Exception:
                img_label = tk.Label(item_frame, text="No Image")
                img_label.grid(row=0, column=0, rowspan=3, padx=5)

            name_label = tk.Label(item_frame, text=f"{item['name']} - Stock: {item['stock']}", font=("Arial", 10, "bold"))
            name_label.grid(row=0, column=1, sticky="w", padx=10)

            price_label = tk.Label(item_frame, text=f"Price: {item['price']:.2f}", font=("Arial", 10))
            price_label.grid(row=1, column=1, sticky="w", padx=10)

            offer_text = offers.get(item['name'].lower(), "No Offer")
            offer_label = tk.Label(item_frame, text=f"Offer: {offer_text}", font=("Arial", 9), fg="green")
            offer_label.grid(row=2, column=1, columnspan=2, sticky="w", padx=10)

            quality_var = StringVar(value=item["quality"])
            quality_menu = OptionMenu(item_frame, quality_var, "Fresh", "Good", "Average", "Expired")
            quality_menu.grid(row=0, column=2, padx=10)

            nutri_btn = tk.Button(item_frame, text="Nutrition Info", command=lambda n=item['name']: show_nutrition(n))
            nutri_btn.grid(row=1, column=2, padx=10, pady=5)

class OffersCouponsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="Offers & Coupons", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        offers_data = {
            "apple":   {"offer": "Buy 1 Get 1 Free",     "coupon": "APPBOGO"},
            "banana":  {"offer": "10% Off",              "coupon": "BANANA10"},
            "milk":    {"offer": "Buy 2 Get 1 Free",     "coupon": "MILK21"},
            "bread":   {"offer": "Flat ₹10 Off",         "coupon": "BREAD10"},
            "eggs":    {"offer": "₹5 Off on dozen",      "coupon": "EGGS5"},
            "cheese":  {"offer": "15% Off",              "coupon": "CHEESE15"},
            "tomato":  {"offer": "Buy 1kg, Get 500g Free", "coupon": "TOMBOGO"},
            "potato":  {"offer": "₹2 Off per kg",        "coupon": "POTATO2"},
            "carrot":  {"offer": "Free with ₹500 Cart",  "coupon": "CARROTFREE"},
            "yogurt":  {"offer": "Buy 4, Pay for 3",      "coupon": "YOGURT143"},
            "chicken": {"offer": "Flat ₹30 Off",         "coupon": "CHICK30"},
            "beef":    {"offer": "₹50 Off 1kg Pack",      "coupon": "BEEF50"},
            "orange":  {"offer": "10% Off",              "coupon": "ORANGE10"},
            "grapes":  {"offer": "₹10 Off 500g",         "coupon": "GRAPE10"},
            "rice":    {"offer": "₹5 Off per kg",        "coupon": "RICE5"},
            "pasta":   {"offer": "Buy 2 Get 1",          "coupon": "PASTA21"},
            "cereal":  {"offer": "Free Spoon Set",       "coupon": "CEREALFREE"},
            "butter":  {"offer": "20% Off",              "coupon": "BUTTER20"},
            "juice":   {"offer": "₹10 Off 1L",           "coupon": "JUICE10"},
            "onion":   {"offer": "Buy 3kg, Pay for 2",   "coupon": "ONION32"},
        }

        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("Product", "Offer", "Coupon Code")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        tree.heading("Product", text="Product")
        tree.heading("Offer", text="Offer")
        tree.heading("Coupon Code", text="Coupon Code")

        tree.column("Product", width=150, anchor="w")
        tree.column("Offer", width=150, anchor="w")
        tree.column("Coupon Code", width=150, anchor="w")

        for product, info in offers_data.items():
            tree.insert("", "end", values=(product.title(), info["offer"], info["coupon"]))

        tree.pack(fill="both", expand=True)

        tk.Button(self, text="Back to Stock & Quality", command=lambda: controller.show_frame(StockAndQuality)).pack(pady=20)

class MonthlyReport(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        products = [
            {"name": "apple", "price": 100, "initial_stock": 100, "stock": 50},
            {"name": "banana", "price": 42, "initial_stock": 120, "stock": 80},
            {"name": "milk", "price": 208, "initial_stock": 90, "stock": 60},
            {"name": "bread", "price": 149, "initial_stock": 70, "stock": 40},
            {"name": "eggs", "price": 249, "initial_stock": 100, "stock": 70},
            {"name": "cheese", "price": 374, "initial_stock": 60, "stock": 30},
            {"name": "tomato", "price": 83, "initial_stock": 150, "stock": 90},
            {"name": "potato", "price": 58, "initial_stock": 160, "stock": 100},
            {"name": "carrot", "price": 75, "initial_stock": 80, "stock": 50},
            {"name": "yogurt", "price": 91, "initial_stock": 60, "stock": 40},
            {"name": "chicken", "price": 540, "initial_stock": 90, "stock": 60},
            {"name": "beef", "price": 623, "initial_stock": 50, "stock": 30},
            {"name": "orange", "price": 108, "initial_stock": 100, "stock": 70},
            {"name": "grapes", "price": 183, "initial_stock": 70, "stock": 50},
            {"name": "rice", "price": 166, "initial_stock": 120, "stock": 80},
            {"name": "pasta", "price": 125, "initial_stock": 100, "stock": 70},
            {"name": "cereal", "price": 266, "initial_stock": 60, "stock": 40},
            {"name": "butter", "price": 232, "initial_stock": 90, "stock": 60},
            {"name": "juice", "price": 199, "initial_stock": 70, "stock": 50},
            {"name": "onion", "price": 50, "initial_stock": 140, "stock": 90},
        ]

        tk.Label(self, text="🧾 Monthly Report", font=("Helvetica", 18, "bold"), bg="white").pack(pady=15)

        canvas = tk.Canvas(self, bg="white")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        back_btn = tk.Button(self, text="Back to Dashboard", command=lambda: self.controller.show_frame(EmployeeDashboard),
                             bg="#007acc", fg="white", font=('Arial', 10, 'bold'), relief="raised")
        back_btn.pack(pady=10, anchor="ne", padx=20)

        headers = ["Product", "Initial Stock", "Units Sold", "Remaining Stock", "Price", "Revenue"]
        for col, header in enumerate(headers):
            label = tk.Label(scroll_frame, text=header, font=('Arial', 10, 'bold'),
                             bg="#cce6ff", fg="black", borderwidth=1, relief="solid", width=18, padx=5, pady=5)
            label.grid(row=0, column=col, sticky="nsew")

        row_colors = ["#ffffff", "#f2f2f2"]

        for i, p in enumerate(products, start=1):
            sold = p["initial_stock"] - p["stock"]
            revenue = sold * p["price"]
            values = [p["name"], p["initial_stock"], sold, p["stock"], f"${p['price']:.2f}", f"${revenue:.2f}"]
            for col, val in enumerate(values):
                label = tk.Label(scroll_frame, text=val, font=('Arial', 10),
                                 bg=row_colors[i % 2], borderwidth=1, relief="solid", width=18, padx=5, pady=5)
                label.grid(row=i, column=col, sticky="nsew")

if __name__ == "__main__":
    print("Creating app...")
    app = DmartApp()
    print("Running mainloop...")
    app.mainloop()
