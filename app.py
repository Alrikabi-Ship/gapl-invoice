
import streamlit as st
from fpdf import FPDF
import qrcode
from io import BytesIO
from PIL import Image

# Title
st.title("GAPL Invoice Generator")

# Form inputs
dealer = st.text_input("Dealer Name")
car_type = st.text_input("Car Type")
amount_paid = st.text_input("Amount Paid (USD)")

# Generate WhatsApp message
msg = f"GAPL Invoice:\nDealer: {dealer}\nCar Type: {car_type}\nAmount Paid: ${amount_paid}"
wa_link = f"https://wa.me/?text={msg.replace(' ', '%20')}"

# Generate invoice button
if st.button("Generate Invoice"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    # Add logo if exists
    logo_path = "logo.png"
    try:
        pdf.image(logo_path, x=10, y=8, w=33)
    except:
        pass

    pdf.set_xy(10, 50)
    pdf.cell(200, 10, txt="GAPL - Global Auto Parts Logistics", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Dealer: {dealer}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Car Type: {car_type}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Amount Paid: ${amount_paid}", ln=True, align="L")

    # Generate QR code for WhatsApp
    qr = qrcode.make(wa_link)
    qr_bytes = BytesIO()
    qr.save(qr_bytes, format="PNG")
    qr_bytes.seek(0)
    pdf.image(qr_bytes, x=160, y=50, w=40)

    # Save PDF
    pdf.output("invoice.pdf")

    with open("invoice.pdf", "rb") as f:
        st.download_button("Download Invoice", f, file_name="invoice.pdf")

    # Show WhatsApp link
    st.markdown(f"[Share via WhatsApp]({wa_link})")
