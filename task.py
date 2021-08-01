"""Template robot with Python."""
"""Template robot with Python."""
import os
from Browser.utils.data_types import ElementState, SelectAttribute
from RPA.HTTP import HTTP
from Browser import Browser
import time

http = HTTP()
browser = Browser()


def open_website():
    browser.open_browser("https://robotsparebinindustries.com/#/robot-order")


def close_popup():
    # browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[2]/div/div""",state="visible")
    browser.click("""xpath=//*[@id="root"]/div/div[2]/div/div/div/div/div/button[1]""")

def build_robot():
    time.sleep(3)
    for i in range(10):
        try:
            close_popup()
            body_number = 4
            browser.select_options_by("id=head",SelectAttribute.label, "Peanut crusher head")
            browser.check_checkbox(f"id=id-body-{body_number}")
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[3]/input""","3")
            browser.type_text("""xpath=/html/body/div/div/div[1]/div/div[1]/form/div[4]/input""","3")
            browser.click("id=order")
            browser.wait_for_elements_state("""xpath=//*[@id="root"]/div/div[1]/div/div[1]/div""", ElementState.visible,timeout=5, message="error")
            
            time.sleep(2)

            browser.click("id=order-another")

        # except (AssertionError) as err:
        #     browser.click("id=order")
        #     browser.click("id=order-another")

        finally:
            print("stop")



    
if __name__ == "__main__":
    open_website()
    build_robot()
 
# <div class="alert alert-danger" role="alert">Guess what? A server Error!</div>