"""Template robot with Python."""

import os
from re import X
from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers
from RPA.HTTP import HTTP
from Browser import Browser
from RPA.Tables import Tables
from RPA.PDF import PDF 
from RPA.FileSystem import FileSystem
from RPA.Archive import Archive

import time

browser = Browser()
pdf =PDF()
file = FileSystem()
archive = Archive()

reciepts_path = os.path.join(os.path.expanduser("~/Downloads"), "Receipts")
file.create_directory(reciepts_path)
app_url = "https://robotsparebinindustries.com/#/robot-order"
orders_url = "https://robotsparebinindustries.com/orders.csv"
orders_path =  os.path.join(os.path.expanduser("~/Downloads"), "orders.csv")

def open_website():
    # browser.new_browser(browser=SupportedBrowsers.chromium,headless=False,  args=["--start-maximized"])
    browser.open_browser(app_url)
    # browser.set_viewport_size(1800,1200)
 
def donwload_orders():
    http = HTTP()
    http.download(orders_url,orders_path)
    
def obtain_data_from_excel():
    table = Tables()
    orders_table = table.read_table_from_csv(orders_path)
    return orders_table
    
def close_popup():
    # browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[2]/div/div""",state="visible")
    browser.click("""xpath=//*[@id="root"]/div/div[2]/div/div/div/div/div/button[1]""")

def build_robot():
    orders = obtain_data_from_excel()
    for order in orders:
        try:
            close_popup()
            browser.select_options_by("id=head",SelectAttribute.value, order['Head'])
            browser.check_checkbox(f"id=id-body-{order['Body']}")
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[3]/input""",order['Legs'])
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[4]/input""",order['Address'])
            take_robot_screenshot()
            browser.click("id=order")
            receipt = browser.get_property("""xpath=//*[@id="receipt"]""", "outerHTML")
                   
            pdf.html_to_pdf(content = receipt,output_path =os.path.join(reciepts_path ,f"receipt_{order['Order number']}.pdf"))
            pdf.add_files_to_pdf(files = [os.path.join(os.path.expanduser("~/Downloads"), "screenshot-1.png")], target_document = os.path.join(reciepts_path, f"receipt_{order['Order number']}.pdf"), append=True)

            # browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[1]/div/div[1]/div""", ElementState.visible,timeout=5, message="error")

            browser.click("id=order-another")
            archive.archive_folder_with_zip(folder = reciepts_path, archive_name="output/Receipts.zip", recursive=True)

        except (AssertionError) as err:
            browser.click("id=order")
            browser.click("id=order-another")

        finally:
            print("stop")


def take_robot_screenshot():
    browser.click("id=preview")
    time.sleep(2)
    browser.take_screenshot(filename= os.path.join(os.path.expanduser("~/Downloads"), "screenshot-1"), selector="""xpath=//*[@id="robot-preview-image"]""",fullPage=True)
    print("done")

if __name__ == "__main__":
    open_website()
    donwload_orders()
    obtain_data_from_excel()
    build_robot()
 
