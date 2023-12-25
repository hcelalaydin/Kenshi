<h1 align="center">Kenshi</h1>

> Kurulumu kolay - ne kadar süreceğini bilmiyorum belli değil - donanım için yeni sunucuya gerek yok

> Ödüllü evet - ama top 200'e - herkes kurabilir ama en iyi performansı veren 200 node ödül alabilir.

> TOPLULUK KANALLARI: [Sohbet Kanalımız](https://t.me/RuesChat) - [Duyurular ve Gelişmeler](https://t.me/RuesAnnouncement) - [Whatsapp](https://whatsapp.com/channel/0029VaBcj7V1dAw1H2KhMk34) - [Kenshi Telegram](https://t.me/KenshiTech)

#

<h1 align="center">Donanım</h1>

> Bir cihaz temin etmedim mevcut nodeların yanına kurdum - ario, santiment, voi yanlarında denedim problem olmadı.

> top 200'de olmak için en önemli kriter internet olacak, [Hetzner](https://hetzner.cloud/?ref=gIFAhUnYYjD3) kullandım.

> illa temin edilecekse 2 CPU 2 RAM ideal 'şimdilik'

#

<h1 align="center">Kurulum</h1>

```console
# sunucu güncelleme
sudo apt update -y && sudo apt upgrade -y

# apt'nin HTTPS üzerinden paket kullanmasına izin veren birkaç önkoşul paketini yükleyin
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Resmi Docker deposu için GPG anahtarını sisteminize ekleyin
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# APT kaynaklarına Docker deposunu ekleyin
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Yeni eklenen depodan Docker paketleriyle paket veritabanını güncelleyin
sudo apt update

# Docker'ı yükleyin
sudo apt install docker-ce

# Docker'ın doğru bir şekilde yüklendiğini doğrulamak için Docker hello-world imajını çalıştırın
sudo docker run hello-world

```

<h1 align="center">Yapılandırma işlemleri ve başlatma</h1>

```console

# KenshiTech Docker dosyasını indirin
wget https://github.com/KenshiTech/unchained/releases/download/v0.8.10/unchained-v0.8.10-docker.zip

# İndirilen ZIP dosyasını açın
unzip unchained-v0.8.10-docker.zip

#klasöre girelim
cd unchained-v0.8.10-docker

#Node başlatmadan önce config dosyamızı kopyalayalım ve değiştirilerim
cp conf.lite.yaml.template conf.lite.yaml

#name: den sonra mevcut yazıyı silin ve kendi koymak istediğiniz ismi küçüktür işaretleri olmadan yazın
#örnek, name: hcelalaydin
nano conf.lite.yaml

#Node başlatma
./unchained.sh lite up -d

#Burada yazan secret ve public anahtarları bir yere kaydedelim !!!
cat conf.lite.yaml


#Logları görüp çalıştığına emin olalım, yeşil yazılar akacak
./unchained.sh lite logs -f

> CTRL C ile loglardan çıkabiliriz.

# Notlar:
> Son komuttan sonra loglar akmaya başlayacak ve sync olmaya başlayacaksınız
> node durdurma, "./unchained.sh lite stop"
 


```



> Kendinizi [burada](hyyps://kenshi.io/unchained) veya [burada](https://charts.mongodb.com/charts-unchained-gpust/public/dashboards/cbb6ccf6-15b2-4187-be56-ff9d2e25a48a) contributions kısmında bulabilirsiniz.

