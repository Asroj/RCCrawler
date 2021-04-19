import requests
import lxml.html as lh
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options

estadosURL = ["Acre", "Alagoas", "Amapa", "Amazonas", "Bahia", "Ceara", "Distrito-Federal", "Espirito-Santo", "Goias", "Maranhao", "Mato-Grosso", "Mato-Grosso-do-Sul", "Minas-Gerais", "Parana", "Paraiba", "Para", "Pernambuco", "Piaui", "Rio-Grande-do-Norte", "Rio-Grande-do-Sul", "Rio-de-Janeiro", "Rondonia", "Roraima", "Santa-Catarina", "Sergipe", "Sao-Paulo", "Tocantins"]
estados = ['\"Acre\"', '\"Alagoas\"', '\"Amapá\"', '\"Amazonas\"', '\"Bahia\"', '\"Ceará\"', '\"Distrito Federal\"', '\"Espírito Santo\"', '\"Goiás\"', '\"Maranhão\"', '\"Mato Grosso\"', '\"Mato Grosso do Sul\"', '\"Minas Gerais\"', '\"Paraná\"', '\"Paraíba\"', '\"Pará\"', '\"Pernambuco\"', '\"Piauí\"', '\"Rio Grande do Norte\"', '\"Rio Grande do Sul\"', '\"Rio de Janeiro\"', '\"Rondônia\"', '\"Roraima\"', '\"Santa Catarina\"', '\"Sergipe\"', '\"São Paulo\"', '\"Tocantins"']
i=0
resultados = [[estados[x]] for x in range (27)]
for estado in estadosURL:
	url='https://sidra.ibge.gov.br/pesquisa/registro-civil/quadros/'+estado+'/2019'


	#Create a handle, page, to handle the contents of the website
	page = requests.get(url)

	#Store the contents of the website under doc
	doc = lh.fromstring(page.content)#Parse data that are stored between <tr>..</tr> of HTML

	#print(doc)

	tr_elements = doc.xpath('//*[@id="quadros-q14"]//tr')
	for valor in tr_elements[3].xpath('.//td'):
		resultados[i].append(valor.text_content().replace(" ",""))

	i+=1

#Coletar os dados de 2020 no site da transparência do registro civil
#Browser Headless
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

#Navega até o site
driver.get('https://transparencia.registrocivil.org.br/registros')

#Seleciona a opção de pesquisar por óbitos
actions = ActionChains(driver)
opcaoObitos = driver.find_element_by_id('__BVID__53_BV_option_3')
actions.move_to_element(opcaoObitos).click().perform()

#Encontra e clica no dropdown de selecionar o ano
elementoData = driver.find_element_by_id('datePickrGroup')
elementoDataClicar = elementoData.find_element_by_xpath('.//*[@class = "multiselect__select"]')
actions.move_to_element(elementoDataClicar).click().perform()
escolherData = elementoData.find_element_by_xpath('.//*[@class = "multiselect__input"]')

#Envia o valor do ano que estamos querendo pesquisar e aperta enter para selecionar o ano
escolherData.send_keys(2020)
escolherData.send_keys(Keys.ENTER)
	
#Clica no botão de pesquisa e espera 1 segundo para a tabela de dados atualizar
driver.find_element_by_css_selector(".btn.btn-success").click()
time.sleep(1)

#Seleciona as linhas da tabela com os dados
tabela = driver.find_element_by_class_name('table-responsive').find_elements_by_xpath('.//tr')
#Salva a data e hora que coletou os dados
now = datetime.now()

contEstado = 0
for linha in tabela[1:]:
	colunas = linha.find_elements_by_xpath('.//td')
	resultados[contEstado].append(colunas[1].text)
	contEstado+=1

print('{',end='')
for dadosFinais in resultados:
	imprimir = ', '.join(map(str, dadosFinais))
	if dadosFinais != resultados[-1]:
		print('{' + imprimir + '},',end='')
	else:
		print('{' + imprimir + '}};')


dt_string = now.strftime("%d/%m/%Y às %H:%M")
print("Dados coletados em", dt_string)

#Fecha o navegador
driver.quit()
