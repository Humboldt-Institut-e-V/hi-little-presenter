#!/usr/bin/env python3
# --------------------------------------------------------------------------------------------------------------------------
# Humboldt-Institut's Little Presenter
#
# Copyright 2020 by Humboldt-Institut e.V. (https://www.humboldt-institut.org)
#
# This file is part of Humboldt-Institut's Little Presenter.
#
# Humboldt-Institut's Little Presenter is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Humboldt-Institut's Little Presenter is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with Humboldt-Institut's Little Presenter. If not,
# see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------------------------------------------------------------
from typing import Optional, Awaitable

import tornado.ioloop
import tornado.web
import asyncio
import os
import sys
import glob
import json
import re
import platform
import lib.webuimethods
import os
import signal
import subprocess
import psutil
import time


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def get_from_list(source_list, index, default=None):
    try:
        return source_list[index]
    except IndexError:
        return default


class Presenter:

    def __init__(self):
        self.valid_extensions_list = ['.pdf', '.odp']
        self.presentation_name = 'presentation'
        self.process = None
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.join(self.base_dir, 'data')

    def stop(self):
        if self.process is not None:
            try:
                process = psutil.Process(self.process.pid)
                for child_process in process.children(recursive=True):
                    child_process.kill()
                self.process.kill()
            except:
                pass
        self.process = None
        time.sleep(0.5)

    def present(self):
        duration_per_slide = 20
        # Try LibreOffice presentation
        file_list = glob.glob(os.path.join(self.data_dir, self.presentation_name + '.odp'))
        if len(file_list) > 0:
            file_path = file_list[0]
            if platform.system() == 'Darwin':
                print(file_path)
                return
            elif platform.system() == 'Windows':
                command = ["C:\\Program Files\\LibreOffice\\program\\simpress.exe", "--norestore", "--show" , file_path]
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
                return
            else:
                command = ["soffice", "--norestore", "--show", file_path]
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
                return
        # Try PDF presentation
        file_list = glob.glob(os.path.join(self.data_dir, self.presentation_name + '.pdf'))
        if len(file_list) > 0:
            file_path = file_list[0]
            if platform.system() == 'Darwin':
                print(file_path)
                return
            elif platform.system() == 'Windows':
                print(file_path)
                return
            else:
                command = ["impressive", "-a", str(duration_per_slide), "-w", "-t", "WipeRight", file_path]
                self.process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=False)
                return

    def reboot_system(self):
        if platform.system() == 'Darwin':
            print("Reboot")
        elif platform.system() == 'Windows':
            print("Reboot")
        else:
            # Command for Raspberry Pi
            command = ["sudo", "shutdown", "-r", "1"]
            subprocess.check_output(command, timeout=3)


class BaseHandler(tornado.web.RequestHandler):

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass


class ApiHandler(BaseHandler):

    class STATUS:
        UNKNOWN = "unknown"
        SUCCESS = "success"
        FAILURE = "failure"

    def initialize(self, presenter):
        self.presenter = presenter

    def get(self, command):
        error_list = []
        result = {}
        status = ApiHandler.STATUS.UNKNOWN
        if command == 'restart-presentation':
            self.presenter.stop()
            self.presenter.present()
            status = ApiHandler.STATUS.SUCCESS
        elif command == 'reboot-system':
            self.presenter.reboot_system()
            status = ApiHandler.STATUS.SUCCESS
        else:
            error_list.append("Unknown API call.")
            status = ApiHandler.STATUS.FAILURE
        self.write({'status': status,
                    'result': result,
                    'errors': error_list})


class MainHandler(BaseHandler):

    def initialize(self, presenter):
        self.presenter = presenter

    def prepare(self):
        error_list = []

    def post(self):
        error_list = []
        valid_extensions_list = self.presenter.valid_extensions_list
        presentation_name = self.presenter.presentation_name
        data_dir = self.presenter.data_dir

        file_upload_list = self.request.files.get('presentation_file', None)
        if file_upload_list is not None:
            file_info = get_from_list(file_upload_list, 0, {})
            file_name = file_info.get('filename', '')
            file_extension = get_from_list(os.path.splitext(file_name), 1, '').casefold()

            if file_extension not in valid_extensions_list:
                error_list.append("File is not of a valid file. Please choose a PDF or an ODP document.")
            else:
                self.presenter.stop()
                for valid_extension in valid_extensions_list:
                    file_to_delete = os.path.join(data_dir, presentation_name + valid_extension)
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)
                presentation_file_path = os.path.join(data_dir, presentation_name + file_extension)
                with open(presentation_file_path, 'wb') as f:
                    f.write(file_info.get('body', b''))
                self.presenter.present()
        self.write_page(error_list)

    def get(self):
        self.write_page()

    def write_page(self, error_list=[]):
        self.render("index.html",
                    hostname=str(platform.node()).upper(),
                    error_list=error_list)


def get_configuration():
    configuration = {
        "port": 8080
    }
    return configuration


def make_app():
    settings = {
        "autoreaload": True,
        "template_path": os.path.join(os.path.dirname(__file__), "www", "templates"),
        "static_url_prefix": "/static/",
        "static_path": os.path.join(os.path.dirname(__file__), "www", "static"),
        "ui_methods": lib.webuimethods
    }
    presenter = Presenter()
    presenter.present()
    app = tornado.web.Application([
        (r"/", MainHandler, dict(presenter=presenter)),
        (r"/api/([^/]*)", ApiHandler, dict(presenter=presenter)),
        (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path']))
    ], **settings)
    return app


def main():
    configuration = get_configuration()
    app = make_app()
    app.listen(configuration['port'])
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
