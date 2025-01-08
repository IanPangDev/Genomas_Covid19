from playwright.sync_api import sync_playwright
import pandas as pd
import time
from os import listdir

def get_country(page):
    df = pd.DataFrame({'Genoma': [i[:-4] for i in listdir('./genomas') if i[-3:] == 'txt']})
    df = pd.concat([df, pd.DataFrame(columns=['Pais', 'Fecha'])])
    for index, genoma in enumerate(df['Genoma']):
        url = "https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus?SeqType_s=Nucleotide&VirusLineage_ss=taxid:2697049"
        page.goto(url)
        time.sleep(2)
        
        #Expandiendo el buscador
        page.click('#ids > i.fa.fa-plus.ncbi-button-icon', timeout=200000)
        time.sleep(2)

        # Colocando la proteina
        element = page.wait_for_selector('#givenText-ids', timeout=200000)
        element.scroll_into_view_if_needed()
        element.fill(genoma)
        page.click('#submit-ids', timeout=200000)
        time.sleep(2)

        # Encontrando la descripcion
        page.click('#DataTables_Table_0 > tbody > tr > td.table-cell-center.usa-fieldset-inputs.details-control > a', timeout=200000)
        time.sleep(2)

        # Tomando el pais
        page.wait_for_selector('#detailProp', timeout=200000)
        atributos = page.locator('#detailProp div')
        pais = ""
        for i in range(atributos.count()):
            texto = atributos.nth(i).inner_text().strip()
            if 'Geo Location: ' in texto:
                pais = texto.split('Geo Location: ')[1]
            elif 'Collection Date: ' in texto:
                df.loc[index, 'Fecha'] = texto.split('Collection Date: ')[1]

        if pais:
            df.loc[index, 'Pais'] = pais
        else:
            pais_alternativo = page.locator('#SubmLocation > span').inner_text().strip()
            df.loc[index, 'Pais'] = pais_alternativo

    df.to_csv('genomas_desc.csv', index=False)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Para ejecutar el proceso completo de proteinas
        get_country(page)
        browser.close()