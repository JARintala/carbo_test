import logging
import azure.functions as func
import numpy as np
import json


# see e.g. https://github.com/kmt112/A2Ztutorial
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        # -------------------------------------------------------------------------------
        # LASKETAAN MAIDONTUOTANTO
        # -------------------------------------------------------------------------------

        # Poimitaan tarvittavat syöttöarvot excelistä
        # klk_pcs = 65             # Keskilehmäluku (lkm)
        # pv_d = 403.24                # Poikkimaväli (pv)
        # uok = 66.21                 # Ummessaolokausi (pv)
        # milk_a = 10138.89              # Maitotuotos (kg/lehmä/pv)
        # fat_p = 4.41 * 10         # Rasvapitoisuus (% -> g/kg)
        # prot_p = 3.59 * 10        # Proteiinipitoisuus (% -> g/kg)
        # lact_p = 4.68 * 10        # Laktoosipitoisuus (% -> g/kg)
        # meijeri_m = 95.15 / 100    # Meijerimaito-osuus (% -> desimaali)

        klk_pcs = float(req.params.get("klk_pcs"))
        pv_d = float(req.params.get("pv_d"))
        uok = float(req.params.get("uok"))
        milk_a = float(req.params.get("milk_a"))
        fat_p = float(req.params.get("fat_p")) * 10
        prot_p = float(req.params.get("prot_p")) * 10
        lact_p = float(req.params.get("lact_p")) * 10
        meijeri_m = float(req.params.get("meijeri_m")) / 100
        # https://carbo-poc-functions.azurewebsites.net/api/milk-production?klk_pcs=65&pv_d=403.24&uok=66.21&milk_a=10138.89&fat_p=4.41&prot_p=3.59&lact_p=4.68&meijeri_m=95.15

        maitotuotos = mmaito(
            klk_pcs, pv_d, uok, milk_a, fat_p, prot_p, lact_p, meijeri_m
        )
        production_groups = [
            "Paivatuotos per lehma",
            "Vuosituotos",
            "Myyty vuosituotos",
        ]
        measures = [
            "Raakamaito (kg)",
            "EKM(kg)",
            "RPKM(kg)",
            "Rasva (kg)",
            "Proteiini (kg)",
            "Laktoosi (kg)",
            "Typpi (kg)",
            "Fosfori (kg)",
            "Kuiva-aine (kg)",
            "Kalorit (kcal)",
        ]

        d = {}
        # Adding a new key value pair
        for i in range(len(production_groups)):
            d.update({production_groups[i]: maitotuotos[i].tolist()})
        d.update({"measures": measures})

        # Serializing json
        json_object = json.dumps(d, indent=4)
        return func.HttpResponse(json_object)

    except Exception as e:
        return func.HttpResponse(f"This HTTP triggered function failed: {e}.")
