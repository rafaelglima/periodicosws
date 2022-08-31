import os
import time
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By

# driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "usr/local/bin/chromedriver")
# driver = webdriver.Chrome(executable_path=DRIVER_BIN)
driver = webdriver.Chrome()
driver.get('https://www.periodicos.unimontes.br/')

# input('Aperte enter para iniciar a navegação automatizada.')

connection = mysql.connector.connect(host='localhost', user='root', password='123456', database='periodicos',
                                     auth_plugin='mysql_native_password', charset='utf8')
cursor = connection.cursor(dictionary=True)

# pegando links dos livros e embaixo adicionando-os em um array para ser possível andar pelos livros
links_livros = driver.find_elements(By.XPATH, "//div[@class='thumb']//*[@href]")
i = []
for span in links_livros:
    i.append(span.get_attribute('href'))
    # i.append('https://www.periodicos.unimontes.br/index.php/alteridade')
    # i.append('https://www.periodicos.unimontes.br/index.php/araticum')
    # i.append('https://www.periodicos.unimontes.br/index.php/argumentos')
    # i.append('https://www.periodicos.unimontes.br/index.php/caminhosdahistoria')
    # i.append('https://www.periodicos.unimontes.br/index.php/cerrados')
    # i.append('https://www.periodicos.unimontes.br/index.php/ciranda')
    # i.append('https://www.periodicos.unimontes.br/index.php/rds')
    # i.append('https://www.periodicos.unimontes.br/index.php/economiaepoliticaspublicas')
    # i.append('https://www.periodicos.unimontes.br/index.php/emd')
    # i.append('https://www.periodicos.unimontes.br/index.php/rees')
    # i.append('https://www.periodicos.unimontes.br/index.php/renef')
    # i.append('https://www.periodicos.unimontes.br/index.php/poiesis')
    # i.append('https://www.periodicos.unimontes.br/index.php/renome')
    # i.append('https://www.periodicos.unimontes.br/index.php/sesoperspectiva')
    # i.append('https://www.periodicos.unimontes.br/index.php/unicientifica')
    # i.append('https://www.periodicos.unimontes.br/index.php/verdegrande')
    break
j = 0

# array de livros
for j in range(len(i)):
    time.sleep(3)
    driver.get(i[j])
    # pegando o livro atual
    aux = driver.current_url
    revista = str(aux).split('/')
    # pegando os livros anteriores
    driver.get(i[j] + '/issue/archive')
    # lendo esses livros anteriores e adicionando em 1 array
    # versoes = driver.find_elements(By.XPATH,"//a[@class='cover']") #so pegava as que tinha figura
    versoes = driver.find_elements(By.XPATH, "//a[@class='title']")
    v = []
    for r in versoes:
        v.append(r.get_attribute('href'))
    r = 0
    # andando pelas versoes anteriores
    for r in range(len(v)):
        driver.get(v[r])
        # pegando os artigos postados e adicionando em 1 array
        artigos = driver.find_elements(By.XPATH, "//h3[@class='title']//*[@href]")
        k = []
        for x in artigos:
            k.append(x.get_attribute('href'))
        y = 0
        for y in range(len(k)):
            # entrando no artigo e pegando os dados necessarios
            driver.get(k[y])
            time.sleep(0)
            if driver.find_element(By.CLASS_NAME,'page_title').text:
                titulo = driver.find_element(By.CLASS_NAME,'page_title').text
                time.sleep(0)
            else:
                titulo = ''

            try:
                if driver.find_element(By.XPATH, "//ul[@class='authors']").text:
                    total = len(driver.find_elements_by_xpath("//ul[@class='authors']//li"))
                    autores = ''
                    for j in range(total):
                        autores += driver.find_element_by_xpath(
                            "//ul[@class='authors']//li[" + str(j + 1) + "]//span[@class='name']").text + ';'

                    time.sleep(0)
            except:
                autores = ''


            if driver.find_elements(By.XPATH,"//section[@class='item keywords']//span[@class='value']"):
                palavra_chave = driver.find_element(By.XPATH,
                    "//section[@class='item keywords']//span[@class='value']").text
                time.sleep(0)
            else:
                palavra_chave = ''
            if driver.find_elements(By.XPATH,"//section[@class='item abstract']//p"):
                resumo = driver.find_element(By.XPATH,"//section[@class='item abstract']//p").text
                time.sleep(0)
            else:
                resumo = ''
            if driver.find_elements(By.XPATH,"//section[@class='item references']//div[@class='value']"):
                referencias = driver.find_element(By.XPATH,
                    "//section[@class='item references']//div[@class='value']").text
                time.sleep(0)
            else:
                referencias = ''
            if driver.find_elements(By.XPATH,"//a[@class='title']"):
                versao = driver.find_element(By.XPATH,"//a[@class='title']").text
                time.sleep(0)
            else:
                versao = ''

            referencias = referencias.replace("'", "")
            referencias = referencias.replace('"', "")

            resumo = resumo.replace("'", "")
            resumo = resumo.replace('"', "")

            palavra_chave = palavra_chave.replace("'", "")
            palavra_chave = palavra_chave.replace('"', "")

            autores = autores.replace("'", "")
            autores = autores.replace('"', "")

            titulo = titulo.replace("'", "")
            titulo = titulo.replace('"', "")

            versao = versao.replace("'", "")
            versao = versao.replace('"', "")

            cursor.execute("DELETE FROM artigos WHERE Titulo='" + titulo + "'")
            connection.commit()
            cursor.execute(
                "INSERT INTO artigos(revista,versao,titulo,autores,palavra_chave,resumo,referencias) VALUES('" +
                revista[4] + "','" + versao + "','" + str(titulo) + "','" + str(autores) + "','" + str(
                    palavra_chave) + "','" + str(resumo) + "','" + str(referencias) + "')")
            connection.commit()
