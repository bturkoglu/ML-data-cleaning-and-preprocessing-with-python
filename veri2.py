import math

class Veri:
	def __init__(self, isim, parca):
		self.isim = isim
		self.min = 0
		self.max = 0
		self.parca = 0
		self.segmentler = dict()

		#segmentteki toplam satır ve positive survival satır bilgisini tutacak.
		self.segmentSatir = dict()

		self.parca = parca

		self.bilgi = 0
		self.kazanim = 0

	def segmentleriBul(self):
		parcaboyu = round((self.max - self.min + 1)/self.parca)
		ilk = self.min
		for i in range(self.parca):
			son = ilk + parcaboyu - 1
			self.segmentler[i] = [ilk, son]
			ilk = son + 1
		# Son parça yuvarlamadan dolayı yüksek çıksa da önemi yok
		# Çünkü datada o değer olmayacak. Düşük çıkabiliyor. Düzelteceğim.
		sonsegment = self.segmentler[self.parca-1]
		sonsegment[1] = self.max
		self.segmentler[self.parca-1] = sonsegment
		if goster:
			print('%s --> Segmentler:%s' %  (self.isim, self.segmentler))

	def verininSegmentiniBul(self, deger):
		# gelen deger hangi segmente giriyorsa onu bulur.
		segmenti = -1
		for ij in range(self.parca):
			bolge = self.segmentler[ij]
			if deger in range(bolge[0], bolge[1]+1):
				segmenti = ij
		if segmenti > -1:
			#if goster:print('%s deger:%s segmenti:%s'% (self.isim, deger, segmenti))
			return segmenti
		else:
			if goster:print('Hata var. Uygun segment bulunamadı. Deger:', deger, 'parca:',self.parca,'Segmentler:',self.segmentler)

	def bilgisiniBul(self, discDatalardakiKolonNo, bilgiPositive):
		sonuc = 0
		toplamSatir = len(discDatalar)
		for i in range(self.parca):
			toplamParcaSatir = 0
			toplamParcaSurvialPositiveValue = 0
			for satir in discDatalar:
				deger = satir[discDatalardakiKolonNo]
				survialdegeri = satir[3]
				if deger == i:
					toplamParcaSatir += 1
					if survialdegeri == 1:
						toplamParcaSurvialPositiveValue += 1

			# parca hesaplandı
			# if goster:
			# 	print('İsim:%s  Parca:%s ToplamParcaSatir:%s ToplamParcaSurvialPositiveValue:%s' % (self.isim, i, toplamParcaSatir, toplamParcaSurvialPositiveValue))

			self.segmentSatir[i] = (toplamParcaSatir, toplamParcaSurvialPositiveValue)
			sonuc = sonuc + toplamParcaSatir / toplamSatir * logBul(toplamParcaSurvialPositiveValue, toplamParcaSatir)

		self.bilgi = sonuc
		self.kazanim = bilgiPositive - sonuc
		if goster:
			print('İsim:%s  Bilgi:%s Kazanım:%s SegmentSatır:%s' % (self.isim, self.bilgi, self.kazanim, self.segmentSatir))
		return

def dosyaoku(filename):

	global Age, Year, Positive, datalar, discDatalar

	#Discreate değerleri bir kez hesaplamak için kullanılacak
	giris = True

	with open(filename,'r') as f:
		for line in f:
			satir = line.strip().split()
			#if goster:print('satir:',satir)
			if satir[0] == '@attribute' and satir[1] == 'Age':
				Age.min = int(satir[3].strip('[, ]'))
				Age.max = int(satir[4].strip('[, ]'))

			if satir[0] == '@attribute' and satir[1]=='Year':
				Year.min = int(satir[3].strip('[, ]'))
				Year.max = int(satir[4].strip('[, ]'))

			if satir[0] == '@attribute' and satir[1]=='Positive':
				Positive.min = int(satir[3].strip('[, ]'))
				Positive.max = int(satir[4].strip('[, ]'))

			# Datalar okunacak
			if satir[0][0] != '@':

				AgeValue = int(satir[0].strip(', '))
				YearValue = int(satir[1].strip(', '))
				PositiveValue = int(satir[2].strip(', '))
				SurvialValue = 0
				if satir[3].strip() == 'positive':
					SurvialValue = 1

				datalar.append((AgeValue, YearValue, PositiveValue, SurvialValue))

				if giris:
					for ii in [Age, Year, Positive]:
						ii.segmentleriBul()
					giris = False

				AgeDisc = Age.verininSegmentiniBul(AgeValue)
				YearDisc = Year.verininSegmentiniBul(YearValue)
				PositiveDisc = Positive.verininSegmentiniBul(PositiveValue)

				discDatalar.append((AgeDisc, YearDisc, PositiveDisc, SurvialValue))

def dosyayaYaz(dosyaYazilacak):
	with open(dosyaYazilacak, 'w') as f:
		for i in discDatalar:
			f.write(str(i).strip('()')+'\n')

def logBul(top1, toplam):
	# top1 veya toplam sıfırsa ne olacak? log2(x)'de x>0 olmak zorundadır.
	if top1 == 0 or toplam == 0 or top1 == toplam:
		sonuc = 0
	else:
		oran1 = top1 / toplam
		oran2 = (toplam - top1)/toplam
		#if goster:print('oran1',oran1,'oran2',oran2)
		#if goster:print('log1', math.log2(oran1))
		#if goster: print('log2', math.log2(oran2))
		sonuc = - oran1 * math.log2(oran1) - oran2 * math.log2(oran2)
	return sonuc

def bilgiHesapla():
	toplamSatir = len(discDatalar)
	toplamSurvialPositiveValue = 0
	for i in discDatalar:
		if i[3] == 1:
			toplamSurvialPositiveValue += 1

	bilgiPositive = logBul(toplamSurvialPositiveValue, toplamSatir)
	if goster: print('---> TOPLAM SATIR:%s  TOPLAM SURVIAL POSITIVE SATIR :%s' % (toplamSatir, toplamSurvialPositiveValue))

	# Age için yapalım.
	Age.bilgisiniBul(0, bilgiPositive)
	Year.bilgisiniBul(1, bilgiPositive)
	Positive.bilgisiniBul(2, bilgiPositive)


def test1():
	Age = Veri('Age',3)
	Age.min = 30
	Age.max = 83
	Age.segmentleriBul()
	print(Age.segmentler)
	for i in [30, 35, 40, 45, 47, 48, 50, 64, 65, 66, 83, 85, 90]:
		print(Age.verininSegmentiniBul(i))

def test2():
	dosyaoku(dosya)
	for i in [Age, Year, Positive]:
		i.segmentleriBul()
		print(i.min, i.max, i.parca, i.segmentler)

def test3():
	dosyaoku(dosya)
	for i in datalar:
		print(i)

def test4():
	dosyaoku(dosya)
	for i in discDatalar:
		print(i)

def test5():
	dosyaoku(dosya)
	dosyayaYaz(dosyaYazilacak)

def test6():
	dosyaoku(dosya)
	dosyayaYaz(dosyaYazilacak)
	bilgiHesapla()

if __name__ == '__main__':

	goster = True

	dosya = 'haberman.dat'
	dosyaYazilacak = 'HabermanYaz1.dat'

	datalar = list()
	discDatalar = list()

	AgeParcaAdedi = 3
	YearParcaAdedi = 4
	PositiveParcaAdedi = 10

	Age = Veri('Age', AgeParcaAdedi)
	Year = Veri('Year', YearParcaAdedi)
	Positive = Veri('Positive', PositiveParcaAdedi)

	# test1()
	# test2()
	# test3()
	# test4()
	# test5()
	test6()
