# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
from tkinter.filedialog import asksaveasfile 
import json
import codecs
from tkinter import ttk
from datetime import date

class App:
    def __init__(self, root, path):
        #setting title
        root.title("Latex Launcher")
        #setting window size
        width=350
        height=220
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        
        #Titres Colonnes
            #Mes Modèles
        LAB_MyModels=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        LAB_MyModels["font"] = ft
        LAB_MyModels["fg"] = "#333333"
        LAB_MyModels["justify"] = "center"
        LAB_MyModels["text"] = "Mes modèles"
        LAB_MyModels.grid(column=0, row=0)

        
            #Mon Document
        LAB_MonDoc=tk.Label(root)
        ft = tkFont.Font(family='Times',size=14)
        LAB_MonDoc["font"] = ft
        LAB_MonDoc["fg"] = "#333333"
        LAB_MonDoc["justify"] = "center"
        LAB_MonDoc["text"] = "Mon Document"
        LAB_MonDoc.grid(column=1, row=0, columnspan=2)

        #Liste des modèles
        self.LB_Models=tk.Listbox(root)
        self.LB_Models["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.LB_Models["font"] = ft
        self.LB_Models["fg"] = "#333333"
        self.LB_Models["justify"] = "center"
        self.LB_Models.grid(column=0, row=1, rowspan=5)

        #Config du document
            #Titre

        LAB_Titre=tk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Titre["font"] = ft
        LAB_Titre["fg"] = "#333333"
        LAB_Titre["justify"] = "center"
        LAB_Titre["text"] = "Titre"
        LAB_Titre.grid(column=1, row=1)

    
        self.docTitle = tk.StringVar()
        
        ENT_Titre=tk.Entry(root)
        ENT_Titre["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_Titre["font"] = ft
        ENT_Titre["fg"] = "#333333"
        ENT_Titre["justify"] = "center"
        ENT_Titre["text"] = self.docTitle
        ENT_Titre.grid(column=2, row=1)
        
            #Auteur
        LAB_Auteur=tk.Label(root)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Auteur["font"] = ft
        LAB_Auteur["fg"] = "#333333"
        LAB_Auteur["justify"] = "center"
        LAB_Auteur["text"] = "Auteur"
        LAB_Auteur.grid(column=1, row=2)

        self.docAuthor = tk.StringVar()
        
        ENT_Auteur=tk.Entry(root)
        ENT_Auteur["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_Auteur["font"] = ft
        ENT_Auteur["fg"] = "#333333"
        ENT_Auteur["justify"] = "center"
        ENT_Auteur["text"] = self.docAuthor
        ENT_Auteur.grid(column=2, row=2)

        #Boutons
            #Générer
        B_GENERER=tk.Button(root)
        B_GENERER["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_GENERER["font"] = ft
        B_GENERER["fg"] = "#000000"
        B_GENERER["justify"] = "center"
        B_GENERER["text"] = "Générer"
        B_GENERER.grid(column=1, row=3, columnspan=2, sticky="NSEW")
        B_GENERER["command"] = self.B_GENERER_command

            #Nouveau Modèle
        B_NEWMODEL=tk.Button(root)
        B_NEWMODEL["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_NEWMODEL["font"] = ft
        B_NEWMODEL["fg"] = "#000000"
        B_NEWMODEL["justify"] = "center"
        B_NEWMODEL["text"] = "Nouveau Modèle"
        B_NEWMODEL.grid(column=1, row=5, columnspan=2, sticky="NSEW")
        B_NEWMODEL["command"] = self.B_NEWMODEL_command

            #Editer
        B_EDIT=tk.Button(root)
        B_EDIT["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_EDIT["font"] = ft
        B_EDIT["fg"] = "#000000"
        B_EDIT["justify"] = "center"
        B_EDIT["text"] = "Editer"
        B_EDIT.grid(column=1, row=4, columnspan=2, sticky="NSEW")
        B_EDIT["command"] = self.B_EDIT_command

        #Importation des modèles
        self.datafile = path

        try:
            self.mem = self.loadFromJson()
        except(FileNotFoundError):
            self.generateEmptyDataFile()
            self.mem = self.loadFromJson()

        self.docTitle.set("New Document")
        self.docAuthor.set(self.mem["DefaultAuthor"])
            

    def B_GENERER_command(self):
        modelid = self.LB_Models.curselection()[0]
        model = self.mem["models"][modelid]
        title = self.docTitle.get()
        author = self.docAuthor.get()
        curdate = date.today()

        LaTexStr = ""

        LaTexStr += "\\documentclass["+model["documentclass"]["args"]+"]{"+model["documentclass"]["type"]+"}"+"\n"

        LaTexStr += model["packages"]
        LaTexStr += "\n\n"
        LaTexStr += model["commands"]
        LaTexStr += "\n\n"
        LaTexStr += "\\author{"+self.docAuthor.get()+"}"+"\n"
        LaTexStr += "\\title{"+self.docTitle.get()+"}"+"\n"
        LaTexStr += "\n\n"
        LaTexStr += "\\begin{document}\n\maketitle\n\nWRITE HERE\n\n\\end{document}"

        LaTexStr = LaTexStr.replace("§TITRE§",title)
        LaTexStr = LaTexStr.replace("§AUTEUR§",author)
        LaTexStr = LaTexStr.replace("§DATE§",str(curdate))

        print(LaTexStr)

        savePath = tk.filedialog.asksaveasfilename(filetypes=[("Tex file", ".tex")], defaultextension=".tex")
        with codecs.open(savePath,"w+", "utf-8") as f:
            f.write(LaTexStr)
            

    def B_NEWMODEL_command(self):
        #Création d'une sous-fenètre
        tl = tk.Toplevel()
        tl.title("Création de Model")
        tl.geometry("310x360")
        tl.resizable(width=True, height=True)

        #Config de la sous-fenètre

        LAB_Title =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Title["font"] = ft
        LAB_Title["fg"] = "#333333"
        LAB_Title["justify"] = "center"
        LAB_Title["text"] = "Model Title"
        LAB_Title.grid(column=0, row=0)

        modeleTitle = tk.StringVar()
        modeleTitle.set("New Model")
        
        ENT_Title=tk.Entry(tl)
        ENT_Title["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_Title["font"] = ft
        ENT_Title["fg"] = "#333333"
        ENT_Title["justify"] = "center"
        ENT_Title["text"] = modeleTitle
        ENT_Title.grid(column=1, row=0)
        

        LAB_Documentclass =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Documentclass["font"] = ft
        LAB_Documentclass["fg"] = "#333333"
        LAB_Documentclass["justify"] = "center"
        LAB_Documentclass["text"] = "DocumentClass"
        LAB_Documentclass.grid(column=0, row=1)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=1,ipadx=100)

        LAB_DocumentclassType =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_DocumentclassType["font"] = ft
        LAB_DocumentclassType["fg"] = "#333333"
        LAB_DocumentclassType["justify"] = "center"
        LAB_DocumentclassType["text"] = "Type"
        LAB_DocumentclassType.grid(column=0, row=2)

        docClassType = tk.StringVar()
        docClassType.set("report")
        
        ENT_docClassType=tk.Entry(tl)
        ENT_docClassType["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_docClassType["font"] = ft
        ENT_docClassType["fg"] = "#333333"
        ENT_docClassType["justify"] = "center"
        ENT_docClassType["text"] = docClassType
        ENT_docClassType.grid(column=1, row=2)

        LAB_DocumentclassType =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_DocumentclassType["font"] = ft
        LAB_DocumentclassType["fg"] = "#333333"
        LAB_DocumentclassType["justify"] = "center"
        LAB_DocumentclassType["text"] = "Args"
        LAB_DocumentclassType.grid(column=0, row=3)

        docClassArgs = tk.StringVar()
        docClassArgs.set("12pt,a4paper")
        
        ENT_docClassArgs=tk.Entry(tl)
        ENT_docClassArgs["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_docClassArgs["font"] = ft
        ENT_docClassArgs["fg"] = "#333333"
        ENT_docClassArgs["justify"] = "center"
        ENT_docClassArgs["text"] = docClassArgs
        ENT_docClassArgs.grid(column=1, row=3)

        LAB_Packages =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Packages["font"] = ft
        LAB_Packages["fg"] = "#333333"
        LAB_Packages["justify"] = "center"
        LAB_Packages["text"] = "Packages"
        LAB_Packages.grid(column=0, row=4)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=4,ipadx=100)

        T_Packages = tk.Text(tl, height = 5, width = 25)
        T_Packages.grid(column=0, row=5, columnspan=2,sticky="NSEW")
        T_Packages.insert("1.0","\\usepackage{amsmath}\n\\usepackage{amsfonts}\n\\usepackage{amssymb}\n\\usepackage{tcolorbox}")

        LAB_Commands =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Commands["font"] = ft
        LAB_Commands["fg"] = "#333333"
        LAB_Commands["justify"] = "center"
        LAB_Commands["text"] = "Commands"
        LAB_Commands.grid(column=0, row=6)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=6,ipadx=100)

        T_Commands = tk.Text(tl, height = 5, width = 25)
        T_Commands.grid(column=0, row=7, columnspan=2,sticky="NSEW")

        B_ADD=tk.Button(tl)
        B_ADD["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_ADD["font"] = ft
        B_ADD["fg"] = "#000000"
        B_ADD["justify"] = "center"
        B_ADD["text"] = "Ajouter"
        B_ADD.grid(column=0, row=8, columnspan=2, sticky="NSEW")

        def B_ADD_command():
            model = {}
            model["title"] = modeleTitle.get()
            model["documentclass"] = {}
            model["documentclass"]["type"] = docClassType.get()
            model["documentclass"]["args"] = docClassArgs.get()
            model["packages"] = T_Packages.get("1.0","end-1c")
            model["commands"] = T_Commands.get("1.0","end-1c")

            self.mem["models"].append(model)
            self.updateDataFile()
            self.loadFromJson()

            tl.destroy()
            tl.update()
        
        B_ADD["command"] = B_ADD_command


    def B_EDIT_command(self):
        modelid = self.LB_Models.curselection()[0]
        model = self.mem["models"][modelid]

                #Création d'une sous-fenètre
        tl = tk.Toplevel()
        tl.title("Création de Model")
        tl.geometry("310x390")
        tl.resizable(width=True, height=True)

        #Config de la sous-fenètre

        LAB_Title =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Title["font"] = ft
        LAB_Title["fg"] = "#333333"
        LAB_Title["justify"] = "center"
        LAB_Title["text"] = "Model Title"
        LAB_Title.grid(column=0, row=0)

        modeleTitle = tk.StringVar()
        modeleTitle.set(model["title"])
        
        ENT_Title=tk.Entry(tl)
        ENT_Title["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_Title["font"] = ft
        ENT_Title["fg"] = "#333333"
        ENT_Title["justify"] = "center"
        ENT_Title["text"] = modeleTitle
        ENT_Title.grid(column=1, row=0)
        

        LAB_Documentclass =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Documentclass["font"] = ft
        LAB_Documentclass["fg"] = "#333333"
        LAB_Documentclass["justify"] = "center"
        LAB_Documentclass["text"] = "DocumentClass"
        LAB_Documentclass.grid(column=0, row=1)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=1,ipadx=100)

        LAB_DocumentclassType =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_DocumentclassType["font"] = ft
        LAB_DocumentclassType["fg"] = "#333333"
        LAB_DocumentclassType["justify"] = "center"
        LAB_DocumentclassType["text"] = "Type"
        LAB_DocumentclassType.grid(column=0, row=2)

        docClassType = tk.StringVar()
        docClassType.set(model["documentclass"]["type"])
        
        ENT_docClassType=tk.Entry(tl)
        ENT_docClassType["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_docClassType["font"] = ft
        ENT_docClassType["fg"] = "#333333"
        ENT_docClassType["justify"] = "center"
        ENT_docClassType["text"] = docClassType
        ENT_docClassType.grid(column=1, row=2)

        LAB_DocumentclassType =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_DocumentclassType["font"] = ft
        LAB_DocumentclassType["fg"] = "#333333"
        LAB_DocumentclassType["justify"] = "center"
        LAB_DocumentclassType["text"] = "Args"
        LAB_DocumentclassType.grid(column=0, row=3)

        docClassArgs = tk.StringVar()
        docClassArgs.set(model["documentclass"]["args"])
        
        ENT_docClassArgs=tk.Entry(tl)
        ENT_docClassArgs["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=12)
        ENT_docClassArgs["font"] = ft
        ENT_docClassArgs["fg"] = "#333333"
        ENT_docClassArgs["justify"] = "center"
        ENT_docClassArgs["text"] = docClassArgs
        ENT_docClassArgs.grid(column=1, row=3)

        LAB_Packages =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Packages["font"] = ft
        LAB_Packages["fg"] = "#333333"
        LAB_Packages["justify"] = "center"
        LAB_Packages["text"] = "Packages"
        LAB_Packages.grid(column=0, row=4)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=4,ipadx=100)

        T_Packages = tk.Text(tl, height = 5, width = 25)
        T_Packages.grid(column=0, row=5, columnspan=2,sticky="NSEW")
        T_Packages.insert("1.0",model["packages"])

        LAB_Commands =tk.Label(tl)
        ft = tkFont.Font(family='Times',size=12)
        LAB_Commands["font"] = ft
        LAB_Commands["fg"] = "#333333"
        LAB_Commands["justify"] = "center"
        LAB_Commands["text"] = "Commands"
        LAB_Commands.grid(column=0, row=6)

        ttk.Separator(tl, orient='horizontal').grid(column=1,row=6,ipadx=100)

        T_Commands = tk.Text(tl, height = 5, width = 25)
        T_Commands.grid(column=0, row=7, columnspan=2,sticky="NSEW")
        T_Commands.insert("1.0",model["commands"])

        B_SAVE=tk.Button(tl)
        B_SAVE["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_SAVE["font"] = ft
        B_SAVE["fg"] = "#000000"
        B_SAVE["justify"] = "center"
        B_SAVE["text"] = "Sauvegarder"
        B_SAVE.grid(column=0, row=8, columnspan=2, sticky="NSEW")

        B_DEL=tk.Button(tl)
        B_DEL["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=12)
        B_DEL["font"] = ft
        B_DEL["fg"] = "#000000"
        B_DEL["justify"] = "center"
        B_DEL["text"] = "Supprimer"
        B_DEL.grid(column=0, row=9, columnspan=2, sticky="NSEW")


        def B_SAVE_command():
            model = {}
            model["title"] = modeleTitle.get()
            model["documentclass"] = {}
            model["documentclass"]["type"] = docClassType.get()
            model["documentclass"]["args"] = docClassArgs.get()
            model["packages"] = T_Packages.get("1.0","end-1c")
            model["commands"] = T_Commands.get("1.0","end-1c")

            self.mem["models"][modelid] = model
            self.updateDataFile()
            self.loadFromJson()

            tl.destroy()
            tl.update()

        def B_DEL_command():
            self.mem["models"].pop(modelid)
            self.updateDataFile()
            self.loadFromJson()

            tl.destroy()
            tl.update()
        
        B_SAVE["command"] = B_SAVE_command
        B_DEL["command"] = B_DEL_command


    def loadFromJson(self):
        with open(self.datafile,"r") as f:
            data = json.loads(f.read())

        self.LB_Models.delete(0,'end')
        for i in range(len(data["models"])):
            self.LB_Models.insert(i,data["models"][i]["title"])
    
        return data

    def updateDataFile(self):
        with open(self.datafile, "w") as f:
            f.write(json.dumps(self.mem))
            

    def generateEmptyDataFile(self):
        data = {}
        data["version"] = AppVersion
        data["dev"] = AppDev
        data["models"] = []
        data["DefaultAuthor"] = DefaultAuthor

        #Default Model
        model = {}
        model["title"] = "default"
        model["documentclass"] = {}
        model["documentclass"]["type"] = "report"
        model["documentclass"]["args"] = "12pt,a4paper"
        model["packages"] = "\\usepackage{amsmath}\n\\usepackage{amsfonts}\n\\usepackage{amssymb}\n\\usepackage{tcolorbox}"
        model["commands"] = "\\newtcolorbox{theoreme}[1]{colback=yellow!7!white,colframe=yellow!85!black,fonttitle=\\bfseries, coltitle=black, title=Théorême. \\underline{#1}}\n\\newtcolorbox{lemme}[1]{colback=yellow!7!white,colframe=yellow!85!black,fonttitle=\\bfseries, coltitle=black, title=Lemme. \\underline{#1}}"
        

        data["models"].append(model)
        

        with open(self.datafile, "a") as f:
            f.write(json.dumps(data))

if __name__ == "__main__":
    AppVersion = "1.0" #Ne pas modifier svp
    AppDev = "Eliot Poulette" #Ne pas modifier svp

    DefaultAuthor = "Eliot Poulette" #Mettez le nom le plus souvent utilisé sur vos documents

    print("LatexLauncher - ver{}".format(AppVersion))
    print("Les Balises §TITRE§, §AUTEUR§, §DATE§ seront remplacées dans le document généré")
    
    root = tk.Tk()
    app = App(root,"data")
    root.mainloop()
