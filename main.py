from tkinter import *
from tkinter import ttk
import tkintermapview

# --- Nowe klasy danych ---
class JednostkaStrazy:
    def __init__(self, nazwa, lokalizacja):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.pracownicy = []  # lista obiektów Pracownik
        self.pozary = []      # lista obiektów Pozar
        self.coordinates = get_coordinates(lokalizacja)
        self.marker = None

class Pracownik:
    def __init__(self, imie, nazwisko, lokalizacja, jednostka=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.jednostka = jednostka  # referencja do JednostkaStrazy
        self.coordinates = get_coordinates(lokalizacja)
        self.marker = None

class Pozar:
    def __init__(self, lokalizacja, opis, jednostka=None):
        self.lokalizacja = lokalizacja
        self.opis = opis
        self.jednostka = jednostka  # referencja do JednostkaStrazy
        self.coordinates = get_coordinates(lokalizacja)
        self.marker = None

# --- Listy główne ---
jednostki_strazy = []  # lista JednostkaStrazy
pracownicy = []        # lista Pracownik
pozary = []            # lista Pozar

# --- Funkcja do pobierania współrzędnych ---
def get_coordinates(location):
    import requests
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location,
        'format': 'json',
        'limit': 1,
        'accept-language': 'pl'
    }
    headers = {'User-Agent': 'Mozilla/5.0 (projekt_straz)'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        return [float(data[0]['lat']), float(data[0]['lon'])]
    else:
        return [52.23, 21.00]  # domyślne współrzędne (Warszawa) jeśli nie znaleziono

# --- GUI ---
root = Tk()
root.title('System zarządzania strażą pożarną')
root.geometry("1400x800")
root.minsize(900, 600)

# Zakładki
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

# --- Zakładka Jednostki ---
frame_jednostki = Frame(notebook)
notebook.add(frame_jednostki, text='Jednostki')

frame_form_jednostka = Frame(frame_jednostki)
frame_form_jednostka.pack(fill=X, padx=5, pady=5)
Label(frame_form_jednostka, text='Nazwa:').pack(side=LEFT)
entry_nazwa_jednostki = Entry(frame_form_jednostka, width=12)
entry_nazwa_jednostki.pack(side=LEFT, padx=2)
Label(frame_form_jednostka, text='Lokalizacja:').pack(side=LEFT)
entry_lokalizacja_jednostki = Entry(frame_form_jednostka, width=12)
entry_lokalizacja_jednostki.pack(side=LEFT, padx=2)
button_dodaj_jednostke = Button(frame_form_jednostka, text='Dodaj', command=lambda: dodaj_jednostke())
button_dodaj_jednostke.pack(side=LEFT, padx=2)
button_usun_jednostke = Button(frame_form_jednostka, text='Usuń', command=lambda: usun_jednostke())
button_usun_jednostke.pack(side=LEFT, padx=2)
button_edytuj_jednostke = Button(frame_form_jednostka, text='Edytuj', command=lambda: edytuj_jednostke())
button_edytuj_jednostke.pack(side=LEFT, padx=2)
button_szczegoly_jednostki = Button(frame_form_jednostka, text='Pokaż szczegóły', command=lambda: pokaz_szczegoly_jednostki())
button_szczegoly_jednostki.pack(side=LEFT, padx=2)

listbox_jednostki = Listbox(frame_jednostki)
listbox_jednostki.pack(fill=BOTH, expand=True, padx=5, pady=5)

mapa_jednostki = tkintermapview.TkinterMapView(frame_jednostki, width=600, height=300, corner_radius=0)
mapa_jednostki.pack(fill=BOTH, expand=True, padx=5, pady=5)
mapa_jednostki.set_position(52.23, 21.00)
mapa_jednostki.set_zoom(6)

# --- Zakładka Pracownicy ---
frame_pracownicy = Frame(notebook)
notebook.add(frame_pracownicy, text='Pracownicy')

frame_form_pracownik = Frame(frame_pracownicy)
frame_form_pracownik.pack(fill=X, padx=5, pady=5)
Label(frame_form_pracownik, text='Imię:').pack(side=LEFT)
entry_imie_pracownika = Entry(frame_form_pracownik, width=10)
entry_imie_pracownika.pack(side=LEFT, padx=2)
Label(frame_form_pracownik, text='Nazwisko:').pack(side=LEFT)
entry_nazwisko_pracownika = Entry(frame_form_pracownik, width=10)
entry_nazwisko_pracownika.pack(side=LEFT, padx=2)
Label(frame_form_pracownik, text='Lokalizacja:').pack(side=LEFT)
entry_lokalizacja_pracownika = Entry(frame_form_pracownik, width=12)
entry_lokalizacja_pracownika.pack(side=LEFT, padx=2)
Label(frame_form_pracownik, text='Jednostka:').pack(side=LEFT)
combobox_jednostka_pracownika = ttk.Combobox(frame_form_pracownik, width=15, state='readonly')
combobox_jednostka_pracownika.pack(side=LEFT, padx=2)
button_dodaj_pracownika = Button(frame_form_pracownik, text='Dodaj', command=lambda: dodaj_pracownika())
button_dodaj_pracownika.pack(side=LEFT, padx=2)
button_usun_pracownika = Button(frame_form_pracownik, text='Usuń', command=lambda: usun_pracownika())
button_usun_pracownika.pack(side=LEFT, padx=2)
button_edytuj_pracownika = Button(frame_form_pracownik, text='Edytuj', command=lambda: edytuj_pracownika())
button_edytuj_pracownika.pack(side=LEFT, padx=2)
button_szczegoly_pracownika = Button(frame_form_pracownik, text='Pokaż szczegóły', command=lambda: pokaz_szczegoly_pracownika())
button_szczegoly_pracownika.pack(side=LEFT, padx=2)

listbox_pracownicy = Listbox(frame_pracownicy)
listbox_pracownicy.pack(fill=BOTH, expand=True, padx=5, pady=5)

mapa_pracownicy = tkintermapview.TkinterMapView(frame_pracownicy, width=600, height=300, corner_radius=0)
mapa_pracownicy.pack(fill=BOTH, expand=True, padx=5, pady=5)
mapa_pracownicy.set_position(52.23, 21.00)
mapa_pracownicy.set_zoom(6)

# --- Zakładka Pożary ---
frame_pozary = Frame(notebook)
notebook.add(frame_pozary, text='Pożary')

frame_form_pozar = Frame(frame_pozary)
frame_form_pozar.pack(fill=X, padx=5, pady=5)
Label(frame_form_pozar, text='Lokalizacja:').pack(side=LEFT)
entry_lokalizacja_pozaru = Entry(frame_form_pozar, width=15)
entry_lokalizacja_pozaru.pack(side=LEFT, padx=2)
Label(frame_form_pozar, text='Opis:').pack(side=LEFT)
entry_opis_pozaru = Entry(frame_form_pozar, width=15)
entry_opis_pozaru.pack(side=LEFT, padx=2)
Label(frame_form_pozar, text='Jednostka:').pack(side=LEFT)
combobox_jednostka_pozaru = ttk.Combobox(frame_form_pozar, width=15, state='readonly')
combobox_jednostka_pozaru.pack(side=LEFT, padx=2)
button_dodaj_pozar = Button(frame_form_pozar, text='Dodaj', command=lambda: dodaj_pozar())
button_dodaj_pozar.pack(side=LEFT, padx=2)
button_usun_pozar = Button(frame_form_pozar, text='Usuń', command=lambda: usun_pozar())
button_usun_pozar.pack(side=LEFT, padx=2)
button_edytuj_pozar = Button(frame_form_pozar, text='Edytuj', command=lambda: edytuj_pozar())
button_edytuj_pozar.pack(side=LEFT, padx=2)
button_szczegoly_pozaru = Button(frame_form_pozar, text='Pokaż szczegóły', command=lambda: pokaz_szczegoly_pozaru())
button_szczegoly_pozaru.pack(side=LEFT, padx=2)

listbox_pozary = Listbox(frame_pozary)
listbox_pozary.pack(fill=BOTH, expand=True, padx=5, pady=5)

mapa_pozary = tkintermapview.TkinterMapView(frame_pozary, width=600, height=300, corner_radius=0)
mapa_pozary.pack(fill=BOTH, expand=True, padx=5, pady=5)
mapa_pozary.set_position(52.23, 21.00)
mapa_pozary.set_zoom(6)

# --- Funkcja do odświeżania comboboxów jednostek ---
def odswiez_comboboxy_jednostek():
    jednostki = [j.nazwa for j in jednostki_strazy]
    combobox_jednostka_pracownika['values'] = jednostki
    combobox_jednostka_pozaru['values'] = jednostki

# --- Funkcje obsługi jednostek ---
def odswiez_liste_jednostek():
    listbox_jednostki.delete(0, END)
    for idx, j in enumerate(jednostki_strazy):
        listbox_jednostki.insert(idx, f"{j.nazwa} ({j.lokalizacja})")
    odswiez_comboboxy_jednostek()
    # Odśwież markery na mapie jednostek
    mapa_jednostki.delete_all_marker()
    for j in jednostki_strazy:
        j.marker = mapa_jednostki.set_marker(j.coordinates[0], j.coordinates[1], text=j.nazwa)

def dodaj_jednostke():
    nazwa = entry_nazwa_jednostki.get()
    lokalizacja = entry_lokalizacja_jednostki.get()
    if not nazwa or not lokalizacja:
        return
    jednostka = JednostkaStrazy(nazwa, lokalizacja)
    jednostka.marker = mapa_jednostki.set_marker(jednostka.coordinates[0], jednostka.coordinates[1], text=nazwa)
    jednostki_strazy.append(jednostka)
    odswiez_liste_jednostek()
    entry_nazwa_jednostki.delete(0, END)
    entry_lokalizacja_jednostki.delete(0, END)

def usun_jednostke():
    idx = listbox_jednostki.curselection()
    if not idx:
        return
    idx = idx[0]
    jednostka = jednostki_strazy[idx]
    if jednostka.marker:
        jednostka.marker.delete()
    jednostki_strazy.pop(idx)
    odswiez_liste_jednostek()

def edytuj_jednostke():
    idx = listbox_jednostki.curselection()
    if not idx:
        return
    idx = idx[0]
    jednostka = jednostki_strazy[idx]
    entry_nazwa_jednostki.delete(0, END)
    entry_lokalizacja_jednostki.delete(0, END)
    entry_nazwa_jednostki.insert(0, jednostka.nazwa)
    entry_lokalizacja_jednostki.insert(0, jednostka.lokalizacja)
    button_dodaj_jednostke.config(text='Zapisz', command=lambda: zapisz_edycje_jednostki(idx))

def zapisz_edycje_jednostki(idx):
    nazwa = entry_nazwa_jednostki.get()
    lokalizacja = entry_lokalizacja_jednostki.get()
    jednostka = jednostki_strazy[idx]
    jednostka.nazwa = nazwa
    jednostka.lokalizacja = lokalizacja
    jednostka.coordinates = get_coordinates(lokalizacja)
    if jednostka.marker:
        jednostka.marker.delete()
    jednostka.marker = mapa_jednostki.set_marker(jednostka.coordinates[0], jednostka.coordinates[1], text=nazwa)
    odswiez_liste_jednostek()
    entry_nazwa_jednostki.delete(0, END)
    entry_lokalizacja_jednostki.delete(0, END)
    button_dodaj_jednostke.config(text='Dodaj', command=lambda: dodaj_jednostke())

# --- Funkcje obsługi pracowników ---
def odswiez_liste_pracownikow():
    listbox_pracownicy.delete(0, END)
    for idx, p in enumerate(pracownicy):
        jednostka = p.jednostka.nazwa if p.jednostka else '-'
        listbox_pracownicy.insert(idx, f"{p.imie} {p.nazwisko} ({p.lokalizacja}) [{jednostka}]")
    # Odśwież markery na mapie pracowników
    mapa_pracownicy.delete_all_marker()
    for p in pracownicy:
        p.marker = mapa_pracownicy.set_marker(p.coordinates[0], p.coordinates[1], text=f"{p.imie} {p.nazwisko}")

def dodaj_pracownika():
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()
    jednostka_nazwa = combobox_jednostka_pracownika.get()
    jednostka = next((j for j in jednostki_strazy if j.nazwa == jednostka_nazwa), None) if jednostka_nazwa else None
    pracownik = Pracownik(imie, nazwisko, lokalizacja, jednostka)
    pracownik.marker = mapa_pracownicy.set_marker(pracownik.coordinates[0], pracownik.coordinates[1], text=f"{imie} {nazwisko}")
    pracownicy.append(pracownik)
    if jednostka:
        jednostka.pracownicy.append(pracownik)
    odswiez_liste_pracownikow()
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    combobox_jednostka_pracownika.set('')

def usun_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = pracownicy[idx]
    if pracownik.marker:
        pracownik.marker.delete()
    if pracownik.jednostka and pracownik in pracownik.jednostka.pracownicy:
        pracownik.jednostka.pracownicy.remove(pracownik)
    pracownicy.pop(idx)
    odswiez_liste_pracownikow()

def edytuj_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = pracownicy[idx]
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    combobox_jednostka_pracownika.set('')
    entry_imie_pracownika.insert(0, pracownik.imie)
    entry_nazwisko_pracownika.insert(0, pracownik.nazwisko)
    entry_lokalizacja_pracownika.insert(0, pracownik.lokalizacja)
    if pracownik.jednostka:
        combobox_jednostka_pracownika.set(pracownik.jednostka.nazwa)
    button_dodaj_pracownika.config(text='Zapisz', command=lambda: zapisz_edycje_pracownika(idx))

def zapisz_edycje_pracownika(idx):
    imie = entry_imie_pracownika.get()
    nazwisko = entry_nazwisko_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()
    jednostka_nazwa = combobox_jednostka_pracownika.get()
    jednostka = next((j for j in jednostki_strazy if j.nazwa == jednostka_nazwa), None) if jednostka_nazwa else None
    pracownik = pracownicy[idx]
    if pracownik.jednostka and pracownik in pracownik.jednostka.pracownicy:
        pracownik.jednostka.pracownicy.remove(pracownik)
    pracownik.imie = imie
    pracownik.nazwisko = nazwisko
    pracownik.lokalizacja = lokalizacja
    pracownik.jednostka = jednostka
    pracownik.coordinates = get_coordinates(lokalizacja)
    if pracownik.marker:
        pracownik.marker.delete()
    pracownik.marker = mapa_pracownicy.set_marker(pracownik.coordinates[0], pracownik.coordinates[1], text=f"{imie} {nazwisko}")
    if jednostka:
        jednostka.pracownicy.append(pracownik)
    odswiez_liste_pracownikow()
    entry_imie_pracownika.delete(0, END)
    entry_nazwisko_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)
    combobox_jednostka_pracownika.set('')
    button_dodaj_pracownika.config(text='Dodaj', command=lambda: dodaj_pracownika())

# --- Funkcje obsługi pożarów ---
def odswiez_liste_pozarow():
    listbox_pozary.delete(0, END)
    for idx, p in enumerate(pozary):
        jednostka = p.jednostka.nazwa if p.jednostka else '-'
        listbox_pozary.insert(idx, f"{p.lokalizacja} - {p.opis} [{jednostka}]")
    # Odśwież markery na mapie pożarów
    mapa_pozary.delete_all_marker()
    for p in pozary:
        p.marker = mapa_pozary.set_marker(p.coordinates[0], p.coordinates[1], text=f"Pożar: {p.opis}")

def dodaj_pozar():
    lokalizacja = entry_lokalizacja_pozaru.get()
    opis = entry_opis_pozaru.get()
    jednostka_nazwa = combobox_jednostka_pozaru.get()
    jednostka = next((j for j in jednostki_strazy if j.nazwa == jednostka_nazwa), None) if jednostka_nazwa else None
    pozar = Pozar(lokalizacja, opis, jednostka)
    pozar.marker = mapa_pozary.set_marker(pozar.coordinates[0], pozar.coordinates[1], text=f"Pożar: {opis}")
    pozary.append(pozar)
    if jednostka:
        jednostka.pozary.append(pozar)
    odswiez_liste_pozarow()
    entry_lokalizacja_pozaru.delete(0, END)
    entry_opis_pozaru.delete(0, END)
    combobox_jednostka_pozaru.set('')

def usun_pozar():
    idx = listbox_pozary.curselection()
    if not idx:
        return
    idx = idx[0]
    pozar = pozary[idx]
    if pozar.marker:
        pozar.marker.delete()
    if pozar.jednostka and pozar in pozar.jednostka.pozary:
        pozar.jednostka.pozary.remove(pozar)
    pozary.pop(idx)
    odswiez_liste_pozarow()

def edytuj_pozar():
    idx = listbox_pozary.curselection()
    if not idx:
        return
    idx = idx[0]
    pozar = pozary[idx]
    entry_lokalizacja_pozaru.delete(0, END)
    entry_opis_pozaru.delete(0, END)
    combobox_jednostka_pozaru.set('')
    entry_lokalizacja_pozaru.insert(0, pozar.lokalizacja)
    entry_opis_pozaru.insert(0, pozar.opis)
    if pozar.jednostka:
        combobox_jednostka_pozaru.set(pozar.jednostka.nazwa)
    button_dodaj_pozar.config(text='Zapisz', command=lambda: zapisz_edycje_pozaru(idx))

def zapisz_edycje_pozaru(idx):
    lokalizacja = entry_lokalizacja_pozaru.get()
    opis = entry_opis_pozaru.get()
    jednostka_nazwa = combobox_jednostka_pozaru.get()
    jednostka = next((j for j in jednostki_strazy if j.nazwa == jednostka_nazwa), None) if jednostka_nazwa else None
    pozar = pozary[idx]
    if pozar.jednostka and pozar in pozar.jednostka.pozary:
        pozar.jednostka.pozary.remove(pozar)
    pozar.lokalizacja = lokalizacja
    pozar.opis = opis
    pozar.jednostka = jednostka
    pozar.coordinates = get_coordinates(lokalizacja)
    if pozar.marker:
        pozar.marker.delete()
    pozar.marker = mapa_pozary.set_marker(pozar.coordinates[0], pozar.coordinates[1], text=f"Pożar: {opis}")
    if jednostka:
        jednostka.pozary.append(pozar)
    odswiez_liste_pozarow()
    entry_lokalizacja_pozaru.delete(0, END)
    entry_opis_pozaru.delete(0, END)
    combobox_jednostka_pozaru.set('')
    button_dodaj_pozar.config(text='Dodaj', command=lambda: dodaj_pozar())

# --- Funkcje szczegółów ---
def pokaz_szczegoly_jednostki():
    idx = listbox_jednostki.curselection()
    if not idx:
        return
    idx = idx[0]
    jednostka = jednostki_strazy[idx]
    if jednostka.marker:
        mapa_jednostki.set_zoom(15)
        mapa_jednostki.set_position(jednostka.coordinates[0], jednostka.coordinates[1])

def pokaz_szczegoly_pracownika():
    idx = listbox_pracownicy.curselection()
    if not idx:
        return
    idx = idx[0]
    pracownik = pracownicy[idx]
    if pracownik.marker:
        mapa_pracownicy.set_zoom(15)
        mapa_pracownicy.set_position(pracownik.coordinates[0], pracownik.coordinates[1])

def pokaz_szczegoly_pozaru():
    idx = listbox_pozary.curselection()
    if not idx:
        return
    idx = idx[0]
    pozar = pozary[idx]
    if pozar.marker:
        mapa_pozary.set_zoom(15)
        mapa_pozary.set_position(pozar.coordinates[0], pozar.coordinates[1])

# --- Automatyczne odświeżenie listy przy starcie ---
odswiez_liste_jednostek()
odswiez_liste_pracownikow()
odswiez_liste_pozarow()
odswiez_comboboxy_jednostek()

root.mainloop()
# --- KONIEC SZKIELETU ---
