import copy

from database import meteo_dao
from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._mappa_situazioni = None
        self.soluzione = []
        self.costo = None
        self.counter = {"Torino": 0, "Milano": 0, "Genova": 0}


    def leggi_situazioni(self):
        self._mappa_situazioni = MeteoDao.get_all_situazioni()

    def umidita_media(self, _mese):
        if self._mappa_situazioni is None:
            self.leggi_situazioni()

        res = dict()
        num = dict()
        for s in self._mappa_situazioni:
            if s.data.month == _mese:
                if s.localita not in res.keys():
                    res[s.localita] = s.umidita
                    num[s.localita] = 1
                else:
                    res[s.localita] += s.umidita
                    num[s.localita] += 1

        for k in res.keys():
            res[k] = res[k]/num[k]

        return res

    def citta_visitate(self, _mese):

        if self._mappa_situazioni is None:
            self.leggi_situazioni()

        da_visitare = []
        for s in self._mappa_situazioni:
            if s.data.month == _mese and s.data.day <= 15:
                da_visitare.append(s)

        self.soluzione = []
        self.costo = 100000

        da_visitare.sort(key=lambda x: x.data)
        print(da_visitare)
        self.ricorsione(da_visitare, [], 0, 0)
        print(self.soluzione)
        return self.soluzione, self.costo


    def ricorsione(self, da_visitare, soluzione, step, costo):
        lun = len(soluzione)
        if lun == 15:
            if self.costo > costo:
                self.soluzione = copy.deepcopy(soluzione)
                self.costo = costo
                print(soluzione)
        else:
            for i in range(step*3, (step+1) * 3):
                citta = da_visitare[i].localita
                if self.controlla_step(soluzione, citta, costo):
                    soluzione.append(da_visitare[i])
                    aggiunta = 0
                    if len(soluzione) > 1 and soluzione[-1].localita != soluzione[-2].localita:
                        aggiunta = 100
                    self.ricorsione(da_visitare, soluzione, step+1, (costo + da_visitare[i].umidita + aggiunta))
                    soluzione.pop()


    def controlla_step(self, soluzione, citta, costo):
        contatore = 0
        for s in soluzione:
            if s.localita == citta:
                contatore += 1

        if contatore >= 6 or costo > self.costo:
            return False

        if len(soluzione) < 3 and len(soluzione) > 0 and soluzione[-1].localita != citta:
            return False
        if len(soluzione) > 3:
            primo = soluzione[-1].localita
            secondo = soluzione[-2].localita
            terzo = soluzione[-3].localita
            if not (primo == secondo and secondo == terzo):
                if primo != citta:
                    return False

        return True




    def calcola_costo(self, soluzione):
        costo = 0
        for i, s in enumerate(self.soluzione):
            costo += s.umidita
            if self.soluzione[i - 1].localita != s.localita:
                costo += 100
        return costo