from database import meteo_dao
from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._mappa_situazioni = None
        self.soluzione = []
        self.costo = 100000
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

        da_visitare.sort(key=lambda x: x.data)
        self.ricorsione(da_visitare, [], 0, 0)
        return self.soluzione


    def ricorsione(self, da_visitare, soluzione, step, costo):
        lun = len(soluzione)
        if lun == 15:
            if self.costo > costo:
                self.soluzione = soluzione
                self.costo = costo
                #print("ho finito")
        else:
            for i in range(step*3, (step+1) * 3):
                citta = da_visitare[i].localita
                if self.counter[citta] < 6 and costo < self.costo:
                    soluzione.append(da_visitare[i])
                    self.counter[citta] += 1
                    aggiunta = 0
                    if len(soluzione) > 1 and soluzione[step].localita != soluzione[step-1].localita:
                        aggiunta = 100
                    self.ricorsione(da_visitare, soluzione, step+1, (costo + da_visitare[i].umidita + aggiunta))

                    costo -= aggiunta
                    costo -= da_visitare[i].umidita
                    soluzione.pop()



    def calcola_costo(self, soluzione):
        costo = 0
        for i, s in enumerate(self.soluzione):
            costo += s.umidita
            if self.soluzione[i - 1].localita != s.localita:
                costo += 100
        return costo