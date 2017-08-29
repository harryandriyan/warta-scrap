# warta-scrap
Indonesia Index News Crawler, including 10 online

### Online Media List:
- Detik.com
  http://news.detik.com/indeks
- Republika.co.id
  http://www.republika.co.id/indeks
- Viva.co.id
  http://www.viva.co.id/indeks
- Kompas.com 
  http://indeks.kompas.com/
- Antaranews.com
  http://www.antaranews.com/terkini
- Tempo.co
  https://www.tempo.co/indeks
- Okezone.com
  http://index.okezone.com/
- Liputan6.com
  http://www.liputan6.com/indeks
- Kumparan.com
  https://kumparan.com/
- Tirto.id
  https://tirto.id/indeks

### Installation :
Open Terminal, and clone this repo:  
> git clone https://github.com/harryandriyan/warta-scrap

Go to project folder
> cd warta-scrap

Setup virtualenv
> virtualenv venv

Activate virtualenv
> . venv/bin/activate

Install requirements
> pip install -r requirements.txt

### How to use
Open the specific project, example
> cd republika

Run crawl command, example
> scrapy crawl republika -o sampleResult.json -t json