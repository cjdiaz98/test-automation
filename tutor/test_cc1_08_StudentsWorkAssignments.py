"""Concept Coach v1, Epic 08 - Students Work Assignments."""

import inspect
import json
import os
import pytest
import unittest

from autochomsky import chomsky
from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect  # NOQA
from staxing.assignment import Assignment
from staxing.helper import Teacher, Student  # NOQA
from selenium.webdriver import ActionChains  # NOQA

basic_test_env = json.dumps([{
    'platform': 'Windows 10',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1280x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        7691
        # 7691, 7692, 7693, 7694, 7695,
        # 7696, 7697, 7698, 7699, 7700,
        # 7701, 7702, 100131, 100132
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestStudentsWorkAssignments(unittest.TestCase):
    """CC1.08 - Students Work Assignments."""

    def setUp(self):
        """Pretest settings."""
        self.ps = PastaSauce()
        self.desired_capabilities['name'] = self.id()
        if not LOCAL_RUN:
            self.teacher = Teacher(
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True,
            )
            self.student = Student(
                use_env_vars=True,
                existing_driver=self.teacher.driver,
            )
        self.student.login()
        self.student.driver.find_element(
            By.XPATH,
            '//p[contains(text(),"OpenStax Concept Coach")]'
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[@class="go-now"]')
            )
        ).click()

        # self.teacher.login()
        # self.teacher.driver.find_element(
        #     By.XPATH,
        #     '//p[contains(text(),"OpenStax Concept Coach")]'
        # ).click()
        # self.teacher.goto_course_roster()
        # try:
        #     section = self.teacher.find_all(
        #         By.XPATH,
        #         '//*[contains(@class,"nav-tabs")]//a'
        #     )
        #     if isinstance(section, list):
        #         section = '%s' % section[randint(0, len(section) - 1)].text
        #     else:
        #         section = '%s' % section.text
        # except Exception:
        #     section = '%s' % randint(100, 999)
        #     self.teacher.add_course_section(section)
        # self.code = self.teacher.get_enrollment_code(section)
        # print('Course Phrase: ' + self.code)
        # self.book_url = self.teacher.find(
        #     By.XPATH, '//a[span[contains(text(),"Online Book")]]'
        # ).get_attribute('href')
        # self.teacher.find(By.CSS_SELECTOR, 'button.close').click()
        # self.teacher.sleep(0.5)
        # self.teacher.logout()
        # self.teacher.sleep(1)
        # self.student = Student(use_env_vars=True,
        #                        existing_driver=self.teacher.driver)
        # self.first_name = Assignment.rword(6)
        # self.last_name = Assignment.rword(8)
        # self.email = self.first_name + '.' \
        #     + self.last_name \
        #     + '@tutor.openstax.org'

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        try:
            self.teacher.delete()
        except:
            pass

    # Case C7691 - 001 - Student | Selects an exercise answer
    @pytest.mark.skipif(str(7691) not in TESTS, reason='Excluded')
    def test_student_select_an_exercise_answer_7691(self):
        """Select an exercise answer.

        Steps:
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click the 'Answer' button
        Click a multiple choice answer

        Expected Result:
        The 'Submit' button is now clickable.
        """
        self.ps.test_updates['name'] = 'cc1.08.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.001',
            '7691'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[text()="Contents"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//span[@class="chapter-number" and text()="1.1"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//a[text()="Jump to Concept Coach"]')
            )
        ).click()
        # self.student.driver.find_element(
        #     By.XPATH, '//a[text()="Jump to Concept Coach"]'
        # ).click()
        self.student.sleep(0.5)
        self.student.driver.find_element(
            By.XPATH, '//button[text()="Launch Concept Coach"]'
        ).click()
        # click on an answer
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="openstax-answer"]')
            )
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//button[text()="Submit"]')
            )
        ).click()
        self.student.sleep(1)
        # check that answer was selected
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH,
                 '//div[@class="has-correct-answer"]')
            )
        )
        self.ps.test_updates['passed'] = True

    # Case C7692 - 002 - Student | After answering an exercise feedback
    # is presented
    @pytest.mark.skipif(str(7692) not in TESTS, reason='Excluded')  # NOQA
    def test_student_after_answering_an_exercise_feedback_7692(self):
        """View section completion report.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the teacher user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click the 'Answer' button
        Click a multiple choice answer
        Click the 'Submit' button

        Expected Result:
        The correct answer is displayed and feedback is given.
        """
        self.ps.test_updates['name'] = 'cc1.08.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.002',
            '7692'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        # //span[@class='title section']
        # get the 21 drop downs in toc

        #    By.PARTIAL_LINK_TEXT, "Macro Econ").click()
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        finished = False

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' not in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                self.student.find(
                    By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']"
                ).click()
                self.student.sleep(2)
                self.student.find(
                    By.XPATH, "//button[@class='btn btn-lg btn-primary']"
                ).click()
                self.student.sleep(2)

                # If this section has been completed already,
                # leave and go to the next section
                breadcrumbs = self.student.driver.find_elements_by_xpath(
                    "//div[@class='task-breadcrumbs']/span")

                breadcrumbs[-1].click()
                self.student.sleep(3)

                if len(self.student.driver.find_elements_by_xpath(
                    "//div[@class='card-body coach-coach-review-completed'][1]"
                )) > 0:
                    self.student.find(
                        By.XPATH,
                        "//a/button[@class='btn-plain " +
                        "-coach-close btn btn-default']").click()

                # Else, go through questions until a blank one is found
                # and answer the question
                else:
                    for question in breadcrumbs:
                        question.click()

                        if len(self.student.driver.find_elements_by_xpath(
                            "//div[@class='question-feedback bottom']"
                        )) > 0:
                            continue

                        else:
                            while len(
                                self.student.driver.find_elements_by_xpath(
                                    "//div[@class='question-feedback bottom']"
                                )
                            ) == 0:

                                if len(
                                    self.student.driver.find_elements_by_xpath(
                                        "//button[@class='btn btn-default']"
                                    )
                                ) > 0:
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='btn btn-default']"
                                    ).click()
                                    continue

                                # Free response
                                if self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Answer':
                                    self.student.find(
                                        By.XPATH,
                                        "//textarea").send_keys(
                                        'An answer for this textarea')
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='async-button " +
                                        "continue btn btn-primary']"
                                    ).click()
                                    self.student.sleep(3)

                                # Multiple Choice
                                elif self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Submit':
                                    answers = self.student.driver.find_elements(  # NOQA
                                        By.CLASS_NAME, 'answer-letter')
                                    self.student.sleep(0.8)
                                    rand = randint(0, len(answers) - 1)
                                    answer = chr(ord('a') + rand)
                                    Assignment.scroll_to(
                                        self.student.driver, answers[0])
                                    if answer == 'a':
                                        self.student.driver.execute_script(
                                            'window.scrollBy(0, -160);')
                                    elif answer == 'd':
                                        self.student.driver.execute_script(
                                            'window.scrollBy(0, 160);')
                                    answers[rand].click()

                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='async-button " +
                                        "continue btn btn-primary']"
                                    ).click()
                                    self.student.sleep(3)

                                    finished = True

                        break

            if finished:
                break

        self.student.sleep(5)
        self.student.find(
            By.XPATH, "//div[@class='question-feedback bottom']")

        self.ps.test_updates['passed'] = True

    # Case C7693 - 003 - System | Assessments are from the current module
    @pytest.mark.skipif(str(7693) not in TESTS, reason='Excluded')  # NOQA
    def test_system_assessments_are_from_the_current_module_7693(self):
        """Assessment is from the current module.

        Steps:


        Expected Result:
        """
        self.ps.test_updates['name'] = 'cc1.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.003',
            '7693'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7694 - 004 - System | Spaced practice assessments are from
    # previously worked modules
    @pytest.mark.skipif(str(7694) not in TESTS, reason='Excluded')  # NOQA
    def test_system_spaced_practice_assessments_are_from_previo_7694(self):
        """Spaced practice assessments are from previousy worked modules.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Select a non-introductory section
        Click Jump to Concept Coach
        Click Launch Concept Coach
        Go through the assessments until you get to the Spaced Practice

        Expected Result:
        The section number beneath the text box is from a previous section
        """
        self.ps.test_updates['name'] = 'cc1.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.004',
            '7694'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7695 - 005 - System | Modules without assessments do not display
    # the Concept Coach widget
    @pytest.mark.skipif(str(7695) not in TESTS, reason='Excluded')  # NOQA
    def test_system_modules_without_assessments_do_not_display_7695(self):
        """Module without assessments does not display the CC widget.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on an introductory section

        Expected Result:
        The Concept Coach widget does not appear.
        """
        self.ps.test_updates['name'] = 'cc1.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.005',
            '7695'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                count = self.student.driver.find_elements_by_xpath(
                    "//div[@class='jump-to-cc']/a[@class='btn']"
                )
                self.student.sleep(2)

                assert (len(count) == 0), "Intro should not have CC widget"
                break

        self.ps.test_updates['passed'] = True

    # Case C7696 - 006 - Student | Assignment is assistive technology friendly
    @pytest.mark.skipif(str(7696) not in TESTS, reason='Excluded')  # NOQA
    def test_student_assignment_is_assistive_technology_friendly_7696(self):
        """Assignment is assistive technology friendly.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click the 'Answer' button
        Type a, b, c, or d

        Expected Result:
        A multiple choice answer matching the letter typed should be selected.
        """
        self.ps.test_updates['name'] = 'cc1.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.006',
            '7696'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        finished = False

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' not in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                self.student.find(
                    By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']"
                ).click()
                self.student.sleep(2)
                self.student.find(
                    By.XPATH, "//button[@class='btn btn-lg btn-primary']"
                ).click()
                self.student.sleep(2)

                # If this section has been completed already,
                # leave and go to the next section
                breadcrumbs = self.student.driver.find_elements_by_xpath(
                    "//div[@class='task-breadcrumbs']/span")

                breadcrumbs[-1].click()
                self.student.sleep(3)

                if len(self.student.driver.find_elements_by_xpath(
                    "//div[@class='card-body coach-coach-review-completed'][1]"
                )) > 0:
                    self.student.find(
                        By.XPATH,
                        "//a/button[@class='btn-plain " +
                        "-coach-close btn btn-default']").click()

                # Else, go through questions until a blank one is found
                # and answer the question
                else:
                    for question in breadcrumbs:
                        question.click()

                        if len(self.student.driver.find_elements_by_xpath(
                            "//div[@class='question-feedback bottom']"
                        )) > 0:
                            continue

                        else:
                            while len(
                                self.student.driver.find_elements_by_xpath(
                                    "//div[@class='question-feedback bottom']"
                                )
                            ) == 0:

                                if len(
                                    self.student.driver.find_elements_by_xpath(
                                        "//button[@class='btn btn-default']"
                                    )
                                ) > 0:
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='btn btn-default']"
                                    ).click()
                                    continue

                                # Free response
                                if self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Answer':
                                    self.student.find(
                                        By.XPATH,
                                        "//textarea").send_keys(
                                        'An answer for this textarea')
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='async-button " +
                                        "continue btn btn-primary']"
                                    ).click()
                                    self.student.sleep(3)

                                # Multiple Choice
                                elif self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Submit':
                                    action = ActionChains(self.student.driver)
                                    action.send_keys('c')
                                    action.perform()

                                    self.student.find(
                                        By.XPATH,
                                        "//div[@class='answers-answer " +
                                        "answer-checked']"
                                    )
                                    self.student.sleep(3)

                                    finished = True
                                    break

                        break

            if finished:
                break

        self.student.sleep(5)

        self.student.sleep(3)

        self.ps.test_updates['passed'] = True

    # Case C7697 - 007 - Student | Display the assignment summary
    # after completing the assignment
    @pytest.mark.skipif(str(7697) not in TESTS, reason='Excluded')  # NOQA
    def test_student_display_the_assignment_summary_after_completin_7697(self):
        """Display the assignment summary after completing the assignment.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button
        After answering the last question, click the 'Next Question' button

        Expected Result:
        The summary is displayed
        """
        self.ps.test_updates['name'] = 'cc1.08.007' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.007',
            '7697'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        finished = False

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' not in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                self.student.find(
                    By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']"
                ).click()
                self.student.sleep(2)
                self.student.find(
                    By.XPATH, "//button[@class='btn btn-lg btn-primary']"
                ).click()
                self.student.sleep(2)

                # If this section has been completed already,
                # leave and go to the next section
                breadcrumbs = self.student.driver.find_elements_by_xpath(
                    "//div[@class='task-breadcrumbs']/span")

                breadcrumbs[-1].click()
                self.student.sleep(3)

                if len(self.student.driver.find_elements_by_xpath(
                    "//div[@class='card-body coach-coach-review-completed'][1]"
                )) > 0:
                    self.student.find(
                        By.XPATH,
                        "//a/button[@class='btn-plain " +
                        "-coach-close btn btn-default']").click()

                # Else, go through questions until a blank one is found
                # and answer the question
                else:
                    for question in breadcrumbs:
                        question.click()

                        if len(self.student.driver.find_elements_by_xpath(
                            "//div[@class='question-feedback bottom']"
                        )) > 0:
                            if len(self.student.driver.find_elements_by_xpath(
                                "//div[@class='card-body coach-" +
                                "coach-review-completed'][1]"
                            )) > 0:
                                finished = True
                            continue

                        else:
                            while len(
                                self.student.driver.find_elements_by_xpath(
                                    "//div[@class='question-feedback bottom']"
                                )
                            ) == 0:
                                # Free response

                                if len(
                                    self.student.driver.find_elements_by_xpath(
                                        "//button[@class='btn btn-default']"
                                    )
                                ) > 0:
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='btn btn-default']"
                                    ).click()
                                    continue

                                if self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Answer':
                                    self.student.find(
                                        By.XPATH,
                                        "//textarea").send_keys(
                                        'An answer for this textarea')
                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='async-button " +
                                        "continue btn btn-primary']"
                                    ).click()
                                    self.student.sleep(3)

                                # Multiple Choice
                                elif self.student.find(
                                    By.XPATH,
                                    "//button[@class='async-button " +
                                    "continue btn btn-primary']"
                                ).text == 'Submit':
                                    answers = self.student.driver.find_elements(  # NOQA
                                        By.CLASS_NAME, 'answer-letter')
                                    self.student.sleep(0.8)
                                    rand = randint(0, len(answers) - 1)
                                    answer = chr(ord('a') + rand)
                                    Assignment.scroll_to(
                                        self.student.driver, answers[0])
                                    if answer == 'a':
                                        self.student.driver.execute_script(
                                            'window.scrollBy(0, -160);')
                                    elif answer == 'd':
                                        self.student.driver.execute_script(
                                            'window.scrollBy(0, 160);')
                                    answers[rand].click()

                                    self.student.find(
                                        By.XPATH,
                                        "//button[@class='async-button " +
                                        "continue btn btn-primary']"
                                    ).click()
                                    self.student.sleep(3)

            if finished:
                break

        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C7698 - 008 - Student | The exercise ID is visible within
    # the assessment pane
    @pytest.mark.skipif(str(7698) not in TESTS, reason='Excluded')  # NOQA
    def test_student_exercise_id_is_visible_within_the_assessment_7698(self):
        """The exercise ID is visible within the assessment pane.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a CC course name
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page

        Expected Result:
        The exercise ID is visivle on the exercise.
        """
        self.ps.test_updates['name'] = 'cc1.08.008' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.008',
            '7698'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' not in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                self.student.find(
                    By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']"
                ).click()
                self.student.sleep(2)
                self.student.find(
                    By.XPATH, "//button[@class='btn btn-lg btn-primary']"
                ).click()
                self.student.sleep(2)

                # View summary
                breadcrumbs = self.student.driver.find_elements_by_xpath(
                    "//div[@class='task-breadcrumbs']/span")

                breadcrumbs[-1].click()
                self.student.sleep(3)

                # Verify the first question has an exercise ID
                breadcrumbs[2].click()

                self.student.find(
                    By.XPATH,
                    "//span[@class='exercise-identifier-link']/span[2]")

                break

        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C7699 - 009 - Student | Able to refer an assessment to OpenStax
    # via Errata Form
    @pytest.mark.skipif(str(7699) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_refer_an_assessment_to_openstax_7699(self):
        """Able to refer to an assessment to OpenStax via Errata form.

        Steps:
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Click the 'Report an error' link

        Expected Result:
        User is taken to the Errata form with the exercise ID prefilled
        """
        self.ps.test_updates['name'] = 'cc1.08.009' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.009',
            '7699'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.select_course(appearance='macro_economics')
        self.student.sleep(5)
        self.student.find(By.XPATH, "//button[@class='toggle btn']").click()
        self.student.sleep(3)

        # Expand all the chapters in the table of contents
        chapters = self.student.driver.find_elements_by_xpath(
            "//span[@class='title section']")
        chapters.pop(0)
        for chapter in chapters:
            chapter.click()

        # Get all sections, excluding the preface
        sections = self.student.driver.find_elements_by_xpath(
            "//a/span[@class='title']")
        sections.pop(0)

        self.student.sleep(2)

        length = len(sections)

        for num in range(length):

            sections = self.student.driver.find_elements_by_xpath(
                "//a/span[@class='title']")
            sections.pop(0)
            sections[num].click()
            self.student.sleep(3)

            if 'Introduction-to' not in self.student.current_url():
                # Jump to the Concept Coach widget and open Concept Coach
                self.student.find(
                    By.XPATH, "//div[@class='jump-to-cc']/a[@class='btn']"
                ).click()
                self.student.sleep(2)
                self.student.find(
                    By.XPATH, "//button[@class='btn btn-lg btn-primary']"
                ).click()
                self.student.sleep(2)

                # View summary
                breadcrumbs = self.student.driver.find_elements_by_xpath(
                    "//div[@class='task-breadcrumbs']/span")

                breadcrumbs[-1].click()
                self.student.sleep(3)

                # Verify the first question has an exercise ID
                breadcrumbs[2].click()

                self.student.find(
                    By.XPATH,
                    "//span[@class='exercise-identifier-link']/a"
                ).click()

                self.student.driver.switch_to.window(
                    self.student.driver.window_handles[-1])

                assert("google" in self.student.current_url()), \
                    'Not viewing the errata form'

                break

        self.student.sleep(5)

        self.ps.test_updates['passed'] = True

    # Case C7700 - 010 - Student | Able to work an assignment on an
    # Apple tablet device
    @pytest.mark.skipif(str(7700) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_an_apple_tablet_7700(self):
        """Able to work an assignment on an Apple tablet device.

        Steps:
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button

        Expected Result:
        Answer is successfully submitted.
        """
        self.ps.test_updates['name'] = 'cc1.08.010' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.010',
            '7700'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7701 - 011 - Student | Able to work an assignment on an
    # Android tablet device
    @pytest.mark.skipif(str(7701) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_android_tablet_7701(self):
        """Able to work an assignment on an Android tablet device.

        Steps:
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button

        Expected Result:
        Answer is successfully submitted.
        """
        self.ps.test_updates['name'] = 'cc1.08.011' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.011',
            '7701'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C7702 - 012 - Student | Able to work an assignment on a
    # Windows tablet device
    @pytest.mark.skipif(str(7701) not in TESTS, reason='Excluded')  # NOQA
    def test_student_able_to_work_an_assignment_on_windows_tablet_7702(self):
        """Able to work an assignment on a WIndows tablet device.

        Steps:
        Click the 'Contents' button to open the table of contents
        Click on a chapter
        Click on a non-introductory section
        Click the 'Launch Concept Coach' button at the bottom of the page
        Type text into the 'Enter your response' text box
        Click a multiple choice answer
        Click the 'Submit' button

        Expected Result:
        Answer is successfully submitted.
        """
        self.ps.test_updates['name'] = 'cc1.08.012' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.012',
            '7702'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    '''
    # Case C7703 - 013 - Student | Sees product error modals
    @pytest.mark.skipif(str(7703) not in TESTS, reason='Excluded')  # NOQA
    def test_student_sees_product_error_modals_7703(self):
        """See product error modals.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.08.013' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.013',
            '7703'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
    '''

    # Case C100131 - 014 - Student | Work a two-step assessment
    @pytest.mark.skipif(str(100131) not in TESTS, reason='Excluded')  # NOQA
    def test_student_work_a_two_step_assessment_100131(self):
        """Work a two-step assessment.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.08.014' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.014',
            '100131'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # Case C100132 - 015 - Student | Work a multiple-choice-only assessment
    @pytest.mark.skipif(str(100131) not in TESTS, reason='Excluded')  # NOQA
    def test_student_work_a_multiple_choice_only_assessment_100132(self):
        """Work a multiple-choice-only assessment.

        Steps:


        Expected Result:

        """
        self.ps.test_updates['name'] = 'cc1.08.015' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = [
            'cc1',
            'cc1.08',
            'cc1.08.015',
            '100131'
        ]
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True
