"""Template robot with Python."""

import os
from Browser.utils.data_types import ElementState, SelectAttribute
from RPA.HTTP import HTTP
from Browser import Browser
from RPA.Tables import Tables
import time


browser = Browser()
app_url = "https://robotsparebinindustries.com/#/robot-order"
orders_url = "https://robotsparebinindustries.com/orders.csv"
orders_path =  os.path.join(os.path.expanduser("~/Downloads"), "orders.csv")

def open_website():
    browser.open_browser(app_url)

def donwload_orders():
    http = HTTP()
    http.download(orders_url,orders_path)
    time.sleep(5)

def obtain_data_from_excel():
    table = Tables()
    orders_table = table.read_table_from_csv(orders_path,header=True)
    return orders_table
    
def close_popup():
    # browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[2]/div/div""",state="visible")
    browser.click("""xpath=//*[@id="root"]/div/div[2]/div/div/div/div/div/button[1]""")

def build_robot():
    time.sleep(3)
    orders = obtain_data_from_excel()
    for order in orders:
        try:
            close_popup()
            body_number = 4
            browser.select_options_by("id=head",SelectAttribute.value, order['Head'])
            browser.check_checkbox(f"id=id-body-{order['Body']}")
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[3]/input""",order['Legs'])
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[4]/input""",order['Address'])
            take_robot_screenshot()
            browser.click("id=order")
            browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[1]/div/div[1]/div""", ElementState.visible,timeout=5, message="error")
            
            time.sleep(2)
            browser.click("id=order-another")

        # except (AssertionError) as err:
        #     browser.click("id=order")
        #     browser.click("id=order-another")

        finally:
            print("stop")

def take_robot_screenshot():
    browser.click("id=preview")
    browser.take_screenshot(filename= os.path.join(os.path.expanduser("~/Downloads"), "screenshot-{index}"), selector="id=robot-preview-image")
    print("done")


if __name__ == "__main__":
    open_website()
    donwload_orders()
    obtain_data_from_excel()
    build_robot()
 
# <div class="alert alert-danger" role="alert">Guess what? A server Error!</div>
