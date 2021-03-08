# Fill the Pokedex : how to perform a simple web scrapping on a dynamic website and do some Dataviz
### Python | Pandas, Selenium, BeautifulSoup, Matplotlib, Seaborn, Altair
#### **Authors : Gaëtan LE FLOCH, Lucas PRUTKI, Alexis VIGNARD**

##### Description

This project aims to complete a so-called "Pokedex" using available data on Bulbapedia. We begin with a small database containing names, HPs, types ect. and we add informations such as height, weight, catch rate and hatch steps.

<p align='center'><img src="https://github.com/GaetanLF/Fill-the-Pokedex/blob/main/Bulbasaur.png" alt="Bulbasaur's infos" /></p>

<p align="center"><i>Here are some informations available on Bulbapedia for Bulbasaur</i></p>

Nonetheless, our Pokedex still stays light as we could have taken much more data about gender ratio, evolution levels, natural moves' levels ect.. We've decided not to take it as this shouldn't be relevant for our original task (which was to make some dataviz about pokemons within the framework of our Python assignment at Paris 1 Pantheon-Sorbonne University).

You can use either the raw program (FtP.py) or the Notebook (FtP.ipynb). The last one explains step by step the methodology and should be usefull for beginners as you can not directly run this program : you might want to make some adjustments regarding pathfiles if needed.

##### Requirements

Since pokedex.org is a dynamic website, you will need to install the selenium package (which should be already available if you have Anaconda). You should also need an appropriate driver for your web browser which are all available on https://www.selenium.dev/downloads/ if you are using a regular browser. Mozilla Firefox users could take a look at the Github repository for GeckoDriver : https://github.com/mozilla/geckodriver/releases and Chrome users should dwell on ChromeDriver : https://chromedriver.chromium.org/downloads . 

##### Inquiries

For any inquiry about the Notebook, please contact me at : gaetan.le-floch@etu.univ-paris1.fr
