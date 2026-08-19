from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import requests, time, threading

# Ini link server lu yang udah kita tes tadi
URL_SERVER = "https://mistress-switched-phil-envelope.trycloudflare.com"
HEADERS = {"x-api-key": "KunciSuperKuat123"}

class PekerjaApp(App):
    def build(self):
        # Bikin tampilan layar
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.status = Label(text="Agen Komputasi Siap.\nMenunggu Perintah...", halign="center")
        self.btn = Button(text="Ambil Tugas Hitung!", size_hint=(1, 0.3))
        self.btn.bind(on_press=self.mulai_kerja)
        
        self.layout.add_widget(self.status)
        self.layout.add_widget(self.btn)
        return self.layout

    def mulai_kerja(self, instance):
        self.status.text = "Menghubungi markas pusat..."
        self.btn.disabled = True
        # Jalankan proses di latar belakang biar layar HP nggak nge-freeze
        threading.Thread(target=self.proses_kerja).start()

    def update_status(self, teks):
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', teks))

    def proses_kerja(self):
        try:
            respons = requests.get(f"{URL_SERVER}/minta_tugas", headers=HEADERS).json()
            if "pesan" in respons and respons["pesan"] == "Akses Ditolak!":
                self.update_status("AKSES DITOLAK! Kunci Salah.")
                return
                
            jumlah = respons.get("jumlah_loop", 10000000)
            self.update_status(f"Mengerjakan komputasi\n{jumlah} perulangan...")
            
            mulai = time.time()
            hasil = 0
            for i in range(jumlah):
                hasil += i * 2
                
            waktu = round(time.time() - mulai, 2)
            self.update_status(f"Selesai dalam {waktu} detik.\nMengirim hasil...")
            
            data_setoran = {"id_tugas": 2, "hasil": hasil, "waktu": waktu}
            requests.post(f"{URL_SERVER}/kirim_hasil", json=data_setoran, headers=HEADERS)
            
            self.update_status(f"Hasil Terkirim!\nServer mencatat waktumu.")
            
        except Exception as e:
            self.update_status("Gagal terhubung ke server! Pastikan server Termux nyala.")
        finally:
            # Nyalain tombolnya lagi
            Clock.schedule_once(lambda dt: setattr(self.btn, 'disabled', False))

if __name__ == '__main__':
    PekerjaApp().run()

