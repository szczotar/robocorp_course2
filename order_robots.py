"""Template robot with Python."""

import os
from time import thread_time
from Browser.utils.data_types import ElementState, SelectAttribute, SupportedBrowsers
from RPA.Dialogs.dialog_types import Options, Result, Size
from RPA.HTTP import HTTP
from Browser import Browser
from RPA.Tables import Tables
from RPA.PDF import PDF 
from RPA.FileSystem import FileSystem
from RPA.Archive import Archive
from RPA.Robocloud.Secrets import Secrets
from RPA.Dialogs import Dialogs

browser = Browser()
pdf =PDF()
file = FileSystem()
archive = Archive()
http = HTTP()
secrets = Secrets()
dialog = Dialogs()


# reciepts_path = os.path.join(os.path.expanduser("~/Downloads"), "Receipts")
# file.create_directory(reciepts_path)
orders_path =  os.path.join(os.path.expanduser("~/Downloads"), "orders.csv")

def open_website():
    # browser.new_browser(browser=SupportedBrowsers.chromium,headless=False,  args=["--start-maximized"])
    app_url = secrets.get_secret("process_website")["url"]
    browser.open_browser(app_url)
    # browser.set_viewport_size(1800,1200)

def ask_user():
    dialog.add_heading("The url for the input is required",Size.Medium)
    dialog.add_text_input("url","Enter the input url",rows=1)
    dialog.add_submit_buttons(buttons="Yes,No")
    d = dialog.show_dialog(height=300, width=400)
    result = dialog.wait_dialog(d, timeout=60)
    return result['url']


def donwload_orders():
    orders_url = ask_user()
    http.download(orders_url,orders_path)
        
def obtain_data_from_excel():
    table = Tables()
    orders_table = table.read_table_from_csv(orders_path)
    return orders_table
    
# close popup which shows up after each order
def close_popup():
    browser.click("""xpath=//*[@id="root"]/div/div[2]/div/div/div/div/div/button[1]""")

def build_robot():
    reciepts_path = os.path.join(os.path.expanduser("~/Downloads"), "Receipts")
    file.create_directory(reciepts_path)
    orders = obtain_data_from_excel()
    for order in orders:
        while True:
            try:
                # fill an order with data from the excel
                close_popup()
                browser.select_options_by("id=head",SelectAttribute.value, order['Head'])
                browser.check_checkbox(f"id=id-body-{order['Body']}")
                browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[3]/input""",order['Legs'])
                browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[4]/input""",order['Address'])
                # take a screenshot
                take_robot_screenshot()
                # confirm an order
                browser.click("id=order")
                # save a receipt as pdf and add a robot image indside.
                receipt = browser.get_property("""xpath=//*[@id="receipt"]""", "outerHTML")                    
                pdf.html_to_pdf(content = receipt,output_path =os.path.join(reciepts_path ,f"receipt_{order['Order number']}.pdf"))
                pdf.add_files_to_pdf(files = [os.path.join(os.path.expanduser("~/Downloads"), "screenshot-1.png")], target_document = os.path.join(reciepts_path, f"receipt_{order['Order number']}.pdf"), append=True)
                browser.click("id=order-another")
                break
                
            except (AssertionError) as err:
                # reload the page in case of exception
                browser.reload()
                continue

    # archive folder with all receipts and move it to output folder
    archive.archive_folder_with_zip(folder = reciepts_path, archive_name="output/Receipts.zip", recursive=True)

def take_robot_screenshot():
    browser.click("id=preview")
    browser.take_screenshot(filename= os.path.join(os.path.expanduser("~/Downloads"), "screenshot-1"), selector="""xpath=//*[@id="robot-preview-image"]""",fullPage=True)

if __name__ == "__main__":
    try:
        open_website()
        donwload_orders()
        obtain_data_from_excel()
        build_robot()

    finally:
        browser.close_browser()
 
