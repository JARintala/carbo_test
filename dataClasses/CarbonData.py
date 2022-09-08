from numbers import Number
from dataClasses.MilkProductionData import MilkProductionData
from dataClasses.OutdoorRecreationOfCattleData import OutdoorRecreationOfCattleData
from dataClasses.CattleIndicatorsData import CattleIndicatorsData


class CarbonData:
    cattleIndicatorsData: CattleIndicatorsData
    outdoorRecreationOfCattleData: OutdoorRecreationOfCattleData
    milkProductionData: MilkProductionData

    id: str
    year: Number
    status: str
    userId: str
