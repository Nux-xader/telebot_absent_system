###############################################
# for store data
BASE_API = "http://192.168.1.9:8000"
START_ABSENT_URL = BASE_API+"/api/absen/datang"
END_ABSENT_URL = BASE_API+"/api/absen/pulang"
REGISTER_ABSENT_URL = BASE_API+"/api/absen/register"
###############################################
# format : HH:MM
ABSENT_START = "07:00"
LATE_ABSENT = "07:45"
ABSENT_FINISH = "16:08"
###############################################
###############################################
ABSENT_START_MSG = """
Hai!
Udah siap kerja belom:V
Absen yuk supaya jam kerjamu terhitung
klik hadir atau alpa
/hadir    /alpa
"""
LATE_ABSENT_MSG = f"""
Waduh kok bisa telat sih absen nya
catat ini ya jam mulai absen {ABSENT_START} , dan jam telat absen {LATE_ABSENT}
Lain kali jangan telat absen lagi ya!
Semangat kerja nyaaaa
"""
ABSENT_FINISH_MSG = f"""
Haiii!
Udah jam {ABSENT_FINISH} nih, jam kerja kmu udah habis tau
klik selesaikerja terus istirahat biar pegel pegel nya ilang
/selesaikerja
"""
###############################################
ATTENTION_PASSWORD = "admin123"
###############################################