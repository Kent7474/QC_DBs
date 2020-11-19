import main
import CONSTANTS

from tkinter import *
from tkinter import ttk
import os


class Surface:
    def __init__(self, master, ow_obj):
        # create empty database if it does not exist in the directory

        self.openworks = ow_obj

        leftFrame = Frame(width=150, height=600)
        leftFrame.grid(row=0, column=0, padx=10, pady=5, sticky=N)
        rightFrame = Frame(width=150, height=600)
        rightFrame.grid(row=0, column=1, padx=0, pady=5)

        # ------ LEFT FRAME ---------------
        # Label y nombre de archivo de  BSAS
        Label(leftFrame, text='BSAS File Name: ').grid(row=0, column=0, sticky=W + N)
        mystr_bsas = StringVar()
        mystr_bsas.set(self.openworks.ARCH_BSAS)
        self.name_bsas = Entry(leftFrame, textvariable=mystr_bsas, state=DISABLED, width=45)
        self.name_bsas.grid(row=0, column=1)

        # Label y nombre de archivos de NQN
        Label(leftFrame, text='NQN File Name: ').grid(row=1, column=0, sticky=W + N)
        mystr_nqn = StringVar()
        mystr_nqn.set(self.openworks.ARCH_NQN)
        self.name_nqn = Entry(leftFrame, textvariable=mystr_nqn, state=DISABLED, width=45)
        self.name_nqn.grid(row=1, column=1)

        # Button do_comparison
        self.comparisonDone = False
        self.docomparisonBtn = ttk.Button(leftFrame, text='Run', width=15, command=self.doComparison)
        self.docomparisonBtn.grid(row=2, column=1, sticky=W + N, pady=20)

        # LABELS DE RESULTADOS ///
        Label(leftFrame, text='RESULTADOS: ').grid(row=7, column=0, sticky=W + N, pady=5, padx=3)

        # Labels de totales
        Label(leftFrame, text='Total BSAS: ', fg='blue').grid(row=8, column=0, sticky=W + N)
        Label(leftFrame, text='Total NQN: ', fg='blue').grid(row=9, column=0, sticky=W + N)
        self.total_bsas = Entry(leftFrame, textvariable='', state=DISABLED, width=10)
        self.total_bsas.grid(row=8, column=1, sticky=W)
        self.total_nqn = Entry(leftFrame, textvariable='', state=DISABLED, width=10)
        self.total_nqn.grid(row=9, column=1, sticky=W)

        # Labels de resultados de comparacion
        Label(leftFrame, text=' ', fg='red').grid(row=10, column=0, sticky=W + N)
        Label(leftFrame, text='Pozos que no estan en BSAS -> ', fg='dark green').grid(row=11, column=0,
                                                                                      sticky=W + N)
        Label(leftFrame, text='Pozos que no estan en NQN -> ', fg='dark green').grid(row=12, column=0,
                                                                                     sticky=W + N)
        self.result_bsas = Entry(leftFrame, textvariable='', state=DISABLED, width=10)
        self.result_bsas.grid(row=11, column=1, sticky=W)
        self.result_nqn = Entry(leftFrame, textvariable='', state=DISABLED, width=10)
        self.result_nqn.grid(row=12, column=1, sticky=W)

        # Labels y nombres de archivos RESULTADOS
        Label(leftFrame, text=' ', fg='red').grid(row=13, column=0, sticky=W + N)
        Label(leftFrame, text='Datos guardados en: ').grid(row=14, column=0, sticky=W + N)
        self.result_arch_bsas = Entry(leftFrame, textvariable='', state=DISABLED, width=45)
        self.result_arch_bsas.grid(row=14, column=1, sticky=W)
        self.result_arch_nqn = Entry(leftFrame, textvariable='', state=DISABLED, width=45)
        self.result_arch_nqn.grid(row=15, column=1, sticky=W)

        # Boton export a base de datos
        self.expBtn = ttk.Button(leftFrame, text='Export to DB', state=DISABLED, width=15,
                                 command=self.addWellsToDB)
        self.expBtn.grid(row=16, column=0, sticky=W + N, pady=20)

        self.flechita_bsas = ttk.Button(leftFrame, text='Faltantes en bsas->', width=25, command=self.update_treeBsas)
        self.flechita_bsas.grid(row=16, column=1, sticky=E, pady=10)

        self.flechita_nqn = ttk.Button(leftFrame, text='Faltantes en nqn->', width=25, command=self.update_treeNqn)
        self.flechita_nqn.grid(row=17, column=1, sticky=E, pady=0)

        self.clear_treeBtn = ttk.Button(leftFrame, text='Clear table', width=25, command=self.clear_tree)
        self.clear_treeBtn.grid(row=18, column=1, sticky=E, pady=10)

        # -----------------------------------##
        # ------ RIGHT FRAME ---------------##

        # Mensaje ARRIBA del tree
        self.msg = Label(rightFrame, text='', fg='red')
        self.msg.grid(row=0, column=1, sticky=N)

        # Tree bsas
        self.tree = ttk.Treeview(rightFrame, show='headings', height=20, column=4, selectmode='browse')
        self.tree.grid(row=1, column=1, rowspan=20, pady=10, sticky=N)
        self.vsbv = ttk.Scrollbar(rightFrame, orient="vertical", command=self.tree.yview)
        self.vsbv.grid(row=1, column=2, sticky=N + S + E + W, rowspan=20)
        self.tree.configure(yscrollcommand=self.vsbv.set)

        self.tree["columns"] = ("zero", "one", "two", "three", "four", "five")
        self.tree.column("zero", width=30)
        self.tree.column("one", width=140)
        self.tree.column("two", width=140)
        self.tree.column("three", width=140)
        self.tree.column("four", width=140)
        self.tree.column("five", width=140)
        self.tree.heading("zero", text='n', anchor=N)
        self.tree.heading("one", text='UWI', anchor=N)
        self.tree.heading("two", text='WELL_LOCATION_UWI', anchor=N)
        self.tree.heading("three", text='WELL_UWI_TYPE', anchor=N)
        self.tree.heading("four", text='COMMON_WELL_NAME', anchor=N)
        self.tree.heading("five", text='WELL_LEASE_NAME', anchor=N)

        # Mensaje debajo del tree
        self.msg = Label(rightFrame, text='', fg='red')
        self.msg.grid(row=0, column=1, sticky=N)

        # Boton de pozos alternativos
        self.alternateBtn = ttk.Button(rightFrame, text='Alternative wells', width=15,
                                       command=self.alternativeWellsDialog)
        self.alternateBtn.grid(row=23, column=1, sticky=N)

        self.context_open = False

    def alternativeWellsDialog(self):
        try:
            self.wellSelection = self.tree.item(self.tree.selection()[0])['values']
            print(self.wellSelection)

            self.altWind = Tk()
            self.altWind.title("Alternative Wells")
            x = root.winfo_rootx() + 200
            y = root.winfo_rooty() + 50
            self.altWind.geometry('+%d+%d' % (x, y))

            # -----------------------------------##
            # ------ LEFT FRAME ---------------##

            leftFrameAlt = Frame(self.altWind, width=400, height=600)
            leftFrameAlt.grid(row=0, column=0, padx=10, pady=5, sticky=N)
            Label(leftFrameAlt, text="Seleccionar tipo de dato para buscar alternativas de pozos").grid(row=1, column=0,
                                                                                                        pady=10,
                                                                                                        sticky=W + E)
            # Opciones de fields
            fieldOption = ["UWI", "UWI", "WELL_LOCATION_UWI", "WELL_UWI_TYPE", "COMMON_WELL_NAME", "WELL_LEASE_NAME"]
            self.myStrOption = StringVar(leftFrameAlt)
            self.myStrOption.set(fieldOption[0])

            self.menuOpt = ttk.OptionMenu(leftFrameAlt, self.myStrOption, *fieldOption)
            self.menuOpt.grid(row=2, column=0, sticky=W)

            searchAlt = ttk.Button(leftFrameAlt, text='Search... ', width=15, command=self.searchAlternative)
            searchAlt.grid(row=2, column=0, sticky=E)

            self.fieldWell = Label(leftFrameAlt, text='', fg='red')
            self.fieldWell.grid(row=3, column=0, sticky=W, pady=10)

            # -----------------------------------##
            # ------ RIGHT FRAME ---------------##
            rightFrameAlt = Frame(self.altWind, width=400, height=600)
            rightFrameAlt.grid(row=0, column=1, padx=10, pady=5)

            # TREE TOP
            # Mensaje arriba del tree_alt_TOP
            self.msgAltTop = Label(rightFrameAlt, text='SERVIDOR DE BSAS', fg='green')
            self.msgAltTop.grid(row=0, column=0, sticky=N)

            self.tree_alt_TOP = ttk.Treeview(rightFrameAlt, show='headings', height=10, column=6, selectmode='browse')
            self.tree_alt_TOP.grid(row=1, column=0, rowspan=10, pady=10, sticky=N)
            vsbAltTOP = ttk.Scrollbar(rightFrameAlt, orient="vertical", command=self.tree_alt_TOP.yview)
            vsbAltTOP.grid(row=1, column=2, sticky=N + S + E + W, rowspan=20)
            self.tree_alt_TOP.configure(yscrollcommand=vsbAltTOP.set)

            self.tree_alt_TOP["columns"] = ("zero", "one", "two", "three", "four", "five")
            self.tree_alt_TOP.column("zero", width=40)
            self.tree_alt_TOP.column("one", width=140)
            self.tree_alt_TOP.column("two", width=140)
            self.tree_alt_TOP.column("three", width=140)
            self.tree_alt_TOP.column("four", width=140)
            self.tree_alt_TOP.column("five", width=140)
            self.tree_alt_TOP.heading("zero", text='ID', anchor=N)
            self.tree_alt_TOP.heading("one", text='UWI', anchor=N)
            self.tree_alt_TOP.heading("two", text='WELL_LOCATION_UWI', anchor=N)
            self.tree_alt_TOP.heading("three", text='WELL_UWI_TYPE', anchor=N)
            self.tree_alt_TOP.heading("four", text='COMMON_WELL_NAME', anchor=N)
            self.tree_alt_TOP.heading("five", text='WELL_LEASE_NAME', anchor=N)

            # TREE BOT
            # Mensaje arriba del tree_alt_BOT
            self.msgAltBot = Label(rightFrameAlt, text='SERVIDOR DE NQN', fg='blue')
            self.msgAltBot.grid(row=13, column=0, sticky=N)

            self.tree_alt_BOT = ttk.Treeview(rightFrameAlt, show='headings', height=10, column=6, selectmode='browse')
            self.tree_alt_BOT.grid(row=14, column=0, rowspan=10, pady=10, sticky=N)
            vsbAltBOT = ttk.Scrollbar(rightFrameAlt, orient="vertical", command=self.tree_alt_BOT.yview)
            vsbAltBOT.grid(row=14, column=2, sticky=N + S + E + W, rowspan=20)
            self.tree_alt_BOT.configure(yscrollcommand=vsbAltBOT.set)

            self.tree_alt_BOT["columns"] = ("zero", "one", "two", "three", "four", "five")
            self.tree_alt_BOT.column("zero", width=40)
            self.tree_alt_BOT.column("one", width=140)
            self.tree_alt_BOT.column("two", width=140)
            self.tree_alt_BOT.column("three", width=140)
            self.tree_alt_BOT.column("four", width=140)
            self.tree_alt_BOT.column("five", width=140)
            self.tree_alt_BOT.heading("zero", text='ID', anchor=N)
            self.tree_alt_BOT.heading("one", text='UWI', anchor=N)
            self.tree_alt_BOT.heading("two", text='WELL_LOCATION_UWI', anchor=N)
            self.tree_alt_BOT.heading("three", text='WELL_UWI_TYPE', anchor=N)
            self.tree_alt_BOT.heading("four", text='COMMON_WELL_NAME', anchor=N)
            self.tree_alt_BOT.heading("five", text='WELL_LEASE_NAME', anchor=N)

            # CONFIG PARA CUANDO SE CIERRA LA VENTANA NO SE TRULE
            self.config()
            self.altWind.protocol("WM_DELETE_WINDOW", self.config)

            self.altWind.mainloop()
        except IndexError:
            self.msg["fg"] = "red"
            self.msg["text"] = "Seleccionar un pozo del listado"

    def clearTreeAltDiag(self, tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def searchAlternative(self):
        # limpiar los 2 trees antes de completar
        self.clearTreeAltDiag(self.tree_alt_TOP)
        self.clearTreeAltDiag(self.tree_alt_BOT)

        # selection = Nombre del campo que se selecciona
        selection = self.myStrOption.get()
        # valueWell = el valor del campo que se selecciona
        valueWell = self.wellSelection[CONSTANTS.FIELD_NAMES.index(str(selection))]
        self.fieldWell["text"] = valueWell

        # listas de resultados
        bsasList = []
        nqnList = []

        self.openworks.likelyWells(str(valueWell), self.openworks.ARCH_BSAS, bsasList)
        self.openworks.likelyWells(str(valueWell), self.openworks.ARCH_NQN, nqnList)

        for x in bsasList:
            try:
                self.tree_alt_TOP.insert("", END, text="", values=(x[0], x[1], x[2], x[3], x[4], x[5]))
            except IndexError:
                print ("ERROR en el tree_alt_TOP.insert")

        for z in nqnList:
            try:
                self.tree_alt_BOT.insert("", END, text="", values=(z[0], z[1], z[2], z[3], z[4], z[5]))
            except IndexError:
                print("ERROR en el tree_alt_BOT.insert")

        print('Campo Seleccionado: ' + selection)
        print('Campo Value: ' + valueWell)
        print('lista bsas:', bsasList)
        print('lista nqn :', nqnList)

    def __myStr_results(self):
        # Asigna variables para mostrar en los Entry
        # Totales de archivos base
        mystr_total_nqn = StringVar()
        mystr_total_bsas = StringVar()
        mystr_total_nqn.set(len(self.openworks.list_uwi_nqn))
        mystr_total_bsas.set(len(self.openworks.list_uwi_bsas))
        self.total_bsas["textvariable"] = mystr_total_bsas
        self.total_nqn["textvariable"] = mystr_total_nqn
        # Totales resultados
        mystr_result_bsas = StringVar()
        mystr_result_nqn = StringVar()
        mystr_result_bsas.set(len(self.openworks.list_uwi_no_estan_bsas))
        mystr_result_nqn.set(len(self.openworks.list_uwi_no_estan_nqn))
        self.result_bsas["textvariable"] = mystr_result_bsas
        self.result_nqn["textvariable"] = mystr_result_nqn
        # Ruta de archivos de resultado
        mystr_result_arch_bsas = StringVar()
        mystr_result_arch_nqn = StringVar()
        mystr_result_arch_bsas.set(self.openworks.RESULT_BSAS)
        mystr_result_arch_nqn.set(self.openworks.RESULT_NQN)
        self.result_arch_bsas["textvariable"] = mystr_result_arch_bsas
        self.result_arch_nqn["textvariable"] = mystr_result_arch_nqn

    def doComparison(self):
        # Realizar la comparacion
        self.openworks.do_comparison()
        self.__myStr_results()

        self.docomparisonBtn["state"] = DISABLED
        self.expBtn["state"] = NORMAL
        self.msg["text"] = "DONE"
        self.comparisonDone = True

    def clear_tree(self):
        # Limpiar tree
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)

    def update_treeBsas(self):
        self.clear_tree()
        if os.path.exists(self.openworks.RESULT_BSAS):
            num = 1
            with open(self.openworks.RESULT_BSAS, "r") as file:
                for row in file:
                    self.tree.insert("", END, text="",
                                     values=(num, row.split(";")[1], row.split(";")[2], row.split(";")[3],
                                             row.split(";")[4], row.split(";")[5]))
                    num += 1
            # -----------------------------------------------------------
            # LEER DESDE LA BASE DE DATOS
            # conn = sqlite3.connect('data.db')
            # c = conn.cursor()
            # list = c.execute("SELECT * FROM bsas ORDER BY UWI DESC;")
            #
            # for row in list:
            #     self.tree.insert("", END, text="", values=(row[1], row[2], row[3], row[4], row[5]))
            #
            # conn.commit()
            # c.close()
            self.msg["text"] = "Datos del Servidor de Neuquen que faltan o se repiten en BSAS"
            self.msg["fg"] = "blue"
        else:
            self.msg["text"] = "No existe el archivo RESULTADOS de BSAS"

    def update_treeNqn(self):
        self.clear_tree()
        if os.path.exists(self.openworks.RESULT_NQN):
            num = 1
            with open(self.openworks.RESULT_NQN, "r") as file:
                for row in file:
                    self.tree.insert("", END, text="",
                                     values=(num, row.split(";")[1], row.split(";")[2], row.split(";")[3],
                                             row.split(";")[4], row.split(";")[5]))
                    num += 1
            self.msg["text"] = "Datos del Servidor de BSAS que faltan o se repiten en Neuquen"
            self.msg["fg"] = "blue"
        else:
            self.msg["text"] = "No existe el archivo RESULTADOS de BSAS"

    def addWellsToDB(self):
        try:
            self.openworks.add_wells_to_db()
        except IndexError:
            self.msg["text"] = "Error"

    def config(self):
        """Windows management Function"""
        if self.context_open:
            self.altWind.destroy()
            if os.path.exists(self.openworks.RESULT_BSAS) and os.path.exists(self.openworks.RESULT_NQN):
                self.expBtn.config(state=NORMAL)
            if not self.comparisonDone:
                self.docomparisonBtn.config(state=NORMAL)
            self.alternateBtn.config(state=NORMAL)
            self.flechita_nqn.config(state=NORMAL)
            self.flechita_bsas.config(state=NORMAL)
            self.clear_treeBtn.config(state=NORMAL)
            self.tree.config(selectmode="browse")
            root.protocol('WM_DELETE_WINDOW', root.destroy)
        else:
            root.protocol('WM_DELETE_WINDOW', lambda: 0)
            self.expBtn.config(state=DISABLED)
            self.docomparisonBtn.config(state=DISABLED)
            self.alternateBtn.config(state=DISABLED)
            self.flechita_nqn.config(state=DISABLED)
            self.flechita_bsas.config(state=DISABLED)
            self.clear_treeBtn.config(state=DISABLED)
            self.tree.config(selectmode="none")
        self.context_open = not self.context_open


if __name__ == '__main__':
    root = Tk()
    ow = main.OpenWorks()
    root.title('CALIDAD_DBs')
    application = Surface(root, ow)
    root.mainloop()
