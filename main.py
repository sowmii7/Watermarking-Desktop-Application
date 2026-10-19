
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

CANVAS_W= 700
CANVAS_H= 400
drag = {"x": 0,
        "y":0,}
display_scale = 1.0
base_id = 0
base_image = None
logo_image = None

def add_file():
    global base_image, display_scale, base_id
    file_path = filedialog.askopenfilename(title="Select an image",
                              filetypes= [("Images files", "*.png *.jpg *.jpeg *.gif *.bmp")])

    if not file_path:
        return
    base_image = Image.open(file_path)
    preview = base_image.copy()
    preview.thumbnail((CANVAS_W,CANVAS_H))
    display_scale = preview.width / base_image.width

    canvas.photo = ImageTk.PhotoImage(preview)

    canvas.delete("all")
    button_3.grid_remove()

    canvas.create_image(CANVAS_W//2, CANVAS_H//2, image=canvas.photo)

    button_4 = Button(text="Add logo", highlightthickness=0, height=3, width=20, command=add_logo)
    button_4.grid(row=4, column=2, columnspan=3)

def download_image():
    if base_image is None:
        messagebox.showwarning("No image", "Please add an image first.")
        return

    result = base_image.copy()

    if logo_image is not None and canvas.find_withtag("logo"):
        bx1, by1, _, _ = canvas.bbox(base_id)
        lx1, ly1, lx2, ly2 = canvas.bbox("logo")

        # convert preview coordinates back to original-image pixels
        x = round((lx1 - bx1) / display_scale)
        y = round((ly1 - by1) / display_scale)
        w = round((lx2 - lx1) / display_scale)
        h = round((ly2 - ly1) / display_scale)

        logo = logo_image.resize((w, h))
        result.paste(logo, (x, y), logo)     # third argument keeps transparency

    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")]
    )
    if not save_path:
        return

    if save_path.lower().endswith((".jpg", ".jpeg")):
        result = result.convert("RGB")       # JPEG has no transparency
    result.save(save_path)
    messagebox.showinfo("Saved", "Image saved successfully.")

def add_logo():
    global logo_image
    if base_image is None:
        messagebox.showwarning("No image", "Please add an image first.")
        return

    logo_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("Images files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if not logo_path:
        return

    logo_image = Image.open(logo_path).convert("RGBA")
    # start the logo at 20% of the preview width, keeping its aspect ratio
    w = max(1, int(base_image.width * display_scale * 0.2))
    h = max(1, logo_image.height * w/logo_image.width)
    preview_logo = logo_image.resize((w, h))


    canvas.logo_photo = ImageTk.PhotoImage(preview_logo)
    canvas.delete("logo")
    canvas.create_image(CANVAS_W//2, CANVAS_H//2, image=canvas.logo_photo, tags="logo")

    button_5 = Button(text="Download Image", highlightthickness=0, height=3, width=20, command = download_image)
    button_5.grid(row=4, column=2, columnspan=3)

def start(event):
    drag["x"], drag["y"] = event.x, event.y

def do_drag(event):
    dx, dy =  event.x - drag["x"], event.y - drag["y"]

    # keep the logo inside the image
    bx1, by1, bx2, by2 = canvas.bbox(base_id)
    lx1, ly1, lx2, ly2 = canvas.bbox("logo")
    dx = max(bx1 - lx1, min(dx, bx2 - lx2))
    dy = max(by1 - ly1, min(dy, by2 - ly2))

    canvas.move("logo", dx, dy)
    drag["x"], drag["y"] = event.x, event.y


def clear():
    canvas = Canvas(width=700, height=400, bg="white")
    canvas.photo = PhotoImage(file="Screenshot 2026-10-18 144236 (1).png")
    canvas.create_image(250, 150, image=canvas.photo)
    canvas.create_text(400, 150, text="Add Watermark", font=("Open Sans", 20, "bold"), fill="black")
    canvas.grid(row=3, column=2, columnspan=3)

    button_3 = Button(text="Select Files", highlightthickness=0, height=3, width=20, command=add_file)
    button_3.grid(row=3, column=2, columnspan=3)

    canvas.create_text(350, 240, text="or drag your files here", font=("Montserrat", 10, "bold"))
    canvas.create_text(350, 350,text="Files stay private, We process files on your device.\n We donot send to our servers and never store them",
                                font=("Montserrat", 10, "bold"))





window = Tk()
window.title("Watermarkly")
window.config(padx=20, pady=20, bg="white")
window.minsize(400, 300)

logo = PhotoImage(file="Screenshot 2026-10-18 144236 (1).png")
label_image = Label(window,image=logo, bg="white")
label_image.grid(row=0, column=0)


top_label = Label(text = "Watermarkly", font =("Montserrat",20,"bold"), bg="white")
top_label.grid(row=0, column=1)


button_1 = Button(text = "Add file",highlightthickness=0,height=2, width=30, command=add_file)
button_1.grid(row=1, column = 2)

button_2 = Button(text = "Clear",highlightthickness=0, height=2, width=30, command=clear)
button_2.grid(row=1, column = 3)

canvas = Canvas(width=700, height=400, bg="white")
logo_center = PhotoImage(file="Screenshot 2026-10-18 144236 (1).png")
image = canvas.create_image(250, 150, image=logo_center)
canva_text = canvas.create_text(400, 150, text="Add Watermark", font=("Open Sans", 20, "bold"), fill="black")
canvas.grid(row=3, column=2, columnspan=3)

button_3 = Button(text="Select Files", highlightthickness=0, height=3, width=20, command=add_file)
button_3.grid(row=3, column=2, columnspan=3)

label_text = canvas.create_text(350, 240, text="or drag your files here", font=("Montserrat", 10, "bold"))
label_text_2 = canvas.create_text(350, 350,
                                  text="Files stay private, We process files on your device.\n We donot send to our servers and never store them",
                                  font=("Montserrat", 10, "bold"))





window.mainloop()
