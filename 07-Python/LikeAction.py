from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
from selenium.webdriver.chrome.options import Options
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


class LikeAction:
    BASE_URL = 'http://saha.moi.ir/'
    BASE_WINDOW = None
    item_count = 0
    item_reset_count = 20
    max_unsed_post_count = 200
    IS_LOGGED_IN = False
    posts = None
    user_profile_id = 'profile-42137'
    each_post_max_comment = 30

    def __init__(self, url, username, password, item_reset_count, max_unsed_post_count, user_profile_id, headless=True):
        self.BASE_URL = url
        self.username = username
        self.password = password,
        self.item_reset_count = item_reset_count
        self.max_unsed_post_count = max_unsed_post_count
        self.user_profile_id = user_profile_id
        self.headless = headless
        self.driver = self.create_driver()
        print('starting ...')

    def random_comment(self):
        comments = [
            'درود',
            # 'سپاس',
            # 'متشکرم',
            # 'خداقوت',
            '✔️',
            '🙏🏻',
            '🙏🏻🙏🏻',
            # '🙏🏻🙏🏻🙏🏻',
            '✅️',
            '👍🏻',
            '👍🏻👍🏻',
            # '👍🏻👍🏻👍🏻',
            # 'تشکر',
            # 'درود بر شما',
            # 'ممنون',
            '👌',
            '👌👌',
            # 'تشکر از ارائه مطالب ارزنده شما',
            # ' ممنون از مطالب خوبتون',
            # 'آموزنده بود',
            'سپاس',
            # 'احسنت',
            'خداقوت',
            'بسیار عالی',
            # 'جالب بود',
            # 'ممنون از اشتراک گذاری'
        ]
        _ = ''
        for i in range(random.choice([1, 2])):
            selected = random.choice(comments).strip()
            if selected == _.strip():
                continue
            _ += f' {selected}'
            _ = _.strip()
        return _

    def init_posts(self):
        return pd.DataFrame(columns=['id', 'element', 'href', 'done'])

    def create_driver(self):
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('ignore-certificate-errors')

        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=Service(
            "/usr/bin/chromedriver"), options=options)
        driver.set_window_size(700, 800)
        driver.set_window_position(900, 100, windowHandle='current')
        return driver

    def refresh_page(self):
        self.driver.refresh()

    def auto_login(self):
        self.driver.get(self.BASE_URL)
        self.driver.find_element(By.ID, "login").send_keys(self.username)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "loginbtn").click()
        self.IS_LOGGED_IN = True
        print('successfully logined ... \n')

    def set_base_window(self):
        self.BASE_WINDOW = self.driver.current_window_handle

    def scroll_bottom(self):
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def print_board(self):
        message = f'| completed ==> {len(self.posts)} post | {self.item_count} like |'
        print('-'*len(message))
        print(message)
        print('-'*len(message))
        print('->load more posts ...')
        time.sleep(1)

    def get_comment_parent_id(self, comment):
        return self.driver.execute_script("""
                                function findAncestor (el, sel) {
                                    while ((el = el.parentElement) && !((el.matches || el.matchesSelector).call(el,sel)));
                                    return el;
                                }
                                
                                function parent_id(comment){
                                    try {
                                        return findAncestor(comment,'.js_mini_feed_comment')
                                        .querySelector('.comment_mini_content')
                                        .querySelector(".user_profile_link_span>a")
                                        .getAttribute('href').split('/')[3]
                                        }
                                        catch(err) {
                                            return null
                                        }
                                }
                                return parent_id(arguments[0])
                                """, comment)

    def get_root_child_comment(self, comment_id):
        try:
            return self.driver.execute_script("""
                                return document.querySelectorAll(`#js_comment_children_holder_${arguments[0]} > [id*="js_comment_"]`)
                                """, comment_id)
        except Exception:
            return None

    def get_comment_id(self, comment):
        try:
            return self.driver.execute_script("""
            return arguments[0].getAttribute('id')
            """, comment).split('_')[-1]
        except Exception:
            return None

    def get_comment_user_id(self, comment):
        try:
            return self.driver.execute_script("""
            user = arguments[0].querySelector(".user_profile_link_span>a")
            return user.getAttribute('href')
            """, comment).split('/')[-2]
        except Exception:
            return None

    def open_new_page(self, url):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url)

    def reset_max_item_handler(self):
        self.print_board()
        print('item_count reset fire ....')
        self.driver.close()
        self.driver.switch_to.window(self.BASE_WINDOW)
        self.reset()
        return self.get_score()

    def reply_comment(self, comment):

        try:
            comment_id = self.get_comment_id(comment)
            user_id = self.get_comment_user_id(comment)

            if user_id == self.user_profile_id or self.is_replied(comment_id):
                return
            self.driver.execute_script(
                f'arguments[0].querySelector(".js_comment_feed_new_reply").click()', comment)
            self.driver.execute_script("""
                textarea = arguments[0].querySelector(".js_comment_feed_textarea.spmentionRes")
                textarea.value = arguments[1]
                arguments[0].querySelector(".js_feed_add_comment_button> input").click()
                """, comment, self.random_comment())
            # arguments[0].querySelector(".js_feed_add_comment_button> input").click()
            print(f'comment inserted parent: {comment.getAttribute("id")}')
            self.item_count += 1
        except Exception:
            return

    def get_root_comment_post(self):
        try:
            return self.driver.find_elements(
            By.CSS_SELECTOR, '[id*="js_feed_comment_post_"] > div > [id*="js_comment_"]')
        except Exception:
            return None

    def get_current_post_user_id(self):
        try:
            url = self.driver.execute_script(
            "return document.querySelector('.user_profile_link_span > a').getAttribute('href')")
            return url.split('/')[-2]
        except Exception:
            return None

    def write_comment(self):
        try:
            if self.get_current_post_user_id() == self.user_profile_id:
                return False
            root_comments = self.get_root_comment_post()
            is_write_root_commente = False
            for comment in root_comments:
                user_id = self.get_comment_user_id(comment)
                if user_id == self.user_profile_id:
                    is_write_root_commente = True

            if not is_write_root_commente:
                self.driver.execute_script("""
                textarea = document.querySelector('textarea[id*="js_feed_comment_form_textarea_"]')
                textarea.value = arguments[0]
                document.querySelector('[id*="comment_form"] > div.feed_comment_buttons_wrap > div > input').click()
                """,  self.random_comment())
            
            self.item_count += 1
        except Exception:
            return None

    def is_replied(self, comment_id):
        childs = self.get_root_child_comment(comment_id)
        for child in childs:
            user_id = self.get_comment_user_id(child)
            if user_id == self.user_profile_id:
                return True
        return False

    def count_of_my_comment(self, comments):
        count = 0
        for comment in comments:
            user_id = self.get_comment_user_id(comment)
            if user_id == self.user_profile_id:
                count += 1
        return count

    def action(self, post):
        self.driver.execute_script("window.open();")
        self.driver.switch_to.window(self.driver.window_handles[1])
        if(len(post['href'])<2):
            return False
        self.driver.get(post['href'])

        tumbs = self.driver.find_elements(By.CLASS_NAME, "js_like_link_like")
        for tumb in tumbs:

            if self.item_count == self.item_reset_count:

                self.print_board()

                print('item_count reset fire ....')
                self.driver.close()
                self.driver.switch_to.window(self.BASE_WINDOW)
                self.reset()
                return self.get_score()

            try:
                unlike = tumb.find_element(
                    By.XPATH, "following-sibling::*[1]"
                ).get_attribute('style')
                if unlike == 'display: none;':
                    tumb.click()
                    self.item_count += 1
                    # print(f'*item_{self.item_count}...')
            except Exception as err:
                continue

        self.driver.close()
        self.driver.switch_to.window(self.BASE_WINDOW)

    def click_more_button(self, new_items):
        try:
            if (True):
                self.driver.execute_script("""
                                                btn = document.querySelector("#feed_view_more > a")
                                                isHidden = btn.offsetParent === null
                                                if(! btn || isHidden ){
                                                    return false
                                                }
                                                btn.click()
                                                return true
                                            """)
                time.sleep(3)
        except Exception:
            return None

    def collect_posts(self):

        new = self.driver.find_elements(
            By.CLASS_NAME, "js_feed_view_more_entry_holder")

        for post in tqdm(new):
            ID = post.get_attribute('id')
            if len(self.posts[self.posts['id'] == ID]):

                continue

            href = post.find_element(
                By.CLASS_NAME, 'feed_permalink').get_attribute('href')
            _ = pd.Series({
                "id": ID,
                "element": post,
                "href": href,
                "done": False
            })
            self.posts = self.posts.append(_, ignore_index=True)

            self.action(self.posts.iloc[-1])
            # self.posts.iloc[-1]['done'] = True

        self.print_board()
        if len(new) >= self.max_unsed_post_count and self.item_count <= self.item_reset_count:
            print('reseting ...')
            self.refresh_page()
            self.reset()
            return self.get_score()

        self.click_more_button(new)
        self.scroll_bottom()
        return self.collect_posts()

    def get_score(self):
        try:
            if not self.IS_LOGGED_IN:
                self.auto_login()
            self.set_base_window()
            self.posts = self.init_posts()
            self.collect_posts()
        except Exception:
            return self.get_score()

    def reset(self):
        self.set_base_window()
        self.item_count = 0
        self.posts = self.init_posts()
        self.refresh_page()


if __name__ == '__main__':
    user = input('who? masoud|abbas: ') or 'masoud'
    BASE_URL = input('page_url: https://saha.moi.ir ?') or 'https://saha.moi.ir'
    itemResetCount = input('item_count: ') or 10
    itemResetCount = int(itemResetCount)
    maxUnsedPostCount = input('max_unsed_post_count: ') or 60
    maxUnsedPostCount = int(maxUnsedPostCount)

    if user == 'masoud':
        USERNAME = '1741995108'
        PASSWORD = '4NpzuFqdEyCDv6T'
        user_profile_id = 'profile-42137'
    elif user == 'abbas':
        USERNAME = '1270609726'
        PASSWORD = '093678900450'
        user_profile_id = 'profile-42029'
    else:
        print('wrong user ...')
        exit(1)

    try:
        Action = LikeAction(
            BASE_URL,
            USERNAME,
            PASSWORD,
            itemResetCount,
            maxUnsedPostCount,
            user_profile_id,
            True
        )
        Action.get_score()
    except Exception:
        Action = LikeAction(
            BASE_URL,
            PASSWORD,
            itemResetCount,
            maxUnsedPostCount,
            user_profile_id,
            True
        )
        Action.get_score()
