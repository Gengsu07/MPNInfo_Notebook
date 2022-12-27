import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as mysql
psql_conn = create_engine("postgresql+pg8000://postgres:sgwi2341@localhost/penerimaan")
db_conn = create_engine("mysql://sugengw07:sgwi2341@localhost/data_penerimaan")
mpninfokantor_conn = create_engine("mysql://admin:A1110PF@10.4.19.15/mpninfo")


def KueriUnion(tahun_pajak,conn_awal, conn_akhir):
    kueri = f'''
    SELECT admin,
       npwp,
       kpp,
       cabang,
       nama,
       kdmap,
       kdbayar,
       masa,
       tahun,
       tanggalbayar,
       bulanbayar,
       tahunbayar,
       datebayar,
       nominal,
       ntpn,
       bank,
       nosk,
       nospm,
       tipe,
       source,
       extra,
       billing,
       nop,
       pembuat,
       CASE
         WHEN SOURCE = 1 THEN 'MPN'
         ELSE 'SPM'
       END AS ket
FROM MPN
WHERE (tahunbayar) = {tahun_pajak}
UNION ALL
SELECT admin,
       npwp,
       kpp,
       cabang,
       '',
       kdmap,
       '',
       '',
       '',
       DAY(tanggal) AS TANGGALBAYAR,
       BULAN,
       TAHUN,
       tanggal,
       NOMINAL*-1,
       '',
       '',
       '',
       '',
       '',
       3 AS SOURCE,
       '',
       '',
       '',
       '',
       'SPMKP' AS ''
FROM spmkp
WHERE (TAHUN) = {tahun_pajak}
UNION ALL
SELECT A.admin,
       A.npwp,
       A.kpp,
       A.cabang,
       A.nama,
       kdmap,
       kdbayar,
       masapajak,
       tahunpajak,
       DAY(TANGGALDOC) AS TANGGALBAYAR,
       MONTH(TANGGALDOC) BULAN,
       YEAR(TANGGALDOC) TAHUN,
       TANGGALDOC,
       NOMINAL*-1,
       ntpn,
       '',
       nopbk,
       '',
       '',
       4 AS SOURCE,
       '',
       '',
       '',
       '',
       'PBK KIRIM' AS ''
FROM PBK A
  INNER JOIN MASTERFILE B ON A.NPWP = B.NPWP
WHERE YEAR(TANGGALDOC) = {tahun_pajak}
AND   A.KPP = B.KPP
AND   A.CABANG = B.CABANG
UNION ALL
SELECT A.ADMIN,
       npwp2,
       kpp2,
       cabang2,
       nama2,
       kdmap2,
       kdbayar2,
       masapajak2,
       tahunpajak2,
       DAY(TANGGALDOC) AS TANGGALBAYAR,
       MONTH(TANGGALDOC) BULAN,
       YEAR(TANGGALDOC) TAHUN,
       TANGGALDOC,
       NOMINAL,
       ntpn,
       '',
       nopbk,
       '',
       '',
       5 AS SOURCE,
       '',
       '',
       '',
       '',
       'PBK TERIMA' AS ''
FROM PBK A
  INNER JOIN MASTERFILE B ON A.NPWP2 = B.NPWP
WHERE YEAR(TANGGALDOC) = {tahun_pajak}
AND   A.KPP2 = B.KPP
AND   A.CABANG2 = B.CABANG;
    '''
    
    data = pd.read_sql(kueri,conn_awal)
    data.to_sql(f'{tahun_pajak}',con=conn_akhir,schema='data',index=False)
    
tahun = ['2022']    
for tahun_pajak in tahun:
    KueriUnion(tahun_pajak,mpninfokantor_conn,psql_conn)
    print(f'{tahun_pajak} done')