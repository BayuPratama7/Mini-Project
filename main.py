# Sistem Manajemen Keuangan Toko Cuci Sepatu

import os
import datetime
import time
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Konfigurasi Database
DB_URL = 'sqlite:///toko_cuci_sepatu.db'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Model Data
class Transaksi(Base):
    __tablename__ = 'transaksi'

    id = Column(Integer, primary_key=True)
    tanggal = Column(DateTime, default=datetime.datetime.now)
    jenis = Column(String)
    jumlah = Column(Float)
    keterangan = Column(String)

class Pelanggan(Base):
    __tablename__ = 'pelanggan'

    id = Column(Integer, primary_key=True)
    nama = Column(String)
    kontak = Column(String)

class Pemasok(Base):
    __tablename__ = 'pemasok'

    id = Column(Integer, primary_key=True)
    nama = Column(String)
    kontak = Column(String)

# Fungsi-fungsi Utama
def catat_transaksi(session, jenis, jumlah, keterangan):
    transaksi = Transaksi(jenis=jenis, jumlah=jumlah, keterangan=keterangan)
    session.add(transaksi)
    session.commit()

def tambah_pelanggan(session, nama, kontak):
    pelanggan = Pelanggan(nama=nama, kontak=kontak)
    session.add(pelanggan)
    session.commit()

def tambah_pemasok(session, nama, kontak):
    pemasok = Pemasok(nama=nama, kontak=kontak)
    session.add(pemasok)
    session.commit()

def buat_laporan_laba_rugi(session):
    pendapatan = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Pendapatan').scalar()
    biaya = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Biaya').scalar()
    laba_rugi = pendapatan - biaya
    return laba_rugi

def buat_laporan_neraca(session):
    aset = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Aset').scalar()
    liabilitas = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Liabilitas').scalar()

    if aset is None:
        aset = 0.0
    if liabilitas is None:
        liabilitas = 0.0

    ekuitas = aset - liabilitas
    return aset, liabilitas, ekuitas

def buat_laporan_arus_kas(session):
    kas_masuk = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Kas Masuk').scalar()
    kas_keluar = session.query(func.sum(Transaksi.jumlah)).filter(Transaksi.jenis == 'Kas Keluar').scalar()

    if kas_masuk is None:
        kas_masuk = 0.0
    if kas_keluar is None:
        kas_keluar = 0.0

    arus_kas = kas_masuk - kas_keluar
    return arus_kas

# Contoh Penggunaan
if __name__ == '__main__':
    # Inisialisasi Database
    Base.metadata.create_all(engine)

    # Buat Sesi
    session = Session()

    while True:
        # Catat Transaksi (contoh data)
        catat_transaksi(session, 'Pendapatan', 10000.0, 'Jasa Cuci Sepatu')
        catat_transaksi(session, 'Biaya', 500.0, 'Biaya Bahan Pembersih')

        # Buat Laporan Keuangan
        laba_rugi = buat_laporan_laba_rugi(session)
        aset, liabilitas, ekuitas = buat_laporan_neraca(session)
        arus_kas = buat_laporan_arus_kas(session)

        # Cetak Laporan
        print(f'Laporan Laba Rugi: {laba_rugi}')
        print(f'Laporan Neraca: Aset={aset}, Liabilitas={liabilitas}, Ekuitas={ekuitas}')
        print(f'Laporan Arus Kas: {arus_kas}')

       
        time.sleep(1)