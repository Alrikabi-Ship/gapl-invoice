import streamlit as st
from fpdf import FPDF
import qrcode
from io import BytesIO
from PIL import Image
from pathlib import Path

st.set_page_config(page_title="فاتورة GAPL", page_icon="🧾")
st.title("نموذج توليد فاتورة PDF - GAPL")
st.markdown("أدخل معلومات السيارة لإنشاء الفاتورة الرسمية.")

# إدخال البيانات
supplier = st.text_input("اسم المورد")
dealer = st.text_input("اسم التاجر")
car_type = st.text_input("نوع السيارة")
car_model = st.text_input("موديل السيارة")
purchase_date = st.date_input("تاريخ الشراء")
payment_date = st.date_input("تاريخ الدفع")
amount_paid = st.text_input("المبلغ المدفوع")
total_amount = st.text_input("إجمالي الصفقة")
balance = st.text_input("الرصيد المتبقي")
status = st.selectbox("حالة الصفقة", ["قيد التنفيذ", "مكتملة", "ملغاة"])
notes = st.text_area("ملاحظات")

# توليد الفاتورة
if st.button("توليد الفاتورة"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    logo_path = "logo.png"
    if Path(logo_path).exists():
        pdf.image(logo_path, x=10, y=8, w=33)
        pdf.ln(25)

    def row(label, value):
        pdf.cell(60, 10, label, border=1)
        pdf.cell(0, 10, value, border=1, ln=True)

    row("اسم المورد", supplier)
    row("اسم التاجر", dealer)
    row("نوع السيارة", car_type)
    row("موديل السيارة", car_model)
    row("تاريخ الشراء", str(purchase_date))
    row("تاريخ الدفع", str(payment_date))
    row("المبلغ المدفوع", amount_paid)
    row("إجمالي الصفقة", total_amount)
    row("الرصيد المتبقي", balance)
    row("حالة الصفقة", status)
    row("ملاحظات", notes)

    msg = f"فاتورة GAPL:\nالتاجر: {dealer}\nنوع السيارة: {car_type}\nالمبلغ: {amount_paid}"
    wa_link = f"https://wa.me/?text={msg.replace(' ', '%20')}"
    st.markdown(f"[مشاركة على واتساب]({wa_link})")

    qr = qrcode.make(wa_link)
    qr_bytes = BytesIO()
    qr.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)

    qr_path = "qr_temp.png"
    with open(qr_path, "wb") as f:
        f.write(qr_bytes.read())
    pdf.image(qr_path, x=80, w=50)

    pdf.output("invoice.pdf")
    with open("invoice.pdf", "rb") as f:
        st.download_button("تحميل الفاتورة PDF", data=f, file_name="invoice.pdf")
