import tkinter as tk
from tkinter import ttk, messagebox
import ttkthemes as themes # type: ignore
import flexion_pure_max
import flexion_pure_vérification
import flexion_pure_dimensionnement
import flexion_simple_max
import flexion_simple_vérification
import flexion_simple_dimensionnement
import threading
import time
import os
import sys
from utils import resource_path  # Au lieu de définir la fonction ici

class ModernApp:
    def __init__(self):
        self.root = themes.ThemedTk(theme="black")
        self.root.title("Calcul de Résistance des Profilés")
        self.root.geometry("900x900")
        
        # Configuration du style sombre
        self.style = ttk.Style()
        self.style.configure("Custom.TButton",
                           padding=10,
                           font=("Helvetica", 10))
        
        # Configuration des couleurs sombres
        self.root.configure(bg='#2b2b2b')
        self.style.configure("TFrame", background='#2b2b2b')
        self.style.configure("TLabelframe", background='#2b2b2b', foreground='white')
        self.style.configure("TLabelframe.Label", background='#2b2b2b', foreground='white')
        self.style.configure("TLabel", background='#2b2b2b', foreground='white')
        self.style.configure("TButton", background='#404040', foreground='white')
        
        # Configuration de la zone de texte des résultats
        self.style.configure("Result.TFrame", background='#363636')
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # En-tête
        self.header = ttk.Label(
            self.main_frame,
            text="Module Flexion Pure & Flexion simple",
            font=("Helvetica", 24)
        )
        self.header.pack(pady=20)
        
        # Choix de l'opération
        self.operation_frame = ttk.LabelFrame(self.main_frame, text="Type d'opération")
        self.operation_frame.pack(fill=tk.X, pady=10)
        
        self.operations = [
            "1: Flexion pure vérification",
            "2: Flexion pure Moment résistant max",
            "3: Flexion pure dimensionnement",
            "4: Flexion simple vérification",
            "5: Flexion simple (Effort et moment max)",
            "6: Flexion simple dimensionnement"
        ]
        
        self.operation_var = tk.StringVar()
        self.operation_combo = ttk.Combobox(
            self.operation_frame, 
            values=self.operations,
            textvariable=self.operation_var,
            state="readonly"
        )
        self.operation_combo.pack(pady=10, padx=10, fill=tk.X)
        self.operation_combo.bind('<<ComboboxSelected>>', self.on_operation_select)
        
        # Frame pour les inputs
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Paramètres")
        self.input_frame.pack(fill=tk.X, pady=10)
        
        # Variables pour les inputs
        self.profile_var = tk.StringVar()
        self.fy_var = tk.StringVar()
        self.appuis_var = tk.StringVar()
        self.lo_var = tk.StringVar()
        self.med_var = tk.StringVar()
        self.ved_var = tk.StringVar()
        self.section_trans_var = tk.StringVar()
        self.section_trans2_var = tk.StringVar()
        self.famille_profile_var = tk.StringVar()
        self.nature_var = tk.StringVar()
        self.effort_var = tk.StringVar()
        
        # Création des widgets (initialement cachés)
        self.create_input_widgets()
        
        # Ajout du loader
        self.loader_label = ttk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 10)
        )
        self.loader_label.pack(pady=5)
        
        # Bouton de calcul
        self.calc_button = ttk.Button(
            self.main_frame,
            text="Calculer",
            style="Custom.TButton",
            command=self.start_calculation
        )
        self.calc_button.pack(pady=20)
        
        # Zone de résultats
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Résultats")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(self.result_frame, height=10)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_input_widgets(self):
        # Création des widgets pour chaque paramètre
        self.inputs = {}
        
        # Profilé
        self.inputs['profile'] = self.create_input_row("Profilé:", self.profile_var)
        
        # Nuance d'acier
        self.inputs['fy'] = self.create_input_row("Nuance d'acier (S235/S275/S355):", self.fy_var)
        
        # Types d'appuis
        appuis_options = ["1: Articulé-Articulé", "2: Encastré-Articulé", 
                         "3: Encastré-Encastré", "4: Encastré-Libre"]
        self.inputs['appuis'] = self.create_combo_row("Types d'appuis:", 
                                                     self.appuis_var, appuis_options)
        
        # Longueur de la poutre
        self.inputs['lo'] = self.create_input_row("Longueur de la poutre (m):", self.lo_var)
        
        # Moment fléchissant
        self.inputs['med'] = self.create_input_row("Moment fléchissant M_Ed (N.m):", self.med_var)
        
        # Effort tranchant
        self.inputs['ved'] = self.create_input_row("Effort tranchant V_Ed (N):", self.ved_var)
        
        # Section transversale
        section_trans_options = ["1: Section en I laminées", "2: Section en I soudées", "3: Autres section"]
        self.inputs['section_trans'] = self.create_combo_row("Type de section transversale:", 
                                                            self.section_trans_var,
                                                            section_trans_options)
        
        # Section transversale 2
        section_trans2_options = ["1: Section en I et H", "2: Profil en U laminés", "3: Pour les cornière"]
        self.inputs['section_trans2'] = self.create_combo_row("Type de section transversale 2:", 
                                                             self.section_trans2_var,
                                                             section_trans2_options)
        
        # Famille de profilé
        famille_options = ["1: IPE", "2: IPN", "3: UPE", "4: UPN", "5: HE", "6: L","7: HL", "8: HD", "9: HP","10: U"]
        self.inputs['famille_profile'] = self.create_combo_row("Famille de profilé:", 
                                                              self.famille_profile_var,
                                                              famille_options)
        
        # Ajouter les nouveaux menus déroulants
        nature_options = ["1: Laminé", "0: Reconstitué"]
        self.inputs['nature'] = self.create_combo_row(
            "Type de profilé:", 
            self.nature_var,
            nature_options
        )
        
        effort_options = ["1: Effort tranchant parallèle à l'âme", "2: Parallèle aux semelles"]
        self.inputs['effort'] = self.create_combo_row(
            "Direction de l'effort:", 
            self.effort_var,
            effort_options
        )

    def create_input_row(self, label_text, variable):
        frame = ttk.Frame(self.input_frame)
        label = ttk.Label(frame, text=label_text)
        entry = ttk.Entry(frame, textvariable=variable)
        
        label.pack(side=tk.LEFT, padx=5)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        return frame
        
    def create_combo_row(self, label_text, variable, options):
        frame = ttk.Frame(self.input_frame)
        label = ttk.Label(frame, text=label_text)
        combo = ttk.Combobox(frame, textvariable=variable, values=options, state="readonly")
        
        label.pack(side=tk.LEFT, padx=5)
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        return frame
        
    def on_operation_select(self, event=None):
        # Masquer tous les widgets
        for widget in self.inputs.values():
            widget.pack_forget()
            
        # Afficher les widgets nécessaires selon l'opération sélectionnée
        operation = self.operation_combo.current() + 1
        
        # Afficher les widgets communs
        self.inputs['fy'].pack(fill=tk.X, pady=5)
        self.inputs['appuis'].pack(fill=tk.X, pady=5)
        self.inputs['lo'].pack(fill=tk.X, pady=5)
        
        # Afficher les widgets spécifiques selon l'opération
        if operation in [1, 2, 4, 5]:
            self.inputs['profile'].pack(fill=tk.X, pady=5)
        
        if operation in [1, 3, 4, 6]:
            self.inputs['med'].pack(fill=tk.X, pady=5)
        
        if operation in [4, 6]:
            self.inputs['ved'].pack(fill=tk.X, pady=5)
        
        if operation in [4, 5, 6]:
            self.inputs['section_trans2'].pack(fill=tk.X, pady=5)
            # Ajouter un gestionnaire d'événements pour section_trans2
            self.section_trans2_var.trace_add('write', self.on_section_trans2_change)
        
        if operation in [1, 2, 3, 4, 5, 6]:
            self.inputs['section_trans'].pack(fill=tk.X, pady=5)
        
        if operation in [3, 6]:
            self.inputs['famille_profile'].pack(fill=tk.X, pady=5)
        
        # Réinitialiser les variables
        self.section_trans2_var.set('')
        self.nature_var.set('')
        self.effort_var.set('')
        
    def on_section_trans2_change(self, *args):
        # Vérifier si section_trans2 est sélectionné et non vide
        if self.section_trans2_var.get():
            try:
                if int(self.section_trans2_var.get().split(':')[0]) == 1:
                    self.inputs['nature'].pack(fill=tk.X, pady=5)
                    # Ajouter un gestionnaire d'événements pour nature
                    self.nature_var.trace_add('write', self.on_nature_change)
                else:
                    self.inputs['nature'].pack_forget()
                    self.inputs['effort'].pack_forget()
            except (ValueError, IndexError):
                pass

    def on_nature_change(self, *args):
        # Vérifier si nature est sélectionné
        if self.nature_var.get():
            try:
                if self.nature_var.get().startswith('0'):  # Si reconstitué
                    self.inputs['effort'].pack(fill=tk.X, pady=5)
                else:
                    self.inputs['effort'].pack_forget()
            except (ValueError, IndexError):
                pass
    
    def show_loader(self):
        self.calc_button.configure(state='disabled')
        self.loader_label.configure(text="Calcul en cours...")
        self.root.update()
    
    def hide_loader(self):
        self.calc_button.configure(state='normal')
        self.loader_label.configure(text="")
        self.root.update()
    
    def start_calculation(self):
        # Démarrer le calcul dans un thread séparé
        thread = threading.Thread(target=self.threaded_calculate)
        thread.start()
    
    def threaded_calculate(self):
        try:
            self.show_loader()
            
            # Exécuter le calcul
            result = self.calculate()
            
            # Mettre à jour l'interface avec les résultats
            self.root.after(0, self.update_results, result)
            
        except Exception as error:
            self.root.after(0, lambda err=error: messagebox.showerror("Erreur", str(err)))
        finally:
            self.root.after(0, self.hide_loader)
    
    def update_results(self, result):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, str(result))
    
    def calculate(self):
        try:
            operation = self.operation_combo.current() + 1
            
            # Récupérer les valeurs communes
            fy = int(self.fy_var.get().replace('S', ''))
            appuis = int(self.appuis_var.get().split(':')[0])
            lo = float(self.lo_var.get())
            
            # Pour les sections transversales, extraire le numéro
            section_trans = int(self.section_trans_var.get().split(':')[0]) if self.section_trans_var.get() else 1
            section_trans2 = int(self.section_trans2_var.get().split(':')[0]) if self.section_trans2_var.get() else 1
            
            # Pour la famille de profilé
            famille_profile = int(self.famille_profile_var.get().split(':')[0]) if self.famille_profile_var.get() else 1
            
            # Pour les opérations nécessitant le type de profilé
            nature = int(self.nature_var.get().split(':')[0]) if self.nature_var.get() else 1
            effort_direction = int(self.effort_var.get().split(':')[0]) if self.effort_var.get() else 1
            
            # Effectuer le calcul selon l'opération
            if operation == 1:
                if not all([self.profile_var.get(), self.med_var.get()]):
                    raise ValueError("Veuillez remplir tous les champs requis")
                profile = self.profile_var.get()
                M_Ed = float(self.med_var.get())
                result = flexion_pure_vérification.flexion_pure_vérification(
                    M_Ed, profile, fy, appuis, lo, section_trans
                )
            elif operation == 2:
                if not self.profile_var.get():
                    raise ValueError("Veuillez entrer un profilé")
                profile = self.profile_var.get()
                result = flexion_pure_max.flexion_pure_max(
                    profile, fy, appuis, lo, section_trans
                )
                result = f"La résistance maximale est : {result} N.m pour le profilé choisi"
            elif operation == 3:
                if not self.med_var.get():
                    raise ValueError("Veuillez entrer un moment fléchissant")
                M_Ed = float(self.med_var.get())
                result = flexion_pure_dimensionnement.flexion_pure_dimensionnement(
                    famille_profile, M_Ed, fy, appuis, lo, section_trans
                )
            elif operation == 4:
                if not all([self.profile_var.get(), self.med_var.get(), self.ved_var.get()]):
                    raise ValueError("Veuillez remplir tous les champs requis")
                profile = self.profile_var.get()
                M_Ed = float(self.med_var.get())
                Ved = float(self.ved_var.get())
                
                # Récupérer les valeurs de nature et effort_direction si nécessaire
                if section_trans2 == 1:
                    nature = int(self.nature_var.get().split(':')[0]) if self.nature_var.get() else 1
                    effort_direction = int(self.effort_var.get().split(':')[0]) if self.nature_var.get().startswith('0') else 1
                else:
                    nature = 1
                    effort_direction = 1
                
                result = flexion_simple_vérification.flexion_simple_vérification(
                    M_Ed, Ved, profile, fy, appuis, lo, 
                    section_trans, section_trans2,
                    nature=nature,
                    effort_direction=effort_direction
                )
            elif operation == 5:
                if not self.profile_var.get():
                    raise ValueError("Veuillez entrer un profilé")
                profile = self.profile_var.get()
                [M_Rd, Vpl_Rd] = flexion_simple_max.flexion_simple_max(
                    profile, fy, appuis, lo, section_trans, section_trans2,
                    nature=nature, effort_direction=effort_direction
                )
                result = f"Pour le profilé {profile}:\n"
                result += f"Moment résistant maximal (M_Rd): {M_Rd:.2f} N.m\n"
                result += f"Effort tranchant maximal (Vpl_Rd): {Vpl_Rd:.2f} N"
            elif operation == 6:
                if not all([self.med_var.get(), self.ved_var.get()]):
                    raise ValueError("Veuillez remplir tous les champs requis")
                M_Ed = float(self.med_var.get())
                Ved = float(self.ved_var.get())
                result = flexion_simple_dimensionnement.flexion_simple_dimensionnement(
                    famille_profile, M_Ed, Ved, fy, appuis, lo, section_trans, section_trans2
                )
            
            return result  # Retourner le résultat au lieu de l'afficher directement
            
        except ValueError as e:
            raise ValueError(str(e) if str(e) else "Veuillez vérifier les valeurs entrées")
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernApp()
    app.run() 