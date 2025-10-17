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
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_inventory(inventory):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=4, ensure_ascii=False)

# --- تحميل البيانات ---
inventory = load_inventory()

# --- واجهة التطبيق ---
st.set_page_config(layout="wide", page_title="نظام المخزون - هنان")

st.title("نظام إدارة المخزون الاحترافي")
st.write("---")

# --- قائمة جانبية للإجراءات ---
menu = ["عرض المنتجات", "إضافة منتج", "بحث وحذف"]
choice = st.sidebar.selectbox("القائمة", menu)

if choice == "عرض المنتجات":
    st.subheader("جميع المنتجات في المخزون")
    if not inventory:
        st.warning("المخزون فارغ حالياً.")
    else:
        st.table(inventory)

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
                new_product = {'name': name, 'quantity': quantity, 'price': price}
                inventory.append(new_product)
                save_inventory(inventory)
                st.success(f"تمت إضافة المنتج '{name}' بنجاح!")

elif choice == "بحث وحذف":
    st.subheader("البحث عن منتج أو حذفه")
    search_term = st.text_input("اكتب اسم المنتج للبحث")

    if not inventory:
        st.warning("المخزون فارغ، لا يوجد شيء للبحث فيه.")
    else:
        results = [p for p in inventory if search_term.lower() in p['name'].lower()]
            
        if search_term and not results:
            st.info(f"لم يتم العثور على منتج باسم '{search_term}'.")

        for product in results:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"المنتج: {product['name']} | الكمية: {product['quantity']} | السعر: {product['price']}")
            with col2:
                if st.button(f"❌ حذف", key=f"delete_{product['name']}"):
                    inventory.remove(product)
                    save_inventory(inventory)
                    st.rerun()
