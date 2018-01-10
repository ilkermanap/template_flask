<div class="maketitle">

Flask Taslak Kullanımı {#flask-taslak-kullanımı .titleHead}
----------------------

<div class="author">

<span class="cmr-12">Ilker Manap</span>

</div>

\
<div class="date">

<span class="cmr-12">10</span><span class="cmr-12"> Ocak 2018</span>

</div>

</div>

[](){#x1-1000}İçindekiler {#içindekiler .likechapterHead}
-------------------------

<div class="tableofcontents">

<span class="chapterToc">1 [Giriş](#x1-20001){#QQ2-1-2}</span>\
<span class="chapterToc">2 [Sanal Domain Nasıl
Ayarlanır?](#x1-30002){#QQ2-1-3}</span>\
 <span class="sectionToc">2.1 [DNS](#x1-40002.1){#QQ2-1-4}</span>\
 <span class="sectionToc">2.2 [Nginx
Ayarları](#x1-50002.2){#QQ2-1-5}</span>\
<span class="chapterToc">3 [Flask Kurulumu](#x1-60003){#QQ2-1-6}</span>\
<span class="chapterToc">4 [Flask Uygulamanın Sunucuya
Kurulması](#x1-70004){#QQ2-1-7}</span>

</div>

<span class="titlemark">Bölüm 1</span>\
[](){#x1-20001}Giriş {#bölüm1-giriş .chapterHead}
---------------------------------------

Flask ile yazılmış uygulamaların bir web sunucu üzerinden sunulması çoğu
kişi için başa çıkılamaz karmaşık işlemler gerektiren bir süreç gibidir.
Birden fazla konuda doğru ayarlamalar yapmak gerektiği için, konuyu az
bilenler tarafından yapılmaya çalışıldığında sorun çıkması ihtimali de
yüksektir.

Bu belge ile, karmaşık görünen işlemlerin daha kolay yapılabilmesini
sağla-maya çalışacağız. Düzgün ayarlanması gereken birden fazla nokta
olduğundan, ayar gerektiren her bir bölüm için olabildiğince detaylı
anlatılacaktır.

<span class="titlemark">Bölüm 2</span>\
[](){#x1-30002}Sanal Domain Nasıl Ayarlanır? {#bölüm2-sanal-domain-nasıl-ayarlanır .chapterHead}
--------------------------------------------

DNS[](){#dx1-3001} ve nginx[](){#dx1-3002} ayarları

### <span class="titlemark">2.1 </span> [](){#x1-40002.1}DNS {#dns .sectionHead}

Bir web sunucusunun bir domain adına bağlı olarak çalışabilmesi için
önce domain alınan yerde ayarlar gerekir. Çoğunlukla dns servisi domain
alınan yer üzerinden kullanılır. Yani domain satın aldığınız ﬁrma,
aldığınız domaini yönetmek için size bir arayüz sağlar. Örnek olarak,
godaddy ﬁrmasından deneme.com adresini aldığımızı düşünelim. Godaddy.com
adresindeki bir yönetim paneli ile deneme.com için www.deneme.com,
mail.deneme.com gibi yeni adresler ekleyebiliriz. Burada yazdığımız
uygulamanın hello.deneme.com adresinden sunulacağını varsayalım.

Öncelikle, hello.deneme.com adı için DNS panelinde A kaydı
oluşturmalıyız. A kaydı ile, verdiğimiz adın sahip olacağı IP adresini
tanımlamış oluruz. hello.de-neme.com için 56.35.3.122 gibi. Buradaki
isim ve IP adresleri tamamen uydurmadır.

Bir sanal sunucu aldığınızda, sanal sunucunuzun IP adresini bu amaçla
kullanabilirsiniz. Bir sanal sunucuda çok sayıda farklı domain için web
siteleri barındırmak mümkündür. Yani, hello.deneme.com için
kullandığınız sunucuyu, www.baskabirdomain.com için de sorun olmadan
kullanabilirsiniz. İki web sitesinin birbirine karışmadan sunulması
işini ise nginx ve apache gibi sunucular üstlenirler. Detayı nginx
sunucusu için aşağıda anlatılacaktır.

DNS ile ilgili işlem tamamlandığında (web adresi için A kaydı
tanımlaması), internete bağlı herhangi bir yerden, hello.deneme.com
adresinini isim çözümlemesi yapılabiliyor olmalıdır.

Dns detayları

### <span class="titlemark">2.2 </span> [](){#x1-50002.2}Nginx Ayarları {#nginx-ayarları .sectionHead}

Nginx

<span class="titlemark">Bölüm 3</span>\
[](){#x1-60003}Flask Kurulumu {#bölüm3-flask-kurulumu .chapterHead}
---------------------------------------

<span class="titlemark">Bölüm 4</span>\
[](){#x1-70004}Flask Uygulamanın Sunucuya Kurulması {#bölüm4-flask-uygulamanın-sunucuya-kurulması .chapterHead}
---------------------------------------------------

[](){#x1-80004}Dizin {#dizin .likechapterHead}
--------------------

<div class="theindex">

<span class="index-item">DNS, 7\
</span>
<span class="index-item">nginx, 7\
</span>

</div>
