import CONSTANTS
from time import time
from datetime import date
import os
import sqlite3

init_time = time()
day = str(date.today())


class OpenWorks:
    list_uwi_bsas = []
    list_uwi_no_estan_nqn = []
    list_uwi_nqn = []
    list_uwi_no_estan_bsas = []

    ARCH_BSAS = "Archivos_Bases/OW_BSAS_Neuquina_Headers.txt"
    ARCH_NQN = "Archivos_Bases/OW_NQN_Neuquina_Headers.txt"
    RESULT_BSAS = f"Resultados/no_estan_en_BSAS-{day}.txt"
    RESULT_NQN = f"Resultados/no_estan_en NQN-{day}.txt"

    def __init__(self):
        if not os.path.exists('data.db'):
            print('Create database... ')
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE bsas (WELL_ID , UWI , WELL_LOCATION_UWI , WELL_UWI_TYPE , COMMON_WELL_NAME , "
                        "WELL_LEASE_NAME , ELEV_TYPE , ELEVATION , TOTAL_DEPTH , X_COORDINATE , Y_COORDINATE , "
                        "FIELD , STATE , COUNTY , OPERATOR , SPUD_DATE , WELL_NUMBER , GOVERN_AREA , BASIN , INTERP , "
                        "REMARK , DRILLING_OPERATOR);")
            cur.execute("CREATE TABLE nqn (WELL_ID , UWI , WELL_LOCATION_UWI , WELL_UWI_TYPE , COMMON_WELL_NAME , "
                        "WELL_LEASE_NAME , ELEV_TYPE , ELEVATION , TOTAL_DEPTH , X_COORDINATE , Y_COORDINATE , "
                        "FIELD , STATE , COUNTY , OPERATOR , SPUD_DATE , WELL_NUMBER , GOVERN_AREA , BASIN , INTERP , "
                        "REMARK , DRILLING_OPERATOR);")
            con.commit()
            con.close()
            if os.path.exists('data.db'):
                print('Done.')
        else:
            print('Database already exist...')

    # Metodos encapsulados, solo se pueden utilizar dentro de la clase.
    def __append_uwis(self, ARCH, LIST, WELL_ID):
        """Crea una lista con todos los uwis del archivo. Ignora los wells id descartados"""
        with open(ARCH, "r", errors='ignore') as file:
            for line in file:
                if line.split(';')[CONSTANTS.WELL_ID] not in WELL_ID:
                    LIST.append(line.split(';')[CONSTANTS.UWI])
        print(ARCH, len(LIST))
        print(LIST[0:8], '...', end='\n\n')

    def __list_diff(self, list_uwi_1, list_uwi_2, list_diff, REGIONAL):
        """ Genera una lista DIFF con los uwis que estan en list_uwi_1 pero no en list_uwi_2"""
        assert len(list_uwi_1) > 0 and len(list_uwi_2) > 0, "UNA DE LAS LISTAS ESTA VACIA"
        for i in list_uwi_1:
            if i not in list_uwi_2:
                list_diff.append(i)
        print(f'Total de UWIS que no estan en {REGIONAL}: ', '-->', len(list_diff))

    def __resutls(self, ARCH, RESULT, LIST_NE):
        """Genera un txt con los registros de pozos faltantes"""
        assert len(LIST_NE) > 0, "Lista de diferencia vacia"
        with open(ARCH, 'r', errors='ignore') as file, open(RESULT, 'w', errors='ignore') as result:
            # result.write(CONSTANTS.WELL_HEADER)
            for line in file:
                if line.split(';')[CONSTANTS.UWI] in LIST_NE:
                    result.write(line)
        print(f"Datos guardados en el archivo: {RESULT}")

    # Ejecucion de los metodos encapsulados
    # Agregar los uwis a las listas
    def append_BsasNqn(self):
        """Crea una lista con todos los uwis de BSAS. Ignora los wells id descartados
        Crea una lista con todos los uwis de NQN. Ignora los wells id descartados"""
        self.__append_uwis(self.ARCH_BSAS, self.list_uwi_bsas, CONSTANTS.WELL_ID_DISMISS_BSAS)
        self.__append_uwis(self.ARCH_NQN, self.list_uwi_nqn, CONSTANTS.WELL_ID_DISMISS_NQN)

    # Sacar la diferencias de cada lista
    def diff_BsasNqn(self):
        """ Los uwis de BSAS que no esten en NQN, se guardan en list_uwi_no_estan_nqn
        Los uwis de NQN que no esten en BSAS, se guardan en list_uwi_no_estan_bsas"""
        self.__list_diff(self.list_uwi_bsas, self.list_uwi_nqn, self.list_uwi_no_estan_nqn, 'BSAS')
        self.__list_diff(self.list_uwi_nqn, self.list_uwi_bsas, self.list_uwi_no_estan_bsas, 'NQN')

    # Escribir los resultados de las diferencias en los archivos RESULT
    def result_BsasNqn(self):
        """Escribe los regitros de loz pozos que no estan en BSAS en el archivo RESULT_BSAS.
        Escribe los regitros de loz pozos que no estan en NQN en el archivo RESULT_NQN."""
        self.__resutls(self.ARCH_NQN, self.RESULT_BSAS, self.list_uwi_no_estan_bsas)
        self.__resutls(self.ARCH_BSAS, self.RESULT_NQN, self.list_uwi_no_estan_nqn)

    # Ejecuta los tres pasos para realizar la comparacion de pozos.
    def do_comparison(self):
        self.append_BsasNqn()
        self.diff_BsasNqn()
        self.result_BsasNqn()

    # Agrega los resultados a la base de datos.
    def add_wells_to_db(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        with open(self.RESULT_NQN, 'r') as file_nqn:
            for i in file_nqn:
                cur.execute("INSERT INTO nqn VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", i.split(';'))

        with open(self.RESULT_BSAS, 'r') as file_bsas:
            for k in file_bsas:
                cur.execute("INSERT INTO bsas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", k.split(';'))

        conn.commit()
        cur.close()

        print(' Exportado a Base de Datos')

    # Busca en todos los campos el 'data'
    def likelyWells(self, data, base, lista):
        with open(base, 'r', encoding='utf-8') as arch:
            try:
                for line in arch:
                    for i in range(1, 6):
                        if data == line.split(';')[i]:
                            lista.append(line.split(';')[0:6])
                            break
            except UnicodeDecodeError:
                print('utf-8 error...')

