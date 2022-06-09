from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from project import db
from project.models import Tokens, TokensArbitrum, TokensOptimism

classes = [Tokens, TokensOptimism, TokensArbitrum]
networks = ['ethereum', 'optimism', 'arbitrum']
i=0

def run_scraper(i):
    service = Service("C:\development\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(f"https://info.uniswap.org/#/{networks[i]}/")
    time.sleep(15)

    counter = 1

    names = []
    perc = []
    volume = []
    tvl = []

    pages = driver.find_element(By.CSS_SELECTOR, "#root > div > div.sc-qrIAp.eqcyAL > div.sc-fOKMvo.knkUAB > div.sc-brqgnP.klmLHi > div.sc-jKJlTe.sc-gipzik.sc-hzDkRC.sc-daURTG.gkTejM > div > div.sc-iujRgT.cVwlxW > div.sc-chPdSV.goKJOd.css-1frkxb8")
    pages = int(pages.text[-1])

    tokens = driver.find_elements(By.CSS_SELECTOR,"#root > div > div.sc-qrIAp.eqcyAL > div.sc-fOKMvo.knkUAB > div.sc-brqgnP.klmLHi > div.sc-jKJlTe.sc-gipzik.sc-hzDkRC.sc-cbkKFq.hDKAee > div > a")

    def convert(new_vol):
        try:
            if new_vol[-1] == "m":
                new_vol = float(new_vol[1:-1]) * 1000000
            elif new_vol[-1] == "k":
                new_vol = float(new_vol[1:-1]) * 1000
            else:
                new_vol = float(new_vol[1:])
            return new_vol
        except:
            print(new_vol)

    while counter <= pages:
        button = driver.find_element(By.CSS_SELECTOR, "#root > div > div.sc-qrIAp.eqcyAL > div.sc-fOKMvo.knkUAB > div.sc-brqgnP.klmLHi > div.sc-jKJlTe.sc-gipzik.sc-hzDkRC.sc-cbkKFq.hDKAee > div > div.sc-iujRgT.cVwlxW > div:nth-child(3) > div")
        for token in tokens:
            name = token.find_element(By.CLASS_NAME, "sc-chPdSV.goKJOd.css-1j9mh98")
            names.append(name.text)

            percentage = token.find_element(By.CLASS_NAME, "sc-jKJlTe.sc-gipzik.sc-fAjcbJ.dsySXo")
            perc.append(percentage.text)

            vol = token.find_elements(By.CLASS_NAME, "sc-chPdSV.goKJOd.sc-bMVAic.eOIWzG.css-63v6lo")
            new_vol = vol[1].text
            adj_vol = convert(new_vol)
            volume.append(adj_vol)

            new_tvl = vol[0].text
            adj_tvl = convert(new_tvl)
            tvl.append(adj_tvl)

        counter += 1
        button.click()

    db.drop_all(bind=networks[i])
    db.create_all(bind=networks[i])

    columns = {"Pool Tokens": names, "Fee Percentage": perc, "Volume": volume, "TVL": tvl}
    for element in range(len(columns['Pool Tokens'])):
        token_db = columns["Pool Tokens"][element]
        fee_db = columns["Fee Percentage"][element]
        fee_no_perc_db = float(fee_db[0:-1])
        fee_rounded = round(fee_no_perc_db, 2)
        volume_db = columns["Volume"][element]
        tvl_db = columns["TVL"][element]
        apy_db = volume_db * fee_no_perc_db / tvl_db * 365
        apy_rounded = round(apy_db, 2)
        new_token = classes[i](id=element, token=token_db, fee=fee_rounded, volume=volume_db, tvl=tvl_db,
                           apy=apy_rounded)
        db.session.add(new_token)
    db.session.commit()

while i < len(networks):
    run_scraper(i)
    i += 1