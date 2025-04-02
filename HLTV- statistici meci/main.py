import json
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Numele coloanei din CSV care conține URL-urile meciurilor
LINK_COLUMN = "Match URL"
# Dimensiunea chunk-ului: numărul de meciuri procesate înainte de salvare
CHUNK_SIZE = 100

cookie_handled = False

def check_and_handle_cookies(driver):
    """Elimină pop-up-ul de cookies, dacă apare (doar o singură dată)."""
    global cookie_handled
    if cookie_handled:
        return
    try:
        wait = WebDriverWait(driver, 10)
        cookie_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Allow all cookies')]")
        ))
        cookie_button.click()
        cookie_handled = True
        print("Pop-up-ul de cookies a fost eliminat.")
    except Exception as e:
        print("Pop-up-ul de cookies nu a fost găsit sau a apărut o eroare:", e)

def extract_map_menu(driver):
    """
    Extrage meniul de hărți din zona header.
    Returnează o listă de dicționare, fiecare conținând:
      - map_name: numele complet (ex: "Inferno")
      - map_id: id-ul butonului (ex: "196700")
    """
    maps = []
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.box-headline.flexbox.nowrap.header div.flexbox.nowrap")
            )
        )
        map_elements = container.find_elements(By.CSS_SELECTOR, "div.small-padding div.stats-menu-link")
        for elem in map_elements:
            try:
                full_elem = elem.find_element(By.CSS_SELECTOR, "div.dynamic-map-name-full")
                map_name = full_elem.text.strip()
                map_id = full_elem.get_attribute("id")
                maps.append({"map_name": map_name, "map_id": map_id})
            except Exception as e:
                print("Eroare la extragerea unei hărți:", e)
    except Exception as e:
        print("Eroare la localizarea meniului de hărți:", e)
    return maps

def extract_map_stats(driver):
    """
    Extrage datele din containerul de statistici vizibil (cu clasa "stats-content" care nu are "display: none").
    Pentru fiecare tabel din container se colectează rândurile (liste de celule) și se filtrează rândurile goale.
    Returnează un dicționar în care fiecare cheie este de forma "table_X (<class-ul tabelului>)".
    """
    stats = {}
    try:
        container = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.stats-content:not([style*='display: none'])"))
        )
        tables = container.find_elements(By.TAG_NAME, "table")
        for idx, table in enumerate(tables, start=1):
            table_class = table.get_attribute("class")
            rows = table.find_elements(By.TAG_NAME, "tr")
            table_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if cells:
                    row_data = [cell.text.strip() for cell in cells]
                    if any(row_data):
                        table_data.append(row_data)
            if table_data:
                stats[f"table_{idx} ({table_class})"] = table_data
    except Exception as e:
        print("Eroare la extragerea datelor din zona de statistici:", e)
    return stats

def extract_side_stats(driver, side_name):
    """
    Dă click pe elementul <span> cu clasa "gtSmartphone-only" care conține textul side_name
    (ex: "Terrorist" sau "Counter-Terrorist"), așteaptă actualizarea zonei de statistici și extrage datele.
    Returnează datele extrase ca dicționar.
    """
    try:
        side_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[contains(@class, 'gtSmartphone-only') and contains(text(), '{side_name}')]")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", side_button)
        driver.execute_script("arguments[0].click();", side_button)
    except Exception as e:
        print(f"Eroare la click pe side-ul {side_name}:", e)
        return None
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.stats-content:not([style*='display: none'])"))
        )
    except Exception as e:
        print(f"Eroare la așteptarea zonei de statistici pentru side-ul {side_name}:", e)
        return None
    return extract_map_stats(driver)

def navigate_and_extract_map_stats(driver, map_info):
    """
    Pentru o hartă dată:
      - Dă click pe butonul hărții folosind JavaScript.
      - Așteaptă actualizarea zonei de statistici.
      - Extrage datele din modul implicit (Overall) și apoi pentru side-urile "Terrorist" și "Counter-Terrorist".
    Returnează un dicționar cu cheile "Overall", "Terrorist" și "Counter-Terrorist".
    """
    map_name = map_info["map_name"]
    print(f"Procesăm harta: {map_name}")
    try:
        map_button = driver.find_element(By.XPATH, f"//div[@id='{map_info['map_id']}']")
        driver.execute_script("arguments[0].scrollIntoView(true);", map_button)
        driver.execute_script("arguments[0].click();", map_button)
    except Exception as e:
        print(f"Eroare la click pe harta {map_name}:", e)
        return None
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.stats-content:not([style*='display: none'])"))
        )
    except Exception as e:
        print(f"Eroare la așteptarea zonei de statistici pentru {map_name}: {e}")
        return None

    overall_stats = extract_map_stats(driver)
    print(f"Date colectate pentru harta {map_name} (Overall):", overall_stats)
    terrorist_stats = extract_side_stats(driver, "Terrorist")
    if terrorist_stats is not None:
        print(f"Date colectate pentru harta {map_name} (Terrorist):", terrorist_stats)
    ct_stats = extract_side_stats(driver, "Counter-Terrorist")
    if ct_stats is not None:
        print(f"Date colectate pentru harta {map_name} (Counter-Terrorist):", ct_stats)
    return {"Overall": overall_stats, "Terrorist": terrorist_stats, "Counter-Terrorist": ct_stats}

def main():
    input_csv = "combined_output.csv"
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print("Eroare la citirea CSV-ului:", e)
        return

    links = df[LINK_COLUMN].tolist()  # Toate link-urile din CSV

    driver = uc.Chrome()
    results = {}  # Structura finală: { URL: { map_name: { side: stats, ... }, ... }, ... }
    file_count = 1
    chunk_results = {}

    for index, url in enumerate(links):
        print(f"\nProcesăm: {url}")
        driver.get(url)
        check_and_handle_cookies(driver)
        print("Titlul paginii:", driver.title)

        map_menu = extract_map_menu(driver)
        print("Meniul de hărți:", map_menu)

        match_data = {}
        for map_info in map_menu:
            map_data = navigate_and_extract_map_stats(driver, map_info)
            if map_data is not None:
                match_data[map_info["map_name"]] = map_data
        chunk_results[url] = match_data

        # La fiecare CHUNK_SIZE meciuri, salvăm un fișier JSON și resetăm rezultatele chunk-ului
        if (index + 1) % CHUNK_SIZE == 0:
            output_file = f"match_stats_{file_count}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(chunk_results, f, ensure_ascii=False, indent=2)
            print(f"Datele pentru meciurile {index + 1 - CHUNK_SIZE + 1} - {index + 1} au fost salvate în {output_file}")
            file_count += 1
            chunk_results = {}

    # Salvăm eventualul chunk final, dacă există
    if chunk_results:
        output_file = f"match_stats_{file_count}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunk_results, f, ensure_ascii=False, indent=2)
        print(f"Datele pentru ultimele meciuri au fost salvate în {output_file}")

    driver.quit()
    print("Toate datele au fost colectate și salvate.")

if __name__ == "__main__":
    main()
