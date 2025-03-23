# # utils.py

# from io import BytesIO
# import qrcode

# def generate_qr(data):
#     """Generate QR code from data"""
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(data)
#     qr.make(fit=True)
    
#     img = qr.make_image(fill_color="black", back_color="white")
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)
    
#     return buffer

# def sats_to_ngn(sats, rate=0.01):
#     """Convert sats to NGN using the provided rate"""
#     return sats * rate

# def ngn_to_sats(ngn, rate=0.01):
#     """Convert NGN to sats using the provided rate"""
#     return int(ngn / rate)