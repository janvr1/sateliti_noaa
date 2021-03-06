## Satelitske komunikacije in navigacija 2019/2020
### Program za obdelavo satelitskih slik NOAA satelitov

#### Inštalacija
Za zagon programa potrebujemo inštaliran programski jezik [Python](https://www.python.org/) (lahko tudi različica [Anaconda](https://www.anaconda.com/distribution/#download-section)).
1. Kloniramo ta repozitorij: `git clone https://github.com/janvr1/sateliti_noaa.git` ali prenesemo zip datoteko.
2. Odpremo ukazno vrstico v mapi repozitorija in ustvarimo virtualno okolje
    * Python: `python -m venv venv_noaa`
    * Anaconda: `conda create venv_noaa`
3. Aktiviramo virtualno okolje:
    * Python: `.\venv_noaa\Scripts\activate` oz. `source ./venv_noaa/bin/activate`(Linux)
    * Anaconda: `conda activate venv_noaa`
4. Inštaliramo potrebno knjižnice:
    * Python: `pip install -r req.txt`
    * Anaconda: `conda install numpy matplotlib pillow scikit-image` in `conda install -c conda-forge pyside2`
5. Program zaženemo z: `python main.py`

#### Uporaba programa
Program omogoča obdelavo slik sprejetih po APT protokolu. Trenutno takšne slike oddajajo sateliti NOAA 15, NOAA 18 in NOAA 19 na frekvenci cca. 137 Mhz.
1. Za uporabo programa potrebujemo dekodirano sliko. Za dekodiranje zvočnega posnetka APT signala se lahko uporabi program kot je naprimer [noaa-apt](https://noaa-apt.mbernardi.com.ar) ali [aptdec](https://github.com/dankolbrs/aptdec).

2. V zavihku `File` izberemo `Load` (bližnjica ctrl+O) in izberemo sliko, ki jo želimo odpreti (nekaj slik je na voljo v mapi `images/`).
3. Naložena slika se razdeli na dva dela: Image A (bližnja IR slika) in Image B (daljna IR slika). Obe sliki sta 8-bitni sivinske slike.
4. Z uporabo gumba `Select active image` izberemo sliko, ki jo želimo urejati. Na voljo so različne funkcije kot so razni filtri, popravki kontrasta, iskanje robov, obarvanje...
5. Obdelano sliko lahko shranimo (zavihek `File` in izberemo eno izmed možnosti)

#### Primer uporabe
1. Odpremo sliko `images/italy.png`. V levem delu uporabniškega vmesnika se odpre surova slika, desno spodaj pa lahko vidimo histogram trenutno aktivne slike.
![](screenshots/raw_image.png)

2. Na sliki uporabimo željene izboljšave. V tem primeru so bili uporabljeni `Equalize histogram`, `Median filter`, `Gamma correction` in `Flip image`.
![](screenshots/processed_image.png)

3. Po žeji lahko sliko tudi obarvamo  z gumbom `Colorize`. Rezultirajoče barve niso realne barve terena, saj podatka o tem nimamo (na voljo imamo samo IR slike) temveč so t.i. "lažne barve" in služijo le za vizualno olepšavo in boljšo razpoznavnost slike.
![](screenshots/colorized_image.png)
