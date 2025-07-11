import mysql.connector
import pandas as pd
from datetime import datetime, timedelta

class Report():

    def __init__(self, database):
        self.database = database
        self.df_dailyLogData = self.sql_connection() 

    def sql_connection(self):

        conn = mysql.connector.connect(
            host="your_database_host",
            port=your_database_post,        
            user="your_database_user",    
            password="your_database_password",       
            database=self.database
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM db_dailylog order by repDay desc limit 1 offset 1")
        dailyLogData = cursor.fetchall()  
        df_dailyLogData = pd.DataFrame(dailyLogData)
        df_dailyLogData.columns = ["your_database_columns"]
        
        cursor.close()
        conn.close()

        return df_dailyLogData
        #, df_dblogsDatas 

    def take_datetime(self):
        turkce_aylar = {
            1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
            7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
        }

        turkce_gunler = {
            0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
            4: "Cuma", 5: "Cumartesi", 6: "Pazar"
        }

        yesterday = datetime.today() - timedelta(days=1)
        gun = turkce_gunler[yesterday.weekday()]  # 0 = Pazartesi
        ay = turkce_aylar[yesterday.month]
        tarih_str = f"{yesterday.day} {ay} {gun} {yesterday.year}"
        return tarih_str
    
    def getTramKm(self):
        df_rows = self.df_dailyLogData
        """
        KM HESAPLAMA KISMI
        """
        tramKm = df_rows.tramKm.iloc[0] / 1000000  
        tramKmStr = f"{tramKm:.3f} km"  

        return tramKmStr
    
    def getTramWorkTime(self):
        df_rows = self.df_dailyLogData
        """
        KM HESAPLAMA KISMI
        """
        depoSureTime = df_rows.depoSure / 3600
        hatSureTime = df_rows.hatSure / 3600

        total_hours = depoSureTime + hatSureTime
        self.calismaSure = total_hours.apply(lambda x: f"{int(x)}:{int((x * 60) % 60):02d}")  

        return self.calismaSure[0]
    

    def getTramMoveTime(self):
        df_rows = self.df_dailyLogData
        """
        HAREKET SÜRESİ HESAPLAMA
        """
        hareketSureTime = df_rows.hareketSure / 3600
        self.hareketSureTotalTime = hareketSureTime.apply(lambda x: f"{int(x)}:{int((x * 60) % 60):02d}")
        
        return self.hareketSureTotalTime[0]
    

    def getTramZeroTime(self):
        df_rows = self.df_dailyLogData
        """
        SIFIR HIZ SÜRESİ HESAPLAMA
        """
        beklemeSuresiTime = df_rows.sifirHizSure / 3600
        self.bekleSuresTotalTime = beklemeSuresiTime.apply(lambda x: f"{int(x)}:{int((x * 60) % 60):02d}")

        return self.bekleSuresTotalTime[0]
    
    def getTramDailyKm(self):
        df_rows = self.df_dailyLogData
        """
        GÜNLÜK KM HESAPLAMA
        """
        günlükKm = df_rows.gnlKM / 1000 
        günlükKmStr = günlükKm.apply(lambda x: f"{x:.0f}")
        self.günlükTotalKm = günlükKmStr + " km"

        return self.günlükTotalKm[0]
    
    def getTramTotalCekisPower(self):
        df_rows = self.df_dailyLogData
        """
        ÇEKİŞ ÜNİTESİ GÜÇ HESAPLAMA
        """
        cekisUnite = df_rows.gnlkWH_a0 + df_rows.gnlkWH_b0
        totalCekisUnite = int(cekisUnite.iloc[0]) 

        return totalCekisUnite
    
    def getTramBackGainEnergy(self):
        df_rows = self.df_dailyLogData
        """
        GERİ KAZANDIRILAN ENERJİ GÜÇ HESAPLAMA
        """
        kazandirilanEnerji = df_rows.gnlkWH_a1 + df_rows.gnlkWH_b1
        totalKazandirilanEnerji = int(kazandirilanEnerji.iloc[0])

        return totalKazandirilanEnerji
    
    def getTramBreakResEnergy(self):
        df_rows = self.df_dailyLogData
        """
        TÜKETİM FRENLEME DİRENCİ ENERJİ GÜÇ HESAPLAMA
        """
        dirençEnerji = df_rows.gnlkWH_a2 + df_rows.gnlkWH_b2
        totalDirençEnerji = int(dirençEnerji.iloc[0])

        return totalDirençEnerji
    
    def getTramTcuEnergy(self):
        df_rows = self.df_dailyLogData
        """
        TÜKETİM YARDIMCI GÜÇ HESAPLAMA
        """
        yardimciGuc = df_rows.gnlkWH_a3 + df_rows.gnlkWH_b3
        totalYardimciGuc = int(yardimciGuc.iloc[0])

        return totalYardimciGuc
    
    def getTramTotalEnergy(self):

        """
        TOPLAM TÜKETİLEN ENERJİ HESAPLAMA

        FONKSİYONLARIN ÇAĞIRILDIĞI YERDE HESAPLANMAKTADIR
        """
        pass
        

    def getTramEnergyByKm(self):
        """
        KM'DE TÜKETİLEN TOPLAM ENERJİ HESAPLAMA

        FONKSİYONLARIN ÇAĞIRILDIĞI YERDE HESAPLANMAKTADIR
        """
        pass
        
