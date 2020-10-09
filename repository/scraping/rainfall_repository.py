import logging
import time

import requests
from bs4 import BeautifulSoup

from repository.rainfall_repository import RainfallRepository as BaseRepository
from utils.text_util import get_text
from model.rainfall import Rainfall
from model.rainfall import RainfallTimeLine


logger = logging.getLogger(__name__)

class RainfallRepository(BaseRepository):
    def __init__(self):
        self.base_url = 'https://www.river-gunma.jp/gunma/p1102/'
        self.first_page_url = '1_13_1_0.html'

    def find_all(self, unit=10, area_no=13):
        param = str(time.time_ns())
        rainfalls = self._get_rains_from_hp(self.first_page_url, unit, param)
        return rainfalls
        
    def _get_rains_from_hp(self, page_url, unit, param):
        url = f'{self.base_url}/{unit}/{page_url}?{param}'
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        form = soup.find('form', {'id': 'param'})
        trs = form.find('thead').find_all('tr')
        rains = self._create_rains_from_tr(trs, unit)
        trs = form.find('tbody').find_all('tr')
        rains = self._append_timeline(rains, trs)

        if self._has_next_page(soup):
            next_page_url = self._get_next_page_url(form)
            rains += self._get_rains_from_hp(next_page_url, unit, param)
        
        return rains


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


    def _create_rains_from_tr(self, trs, unit):
        """
        <tr class="highCol">
            <th style="width:12%">観測所名</th>
            <th  style="width:11%" colspan="2"><a href="p1103,13," class="js-chage-relDisp">四万川ダム</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,13," class="js-chage-relDisp">ブノウ沢</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,13," class="js-chage-relDisp">大道(砂)</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,13," class="js-chage-relDisp">上沢渡(砂)</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,,18" class="js-chage-relDisp">中之条(国)</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,,18" class="js-chage-relDisp">四万(国)</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,,18" class="js-chage-relDisp">暮坂峠(国)</a></th>
            <th  style="width:11%" colspan="2"><a href="p1103,,18" class="js-chage-relDisp">野反(国)</a></th>
        </tr>
        <tr class="highCol">
            <th>降雨開始時刻</th>
            <td colspan="2" class="alignColC">10/07 19:10</td>
            <td colspan="2" class="alignColC">10/07 18:50</td>
            <td colspan="2" class="alignColC">10/07 19:10</td>
            <td colspan="2" class="alignColC">10/07 17:30</td>
            <td colspan="2" class="alignColC">10/07 18:50</td>
            <td colspan="2" class="alignColC">10/07 18:40</td>
            <td colspan="2" class="alignColC">10/07 18:20</td>
            <td colspan="2" class="alignColC">10/07 18:30</td>
        </tr>
        """
        rains = []
        if len(trs) < 2:
            return rains

        for i, th in enumerate(trs[0].find_all('th')):
            if i == 0:
                continue
            rainfall = Rainfall(str(unit), get_text(th.text))
            rains.append(rainfall)
        
        for i, td in enumerate(trs[1].find_all('td')):
            rains[i].start_time = get_text(td.text)

        return rains

    def _create_timeline(self, rains, tds):
        dt = ''
        for i, td in enumerate(tds):
            if i == 0:
                dt = get_text(td.text)
            elif i % 2:
                timeline = RainfallTimeLine(dt)
                timeline.unit_amount = get_text(td.text)
                rains[int(i/2)].timelines.append(timeline)
            else:
                rains[int(i/2)-1].timelines[-1].total_amount = get_text(td.text)
        return rains


    def _append_timeline(self, rains, trs):
        """
        <tr class="odd">
            <td>10/08 15:20</td>
            <td>0.0</td>
            <td class="rainfallLv3">43.0</td>
            <td>0.0</td>
            <td class="rainfallLv3">48.0</td>
            <td>0.0</td>
            <td class="rainfallLv3">40.0</td>
            <td>0.0</td>
            <td class="rainfallLv4">51.0</td>
            <td>0.0</td>
            <td class="rainfallLv3">41.0</td>
            <td>0.0</td>
            <td class="rainfallLv3">48.0</td>
            <td>0.0</td>
            <td class="rainfallLv4">52.0</td>
            <td>0.0</td>
            <td class="rainfallLv4">55.0</td>
        </tr>
        """
        for tr in trs:
            tds = tr.find_all('td')
            rains = self._create_timeline(rains, tds)
        
        return rains

