import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Food Mamy 🍔", page_icon="🍔", layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════════
#  OOP CLASSES
# ══════════════════════════════════════════════════════════════════

class MenuItem:
    restaurant_name = "Food Mamy"
    def __init__(self, item_id, name, price, category, preparation_time, emoji="🍽️", description=""):
        self.item_id = item_id
        self.name = name
        self.__price = price
        self.category = category
        self.preparation_time = preparation_time
        self.is_available = True
        self.emoji = emoji
        self.description = description
    def get_price(self):       return self.__price
    def set_price(self, p):
        if p > 0: self.__price = p; return True
        return False
    def set_availability(self, s): self.is_available = s
    def apply_discount(self, pct):
        if 0 < pct <= 100: self.__price -= self.__price * pct / 100; return True
        return False

class MainDish(MenuItem):
    def __init__(self, item_id, name, price, prep, portion, emoji, desc=""):
        super().__init__(item_id, name, price, "Main Dish", prep, emoji, desc)
        self.portion_size = portion
        self.extra = f"Portion: {portion}"

class Sandwich(MenuItem):
    def __init__(self, item_id, name, price, prep, bread_type, emoji, desc=""):
        super().__init__(item_id, name, price, "Sandwiches", prep, emoji, desc)
        self.bread_type = bread_type
        self.extra = f"Bread: {bread_type}"

class Breakfast(MenuItem):
    def __init__(self, item_id, name, price, prep, serves, emoji, desc=""):
        super().__init__(item_id, name, price, "Breakfast", prep, emoji, desc)
        self.serves = serves
        self.extra = f"Serves: {serves}"

class Drink(MenuItem):
    def __init__(self, item_id, name, price, prep, size, emoji, desc=""):
        super().__init__(item_id, name, price, "Drink", prep, emoji, desc)
        self.size = size
        self.extra = f"Size: {size}"

class Dessert(MenuItem):
    def __init__(self, item_id, name, price, prep, sweetness, emoji, desc=""):
        super().__init__(item_id, name, price, "Dessert", prep, emoji, desc)
        self.sweetness_level = sweetness
        self.extra = f"Sweetness: {sweetness}"

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []
    def add_item(self, item):    self.items.append(item)
    def remove_item(self, iid): self.items = [i for i in self.items if i.item_id != iid]
    def calculate_subtotal(self): return sum(i.get_price() for i in self.items)
    def calculate_tax(self, r=0.14): return self.calculate_subtotal() * r
    def calculate_delivery(self):
        sub = self.calculate_subtotal()
        return 0 if sub >= 1000 else 20
    def calculate_total(self, promo_discount=0):
        return max(self.calculate_subtotal() + self.calculate_tax() + self.calculate_delivery() - promo_discount, 0)

class RestaurantSystem:
    def __init__(self):
        self.menu = []
    def add_menu_item(self, item): self.menu.append(item)
    def get_by_category(self, cat): return [i for i in self.menu if i.category == cat and i.is_available]

# ══════════════════════════════════════════════════════════════════
#  PROMO CODES
# ══════════════════════════════════════════════════════════════════
PROMO_CODES = {
    "WELCOME10": {
        "discount": 10,
        "type": "percent",
        "label": "10% خصم لأول أوردر!",
        "condition": "first_order",
        "desc": "للعملاء الجدد فقط – أول أوردر بـ 10% خصم"
    },
    "BIG500": {
        "discount": 15,
        "type": "percent",
        "label": "15% خصم على الأوردرات فوق 500 جنيه!",
        "condition": "min_500",
        "desc": "لما الأوردر بتاعك يعدي 500 جنيه"
    },
}

def validate_promo(code, cart_subtotal, order_history):
    if code not in PROMO_CODES:
        return False, "❌ كود غلط، جرب WELCOME10 أو BIG500"
    info = PROMO_CODES[code]
    if info["condition"] == "first_order" and len(order_history) > 0:
        return False, "❌ الكود ده للعملاء الجدد بس – أول أوردر!"
    if info["condition"] == "min_500" and cart_subtotal < 500:
        return False, f"❌ الأوردر لازم يكون فوق 500 جنيه (حالياً {cart_subtotal:.0f} جنيه)"
    return True, info["label"]

def compute_promo_discount(code, cart_subtotal):
    if code not in PROMO_CODES:
        return 0
    info = PROMO_CODES[code]
    if info["type"] == "percent":
        return cart_subtotal * info["discount"] / 100
    return min(info["discount"], cart_subtotal)

# ══════════════════════════════════════════════════════════════════
#  MENU DATA
# ══════════════════════════════════════════════════════════════════
@st.cache_resource
def init_system():
    s = RestaurantSystem()
    s.add_menu_item(MainDish(1,  "Classic Burger",      120, 15, "Large",    "🍔", "Beef patty, lettuce, tomato, pickles"))
    s.add_menu_item(MainDish(2,  "Pepperoni Pizza",     200, 20, "Medium",   "🍕", "Crispy dough, mozzarella, pepperoni"))
    s.add_menu_item(MainDish(3,  "Crispy Chicken",      150, 18, "Large",    "🍗", "Golden fried chicken with coleslaw"))
    s.add_menu_item(MainDish(4,  "Pasta Alfredo",       130, 20, "Medium",   "🍝", "Creamy white sauce with mushrooms"))
    s.add_menu_item(MainDish(5,  "Grilled Steak",       280, 25, "Large",    "🥩", "Char-grilled sirloin, peppercorn sauce"))
    s.add_menu_item(MainDish(6,  "Chicken Shawarma",    110, 15, "Medium",   "🌯", "Garlic sauce, pickles, fries"))
    s.add_menu_item(MainDish(7,  "BBQ Ribs",            320, 30, "Large",    "🍖", "Slow-cooked ribs with BBQ glaze"))
    s.add_menu_item(MainDish(8,  "Koshary Special",      60, 10, "Large",    "🍛", "Lentils, rice, pasta, crispy onions"))
    s.add_menu_item(Sandwich(9,  "Club Sandwich",        90, 12, "Toast",    "🥪", "Chicken, egg, lettuce, cheese"))
    s.add_menu_item(Sandwich(10, "Falafel Wrap",          55,  8, "Pita",    "🧆", "Crispy falafel, tahini, fresh veggies"))
    s.add_menu_item(Sandwich(11, "Grilled Chicken Sub", 100, 14, "Sub Roll", "🥖", "Grilled chicken, jalapeños, mayo"))
    s.add_menu_item(Sandwich(12, "Kofta Baladi",         75, 12, "Aish",    "🫓", "Spiced kofta, tomatoes, onions"))
    s.add_menu_item(Breakfast(13,"Full English",        110, 20, "1 person", "🍳", "Eggs, beans, sausage, toast"))
    s.add_menu_item(Breakfast(14,"Ful & Tamiya Plate",   50, 10, "2 persons","🥚", "Classic Egyptian breakfast"))
    s.add_menu_item(Breakfast(15,"Pancake Stack",        80, 15, "1 person", "🥞", "Fluffy pancakes, maple syrup, butter"))
    s.add_menu_item(Breakfast(16,"Halloumi & Eggs",      95, 15, "1 person", "🧀", "Grilled halloumi, scrambled eggs"))
    s.add_menu_item(Drink(17,    "Cola",                  50,  5, "Small",   "🥤", "Ice cold classic"))
    s.add_menu_item(Drink(18,    "Fanta Orange",          50,  5, "Medium",  "🍊", "Fizzy and refreshing"))
    s.add_menu_item(Drink(19,    "Fresh Lemon Juice",     70,  8, "Large",   "🍋", "Freshly squeezed, mint optional"))
    s.add_menu_item(Drink(20,    "Mango Smoothie",        90, 10, "Medium",  "🥭", "100% fresh mango blended"))
    s.add_menu_item(Drink(21,    "Karkade Iced",          60,  8, "Large",   "🌺", "Hibiscus cold brew with sugar"))
    s.add_menu_item(Drink(22,    "Turkish Coffee",        45,  5, "Small",   "☕", "Rich & bold"))
    s.add_menu_item(Dessert(23,  "Chocolate Lava Cake",  90, 12, "High",    "🎂", "Warm cake, molten center"))
    s.add_menu_item(Dessert(24,  "Vanilla Ice Cream",    60,  5, "Medium",  "🍦", "3 scoops with wafer"))
    s.add_menu_item(Dessert(25,  "Kunafa Nabulsiyya",   100, 12, "High",    "🍯", "Cream-filled, crunchy, syrupy"))
    s.add_menu_item(Dessert(26,  "Om Ali",               80, 15, "Medium",  "🥛", "Egyptian bread pudding, nuts & cream"))
    s.add_menu_item(Dessert(27,  "Creme Brulee",        110, 18, "Low",     "🍮", "Classic French custard"))
    return s

system = init_system()

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
defaults = {
    "cart": Order(101),
    "order_placed": False,
    "active_tab": "menu",
    "show_animation": False,
    "promo_applied": None,
    "promo_discount": 0,
    "final_total": 0,
    "customer_name": "",
    "order_history": [],
    "next_order_id": 101,
    "checkout_step": 1,
    "dark_mode": True,   # ← NEW: default dark mode
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
#  THEME VARIABLES
# ══════════════════════════════════════════════════════════════════
is_dark = st.session_state.dark_mode

if is_dark:
    theme = {
        "surface":        "#0f0f0f",
        "card":           "#161616",
        "card_grad":      "linear-gradient(145deg, #1a1a1a, #111)",
        "border":         "#222",
        "border_rgb":     "34,34,34",
        "text":           "#f0ebe0",
        "muted":          "#666",
        "input_bg":       "#111",
        "input_border":   "#222",
        "input_text":     "#f0ebe0",
        "order_box_bg":   "#0d0d0d",
        "order_box_border":"#1e1e1e",
        "confirm_card_bg":"#0d0d0d",
        "hist_card_bg":   "#111",
        "stat_box_bg":    "#111",
        "total_row_border":"#151515",
        "total_grand_border":"#222",
        "cart_item_bg":   "#131313",
        "empty_col":      "#444",
        "empty_text_col": "#555",
        "empty_hist_col": "#333",
        "hr_col":         "#1a1a1a",
        "footer_col":     "#1e1e1e",
        "form_card_bg":   "#ffffff",
        "form_card_border":"#efefef",
        "form_card_shadow":"rgba(0,0,0,0.4)",
        "form_title_col": "#1a1a1a",
        "form_sub_col":   "#999",
        "form_border_col":"#f0f0f0",
        "form_label_col": "#333",
        "form_input_bg":  "#f7f7f7",
        "form_input_border":"#ddd",
        "form_input_text":"#111",
        "confirm_sec_col":"#444",
        "confirm_val_col":"#f0ebe0",
        "confirm_row_border":"#151515",
        "confirm_row_label":"#444",
        "hist_header_border":"#1a1a1a",
        "hist_items_col": "#666",
        "hist_detail_col":"#444",
        "step_circle_bg": "#111",
        "step_circle_border":"#222",
        "step_circle_col":"#333",
        "step_label_col": "#333",
        "progress_bg":    "#0d0d0d",
        "progress_border":"#1a1a1a",
        "step_line_bg":   "#1a1a1a",
        "select_bg":      "#111",
        "select_border":  "#222",
        "select_col":     "#f0ebe0",
        "tab_col":        "#666",
        "promo_card_bg":  "#111",
        "promo_card_border":"#1e1e1e",
        "promo_val_col":  "#444",
        "promo_note_col": "#444",
    }
else:
    theme = {
        "surface":        "#faf8f5",
        "card":           "#ffffff",
        "card_grad":      "linear-gradient(145deg, #ffffff, #f5f3f0)",
        "border":         "#e8e3da",
        "border_rgb":     "232,227,218",
        "text":           "#1a1512",
        "muted":          "#888",
        "input_bg":       "#f5f3f0",
        "input_border":   "#d5d0c8",
        "input_text":     "#1a1512",
        "order_box_bg":   "#ffffff",
        "order_box_border":"#e8e3da",
        "confirm_card_bg":"#ffffff",
        "hist_card_bg":   "#ffffff",
        "stat_box_bg":    "#ffffff",
        "total_row_border":"#f0ece5",
        "total_grand_border":"#e8e3da",
        "cart_item_bg":   "#f8f6f3",
        "empty_col":      "#bbb",
        "empty_text_col": "#999",
        "empty_hist_col": "#bbb",
        "hr_col":         "#e8e3da",
        "footer_col":     "#ccc",
        "form_card_bg":   "#ffffff",
        "form_card_border":"#e8e3da",
        "form_card_shadow":"rgba(0,0,0,0.06)",
        "form_title_col": "#1a1a1a",
        "form_sub_col":   "#999",
        "form_border_col":"#eee",
        "form_label_col": "#333",
        "form_input_bg":  "#f5f3f0",
        "form_input_border":"#d5d0c8",
        "form_input_text":"#111",
        "confirm_sec_col":"#888",
        "confirm_val_col":"#1a1512",
        "confirm_row_border":"#f0ece5",
        "confirm_row_label":"#888",
        "hist_header_border":"#f0ece5",
        "hist_items_col": "#666",
        "hist_detail_col":"#888",
        "step_circle_bg": "#f0ece5",
        "step_circle_border":"#ddd",
        "step_circle_col":"#aaa",
        "step_label_col": "#aaa",
        "progress_bg":    "#ffffff",
        "progress_border":"#e8e3da",
        "step_line_bg":   "#e8e3da",
        "select_bg":      "#ffffff",
        "select_border":  "#e0dbd0",
        "select_col":     "#1a1512",
        "tab_col":        "#888",
        "promo_card_bg":  "#ffffff",
        "promo_card_border":"#e8e3da",
        "promo_val_col":  "#888",
        "promo_note_col": "#aaa",
    }

# ══════════════════════════════════════════════════════════════════
#  CSS (theme-aware)
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Nunito:wght@400;600;700;800;900&display=swap');

:root {{
  --fire: #ff4500;
  --amber: #ff8c00;
  --gold: #ffd700;
  --surface: {theme["surface"]};
  --card: {theme["card"]};
  --border: {theme["border"]};
  --text: {theme["text"]};
  --muted: {theme["muted"]};
  --green: #22c55e;
}}

html, body, [class*="css"] {{
  font-family: 'Nunito', sans-serif;
  background: var(--surface);
  color: var(--text);
}}
.main, [data-testid="stAppViewContainer"] {{ background: var(--surface); }}
section[data-testid="stSidebar"] {{ display: none; }}
[data-testid="stHeader"] {{ background: transparent; }}

/* ─── THEME TOGGLE BUTTON ─── */
.theme-toggle-btn > button {{
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 15px !important;
  border-radius: 50px !important;
  border: 2px solid {theme["border"]} !important;
  background: {theme["card"]} !important;
  color: {theme["text"]} !important;
  padding: 8px 22px !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 2px 12px rgba(0,0,0,0.12) !important;
  width: auto !important;
}}
.theme-toggle-btn > button:hover {{
  border-color: var(--amber) !important;
  color: var(--amber) !important;
  transform: scale(1.05) !important;
  box-shadow: 0 4px 20px rgba(255,140,0,0.25) !important;
}}

/* ─── HERO ─── */
.hero-wrap {{
  background: linear-gradient(135deg, #1a0000 0%, #3d0000 30%, #7a1500 60%, #c44b00 100%);
  border-radius: 28px;
  padding: 60px 40px 52px;
  text-align: center;
  margin-bottom: 8px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(255,69,0,0.3);
  box-shadow: 0 0 80px rgba(255,69,0,0.25), inset 0 1px 0 rgba(255,255,255,0.07);
}}
.hero-wrap::before {{
  content: '';
  position: absolute;
  top: -40%; left: -40%;
  width: 180%; height: 180%;
  background: radial-gradient(ellipse at 50% 50%, rgba(255,140,0,0.12) 0%, transparent 60%);
  animation: pulse-glow 4s ease-in-out infinite;
}}
@keyframes pulse-glow {{
  0%,100%{{opacity:0.6;}} 50%{{opacity:1;}}
}}
.hero-title {{
  font-family: 'Bebas Neue', cursive;
  font-size: 96px;
  color: #fff;
  margin: 0;
  letter-spacing: 8px;
  text-shadow: 0 0 40px rgba(255,100,0,0.6), 0 4px 0 rgba(0,0,0,0.5);
  position: relative;
}}
.hero-flame {{
  font-size: 70px;
  display: inline-block;
  animation: flame-dance 1.5s ease-in-out infinite;
  vertical-align: middle;
}}
@keyframes flame-dance {{
  0%,100%{{transform:scale(1) rotate(-3deg);}}
  50%{{transform:scale(1.1) rotate(3deg);}}
}}
.hero-sub {{
  font-size: 17px;
  color: rgba(255,255,255,0.75);
  margin-top: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  position: relative;
}}
.hero-badges {{
  margin-top: 22px;
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
  position: relative;
}}
.hero-badge {{
  background: rgba(255,255,255,0.08);
  color: #fff;
  border-radius: 50px;
  padding: 7px 20px;
  font-size: 13px;
  font-weight: 800;
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(8px);
  transition: all 0.2s;
}}
.hero-badge:hover {{ background: rgba(255,69,0,0.3); border-color: var(--fire); }}

/* ─── NAV BUTTONS ─── */
div.stButton > button {{
  font-family: 'Nunito', sans-serif !important;
  font-weight: 800 !important;
  font-size: 14px !important;
  border-radius: 14px !important;
  border: 1px solid {theme["border"]} !important;
  background: {theme["card"]} !important;
  color: {theme["muted"]} !important;
  padding: 12px 20px !important;
  transition: all 0.2s !important;
  box-shadow: none !important;
  width: 100%;
}}
div.stButton > button:hover {{
  background: {theme["card"]} !important;
  border-color: {theme["border"]} !important;
  color: {theme["text"]} !important;
  transform: translateY(-1px) !important;
}}

.btn-fire > button {{
  background: linear-gradient(135deg, var(--fire), var(--amber)) !important;
  border-color: transparent !important;
  color: #fff !important;
  box-shadow: 0 4px 20px rgba(255,69,0,0.4) !important;
}}
.btn-fire > button:hover {{
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(255,69,0,0.55) !important;
  color: #fff !important;
}}
.btn-green > button {{
  background: linear-gradient(135deg, #16a34a, var(--green)) !important;
  border-color: transparent !important;
  color: #fff !important;
  box-shadow: 0 4px 20px rgba(34,197,94,0.35) !important;
  font-size: 17px !important;
  padding: 16px 28px !important;
}}
.btn-green > button:hover {{
  box-shadow: 0 8px 30px rgba(34,197,94,0.5) !important;
  color: #fff !important;
}}
.btn-ghost > button {{
  background: {theme["card"]} !important;
  color: {theme["muted"]} !important;
  border-color: {theme["border"]} !important;
}}
.btn-ghost > button:hover {{ color: {theme["text"]} !important; }}
.btn-danger > button {{
  background: {"#1a0000" if is_dark else "#fff0f0"} !important;
  color: #ff4444 !important;
  border-color: {"#2a0000" if is_dark else "#ffd0d0"} !important;
  font-size: 16px !important;
  padding: 10px !important;
}}
.btn-danger > button:hover {{
  background: {"#2a0000" if is_dark else "#ffe0e0"} !important;
  color: #ff6666 !important;
}}
.btn-promo > button {{
  background: linear-gradient(135deg, #16a34a, var(--green)) !important;
  border-color: transparent !important;
  color: #fff !important;
}}

/* ─── SECTION HEADING ─── */
.section-heading {{
  font-family: 'Bebas Neue', cursive;
  font-size: 42px;
  color: var(--amber);
  margin: 8px 0 22px;
  letter-spacing: 3px;
}}

/* ─── MENU CARDS ─── */
.menu-card {{
  background: {theme["card_grad"]};
  border: 1px solid {theme["border"]};
  border-radius: 20px;
  padding: 22px 18px 18px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}}
.menu-card::before {{
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,69,0,0.04), transparent);
  opacity: 0;
  transition: 0.3s;
}}
.menu-card:hover {{
  border-color: rgba(255,100,0,0.4);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(255,69,0,{"0.18" if is_dark else "0.10"});
}}
.menu-card:hover::before {{ opacity: 1; }}
.card-emoji {{ font-size: 52px; margin-bottom: 10px; display: block; filter: drop-shadow(0 4px 8px rgba(0,0,0,{"0.5" if is_dark else "0.15"})); }}
.card-name {{ font-size: 17px; font-weight: 900; color: {theme["text"]}; margin: 0 0 5px; }}
.card-desc {{ font-size: 12px; color: {theme["muted"]}; margin-bottom: 8px; line-height: 1.5; }}
.card-extra {{ font-size: 11px; color: {theme["muted"]}; margin-bottom: 6px; }}
.card-prep {{ font-size: 11px; color: {theme["muted"]}; margin-bottom: 12px; }}
.card-price {{
  font-family: 'Bebas Neue', cursive;
  font-size: 32px;
  color: var(--amber);
  margin-bottom: 14px;
  letter-spacing: 1px;
}}
.badge {{
  display: inline-block;
  background: rgba(255,69,0,0.15);
  color: #ff7744;
  border: 1px solid rgba(255,69,0,0.3);
  font-size: 10px;
  font-weight: 800;
  border-radius: 50px;
  padding: 3px 10px;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.badge-blue   {{ background: rgba(59,130,246,0.12); color: #60a5fa; border-color: rgba(59,130,246,0.25); }}
.badge-green  {{ background: rgba(34,197,94,0.12);  color: #4ade80; border-color: rgba(34,197,94,0.25); }}
.badge-purple {{ background: rgba(139,92,246,0.12); color: #a78bfa; border-color: rgba(139,92,246,0.25); }}
.badge-pink   {{ background: rgba(236,72,153,0.12); color: #f472b6; border-color: rgba(236,72,153,0.25); }}

/* ─── CART ITEMS ─── */
.cart-item {{
  background: {theme["cart_item_bg"]};
  border: 1px solid {theme["border"]};
  border-radius: 16px;
  padding: 14px 18px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: border-color 0.2s;
}}
.cart-item:hover {{ border-color: rgba({theme["border_rgb"]},0.6); }}
.cart-item-emoji {{ font-size: 34px; flex-shrink: 0; }}
.cart-item-info  {{ flex: 1; }}
.cart-item-name  {{ font-weight: 800; font-size: 15px; color: {theme["text"]}; }}
.cart-item-price {{ color: var(--amber); font-weight: 700; font-size: 13px; margin-top: 3px; }}

/* ─── PROGRESS BAR ─── */
.checkout-progress {{
  background: {theme["progress_bg"]};
  border: 1px solid {theme["progress_border"]};
  border-radius: 18px;
  padding: 22px 30px;
  margin-bottom: 28px;
}}
.progress-steps {{ display: flex; align-items: center; justify-content: center; }}
.step-item {{ display: flex; flex-direction: column; align-items: center; flex: 1; }}
.step-circle {{
  width: 48px; height: 48px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 900;
  border: 2px solid {theme["step_circle_border"]};
  background: {theme["step_circle_bg"]};
  color: {theme["step_circle_col"]};
  transition: all 0.3s;
  font-family: 'Nunito', sans-serif;
}}
.step-circle.active {{
  background: linear-gradient(135deg, var(--fire), var(--amber));
  border-color: var(--amber);
  color: #fff;
  box-shadow: 0 0 24px rgba(255,140,0,0.5);
}}
.step-circle.done {{ background: {"#0a1f0a" if is_dark else "#f0fff4"}; border-color: var(--green); color: var(--green); }}
.step-label {{ font-size: 11px; font-weight: 800; margin-top: 8px; color: {theme["step_label_col"]}; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }}
.step-label.active {{ color: var(--amber); }}
.step-label.done   {{ color: var(--green); }}
.step-line {{ flex: 1; height: 2px; background: {theme["step_line_bg"]}; margin: 0 6px 22px; border-radius: 2px; max-width: 80px; }}
.step-line.done   {{ background: var(--green); }}
.step-line.active {{ background: linear-gradient(90deg, var(--fire), var(--amber)); }}

/* ─── ORDER BOX ─── */
.order-box {{
  background: {theme["order_box_bg"]};
  border: 1px solid {theme["order_box_border"]};
  border-radius: 20px;
  padding: 24px;
  margin-top: 12px;
}}
.total-row {{
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: {theme["muted"]};
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid {theme["total_row_border"]};
}}
.total-row:last-of-type {{ border-bottom: none; }}
.total-grand {{
  display: flex;
  justify-content: space-between;
  font-family: 'Bebas Neue', cursive;
  font-size: 36px;
  color: var(--amber);
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid {theme["total_grand_border"]};
  letter-spacing: 1px;
}}
.promo-box {{
  background: {"#0a1f0a" if is_dark else "#f0fff4"};
  border: 1px solid {"#1a4a1a" if is_dark else "#86efac"};
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 12px;
  color: #4ade80;
  font-weight: 800;
  font-size: 14px;
}}
.promo-box span {{ color: {"#86efac" if is_dark else "#22c55e"}; font-size: 12px; font-weight: 600; display: block; margin-top: 3px; }}

/* ─── DELIVERY FORM CARDS ─── */
.form-card {{
  background: {theme["form_card_bg"]};
  border-radius: 18px;
  padding: 22px 24px;
  margin-bottom: 14px;
  border: 1.5px solid {theme["form_card_border"]};
  box-shadow: 0 4px 20px {theme["form_card_shadow"]};
}}
.form-card-header {{
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 16px; padding-bottom: 12px;
  border-bottom: 1.5px solid {theme["form_border_col"]};
}}
.form-card-icon {{
  width: 42px; height: 42px;
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}}
.form-card-icon.orange {{ background: linear-gradient(135deg, var(--fire), var(--amber)); }}
.form-card-icon.blue   {{ background: linear-gradient(135deg, #3b82f6, #60a5fa); }}
.form-card-icon.green  {{ background: linear-gradient(135deg, #16a34a, var(--green)); }}
.form-card-title {{ font-family: 'Bebas Neue', cursive; font-size: 20px; color: {theme["form_title_col"]}; letter-spacing: 1px; }}
.form-card-sub   {{ font-size: 12px; color: {theme["form_sub_col"]}; margin-top: 2px; }}

.form-card div[data-baseweb="input"] input,
.form-card div[data-baseweb="textarea"] textarea {{
  background: {theme["form_input_bg"]} !important;
  border-color: {theme["form_input_border"]} !important;
  color: {theme["form_input_text"]} !important;
  border-radius: 10px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  font-family: 'Nunito', sans-serif !important;
}}
.form-card label {{ color: {theme["form_label_col"]} !important; font-weight: 800 !important; font-size: 13px !important; }}

div[data-baseweb="input"] input {{
  background: {theme["input_bg"]} !important;
  border-color: {theme["input_border"]} !important;
  color: {theme["input_text"]} !important;
  border-radius: 10px !important;
}}

/* ─── CONFIRM CARD ─── */
.confirm-card {{
  background: {theme["confirm_card_bg"]};
  border: 1px solid {theme["order_box_border"]};
  border-radius: 18px;
  padding: 22px 24px;
  margin-bottom: 14px;
}}
.confirm-section-title {{
  font-size: 11px;
  font-weight: 800;
  color: {theme["confirm_sec_col"]};
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 14px;
}}
.confirm-row {{
  display: flex; align-items: center; gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid {theme["confirm_row_border"]};
}}
.confirm-row:last-child {{ border-bottom: none; }}
.confirm-row-icon  {{ font-size: 18px; flex-shrink: 0; }}
.confirm-row-label {{ font-size: 11px; color: {theme["confirm_row_label"]}; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; }}
.confirm-row-value {{ font-size: 15px; color: {theme["confirm_val_col"]}; font-weight: 800; margin-top: 2px; }}

/* ─── BANNERS ─── */
.free-delivery-banner {{
  background: {"linear-gradient(90deg, #0a1f0a, #122a14)" if is_dark else "linear-gradient(90deg, #f0fff4, #dcfce7)"};
  border: 1px solid {"#1a4a1a" if is_dark else "#86efac"};
  border-radius: 12px; padding: 12px 18px;
  margin-bottom: 12px; color: {"#4ade80" if is_dark else "#16a34a"};
  font-size: 13px; font-weight: 800; text-align: center;
}}
.delivery-warn {{
  background: {"#110d00" if is_dark else "#fffbeb"};
  border: 1px solid {"#3a2800" if is_dark else "#fcd34d"};
  border-radius: 12px; padding: 12px 18px;
  margin-bottom: 12px; color: {"#fbbf24" if is_dark else "#d97706"};
  font-size: 13px; font-weight: 700; text-align: center;
}}
.empty-cart {{ text-align: center; padding: 60px 20px; color: {theme["empty_col"]}; }}
.empty-cart-icon {{ font-size: 80px; margin-bottom: 14px; }}
.empty-cart-text {{ font-size: 20px; font-weight: 800; color: {theme["empty_text_col"]}; }}

/* ─── HISTORY ─── */
.history-card {{
  background: {theme["hist_card_bg"]};
  border: 1px solid {theme["order_box_border"]};
  border-radius: 18px;
  padding: 20px 22px;
  margin-bottom: 12px;
  transition: border-color 0.2s;
}}
.history-card:hover {{ border-color: rgba(255,100,0,0.3); }}
.history-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
.history-order-id {{ font-family: 'Bebas Neue', cursive; font-size: 22px; color: var(--amber); letter-spacing: 1px; }}
.history-date  {{ font-size: 12px; color: {theme["hist_detail_col"]}; }}
.history-items {{ font-size: 13px; color: {theme["hist_items_col"]}; margin-bottom: 8px; line-height: 1.6; }}
.history-footer {{
  display: flex; justify-content: space-between; align-items: center;
  border-top: 1px solid {theme["hist_header_border"]}; padding-top: 10px;
}}
.history-total  {{ font-family: 'Bebas Neue', cursive; font-size: 24px; color: {theme["text"]}; }}
.history-status {{
  background: {"#0a1f0a" if is_dark else "#f0fff4"}; color: var(--green);
  border: 1px solid {"#1a4a1a" if is_dark else "#86efac"};
  border-radius: 50px; padding: 4px 14px;
  font-size: 11px; font-weight: 800;
}}
.empty-history {{ text-align: center; padding: 70px 20px; color: {theme["empty_hist_col"]}; }}

/* ─── STATS BOX ─── */
.stat-box {{
  background: {theme["stat_box_bg"]};
  border: 1px solid {theme["order_box_border"]};
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  transition: border-color 0.2s;
}}
.stat-box:hover {{ border-color: rgba(255,100,0,0.3); }}
.stat-label {{ font-size: 12px; color: {theme["muted"]}; margin-bottom: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
.stat-value {{ font-family: 'Bebas Neue', cursive; font-size: 36px; color: var(--amber); letter-spacing: 2px; }}

/* ─── ANIMATIONS ─── */
@keyframes road-scroll {{ from{{background-position:0 0;}} to{{background-position:-200px 0;}} }}
@keyframes bike-ride   {{ 0%{{left:-160px;}} 100%{{left:110%;}} }}
@keyframes confetti-fall {{
  0%   {{ transform: translateY(-30px) rotate(0deg); opacity: 1; }}
  100% {{ transform: translateY(110vh) rotate(720deg); opacity: 0; }}
}}
@keyframes pop-in {{
  0%  {{ transform: scale(0.3); opacity: 0; }}
  70% {{ transform: scale(1.12); }}
  100%{{ transform: scale(1); opacity: 1; }}
}}
@keyframes slide-up {{
  from {{ transform: translateY(40px); opacity: 0; }}
  to   {{ transform: translateY(0); opacity: 1; }}
}}

/* ─── SUCCESS SCENE ─── */
.delivery-scene {{
  position: fixed; bottom: 0; left: 0;
  width: 100%; height: 180px;
  z-index: 9999; pointer-events: none; overflow: hidden;
}}
.road {{
  position: absolute; bottom: 0; left: 0; width: 100%; height: 90px;
  background: repeating-linear-gradient(90deg,
    #111 0px, #111 60px, var(--amber) 60px,
    var(--amber) 80px, #111 80px, #111 140px);
  animation: road-scroll 0.4s linear infinite;
  border-top: 3px solid #222;
}}
.bike {{
  position: absolute; bottom: 62px; left: -160px;
  animation: bike-ride 3.4s cubic-bezier(.25,0,.6,1) forwards;
  font-size: 70px; line-height: 1;
}}
.confetti-piece {{
  position: fixed; border-radius: 2px;
  animation: confetti-fall linear forwards;
  z-index: 10000;
}}
.success-scene {{
  background: {"linear-gradient(135deg, #060f06, #0a2010)" if is_dark else "linear-gradient(135deg, #f0fff4, #dcfce7)"};
  border: 1px solid {"#1a4a1a" if is_dark else "#86efac"};
  border-radius: 24px; padding: 50px 30px; text-align: center;
  box-shadow: 0 20px 80px rgba(34,197,94,{"0.2" if is_dark else "0.1"});
  animation: pop-in .5s ease forwards;
  position: relative; overflow: hidden;
}}
.success-scene::before {{
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(34,197,94,0.08), transparent 60%);
}}
.success-icon  {{ font-size: 90px; display: block; position: relative; }}
.success-title {{
  font-family: 'Bebas Neue', cursive;
  font-size: 58px; color: {"#fff" if is_dark else "#1a1512"}; margin: 16px 0 8px;
  letter-spacing: 4px;
  animation: slide-up .6s .15s ease both;
  position: relative;
}}
.success-sub {{
  font-size: 17px; color: {"rgba(255,255,255,0.8)" if is_dark else "#444"};
  animation: slide-up .6s .3s ease both;
  position: relative; line-height: 1.7;
}}
.order-id-tag {{
  display: inline-block;
  background: rgba(34,197,94,0.15);
  color: {"#4ade80" if is_dark else "#16a34a"};
  border: 1px solid rgba(34,197,94,0.3);
  border-radius: 50px; padding: 7px 22px;
  font-weight: 800; font-size: 14px;
  margin-top: 18px;
  animation: slide-up .6s .45s ease both;
  position: relative;
}}

/* Tabs */
button[data-baseweb="tab"] {{ font-weight: 700; font-family: 'Nunito', sans-serif; color: {theme["tab_col"]}; }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: var(--amber) !important; }}

/* Selectbox */
div[data-baseweb="select"] > div {{
  background: {theme["select_bg"]} !important;
  border-color: {theme["select_border"]} !important;
  color: {theme["select_col"]} !important;
  border-radius: 12px !important;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  ANIMATION HTML
# ══════════════════════════════════════════════════════════════════
DELIVERY_ANIM = """
<div class="delivery-scene">
  <div class="road"></div>
  <div class="bike">🛵</div>
</div>
<script>
(function(){
  var colors=['#ff4500','#ff8c00','#ffd700','#22c55e','#3b82f6','#ec4899','#ffffff','#a855f7'];
  for(var i=0;i<70;i++){
    var el=document.createElement('div');
    el.className='confetti-piece';
    el.style.left=Math.random()*100+'vw';
    el.style.top='-20px';
    el.style.background=colors[Math.floor(Math.random()*colors.length)];
    el.style.width=(5+Math.random()*12)+'px';
    el.style.height=(5+Math.random()*12)+'px';
    el.style.animationDuration=(2.5+Math.random()*3)+'s';
    el.style.animationDelay=(Math.random()*2.5)+'s';
    document.body.appendChild(el);
  }
})();
</script>
"""

# ══════════════════════════════════════════════════════════════════
#  PROGRESS BAR
# ══════════════════════════════════════════════════════════════════
def render_progress_bar(current_step):
    steps = [("🛒", "Review Cart"), ("📍", "Delivery Info"), ("✅", "Confirm")]
    circles = ""
    for i, (icon, label) in enumerate(steps):
        sn = i + 1
        if sn < current_step:
            c, l, display = "done", "done", "✓"
        elif sn == current_step:
            c, l, display = "active", "active", icon
        else:
            c, l, display = "", "", icon
        circles += f'<div class="step-item"><div class="step-circle {c}">{display}</div><div class="step-label {l}">{label}</div></div>'
        if i < len(steps) - 1:
            lc = "done" if current_step > i + 1 else ("active" if current_step == i + 1 else "")
            circles += f'<div class="step-line {lc}"></div>'
    st.markdown(f'<div class="checkout-progress"><div class="progress-steps">{circles}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HERO + THEME TOGGLE
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">
    <span class="hero-flame">🔥</span> FOOD MAMY <span class="hero-flame">🔥</span>
  </div>
  <div class="hero-sub">Fresh · Fast · Fired Up — Best in Town</div>
  <div class="hero-badges">
    <span class="hero-badge">🚀 30-min delivery</span>
    <span class="hero-badge">🛵 Delivery 20 EGP</span>
    <span class="hero-badge">🎁 Free delivery over 1000 EGP</span>
    <span class="hero-badge">⭐ 4.9 rating</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── THEME TOGGLE ROW ──
t_col, _ = st.columns([1, 5])
with t_col:
    toggle_icon  = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
    st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
    if st.button(toggle_icon, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  NAV
# ══════════════════════════════════════════════════════════════════
cart_count    = len(st.session_state.cart.items)
history_count = len(st.session_state.order_history)

c1, c2, c3, c4 = st.columns(4)
with c1:
    active_menu = st.session_state.active_tab == "menu"
    st.markdown('<div class="btn-fire">' if active_menu else '<div>', unsafe_allow_html=True)
    if st.button("🍽️  Menu", use_container_width=True):
        st.session_state.active_tab = "menu"
        st.session_state.order_placed = False
        st.session_state.checkout_step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    label = f"🛒  Cart  ·  {cart_count}" if cart_count else "🛒  Cart"
    active_cart = st.session_state.active_tab == "cart"
    st.markdown('<div class="btn-fire">' if active_cart else '<div>', unsafe_allow_html=True)
    if st.button(label, use_container_width=True):
        st.session_state.active_tab = "cart"
        st.session_state.order_placed = False
        st.session_state.checkout_step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    active_promo = st.session_state.active_tab == "promo"
    st.markdown('<div class="btn-fire">' if active_promo else '<div>', unsafe_allow_html=True)
    if st.button("🏷️  Promo Codes", use_container_width=True):
        st.session_state.active_tab = "promo"
        st.session_state.order_placed = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with c4:
    hlabel = f"📋  Orders  ·  {history_count}" if history_count else "📋  My Orders"
    active_hist = st.session_state.active_tab == "history"
    st.markdown('<div class="btn-fire">' if active_hist else '<div>', unsafe_allow_html=True)
    if st.button(hlabel, use_container_width=True):
        st.session_state.active_tab = "history"
        st.session_state.order_placed = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<hr style='border-color:{theme['hr_col']};margin:8px 0 28px;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  MENU TAB
# ══════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "menu":
    CATEGORIES = [
        ("Main Dish",  "🍛 Main Dishes",  "badge"),
        ("Sandwiches", "🥪 Sandwiches",   "badge badge-purple"),
        ("Breakfast",  "🌅 Breakfast",    "badge badge-pink"),
        ("Drink",      "🥤 Drinks",       "badge badge-blue"),
        ("Dessert",    "🍰 Desserts",     "badge badge-green"),
    ]
    filter_cat = st.selectbox(
        "", ["🍽️ All Categories"] + [c[1] for c in CATEGORIES],
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)

    for cat_key, cat_label, badge_cls in CATEGORIES:
        if filter_cat != "🍽️ All Categories" and filter_cat != cat_label:
            continue
        items = system.get_by_category(cat_key)
        if not items:
            continue
        st.markdown(f'<div class="section-heading">{cat_label}</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for idx, item in enumerate(items):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="menu-card">
                  <span class="card-emoji">{item.emoji}</span>
                  <div class="card-name">{item.name}</div>
                  <div class="card-desc">{item.description}</div>
                  <div class="card-extra">{getattr(item,'extra','')}</div>
                  <div class="card-prep">⏱ {item.preparation_time} min</div>
                  <span class="{badge_cls}">{item.category}</span>
                  <div class="card-price">{item.get_price():.0f} EGP</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
                if st.button("🛒 Add to Cart", key=f"add_{item.item_id}", use_container_width=True):
                    st.session_state.cart.add_item(item)
                    st.toast(f"{item.emoji} {item.name} added!", icon="✅")
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  PROMO CODES TAB
# ══════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "promo":
    st.markdown('<div class="section-heading">🏷️ Promo Codes</div>', unsafe_allow_html=True)
    col_l, col_r = st.columns([2, 3], gap="large")

    with col_l:
        st.markdown("#### Enter your code")
        promo_input = st.text_input(
            "", placeholder="WELCOME10 أو BIG500",
            label_visibility="collapsed"
        ).strip().upper()

        st.markdown('<div class="btn-promo">', unsafe_allow_html=True)
        if st.button("✅  Apply Code", use_container_width=True):
            if promo_input == "":
                st.warning("اكتب الكود الأول!")
            else:
                cart_sub = st.session_state.cart.calculate_subtotal()
                ok, msg = validate_promo(promo_input, cart_sub, st.session_state.order_history)
                if ok:
                    st.session_state.promo_applied  = promo_input
                    st.session_state.promo_discount = compute_promo_discount(promo_input, cart_sub)
                    st.success(f"🎉 {msg}")
                    st.balloons()
                else:
                    st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.promo_applied:
            info = PROMO_CODES[st.session_state.promo_applied]
            st.markdown(f"""
            <div class="promo-box">
              🏷️ Active: <strong>{st.session_state.promo_applied}</strong>
              <span>{info['label']} · وفّرت {st.session_state.promo_discount:.0f} جنيه</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✕ Remove promo", key="remove_promo"):
                st.session_state.promo_applied  = None
                st.session_state.promo_discount = 0
                st.rerun()

    with col_r:
        st.markdown("#### 🎁 الكودات المتاحة")
        descriptions = {
            "WELCOME10": ("🆕", "للعملاء الجدد فقط", "أول أوردر بخصم 10%"),
            "BIG500":    ("💰", "أوردر فوق 1500 جنيه", "خصم 15% على الأوردرات الكبيرة"),
        }
        for code, info in PROMO_CODES.items():
            icon, cond, note = descriptions[code]
            disc_str = f"{info['discount']}%" if info["type"] == "percent" else f"{info['discount']} EGP"
            active_dot = "🟢 " if st.session_state.promo_applied == code else ""
            st.markdown(f"""
            <div style="background:{theme['promo_card_bg']};border:1px solid {theme['promo_card_border']};border-radius:16px;
              padding:18px 20px;margin-bottom:12px;display:flex;align-items:center;gap:16px;
              transition:border-color 0.2s;">
              <div style="font-size:38px;">{icon}</div>
              <div style="flex:1;">
                <div style="font-family:'Bebas Neue',cursive;font-size:24px;color:#ff8c00;letter-spacing:1px;">{active_dot}{code}</div>
                <div style="color:{theme['promo_val_col']};font-size:13px;margin-top:2px;">{cond}</div>
                <div style="color:{theme['promo_note_col']};font-size:12px;">{note}</div>
              </div>
              <div style="font-family:'Bebas Neue',cursive;font-size:28px;color:#22c55e;letter-spacing:1px;">{disc_str} OFF</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  CART TAB — 3-STEP CHECKOUT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "cart" and not st.session_state.order_placed:

    cart = st.session_state.cart
    step = st.session_state.checkout_step

    if not cart.items:
        st.markdown(f"""
        <div class="empty-cart">
          <div class="empty-cart-icon">🛒</div>
          <div class="empty-cart-text">Your cart is empty!</div>
          <p style="color:{theme['muted']};margin-top:8px;">Head to the menu and add something delicious 🍔</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_progress_bar(step)

        subtotal  = cart.calculate_subtotal()
        tax       = cart.calculate_tax()
        delivery  = cart.calculate_delivery()
        promo_off = st.session_state.promo_discount
        total     = cart.calculate_total(promo_off)

        def order_summary_html(delivery, subtotal, tax, promo_off, total, items_count, promo_applied, title="🧾 Order Summary"):
            delivery_label = '<span style="color:#22c55e;">FREE 🎉</span>' if delivery == 0 else f'{delivery:.0f} EGP'
            promo_row = ""
            if promo_off > 0:
                promo_row = f'<div class="total-row"><span>🏷️ Promo ({promo_applied})</span><span style="color:#22c55e;">- {promo_off:.0f} EGP</span></div>'
            return f"""
            <div class="order-box">
              <div style="font-family:'Bebas Neue',cursive;font-size:22px;color:{theme['text']};margin-bottom:18px;letter-spacing:1px;">{title}</div>
              <div class="total-row"><span>Subtotal ({items_count} items)</span><span style="color:{theme['text']};font-weight:800;">{subtotal:.0f} EGP</span></div>
              <div class="total-row"><span>Tax (14%)</span><span>{tax:.0f} EGP</span></div>
              <div class="total-row"><span>Delivery 🛵</span><span>{delivery_label}</span></div>
              {promo_row}
              <div class="total-grand"><span>TOTAL</span><span>{total:.0f} EGP</span></div>
            </div>
            """

        # ══ STEP 1: REVIEW CART ══
        if step == 1:
            st.markdown('<div class="section-heading">🛒 Review Your Order</div>', unsafe_allow_html=True)
            left, right = st.columns([3, 2], gap="large")

            with left:
                for i, item in enumerate(list(cart.items)):
                    ci, cd = st.columns([6, 1])
                    with ci:
                        st.markdown(f"""
                        <div class="cart-item">
                          <div class="cart-item-emoji">{item.emoji}</div>
                          <div class="cart-item-info">
                            <div class="cart-item-name">{item.name}</div>
                            <div class="cart-item-price">{item.get_price():.0f} EGP &nbsp;·&nbsp; ⏱ {item.preparation_time} min</div>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with cd:
                        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
                        if st.button("✕", key=f"del_{i}_{item.item_id}"):
                            cart.remove_item(item.item_id)
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

            with right:
                if delivery == 0:
                    st.markdown('<div class="free-delivery-banner">🎉 التوصيل مجاني! (فوق 1000 جنيه)</div>', unsafe_allow_html=True)
                else:
                    remaining = 1000 - subtotal
                    st.markdown(f'<div class="delivery-warn">🛵 توصيل 20 جنيه · أضف {remaining:.0f} جنيه وخلّيه مجاني!</div>', unsafe_allow_html=True)

                st.markdown(order_summary_html(delivery, subtotal, tax, promo_off, total, len(cart.items), st.session_state.promo_applied), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
                if st.button("📍 Next: Delivery Info →", use_container_width=True, key="next_step1"):
                    st.session_state.checkout_step = 2; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # ══ STEP 2: DELIVERY INFO ══
        elif step == 2:
            st.markdown('<div class="section-heading">📍 Delivery Details</div>', unsafe_allow_html=True)
            left, right = st.columns([3, 2], gap="large")

            with left:
                st.markdown("""
                <div class="form-card">
                  <div class="form-card-header">
                    <div class="form-card-icon orange">👤</div>
                    <div>
                      <div class="form-card-title">Your Name</div>
                      <div class="form-card-sub">اسمك الكامل للتعامل مع الديليفري</div>
                    </div>
                  </div>
                """, unsafe_allow_html=True)
                name = st.text_input("Full Name", placeholder="Ahmed Mohamed", key="inp_name")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""
                <div class="form-card">
                  <div class="form-card-header">
                    <div class="form-card-icon blue">📍</div>
                    <div>
                      <div class="form-card-title">Delivery Address</div>
                      <div class="form-card-sub">عنوان التوصيل بالتفصيل</div>
                    </div>
                  </div>
                """, unsafe_allow_html=True)
                address = st.text_input("Street, Building, Apartment", placeholder="12 شارع النيل، الدور 3، شقة 7، القاهرة", key="inp_address")
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("""
                <div class="form-card">
                  <div class="form-card-header">
                    <div class="form-card-icon green">📞</div>
                    <div>
                      <div class="form-card-title">Phone Number</div>
                      <div class="form-card-sub">رقم تليفونك عشان الديليفري يتصل بيك</div>
                    </div>
                  </div>
                """, unsafe_allow_html=True)
                phone = st.text_input("Mobile Number", placeholder="01012345678", key="inp_phone")
                st.markdown("</div>", unsafe_allow_html=True)

            with right:
                st.markdown(order_summary_html(delivery, subtotal, tax, promo_off, total, len(cart.items), st.session_state.promo_applied), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                bc, nc = st.columns(2)
                with bc:
                    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
                    if st.button("← Back", use_container_width=True, key="back_step2"):
                        st.session_state.checkout_step = 1; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with nc:
                    st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
                    if st.button("✅ Review Order →", use_container_width=True, key="next_step2"):
                        import re
                        errors = []
                        if not name.strip():    errors.append("⚠️ اكتب اسمك!")
                        if not address.strip(): errors.append("⚠️ اكتب عنوانك!")
                        if not phone.strip():
                            errors.append("⚠️ اكتب رقم التليفون!")
                        else:
                            clean = re.sub(r'[\s\-]', '', phone.strip())
                            if not re.match(r'^(01[0-9]{9}|(\+2)?01[0-9]{9})$', clean):
                                errors.append("⚠️ رقم غلط! لازم يبدأ بـ 01 ويكون 11 رقم")
                        if errors:
                            for e in errors: st.error(e)
                        else:
                            st.session_state["saved_name"]    = name.strip()
                            st.session_state["saved_address"] = address.strip()
                            st.session_state["saved_phone"]   = phone.strip()
                            st.session_state.checkout_step = 3; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

        # ══ STEP 3: CONFIRM ══
        elif step == 3:
            st.markdown('<div class="section-heading">✅ Confirm Your Order</div>', unsafe_allow_html=True)

            sname    = st.session_state.get("saved_name", "")
            saddress = st.session_state.get("saved_address", "")
            sphone   = st.session_state.get("saved_phone", "")

            left, right = st.columns([3, 2], gap="large")

            with left:
                st.markdown(f"""
                <div class="confirm-card">
                  <div class="confirm-section-title">📍 Delivery Info</div>
                  <div class="confirm-row">
                    <div class="confirm-row-icon">👤</div>
                    <div><div class="confirm-row-label">Name</div><div class="confirm-row-value">{sname}</div></div>
                  </div>
                  <div class="confirm-row">
                    <div class="confirm-row-icon">📍</div>
                    <div><div class="confirm-row-label">Address</div><div class="confirm-row-value">{saddress}</div></div>
                  </div>
                  <div class="confirm-row">
                    <div class="confirm-row-icon">📞</div>
                    <div><div class="confirm-row-label">Phone</div><div class="confirm-row-value">{sphone}</div></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                items_html = "".join([
                    f'<span style="display:inline-block;background:{theme["cart_item_bg"]};border:1px solid {theme["border"]};'
                    f'border-radius:8px;padding:5px 12px;margin:4px;font-size:14px;font-weight:700;color:{theme["text"]};">'
                    f'{item.emoji} {item.name}</span>'
                    for item in cart.items
                ])

                st.markdown(f"""
                <div class="confirm-card">
                  <div class="confirm-section-title">🍽️ Order Items ({len(cart.items)})</div>
                  <div style="line-height:2;">{items_html}</div>
                </div>
                """, unsafe_allow_html=True)

            with right:
                st.markdown(order_summary_html(delivery, subtotal, tax, promo_off, total, len(cart.items), st.session_state.promo_applied, title="🧾 Final Total"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                bc2, nc2 = st.columns(2)
                with bc2:
                    st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
                    if st.button("← Edit Info", use_container_width=True, key="back_step3"):
                        st.session_state.checkout_step = 2; st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                with nc2:
                    st.markdown('<div class="btn-green">', unsafe_allow_html=True)
                    if st.button("🚀 Place Order!", use_container_width=True, key="place_order"):
                        with st.spinner("🍳 Sending your order to the kitchen..."):
                            time.sleep(1.2)
                        order_snapshot = {
                            "order_id":       st.session_state.cart.order_id,
                            "name":           sname,
                            "phone":          sphone,
                            "address":        saddress,
                            "items":          [(i.emoji, i.name, i.get_price()) for i in cart.items],
                            "subtotal":       subtotal,
                            "tax":            tax,
                            "delivery":       delivery,
                            "promo":          st.session_state.promo_applied,
                            "promo_discount": promo_off,
                            "total":          total,
                            "timestamp":      datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "status":         "🛵 On the way",
                        }
                        st.session_state.order_history.append(order_snapshot)
                        st.session_state.order_placed   = True
                        st.session_state.show_animation = True
                        st.session_state.customer_name  = sname
                        st.session_state.final_total    = total
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  ORDER SUCCESS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "cart" and st.session_state.order_placed:

    if st.session_state.show_animation:
        st.markdown(DELIVERY_ANIM, unsafe_allow_html=True)
        st.session_state.show_animation = False

    total = st.session_state.final_total
    name  = st.session_state.customer_name
    oid   = st.session_state.cart.order_id

    st.markdown(f"""
    <div class="success-scene">
      <span class="success-icon">🎉</span>
      <div class="success-title">Order on its Way!</div>
      <div class="success-sub">
        Thank you, <strong>{name}</strong>! Your food is being prepared right now.<br>
        Estimated delivery: <strong>~30 minutes</strong><br><br>
        Total charged: <strong style="color:{'#4ade80' if is_dark else '#16a34a'};">{total:.0f} EGP</strong>
      </div>
      <div class="order-id-tag">Order #{oid} &nbsp;·&nbsp; 🛵 Rider assigned</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="btn-fire">', unsafe_allow_html=True)
    if st.button("🍔 Place New Order", use_container_width=True, key="new_order"):
        st.session_state.next_order_id += 1
        st.session_state.cart           = Order(st.session_state.next_order_id)
        st.session_state.order_placed   = False
        st.session_state.promo_applied  = None
        st.session_state.promo_discount = 0
        st.session_state.checkout_step  = 1
        st.session_state.active_tab     = "menu"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  ORDER HISTORY TAB
# ══════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "history":
    st.markdown('<div class="section-heading">📋 طلباتي</div>', unsafe_allow_html=True)
    history = st.session_state.order_history

    if not history:
        st.markdown(f"""
        <div class="empty-history">
          <div style="font-size:72px;margin-bottom:16px;">📋</div>
          <div style="font-size:22px;font-weight:800;color:{theme['empty_hist_col']};">مفيش طلبات لحد دلوقتي!</div>
          <p style="color:{theme['muted']};margin-top:8px;">اطلب أول أوردر من المنيو 🍔</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_spent = sum(o["total"] for o in history)
        avg = total_spent / len(history) if history else 0
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="stat-box">
              <div class="stat-label">إجمالي الطلبات</div>
              <div class="stat-value">{len(history)}</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="stat-box">
              <div class="stat-label">إجمالي الإنفاق</div>
              <div class="stat-value">{total_spent:.0f} EGP</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="stat-box">
              <div class="stat-label">متوسط الأوردر</div>
              <div class="stat-value">{avg:.0f} EGP</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for order in reversed(history):
            items_str    = " · ".join([f"{e} {n}" for e, n, _ in order["items"]])
            promo_str    = f"🏷️ {order['promo']} (وفّرت {order['promo_discount']:.0f} جنيه)" if order["promo"] else "بدون كود"
            delivery_str = "مجاني 🎉" if order["delivery"] == 0 else f"{order['delivery']:.0f} جنيه"
            st.markdown(f"""
            <div class="history-card">
              <div class="history-header">
                <div class="history-order-id">Order #{order['order_id']}</div>
                <div class="history-date">🕐 {order['timestamp']}</div>
              </div>
              <div class="history-items">{items_str}</div>
              <div style="font-size:12px;color:{theme['hist_detail_col']};margin-bottom:10px;">
                👤 {order['name']} &nbsp;·&nbsp; 📞 {order['phone']} &nbsp;·&nbsp; 📍 {order['address']}<br>
                🛵 توصيل: {delivery_str} &nbsp;·&nbsp; {promo_str}
              </div>
              <div class="history-footer">
                <div class="history-total">{order['total']:.0f} EGP</div>
                <div class="history-status">{order['status']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div style='text-align:center;margin-top:70px;color:{theme['footer_col']};font-size:12px;padding-bottom:30px;'>
  🍔 Food Mamy · Built with OOP Python 🐍 · Powered by Streamlit
</div>
""", unsafe_allow_html=True)