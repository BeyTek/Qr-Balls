import qrcode
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode

def diviser_qr_code():
    texte_a_encoder = entry_texte.get()
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(texte_a_encoder)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_image = qr_img.convert("RGB") 
    largeur, hauteur = qr_image.size
    
    qr_partie_1 = qr_image.crop((0, 0, largeur, hauteur // 7))
    qr_partie_2 = qr_image.crop((0, hauteur // 7, largeur, 2 * hauteur // 7))
    qr_partie_3 = qr_image.crop((0, 2 * hauteur // 7, largeur, 3 * hauteur // 7))
    qr_partie_4 = qr_image.crop((0, 3 * hauteur // 7, largeur, 4 * hauteur // 7))
    qr_partie_5 = qr_image.crop((0, 4 * hauteur // 7, largeur, 5 * hauteur // 7))
    qr_partie_6 = qr_image.crop((0, 5 * hauteur // 7, largeur, 6 * hauteur // 7))
    qr_partie_7 = qr_image.crop((0, 6 * hauteur // 7, largeur, hauteur))
    
    qr_partie_1.save("qr_part_1.png")
    qr_partie_2.save("qr_part_2.png")
    qr_partie_3.save("qr_part_3.png")
    qr_partie_4.save("qr_part_4.png")
    qr_partie_5.save("qr_part_5.png")
    qr_partie_6.save("qr_part_6.png")
    qr_partie_7.save("qr_part_7.png")
    
    label_status.config(text="Succesfull 7 QR balls created")

def rassembler_qr_code():
    qr_parties = [Image.open(f"qr_part_{i}.png") for i in range(1, 8)]
    
    partie_largeur, partie_hauteur = qr_parties[0].size
    largeur_totale = partie_largeur
    hauteur_totale = partie_hauteur * 7
    
    qr_combine = Image.new("RGB", (largeur_totale, hauteur_totale))
    
    for i, qr_partie in enumerate(qr_parties):
        qr_combine.paste(qr_partie, (0, i * partie_hauteur))
    
    qr_combine.save("qr_code_comp.png")
    label_status.config(text="Succes!")
    
    texte_dechiffre = dechiffrer_qr_code(qr_combine)  
    label_dechiffre.config(text=texte_dechiffre)  

def dechiffrer_qr_code(qr_image):
    decoded_objects = decode(qr_image)
    
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return "Unable to decipher the QR Code"


root = tk.Tk()
root.title("QR BALLS")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_texte = tk.Label(frame, text="Enter text or link:")
label_texte.grid(row=0, column=0)
label_dechiffre = tk.Label(frame, text="")
label_dechiffre.grid(row=3, columnspan=3)
entry_texte = tk.Entry(frame, width=40)
entry_texte.grid(row=0, column=1)

btn_diviser = tk.Button(frame, text="Create QR balls", command=diviser_qr_code)
btn_diviser.grid(row=1, column=1)

btn_rassembler = tk.Button(frame, text="Collect QR balls", command=rassembler_qr_code)
btn_rassembler.grid(row=1, column=2)

label_status = tk.Label(frame, text="")
label_status.grid(row=2, columnspan=3)

root.mainloop()
