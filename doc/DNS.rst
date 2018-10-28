DNS
=== 

DNS,(Domain Name Server) kısaca ip alan adı dönüşümünü ya da alan adı ip adresi dönüşümünü yapar.

DNS'se sorulan alan adı adresini DNS biliyorsa ya da cache'in de var ise hemen geri dönüş yapar. Eğer ki DNS alan adının adresini bilmiyorsa bilen bir başka DNS sunucusuna sorar böylece ve adres bilgisini soran kişiye cevap verir.

DNS sunucularının çeşiteri vardır.
1- Birincil(Master) DNS 
2- İkincil(Slave) DNS
3- Depolama(Cache Only) DNS
4- Gizli(Stealth) DNS

Birincil DNS 
............
Tek başına çalışan DNS sunucularıdır. 

İkincil DNS 
...........
DNS önemli bir servistir. Tek başına çalışmaması önerilir. DNS sunucuları çok fazla istek aldığı için ikincil yardımcı sunuculara ihtiyaç vardır.

Depolama DNS
............
Herhangi bir alanadı sunmaz, sadece sorgulara daha hızlı yanıt verir. Verdiği cevapları bir süre önbelleğinde tuttuğu için depolama (cache only dns) denilmektedir.


Biz anlatımımızı Bind DNS için yapacağız.

Bind DNS kurulumu;

Debian/Ubuntu Sistemler için
............................

.. code-block:: bash

   $ sudo apt-get install bind9 dnsutils


Debian ve ubuntu sistemleri için dns ayarları "/etc/bind" dizini altından yapılır.
DNS ayarları "named.conf.options" dosyasından yapılır.(forwarders, recursive, port...)

DNS sunucunuzu çalıştırmak için;


.. code-block:: bash
   
   $ sudo systemctl start bind9


DNS sunucunuzun açılışta çalışması için;

.. code-block:: bash

   $ sudo systemctl enable bind9


DNS sunucusu kurulduktan sonra "named.conf.options" dosyasından "forwarders" bloğunu yorum satırı olmaktan çıkartırsanız. DNS sunucusuna gelen sorgulari kendinde bulamaz ise "forwarders" bilgisine bakar ve o adrese kendine gelen soruyu sorar cevap geldiğin de kendine gelen sorguyu cevaplar.

ÖRNEK:

.. code-block:: bash

   forwarders{
 	8.8.8.8;
	8.8.4.4;
   }
   


DNS sunucunuzu ayarların geçerli olması için yeniden başlatın.


.. code-block:: bash
   
   $ systemctl restart bind9


Sisteminizin DNS adreserini DNS sunucunuzun ip adresini girin ve google'a ping atmayı deneyin. Cevap alıyor iseniz DNS sunucunuz olması gerektiği gibi çalışıyor demektir.

DNS sunucunuz sadece sizin sorgularınıza cevap veriyor. Yani ona "example.com" gibi bir adrese gitmek istediğinizi söylediğiniz de size "example.com" alanadının bilgisini verecektir. 

DNS suncunuz için bir alan adı belirleyelim.

Zone tanımlarımızı "named.conf.local" dosyasına yaparız.

ÖRNEK (manap.com adından bir zone oluşturalım):

.. code-block:: bash

   zone "manap.com" {
	type master;
	file "/etc/bind/db.manap.com";
   };


Zone dosyasını kolayca oluşturmak için "/etc/bind/db.local" dosyasının kopyasını kullanabiliriz. 

.. code-block:: bash

   $ cp /etc/bind/db.local /etc/bind/db.manap.com


Daha sonra "db.manap.com" dosyasını şu şekilde dolduruyoruz.

.. code-block:: bash

   root@ubuntu:/etc/bind# cat db.manap.com 
   ;
   ; BIND data file for local loopback interface
   ;
   $TTL    604800	
   @       IN      SOA     localhost. root@manap.com. (    	 soa kaydi
                              2         ; Serial			 seri numarasi bu dosyada herdegisklik yapildiginda bu degerin onceki degerinden fazla olmasi gerekir.
                         604800         ; Refresh			 yenilenme suresi
                          86400         ; Retry				 tekrar etme suresi
                        2419200         ; Expire			 gecerlilik suresi
                         604800 )       ; Negative Cache TTL cache te bekleme suresi
   ;
   @       IN      NS      manap.com. 		; isim sunucusunun adi
   @       IN      A       192.168.1.102	; isim sunucusunun adresi
   @       IN      AAAA    ::1


DNS sunucumuza "manap.com" alanadına erişip erişemediğini test edelim.

.. code-block:: bash

   root@ubuntu:/etc/bind# ping -c 2 manap.com
   PING manap.com (192.168.1.102) 56(84) bytes of data.
   64 bytes from 192.168.1.102: icmp_seq=1 ttl=64 time=0.017 ms
   64 bytes from 192.168.1.102: icmp_seq=2 ttl=64 time=0.029 ms

   --- manap.com ping statistics ---
   2 packets transmitted, 2 received, 0% packet loss, time 1001ms
   rtt min/avg/max/mdev = 0.017/0.023/0.029/0.006 ms


Erişebiliyor, buraya tüm sonuçlar aynı ise herhangi bi sorun yoktur demektir.
DNS sunucumuz alan adını sorduğumuz ip adresini söyleyebiliyor fakat ip adresinden alan adını getiremiyor.

.. code-block:: bash

   root@ubuntu:/etc/bind# host 192.168.1.102

   ;; connection timed out; no servers could be reached

DNS sunucumuzun ip adresinden alan adını getirebilmesi için reverzone dosyasının da oluşturulması gerekir.

"named.conf.local" dosyasına reverse zone dosyasını ve adresini oluşturmamız gerekir.
reverse zone dosyasını kolay oluşturmak için "/etc/bind/db.127" dosyasının bir kopyasını oluşturuyoruz.

.. code-block:: bash

   $ cp /etc/bind/db.127 /etc/bind/rev.manap.com


Daha sonra içerisini şu şekilde dolduruyoruz.

.. code-block:: bash

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

.. code-block:: bash

   root@ubuntu:/etc/bind# host 192.168.1.102
   102.1.168.192.in-addr.arpa domain name pointer ns.manap.com.


DNS sunucusun en temel kurulumu yukarıdaki gibidir. 
"named.conf.options" dosyasında yapılabilecek bazı ayarlar 

"recursion yes;" = DNS sunucusunun bilemediği bir adresi başka bir dns sunucusunu sorulmasını isteniyor ise yes değeri verilir.

.. code-block:: bash

   "acl 'trusted'{
	192.168.1.105;
	192.168.1.104;
	192.168.2.0/24;
  };

" = acl ile sadece belirtilen ip adreslerinden veya networklerden sorguları kabul etmesi için kullanılır. Fakat sadece bu kullanımı ile çalışmayacaktır.
"allow-recursion { trusted; };" = ile acl trusted olanlardan sorgu alabilir.
"listen-on { 192.168.1.102; };" = hangi ip adresinden dns sorgularını dinleyeceğini belirtmek için kullanılır.
"allow-transfer { none; };" = zone tranferi yapıp yapmayacağını karar vermek için kullanılır. Zone transferi ikincil sunucuya yapılacak ise "none" değeri yerine ip adresi yazılmalıdır.


UBUNTU İÇİN DNS KURULUMU BU KADAR ŞİMDİ CENTOS SİSTEMLER İÇİN DNS KURULUMUNUN ANLATIMINA GEÇELİM.

Centos için dns kurulumu
........................

.. code-block:: bash

   $ sudo yum install bind bind-chroot bind-libs bind-utils


Centos sistemlerde dns ayarları "/etc/named.conf" dosyasından yapılır.

Dosyanın içerisinde yapılması gereken bir kaç temel ayar vardır bunlar;

.. code-block:: bash

   options {
	listen-on port 53 { 127.0.0.1; 192.168.1.101; }; /* hangi ip adresinden dns sorgularını dinleyeceğiniz ve hangi portu dinleyeceğiniz */
	directory "/var/named"; /* zone dosyalarını nerede tutacağınızın bilgileri*/
	forwarders{
		8.8.8.8;
		8.8.4.4;
	}; /* dns sunucu gelen sorgulara cevap veremeyince kime soracağının bilgisi */

	recursion yes; /* dns sunucusun diğer dns sunuculara alanadı bilgilerini sorması için */

   };

Centos sistemlerde zone bilgileri "/etc/named.conf" dosyasına yazılır.

.. code-block:: bash

   zone "manap.com" {
	type master;
	file "/var/named/db.manap.com";	
   };

Daha "/var/named/" dizinine gidilir. Buradaki "named.localhost" dosyasının bir kopyası oluşturulur.

.. code-block:: bash
   
   $ cp /var/named/named.localhost /var/named/db.manap.com

Daha içerisi aşağıdaki gibi düzenlenir.

.. code-block:: bash
		
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

Daha sonra "db.manap.com" dosyasının sahiplik bilgileri "named" kullanıcısına verilir. Eğer sahiplik bilgileri değiştirilmez ise dns sunucusu çalışmayacaktır.

.. code-block:: bash
		
   $ chown named:named db.manap.com

Şimdi dns sunucusunu yeniden başlatabiliriz. DNS sunucusu yeniden başlatıldıktan sonra sisteminizin dns adresleri olarak dns sunucunuzun ip adreslerini girmelisiniz.

.. code-block:: bash
		
   $ systemctl restart named

   [root@centos named]# ping -c 2 manap.com
   PING manap.com (192.168.1.101) 56(84) bytes of data.
   64 bytes from centos (192.168.1.101): icmp_seq=1 ttl=64 time=0.014 ms
   64 bytes from centos (192.168.1.101): icmp_seq=2 ttl=64 time=0.032 ms

   --- manap.com ping statistics ---
   2 packets transmitted, 2 received, 0% packet loss, time 1001ms
   rtt min/avg/max/mdev = 0.014/0.023/0.032/0.009 ms

DNS sunucusu alanadı ip adresi dönüşümünü yapıyor fakat ip adresi alan adı dönüşümünü yapamıyor. Bunun için Reversezone dns bilgileri oluşturmamız gerekir.

.. code-block:: bash

   [root@centos named]# host 192.168.1.101
   Host 101.1.168.192.in-addr.arpa. not found: 3(NXDOMAIN)

DNS sunucumuz ip adresi alan adı dönüşümünü yapamıyor.

"/etc/named.conf" dosyamıza aşağıdaki gibi zone bilgilerini giriyroruz.

.. code-block:: bash
		
   zone "1.168.192.in-addr.arpa" {
      type master;
      file "/var/named/rev.manap.com";
   };

Daha sonra "/var/named" dizinine gidip "named.loopback" dosyasının bir kopyasını oluşturuyoruz.

.. code-block:: bash
		
   $ cp /var/named/named.loopback /var/named/rev.manap.com

"rev.manap.com" dosyasının içerisi aşağıdaki gibi doldurup, sahiplik bilgisini değiştiriyoruz ve dns sunucumuzu yeniedn başlatıyoruz.

.. code-block:: bash
		
   [root@centos named]# host 192.168.1.101
   101.1.168.192.in-addr.arpa domain name pointer ns.manap.com.
   
Tüm bunları yaptıktan sonra DNS sunucumuza ip adresini sorduğumuzda bize alan adını verdiğini gördük.

















































































