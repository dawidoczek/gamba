import json
import random
import time
import threading
class Gamba:
    colors = {
        "Red": "\033[41m",
        "Green": "\033[42m",
        "Yellow": "\033[43m",
        "Blue": "\033[44m",
        "Purple": "\033[45m",
        "Cyan": "\033[46m",
        "Reset": "\033[0m" 
    }
    symbols = ['🍒', '🍋', '🍉', '🔔','🍀','💰',"💎","🃏","💣"]
    wyniki = []
    odds =  [21,21,12,10,8,7,6,3,4]
    tabela_wyplat = {
        '🍒': {2: 1, 3: 2, 4: 5, 5: 8},
        '🍋': {2: 1, 3: 2, 4: 5, 5: 8},
        '🍉': {2: 2, 3: 4, 4: 10, 5: 20},
        '🔔': {3: 10, 4: 20, 5: 60},
        '🍀': {3: 50, 4: 100, 5: 150},
        '💰': {3: 40, 4: 80, 5: 120},
        '💎': {3: 125, 4: 250, 5: 400},
        '🃏': {3: 300, 4: 600, 5: 900},
        '💣': {3: 0, 4: 0, 5: 0} 
    }

    linie_wygrywajace = {
        "Linia 1 (Środek)":       [(0,1), (1,1), (2,1), (3,1), (4,1)],
        "Linia 2 (Góra)":         [(0,0), (1,0), (2,0), (3,0), (4,0)],
        "Linia 3 (Dół)":          [(0,2), (1,2), (2,2), (3,2), (4,2)],
        "Linia 4 (V)":            [(0,0), (1,1), (2,2), (3,1), (4,0)],
        "Linia 5 (Odwrócone V)":  [(0,2), (1,1), (2,0), (3,1), (4,2)],
        "Linia 6 (Zygzak Górny)": [(0,0), (1,1), (2,0), (3,1), (4,0)], 
        "Linia 7 (Zygzak Dolny)": [(0,2), (1,1), (2,2), (3,1), (4,2)],    
    }

    def __init__(self, plik):
        self.dane = plik
        self.free_spins = 0
        self.kasa = 0
        self.stawka = 10
        
        self.spiny_lacznie = 0
        self.wygrane_razy = 0
        self.wygrana_kasa_lacznie = 0
        
        self.ostatnia_wiadomosc = ""
        
        self.load()
        
        if not self.wyniki:
            self.wyniki = [['💎']*5, ['💎']*5, ['💎']*5]
            
        print("\n" * 11) 
        
        self.graj()

    def symuluj_rtp(self, liczba_spinow=100000):
        print(f"\n Uruchamiam symulację RTP na {liczba_spinow} spinów... Proszę czekać.")
        start_time = time.time()
        
        calkowity_wklad = 0
        calkowita_wygrana = 0
        symulowane_free_spiny = 0
        bonus_do_wygranej = max(0, (self.stawka - 10) * 0.10)
        
        spiny_do_wykonania = liczba_spinow
        
        
        wygrane_ze_symboli = {}
        najwieksza_pojedyncza_wygrana = 0
        krok_postepu = max(1, liczba_spinow // 100) 
        
        while spiny_do_wykonania > 0 or symulowane_free_spiny > 0:
            
            
            if symulowane_free_spiny == 0 and spiny_do_wykonania % krok_postepu == 0:
                procent = ((liczba_spinow - spiny_do_wykonania) / liczba_spinow) * 100
                print(f"\r⏳ Postęp symulacji: {procent:.0f}%...", end="", flush=True)
            
            if symulowane_free_spiny > 0:
                symulowane_free_spiny -= 1
            else:
                calkowity_wklad += self.stawka
                spiny_do_wykonania -= 1
                
            bębny = [random.choices(self.symbols, weights=self.odds, k=3) for _ in range(5)]
            wyniki = [[bębny[kol][rzad] for kol in range(5)] for rzad in range(3)]
            
            
            wygrana_w_tym_spinie = 0 
            
            for nazwa_linii, koordynaty in self.linie_wygrywajace.items():
                symbole_na_linii = [wyniki[rzad][kolumna] for kolumna, rzad in koordynaty]
                najlepszy_mnoznik = 0
                najlepszy_symbol_linii = None 
                
                for start_idx in range(len(symbole_na_linii)):
                    symbol_bazy = None
                    trafienia = 0
                    
                    for i in range(start_idx, len(symbole_na_linii)):
                        obecny_symbol = symbole_na_linii[i]
                        if obecny_symbol == '🃏':  
                            trafienia += 1
                        elif symbol_bazy is None:
                            symbol_bazy = obecny_symbol
                            trafienia += 1
                        elif obecny_symbol == symbol_bazy:
                            trafienia += 1
                        else:
                            break
                            
                    if symbol_bazy is None:
                        symbol_bazy = '🃏'

                    mnoznik = self.tabela_wyplat.get(symbol_bazy, {}).get(trafienia, 0)
                    if trafienia == 2 and symbol_bazy in ['🍒', '🍋']:
                        mnoznik = 2

                    if mnoznik > najlepszy_mnoznik:
                        najlepszy_mnoznik = mnoznik
                        najlepszy_symbol_linii = symbol_bazy 
                        
                wygrana_z_linii = int(najlepszy_mnoznik * (1 + bonus_do_wygranej))
                
                
                if wygrana_z_linii > 0:
                    wygrana_w_tym_spinie += wygrana_z_linii
                    
                    wygrane_ze_symboli[najlepszy_symbol_linii] = wygrane_ze_symboli.get(najlepszy_symbol_linii, 0) + wygrana_z_linii

            
            calkowita_wygrana += wygrana_w_tym_spinie
            
            
            if wygrana_w_tym_spinie > najwieksza_pojedyncza_wygrana:
                najwieksza_pojedyncza_wygrana = wygrana_w_tym_spinie

            
            liczba_bomb = sum(rzad.count('💣') for rzad in wyniki)
            if liczba_bomb >= 3:
                nowe_spiny = {3: 10, 4: 25, 5: 50}.get(liczba_bomb, 50)
                symulowane_free_spiny += nowe_spiny
                
        
        
        print("\r" + " " * 50 + "\r", end="", flush=True) 
        
        czas_trwania = time.time() - start_time
        rtp = (calkowita_wygrana / calkowity_wklad * 100) if calkowity_wklad > 0 else 0
        
        print(f" Symulacja zakończona w {czas_trwania:.2f} s")
        print(f" Największa pojedyncza wygrana: {najwieksza_pojedyncza_wygrana} monet")
        print(f" RTP: {rtp:.2f}%")
        print("\n Wkład poszczególnych symboli w całkowitą wygraną:")
        
        
        posortowane_symbole = sorted(wygrane_ze_symboli.items(), key=lambda item: item[1], reverse=True)
        for symbol, suma_monet in posortowane_symbole:
            procent_wkladu = (suma_monet / calkowita_wygrana * 100) if calkowita_wygrana > 0 else 0
            print(f"   {symbol}: {suma_monet} monet ({procent_wkladu:.2f}%)")
        
        return rtp 

    def graj(self):
        while True:
            print("\033[F" * 10, end="")
            bonus = max(0, (self.stawka - 10) * 0.10)
            txt_bonus = f"(+{int(bonus*100)}% Wypłaty)" if bonus > 0 else ""
            
            print(f"\033[KSTATYSTYKI | Spiny: {self.spiny_lacznie} | Wygrane rundy: {self.wygrane_razy} | Łącznie wygrano: {self.wygrana_kasa_lacznie}¢")
            max_win = int(900 * (1 + bonus)*self.linie_wygrywajace.__len__())
            print(f"\033[KSTAWKA: {self.stawka} PLN {txt_bonus} | 🏆 MAX WYGRANA: {max_win}¢ | Saldo: {self.kasa}¢")
            print("\033[K") 
            
            
            for rzad in range(3):
                linia_text = " ".join([f"[ {self.wyniki[rzad][kolumna]} ]" for kolumna in range(5)])
                print(f"\033[K{linia_text}") 
                
            
            print("\033[K")
            
            
            print(f"\033[K{self.ostatnia_wiadomosc}")
            
            self.is_free_spin = self.free_spins > 0
            
            
            if self.is_free_spin:
                print(f"\033[KFREE SPINY: Pozostało {self.free_spins}")
            else:
                print("\033[K")
                
            
            print("\033[K")
            
            
            if self.is_free_spin:
                akcja = input(f"\033[K [ENTER] by wykorzystać Darmowy Spin: ")
            else:
                akcja = input(f"\033[K 'q' by wyjśc, '+' (zwiększ ), '-' (zmniejsz), [ENTER] by zakręcić (-{self.stawka}¢): ")
            
            
            print("\033[F\033[K", end="") 

            
            if not self.is_free_spin:
                if akcja == '+':
                    self.stawka += 1
                    self.save()
                    continue
                elif akcja == '-':
                    if self.stawka > 10:
                        self.stawka -= 1
                        self.save()
                    continue
                elif akcja == "q":
                    print("\033[F\033[K" * 10, end="")
                    print("\033[K Do zobaczenia! ")
                    break
                    
                if self.kasa < self.stawka:
                    self.ostatnia_wiadomosc = f" Brak środków! Saldo: {self.kasa}¢. Zmień w dane.json."
                    continue
                    
                self.kasa -= self.stawka
            else:
                self.free_spins -= 1
                
            self.spiny_lacznie += 1
            self.save()
            
            
            
            print("\033[F" * 7, end="") 
            
            self.stop_event = threading.Event()
            watek_animacji = threading.Thread(target=self.animuj)
            watek_animacji.daemon = True
            watek_animacji.start()
            
            
            time.sleep(2.5)
            self.stop_event.set()
            watek_animacji.join()
            
            
            print("\n" * 4, end="") 
            
            
            wygrana = self.sprawdz_wygrane()
            
            if wygrana > 0:
                self.kasa += wygrana
                self.wygrana_kasa_lacznie += wygrana
                self.wygrane_razy += 1
                self.save()
                self.ostatnia_wiadomosc = f" ŁĄCZNA WYGRANA Z TEGO SPINA: {wygrana}¢ 💰"
            else:
                self.ostatnia_wiadomosc = " Brak wygranej."

            if self.free_spins > 0:
                time.sleep(1.5) 

    def load(self):
        try:
            with open(self.dane, 'r') as file:
                data = json.load(file)
                self.data = data
                self.kasa = data.get("kasa", 1000)
                self.free_spins = data.get("free_spiny", 0)
                self.stawka = data.get("stawka", 10)
                if self.stawka < 10: 
                    self.stawka = 10
                self.spiny_lacznie = data.get("spiny", 0)
                self.wygrane_razy = data.get("wygrane_razy", 0)
                self.wygrana_kasa_lacznie = data.get("wygrana_kasa", 0)
        except FileNotFoundError:
            self.save()

    def save(self):
        with open(self.dane, 'w') as file:
            json.dump({
                "kasa": self.kasa,
                "free_spiny": self.free_spins,
                "stawka": self.stawka,
                "spiny": self.spiny_lacznie,
                "wygrane_razy": self.wygrane_razy,
                "wygrana_kasa": self.wygrana_kasa_lacznie
            }, file, indent=4)

    def przygotuj_wyniki(self, beben1, beben2, beben3, beben4, beben5):
        self.wyniki = []
        for i in range(3):
            temp = [beben1[i], beben2[i], beben3[i], beben4[i], beben5[i]]
            self.wyniki.append(temp)

    def animuj(self):
        beben = []
        for _ in range(5):
            beben.append(random.choices(self.symbols, weights=self.odds, k=3))
            
        zatrzymane = 0 
        
        while zatrzymane < 5:
            for i in range(5):

                if i >= zatrzymane:
                    nowy_symbol = random.choices(self.symbols, weights=self.odds, k=1)[0]

                    beben[i] = [nowy_symbol, beben[i][0], beben[i][1]]
            
            for i in range(3):
                print(f"\033[K[ {beben[0][i]} ] [ {beben[1][i]} ] [ {beben[2][i]} ] [ {beben[3][i]} ] [ {beben[4][i]} ]", flush=True)
            
            if self.stop_event.is_set():
                zatrzymane += 1
                
                time.sleep(0.4) 
            else:
                time.sleep(0.1) 
                
            if zatrzymane < 5:
                print("\033[F" * 3, end="")
                
        self.przygotuj_wyniki(beben[0], beben[1], beben[2], beben[3], beben[4])

    def sprawdz_wygrane(self):
        calkowita_wygrana = 0
        bonus_do_wygranej = max(0, (self.stawka - 10) * 0.10)
        
        for nazwa_linii, koordynaty in self.linie_wygrywajace.items():
            symbole_na_linii = [self.wyniki[rzad][kolumna] for kolumna, rzad in koordynaty]
            
            najlepszy_mnoznik = 0
            najlepszy_symbol = None
            najlepsze_trafienia = 0
            najlepszy_start = 0

            for start_idx in range(len(symbole_na_linii)):
                symbol_bazy = None
                trafienia = 0
                
                for i in range(start_idx, len(symbole_na_linii)):
                    obecny_symbol = symbole_na_linii[i]
                    if obecny_symbol == '🃏':  
                        trafienia += 1
                    elif symbol_bazy is None:
                        symbol_bazy = obecny_symbol 
                        trafienia += 1
                    elif obecny_symbol == symbol_bazy:
                        trafienia += 1
                    else:
                        break 
                
                if symbol_bazy is None:
                    symbol_bazy = '🃏'

                
                mnoznik_bazowy = self.tabela_wyplat.get(symbol_bazy, {}).get(trafienia, 0)
                if trafienia == 2 and symbol_bazy in ['🍒', '🍋']:
                    mnoznik_bazowy = 2
                    
                
                mnoznik_ostateczny = int(mnoznik_bazowy * (1 + bonus_do_wygranej))

                if mnoznik_ostateczny > najlepszy_mnoznik:
                    najlepszy_mnoznik = mnoznik_ostateczny
                    najlepszy_symbol = symbol_bazy
                    najlepsze_trafienia = trafienia
                    najlepszy_start = start_idx
            
            if najlepszy_mnoznik > 0:
                calkowita_wygrana += najlepszy_mnoznik
                trafione_koordynaty = koordynaty[najlepszy_start : najlepszy_start + najlepsze_trafienia]
                
                if najlepsze_trafienia >= 3:
                    wiadomosc = f"🎉 BINGO! {nazwa_linii}: Trafiłeś {najlepsze_trafienia}x {najlepszy_symbol}! (+{najlepszy_mnoznik}¢)"
                    self.rysuj_wygrana_siatke(trafione_koordynaty, self.colors['Green'], wiadomosc)
                else:
                    wiadomosc = f"🎉 {nazwa_linii}: Trafiłeś 2x {najlepszy_symbol}! (+{najlepszy_mnoznik}¢)"
                    self.rysuj_wygrana_siatke(trafione_koordynaty, self.colors['Yellow'], wiadomosc)
                
                time.sleep(1.2)

        liczba_bomb = sum(rzad.count('💣') for rzad in self.wyniki)
        if liczba_bomb >= 3:
            nowe_spiny = {3: 10, 4: 15, 5: 20}.get(liczba_bomb, 20)
            self.free_spins += nowe_spiny
            wiadomosc_scatter = f"💣 SCATTER! Trafiłeś {liczba_bomb}x 💣! Wygrywasz +{nowe_spiny} darmowych spinów!"
            
            koordynaty_bomb = [(k, r) for r in range(3) for k in range(5) if self.wyniki[r][k] == '💣']
            self.rysuj_wygrana_siatke(koordynaty_bomb, self.colors['Purple'], wiadomosc_scatter)
            time.sleep(2.5)
        
        return calkowita_wygrana

    def rysuj_wygrana_siatke(self, wygrywajace_koordynaty, kolor, wiadomosc):
        
        print("\033[F" * 7, end="") 
        
        for rzad in range(3):
            linia_text = ""
            for kolumna in range(5):
                symbol = self.wyniki[rzad][kolumna]
                if (kolumna, rzad) in wygrywajace_koordynaty:
                    linia_text += f"{kolor}[ {symbol} ]{self.colors['Reset']} "
                else:
                    linia_text += f"[ {symbol} ] "
            print(f"\033[K{linia_text}") 
            
        print("\033[K") 
        print(f"\033[K{wiadomosc}") 
        print("\033[K") 
        print("\033[K") 
        print("\033[K", end="") 

if __name__ == "__main__":
    gamba = Gamba('dane.json')