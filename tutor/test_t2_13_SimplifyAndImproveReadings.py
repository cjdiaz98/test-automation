"""Tutor v2, Epic 13 - Simplify and Improve Readings."""

import inspect
import json
import os
import pytest
import unittest
import datetime

from pastasauce import PastaSauce, PastaDecorator
from random import randint
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from staxing.assignment import Assignment

# select user types: Admin, ContentQA, Teacher, and/or Student
from staxing.helper import Teacher, Student

basic_test_env = json.dumps([{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': 'latest',
    'screenResolution': "1024x768",
}])
BROWSERS = json.loads(os.getenv('BROWSERS', basic_test_env))
LOCAL_RUN = os.getenv('LOCALRUN', 'false').lower() == 'true'
TESTS = os.getenv(
    'CASELIST',
    str([
        100127
        # 14745, 14746, 85291, 100126, 100127,
        # 100128
    ])
)


@PastaDecorator.on_platforms(BROWSERS)
class TestSimplifyAndImproveReadings(unittest.TestCase):
    """T2.13 - Simplify and Improve Readings."""

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
                existing_driver=self.teacher.driver,
                use_env_vars=True,
                pasta_user=self.ps,
                capabilities=self.desired_capabilities
            )
        else:
            self.teacher = Teacher(
                use_env_vars=True,
            )
            self.student = Student(
                existing_driver=self.teacher.driver,
                use_env_vars=True,
            )

    def tearDown(self):
        """Test destructor."""
        if not LOCAL_RUN:
            self.ps.update_job(
                job_id=str(self.teacher.driver.session_id),
                **self.ps.test_updates
            )
        self.student = None
        try:
            self.teacher.delete()
        except:
            pass

    def create_a_reading_and_click_on_it(self):
        """
        Login as a teacher and create a reading, then logout
        Login as a student and click on the reading
        """
        # create a reading for the student to work
        self.teacher.login()
        course = self.teacher.find(
            By.XPATH, '//div[@data-title="College Physics with Courseware"]')
        course_id = course.get_attribute('data-course-id')
        course.click()
        self.teacher.sleep(4)
        self.assignment_name = 't1.13 reading-%s' % randint(100, 999)
        today = datetime.date.today()
        begin = today.strftime('%m/%d/%Y')
        end = (today + datetime.timedelta(days=randint(1, 10))) \
            .strftime('%m/%d/%Y')
        self.teacher.add_assignment(
            assignment='reading',
            args={
                'title': self.assignment_name,
                'description': 'description',
                'periods': {'all': (begin, end)},
                'reading_list': ['1.1', '1.2'],
                'status': 'publish',
            }
        )
        self.teacher.wait.until(
            expect.visibility_of_element_located(
                (By.XPATH, '//div[contains(@class,"calendar-container")]')
            )
        )
        self.teacher.logout()
        # login as a student to work the reading
        self.student.login()
        print(course_id)
        self.student.find(
            By.XPATH, "//div[@data-course-id='" + course_id + "']"
        ).click()
        self.student.wait.until(
            expect.visibility_of_element_located(
                (By.LINK_TEXT, 'This Week')
            )
        )
        reading = self.student.driver.find_element(
            By.XPATH,
            '//div[text()="%s"]' % self.assignment_name
        )
        self.teacher.driver.execute_script(
            'return arguments[0].scrollIntoView();',
            reading
        )
        self.teacher.driver.execute_script('window.scrollBy(0, -80);')
        reading.click()

    # 14745 - 001 - Student | Relative size and progress are displayed while
    # working a reading assignment
    @pytest.mark.skipif(str(14745) not in TESTS, reason='Excluded')
    def test_student_relative_size_and_progress_are_displayed_whil_14745(self):
        """Size and progress are displayed while working a reading.

        Steps:
        Go to Tutor
        Click on the 'Login' button
        Enter the student user account in the username and password text boxes
        Click on the 'Sign in' button
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the right arrow

        Expected Result:
        The progress bar at the top reflects how far along you are as you work
        through the reading assignment
        """
        self.ps.test_updates['name'] = 't2.13.001' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.001', '14745']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.create_a_reading_and_click_on_it()
        self.student.driver.find_element(
            By.XPATH,
            '//div[contains(@class,"progress-bar progress-bar-success")]')

        self.ps.test_updates['passed'] = True

    # 14746 - 002 - Student | Access prior milestones in the reading assignment
    # with breadcrumbs
    @pytest.mark.skipif(str(14746) not in TESTS, reason='Excluded')
    def test_student_access_prior_milestones_in_the_reading_assign_14746(self):
        """Access prior milestones in the reading assignment with breadcrumbs.

        Steps:
        If the user has more than one course, click on a Tutor course name
        Click on a reading assignment
        Click on the icon next to the calendar on the header

        Expected Result:
        The user is presented with prior milestones
        """
        self.ps.test_updates['name'] = 't2.13.002' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.13', 't2.13.002', '14746']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.create_a_reading_and_click_on_it()
        self.student.find(By.XPATH, '//a[@class="milestones-toggle"]').click()
        self.student.find(
            By.XPATH, '//div[contains(@class,"milestone-reading")]'
        )
        self.ps.test_updates['passed'] = True

    # C85291 - 003 - Student | Reading Review card appears before the first
    # spaced practice question
    @pytest.mark.skipif(str(85291) not in TESTS, reason='Excluded')
    def test_student_reading_review_card_appears_before_first_spac_85291(self):
        """Reading Review card appears before first spaced practice question.

        Steps:
        Login as student
        Work the reading assignment
        After completing reading the sections you get a spaced practice problem

        Expected Result:
        The reading review card should appear before the first spaced practice
            question
        """
        self.ps.test_updates['name'] = 't2.08.003' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.003', '85291']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C100126 - 004 - Student | Section number is seen at the beginning of each
    # new section in a reading assignment
    @pytest.mark.skipif(str(100126) not in TESTS, reason='Excluded')
    def test_student_section_number_is_seen_st_the_beginning_of_e_100126(self):
        """Section number is seen at the beginning of each new section in a
        reading assignment.

        Steps:
        Login as a student
        Click on a tutor course
        Click on a reading assignment
        Continue to work through reading assignment

        Expected Result:
        At the start of each new section, the section number is displayed
        """
        self.ps.test_updates['name'] = 't2.08.004' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.004', '100126']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        raise NotImplementedError(inspect.currentframe().f_code.co_name)

        self.ps.test_updates['passed'] = True

    # C100127 - 005 - Teacher | Section numbers are listed at the top of each
    # section in reference view
    @pytest.mark.skipif(str(100127) not in TESTS, reason='Excluded')
    def test_student_section_numbers_listed_at_the_top_of_each_se_100127(self):
        """Section numbers listed at the top of each section in reference view.

        Steps:
        Login as teacher
        Click on a tutor course
        Click "Browse the Book" or select "Browse the Book" from the user menu
        Select a section from the contents

        Expected Result:
        Section number listed in header
        """
        self.ps.test_updates['name'] = 't2.08.005' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.005', '100127']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.teacher.login()
        self.teacher.find(
            By.XPATH, '//div[@data-title="College Physics with Courseware"]'
        ).click()
        book = self.teacher.find(
            By.XPATH, '//a[text()="Browse the Book"]')
        Assignment.scroll_to(self.teacher.driver, book)
        book.click()
        window_with_book = self.teacher.driver.window_handles[1]
        self.teacher.driver.switch_to_window(window_with_book)
        assert('book' in self.teacher.current_url()), \
            'Not viewing the textbook PDF'
        self.teacher.find(
            By.XPATH, '//li[@data-section="1.1"]'
        ).click()
        self.teacher.find(
            By.XPATH, '//h4//span[text()="1.1"]'
        ).click()

        self.ps.test_updates['passed'] = True

    # C100128 - 006 - Student | Section numbers are listed at the top of each
    # section in reference view
    @pytest.mark.skipif(str(100128) not in TESTS, reason='Excluded')
    def test_student_section_numbers_listed_at_the_top_of_each_se_100128(self):
        """Section numbers listed at the top of each section in reference view.

        Steps:
        Login as student
        Click on a tutor course
        Click "Browse the Book" or select "Browse the Book" from the user menu
        Select a section from the contents

        Expected Result:
        Section number listed in header
        """
        self.ps.test_updates['name'] = 't2.08.006' \
            + inspect.currentframe().f_code.co_name[4:]
        self.ps.test_updates['tags'] = ['t2', 't2.08', 't2.08.006', '100128']
        self.ps.test_updates['passed'] = False

        # Test steps and verification assertions
        self.student.login()
        self.student.find(
            By.XPATH, '//div[@data-title="College Physics with Courseware"]'
        ).click()
        book = self.student.find(
            By.XPATH, '//a[text()="Browse the Book"]')
        Assignment.scroll_to(self.student.driver, book)
        book.click()
        window_with_book = self.student.driver.window_handles[1]
        self.student.driver.switch_to_window(window_with_book)
        assert('book' in self.student.current_url()), \
            'Not viewing the textbook PDF'
        self.student.find(
            By.XPATH, '//li[@data-section="1.1"]'
        ).click()
        self.student.find(
            By.XPATH, '//h4//span[text()="1.1"]'
        ).click()

        self.ps.test_updates['passed'] = True
