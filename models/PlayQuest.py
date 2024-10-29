import customtkinter as ctk
import tkinter.messagebox as tkmb
import mysql.connector
import hashlib
from PIL import ImageTk, Image
import tkinter
import webbrowser
import os
import random
import json
from time import strftime
import pickle
import winreg as reg
import platform
from tkinter import StringVar
# from database_connection import db

# cursor = db.cursor()
notes = []
text_entry = None
notes_listbox = None
note_num_entry = None
notes_file = "zmienne/notes.json"
texk_bout_me = None
logged_in_user=None
user_id = None
STATUS_FILE = "zmienne/checkbox_status.pkl"
FORMAT_FILE = "zmienne/time_format.pkl"
COLOR_FILE = "zmienne/clock_color.pkl"
AUTOSTART_FILE = "zmienne/autostart_status.pkl"
CONFIG_FILE = "zmienne/config.txt"  # Plik do przechowywania ustawień zasilania

ctk.set_appearance_mode("System") # Ustawienie trybu wyglądu na systemowy
ctk.set_default_color_theme("dark-blue") # Ustawienie domyślnego motywu kolorystycznego na niebieski

db = mysql.connector.connect(
    host="109.207.145.26",
    port='32770',
    user="proj_inz_user",
    password="proj_inz_user",
    database="proj_inz"
)

# Utworzenie kursora
cursor = db.cursor()

# Utworzenie okna logowania aplikacji
app = ctk.CTk()
app.geometry("660x440")
app.title("Login")

login_frame = ctk.CTkFrame(app)
register_frame = ctk.CTkFrame(app)

credentials_file = 'credentials.json'  # Plik do zapisywania danych logowania

# Funkcja do odczytywania zapisanych danych logowania
def load_credentials():
    if os.path.exists(credentials_file):
        with open(credentials_file, 'r') as file:
            return json.load(file)
    return None

# Funkcja do zapisywania danych logowania
def save_credentials(email, password):
    with open(credentials_file, 'w') as file:
        json.dump({'email': email, 'password': password}, file)

# Funkcja do usuwania zapisanych danych logowania
def remove_credentials():
    if os.path.exists(credentials_file):
        os.remove(credentials_file)

def get_random_avatar():
    avatars_folder = 'avatars/'  # Folder z awatarami
    avatars = os.listdir(avatars_folder)  # Lista plików w folderze
    random_avatar = random.choice(avatars)  # Wybór losowego awatara
    return os.path.join(avatars_folder, random_avatar)

def handle_label_click():
    print("Etykieta została kliknięta!")

# zmaina ramki programu pomiedzy register a login
def login_frame_switch():
    register_frame.place_forget()
    login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

def register_frame_switch():
    login_frame.place_forget()
    register_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Funkcja logowania
def login():
    global logged_in_user
    mail = user_entry.get()
    password = user_pass.get()

    # sprawdzanie czy są podane informacje
    if not mail or not password:
        tkmb.showerror(title='Błąd', message='Wprowadź E-mail i hasło')
        return
    
    # Haszowanie hasła
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Sprawdzenie, czy podane dane logowania są poprawne
    cursor.execute("SELECT * FROM users WHERE mail = %s AND password = %s", (mail, hashed_password))
    result = cursor.fetchone()

    if result:
        logged_in_user = mail
        if remember_var.get():
            save_credentials(mail, password)
        else:
            remove_credentials()
        app.destroy()  # Ukrycie głównego okna
        show_main_menu()  # Wyświetlenie menu głównego
    else:
        tkmb.showerror(title='Logowanie nieudane', message='Nieprawidłowa kombinacja E-mail lub hasła')

def load_login_data():
    credentials = load_credentials()
    if credentials:
        user_entry.insert(0, credentials['email'])
        user_pass.insert(0, credentials['password'])  # Wstawiamy hasło w formie jawnej
        remember_var.set(True)  # Ustawienie opcji "Zapamiętaj mnie" na True

# Funkcja rejestrowania
def register():
    new_username = new_user_entry.get()
    new_password = new_user_pass.get()
    new_mail = new_user_mail.get()

    avatar_path = get_random_avatar()

    # sprawdzanie czy są podane informacje
    if not new_username or not new_password or not new_mail:
        tkmb.showerror(title='Błąd', message='Wprowadź wszystkie wymagane informaje')
        return
    
    # Haszowanie hasła
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

    # Dodanie nowego użytkownika do bazy danych
    cursor.execute("INSERT INTO users (username, password, mail, avatar_path) VALUES (%s, %s, %s,%s)", (new_username, hashed_password, new_mail, avatar_path))
    db.commit()

    tkmb.showinfo(title="Rejestracja udana", message="Użytkownik zarejestrowany pomyślnie!")

# Funkcja logowania za pomocą konta Google
# def login_with_google():
#     # Otwórz stronę logowania Google w przeglądarce
#         google_auth_url = "https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=email"
#         webbrowser.open(google_auth_url)

# def login_with_facebook():
#         # Implementacja Facebook OAuth2 (dla celów demonstracyjnych)
#     facebook_auth_url = "https://www.facebook.com/dialog/oauth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=email"
#     webbrowser.open(facebook_auth_url)

img1=ImageTk.PhotoImage(Image.open("./images/background_login.jpg"))
l1=ctk.CTkLabel(master=app,image=img1)
l1.pack()

# ######################################## REGISTER FRAME ######################################## #

#create register frame
register_frame=ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
register_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

f3=ctk.CTkLabel(master=register_frame, text="Register your account",font=('Century Gothic',20))
f3.place(x=50, y=45)

new_user_entry=ctk.CTkEntry(master=register_frame, width=220, placeholder_text='Username')
new_user_entry.place(x=50, y=110)

new_user_pass=ctk.CTkEntry(master=register_frame, width=220, placeholder_text='Password', show="*")
new_user_pass.place(x=50, y=165)

new_user_mail=ctk.CTkEntry(master=register_frame, width=220, placeholder_text='Email')
new_user_mail.place(x=50, y=215)


#create register buttons
register_button = ctk.CTkButton(master=register_frame, width=220, text="Register", command=register, corner_radius=6)
register_button.place(x=50, y=280)

switch_to_login = ctk.CTkButton(master=register_frame, width= 220, text="Switch to login", corner_radius=6, command=login_frame_switch, fg_color = 'transparent')
switch_to_login.place(x=50, y= 320)

# ######################################## LOGIN FRAME ######################################## #

#creating login frame
login_frame=ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
login_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

f2=ctk.CTkLabel(master=login_frame, text="Log into your Account",font=('Century Gothic',20))
f2.place(x=50, y=45)

user_entry=ctk.CTkEntry(master=login_frame, width=220, placeholder_text='E-mail')
user_entry.place(x=50, y=110)

user_pass=ctk.CTkEntry(master=login_frame, width=220, placeholder_text='Password', show="*")
user_pass.place(x=50, y=165)

# l3=ctk.CTkLabel(master=login_frame, text="Forget password?",font=('Century Gothic',12))
# l3.place(x=155,y=195)

#Create login buttons
login_button = ctk.CTkButton(master=login_frame, width=220, text="Login", command=login, corner_radius=6)
login_button.place(x=50, y=240)

remember_var = ctk.BooleanVar()
remember_checkbox = ctk.CTkCheckBox(master=login_frame, text="Zapamiętaj mnie", variable=remember_var)
remember_checkbox.place(x=95, y=210)


# img2=ctk.CTkImage(Image.open("./images/Google__G__Logo.svg.webp").resize((20,20), Image.Resampling.LANCZOS))
# img3=ctk.CTkImage(Image.open("./images/124010.png").resize((20,20), Image.Resampling.LANCZOS))
# google_login_button= ctk.CTkButton(master=login_frame, image=img2, text="Google", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF', command=login_with_google)
# google_login_button.place(x=50, y=290)

# facebook_login_button= ctk.CTkButton(master=login_frame, image=img3, text="Facebook", width=100, height=20, compound="left", fg_color='white', text_color='black', hover_color='#AFAFAF', command=login_with_facebook)
# facebook_login_button.place(x=170, y=290)

switch_to_register = ctk.CTkButton(master=login_frame, width= 220, text="Don't have account ?", corner_radius=6, command=register_frame_switch, fg_color = 'transparent')
switch_to_register.place(x=50, y= 320)

load_login_data()

def show_main_menu():
    import customtkinter as ctk
    import tkinter.messagebox as tkmb
    import mysql.connector
    import hashlib
    from PIL import ImageTk, Image
    import tkinter
    import webbrowser
    import os
    from tkinter import filedialog
    import subprocess
    import os
    import sys

    # cursor.execute("SELECT username FROM users WHERE mail = %s ", (logged_in_user,))
    # username = cursor.fetchone()

    #Fonts
    font1= ('Helvetica',25,'bold')
    font2= ('Arial',16,'bold')
    font3= ('Arial',9,'bold')
    font4= ('Arial',9,'bold','underline')
    font5= ('Helvetica',18,'bold')
    font6= ('Helvetica',10,'bold')
    font7= ('Helvetica',14,'bold')
    font8= ('Helvetica',12,'bold')
    font9= ('Helvetica',32,'bold')
    font10= ('Helvetica',48,'bold')

    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("System") # Ustawienie trybu wyglądu na systemowy
    ctk.set_default_color_theme("dark-blue") # Ustawienie domyślnego motywu kolorystycznego na niebieski

    main = ctk.CTk()
    main.geometry("1280x720")
    # main.resizable(False,False)
    main.title("PlayQuest.")


    image_1=ImageTk.PhotoImage(Image.open("./icons/quest.png"),size=(40,40))
    image_2=ImageTk.PhotoImage(Image.open("./icons/shopping-cart.png"),size=(30,30))
    image_3=ImageTk.PhotoImage(Image.open("./icons/game.png"),size=(30,30))
    image_4=ImageTk.PhotoImage(Image.open("./icons/community.png"),size=(30,30))
    image_5=ImageTk.PhotoImage(Image.open("./icons/checklist.png"),size=(30,30))
    image_6=ImageTk.PhotoImage(Image.open("./icons/user.png"),size=(30,30))
    image_7=ImageTk.PhotoImage(Image.open("./icons/setting.png"),size=(30,30))
    image_8=ImageTk.PhotoImage(Image.open("./icons/user_up.png"),size=(20,20))
    image_9=ImageTk.PhotoImage(Image.open("./icons/news_up.png"),size=(20,20))
    image_10=ImageTk.PhotoImage(Image.open("./icons/settings_up.png"),size=(20,20))
    image_11=ImageTk.PhotoImage(Image.open("./icons/update.png"),size=(20,20))
    image_12=ImageTk.PhotoImage(Image.open("./icons/diskette.png"),size=(20,20))
    image_13=ImageTk.PhotoImage(Image.open("./icons/bin.png"),size=(40,40))
    image_14=ImageTk.PhotoImage(Image.open("./avatars/avatar1.png"),size=(200,200))

    def add_note():
        note = text_entry.get("1.0", "end-1c").strip()
        if note:
            notes.append(note)
            update_notes_listbox()
            text_entry.delete("1.0", "end")
            save_notes()

    def delete_note():
        try:
            note_number = int(note_num_entry.get())
            if 1 <= note_number <= len(notes):
                notes.pop(note_number - 1)
                update_notes_listbox()
                note_num_entry.delete(0, 'end')
                save_notes()
            else:
                tkmb.showerror(title="Info", message="Invalid note number.")
        except ValueError:
            tkmb.showerror(title="Info", message="Please enter a valid number.")

    def update_notes_listbox():
        notes_listbox.delete("1.0", "end")
        for index, note in enumerate(notes, start=1):
            numbered_note = f"{index}. {note}\n\n"
            notes_listbox.insert("end", numbered_note)

    def save_notes():
        with open(notes_file, 'w') as file:
            json.dump(notes, file)

    def load_notes():
        if os.path.exists(notes_file):
            with open(notes_file, 'r') as file:
                return json.load(file)
        return []

    def select_image():
        # Otwórz okno dialogowe wyboru pliku
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        
        if file_path:
            # Wczytaj i przeskaluj obraz do 200x200 pikseli
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)

            
            # Zapisz obraz jako 'avatar1' w folderze 'avatars'
            save_path = os.path.join("avatars", "avatar1.png")
            image.save(save_path, format="PNG")


    def load_power_mode():
        """Wczytaj zapisany tryb zasilania z pliku konfiguracyjnego."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return file.read().strip()
        return power_modes[0]  # Zwróć domyślny tryb, jeśli plik nie istnieje

    def save_power_mode(mode):
        """Zapisz wybrany tryb zasilania do pliku konfiguracyjnego."""
        with open(CONFIG_FILE, "w") as file:
            file.write(mode)

    def set_power_mode():
        selected_mode = power_mode_var.get()

        if platform.system() == "Windows":
            if selected_mode == "Wysoka wydajność":
                os.system("powercfg /setactive SCHEME_MIN")  # Wysoka wydajność
            elif selected_mode == "Zrównoważony":
                os.system("powercfg /setactive SCHEME_BALANCED")  # Zrównoważony
            elif selected_mode == "Oszczędzanie energii":
                os.system("powercfg /setactive SCHEME_MAX")  # Oszczędzanie energii

            # Zapisz wybór do pliku konfiguracyjnego
            save_power_mode(selected_mode)
            tkmb.showinfo("Info", f"Ustawiono tryb zasilania: {selected_mode}")
        else:
            tkmb.showerror("Błąd", "Zmiana trybu zasilania obsługiwana tylko na Windows.")

    power_modes = ["Wysoka wydajność", "Zrównoważony", "Oszczędzanie energii"]

    # Wczytaj ostatnio wybrany tryb zasilania lub ustaw domyślny
    initial_mode = load_power_mode()
    power_mode_var = StringVar(value=initial_mode)

# Konfiguracja głównego okna aplikacji

    def wczytaj_status_checkbox_autostart():
         # Wczytuje stan checkboxa z pliku przy użyciu pickle, jeśli plik istnieje
        if os.path.exists(AUTOSTART_FILE):
            with open(AUTOSTART_FILE, "rb") as f:
                return pickle.load(f)
        return False  # Domyślnie zwraca False, jeśli plik nie istnieje
    
    def dodaj_do_autostartu():
        sciezka_do_aplikacji = os.path.abspath(sys.argv[0])
        nazwa_aplikacji = "PlayQuest"
        try:
            klucz = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(klucz, nazwa_aplikacji, 0, reg.REG_SZ, sciezka_do_aplikacji)
            reg.CloseKey(klucz)
            tkmb.showinfo(title='Powodzenie', message='Aplikacja dodana do autostartu')
        except Exception as e:
            tkmb.showerror(title='Błąd', message='Nie udało się dodać aplikacji do autostartu')

    def usun_z_autostartu():
        nazwa_aplikacji = "PlayQuest"
        try:
            klucz = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE)
            reg.DeleteValue(klucz, nazwa_aplikacji)
            reg.CloseKey(klucz)
            tkmb.showinfo(title='Powodzenie', message='Aplikacja usunieta z autostartu')
        except Exception as e:
            tkmb.showerror(title='Błąd', message='Nie udało się usunąć aplikacji z autostartu')

    # Funkcja do zapisywania formatu czasu
    def zapisz_format_czasu():
        with open(FORMAT_FILE, "wb") as f:
            pickle.dump(format_var.get(), f)

    # Funkcja do wczytywania formatu czasu
    def wczytaj_format_czasu():
        if os.path.exists(FORMAT_FILE):
            with open(FORMAT_FILE, "rb") as f:
                format_var.set(pickle.load(f))
        else:
            format_var.set("24")  # Domyślnie ustaw na 24-godzinny

    def wczytaj_status_checkboxa():
        # Wczytuje stan checkboxa z pliku przy użyciu pickle, jeśli plik istnieje
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "rb") as f:
                return pickle.load(f)
        return False  # Domyślnie zwraca False, jeśli plik nie istnieje

    def aktualizuj_czas():
        if format_var.get() == "12":
            teraz = strftime('%I:%M:%S %p')  # 12-godzinny format
        else:
            teraz = strftime('%H:%M:%S')  # 24-godzinny format

        data = strftime('%d-%m-%Y')  # Pobiera aktualną datę
        etykieta_czas.configure(text=teraz,text_color=color_var.get())  # Ustawia tekst czasu
        etykieta_data.configure(text=data,text_color=color_var.get())  # Ustawia tekst daty
        etykieta_czas.after(1000, aktualizuj_czas)

    # Funkcja do zapisywania koloru zegara
    def zapisz_kolor_zegara():
        with open(COLOR_FILE, "wb") as f:
            pickle.dump(color_var.get(), f)

    # Funkcja do wczytywania koloru zegara
    def wczytaj_kolor_zegara():
        if os.path.exists(COLOR_FILE):
            with open(COLOR_FILE, "rb") as f:
                color_var.set(pickle.load(f))
        else:
            color_var.set("#FFFFFF")  # Domyślnie ustaw na biały

    def hide_pages():
        for frame in frame_middle.winfo_children():
            frame.destroy()

    def hide_indicate():
        button2_indicate.configure(bg_color='#3F4462')
        button3_indicate.configure(bg_color='#3F4462')
        button4_indicate.configure(bg_color='#3F4462')
        button5_indicate.configure(bg_color='#3F4462')
        button6_indicate.configure(bg_color='#3F4462')
        button7_indicate.configure(bg_color='#3F4462')

    def indicate(lb,page):
        hide_pages()
        hide_indicate()
        lb.configure(bg_color="white")
        page()

    def logout():
        main.destroy()  # Zamyka aplikację

    # Funkcja do ponownego uruchomienia aplikacji
    def restart_app():
        python = sys.executable
        os.execl(python, python, *sys.argv)  # Uruchamia aplikację ponownie

    # Funkcja do wyjścia z aplikacji
    def exit_app():
        main.destroy()  # Zamyka aplikację

    # Funkcja do rozwijania lub zwijania menu
    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.pack_forget()  # Zwiń menu
        else:
            menu_frame.pack(side="right")  # Rozwiń menu
            l2.focus_force()  # Ustawia fokus na oknie

        ###################################### Left side ######################################

    l1 = ctk.CTkFrame(master=main, width=216, fg_color="#3F4462",border_width=0.6 , border_color="black",corner_radius=0,)
    l1.pack(side="left", fill="both",expand = False)

    button1 = ctk.CTkButton(master=l1,image=image_1, width=142,height=30, text="PlayQuest", text_color="#FFFFFF", font=font1, fg_color="#3F4462",hover=False , anchor="w")
    button1.place(x=10,y=32)

    button2 = ctk.CTkButton(master=l1,image=image_2 , width=108,height=24, text="Shop", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button2_indicate,def_page_shop_card))
    button2.place(x=33,y=133)
    button2_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button2_indicate.place(x=3,y=133)

    button3 = ctk.CTkButton(master=l1,image=image_3 , width=108,height=24, text="Library", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button3_indicate,page_library_def))
    button3.place(x=33,y=182)
    button3_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button3_indicate.place(x=3,y=182)

    button4 = ctk.CTkButton(master=l1,image=image_4 , width=108,height=24, text="Community", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button4_indicate,page_community_def))
    button4.place(x=33,y=231)
    button4_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button4_indicate.place(x=3,y=231)

    button5 = ctk.CTkButton(master=l1,image=image_5 , width=108,height=24, text="Wish List", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button5_indicate,page_wish_list_def))
    button5.place(x=33,y=280)
    button5_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button5_indicate.place(x=3,y=280)

    button6 = ctk.CTkButton(master=l1,image=image_6 , width=108,height=24, text="Account", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button6_indicate,page_account_def))
    button6.place(x=33,y=329)
    button6_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button6_indicate.place(x=3,y=329)

    button7 = ctk.CTkButton(master=l1,image=image_7 , width=108,height=24, text="Settings", text_color="#FFFFFF", font=font2, fg_color="#3F4462",hover_color="#384069",anchor='w',command=lambda: indicate(button7_indicate,page_setting_def))
    button7.place(x=33,y=378)
    button7_indicate = ctk.CTkLabel(master=l1,text="",bg_color="#3F4462",width=5,height=35)
    button7_indicate.place(x=3,y=378)

    # etykieta_czas = ctk.CTkLabel(master=l1, font=('Helvetica', 32), text_color="#FFFFFF",fg_color='#3F4462',anchor="center",width=216)
    # etykieta_czas.pack(side="bottom",pady=5,padx=5)

    etykieta_czas = ctk.CTkLabel(master=l1, font=('Helvetica', 22), text_color="#FFFFFF", fg_color='#3F4462', anchor="center", width=214)
    etykieta_data = ctk.CTkLabel(master=l1, font=('Helvetica', 12), text_color="#FFFFFF", fg_color='#3F4462', anchor="center", width=214,height=8)

        ###################################### Top side ######################################

    l2 = ctk.CTkFrame(master=main, height=85, fg_color="#3F4462", border_width=0.6 , border_color="black",corner_radius=0)
    l2.pack(side="top", fill="both",expand = False)

    label_name1 = ctk.CTkLabel(master=l2,width=112,height=30, text="Overview", text_color="#FFFFFF", font=font1, fg_color="#3F4462",anchor="center")
    # label_name1.place(x=249,y=32)
    label_name1.pack(side = "left", pady =5, padx= 40)

    button8 = ctk.CTkButton(master=l2,image=image_8,width=40,height=40,text="",corner_radius=100, fg_color="#3F4462", hover_color="#384069",anchor="center",command=lambda: indicate(button6_indicate,page_account_def))
    button8.pack(side = "right", pady =16, padx= 5)

    button9 = ctk.CTkButton(master=l2,image=image_9,width=40,height=40,text="",corner_radius=100, fg_color="#3F4462", hover_color="#384069",anchor="center")
    button9.pack(side = "right", pady =16, padx= 5)

    button10 = ctk.CTkButton(master=l2,image=image_10,width=40,height=40,text="",corner_radius=100, fg_color="#3F4462", hover_color="#384069",anchor="center",command=toggle_menu)
    button10.pack(side = "right", pady =16, padx= 5)

    menu_frame = ctk.CTkFrame(master=l2,height=15,fg_color="#3F4462")
    menu_frame.pack(side="right")

    button11 = ctk.CTkButton(master=menu_frame,width=40,height=40,text="Exit",corner_radius=10, fg_color="#2F4462", hover_color="#384069",anchor="center",command=exit_app)
    button11.pack(side = "right", pady =5, padx= 2)
    button12 = ctk.CTkButton(master=menu_frame,width=40,height=40,text="Restart",corner_radius=10, fg_color="#2F4462", hover_color="#384069",anchor="center",command=restart_app)
    button12.pack(side = "right", pady =5, padx= 2)
    button13 = ctk.CTkButton(master=menu_frame,width=40,height=40,text="Logout",corner_radius=10, fg_color="#2F4462", hover_color="#384069",anchor="center",command=logout)
    button13.pack(side = "right", pady =5, padx= 2)

    # entry_search =ctk.CTkEntry(master=l2, width=190, height=18, placeholder_text="Search for something       ⚲", text_color="#FFFFFF", font=font3, fg_color="#51577D",border_color="black",border_width=1.2)
    # # entry_search.place(x=640,y=33)
    # entry_search.pack(side = "right", pady =16, padx= 5)


        ###################################### Middle side ######################################

    frame_middle = ctk.CTkFrame(master=main, fg_color="#555B83",border_width=0.6 , border_color="black",corner_radius=0)
    frame_middle.pack(expand = True,fill="both")
    frame_middle.pack_propagate(0)

    ### SHOP CARD ###
    def def_page_shop_card():
        page_shop = ctk.CTkFrame(master=frame_middle, fg_color="#555B83",border_width=0.6 , border_color="black",corner_radius=0)
        page_shop.pack(anchor=tkinter.W,expand = True, fill="both")
        
        shop_page_load=ctk.CTkLabel(master=page_shop, width=875,  height=432, fg_color="#FFFFFF",corner_radius=15,text="Comming Soon Shop",anchor="center",font=("Arial",58),text_color="black")
        shop_page_load.pack(padx=15, pady=15)

    ## LIBRARY CARD ###
    def page_library_def():
        page_library = ctk.CTkFrame(master=frame_middle, fg_color="#555B83", border_width=0.6, border_color="black", corner_radius=0)
        page_library.pack(anchor=tkinter.W, expand=True, fill="both")

        selected_paths = []

        def create_widgets(page_library):
            # Clear previous widgets, if any
            for widget in page_library.winfo_children():
                widget.destroy()

            # Frame for saved paths buttons
            button_frame = ctk.CTkScrollableFrame(page_library)
            button_frame.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)

            # Buttons for saved paths
            create_path_buttons(button_frame)

            # Frame for file selection and buttons
            frame = ctk.CTkFrame(page_library,fg_color= '#555B83')
            frame.pack(padx=10, pady=(0, 10), fill=ctk.BOTH)

            # File selection entry
            entry_path = ctk.CTkEntry(frame, width=40, bg_color= '#555B83')
            entry_path.pack(side=ctk.LEFT, padx=(0, 5), fill=ctk.X, expand=True)

            # "Browse" button
            button_browse = ctk.CTkButton(frame,bg_color= '#555B83', text="Browse", command=lambda: browse_file(entry_path))
            button_browse.pack(side=ctk.LEFT,padx = 10)

            # "Add" button
            button_add = ctk.CTkButton(frame,bg_color= '#555B83',text="Add", command=lambda: add_path(entry_path, page_library))
            button_add.pack(side=ctk.LEFT)

        def create_path_buttons(button_frame):
            for path in selected_paths:
                filename = os.path.splitext(os.path.basename(path))[0]
                button_frame_child = ctk.CTkFrame(button_frame)
                button_frame_child.pack(side=ctk.TOP, fill=ctk.X)
                button = ctk.CTkButton(button_frame_child, text=filename, command=lambda p=path: start_process(p), fg_color="transparent")
                button.pack(side=ctk.LEFT, fill=ctk.X, expand=True, pady=5)
                remove_button = ctk.CTkButton(button_frame_child, text="Remove", command=lambda p=path: remove_path(p), width=10)
                remove_button.pack(side=ctk.LEFT, padx=(0, 5), pady=5)
                rename_button = ctk.CTkButton(button_frame_child, text="Rename", command=lambda p=path: rename_path(p), width=10)
                rename_button.pack(side=ctk.LEFT, pady=5)

        def browse_file(entry_path):
            filepath = filedialog.askopenfilename()
            entry_path.delete(0, tkinter.END)
            entry_path.insert(0, filepath)

        def start_process(filepath):
            if filepath:
                try:
                    subprocess.Popen(filepath, shell=True)
                except Exception as e:
                    tkmb.showerror("Error", f"Error: {e}")

        def add_path(entry_path, page_library):
            filepath = entry_path.get()
            if filepath and filepath not in selected_paths:
                selected_paths.append(filepath)
                save_paths()  # Zapisz listę ścieżek do pliku
                entry_path.delete(0, tkinter.END)
                create_widgets(page_library)  # Odśwież widżety
            elif filepath in selected_paths:
                tkmb.showinfo("Info", "This path is already added.")
            else:
                tkmb.showerror("Error", "Select a file first")

        def remove_path(filepath):
            if filepath in selected_paths:
                selected_paths.remove(filepath)
                save_paths()  # Zapisz listę ścieżek do pliku
                create_widgets(page_library)  # Odśwież widżety

        def rename_path(filepath):
            new_name = tkinter.simpledialog.askstring("Rename", "Enter new name for the program:")
            if new_name:
                new_path = os.path.join(os.path.dirname(filepath), new_name + os.path.splitext(filepath)[1])
                try:
                    os.rename(filepath, new_path)
                    # Update selected_paths list with new path
                    index = selected_paths.index(filepath)
                    selected_paths[index] = new_path
                    save_paths()  # Zapisz listę ścieżek do pliku
                    create_widgets(page_library)  # Odśwież widżety
                except Exception as e:
                    tkmb.showerror("Error", f"Error renaming file: {e}")

        def save_paths():
            with open("zmienne/selected_paths.txt", "w") as file:
                for path in selected_paths:
                    file.write(path + "\n")

        def load_paths():
            try:
                with open("zmienne/selected_paths.txt", "r") as file:
                    return [line.strip() for line in file.readlines()]
            except FileNotFoundError:
                # Jeśli plik nie istnieje, zaczynamy z pustą listą
                return []
            except Exception as e:
                print("Error loading paths:", e)

        selected_paths = load_paths()  # Load paths at startup
        create_widgets(page_library)


    ### COMMUNITY CARD ###
    def page_community_def():
        page_community = ctk.CTkFrame(master=frame_middle,fg_color="#555B83",border_width=0.6 , border_color="black",corner_radius=0)
        page_community.pack(anchor=tkinter.W,expand = True, fill="both")

        community_page_load=ctk.CTkLabel(master=page_community, width=875,  height=432, fg_color="#FFFFFF",corner_radius=15,text="Comming Soon Community",anchor="center",font=("Arial",58),text_color="black")
        community_page_load.pack(padx=15, pady=15)


    ### WISH LIST CARD ###
    def page_wish_list_def():
        page_wish_list = ctk.CTkFrame(master=frame_middle,fg_color="#555B83",border_width=0.6 , border_color="black",corner_radius=0)
        page_wish_list.pack(anchor=tkinter.W,expand = True, fill="both")

        page_wish_list_load=ctk.CTkLabel(master=page_wish_list, width=875,  height=432, fg_color="#FFFFFF",corner_radius=15,text="Comming Soon WISH List",anchor="center",font=("Arial",58),text_color="black")
        page_wish_list_load.pack(padx=15, pady=15)

    ### ACCOUNT CARD ###
    def page_account_def():
        global text_entry, notes_listbox, note_num_entry, notes

        notes = load_notes()

        page_account = ctk.CTkFrame(master=frame_middle,fg_color="#555B83",border_width=0.6 , border_color="black",corner_radius=0)
        page_account.pack(anchor=tkinter.W,expand = True, fill="both")

        page_account_nickname_label = ctk.CTkLabel(page_account,corner_radius=10)
        page_account_nickname_label.pack(side = "top", padx=30,pady=30,anchor=tkinter.W)
        page_account_nickname_label.configure(text=f"Hello {logged_in_user}",font=font10)

        # page_account_note_abnout_me = ctk.CTkLabel(page_account,corner_radius=10,text="This note is about you")
        # page_account_note_abnout_me.place(x=250,y=500)

        page_account_avatar_label = ctk.CTkLabel(page_account,corner_radius=10,image=image_14,text="")
        page_account_avatar_label.pack(side = "top", padx=40,pady=20,anchor=tkinter.W)

        page_account_aoutyou_label= ctk.CTkLabel(page_account,text="Here you can add some informations about you",text_color="white")
        page_account_aoutyou_label.place(x=280,y=129)
        page_account_aoutyou_label.configure(font=font3)

        page_account_aoutyou_textbox =ctk.CTkTextbox(page_account,width=270,height=160,activate_scrollbars=False,font=font7,corner_radius=5,fg_color="#4B5172")
        page_account_aoutyou_textbox.place(x=286,y=176)
        page_account_aoutyou_textbox.insert("0.0", f"{texk_bout_me}")

        page_account_aoutyou_textbox_button_save= ctk.CTkButton(page_account,fg_color="#555B83",text="Edit Info",bg_color='#555B83',width=60,corner_radius=5)
        page_account_aoutyou_textbox_button_save.place(x=495,y=338)

        page_account_change_photo_button= ctk.CTkButton(page_account,fg_color="#555B83",text="Edit photo",bg_color='#555B83',width=60,corner_radius=5,command=select_image)
        page_account_change_photo_button.place(x=115,y=338)

                # Funkcja ograniczająca ilość znaków do 300
        def limit_text(event=None):
            current_text = page_account_aoutyou_textbox.get("1.0", "end-1c")  # Pobierz tekst z pola
            if len(current_text) > 200:
                page_account_aoutyou_textbox.delete("1.0", "end")  # Wyczyść pole
                page_account_aoutyou_textbox.insert("1.0", current_text[:200])  # Wstaw ograniczony tekst

        # Powiązanie funkcji z wpisywaniem tekstu
        page_account_aoutyou_textbox.bind("<KeyRelease>", limit_text)

        label_text_notes_put= ctk.CTkLabel(page_account,text="Here you can put some notes",text_color="white")
        label_text_notes_put.place(x=80,y=370)
        label_text_notes_put.configure(font=font8)

        text_entry = ctk.CTkTextbox(master=page_account, width=400, height=200,fg_color="#4B5172")
        text_entry.place(x=80,y=400)

        notes_listbox = ctk.CTkTextbox(master=page_account, width=400, height=420,fg_color="#4B5172")
        notes_listbox.place(x=620,y=176)

        label_text_notes= ctk.CTkLabel(page_account,text="Your notes",text_color="white")
        label_text_notes.place(x=620,y=129)
        label_text_notes.configure(font=font8)

        note_num_entry = ctk.CTkEntry(master=page_account, placeholder_text="Enter note number to delete",width=170)
        note_num_entry.place(x=690,y=610)

        add_note_button = ctk.CTkButton(master=page_account, text="Add Note", command=add_note,fg_color="#4B5172")
        add_note_button.place(x=200,y=610)

        delete_note_button = ctk.CTkButton(master=page_account, text="Delete Note",width=80,fg_color="#4B5172",hover_color="#F95454", command=delete_note)
        delete_note_button.place(x=860,y=610)

        update_notes_listbox()

    def show_frame(frame1):
        page_general.pack_forget()
        page_account.pack_forget()
        page_password.pack_forget()
        page_version.pack_forget()

        frame1.pack(side='right', fill=ctk.BOTH, expand=True)
        # Funkcja symulująca sprawdzanie aktualizacji
    def check_for_updates():
        # Ustawiamy komunikat, że sprawdzamy aktualizacje
        update_label.configure(text="Checking for updates...")
    
    # Po 10 sekundach zmieniamy tekst na brak aktualizacji
        frame_middle.after(10000, lambda: update_label.configure(text="No updates available"))

    def zmien_kolor_zegara(new_color):
        color_var.set(new_color)  # Zmieniamy kolor
        zapisz_kolor_zegara()  # Zapisujemy nowy kolor
        aktualizuj_czas()  # Aktualizujemy czas z nowym kolorem

    def przelacz_wyswietlanie():
        # Sprawdza, czy checkbox jest zaznaczony, i odpowiednio pokazuje lub ukrywa etykiety zegara i daty
        if checkbox_var.get() == 1:  # Checkbox zaznaczony
            etykieta_data.pack(side="bottom", pady=8,padx=1)
            etykieta_czas.pack(side="bottom", pady=1,padx=1)
        else:  # Checkbox odznaczony
            etykieta_data.pack_forget()
            etykieta_czas.pack_forget()       
    # Użycie BooleanVar do przechowywania stanu checkboxa
    checkbox_var = ctk.BooleanVar(value=wczytaj_status_checkboxa())
    autostart_var = ctk.BooleanVar(value=wczytaj_status_checkbox_autostart())
    # Zmienna do przechowywania formatu czasu
    format_var = ctk.StringVar(value="24")  # Domyślnie ustawiony na 24-godzinny

    # Zmienna do przechowywania koloru zegara
    color_var = ctk.StringVar(value="#FFFFFF")  # Domyślny kolor biały

    def page_setting_def():

        # def update_new_password():
        #     new_pass_save1 = new_user_pass1.get()
        #     new_pass_save1_1 = new_user_pass1_1.get()

        #     if not new_pass_save1 or not new_pass_save1_1:
        #         tkmb.showerror(title="Błąd", message="Wprowadź hasło i je powtórz")
        #         return
        #     elif new_pass_save1 != new_pass_save1_1:
        #         tkmb.showerror(title="Błąd", message="Wprowadzone dane nie są identyczne")
        #         return
        #     hashed_new_password = hashlib.sha256(new_pass_save1.encode()).hexdigest()

        #     cursor.execute("UPDATE users SET password = %s WHERE username = %s",(hashed_new_password,logged_in_user))

        #     db.commit()

        #     tkmb.showinfo(title="Sukces", message="Hasło zostało zmienione pomyślnie.")


        page_settings = ctk.CTkFrame(master=frame_middle, fg_color="#555B83", border_width=0.6, border_color="black", corner_radius=0)
        page_settings.pack(anchor=tkinter.W, expand=True, fill="both")

        frame1 = ctk.CTkFrame(page_settings, fg_color='#555B83')
        frame1.pack(padx=10, pady=10, fill=ctk.BOTH, expand=True)

        left_frame = ctk.CTkFrame(frame1, fg_color="#4a507d", width=300, corner_radius=5, border_width=1, border_color="black")
        left_frame.pack(side='left', fill=ctk.Y)

        # Przyciski w lewym panelu
        left_frame_button_1 = ctk.CTkButton(master=left_frame, width=200, height=40, text="General", text_color="#FFFFFF", font=font2, fg_color="#4a507d", hover_color="#384069", anchor='center', command=lambda: show_frame(page_general))
        left_frame_button_1.place(x=50, y=50)

        left_frame_button_2 = ctk.CTkButton(master=left_frame, width=200, height=40, text="Account", text_color="#FFFFFF", font=font2, fg_color="#4a507d", hover_color="#384069", anchor='center', command=lambda: show_frame(page_account))
        left_frame_button_2.place(x=50, y=100)

        left_frame_button_3 = ctk.CTkButton(master=left_frame, width=200, height=40, text="Password", text_color="#FFFFFF", font=font2, fg_color="#4a507d", hover_color="#384069", anchor='center', command=lambda: show_frame(page_password))
        left_frame_button_3.place(x=50, y=150)

        left_frame_button_4 = ctk.CTkButton(master=left_frame, width=200, height=40, text="Version", text_color="#FFFFFF", font=font2, fg_color="#4a507d", hover_color="#384069", anchor='center', command=lambda: show_frame(page_version))
        left_frame_button_4.place(x=50, y=200)

        # Strony (Lewy panel)
        global page_general, page_account, page_password, page_version, update_label

        ### Page General ###

        def zapisz_status_checkboxa():
        # Zapisuje aktualny stan checkboxa do pliku przy użyciu pickle
            with open(STATUS_FILE, "wb") as f:
                pickle.dump(checkbox_var.get(), f)

        def zapisz_status_checkboxa_autostart():
        # Zapisuje aktualny stan checkboxa do pliku przy użyciu pickle
            with open(AUTOSTART_FILE, "wb") as f:
                pickle.dump(autostart_var.get(), f)

       #Zapisywanie wszytskich funkcji odnoscie czasu w programie
        main.protocol("WM_DELETE_WINDOW", lambda: (zapisz_status_checkboxa(), zapisz_format_czasu(), zapisz_kolor_zegara(),zapisz_status_checkboxa_autostart(), main.destroy()))

        page_general = ctk.CTkFrame(frame1,fg_color="#4a507d",corner_radius=5,border_width=1,border_color="black")
        page_general_label = ctk.CTkLabel(page_general, fg_color="#4a507d", text="General Page",text_color="white")
        page_general_label.place(x=40,y=30)
        page_general_label.configure(font=font9)

        page_general_time_label = ctk.CTkLabel(page_general, fg_color="#4a507d", text="Clock Settings",text_color="white")
        page_general_time_label.place(x=60,y=100)
        page_general_time_label.configure(font=font2)

        checkbox_time = ctk.CTkCheckBox(master=page_general, text="Show clock", variable=checkbox_var, command=przelacz_wyswietlanie)
        checkbox_time.place(x=60,y=140)

        radio_12 = ctk.CTkRadioButton(master=page_general, text="12-hour-clock", variable=format_var, value="12", command=zapisz_format_czasu)
        radio_12.place(x=90,y=180)

        radio_24 = ctk.CTkRadioButton(master=page_general, text="24-hour-clock", variable=format_var, value="24", command=zapisz_format_czasu)
        radio_24.place(x=90,y=220)

        # Menu rozwijane do zmiany koloru zegara
        kolor_menu = ctk.CTkOptionMenu(
            master=page_general,
            values=["white", "black", "blue", "purple", "red","yellow","orange","green","brown","pink","gray"],
            command=zmien_kolor_zegara,
            dropdown_fg_color='#3F4462'
        )
        kolor_menu.set("Change clock color")
        kolor_menu.place(x=220,y=140)

        page_general_autostart_label = ctk.CTkLabel(page_general, fg_color="#4a507d", text="Auto Start Settings",text_color="white")
        page_general_autostart_label.place(x=60,y=280)
        page_general_autostart_label.configure(font=font2)

        # Checkbox do autostartu
        autostart_checkbox = ctk.CTkCheckBox(master=page_general, text="Start when system start", variable=autostart_var, command=lambda: dodaj_do_autostartu() if autostart_var.get() else usun_z_autostartu())
        autostart_checkbox.place(x=60,y=320)

        # Etykieta wyboru trybu zasilania
        power_label = ctk.CTkLabel(page_general, fg_color="#4a507d",text="Select power option:",text_color="white")
        power_label.place(x=60,y=380)
        power_label.configure(font=font2)

        # Menu rozwijane dla trybu zasilania
        power_dropdown = ctk.CTkOptionMenu(page_general, variable=power_mode_var, values=power_modes)
        power_dropdown.place(x=80,y=420)

        # Przycisk ustawienia trybu zasilania
        set_power_button = ctk.CTkButton(page_general, text="Ustaw tryb zasilania", command=set_power_mode)
        set_power_button.place(x=80,y=460)


        ### Page Account ###
        def save_label_1():
            new_user_username1 = new_user_username.get()
            if not new_user_username1:
                tkmb.showerror(title="Błąd", message="Wprowadź nową nazwę użytkownika")
                return

            # Sprawdzenie, czy nowa nazwa użytkownika już istnieje w bazie danych
            cursor.execute("SELECT username FROM users WHERE username = %s", (new_user_username1,))
            existing_username = cursor.fetchone()

            if existing_username:
                tkmb.showerror(title="Błąd", message="Podana nazwa użytkownika już istnieje")
                return
                
            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET username = %s WHERE mail = %s", (new_user_username1, logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Mail został zmieniony pomyślnie.")

        def save_label_2():
            new_user_email1 = new_user_email.get()
            if not new_user_email1:
                tkmb.showerror(title="Błąd", message="Wprowadź nowy mail")
                return

            # Sprawdzenie, czy nowa nazwa użytkownika już istnieje w bazie danych
            cursor.execute("SELECT mail FROM users WHERE username = %s", (new_user_email1,))
            existing_mail = cursor.fetchone()

            if existing_mail:
                tkmb.showerror(title="Błąd", message="Podany mail już istnieje")
                return
            
            old_mail = logged_in_user

            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET mail = %s WHERE mail = %s", (new_user_email1, old_mail))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Nazwa została zmieniona pomyślnie.")

        def save_label_3():
            new_user_post_addres1 = new_user_post_addres.get()
            if not new_user_post_addres1:
                tkmb.showerror(title="Błąd", message="Wprowadź nowy adres zamieszkania")
                return

            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET post_adress = %s WHERE mail = %s", (new_user_post_addres1, logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Adres zamieszkania został zmieniony pomyślnie.")
        def save_label_4():
            new_user_post_code1 = new_user_post_code.get()
            if not new_user_post_code1:
                tkmb.showerror(title="Błąd", message="Wprowadź nowy kod-pocztowy")
                return

            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET postal_code = %s WHERE mail = %s", (new_user_post_code1, logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Kod-pocztowy został zmieniony pomyślnie.")

        def save_label_5():
            new_user_country1 = new_user_country.get()
            if not new_user_country1:
                tkmb.showerror(title="Błąd", message="Wprowadź nowy kraj")
                return

            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET country = %s WHERE mail = %s", (new_user_country1, logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Kraj został zmieniony pomyślnie.")
        def save_label_6():
            new_user_phone_number1 = new_user_phone_number.get()
            if not new_user_phone_number1:
                tkmb.showerror(title="Błąd", message="Wprowadź nowy numer telefonu")
                return
            
            if not (new_user_phone_number1.isdigit() and len(new_user_phone_number1) == 9):
                tkmb.showerror(title="Błąd", message="Numer telefonu musi składać się z 9 cyfr")
                return

            # Zaktualizowanie nazwy użytkownika
            cursor.execute("UPDATE users SET phone_number = %s WHERE mail = %s", (new_user_phone_number1, logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Numer telefonu został zmieniony pomyślnie.")
        def delete_account():
            # Wyświetlenie okna z ostrzeżeniem i pytaniem o potwierdzenie
            confirm = tkmb.askyesno(title="Potwierdzenie usunięcia", message=f"Czy na pewno chcesz usunąć użytkownika o adresie e-mail: {logged_in_user}?")

        # Sprawdzenie, czy użytkownik potwierdził usunięcie
            if not confirm:
                tkmb.showinfo(title="Anulowano", message="Operacja usunięcia została anulowana.")
                return

            # Zapytanie do usunięcia użytkownika na podstawie e-maila
            cursor.execute("DELETE FROM users WHERE mail = %s", (logged_in_user,))

            # Zatwierdzenie zmian
            db.commit()

            tkmb.showinfo(title="Sukces", message="Użytkownik został pomyślnie usunięty.")
            exit_app()

        page_account = ctk.CTkFrame(frame1, fg_color="#4a507d", corner_radius=5, border_width=1, border_color="black")
        page_account_label = ctk.CTkLabel(page_account, fg_color="#4a507d", text="Account Page",text_color="white")
        page_account_label.place(x=40,y=30)
        page_account_label.configure(font=font9)

        change_account_label=ctk.CTkLabel(page_account, text="Chane account values: ", fg_color="#4a507d",text_color="white")
        change_account_label.place(x=60,y=100)
        change_account_label.configure(font=font2)

        change_account_label_1=ctk.CTkLabel(page_account, text="Input new username: ", fg_color="#4a507d",text_color="white")
        change_account_label_1.place(x=60,y=140)
        change_account_label_1.configure(font=font8)

        new_user_username=ctk.CTkEntry(page_account, width=220, placeholder_text='username')
        new_user_username.place(x=60, y=170)
        new_user_username_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_1)
        new_user_username_button.place(x=280,y=170)

        change_account_label_2=ctk.CTkLabel(page_account, text="Input new e-mail: ", fg_color="#4a507d",text_color="white")
        change_account_label_2.place(x=60,y=200)
        change_account_label_2.configure(font=font8)

        new_user_email=ctk.CTkEntry(page_account, width=220, placeholder_text='e-mail')
        new_user_email.place(x=60, y=230)
        new_user_email_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_2)
        new_user_email_button.place(x=280,y=230)

        change_account_label_3=ctk.CTkLabel(page_account, text="Input new Adress: ", fg_color="#4a507d",text_color="white")
        change_account_label_3.place(x=60,y=260)
        change_account_label_3.configure(font=font8)

        new_user_post_addres=ctk.CTkEntry(page_account, width=220, placeholder_text='adress')
        new_user_post_addres.place(x=60, y=290)
        new_user_post_addres_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_3)
        new_user_post_addres_button.place(x=280,y=290)

        change_account_label_4=ctk.CTkLabel(page_account, text="Input new post-code: ", fg_color="#4a507d",text_color="white")
        change_account_label_4.place(x=60,y=320)
        change_account_label_4.configure(font=font8)

        new_user_post_code=ctk.CTkEntry(page_account, width=220, placeholder_text='post-code')
        new_user_post_code.place(x=60, y=350)
        new_user_post_code_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_4)
        new_user_post_code_button.place(x=280,y=350)

        change_account_label_5=ctk.CTkLabel(page_account, text="Input new country: ", fg_color="#4a507d",text_color="white")
        change_account_label_5.place(x=60,y=380)
        change_account_label_5.configure(font=font8)

        new_user_country=ctk.CTkEntry(page_account, width=220, placeholder_text='country')
        new_user_country.place(x=60, y=410)
        new_user_country_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_5)
        new_user_country_button.place(x=280,y=410)

        change_account_label_6=ctk.CTkLabel(page_account, text="Input new phone-number: ", fg_color="#4a507d",text_color="white")
        change_account_label_6.place(x=60,y=440)
        change_account_label_6.configure(font=font8)

        new_user_phone_number=ctk.CTkEntry(page_account, width=220, placeholder_text='phone-number')
        new_user_phone_number.place(x=60, y=470)
        new_user_phone_number_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_12,width=20,height=20,fg_color='#4a507d',command=save_label_6)
        new_user_phone_number_button.place(x=280,y=470)

        delete_account_label=ctk.CTkLabel(page_account, text="Delete Account: ", fg_color="#4a507d",text_color="white")
        delete_account_label.place(x=60,y=520)
        delete_account_label.configure(font=font2)

        delete_account_button=ctk.CTkButton(page_account,text="",corner_radius=20,image=image_13,width=40,height=40,fg_color='#4a507d',hover_color="#F95454",command=delete_account)
        delete_account_button.place(x=80,y=560)

        ### Page Password ###
        def update_new_password():
            new_pass_save1 = new_user_pass1.get()
            new_pass_save1_1 = new_user_pass1_1.get()

            if not new_pass_save1 or not new_pass_save1_1:
                tkmb.showerror(title="Błąd", message="Wprowadź hasło i je powtórz")
                return
            elif new_pass_save1 != new_pass_save1_1:
                tkmb.showerror(title="Błąd", message="Wprowadzone dane nie są identyczne")
                return
            hashed_new_password = hashlib.sha256(new_pass_save1.encode()).hexdigest()

            cursor.execute("UPDATE users SET password = %s WHERE username = %s",(hashed_new_password,logged_in_user))

            db.commit()

            tkmb.showinfo(title="Sukces", message="Hasło zostało zmienione pomyślnie.")

        page_password = ctk.CTkFrame(frame1, fg_color="#4a507d", corner_radius=5, border_width=1, border_color="black")
        page_password_label = ctk.CTkLabel(page_password, fg_color="#4a507d", text="Password Page",text_color="white")
        page_password_label.place(x=40,y=30)
        page_password_label.configure(font=font9)

        change_password_label=ctk.CTkLabel(page_password, text="Change pasword: ", fg_color="#4a507d",text_color="white")
        change_password_label.place(x=60,y=100)
        change_password_label.configure(font=font2)

        change_password_label1=ctk.CTkLabel(page_password, text="Input new password: ", fg_color="#4a507d",text_color="white")
        change_password_label1.place(x=60,y=140)
        change_password_label1.configure(font=font8)

        new_user_pass1=ctk.CTkEntry(page_password, width=220, placeholder_text='Password', show="*")
        new_user_pass1.place(x=60, y=170)

        change_password_label2=ctk.CTkLabel(page_password, text="Retype new password: ", fg_color="#4a507d",text_color="white")
        change_password_label2.place(x=60,y=210)
        change_password_label2.configure(font=font8)

        new_user_pass1_1=ctk.CTkEntry(page_password, width=220, placeholder_text='Retype password', show="*")
        new_user_pass1_1.place(x=60, y=240)

        new_user_pass_button_save=ctk.CTkButton(page_password, width=220, text="Save", corner_radius=6,fg_color="#4a507d",command=update_new_password)
        new_user_pass_button_save.place(x=60, y=280)


        ### Page Version ###
        page_version = ctk.CTkFrame(frame1, fg_color="#4a507d", corner_radius=5, border_width=1, border_color="black")
        page_version_label = ctk.CTkLabel(page_version, fg_color="#4a507d", text="Version Page",text_color="white")
        page_version_label.place(x=40,y=30)
        page_version_label.configure(font=font9)

        page_version_label1 = ctk.CTkLabel(page_version, fg_color="#4a507d", text="PlayQuest version: 1.0",text_color="white")
        page_version_label1.place(x=60,y=100)
        page_version_label1.configure(font=font5)

        page_version_label2 = ctk.CTkLabel(page_version, fg_color="#4a507d", text="Check for updates",text_color="white")
        page_version_label2.place(x=60,y=140)
        page_version_label2.configure(font=font2)

        # Dodanie przycisku "Check for Updates"
        check_updates_button = ctk.CTkButton(page_version,image=image_11, text="",width=24,height=24, fg_color="#4a507d",command=check_for_updates)
        check_updates_button.place(x=220,y=135)

        # Etykieta z informacją o aktualizacjach
        update_label = ctk.CTkLabel(page_version, text="", width=150, height=30, fg_color="#4a507d")
        update_label.place(x=60,y=190)

        # Początkowo pokaż stronę "General"
        show_frame(page_general)   

    # page_shop.tkraise()

    
    def indicators(page):
        hide_pages()
        page()

    def_page_shop_card()
    #odnoiscie czasu
    wczytaj_status_checkboxa()
    przelacz_wyswietlanie()
    wczytaj_format_czasu()
    aktualizuj_czas()
    #Zmiana koloru zegara i daty
    wczytaj_kolor_zegara()
    wczytaj_status_checkbox_autostart()
    menu_frame.pack_forget()


    main.mainloop()

app.mainloop()


