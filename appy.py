import streamlit as st
import json
import os

# --- ملف البيانات ---
FILE_PATH = 'inventory.json'

# --- دوال التعامل مع الملف ---
def load_inventory():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            # نقرأ الملف ونعود بقائمة فارغة إذا كان فارغاً
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_inventory(inventory):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)

# --- تحميل البيانات في بداية الجلسة ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = load_inventory()

# --- واجهة التطبيق ---
st.set_page_config(layout="wide", page_title="نظام المخزون - هنان")

st.title("نظام إدارة المخزون الاحترافي")
st.write("---")

# --- قائمة جانبية للإجراءات ---
menu = ["عرض المنتجات", "إضافة منتج", "بحث وتعديل وحذف"]
choice = st.sidebar.selectbox("القائمة", menu)

# --- منطق العرض ---
if choice == "عرض المنتجات":
    st.subheader("جميع المنتجات في المخزون")
    if not st.session_state.inventory:
        st.warning("المخزون فارغ حالياً.")
    else:
        st.table(st.session_state.inventory)

# --- منطق الإضافة ---
elif choice == "إضافة منتج":
    st.subheader("إضافة منتج جديد")
    with st.form(key='add_form', clear_on_submit=True):
        name = st.text_input("اسم المنتج")
        quantity = st.number_input("الكمية", min_value=0, step=1)
        price = st.number_input("السعر", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label='✨ إضافة المنتج')

        if submit_button:
            if not name:
                st.error("الرجاء إدخال اسم المنتج.")
            else:
                new_product = {'name': name, 'quantity': int(quantity), 'price': float(price)}
                st.session_state.inventory.append(new_product)
                save_inventory(st.session_state.inventory)
                st.success(f"تمت إضافة المنتج '{name}' بنجاح!")
                st.rerun()

# --- منطق البحث والتعديل والحذف ---
elif choice == "بحث وتعديل وحذف":
    st.subheader("البحث عن منتج، تعديله أو حذفه")
    search_term = st.text_input("اكتب اسم المنتج للبحث")

    if not st.session_state.inventory:
        st.warning("المخزون فارغ، لا يوجد شيء للبحث فيه.")
    else:
        # استخدام enumerate للحصول على الفهرس والمنتج معاً
        for i, product in enumerate(st.session_state.inventory):
            if search_term.lower() in product['name'].lower():
                
                st.write(f"المنتج: {product['name']} | الكمية: {product['quantity']} | السعر: {product['price']}")
                
                # استخدام expander لنموذج التعديل
                with st.expander("✏️ تعديل هذا المنتج"):
                    with st.form(key=f"edit_form_{i}", clear_on_submit=True):
                        new_name = st.text_input("الاسم الجديد", value=product['name'])
                        new_quantity = st.number_input("الكمية الجديدة", value=product['quantity'], min_value=0, step=1)
                        new_price = st.number_input("السعر الجديد", value=product['price'], min_value=0.0, format="%.2f")
                        update_button = st.form_submit_button("حفظ التعديلات")

                        if update_button:
                            # تحديث المنتج في القائمة
                            st.session_state.inventory[i]['name'] = new_name
                            st.session_state.inventory[i]['quantity'] = int(new_quantity)
                            st.session_state.inventory[i]['price'] = float(new_price)
                            save_inventory(st.session_state.inventory)
