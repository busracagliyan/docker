#!/usr/bin/python3
import json
import os, subprocess
import time

class image:
    def __init__(self,data):
        j = json.loads(data)
        self.name = j["Repository"]
        self.tag = j["Tag"]
        self.size = j["Size"]
        self.id = j["ID"]
        self.created = j["CreatedSince"]

    def create_container(self,name=None,options=""):
        if not name:
            name = str(time.time())
        id = subprocess.getoutput("docker create -it \
           --name '{}' \
           {} \
           '{}'".format(name, options, self.name))
        data = subprocess.getoutput("docker ps -a --format '{{json .}}' | grep "+id[0:12])
        if len(data) == 0 or data[0] != "{":
            return None
        return container(data)

    def remove(self):
        return os.system("docker rmi '{}'".format(self.id))

class container:
    def __init__(self,data):
        j = json.loads(data)
        self.name = j["Names"]
        self.image = j["Image"]
        self.status = j["Status"]
        self.state = j["State"]
        self.size = j["Size"]
        self.id = j["ID"]

    def stop(self):
        return os.system("docker kill '{}'".format(self.id)) == 0

    def start(self):
        return os.system("docker start '{}'".format(self.id)) == 0

    def execute(self,command):
        return os.system("docker exec -it '{}' sh -c '{}' ".format(self.id,command)) == 0

    def remove(self):
        return os.system("docker rm '{}' -f".format(self.id)) == 0

class docker:
    def __init__(self):
        self.available = True
        print(os.system("~/bin/docker --version >/dev/null"))
        if os.system("~/bin/docker --version >/dev/null") != 0:
            self.available = False

    def list_containers(self):
        containers =  []
        t = subprocess.getoutput("docker ps -a --format '{{json .}}'")
        for line in t.split("\n"):
            if len(line) == 0 or line[0] != "{":
                continue
            con = container(line)
            containers.append(con)
        return containers

    def list_images(self):
        images =  []
        t = subprocess.getoutput("docker images -a --format '{{json .}}'")
        for line in t.split("\n"):
            if len(line) == 0 or line[0] != "{":
                continue
            con = image(line)
            images.append(con)
        return images

    def fetch_image(self, name, tag="latest"):
        return os.system("docker pull '{}:{}'".format(name, tag)) == 0
