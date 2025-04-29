import re
import csv, yaml, time
from playwright.sync_api import sync_playwright

def load_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def read_locations(path="locations.csv"):
    with open(path) as f:
        return list(csv.DictReader(f))

def select_by_text(page, label_text, timeout=10_000):
    """
    Finds the <option> whose text matches label_text, selects it,
    and fires a change event on the <select>.
    """
    page.wait_for_timeout(500)  # tiny pause so dynamic JS can catch up
    page.evaluate(
        """(label) => {
            const opts = Array.from(
              document.querySelectorAll('option')
            ).filter(o => o.textContent.trim() === label);
            if (opts.length === 0)
              throw `Option not found: "${label}"`;
            const opt = opts[0];
            const sel = opt.closest('select');
            sel.value = opt.value;
            sel.dispatchEvent(new Event('change', { bubbles: true }));
        }""",
        label_text,
    )
    # give the form a moment to repopulate
    page.wait_for_timeout(800)

def main():
    cfg      = load_config()
    rows     = read_locations()
    form_url = "https://www.nyc.gov/html/dot/html/contact/contact-form.shtml"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()

        for r in rows:
            # 1) load the page
            page.goto(form_url, wait_until="load")

            # 2) select your three dynamic dropdowns by TEXT, in order
            select_by_text(page, cfg["submission"]["topic"])
            select_by_text(page, cfg["submission"]["place_type"])
            select_by_text(page, cfg["submission"]["borough"])

            # 3) choose the Street-Segment radio button option
            page.locator('input#address-segment-opt').check()
            # 4) Wait for the segment container to appear
            page.wait_for_selector('#detail-address-segment', state='visible', timeout=10_000)


            # 4) PAUSE for you to manually pick the street and cross-streets
            print("\n→ Fill Street / First Cross / Second Cross, then ENTER →")
            input()

            # # 5) Close any open dropdown so the chosen text spans appear
            # page.keyboard.press("Escape")
            # # page.wait_for_selector("ul.select2-results", state="detached", timeout=5_000)
            #
            # # 6) Wait until at least three chosen spans are rendered
            # page.wait_for_function(
            #     "document.querySelectorAll('span.select2-chosen').length >= 3"
            # )
            #
            # # 7) Scrape those spans in order
            # street = page.locator("span.select2-chosen").nth(0).inner_text().strip()
            # first_cross = page.locator("span.select2-chosen").nth(1).inner_text().strip()
            # second_cross = page.locator("span.select2-chosen").nth(2).inner_text().strip()
            #
            # # 6) now interpolate them into your template
            # desc = cfg["submission"]["description_template"].format(
            #     segment=street,
            #     first_cross=first_cross,
            #     second_cross=second_cross)
            #
            # # wait for the textarea by its id
            # page.wait_for_selector('#request_details', timeout=5_000)
            #
            # # fill it by id
            # page.fill('#request_details', desc)

            # — or — fill it by name
            # page.fill('textarea[name="new_privatedescription"]', desc)


            # # 7) fill in case type
            # page.wait_for_selector('select#case-type', timeout=5_000)
            # page.select_option(
            #     'select#case-type',
            #     label="Concern"
            # )

            # 8) fill in contact info
            c = cfg["contact"]
            # wait for the contact section to render
            page.wait_for_selector('#fieldset-contact', timeout=5_000)

            # by id:
            page.fill('#firstname', c["first_name"])
            page.fill('#lastname', c["last_name"])
            page.fill('#user-email', c["email"])
            page.fill('#user-tel', c["phone"])

            # # 9) check "contact about future projects"
            # page.check('input[name="contact_future_projects"]')

            # 10) Mailing zip code
            page.wait_for_selector('#mailingzipcode', timeout=5_000)
            page.fill('#mailingzipcode', c["zip_code"])

            # 7) pause so you can solve the CAPTCHA & click “Send to DOT”
            print(f"\n→ Ready to submit for “{r['segment']}”.")
            print("  1) Solve the reCAPTCHA,")
            print("  2) click “Send to DOT”,")
            print("  3) press ENTER here to continue.")
            input()

        browser.close()

if __name__ == "__main__":
    main()