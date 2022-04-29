# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 01:12:49 2021

@author: Tim
"""



# %% Start


# Search form element
search_form_element = driver.wait_for_element_presence("#search-form")

# Elements of all the buttons present on the search form. The first one is the
# "search" button and the second one is the "more options" button
more_options_button = search_form_element.find_elements_by_css_selector("button")


# Click the button and summon the advanced search form
# NOTE: In case we are on the "fewer" search form field there should only be
# two buttons on the page
if len(more_options_button) == 2:
    more_options_button[1].click()


# Find element containing the "death button"
death_button = driver.wait_for_element_clickable("span[name='Death-chip']")
if not death_button.is_selected():
    death_button.click()

# Find the "remove element" buttons of all text input field that are not
# the "death" text input field
remove_event_buttons = driver.find_elements_by_css_selector(
    "button[aria-label^='Remove' i]:not([aria-label*='Death' i])"
)

if len(remove_event_buttons) > 0:
    for button_ in remove_event_buttons:
        button_.click()
        sleep(1)

query_str = ", ".join(
    [self.event_munic, self.event_state, self.event_country]
)

# Enter the query string into the formfield
self.driver.formfield_enter("input[name*='deathLikePlace']", query_str)

# Enter starting date for deathyearh
self.driver.formfield_enter(
    "input[name*='q_deathLikeDate_from']", self.year_from
)

# Enter ending date for deathyearh
self.driver.formfield_enter(
    "input[name*='q_deathLikeDate_to']", self.year_to
)
