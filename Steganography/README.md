1. Skrót  
Program służy do ukrywania wiadomości w plikach .zip stosując metodę steganografii.  
2. Opis działania  
Wiadomość (oznaczona jako Bolb) jest ukrywana (przez dopisany kod) po sekcji plików tuż przed nagłówkiem pierwszego katalogu centralnego.  
Następnie aktualizowany jest wskaźnik (już przez samą bibliotekę) który wskazuje na początek katalogu centralnego, a który znajduje się na jego końcu, aby skompensować przesunięcie nagłówka katalogu centralnego spowodowane dodaniem wiadomości.  
Dzięki temu, że plik .zip określa w nagłówkach jaki jest rozmiar poszczególnych plików wiadmość nie jest doklejana do ostatniego pliku ale znajduje się w "pustej przestrzeni" pomiędzy końcem ostatniego pliku, a początkiem katalogu centralnego.  
3. Użytkowanie  
Plik hide.py służy do ukrycia wiadomości. Należy podać ścieżkę lub nazwę pliku oraz wiadomość.
Plik unhide służy do odczytania wiadmości z pliku w którym została ona ukryta. Należy podać ścieżkę do pliku.
Na ten moment nie działają polskie znaki.  
4. Obrazki pomocnicze  
Wizualizacja miejsca ukrycia wiadomości  

![alt text](https://github.com/gromnitsky/zipography/blob/master/doc/zip.svg)

Obrazowa struktura pliku .zip  

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/ZIP-64_Internal_Layout.svg/1920px-ZIP-64_Internal_Layout.svg.png)
