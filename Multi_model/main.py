 
import pandas as pd

from Jauge import Jauge
from .Model_folder.RL import RL
from .Model_folder.GR4J import GR4J
from Choix import Choix
from Pre_process import Pre_Process
from Post_process import Outputs

import os
from os.path import dirname, abspath

def main():
    #root_directory = dirname(dirname(abspath(__file__))) #AAAAAAAAAAAAAAAAAAAAA
    id = "CAMELS_FR_tsd_J001401001"
    nom = "Nancon"
    dossier = "C:\\Users\\enzma\\Documents\\rennes 1\\M2\\Semestre 2\\Stage\\codes_matlab_resev_lin\\stations"
    fichier = "CAMELS_FR_tsd_J001401001.csv"
    bv = Jauge(id, nom, dossier, fichier)

    watershed = Pre_Process(
        example_path=r"C:\Users\enzma\Documents\HydroModPy\Enzo",
        data_path=r"C:\Users\enzma\Documents\HydroModPy\Enzo\data",
        results_path=r"C:\Users\enzma\Documents\HydroModPy\Enzo\results",
        basin_name=nom,
        x=389285.910,
        y=6816518.749,
        dem_raster=r"C:\Users\enzma\Documents\HydroModPy\Enzo\data\regional dem.tif",
        hydrometry_csv=r"hydrometry catchment Nancon.csv",
        year_start=1990,
        year_end=2021,
        example_year=2020
    )

    watershed.pre_processing()

    fct_calib = "crit_NSE"

    transfo = [""]
    dict_crit = {"crit_NSE": 0.5,"crit_KGE": 0.5}

    # TODO prévoir des limites pour l'utilisateur : t_calib_start < t_calib_end etc
    t_calib_start = "2005-01-01"
    #t_calib_start = "2000-01-01"
    t_calib_end = "2005-01-10"
    t_calib_end = "2010-12-31"
    t_valid_start = "2010-01-01"
    t_valid_end = "2020-12-31"
    t_prev_start = "2021-01-01"
    t_prev_end = "2021-12-31"

    mac = Choix()
    """
    model1 = RL(t_calib_start, t_calib_end, t_valid_start, t_valid_end, t_prev_start, t_prev_end, transfo, fct_calib)
    model1.param_calib(bv)
    print("\n=== Résultats du modèle de Résevoir linéaire (RL) ===")
    print(f"  Alpha      : {model1.alpha}")
    print(f"  Vmax       : {model1.Vmax}")
    print(f"  {fct_calib} Calib  : {model1.crit_calib:.4f}")
    print(f"  {fct_calib} Valid  : {model1.crit_valid:.4f}")
    print("===============================\n")
    mac.add_model(model1)
    """
    model2 = GR4J(t_calib_start, t_calib_end, t_valid_start, t_valid_end, t_prev_start, t_prev_end, transfo, fct_calib)
    model2.param_calib(bv)
    print("\n=== Résultats du modèle GR4J ===")
    print(f"{fct_calib} calibration : {model2.crit_calib:.4f}")
    print(f"{fct_calib} validation : {model2.crit_valid:.4f}")
    print("Paramètres calibrés :")
    for i, val in enumerate(model2.x, start=1):
        print(f"  X{i} : {val}")
    print("===============================\n")
    mac.add_model(model2)
    
    try :
        best = mac.comparaison_models(fct_calib)

        d, Q_sim = best.prevision(bv)

        result = Outputs(id,nom,d,Q_sim)
        result.affiche()

        result_compar = Outputs(id,nom,d,Q_sim,bv.serie_debit(t_prev_start,t_prev_end))
        result_compar.affiche()

    except ValueError as e :
        print(f"Erreur lors de la sélection du modèle : {e}")
    
if __name__ == "__main__":
    main()