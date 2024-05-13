
Nasz program "Cordinate Transformer" to program, który stworzyliśmy na potrzeby transformowania współrzędnych między różnymi systemami odniesienia.
Został napisany w języku Python i obsługuje takie przekształcenia jak:

- XYZ(geocentryczne) ---> BLH(geodezyjne)
- BLH(geocentryczne) ---> XYZ(geocentryczne)
- XYZ ---> NEU(topocentryczne)
- BL(GRS80, WGS84, Krasowski) ---> XY w układzie 2000
- BL(GRS80, WGS84, Krasowski) ---> XY w układzie 1992

#Wymagania 
- Python w wersji 3.6 lub nowszej
- Microsoft Windows 10 lub nowszy
- Biblioteki w Pythonie: 'argparse', 'csv', 'math', 'numpy'
- Program korzysta z biblioteki 'sys' do przetwarzania argumentów przekazywanych z linii poleceń, która jest częścią standardowej biblioteki Pythona i nie wymaga osobnej instalacji

  Jeżeli użytkownik nie posiada zainstalowanych wszystkich wyżej wymienionych bibliotek, program nie zadziała.
  Oto przykład jak zainstalować bibliotekę 'numpy':

  '''bash <br>
  pip install numpy
  
#Obsługiwane elipsoidy w naszym programie:

-GRS80 <br>
-WGS84 <br>
-Krasowski <br>

#Uruchomienie programu 

Program można uruchomić z wiersza poleceń postepując zgodnie z poniższymi krokami:

1. '--input': Plik CSV ze współrzędnymi wejściowymi
2. '--output': Plik CSV do zapisania wyników
3. '--transormacja': Typ transformacji
4. '--elipsoida': Typ elipsoidy
 
WAŻNE----Kod został napisany dla plików w formacie CSV na potrzeby  jego uniwersalności, jednakże, jeżeli użytkownik posiada plik txt to program również zadziała.
Należy wtedy uprzednio przygotować plik, co będzie opisane w dalszej częsci----WAŻNE

 Przykłady dla każdego wariantu transformacji:
 Plik wejściowy: wsp_inp.txt (XYZ)

1.XYZ_do_BLH

python skrypt1.py --input wsp_inp.txt --output wyniki.txt --transformacja XYZ_do_BLH --elipsoida GRS80

Plik wejściowy wsp_inp.txt zawiera dane w formacie XYZ, natomiast plik wyjściowy wyniki.txt zawiera przekształcone współrzędne BLH.

2.BLH_do_XYZ

python skrypt1.py --input wsp_inp.txt --output wyniki.txt --transformacja BLH_do_XYZ --elipsoida GRS80

Plik wejściowy wsp_inp.txt zawiera dane w formacie BLH, natomiast plik wyjściowy wyniki.txt zawiera przekształcone współrzędne XYZ.

3.XYZ_do_NEU

python skrypt1.py --input wsp_inp.txt --output wyniki.txt --transformacja XYZ_do_NEU --elipsoida GRS80

Plik wejściowy wsp_inp.txt zawiera dane w formacie XYZ, natomiast plik wyjściowy wyniki.txt zawiera przekształcone współrzędne NEU.

4.BL_do_2000

python skrypt1.py --input wsp_inp.txt --output wyniki.txt --transformacja BL_do_2000 --elipsoida Krasowski

Plik wejściowy wsp_inp.txt zawiera dane w formacie BL, natomiast plik wyjściowy wyniki.txt zawiera przekształcone współrzędne XY w układzie 2000.

5.BL_do_1992

python skrypt1.py --input wsp_inp.txt --output wyniki.txt --transformacja BL_do_1992 --elipsoida Krasowski

Plik wejściowy wsp_inp.txt zawiera dane w formacie BL, natomiast plik wyjściowy wyniki.txt zawiera przekształcone współrzędne XY w układzie 1992.

#Struktura plików wejściowych

Dane w pliku wejściowym powinny być danymi numerycznymi, oddzielonymi przecinkami.
Plik nie powinien zawierać żadnych nagłówków czy opisów kolumn. 
Plik powinien być w formacie CSV bądż TXT.
Plik w zależności od żądanej transformacji pownien posiadać następującą strukturę:

- XYZ(geocentryczne) ---> BLH(geodezyjne): Plik zawiera trzy kolumny 'X','Y','Z'
- BLH(geocentryczne) ---> XYZ(geocentryczne): Plik zawiera trzy kolumny 'B','L','H' ('lat','lon','H')
- XYZ ---> NEU(topocentryczne):  Plik zawiera trzy kolumny 'X','Y','Z'
- BL(GRS80, WGS84, Krasowski) ---> XY w układzie 2000: Plik zawiera dwie kolumny 'B','L' ('lat','lon')
- BL(GRS80, WGS84, Krasowski) ---> XY w układzie 1992: Plik zawiera dwie kolumny 'B','L' ('lat','lon')

#Struktura plików wyjściowych

Pliki wyjściowe otrzymają nazwę podaną przez użytkownika przy uruchomieniu programu. 
Plik wyjściowy będzie zawierał kolumny z przekształconymi danymi w zależności od transformacji.

#Znane błędy i nietypowe zachowania programu 

W przypadku błędu konstrukcyjnego "literówki", podania nieobsługiwanej elipsoidy, bądź wykraczających współrzednych program wyświetli błąd i zakończy pracę.
Nie znaleziono więcej błędów, bądź nietypowego zachowania programu podczas transformacji. 
Program był testowany i transformacje zgadzają się, dając poprawne wyniki. 

#Autorzy <br>
Mateusz Bownik, Maciej Frączek 

 
 

 
  

  
