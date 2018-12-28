# -*- coding: utf-8 -*-
import scrapy
from unicodedata import normalize
from datetime import datetime

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

class ConsultaDetranSpider(scrapy.Spider):
    ano_global = "";
    valor = "esse"
    name = 'consulta_detran'
    allowed_domains = ['detran.se.gov.br']
    start_urls = ['http://www.detran.se.gov.br/estat_RB00093M.asp']

    def parse(self, response):
        anos = response.xpath("//select[contains(@name, 'nr_Ano')]/option/@value").extract()
        municipios = response.xpath("//select[contains(@name, 'cd_Municipio')]/option/@value").extract()

        for ano in anos:
            for municipio in municipios:
                yield scrapy.FormRequest.from_response(
                    response,
                    formdata={'nr_Ano': ano, 'cd_Municipio': municipio},
                    callback=self.numero_frotas
                )


    def numero_frotas(self, response):
        ano = response.xpath('//select[contains(@name, "nr_Ano")]//option[@selected="selected"]/text()').extract_first()
        nome_municipio = response.xpath('//select[contains(@name, "cd_Municipio")]//option[@selected="selected"]/text()').extract_first()
        id_municipio = response.xpath("//option[text()='{}']/@value".format(nome_municipio)).extract_first()
        combustiveis = response.xpath("//table[contains(@id,'table1')]//tr[position() >= 3 and position() < 18]/td[contains(@class,'tblSubtitulo')]/text()").extract()
        #print("Ano: {} Municipio: {}".format(ano, nome_municipio))
        for combustivel in combustiveis:
            valores = response.xpath("//td[text()='{}']/following-sibling::td/text()".format(combustivel)).extract()
            meses = {'01': valores[0], '02': valores[1], '03': valores[2], '04': valores[3], '05': valores[4], '06': valores[5], '07': valores[6], '08': valores[7], '09': valores[8], '10': valores[9], '11': valores[10], '12': valores[11]}

            for mes in meses:
                yield{
                    'ID_MUN': id_municipio,
                    'NME_MUN': nome_municipio,
                    'NME_COMB': remover_acentos(combustivel),
                    'DTA': '{}/{}/{}'.format('01', mes, ano),
                    'QTD': meses[mes]
                }
