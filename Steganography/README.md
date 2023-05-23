1. Skrót  
Program służy do ukrywania wiadomości w plikach .zip stosując metodę steganografii.  

2.  
a) Opis działania - metoda I.  
Struktura pliku .zip przedstawia się tak jak zostało to zaprezentowane na obrazkach pomocniczych. W pierwszej kolejności w pliku zip znajdują się skompresowane pliki zaczynające się od nagłówków. Po sekcji plików jest katalog głowny zawierający informacje dotyczące całego pliku zip. 
Wiadomość (oznaczona jako Bolb) jest zapisywana (przez dopisany kod) po sekcji plików tuż przed nagłówkiem katalogu centralnego (głównego) który znajduje się na końcu pliku. Następnie w procesie zapisywania na dysk wczytanego do pamięci RAM pliku .zip aby skompensować przesunięcie nagłówka katalogu centralnego spowodowane dodaniem wiadomości aktualizowany jest wskaźnik (już przez samą bibliotekę), który wskazuje na początek katalogu centralnego. Wykorzystując wbudowaną fuckję katalog główny jest zapisywany po wiadmości.
Dzięki temu, że plik .zip określa w nagłówkach jaki jest rozmiar poszczególnych plików, wiadmość nie jest doklejana do ostatniego pliku ale znajduje się w "pustej przestrzeni" pomiędzy końcem ostatniego pliku, a początkiem katalogu centralnego.  
b) Opis działania - metoda II.
Wiadomość zostaje ukryta bezpośrednio w komentarzach w nagłówkach każdego pliku oraz w komentarzu w katalogu głównym. Jest ukrywana równomiernie - w każdym miejscu ukryte części mają podobną długość.

3. Użytkowanie  
W pakiecie zip_steganography znajdują się funkcje hide_msg oraz show_msg służace odpowiedni o do ukrywania i pokazywania ukrytej wiadmości. Za pomocą parametru method można wybrać czy wiadomość ukryjemy przed końcem katalogu centralnego czy w komentarzach.
Dodatkowo zaimplementowana została funkcjonalność ukrywania w pliku zip pliku .exe oraz uruchamiania ukrytego pliku .exe.
Służy do tego odpowienio funkcje hide_exe_in_zip i run_exe_from_zip. 
Moduł ukrywa tekst jawny poprzez zmianę kodowania na ibm039 - z tego powodu nie są dozwolone polskie znaki.
Jak pokzały testy niektóre antywirusy uznają plik z wiadomością schowaną przed katalogiem głównym jako niebezpieczny. Żaden antywirus nie uznał za niebezpieczny plik z wiadomością, a newet plikiem .exe schowanym w komentarzach. 

4. Obrazki pomocnicze  
Wizualizacja miejsca ukrycia wiadomości  

![alt text](https://github.com/gromnitsky/zipography/blob/master/doc/zip.svg)

Obrazowa struktura pliku .zip  

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/ZIP-64_Internal_Layout.svg/1920px-ZIP-64_Internal_Layout.svg.png)

5. Wyjaśnienia dotyczące kodu są zamieszczone w załączonej prezentacji.

<!-- 5. Działanie w kodzie - metoda I  
ZAPIS - UKRYWANIE WIADOMOŚCI
Zmodyfikujemy funkcję close oraz konstruktor klasy ZipFile z biblioteki zipfile
```python
from zipfile import ZipFile
```
Przed modyfikacją funkcja wygląda następująco:
 Tworzymy nową klasę która dziedziczy po ZipFile:
 ```python
 class MyZipFileHide(ZipFile):
    def __init__(self, message_to_hide, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message = message_to_hide
 ```
Funcka close przed zmianą wygląda następująco:
 ```python
  def close(self):
      """Close the file, and for mode 'w', 'x' and 'a' write the ending
      records."""
      if self.fp is None:
          return

      if self._writing:
          raise ValueError("Can't close the ZIP file while there is "
                           "an open writing handle on it. "
                           "Close the writing handle before closing the zip.")

      try:
          if self.mode in (
          'w', 'x', 'a') and self._didModify:  # write ending records
              with self._lock:
                  if self._seekable:
                      self.fp.seek(self.start_dir)
                  self._write_end_record()
      finally:
          fp = self.fp
          self.fp = None
          self._fpclose(fp)
  ```
Zmodyfikumemy następującą część:
```python
try:
    if self.mode in (
    'w', 'x', 'a') and self._didModify:  # write ending records
        with self._lock:
            if self._seekable:
                self.fp.seek(self.start_dir)
            self._write_end_record()
```
Zastąpimy ją następującym kodem:
```python
 try:
      with self._lock:
          self.fp.seek(self.start_dir)
          if self._message[0] == "/":
              raise RuntimeError('"/" is illegal at the beggining of message')
          self.fp.write(bytes("X", encoding='utf-8'))
          self.fp.write(self._message)
          shift = len(self._message)
          self.fp.seek(self.start_dir+shift)
          self.start_dir += shift + 1
          self.fp.seek(self.start_dir)
          self._write_end_record()
```
Przeanalizujmy ten fragment...
```python
self.fp.seek(self.start_dir)
```
Ta funkcja znajduje miejsce w którym znajduje się obecnie początek katalogu głównego i ustawia tam wskaźnik. Atrybut ten jest przypisywany podczas odczytu pliku.
Aby zaznaczyć miejsce w którym kończy (a właściwie zazczyna) się nasza wiadomość na jej początku zostaje zapisany znacznik "X". Jeżeli chcemy wpisać znak X w wiadomości musimy go poprzedzić znakiem "/" - od tego znaku nie może zaczynać się wiadomość. Aby sprawdzić czy wiadommość jest poprawna używamy kodu:
```python
if self._message[0] == "/":
    raise RuntimeError('"/" is illegal at the beggining of message')
```
Jeżeli wiadomość jest poprawna wpisujemy ją (w postaci bajtów) po ostatnim pliku, a przed katalogiem głównym:
```python
self.fp.write(bytes("X", encoding='utf-8'))
self.fp.write(self._message)
```
Aby wszystko się zgadzało należy uaktualnić początek katalogu głównego. Do jego poprzedniego początku dodajemy długość wiadomości + 1 (nasz X):
```python
shift = len(self._message)
self.fp.seek(self.start_dir+shift)
self.start_dir += shift + 1
```
Następnie uaktualniamy wskaźnik - od tego miejsca plik będzie dalej zapisywany:
```python
self.fp.seek(self.start_dir)
```
I na końcu wywołujemy funkcję która zapisuje katalog główny:
```python
self._write_end_record()
```
Funkcja do zakodowania wiadmości wykorzystująca stworzoną klasę wygląda następująco:
```python
def hide_txt(msg, filename):
    msg = bytes(msg, encoding='utf-8')
    with MyZipFileHide(msg, filename, 'a') as _:
        pass
```

ODCZYT - ODKRYWANIE WIADOMOŚCI
Aby odcczytać wiadomość z pliku .zip należy zmodyfikować konstruktor klasy ZipFile.
Ponownie zrobimy to poprzez dziedziczenie:
 ```python
 class MyZipFileUnHide(ZipFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = ""
        with self._lock:
            self.fp.seek(self.start_dir)
            message = b''
            end_byte = b'X'
            last = b''
            while True:
                pos = self.fp.tell()
                letter = self.fp.read(1)
                self.fp.seek(pos-1)
                if letter != end_byte:
                    message += letter
                    last = letter
                else:
                    if last == b"/":
                        message += letter
                        continue
                    else:
                        break
            self.msg = message.decode('utf-8')[:0:-1]
```
W nowym konstruktorze wywołujemy poprzedni tak aby wszystko się poprawnie zainicjalizowało.
Następnie przystępujemy do odczytania wiadomości:
Inicjalizujemy potrzebne zmienne oraz ustawiamy wskaźnik odczytu w miejcu gdzie rozpoczyna się katalog główny:
```python
self.fp.seek(self.start_dir)
message = b''
end_byte = b'X'
last = b''
```        
Następnie w pętli do puki nie znajdziemy znacznika "X" po którym (bo czytamy wiadomość od końca) nie następuje "/" dodajemy kolejne bajty do wiadmości.
```python
 while True:
      pos = self.fp.tell()
      letter = self.fp.read(1)
      self.fp.seek(pos-1)
      if letter != end_byte:
          message += letter
          last = letter
      else:
          if last == b"/":
              message += letter
              continue
          else:
              break
```                  
Kiedy już natrafimy na niego natrafimy konwertujemybajty na string, usówamy "X" i odwracamy wiadomość.
```python
self.msg = message.decode('utf-8')[:0:-1]      
```

Funkcja do odczytania wiadmości wykorzystująca stworzoną klasę wygląda następująco:
```python
def unhide_msg(filename):
    with MyZipFileUnHide(filename, 'r') as file:
        msg = file.msg
    return msg
``` -->
