# Gamba

Slotsy w terminalu w twojej okolicy

![slotsy_speed_1 0x](https://github.com/user-attachments/assets/c7d7eb69-e5f7-4814-8805-c9ff7f058101)

## Wymagania

- `Python 3.6+`

## Instalacja i Uruchomienie

```bash
git clone https://github.com/dawidoczek/gamba.git
cd gamba
python main.py
```

## Cechy Gry

- **9 różnych symboli**: 🍒 🍋 🍉 🔔 🍀 💰 💎 🃏 💣
- **7 linii wygrywających**: od prostych (góra, środek, dół) po złożone (V, zygzaki)
- **Tabela wypłat**: Różne mnożniki dla różnych kombinacji symboli
- **Darmowe Spiny**: Wygrywaj dodatkowe spiny bez wkładu finansowego
- **Symulacja RTP**: Sprawdź teoretyczną zwrot gracza dla dużej liczby gier
- **Zapis Gry**: Twoje postępy są automatycznie zapisywane w `dane.json`

## Jak Grać

1. Ustaw stawkę (domyślnie: 10)
2. Naciśnij ENTER, aby uruchomić bębny
3. Czekaj na wynik gry
4. Zbieraj wygrane na aktywnych liniach
5. Korzystaj z darmowych spinów, aby zagrać bez wkładu

## Struktura Plików

```
gamba/
├── main.py        
├── dane.json      
└── README.md      
```

## Notatki Techniczne

- Payout table jest zdefiniowany dla każdego symbolu
- Każdy symbol ma własne szanse na pojawienie się
- Gra wykorzystuje wielowątkowość dla animacji
- Wszystkie dane gry są przechowywane w formacie JSON
