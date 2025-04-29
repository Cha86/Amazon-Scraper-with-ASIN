# 🔍 Amazon ASIN Price-Checker

Give it a list of ASINs and your promo prices, and it will visit every product page on Amazon, grab the live price, shout “Match!” or “Mismatch!” — then toss the results into a tidy CSV for you.
The main goal of this program is to help you quickly check all the prices that you want to run promo or the current buy box status on Amazon without checking manually one by one. It will go through each of the ASINs and generate a report for you.

---

## 🗂️  What it does, step-by-step

1. **Reads** an Excel file `ASIN_list.xlsx` with two columns:  
   `ASIN` | `Promo Price`
2. **Spins up** Chrome via Selenium.
3. **Loads** each product page (`https://www.amazon.com/dp/<ASIN>`).
4. **Scrapes**  
   * Product title  
   * Live price (new or used)  
   * Who’s selling it (Amazon vs 3rd-party)
5. **Compares** that live price to your promo price.
6. **Logs** everything to `ASIN_Price_Comparison.csv`.

---

## ⚙️  Requirements

| Package | Why |
|---------|-----|
| `selenium` | drive Chrome |
| `beautifulsoup4` | HTML parsing |
| `pandas` | read Excel |
| `openpyxl` | Excel driver for pandas |
| Chrome + matching ChromeDriver | headless tourist through Amazon |

> **Easy install**

```bash
pip install selenium beautifulsoup4 pandas openpyxl
```

The output looks like this:
![image](https://github.com/user-attachments/assets/49fd32a1-1b03-4c4a-ad1c-bb3095d77af0)


Note:
Headless mode – add
```bash
options = webdriver.ChromeOptions()
options.add_argument("--headless")
return webdriver.Chrome(options=options)
inside init_driver()
```
