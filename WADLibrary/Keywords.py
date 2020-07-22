import json
from .Sessions import Sessions
from .common.keys import keys
from .common import execute
import time
import re


class Keywords:
    def __init__(self, path, platform, device_name, timeout):
        self.__sessions = []
        self.__platform = platform
        self.__current_session = None
        self.path = path
        self.device_name = device_name
        self.timeout = timeout
        self.keylist = []
        self.resultlist = []
        

    def set_up(self):
        desired_caps = dict()
        desired_caps["app"] = 'Root'
        desired_caps["platformName"] = self.__platform
        desired_caps["deviceName"] = self.device_name

        execute.post(self.path + '/session/', json={'desiredCapabilities': desired_caps})

        res = execute.get(self.path + '/sessions')
        json_obj = json.loads(res.text)
        for session in json_obj['value']:
            cap = session['capabilities']
            session_id = session['id']
            if 'appTopLevelWindow' in cap:
                app_name = cap['appTopLevelWindow']
            elif 'app' in cap:
                app_name = cap['app']
            session_obj = Sessions(session_id=session_id, name=app_name, desired_caps=cap)
            self.__sessions.append(session_obj)
        ses = self.get_session('Root')
        self.__current_session = ses

    def clean_up(self):
        for_deletion = self.__sessions
        for session in self.__sessions:
            self.delete_session(session.get_id())
        for session in for_deletion:
            self.__sessions.remove(session)

    def clean_up_session(self,name):
        session = self.get_session(name)
        self.delete_session(session.get_id())
        self.__sessions.remove(session)

    def get_sessions(self):
        return self.__sessions

    def get_current_session_id(self):
        return self.__current_session.get_id()

    def get_session_ids(self):
        ids = []
        for session in self.__sessions:
            ids.append(session.get_id())
        return ids

    def get_session(self, name):
        for session in self.__sessions:
            if name == session.get_name():
                return session

    def get_session_by_id(self, session_id):
        for session in self.__sessions:
            if session_id == session.get_id():
                return session
    

    def get_window_handle(self, using, value, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(using=using, value=value, session_id=session_id)
        win = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/attribute/NativeWindowHandle')
        json_obj = json.loads(win.text)
        handle = hex(int(json_obj['value']))
        return handle

    def get_window_title(self, session_id=None):
        """
        Get the title of the window you currently handle. 
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/title')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result

    def attach_to_window(self, value, name, using='name', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        window_handle = self.get_window_handle(using=using, value=value, session_id=session_id)
        desired_caps = dict()
        desired_caps["appTopLevelWindow"] = window_handle
        desired_caps["platformName"] = self.__platform
        desired_caps["deviceName"] = self.device_name
        self.__current_session = self.create_session(desired_caps, name)
        self.get_sessions()
        
    def set_value_table(self, value, using='name', path = '//*', session_id=None):
        """
        You should use it before using keyword 'Click Element Text'.
        Then you can click something you want by text.
        If current window's name is calculator, and you set value = calculator, 
        the all text element in caculator will write in value table.
        It will take additional times to build table.
        """
        if session_id is None:
            session_id = self.get_current_session_id()      
        self.keylist.clear()
        self.resultlist.clear() 
        elem = self.find_element(value=value, using=using, session_id=session_id)
        elems = self.find_elements_by_element(elem=elem, value= path, using='xpath', session_id=session_id)
        self.keylist = [item.get('ELEMENT') for item in elems]
        self.resultlist = [self.get_text(item, session_id=session_id) for item in self.keylist]
            
    def get_value_table_list(self):
        """
        Get the list of the value table.
        """
        return  self.resultlist

    def create_session(self, desired_caps, name):
        res = execute.post(self.path + '/session/', json={'desiredCapabilities': desired_caps})
        json_obj = json.loads(res.text)
        session_id = json_obj['sessionId']
        session_obj = Sessions(session_id=session_id, name=name, desired_caps=desired_caps)
        self.__sessions.append(session_obj)
        return session_obj

    def close_window(self, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        execute.delete(self.path + '/session/' + session_id + '/window')

    def delete_session(self, session_id):
        execute.delete(self.path + '/session/' + session_id)

    def set_current_session(self, name):
        self.__current_session = self.get_session(name)

    def find_element(self, value, using='name', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.post(self.path + '/session/' + session_id + '/element',
                           json={'using': using, 'sessionId': session_id, 'value': value})
        json_obj = json.loads(res.text)
        elem = json_obj['value']['ELEMENT']
        return elem
        
    def find_elements(self, value, using='name', session_id=None):
        """
        You can use it to get an element list you find.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.post(self.path + '/session/' + session_id + '/elements',
                           json={'using': using, 'sessionId': session_id, 'value': value})
        json_obj = json.loads(res.text)
        elem = json_obj['value']
        return elem
        
    def get_element_length(self, value, using='name', session_id=None):
        """
        Get the count of element(s) you find.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.post(self.path + '/session/' + session_id + '/elements',
                           json={'using': using, 'sessionId': session_id, 'value': value})
        json_obj = json.loads(res.text)
        elem = json_obj['value']
        length = len(elem)
        return length
        
    def find_sub_elements_under_parent(self, elem, value, using='xpath', session_id=None):
        """
        You can use it to find all the sub elements under a parent element.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.post(self.path + '/session/' + session_id + '/element/' + elem + '/elements',
                           json={'using': using, 'sessionId': session_id, 'value': value})
        json_obj = json.loads(res.text)
        elems = json_obj['value']    
        return elems
        

    def move_to_element(self, elem, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        execute.post(self.path + '/session/' + session_id + '/moveto', json={'element': elem})

    def mouse_click(self, button='left', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        buttons = {'left': 0, 'middle': 1, 'right': 2}
        execute.post(self.path + '/session/' + session_id + '/click', json={'button': buttons[button]})

    def get_attribute(self, elem, attribute, session_id=None):
        """
        You can get the attribute of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/attribute/' + attribute)
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result
        
    def get_name(self, elem, session_id=None):
        """
        You can get the name of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/attribute' + '/Name')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result

    def is_enabled(self, elem, session_id=None):
        """
        You can get the status of an element you want.
        It will return boolean value, enable status is true, disable status is false.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/enabled')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result
    
    def get_text(self, elem, session_id=None):
        """
        You can get the text of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/text')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result

    def double_click(self, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        execute.post(self.path + '/session/' + session_id + '/doubleclick')

    def double_click_element(self, value, using='name', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        self.move_to_element(elem=elem, session_id=session_id)
        self.double_click(session_id=session_id)

    def click_element(self, value, using='name', way='left', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        if self.is_visible_v2(elem):
            self.move_to_element(elem=elem, session_id=session_id)
            self.mouse_click(button=way, session_id=session_id)
        else:
            ex = Exception(value + " is not visible")
            raise ex
        
    def click_element_text(self, value, location=0, way='left', session_id=None):
        """
        You should use Keyword 'Set Value Table' before use it.
        Then you can click the text exist on current window.
        If the area have the same text not only one, 
        you can set location to click the number of location of the same text elements.(location default value is 0)
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        indexlist = [i for i,v in enumerate(self.resultlist) if v==value]
        if self.is_visible_v2(self.keylist[indexlist[location]]):
            self.move_to_element(elem=self.keylist[indexlist[location]], session_id=session_id)
            self.mouse_click(button=way, session_id=session_id)
        else:
            ex = Exception("The Location " + str(location) + " of "  + value +  + " is not visible")
            raise ex

    def get_element_list(self, value, using='name', session_id=None):
        """
        Get a list of all element you find.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        elems = self.find_elements(value=value, using=using, session_id=session_id)
        elem_list = []
        for item in elems:
            elem_list.append(item.get('ELEMENT'))
        return elem_list
    
    def get_element_selected(self, value, using='name', session_id=None):
        """
        You can use it to get the status of the checkbox.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/selected')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result
            
    def get_element_attribute(self, value, attribute, using='name', session_id=None):
        """
        You can get the attribute of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        result = self.get_attribute(elem=elem, attribute=attribute, session_id=session_id)
        return result

    def get_element_enable(self, value, using='name', session_id=None):
        """
        You can get the status of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        result = self.is_enabled(elem=elem, session_id=session_id)
        return result
        
    def get_element_text(self, value, using='name', session_id=None):
        """
        You can get the text of an element you want.
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(value=value, using=using, session_id=session_id)
        result = self.get_text(elem=elem, session_id=session_id)
        return result
    
    def keyboard_keys(self, value, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        execute.post(self.path + '/session/' + session_id + '/keys', json={'value': list(value)})

    def send_key(self, value, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        key = keys(value)
        execute.post(self.path + '/session/' + session_id + '/keys', json={'value': [key]})

    def enter_value(self, value, locator, using='name', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        elem = self.find_element(locator, using, session_id)
        execute.post(self.path + '/session/' + session_id + '/element/' + elem + '/value',
                     json={'value': list(value)})

    def set_focus(self, session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        session = self.get_session_by_id(session_id)
        caps = session.get_desired_caps()
        if 'appTopLevelWindow' in caps:
            app_name = caps['appTopLevelWindow']
        elif 'app' in caps:
            app_name = caps['app']
        json_obj = {'name': app_name}
        execute.post(self.path + '/session/' + session_id + '/window', json=json_obj)
        

#######################################################################################################################
# Waiting functions
#######################################################################################################################

    def is_visible(self, value, using='name', session_id=None):
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.post(self.path + '/session/' + session_id + '/element',
                           json={'using': using, 'sessionId': session_id, 'value': value},
                           catch_error=False)
        json_obj = json.loads(res.text)
        if json_obj['status'] == 0:
            return True
        elif json_obj['status'] == 7:
            return False
        else:
            execute.analyse(res, catch_error=True)
            
    def is_visible_v2(self, elem, session_id=None):
        """
        If element you can see on the current window, the result will return true. 
        """
        if session_id is None:
            session_id = self.get_current_session_id()
        res = execute.get(self.path + '/session/' + session_id + '/element/' + elem + '/displayed')
        json_obj = json.loads(res.text)
        result = json_obj['value']
        return result

    def wait_until_element_is_visible(self, locator, using='name', timeout=None, error=None, session_id=None):
        if timeout is None:
            timeout = self.timeout

        def check_visibility():
            visible = self.is_visible(locator, using, session_id)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (
                                locator, self.timeout)
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self.timeout)

        self.wait_until_no_error(int(timeout), check_visibility)

    def wait_until_element_is_not_visible(self, locator, using='name', timeout=None, error=None, session_id=None):
        if timeout is None:
            timeout = self.timeout

        def check_visibility():
            visible = self.is_visible(locator, using, session_id)
            if visible:
                return error or "Element '%s' is still visible in %s" % (locator, self.timeout)
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (
                                locator, self.timeout)
            else:
                return

        self.wait_until_no_error(int(timeout), check_visibility)

    def wait_until(self, timeout, error, func, *args):
        error = error.replace('<TIMEOUT>', self.timeout)

        def wait_func():
            return None if func(*args) else error

        self.wait_until_no_error(timeout, wait_func)

    def wait_until_no_error(self, timeout, wait_func, *args):
        timeout = self.timeout if timeout is None else timeout
        max_time = time.time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return
            if time.time() > max_time:
                raise AssertionError(timeout_error)
            time.sleep(0.1)
