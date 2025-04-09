
import streamlit as st
import qrcode
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="فاتورة GAPL", layout="centered")
st.title("نموذج توليد فاتورة PDF - GAPL")
st.markdown("املأ البيانات التالية لتوليد فاتورة رسمية بصيغة PDF")

# نموذج الإدخال
supplier = st.text_input("اسم المورد")
dealer = st.text_input("اسم التاجر")
car_type = st.text_input("نوع السيارة")
car_model = st.text_input("موديل السيارة")
purchase_date = st.date_input("تأريخ شراء السيارة")
payment_date = st.date_input("تأريخ الدفع")
amount_paid = st.text_input("المبلغ المدفوع")
total_amount = st.text_input("إجمالي الصفقة")
balance = st.text_input("الرصيد المتبقي")
status = st.selectbox("حالة الصفقة", ["قيد التنفيذ", "مدفوعة جزئياً", "مدفوعة بالكامل"])
notes = st.text_area("ملاحظات")

if st.button("توليد الفاتورة"):
    # توليد QR code
    qr_text = f"فاتورة GAPL | التاجر: {dealer} | المبلغ المدفوع: {amount_paid}"
    qr = qrcode.make(qr_text)
    qr_bytes = BytesIO()
    qr.save(qr_bytes)
    qr_bytes.seek(0)

    # توليد PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
    pdf.set_font('Arial', '', 14)
    pdf.cell(0, 10, "GAPL – الشركة العالمية لوجستيات قطع غيار السيارات", ln=True, align='C')
    pdf.cell(0, 10, "فاتورة صفقة", ln=True, align='C')
    pdf.ln(10)

    def row(label, value):
        pdf.cell(60, 10, label, border=1)
        pdf.cell(0, 10, value, border=1, ln=True)

    row("اسم المورد", supplier)
    row("اسم التاجر", dealer)
    row("نوع السيارة", car_type)
    row("موديل السيارة", car_model)
    row("تأريخ الشراء", str(purchase_date))
    row("تأريخ الدفع", str(payment_date))
    row("المبلغ المدفوع", amount_paid)
    row("إجمالي الصفقة", total_amount)
    row("الرصيد المتبقي", balance)
    row("حالة الصفقة", status)
    row("ملاحظات", notes)

    # QR code
    pdf.image(qr_bytes, x=80, w=50)
    pdf.ln(10)
    pdf.cell(0, 10, "التوقيع الرقمي: مدير قسم الاستيراد", ln=True, align='R')

    # إخراج PDF
    output = BytesIO()
    pdf.output(output)
    st.success("تم توليد الفاتورة!")
    st.download_button("تحميل الفاتورة PDF", data=output.getvalue(), file_name="GAPL_Invoice.pdf")
