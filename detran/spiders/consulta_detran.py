# -*- coding: utf-8 -*-
import scrapy

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
            yield{
                'ID_MUN': id_municipio,
                'NME_MUN': nome_municipio,
                'ANO': ano,
                'NME_COMB': combustivel,
                'JAN': valores[0],
                'FEV': valores[1],
                'MAR': valores[2],
                'ABR': valores[3],
                'MAI': valores[4],
                'JUN': valores[5],
                'JUL': valores[6],
                'AGO': valores[7],
                'SET': valores[8],
                'OUT': valores[9],
                'NOV': valores[10],
                'DEZ': valores[11]
            }
