## Satelitske komunikacije in navigacija 2019/2020
### Program za obdelavo satelitskih slik NOAA satelitov

#### Inštalacija
Za zagon programa potrebujemo inštaliran programski jezik [Python3](https://www.python.org/) (lahko tudi različica [Anaconda](https://www.anaconda.com/distribution/#download-section)).
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
1. V zavihku `File` izberemo `Load` (bližnjica ctrl+O) in izberemo sliko, ki jo želimo odpreti (nekaj slik je na voljo v mapi `images/`).
2. Naložena slika se razdeli na dva dela: Image A (bližnja IR slika) in Image B (daljna IR slika). Obe sliki sta 8-bitni sivinske slike.
3. Z uporabo gumba `Select active image` izberemo sliko, ki jo želimo urejati. Na voljo so različne funkcije kot so razni filtri, popravki kontrasta, iskanje robov, obarvanje...
4. Obdelano sliko lahko shranimo (zavihek `File` in izberemo eno izmed možnosti)

#### Primer uporabe
