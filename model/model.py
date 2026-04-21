from database import meteo_dao
from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._mappa_situazioni = None


    def leggi_situazioni(self):
        self._mappa_situazioni = MeteoDao.get_all_situazioni()

    def umidita_media(self, _mese):
        if self._mappa_situazioni is None:
            self.leggi_situazioni()

        res = dict
        num = dict
        for s in self._mappa_situazioni:
            if s.data.month == _mese:
                if s.localita not in res:
                    res[s.localita] = s.umidita
                    num[s.localita] = 1
                else:
                    res[s.localita] += s.umidita
                    num[s.localita] += 1

        for k in res.keys():
            res[k] = res[k]/num[k]

        return res


