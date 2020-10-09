import logging
import time

import requests
from bs4 import BeautifulSoup

from repository.rainfall_list_repository import RainfallListRepository as BaseRepository
from utils.text_util import get_text
from model.rainfall_summary import RainfallSummary


logger = logging.getLogger(__name__)

class RainfallListRepository(BaseRepository):
    def __init__(self):
        self.base_url = 'https://www.river-gunma.jp/gunma/p1104/10'
        self.first_page_url = '1_13_1_0.html'

    def find_all(self, area_no=13):
        param = str(time.time_ns())
        rainfall_list = self._get_rain_list_from_hp(self.first_page_url, param)
        return rainfall_list
        
    def _get_rain_list_from_hp(self, page_url, param):
        url = f'{self.base_url}/{page_url}?{param}'
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        form = soup.find('form', {'id': 'param'})
        trs = form.find('tbody').find_all('tr')
        rains_list = self._create_rain_list_from_tr(trs)
        if self._has_next_page(soup):
            next_page_url = self._get_next_page_url(form)
            rains_list += self._get_rain_list_from_hp(next_page_url, param)
        
        return rains_list


    def _has_next_page(self, soup):
        next_button = soup.find('button', {'name': 'nextPage'})
        if next_button:
            onclick = next_button.get('onclick')
            if onclick:
                return True
        return False


    def _get_next_page_url(self, form):
        last = form.find('input', {'name': 'last'})['value']
        grid = 0
        page = int(form.find('input', {'name': 'page'})['value']) + 1
        ntim = form.find('input', {'name': 'ntim'})['value']

        return f'{last}_{grid}_{page}_{ntim}.html'


    def _create_rain_list_from_tr(self, trs):
        """
        <tr class="even">
            <td><a href="p1103,13," class="js-chage-relDisp">四万川ダム</a></td>
            <td>0.0</td>
            <td class="missing">&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td class="rainfallLv3">45.0</td>
            <td>10月07日 19時10分</td>
            <td>中之条土木</td>
            <td>中之条町</td>
        </tr>
        """
        rain_list = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) < 11:
                continue
            name = get_text(tds[0].text)
            r = RainfallSummary(name)
            r.amount_10m = get_text(tds[1].text)
            r.amount_60m = get_text(tds[2].text)
            r.amount_1h = get_text(tds[3].text)
            r.amount_3h = get_text(tds[4].text)
            r.amount_6h = get_text(tds[5].text)
            r.amount_24h = get_text(tds[6].text)
            r.amount_total = get_text(tds[7].text)
            r.start_time = get_text(tds[8].text)
            r.office_name = get_text(tds[9].text)
            r.city_name = get_text(tds[10].text)
            rain_list.append(r)

        return rain_list