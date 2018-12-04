# Flask, Uwsgi, Nginx, systemd Kurulum Belgesi!¶

Contents:

## Giriş¶

Bu belgede, sanal sunucu üzerinde flask uygulaması çalıştırmak için
kullanılabilecek yöntemlerden birini örnek ayar dosyalarını da vererek
anlatmaya çalışacağız. Senaryoc

Flask ile yazılmış uygulamaları sanal sunucularda çalıştırmak çoğu kişi için
altından kalkılamayacak bir işyükü gibi görünür. Ayarlanması gereken birden
fazla servis olduğundan,

## DNS¶

DNS,(Domain Name Server) kısaca ip alan adı dönüşümünü ya da alan adı ip
adresi dönüşümünü yapar.

DNS’se sorulan alan adı adresini DNS biliyorsa ya da cache’in de var ise hemen
geri dönüş yapar. Eğer ki DNS alan adının adresini bilmiyorsa bilen bir başka
DNS sunucusuna sorar böylece ve adres bilgisini soran kişiye cevap verir.

DNS sunucularının çeşiteri vardır. 1- Birincil(Master) DNS 2- İkincil(Slave)
DNS 3- Depolama(Cache Only) DNS 4- Gizli(Stealth) DNS

### Birincil DNS¶

Tek başına çalışan DNS sunucularıdır.

### İkincil DNS¶

DNS önemli bir servistir. Tek başına çalışmaması önerilir. DNS sunucuları çok
fazla istek aldığı için ikincil yardımcı sunuculara ihtiyaç vardır.

### Depolama DNS¶

Herhangi bir alanadı sunmaz, sadece sorgulara daha hızlı yanıt verir. Verdiği
cevapları bir süre önbelleğinde tuttuğu için depolama (cache only dns)
denilmektedir.

Biz anlatımımızı Bind DNS için yapacağız.

Bind DNS kurulumu;

### Debian/Ubuntu Sistemler için¶

    
    
    $ sudo apt-get install bind9 dnsutils
    

Debian ve ubuntu sistemleri için dns ayarları “/etc/bind” dizini altından
yapılır. DNS ayarları “named.conf.options” dosyasından yapılır.(forwarders,
recursive, port…)

DNS sunucunuzu çalıştırmak için;

    
    
    $ sudo systemctl start bind9
    

DNS sunucunuzun açılışta çalışması için;

    
    
    $ sudo systemctl enable bind9
    

DNS sunucusu kurulduktan sonra “named.conf.options” dosyasından “forwarders”
bloğunu yorum satırı olmaktan çıkartırsanız. DNS sunucusuna gelen sorgulari
kendinde bulamaz ise “forwarders” bilgisine bakar ve o adrese kendine gelen
soruyu sorar cevap geldiğin de kendine gelen sorguyu cevaplar.

ÖRNEK:

    
    
    forwarders{
         8.8.8.8;
         8.8.4.4;
    }
    

DNS sunucunuzu ayarların geçerli olması için yeniden başlatın.

    
    
    $ systemctl restart bind9
    

Sisteminizin DNS adreserini DNS sunucunuzun ip adresini girin ve google’a ping
atmayı deneyin. Cevap alıyor iseniz DNS sunucunuz olması gerektiği gibi
çalışıyor demektir.

DNS sunucunuz sadece sizin sorgularınıza cevap veriyor. Yani ona “example.com”
gibi bir adrese gitmek istediğinizi söylediğiniz de size “example.com”
alanadının bilgisini verecektir.

DNS suncunuz için bir alan adı belirleyelim.

Zone tanımlarımızı “named.conf.local” dosyasına yaparız.

ÖRNEK (manap.com adından bir zone oluşturalım):

    
    
    zone "manap.com" {
         type master;
         file "/etc/bind/db.manap.com";
    };
    

Zone dosyasını kolayca oluşturmak için “/etc/bind/db.local” dosyasının
kopyasını kullanabiliriz.

    
    
    $ cp /etc/bind/db.local /etc/bind/db.manap.com
    

Daha sonra “db.manap.com” dosyasını şu şekilde dolduruyoruz.

    
    
    root@ubuntu:/etc/bind# cat db.manap.com
    ;
    ; BIND data file for local loopback interface
    ;
    $TTL    604800
    @       IN      SOA     localhost. root@manap.com. (          soa kaydi
                               2         ; Serial                         seri numarasi bu dosyada herdegisklik yapildiginda bu degerin onceki degerinden fazla olmasi gerekir.
                          604800         ; Refresh                        yenilenme suresi
                           86400         ; Retry                          tekrar etme suresi
                         2419200         ; Expire                         gecerlilik suresi
                          604800 )       ; Negative Cache TTL cache te bekleme suresi
    ;
    @       IN      NS      manap.com.           ; isim sunucusunun adi
    @       IN      A       192.168.1.102        ; isim sunucusunun adresi
    @       IN      AAAA    ::1
    

DNS sunucumuza “manap.com” alanadına erişip erişemediğini test edelim.

    
    
    root@ubuntu:/etc/bind# ping -c 2 manap.com
    PING manap.com (192.168.1.102) 56(84) bytes of data.
    64 bytes from 192.168.1.102: icmp_seq=1 ttl=64 time=0.017 ms
    64 bytes from 192.168.1.102: icmp_seq=2 ttl=64 time=0.029 ms
    
    --- manap.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    rtt min/avg/max/mdev = 0.017/0.023/0.029/0.006 ms
    

Erişebiliyor, buraya tüm sonuçlar aynı ise herhangi bi sorun yoktur demektir.
DNS sunucumuz alan adını sorduğumuz ip adresini söyleyebiliyor fakat ip
adresinden alan adını getiremiyor.

    
    
    root@ubuntu:/etc/bind# host 192.168.1.102
    
    ;; connection timed out; no servers could be reached
    

DNS sunucumuzun ip adresinden alan adını getirebilmesi için reverzone
dosyasının da oluşturulması gerekir.

“named.conf.local” dosyasına reverse zone dosyasını ve adresini oluşturmamız
gerekir. reverse zone dosyasını kolay oluşturmak için “/etc/bind/db.127”
dosyasının bir kopyasını oluşturuyoruz.

    
    
    $ cp /etc/bind/db.127 /etc/bind/rev.manap.com
    

Daha sonra içerisini şu şekilde dolduruyoruz.

    
    
    root@ubuntu:/etc/bind# cat rev.manap.com
    ;
    ; BIND reverse data file for local loopback interface
    ;
    $TTL    604800
    @       IN      SOA     manap.com. root.manap.com. (
                               6         ; Serial
                          604800         ; Refresh
                           86400         ; Retry
                         2419200         ; Expire
                          604800 )       ; Negative Cache TTL
    ;
    @       IN      NS      ns.
    102     IN      PTR     ns.manap.com.
    

Dosyamızın içine yukarıdaki gibi doldurduktan sonra ptr kaydını sorgulayalım.

    
    
    root@ubuntu:/etc/bind# host 192.168.1.102
    102.1.168.192.in-addr.arpa domain name pointer ns.manap.com.
    

DNS sunucusun en temel kurulumu yukarıdaki gibidir. “named.conf.options”
dosyasında yapılabilecek bazı ayarlar

“recursion yes;” = DNS sunucusunun bilemediği bir adresi başka bir dns
sunucusunu sorulmasını isteniyor ise yes değeri verilir.

    
    
     "acl 'trusted'{
          192.168.1.105;
          192.168.1.104;
          192.168.2.0/24;
    };
    

” = acl ile sadece belirtilen ip adreslerinden veya networklerden sorguları
kabul etmesi için kullanılır. Fakat sadece bu kullanımı ile çalışmayacaktır.
“allow-recursion { trusted; };” = ile acl trusted olanlardan sorgu alabilir.
“listen-on { 192.168.1.102; };” = hangi ip adresinden dns sorgularını
dinleyeceğini belirtmek için kullanılır. “allow-transfer { none; };” = zone
tranferi yapıp yapmayacağını karar vermek için kullanılır. Zone transferi
ikincil sunucuya yapılacak ise “none” değeri yerine ip adresi yazılmalıdır.

UBUNTU İÇİN DNS KURULUMU BU KADAR ŞİMDİ CENTOS SİSTEMLER İÇİN DNS KURULUMUNUN
ANLATIMINA GEÇELİM.

### Centos için dns kurulumu¶

    
    
    $ sudo yum install bind bind-chroot bind-libs bind-utils
    

Centos sistemlerde dns ayarları “/etc/named.conf” dosyasından yapılır.

Dosyanın içerisinde yapılması gereken bir kaç temel ayar vardır bunlar;

    
    
    options {
         listen-on port 53 { 127.0.0.1; 192.168.1.101; }; /* hangi ip adresinden dns sorgularını dinleyeceğiniz ve hangi portu dinleyeceğiniz */
         directory "/var/named"; /* zone dosyalarını nerede tutacağınızın bilgileri*/
         forwarders{
                 8.8.8.8;
                 8.8.4.4;
         }; /* dns sunucu gelen sorgulara cevap veremeyince kime soracağının bilgisi */
    
         recursion yes; /* dns sunucusun diğer dns sunuculara alanadı bilgilerini sorması için */
    
    };
    

Centos sistemlerde zone bilgileri “/etc/named.conf” dosyasına yazılır.

    
    
    zone "manap.com" {
         type master;
         file "/var/named/db.manap.com";
    };
    

Daha “/var/named/” dizinine gidilir. Buradaki “named.localhost” dosyasının bir
kopyası oluşturulur.

    
    
    $ cp /var/named/named.localhost /var/named/db.manap.com
    

Daha içerisi aşağıdaki gibi düzenlenir.

    
    
    [root@centos named]# cat db.manap.com
    $TTL 1D
    @       IN SOA  ns.manap.com. root@manap.com. (
                                         4       ; serial
                                         1D      ; refresh
                                         1H      ; retry
                                         1W      ; expire
                                         3H )    ; minimum
    @       IN      NS      manap.com.
    @       IN      A       192.168.1.101
    

Daha sonra “db.manap.com” dosyasının sahiplik bilgileri “named” kullanıcısına
verilir. Eğer sahiplik bilgileri değiştirilmez ise dns sunucusu
çalışmayacaktır.

    
    
    $ chown named:named db.manap.com
    

Şimdi dns sunucusunu yeniden başlatabiliriz. DNS sunucusu yeniden
başlatıldıktan sonra sisteminizin dns adresleri olarak dns sunucunuzun ip
adreslerini girmelisiniz.

    
    
    $ systemctl restart named
    
    [root@centos named]# ping -c 2 manap.com
    PING manap.com (192.168.1.101) 56(84) bytes of data.
    64 bytes from centos (192.168.1.101): icmp_seq=1 ttl=64 time=0.014 ms
    64 bytes from centos (192.168.1.101): icmp_seq=2 ttl=64 time=0.032 ms
    
    --- manap.com ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1001ms
    rtt min/avg/max/mdev = 0.014/0.023/0.032/0.009 ms
    

DNS sunucusu alanadı ip adresi dönüşümünü yapıyor fakat ip adresi alan adı
dönüşümünü yapamıyor. Bunun için Reversezone dns bilgileri oluşturmamız
gerekir.

    
    
    [root@centos named]# host 192.168.1.101
    Host 101.1.168.192.in-addr.arpa. not found: 3(NXDOMAIN)
    

DNS sunucumuz ip adresi alan adı dönüşümünü yapamıyor.

“/etc/named.conf” dosyamıza aşağıdaki gibi zone bilgilerini giriyroruz.

    
    
    zone "1.168.192.in-addr.arpa" {
       type master;
       file "/var/named/rev.manap.com";
    };
    

Daha sonra “/var/named” dizinine gidip “named.loopback” dosyasının bir
kopyasını oluşturuyoruz.

    
    
    $ cp /var/named/named.loopback /var/named/rev.manap.com
    

“rev.manap.com” dosyasının içerisi aşağıdaki gibi doldurup, sahiplik bilgisini
değiştiriyoruz ve dns sunucumuzu yeniedn başlatıyoruz.

    
    
    [root@centos named]# host 192.168.1.101
    101.1.168.192.in-addr.arpa domain name pointer ns.manap.com.
    

Tüm bunları yaptıktan sonra DNS sunucumuza ip adresini sorduğumuzda bize alan
adını verdiğini gördük.

## NGINX Kurulum ve Ayarlar¶

NGINX, Apache gibi bir web sunucu uygulamasıdır. Birden fazla web sitesini
farklı domain adları altında kolayca sunar.

Flask, django, php gibi web çatıları ile yazılmış uygulamaları aynı sunucu
üzerinde sunabilirsiniz.

## Ayar ve Uygulama Dosyalari¶

Kodlar, ayar dosyalarini buraya ekleyecegiz.

### NGINX Ayarlari¶

    
    
    server {
    	listen 443 ssl;
    	server_name hello_world.example.com;
    	root /var/www/webservice/hello_world;
    	access_log  /var/log/nginx/hello_world_secure.access.log;
    	error_log  /var/log/nginx/hello_world_secure.error.log error;
    	index	index.html index.htm index.php;
    	
    	ssl_session_timeout  5m;	
    	ssl_protocols        SSLv3 TLSv1;
    	ssl_certificate      /etc/letsencrypt/live/hello_world.example.com/cert.pem;
    	ssl_certificate_key  /etc/letsencrypt/live/hello_world.example.com/privkey.pem;
    
    	location / {
    	    include uwsgi_params;
               uwsgi_modifier1 30;
    	    uwsgi_pass unix:/var/www/webservice/hello_world/uwsgi.sock;
    	}
    
    	location ^~ /static/  {
    	    include  /etc/nginx/mime.types;
    	    root /var/www/html/hello_world_static;
    	}	
    }
    
    server {
    	listen       80;
    	server_name  hello_world.example.com;
    	# eger ssl olmayan siteden otomatik olarak ssl olan siteye 
            # yonelmesini istiyorsaniz, asagidaki satirin onundeki # isaretini kaldirin
    	#return 301 https://$server_name$request_uri; 
    
    	location / {
                include uwsgi_params;
                uwsgi_modifier1 30;
    	    uwsgi_pass unix:/var/www/webservice/hello_world/uwsgi.sock;
            }
    
    
    
    	location ^~ /static/  {
    	    include  /etc/nginx/mime.types;
    	    root /var/www/html/hello_world_static;
    	}	
    
    }
    
    
    

### Systemd Servis Dosyasi¶

    
    
    [Unit]
    Description=Hello_world UWSGI servisi 
    After=network.target
    
    [Service]
    User=nginx
    Group=nginx
    WorkingDirectory=/var/www/webservice/hello_world
    ExecStart=/usr/bin/uwsgi --ini uwsgi.ini
    
    [Install]
    WantedBy=multi-user.target
    

# Tablolar ve Indeksler¶

  * [Dizin](genindex.html)
  * [Modül Dizini](py-modindex.html)
  * [Arama Sayfası](search.html)

# [Flask, Uwsgi, Nginx, systemd](index.html#document-index)

### Gezinti

  * [Giriş](index.html#document-doc/Giris)
  * [DNS](index.html#document-doc/DNS)
  * [NGINX Kurulum ve Ayarlar](index.html#document-doc/Nginx)
  * [Ayar ve Uygulama Dosyalari](index.html#document-doc/AyarDosyalari)

### Related Topics

  * [Documentation overview](index.html#document-index)

(C)2018, Ilker Manap. | Powered by [Sphinx 1.8.2](http://sphinx-doc.org/) &
[Alabaster 0.7.12](https://github.com/bitprophet/alabaster)

