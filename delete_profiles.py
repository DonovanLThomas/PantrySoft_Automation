from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError, expect
import os
from dotenv import load_dotenv

load_dotenv()

CruzID = os.getenv("CruzID")
Password = os.getenv("PASSWORD")
student_ids = []
with open("Student_IDS.txt") as file:
    for line in file:
        student_ids.append(line.strip())


Pantry_Soft_URL = 'https://app.pantrysoft.com/login/ucsc'

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        page.goto(Pantry_Soft_URL, wait_until="domcontentloaded")

        with page.expect_navigation():
            page.get_by_role("link",name="STUDENTS AND STAFF LOGIN").click()

            page.wait_for_selector("#username", state="visible", timeout=10000)
            page.fill("#username", CruzID)
            page.fill("#password", Password)
            
            page.get_by_role("button", name="Log in").click()

        try:
            page.wait_for_selector("h1#header-text:has-text('Check for a Duo Push')", timeout=5000)

            print("2FA detected, please complete, then resume in inspector browser")
            page.wait_for_url('https://app.pantrysoft.com/client/dashboard/', timeout=12000)
        except PWTimeoutError:
            pass

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
        page.focus("body")
        page.keyboard.press("Escape")
        print("✅ Logged in, ready to automate actions.")

        for id in student_ids:
            search_box = page.get_by_label("Search for Client")
            search_box.fill(id)
            search_box.press("Enter")

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            page.focus("body")
            page.keyboard.press("Escape")

            while True:
                delete_note = page.get_by_role("button", name="Delete").first
                try:
                    delete_note.wait_for(state="visible", timeout=700)
                except PWTimeoutError:
                    break
                delete_note.click()

                delete_button = page.locator("button.btn.btn-lg.btn-ps-danger")
                delete_button.hover()
                page.mouse.down()
                page.wait_for_timeout(2000)
                page.mouse.up()
            

            
            while True:
                delete_visit = page.get_by_alt_text("Edit Visit").first
                try:
                    delete_visit.wait_for(state="visible", timeout=700)
                except PWTimeoutError:
                    break

                delete_visit.click()
                page.get_by_role("button", name="Delete").first.click()

                delete_button = page.locator("button.btn.btn-lg.btn-ps-danger")
                delete_button.hover()
                page.mouse.down()
                page.wait_for_timeout(2000)
                page.mouse.up()
            
            delete_registration = page.get_by_alt_text("Edit Last Registration")
            try:
                delete_registration.wait_for(state="visible", timeout=700)
                delete_registration.click()

                page.get_by_role("button", name="Delete").first.click()

                delete_button = page.locator("button.btn.delete-button").first
                delete_button.hover()
                page.mouse.down()
                page.wait_for_timeout(2000)
                page.mouse.up()
            except PWTimeoutError:
                pass

            try:
                profile_edit = page.locator("#edit_client_since_button")
                profile_edit.wait_for(state="visible", timeout=1000)
                profile_edit.click()

                delete_profile = page.locator("#pantrybundle_client_delete")
                delete_profile.wait_for(state="visible", timeout=1000)
                delete_profile.click()

                buttons = page.locator("button.btn.delete-button")
                delete_confirm = buttons.nth(2)
                expect(delete_confirm).to_be_visible(timeout=5000)

                delete_confirm.hover()
                page.mouse.down()
                page.wait_for_timeout(2000)
                page.mouse.up()
                print(f"Student:{id} was deleted\n")
            except PWTimeoutError:
                print(f"Unable to delete Student:{id}")
                pass




if __name__ == "__main__":
    run()