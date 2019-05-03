import threading

class Scraper_thread(threading.Thread):
    def __init__(self, func, menu_dict):
        threading.Thread.__init__(self)
        self.func = func
        self.menu_dict = menu_dict

    def run(self):
        ret_dict = self.func()
        self.menu_dict['detailed'] = ret_dict['detailed']
        self.menu_dict['overview'] = ret_dict['overview']

"""
lock = threading.Lock()

class Scraper_thread(threading.Thread):
    def __init__(self, thread_id, func, date, menu_dict):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.func = func
        self.date = date
        self.menu_dict = menu_dict

    def run(self):
        print("thread " + str(self.thread_id) + " is running")
        ret_dict = self.func(self.date)
        lock.acquire()
        self.menu_dict["menus"].append(ret_dict)
        lock.release()
        print("thread " + str(self.thread_id) + " finish")
"""
