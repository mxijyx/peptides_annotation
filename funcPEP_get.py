import re
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

def get_NCPEP_links(url, driver):
    driver.get(url)
    i = 1
    returned_links = []

    while i < 16:
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and "ncpep" in href:
                returned_links.append(href)
                print(href)
        #<a href="ncpep/NCPEP00146.html" target="_blank">NCPEP00146</a>
        try:
            # finding next page
            i+=1
            next_page = driver.find_element(By.LINK_TEXT, "Next")
            next_page.click()
        except NoSuchElementException:
            break
    return returned_links

def is_coding(ncbi_url, driver):
    try:
        driver.get(ncbi_url)
        if "Page not found" in driver.page_source:
            return "no info"
        page_source = driver.page_source
        #if (driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[6]/div[2]/section[1]/div[2]/div/div/dl/dd[5]")):
        if "protein coding" in page_source:
            return "coding"
        elif "ncRNA" in page_source:
            return "ncRNA"
        return "no info"
    except NoSuchElementException:
        return "no info"


if __name__ == '__main__':
    url = "https://bioinformatics.mdanderson.org/Supplements/FuncPEP/"
    driver = webdriver.Edge()
    links = get_NCPEP_links(url, driver)
    data = []
    for link in links:
        new_url = link
        driver.get(new_url)
        gene_name = driver.find_element(By.XPATH, "/html/body/div[2]/header/table/tbody/tr[3]/td[2]").text
        print("gene name: ", gene_name)
        #aminoacid
        aa = driver.find_element(By.XPATH, "/html/body/div[2]/header/table/tbody/tr[7]/td[2]").text
        #        / html / body / div[2] / header / table / tbody / tr[7] / td[2]
        if re.fullmatch(r"[A-Z]+", aa):
            print("aa: ", aa)

            species = driver.find_element(By.XPATH, "/html/body/div[2]/header/table/tbody/tr[19]/td[2]").text
            print("species: ", species)

            gene_id = driver.find_element(By.XPATH, "/html/body/div[2]/header/table/tbody/tr[4]/td[2]").text
            print("gene ID: ", gene_id)

            pep_name = driver.find_element(By.XPATH, "/html/body/div[2]/header/table/thead/tr/th[2]").text
            print("pep name: ", pep_name)

            coding_bool = is_coding(link, driver)   # coding /not

            #if re.fullmatch(r"[A-Z]+", aa.text) and gene_id and :
            #data.append([pep_name, aa, gene_name, gene_id, coding_bool, species])
            if re.match("Human" or "Kaposi", species):
                with open("new_funcpep_fasta.txt", "a") as f:  # a - append and not w write!
                    f.write(">")
                    f.write(pep_name)
                    f.write("\n")
                    f.write(aa)
                    f.write("\n")

    driver.quit()
