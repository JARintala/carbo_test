from calculatorFolder.calculator import CattleFunctions as cf
from dataClasses.CarbonData import CarbonData
import numpy as np
import json

# -------------------------------------------------------------------------------
# LASKETAAN MUUN MAITOKARJAN TIEDOT
# -------------------------------------------------------------------------------

# Poimitaan ensimmäiset arvot Lypsikki-excelistä
# klk_pcs = 65  # Keskilehmäluku (lkm)                          averageCowCount
# up_p = 32  # Uudistusprosentti (%)                            renewalRate
# pv_d = 403.24  # Poikkimaväli (pv)                            averageCalvingInterval
# hk_d = (25.29 - 8) * 30  # Hiehokausi (kk -> pv)              periodOfStagnation
# vk_p = 6.16 / 100  # Vasikkakuoleisuus (% -> desimaali)       calfMortality

# Muodostetaan lista peruskarjatunnusluvuista
# pktl_list = [1, up_p, pv_d, hk_d] # basicCattleAttributes
class CalculatorService:
    def SaveCarbondata(self, carbonData: CarbonData):
        try:
            y = carbonData.cattleIndicatorsData
            basicCattleAttributesList = [  # pktl_list
                1,
                y.renewalRate,
                y.averageCalvingInterval,
                y.periodOfStagnation,
            ]

            # Muutetaan array muotoon
            basicCattleAttributesArray = np.array(basicCattleAttributesList)  # np_pktl

            # Lasketaan maitotilan koko karja
            # karja_lkm = cf.mkarjaluvut(basicCattleAttributesList, klk_pcs, vk_p)
            numberOfCows = cf.calculateDairyCattleCount(
                basicCattleAttributesList=basicCattleAttributesList,
                averageCowCount=y.averageCowCount,
                calfMortality=y.calfMortality,
            )

            # Seuraavaksi määritetään karjojen massat
            # lkp_kg = 647.35  # Lypsylehmän keskipaino (kg)
            # lkp_kg = float(req.params.get("lkp_kg"))
            # https://carbo-poc-functions.azurewebsites.net/api/HttpTrigger2?klk_pcs=65&up_p=32&pv_d=403.24&hk_d=25.29&vk_p=6.16&lkp_kg=647.35

            # Ajetaan Karjatiedot
            # karja_massa = cf.mkarjamassat(lkp_kg)
            massOfCattle = cf.calculateDairyCattleMassAndAttributes(
                averageWeightOfDairyCows=y.averageWeightOfDairyCows
            )

            # Lasketaan karjan massa, liha, typpi ja fosfori
            cattleCompleted = cf.calculateMassOfDairyCattleMeatNAndP(
                numberOfCows, massOfCattle
            )
            cattleGroups = [
                "Umpilehmat",
                "Syntyneet vasikat",
                "Pikkuvasikka",
                "Vasikat",
                "Hiehot",
                "Poistohiehot",
                "Poistoensikko",
                "Poistonuorilehma",
                "Poistovanhalehma",
                "Ensikko",
                "Sonnivasikka",
                "Myydyt vasikat",
            ]
            measures = [
                "lkm",
                "kokonaismassa (kg)",
                "liha (kg)",
                "typpi (kg)",
                "fosfori (kg)",
            ]

            d = {}
            # Adding a new key value
            for i in range(len(measures)):
                d.update({measures[i]: cattleCompleted[i].tolist()})
            d.update({"cattleGroups": cattleGroups})

            # Serializing json
            jsonObject = json.dumps(d, indent=4)

            return jsonObject

        except Exception as e:
            print(f"This HTTP triggered function failed: {e}.")
