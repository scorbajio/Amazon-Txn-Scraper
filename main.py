#!/usr/bin/python3.8

import os
import time
import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AmazonTransactionScraper(object):

  def __init__(self):
    super().__init__()
    self.all_scrapable_transactions = []
    self.load_env_variables()
    self.driver = self.initialize_driver('./geckodriver')
    self.login()

  def close(self):
    self.driver.quit()

  def load_env_variables(self):
    load_dotenv()
    self.AMAZON_USERNAME = os.environ.get('AMAZON_USERNAME')
    self.AMAZON_PASSWORD = os.environ.get('AMAZON_PASSWORD')

  def initialize_driver(self, path_to_driver):
    return webdriver.Remote('http://localhost:4444')

  def login(self):
    self.driver.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fdp%2FB07QK955LS%2Fref%3Dods_gw_tpr_d_h1_hw_dygi%2F%3F_encoding%3DUTF8%26pd_rd_r%3D7c3d2e8f-e798-440b-aa0b-7a40f8ede18b%26pd_rd_w%3DLrB4v%26pd_rd_wg%3DnVC6G%26pf_rd_p%3Dd342e32b-cf32-40a8-8011-3bd4bb7212a0%26pf_rd_r%3DY6N1JT3PV12MWEHK39FQ%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')
    
    email_input = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//input[@id="ap_email"]'))
    )
    email_input.clear()
    email_input.send_keys(self.AMAZON_USERNAME)

    continue_input = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//input[@id="continue"]'))
    )
    continue_input.click()

    password_input = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//input[@id="ap_password"]'))
    )
    password_input.clear()
    password_input.send_keys(self.AMAZON_PASSWORD)

    signInSubmit_input = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//input[@id="signInSubmit"]'))
    )
    signInSubmit_input.click()

  def scrape_transactions(self):
    self.driver.get('https://www.amazon.com/cpe/yourpayments/transactions')

    while True:
      time.sleep(2)

      transaction_divs = WebDriverWait(self.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@class="a-section a-spacing-base apx-transactions-line-item-component-container"]'))
      )
      transaction_texts = list(map(lambda transaction_div: transaction_div.text, transaction_divs))
      self.all_scrapable_transactions += transaction_texts

      try:
        next_page_input = WebDriverWait(self.driver, 2).until(
          EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next Page")]//parent::span/input'))
        )
        next_page_input.click()
      except:
        return

  def write_transactions_to_file(self, path_to_file):
    with open(path_to_file, 'a') as file_handle:
      for transaction in self.all_scrapable_transactions:
        file_handle.write('\n' + transaction + '\n')

if __name__ == '__main__':
  amazon_transaction_scraper = None
  try:
    amazon_transaction_scraper = AmazonTransactionScraper()
    amazon_transaction_scraper.scrape_transactions()
    amazon_transaction_scraper.write_transactions_to_file(f'{datetime.datetime.now().__str__()}.txt')
  except Exception as e:
    print(e)
  finally:
    amazon_transaction_scraper.close()
