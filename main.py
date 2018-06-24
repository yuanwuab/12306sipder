#encoding: utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Qiangpiao(object):

    def __init__(self):
        self.login_url = "https://kyfw.12306.cn/otn/login/init"
        self.initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
        self.search_url = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.passenger_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.driver = webdriver.Chrome(executable_path="D:\ProgramApp\chromedriver\chromedriver.exe")


    def wait_input(self):
        self.from_station = input("出发地：")
        self.to_station = input("目的地：")
        # 时间格式必须是：yyyy-MM-dd的方式
        self.depart_time = input("出发时间：")
        self.passengers = input("乘客姓名（如有多个乘客，用英文逗号隔开）：").split(",")
        self.trains = input("车次（如有多个车次，用英文逗号隔开）：").split(",") # ["G485","G529"]


    def _login(self):
        self.driver.get(self.login_url)
        # 显示等待
        # 隐示等待
        WebDriverWait(self.driver,1000).until(
            EC.url_to_be(self.initmy_url)
        )
        print('登录成功！')


    def _order_ticket(self):
        # 1. 跳转到查余票的界面
        self.driver.get(self.search_url)

        # 2. 等待出发地是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"fromStationText"),self.from_station)
        )

        # 3. 等待目的地是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"toStationText"),self.to_station)
        )

        # 4. 等待出发日期是否输入正确
        WebDriverWait(self.driver,1000).until(
            EC.text_to_be_present_in_element_value((By.ID,"train_date"),self.depart_time)
        )

        # 5. 等待查询按钮是否可用
        WebDriverWait(self.driver,1000).until(
            EC.element_to_be_clickable((By.ID,"query_ticket"))
        )

        # 6. 如果能够被点击了，那么就找到这个查询按钮，执行点击事件
        searchBtn = self.driver.find_element_by_id("query_ticket")
        searchBtn.click()

        # 7. 在点击了查询按钮以后，等待车次信息是否显示出来了
        WebDriverWait(self.driver,1000).until(
            EC.presence_of_element_located((By.XPATH,".//tbody[@id='queryLeftTable']/tr"))
        )

        # 8. 找到所有没有datatrain属性的tr标签，这些标签是存储了车次信息的
        tr_list = self.driver.find_elements_by_xpath(".//tbody[@id='queryLeftTable']/tr[not(@datatran)]")
        # 9. 遍历所有满足条件的tr标签
        for tr in tr_list:
            train_number = tr.find_element_by_class_name("number").text
            if train_number in self.trains:
                left_ticket = tr.find_element_by_xpath(".//td[4]").text
                if left_ticket == "有" or left_ticket.isdigit:
                    orderBtn = tr.find_element_by_class_name("btn72")
                    orderBtn.click()

                    # 等待是否来到了确认乘客的页面
                    WebDriverWait(self.driver,1000).until(
                        EC.url_to_be(self.passenger_url)
                    )

                    # 等待所有乘客信息是否被加载进来了
                    WebDriverWait(self.driver,1000).until(
                        EC.presence_of_element_located((By.XPATH,".//ul[@id='normal_passenger_id']/li"))
                    )

                    # 找到所有的乘客的label标签
                    passenger_labels = self.driver.find_elements_by_xpath(".//ul[@id='normal_passenger_id']/li/label")
                    for passenger_label in passenger_labels:
                        name = passenger_label.text
                        if name in self.passengers:
                            passenger_label.click()
                            submitBtn = self.driver.find_element_by_id("submitOrder_id")
                            submitBtn.click()
                            WebDriverWait(self.driver,1000).until(
                                EC.presence_of_element_located((By.CLASS_NAME,"dhtmlx_wins_body_outer"))
                            )
                            WebDriverWait(self.driver,1000).until(
                                EC.presence_of_element_located((By.ID,"qr_submit_id"))
                            )
                            confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                            while confirmBtn:
                                confirmBtn.click()
                                confirmBtn = self.driver.find_element_by_id("qr_submit_id")
                            return

    def run(self):
        self.wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = Qiangpiao()
    spider.run()