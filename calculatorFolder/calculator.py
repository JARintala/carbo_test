import numpy as np

# -------------------------------------------------------------------------------
# Name:        mkarjaluvut
# Purpose:     Laskee maitokarjamäärän tunnusluvuista
# -------------------------------------------------------------------------------
class CattleFunctions:
    def calculateDairyCattleCount(
        basicCattleAttributesList, averageCowCount, calfMortality
    ):  # Syötteenä: Karjatunnuslista, Lehmälkm, Vasikkakuoleisuus

        # Järjestys: Intercept, Uudistuprosentti, Poikkimaväli, Hiehokausi
        karja_factor_list = [
            [8.7934300e00, -6.695000e-02, -2.050000e-03, 2.970000e-03],  # Umpilehmät
            [
                7.0046910e01,
                2.075900e-01,
                -5.460000e-02,
                -1.510000e-03,
            ],  # Syntyneet vasikat
            [
                2.8687400e00,
                2.464000e-01,
                -3.170000e-03,
                0.000000e00,
            ],  # Pikkuvasikat (N)
            [-1.915150e00, 2.851200e-01, 1.030000e-03, 0.000000e00],  # Vasikat (N)
            [-1.957733e01, 5.867800e-01, 4.828000e-02, 0.000000e00],  # Hiehot
            [-6.372000e-02, 5.808000e-02, -5.918000e-06, 3.333000e-05],  # Poistohieho
            [-8.768440e00, 2.959000e-01, 5.560000e-03, 4.444000e-05],  # Poistoensikko
            [
                -7.474920e00,
                3.589300e-01,
                5.510000e-03,
                1.111100e-04,
            ],  # Poistonuorilehmä
            [
                1.5776750e01,
                -1.331000e-01,
                -1.177000e-02,
                0.0001000000,
            ],  # Poistovanhalehmä
        ]

        # Muutetaan array muotoon

        np_karja_factor = np.array(karja_factor_list)

        # Lasketaan Tuloskertoimet
        np_karja_factor_result = basicCattleAttributesList * np_karja_factor
        np_karja_factor_result_sum = np.array(
            list(map(sum, np_karja_factor_result))
        ) / np.array(50)

        # Kerrotaan lehmälukumäärällä ja saadaan karjalukumäärät
        np_y = np.array([averageCowCount])
        np_karja_lkm = np_karja_factor_result_sum * np_y

        # Otetaan huomioon vasikkakuoleisuus kertomalla vasikoiden lkm kuoleisuudella
        np_karja_lkm[1] = np_karja_lkm[1] * (1 - calfMortality)
        np_karja_lkm_vk = np_karja_lkm

        # Lasketaan loput karjat (ensikot,sonnivasikat, myydyt vasikat)
        ensikot = (basicCattleAttributesList[1] / 100) * averageCowCount
        sonnivasikat = np_karja_lkm_vk[1] / 2
        myydytvasikat = np_karja_lkm_vk[1] - sonnivasikat - np_karja_lkm_vk[3]
        np_ensikot_sonnivasikat = np.array([ensikot, sonnivasikat, myydytvasikat])

        # Lisätään nämä arrayn loppuun
        np_karja_lkm_all = np.append(np_karja_lkm_vk, np_ensikot_sonnivasikat)

        # Palautetaan kaikki karjamäärät
        return np_karja_lkm_all

    # -------------------------------------------------------------------------------
    # Name:        mkarjamassat
    # Purpose:     Lasketaan maitokarjan keskimääräiset painot ja muut tiedot
    # -------------------------------------------------------------------------------

    def calculateDairyCattleMassAndAttributes(
        averageWeightOfDairyCows,
    ):  # Syötteenä Lypsylehmän keskipaino
        # Järjestys: factor, intercept
        karja_factor_list = [
            [1.000000, 0.000000],  # Umpilehmät
            [-0.00304, 43.71216],  # Syntyneet vasikat
            [-0.00304, 43.71216],  # Pikkuvasikat (N)
            [-0.66434, 619.3451],  # Vasikat (N)
            [1.571189, -514.8519],  # Hiehot
            [1.571189, -514.8519],  # Poistohieho
            [0.619233, 174.4333],  # Poistoensikko
            [0.790163, 94.78435],  # Poistonuorilehmä
            [1.000000, 0.000000],  # Poistovanhalehmä
            [0.619233, 174.4333],  # Ensikko
            [-0.02501, 60.08306],  # Sonnivasikka
            [-0.66434, 619.3451],  # Myydyt vasikat
        ]

        # Muutetaan kaikki array-muotoon

        np_x = np.array([averageWeightOfDairyCows])
        np_karja_factor = np.array(karja_factor_list)

        # Kerrotaan factor lehmäpainolla
        np_karja_factor[:, 0] = np_karja_factor[:, 0] * np_x
        np_karja_new_factor = np_karja_factor

        # Summataan tulos ja intercept
        karjamassa = list(map(sum, np_karja_factor))
        np_karjamassa = np.array(karjamassa)

        return np_karjamassa

    # -------------------------------------------------------------------------------
    # Name:        mliha_n_p
    # Purpose:     Lasketaan maitokarjan kokonaismassa, -liha, N ja P
    # -------------------------------------------------------------------------------

    def calculateMassOfDairyCattleMeatNAndP(
        numberOfCows, massOfCattle
    ):  # Syötteenä karjaluvut ja karjamassa
        # Lasketaan kokonaismassa
        mmassa = numberOfCows * massOfCattle

        # Lasketaan lihamassa
        mliha = mmassa * 0.25

        # Määritetään karjan N ja P pitoisuudet
        karja_N_P_list = [
            [0.0232, 0.0065],  # Umpilehmät
            [0.0320, 0.0080],  # Syntyneet vasikat
            [0.0320, 0.0080],  # Pikkuvasikat (N)
            [0.0304, 0.0078],  # Vasikat (N)
            [0.0272, 0.0703],  # Hiehot
            [0.0272, 0.0703],  # Poistohieho
            [0.0256, 0.0070],  # Poistoensikko
            [0.0240, 0.0067],  # Poistonuorilehmä
            [0.0232, 0.0065],  # Poistovanhalehmä
            [0.0256, 0.0070],  # Ensikko
            [0.0304, 0.0078],  # Sonnivasikka
            [0.0304, 0.0078],  # Myydyt vasikat
        ]

        # Lasketaan N ja P karjassa

        np_N_P = np.array(karja_N_P_list)
        np_mkarja_N = np_N_P[:, 0] * np.array(mmassa)
        np_mkarja_P = np_N_P[:, 1] * np.array(mmassa)

        # Yhdistetään lkm, massa, lihamassa, N ja P yhteen array -muotoon
        np_mkarja_completed = np.concatenate(
            [[numberOfCows], [massOfCattle], [mliha], [np_mkarja_N], [np_mkarja_P]]
        )
        return np_mkarja_completed

    # -------------------------------------------------------------------------------
    # Name:        Milk data
    # Purpose:     Milk production by units and concentrations
    # -------------------------------------------------------------------------------

    # Syöttöjärjestys:
    # Lehmä lkm, Poikimaväli, Ummessaolokausi, Maitotuotos, Rasva, Proteiini, Laktoosi, Meijerimaito
    def calculateMilkProductionAndConcentrations(a, b, c, d, e, f, g, h):

        # Lasketaan lypsy- ja ruokintapäivien määrä
        lypsy_pv = 365 * (b - c) / b
        ruokinta_pv = a * lypsy_pv

        # Lasketaan raakamaidon päivätuotos per lehmä ja kokonaisvuosituotos
        milk_e_d = d / lypsy_pv

        # Lasketaam EKM ja RPKM (päivä- ja vuosituotos)
        if g == 0:
            ekm_e_d = milk_e_d * (38.3 * e + 24.2 * f + 783.2) / 3140
        else:
            ekm_e_d = milk_e_d * (38.3 * e + 24.2 * f + 16.54 * g + 20.7) / 3140

        rpkm_e_d = (0.337 + 0.116 * (e / 10) + 0.06 * (f / 10)) * milk_e_d

        # Lasketaan tuotettu rasva, proteiini ja laktoosi (päivä ja vuosi)
        fat_e_d = milk_e_d * e / 1000  # kg rasvaa per päivä per lehmä
        prot_e_d = milk_e_d * f / 1000  # kg proteiinia per päivä per lehmä
        lact_e_d = milk_e_d * g / 1000  # kg laktoosia per päivä per lehmä

        # Lasketaan typpi ja fosfori raakamaidossa
        n_milk_e_d = prot_e_d * 0.16  # kg maitotyppeä per lehmä per päivä
        p_milk_e_d = milk_e_d * 0.00093  # kg maitofosforia per lehmä per päivä

        # Lasketaan kuiva-aine
        dm_milk_e_d = fat_e_d + prot_e_d + lact_e_d

        # Lasketaan kalorit
        milk_kcal_e_d = ((e * 37 + (f + g) * 17 + (0.2 * 13)) * 1.431644) * milk_e_d

        # Luodaan array kaikista lasketuista tiedoista
        milk_list = [
            milk_e_d,
            ekm_e_d,
            rpkm_e_d,
            fat_e_d,
            prot_e_d,
            lact_e_d,
            n_milk_e_d,
            p_milk_e_d,
            dm_milk_e_d,
            milk_kcal_e_d,
        ]
        milk_info = np.array(milk_list)

        # Lasketaan kok vuosituotos ja vain myyty osuus
        milk_info_a = milk_info * ruokinta_pv
        milk_info_a_sold = milk_info_a * h

        # Yhdistetään kaikki
        milk_info_complete = np.concatenate(
            [[milk_info], [milk_info_a], [milk_info_a_sold]]
        )

        return milk_info_complete
