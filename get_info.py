from playwright.sync_api import sync_playwright
import pandas as pd
import time

def download_files(page, index):
    page.evaluate('window.scrollTo(0, 0);')
    page.evaluate('window.scrollTo(0, 100);')
    time.sleep(3)

    try:
        # Espera a que uno de los dos elementos aparezca
        page.wait_for_selector("#mat-tab-content-0-0 > div > section > div.vf-stack.ng-tns-c3952154888-1 > p.vf-lede.ng-tns-c3952154888-1, #mat-tab-label-0-5", timeout=200000)

        # Verifica si existe el elemento con "No hits found."
        if page.locator("#mat-tab-content-0-0 > div > section > div.vf-stack.ng-tns-c3952154888-1 > p.vf-lede.ng-tns-c3952154888-1").count() > 0:
            if page.locator("#mat-tab-content-0-0 > div > section > div.vf-stack.ng-tns-c3952154888-1 > p.vf-lede.ng-tns-c3952154888-1").inner_text().strip() == "No hits found.":
                return  # Sale si encuentra "No hits found."

        # Salvando png
        page.click('#mat-tab-label-0-2')
        time.sleep(7)
        with page.expect_download() as download_info:
            page.click('body > section > div.vf-content.vf-grid__col--span-1 > div:nth-child(3) > button')
        download = download_info.value
        download.save_as("./info/" + f"{index}.png")

        # Salvando json
        page.click('#mat-tab-label-0-4')
        time.sleep(2)
        divs = page.locator('#mat-tab-content-0-4 > div .ng-star-inserted')
        for i in range(divs.count()):
            try:
                titulo = divs.nth(i).locator('.vf-section-header__heading').inner_text()
                if titulo == 'Output from the Python Parsers CLI application':
                    with page.expect_download() as download_info:
                        divs.nth(i).locator('.vf-button--primary').click()
                    download = download_info.value
                    download.save_as("./info/" + f"{index}.json")
                    break
            except Exception as e:
                pass
        time.sleep(4)
    except Exception as e:
        pass

def get_proteinas(page):
    proteinas = pd.read_csv('df_proteinas_unicas.csv')
    for index, proteina in enumerate(proteinas.Proteinas.values):
        if index <= 50:
            continue
        url = "https://www.ebi.ac.uk/jdispatcher/sss/ncbiblast"
        page.goto(url)
        time.sleep(2)

        # Colocando la proteina
        element = page.wait_for_selector('#sequence', timeout=5000)
        element.scroll_into_view_if_needed()
        element.fill(proteina)
        time.sleep(2)

        # Enviando la peticion
        page.click('#content > app-ncbiblast > div > form > section:nth-child(5) > div.vf-content.vf-grid__col--span-3 > div:nth-child(3) > p > button')
        time.sleep(2)

        # Descargando archivos
        page.wait_for_selector('#mat-mdc-dialog-0 > div > div > jdw-jobwaiting-dialog > div:nth-child(2) > div > button.vf-button.vf-button--primary.ng-star-inserted', timeout=200000).click()
        download_files(page, index)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Para ejecutar el proceso completo de proteinas
        get_proteinas(page)
        browser.close()