# Wdrożenie nowej strony petpatrol.pl

Całość składa się z trzech części: grafik w bibliotece mediów, trzech pól we wtyczce WPCode (wspólny wygląd, header, stopka) oraz jednego bloku HTML na każdej z 8 stron. Motywu Customify nie trzeba zmieniać ani wyłączać: nowy CSS sam chowa stary nagłówek, stopkę i panel boczny.

Podgląd wszystkich stron jest w folderze `podglad/`. Otwórz dowolny plik w przeglądarce, linki między stronami działają.

## 1. Grafiki (ręcznie, raz)

1. Wejdź w **Media → Dodaj nowy plik**.
2. Przeciągnij wszystkie 9 plików z folderu `media/` (wszystkie zaczynają się od `ppw-`).
3. Zrób to w **listopadzie 2026**. WordPress zapisze je wtedy w `/wp-content/uploads/2026/11/`, a kod odwołuje się dokładnie do tej ścieżki.

Jeśli wgrasz je w innym miesiącu, wystarczy przebudować kod z innym folderem, na przykład `python3 build.py /wp-content/uploads/2026/12/`. Nie zmieniaj nazw plików. Jeśli WordPress doda do nazwy końcówkę `-1`, oznacza to, że plik o tej nazwie już istnieje: usuń duplikat i wgraj ponownie.

## 2. Wtyczka WPCode (raz)

1. **Wtyczki → Dodaj nową**, wyszukaj „WPCode”, zainstaluj i włącz **WPCode Lite**.
2. Wejdź w **Code Snippets → Header & Footer**.
3. Do pola **Header** wklej całą zawartość pliku `wordpress/1-wpcode-header.html` (fonty i wygląd całej strony).
4. Do pola **Body** wklej całą zawartość pliku `wordpress/2-wpcode-body.html` (nowy nagłówek z menu i ikonami social).
5. Do pola **Footer** wklej całą zawartość pliku `wordpress/3-wpcode-footer.html` (nowa stopka i skrypt przycisków „Kopiuj” oraz menu mobilnego).
6. Kliknij **Save Changes**.

Nagłówek i stopka pojawią się od razu na wszystkich stronach i we wszystkich starych wpisach.

## 3. Strony (wklejasz HTML)

Najpierw przetestuj na stronie **Jak Pomóc V2** (`/jak-pomoc-v2/`): wklej tam `pomagam.html`. Gdy wszystko wygląda dobrze, przejdź do prawdziwych stron.

Dla każdej strony:

1. Otwórz stronę do edycji.
2. Przełącz się na **Edytor kodu**: menu z trzema kropkami w prawym górnym rogu → „Edytor kodu” (albo skrót Ctrl+Shift+Alt+M, na Macu Cmd+Shift+Option+M).
3. Kliknij w pole z treścią, zaznacz wszystko (Ctrl+A / Cmd+A) i usuń.
4. Otwórz plik z tabeli w edytorze tekstu, zaznacz **cały** plik i wklej.
5. Sprawdź, czy ostatnia linia w polu to `<!-- /wp:html -->`. Jeśli jej nie ma, wklejenie się ucięło: powtórz krok 4.
6. Wyjdź z edytora kodu i kliknij **Aktualizuj**.

| Strona w WordPressie | Plik |
|---|---|
| Strona Startowa | `wordpress/strony/strona-glowna.html` |
| O Nas | `wordpress/strony/o-nas.html` |
| Jak Pomóc | `wordpress/strony/pomagam.html` |
| Zostań wolontariuszem! | `wordpress/strony/zostan-wolontariuszem.html` |
| Warunki adopcji | `wordpress/strony/warunki-adopcji.html` |
| Kontakt | `wordpress/strony/kontakt.html` |
| Dokumenty i Sprawozdania Roczne | `wordpress/strony/dokumenty.html` |
| Polityka prywatności | `wordpress/strony/polityka-prywatnosci.html` |

Wklejaj tylko w Edytorze kodu. Wklejony do zwykłego bloku „Własny HTML” plik zagnieździłby blok w bloku.

## 4. Po wklejeniu (ręcznie, raz)

1. **LiteSpeed Cache → Panel → Purge All**. Bez tego goście mogą jeszcze przez jakiś czas widzieć starą wersję.
2. Otwórz stronę w trybie incognito na telefonie i na komputerze.
3. Jeśli menu mobilne albo przyciski „Kopiuj” nie reagują, wejdź w **LiteSpeed Cache → Ustawienia → Optymalizacja strony → JS** i wyłącz „Load JS Deferred” / „Delay JS”, albo dodaj `ppw` do wyjątków.
4. Stronę testową **Jak Pomóc V2** po testach przenieś do kosza.

## Co później edytujesz ręcznie

- **Pozycje w menu** są wpisane w pliku `2-wpcode-body.html`. Menu z **Wygląd → Menu** nie jest już używane. Zmianę pozycji menu robi się w tym pliku, a potem wkleja go ponownie w pole Body.
- **Dane do wpłat, adres, maile** są wpisane w stronach i w stopce. Przy zmianie numeru konta trzeba poprawić `pomagam`, `kontakt` i stopkę (`3-wpcode-footer.html`).
- **Zdjęcia w nagłówkach stron** pokazują zwierzaki bez imion, więc nie dezaktualizują się, gdy podopieczni znajdą dom.
- **Nowe dokumenty i sprawozdania**: wgraj PDF do mediów, skopiuj jego adres i dopisz nowy blok roku w `dokumenty.html`, wzorując się na istniejących.
- **Tytuły i opisy dla Google** ustawiasz jak dotąd w polu Yoast SEO pod każdą stroną. Kod ich nie zmienia.
- **Baner cookies** to nadal wtyczka Cookie Notice. Kod zmienia tylko jej kolory.

## Do sprawdzenia przez fundację (treści przeniesione bez zmian)

- **Polityka prywatności** podaje stary adres: „ul. Za Torem 11, 44-203 Rybnik”. Reszta strony używa adresu „ul. św. Józefa 33A/B, 44-217 Rybnik”. Polityka wspomina też Google Analytics i Twitter, a na stronie nie ma ani jednego, ani drugiego.
- **Warunki adopcji**: stara strona miała pod spodem zepsuty pokaz zdjęć (`[metaslider id=935]`, wtyczka nie jest aktywna). Pominąłem go.
- **Warsztaty** (strona, regulamin, standardy małoletnich, mail kreatywnypetpatrol) usunięte z nowego kodu. W WordPressie przenieś te strony do kosza / odpublikuj.
- **Zostań wolontariuszem**: link „Więcej o bazarku TUTAJ” prowadził do obrazka PNG. Teraz prowadzi do sekcji Bazarek na stronie „Jak pomóc”.
- **Stopka** zawiera numer zbiórki publicznej `2019/2190/OR` i drugie konto Instagram `pet.patrol.adopcje` (oba z materiałów kalendarza). Usuń je, jeśli są nieaktualne.
